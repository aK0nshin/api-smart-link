from aiohttp import web
from api_smart_link.apispec import validation_middleware, setup_app_apispec

from api_smart_link.log_manager import log_manager
from api_smart_link.middlewares import internal_error_middleware, validation_error_middleware
from api_smart_link.routes import routes
from api_smart_link.settings import storage

LOGGER = log_manager.get_logger(module_name=__name__)


def parse_routes(app: web.Application, params: dict):
    for route in params:
        app.router.add_route(route[0], route[1], route[2], name=route[3])


def make_app(app):
    parse_routes(app, routes)
    setup_app_apispec(app=app, title="API documentation", version="v1",
                      request_data_name='validated_data', swagger_path='/api/doc',
                      static_path="/api/static/swagger")
    app.middlewares.extend([validation_error_middleware, internal_error_middleware, validation_middleware])
    return app


def run(cron_task=None):
    if cron_task is not None:
        if not isinstance(cron_task, list):
            cron_task = [cron_task]
        for task in cron_task:
            task.start()
    app = web.Application()
    make_app(app)
    web.run_app(app, host=storage.config.listen_host, port=storage.config.listen_port)
