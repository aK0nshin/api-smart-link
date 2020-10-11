from dataclasses import field, dataclass
from typing import Optional

from marshmallow.validate import Regexp
from marshmallow_dataclass import add_schema

from api_smart_link.entities import Base, BaseEntity
from api_smart_link.enums import OrderDirEnum


@add_schema(base_schema=Base)
@dataclass
class RequestPageById(BaseEntity):
    id: int = field()


@add_schema(base_schema=Base)
@dataclass
class RequestPageByEndpoint(BaseEntity):
    endpoint: str = field()


@add_schema(base_schema=Base)
@dataclass
class RequestUser(BaseEntity):
    user_id: int = field()


@add_schema(base_schema=Base)
@dataclass
class RequestUserPage(BaseEntity):
    user_id: int = field()
    page_id: int = field()


@add_schema(base_schema=Base)
@dataclass
class RequestUserPagesList(RequestUser):
    offset: Optional[int] = field(default=0, metadata=dict(description="Смещение возвращаемых записей", example=0))
    order: Optional[OrderDirEnum] = field(
        default=OrderDirEnum.asc,
        metadata=dict(description="Сортировка записей. Возможные значения: {}".format([k.name for k in OrderDirEnum]),
                      default=OrderDirEnum.asc, example=OrderDirEnum.asc.name))
    limit: Optional[int] = field(default=100, metadata=dict(description="Количество возвращаемых записей", example=100))


@add_schema(base_schema=Base)
@dataclass
class RequestUserPagePost(RequestUser):
    content: dict = field(metadata=dict(description="Контент создаваемой страницы", example={}))
    endpoint: Optional[str] = field(metadata=dict(description="Название ресурса (хеш) в адресе страницы", example={},
                                                  validate=Regexp(r"^[-_0-9a-zA-Z]{1,128}$")))


@add_schema(base_schema=Base)
@dataclass
class RequestUserPagePut(RequestUserPage):
    content: Optional[dict] = field(metadata=dict(description="Контент создаваемой страницы", example={}))
    endpoint: Optional[str] = field(metadata=dict(description="Название ресурса (хеш) в адресе страницы", example={},
                                                  validate=Regexp(r"^[-_0-9a-zA-Z]{1,128}$")))
