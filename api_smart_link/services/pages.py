from sqlalchemy import select, func, desc, and_

from api_smart_link.database.connection import db
from api_smart_link.database.tables import pages, users
from api_smart_link.entities.requests import RequestPageByEndpoint, RequestUserPagesList, RequestUserPage, \
    RequestUserPagePost, RequestUserPagePut
from api_smart_link.entities.responses import ResponsePageData, ResponsePage, ResponseInternalError, \
    ResponsePageListData
from api_smart_link.enums import OrderDirEnum
from api_smart_link.handlers import abort
from api_smart_link.log_manager import log_manager
from api_smart_link.services.hashing import hash_endpoint, increment_hash

LOGGER = log_manager.get_logger(module_name=__name__)


async def get_page_by_endpoint(query_params: RequestPageByEndpoint) -> ResponsePageData:
    page = await db.fetch_one(
        select([pages.c.id, pages.c.content]).where(pages.c.endpoint == query_params.endpoint))
    if not page:
        return abort(ResponseInternalError(error="Page with this identifier not found"), status=404)
    return ResponsePageData(data=ResponsePage(*page))


async def get_user_pages_list(query_params: RequestUserPagesList) -> ResponsePageListData:
    user_pages = []
    q = select([pages.c.id, pages.c.content]).select_from(pages.join(users)).where(users.c.id == query_params.user_id)

    total = await db.fetch_val(q.with_only_columns([func.count(pages.c.id)]))
    if total:
        user_pages = await db.fetch_all(q.limit(query_params.limit).offset(query_params.offset).order_by(
            pages.c.id if query_params.order == OrderDirEnum.asc else desc(pages.c.id)))

    return ResponsePageListData(data=[ResponsePage(*x) for x in user_pages], limit=query_params.limit,
                                offset=query_params.offset, total=total)


async def get_user_page(query_params: RequestUserPage) -> ResponsePageData:
    model = await db.fetch_one(
        select([pages.c.id, pages.c.content]).select_from(pages.join(users)).where(
            and_(users.c.id == query_params.user_id, pages.c.id == query_params.page_id)))
    if not model:
        return abort(ResponseInternalError(error="Page with this identifier not found"), status=404)
    return ResponsePageData(data=ResponsePage(*model))


async def put_user_page(query_params: RequestUserPagePut) -> ResponsePageData:
    values = {}
    if query_params.content is not None:
        values['content'] = query_params.content
    if query_params.endpoint is not None:
        values['endpoint'] = query_params.endpoint

    if not values:
        return abort(ResponseInternalError(error="No data provided to update"), status=400)

    await db.execute(pages.update().values(**values).where(pages.c.id == query_params.page_id))

    model = await db.fetch_one(select([pages.c.id, pages.c.content]).where(pages.c.id == query_params.page_id))
    if not model:
        return abort(ResponseInternalError(error="Page with this identifier not found"), status=404)
    return ResponsePageData(data=ResponsePage(*model))


async def post_user_page(query_params: RequestUserPagePost) -> ResponsePageData:
    user = await db.fetch_one(users.select().where(users.c.id == query_params.user_id))
    if not user:
        return abort(ResponseInternalError(error="User with this identifier not found"), status=404)

    if query_params.endpoint:
        check_endpoint = await db.fetch_val(
            query=select([func.count(pages.c.id)]).where(pages.c.endpoint == query_params.endpoint))
        if check_endpoint:
            return abort(ResponseInternalError(error="This endpoint already exists"), status=400)
    else:
        query_params.endpoint = hash_endpoint(user.email)
        while await db.fetch_val(
                query=select([func.count(pages.c.id)]).where(pages.c.endpoint == query_params.endpoint).as_scalar()):
            query_params.endpoint = increment_hash(query_params.endpoint)

    new_page_id = await db.fetch_val(
        pages.insert().values(user_id=user.id, content=query_params.content, endpoint=query_params.endpoint))

    model = await db.fetch_one(select([pages.c.id, pages.c.content]).where(pages.c.id == new_page_id))
    return ResponsePageData(data=ResponsePage(*model))
