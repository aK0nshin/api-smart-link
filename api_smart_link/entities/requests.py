from dataclasses import field, dataclass

from marshmallow_dataclass import add_schema

from api_smart_link.entities import Base, BaseEntity


@add_schema(base_schema=Base)
@dataclass
class RequestPage(BaseEntity):
    id: int = field()
