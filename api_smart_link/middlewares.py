from json import JSONDecodeError

from aiohttp import web
from marshmallow import ValidationError

from api_smart_link.log_manager import log_manager

LOGGER = log_manager.get_logger(module_name=__name__)


@web.middleware
async def internal_error_middleware(request, handler):
    try:
        return await handler(request)
    # except (peewee.OperationalError, peewee.ProgrammingError, JSONDecodeError) as exc:
    except JSONDecodeError as exc:
        resp = web.json_response({"error": "Error: {}. Desc: {}".format(type(exc), str(exc))}, status=400)
        return resp


@web.middleware
async def validation_error_middleware(request, handler):
    try:
        return await handler(request)
    except ValidationError as err:
        LOGGER.error('\n'.join(err.messages))
        return web.json_response({"error": err.messages}, status=400)
