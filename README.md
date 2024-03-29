# Property platform poc

A POC for [a property data platform](https://landplatform-fastapi-dev.azurewebsites.net/).

And the [platform API documentation](https://landplatform-fastapi-dev.azurewebsites.net/docs).

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
make init
```


### Run the app

Run the app with
```
make run
```

## Documentations

Read the documentation [here](https://welsh-revenue-authority.github.io/property_platform_app/)

## Command line tools

There are bulk data load scripts in `cli.py`. They are intended to be run on developer's machine or a VM.

