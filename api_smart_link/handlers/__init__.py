from functools import wraps

from aiohttp.web import json_response

from api_smart_link.log_manager import log_manager

LOGGER = log_manager.get_logger(module_name=__name__)


class ReturnErrorException(Exception):
    """Эксепшен для быстрого возвращения из вложенных контекстов"""

    def __init__(self, payload, status=200):
        self.payload = payload
        self.status = status
        super().__init__()


def abortable(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ReturnErrorException as err:
            payload = err.payload.make_dump()
            return json_response(payload, status=err.status)

    return wrapper


def abort(payload, status=200):
    raise ReturnErrorException(payload=payload, status=status)
