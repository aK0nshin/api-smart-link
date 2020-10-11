from aiohttp_apispec import docs, response_schema, querystring_schema, match_info_schema, request_schema

from api_smart_link.entities.requests import RequestPageByEndpoint, RequestUser, RequestUserPagesList, RequestUserPage, \
    RequestUserPagePost, RequestUserPagePut
from api_smart_link.entities.responses import ResponseInternalError, ResponseSuccessData, ResponseSuccess, \
    ResponsePageData, ResponseUserData, ResponsePageListData
from api_smart_link.handlers import JsonHandler, abortable
from api_smart_link.log_manager import log_manager
from api_smart_link.services.pages import get_page_by_endpoint, get_user_pages_list, get_user_page, post_user_page, \
    put_user_page
from api_smart_link.services.users import get_user_by_id

LOGGER = log_manager.get_logger(module_name=__name__)


class PagesByEndpointHandler(JsonHandler):
    @docs(tags=['Pages'],
          summary='Get page by endpoint',
          description='''Get page object''')
    @match_info_schema(RequestPageByEndpoint.Schema())
    @response_schema(ResponsePageData.Schema(), 200, description="Page object in data", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    @response_schema(ResponseInternalError.Schema(), 404, description="Error description", required=True)
    @abortable
    async def get(self):
        query_params = self.request['validated_data']
        result = await get_page_by_endpoint(query_params)
        return result


class UsersHandler(JsonHandler):
    @docs(tags=['Users'],
          summary='Get user by id',
          description='''Get user object''')
    @match_info_schema(RequestUser.Schema())
    @response_schema(ResponseUserData.Schema(), 200, description="User object in data", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    @response_schema(ResponseInternalError.Schema(), 404, description="Error description", required=True)
    @abortable
    async def get(self):
        query_params = self.request['validated_data']
        result = await get_user_by_id(query_params)
        return result


class UsersPagesListHandler(JsonHandler):
    @docs(tags=['Pages'],
          summary='Get pages of certain user',
          description='''Get list of pages objects''')
    @request_schema(RequestUserPagesList.Schema(), locations=["match_info", "querystring"])
    @response_schema(ResponsePageListData.Schema(), 200, description="List of pages in data", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    @abortable
    async def get(self):
        query_params = self.request['validated_data']
        result = await get_user_pages_list(query_params)
        return result

    @docs(tags=['Pages'],
          summary='Create single user page',
          description='''Create single page''')
    @request_schema(RequestUserPagePost.Schema(), locations=["match_info", "json"])
    @response_schema(ResponsePageData.Schema(), 200, description="Page object in data", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    @response_schema(ResponseInternalError.Schema(), 404, description="Error description", required=True)
    @abortable
    async def post(self):
        query_params = self.request['validated_data']
        result = await post_user_page(query_params)
        return result


class UsersPagesHandler(JsonHandler):
    @docs(tags=['Pages'],
          summary='Get single user page by id',
          description='''Get single page by id''')
    @match_info_schema(RequestUserPage.Schema())
    @response_schema(ResponsePageData.Schema(), 200, description="Page object in data", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    @response_schema(ResponseInternalError.Schema(), 404, description="Error description", required=True)
    @abortable
    async def get(self):
        query_params = self.request['validated_data']
        result = await get_user_page(query_params)
        return result

    @docs(tags=['Pages'],
          summary='Update user page by id',
          description='''Update page by id''')
    @request_schema(RequestUserPagePut.Schema(), locations=["match_info", "json"])
    @response_schema(ResponsePageData.Schema(), 200, description="Page object in data", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    @response_schema(ResponseInternalError.Schema(), 404, description="Error description", required=True)
    @abortable
    async def put(self):
        query_params = self.request['validated_data']
        result = await put_user_page(query_params)
        return result
