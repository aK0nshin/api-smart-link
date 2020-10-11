from sqlalchemy import select

from api_smart_link.database.connection import db
from api_smart_link.database.tables import users
from api_smart_link.entities.requests import RequestUser
from api_smart_link.entities.responses import ResponseInternalError, ResponseUserData, ResponseUser
from api_smart_link.handlers import abort


async def get_user_by_id(query_params: RequestUser) -> ResponseUserData:
    model = await db.fetch_one(
        select([users.c.id, users.c.name, users.c.email]).where(users.c.id == query_params.user_id))
    if not model:
        return abort(ResponseInternalError(error="User with this identifier not found"), status=404)
    return ResponseUserData(data=ResponseUser(*model))
