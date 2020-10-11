from functools import wraps

from aiohttp import web, hdrs
from aiohttp.web import json_response
from aiohttp.web_response import StreamResponse

from api_smart_link.entities import BaseEntity
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


class JsonHandler(web.View):
    async def _iter(self) -> StreamResponse:
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        payload = await method()
        if isinstance(payload, BaseEntity):
            resp = payload.make_dump()
            return web.json_response(resp)
        return payload
