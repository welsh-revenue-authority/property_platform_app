# Property platform poc

A POC for [a property data platform](https://land-property-platform.herokuapp.com/).

## Getting started

### Requirements

* Python

### Set up

This app connects to a database on heroku. You need to add the database details to a `.env` file. Set these vars
```
HEROKU_PGDATABASE=
HEROKU_PGHOST=
HEROKU_PGPASSWORD=
HEROKU_PGUSERNAME=
```

We recommend working in a virtual environment.

Install the python dependencies
```
pip install -r requirements.txt
```


### Run the app

Run the app with
```
uvicorn main:app --reload
```

## Documentations

Read the documentation [here](https://welsh-revenue-authority.github.io/property_platform_app/)

