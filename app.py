import atexit
from datetime import datetime, timedelta
from os import getenv

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify, request
from flask_cors import cross_origin

from bot import RestaurantBot
from cache import MemoryCache
import r1
from r1.filter import filter_menu, make_filter
from r1.helpers import threaded

TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
CACHE_TIME = timedelta(hours=2)


def get_menu():
    if 'menu' not in cache:
        _get_full_menu()

    _refresh_menu()

    return cache.get('menu')


@threaded
def _refresh_menu():
    if _cache_expired():
        print("cache expired")
        _get_full_menu()
    else:
        print("cache still valid")


def _cache_expired():
    return 'last_fetched' not in cache or datetime.now() - cache.get('last_fetched') > CACHE_TIME


def _get_full_menu():
    cache.set('menu', r1.get_full_menu())
    cache.set('last_fetched', datetime.now())


bot = RestaurantBot(get_menu)
bot.add_menu_action('r1', ['r1', 'today'])
bot.add_menu_action('r2', ['r2', 'today'])
bot.add_menu_action('r3', ['r3', 'today'])
bot.add_menu_action('today', ['today'])
bot.add_menu_action('tomorrow', ['tomorrow'])
bot.add_menu_action('vegetarian', ['vegetarian', 'today'])

app = Flask(__name__)
cache = MemoryCache()


def refresh():
    print("/refresh called")
    _get_full_menu()


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=refresh,
    trigger=IntervalTrigger(hours=1),
    id='refresh_job',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/telegram/{}/'.format(TELEGRAM_BOT_TOKEN), methods=['POST'])
def handle_telegram():
    resp = bot.respond(request.json)
    if resp is None:
        return 'OK'
    return jsonify(resp)


@app.route('/<path:path>')
@cross_origin()
def json_menu(path):
    filter_ = make_filter(path.split('/'))
    menu = filter_menu(get_menu(), filter_)
    return jsonify(menu=r1.serialize_menu(menu))


@app.route('/')
def index():
    return json_menu('today')


if __name__ == "__main__":
    app.run()
