from databases import Database

from api_smart_link.settings import build_config

build_config()


def get_pool():
    database = Database('postgresql://localhost:5432/smart_link?user=postgres&password=postgres&min_size=5&max_size=20')
    return database


# def get_sync_pool():
#     return PostgresqlDatabase(
#         storage.config.db_name,
#         user=storage.config.db_user,
#         password=storage.config.db_password,
#         host=storage.config.db_host,
#        port=storage.config.db_port,
#     )


def get_manager(pool_):
    manager_ = Manager(pool_)
    manager_.database.set_allow_sync(False)
    return manager_


pool = get_pool()
sync_pool = get_sync_pool()
manager = get_manager(pool)
