from aiohttp import web
from aiohttp_apispec import docs, response_schema, querystring_schema

from api_smart_link.entities.requests import RequestPage
from api_smart_link.entities.responses import ResponseInternalError, ResponseSuccessData, ResponseSuccess
from api_smart_link.log_manager import log_manager

LOGGER = log_manager.get_logger(module_name=__name__)


class PagesHandler(web.View):
    @docs(tags=['Settings'],
          summary='Get settings [Auth required]',
          description='''Get settings for frontend''')
    @querystring_schema(RequestPage.Schema())
    @response_schema(ResponseSuccessData.Schema(), 200, description="Settings", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    async def get(self):
        result = ResponseSuccessData(data=ResponseSuccess(True, "Okay"))
        payload = result.make_dump()
        return web.json_response(payload)
