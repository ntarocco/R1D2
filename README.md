# R1D2
A robot that extracts the menus of the CERN restaurants (R1, R2, R3) for you.


## API
`GET`-only API using [Flask](http://flask.pocoo.org). There are three types of
commands that can be composed to query the menu.

Specify the date
```
/week
/today
/tomorrow
/monday
/…
/friday
```

Specify the restaurant
```
/r1
/r2
/r3
```

Specify the type of dish
```
/menu1
/menu2
/menu3
/vegetarian
/speciality
/grill
/pasta
/pizza
```

Please note that due to the super simple way this API is implemented the order
of the parameters does not matter but using two mutually exclusive parameters
together will result in an empty menu.

The server uses `shelve` to store the menu on the server and thus reduce the
number of times the data needs to be extracted from the Novae website.
