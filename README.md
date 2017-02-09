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

# Next steps

Not much here besides the admin interface to the data model. We'll need a few things:

1. A wireframe of what we'd like the site to look like.
2. The client side of things, matching the wireframe.
3. Some initial data to work with (the data from Virginia seems like a good place to start)
