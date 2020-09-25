from aiohttp import web

from api_smart_link.settings import represent_conf
from api_smart_link.log_manager import log_manager

LOGGER = log_manager.get_logger(module_name=__name__)


class HealthHandler(web.View):
    async def get(self):
        return web.json_response(dict(data=represent_conf()))
