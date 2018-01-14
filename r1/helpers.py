import datetime as dt
import itertools as it
from threading import Thread


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return it.zip_longest(*args, fillvalue=fillvalue)


def today():
    return dt.date.today()


def first_day_of_this_week():
    t = today()
    return t - dt.timedelta(days=t.weekday())


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper