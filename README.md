# prograces
A project for compiling and tracking political contests for progressive purposes

# Getting started

This project uses Python 3, so adjust your interpreters accordingly. The backend is PostgreSQL. So far the dependencies of this project are `django` and `psycopg2`. You will also need the `postgresql-dev` package (appropriate for your version of PostgreSQL) in order to build `psycopg2`.

To get started, check out this repo and do
```
pip3 install -r requirements.txt
python3 manage.py migrate
```

This will install the requirements and build the database schema. Next, create an admin superuser:

```
python3 manage.py createsuperuser
```

To run the test server, do:

```
python3 manage.py runserver
```
and see the admin interface at `localhost:8000/admin`.

# Importing data

You can now import data into the DB. Make sure you have the latest PostGIS extension to PostgreSQL, or you'll get errors. You may have to drop into the `psql` shell and do `CREATE EXTENSION postgis;` although the migrations should take care of that for you.

Migrate to the latest schema changes via `python3 manage.py migrate`. Then, load some data:
```
python3 manage.py init_pres_candidates
python3 ./manage.py import_state_races VA upper data/election_statewide_results.ods data/state_geojson/VA/va_senate.json
python3 ./manage.py import_state_races VA lower data/election_statewide_results.ods data/state_geojson/VA/va_house.json
```

Currently only data for Virginia is available for loading, although the general scheme of slurping electoral data from the spreadsheet should be similar for all states. This should run for a few minutes and tell you about each district that it's importing.

# Next steps

Not much here besides the admin interface to the data model. We'll need a few things:

1. A wireframe of what we'd like the site to look like.
2. The client side of things, matching the wireframe.
3. Creating a REST API to supply data to the frontend.
