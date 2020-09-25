from databases import Database, DatabaseURL

from api_smart_link.settings import build_config, storage

build_config()


def get_url():
    return DatabaseURL(storage.config.db_url)


def get_pool():
    database = Database(get_url())
    return database


async def connect_db(app):
    await db.connect()


async def disconnect_db(app):
    await db.disconnect()


db = get_pool()
