Smart Link (API)
================

Beautiful small page manager.

Quick Run
---------
```bash
cd api-smart-link
poetry install
# if you are using direnv
cp .env.example .env
direnv allow
```

For local development we recommend using [direnv](https://direnv.net/)
Configure .env file or set OS environments:

* **LISTEN_PORT** - Port, that app will listen
* **LISTEN_HOST** - Host, that app will listen

* **DB_NAME** - Database name
* **DB_MAX_CON** - Max database connection for poll
* **DB_USER** - Database user name
* **DB_PASSWORD** - Password for database user
* **DB_HOST** - Host for DB instance
* **DB_PORT** - Database port
* **LOG_LEVEL** - App's default log level

Commands
---------
1. Run server

    ```bash
    api-smart-link-ctl server run
    ```
