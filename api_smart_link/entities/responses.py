from dataclasses import field, dataclass
from typing import Optional

from marshmallow_dataclass import add_schema

from api_smart_link.entities import Base, BaseEntity


# Don't use word 'schema' in naming.


@add_schema(base_schema=Base)
@dataclass
class ResponseInternalError(BaseEntity):
    error: str = field(metadata=dict(description="Error description", example="Everything is bad"))


@add_schema(base_schema=Base)
@dataclass
class ResponseSuccess(BaseEntity):
    success: bool = field(metadata=dict(description="Success status", example=True))
    message: Optional[str] = field(metadata=dict(description="Explanatory message", example="Everything is okay"))


@add_schema(base_schema=Base)
@dataclass
class ResponseSuccessData(BaseEntity):
    data: ResponseSuccess = field()
