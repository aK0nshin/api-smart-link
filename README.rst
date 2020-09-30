Smart Link (API)
================

Beautiful small page manager.

Quick Run
---------

::

    $ cd api-smart-link
    $ poetry install
    $ cp .env.example .env
    # if you are using direnv
    $ direnv allow


For local development we recommend using [direnv](https://direnv.net/)
Configure .env file or set OS environments:

* **LISTEN_PORT** - Port, that app will listen
* **LISTEN_HOST** - Host, that app will listen

* **DB_URL** - Database name
* **LOG_LEVEL** - App's default log level

Commands
---------
1. Run server

::

    $ api-smart-link-ctl server run

2. Migrations

Create revision::

    $ alembic revision -m "Migration name" --autogenerate

Run migrations::

    alembic upgrade head
