import re
import typing

from marshmallow import Schema, post_dump, fields, ValidationError
from marshmallow.validate import Validator
from marshmallow_dataclass import NewType


class Base(Schema):
    missing_fields = []

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if self._validate_none_fields(key, value)
        }

    def _validate_none_fields(self, key, value):
        if value is not None or key not in self._get_none_fields():
            return True

    def _get_none_fields(self):
        missing_fields = []
        for k, v in self.fields.items():
            if not v.required:
                missing_fields.append(k)
        return missing_fields


class BaseEntity:
    def make_dump(self):
        return self.Schema().dump(self)

    @staticmethod
    def Schema():
        pass


class ImageValidator(Validator):
    invalid_content_type = "Doesn't have a valid content type, matching {regex}"
    invalid_filename = "Doesn't have a valid filename, matching {regex}"
    file_is_empty = "Size of the file is {size}"

    content_type_regex = re.compile(r"image/*")
    filename_regex = re.compile(r"^.*\.(jpeg|jpg|gif|png)$")

    def __call__(self, value) -> typing.Any:
        if not hasattr(value, 'content_type') or self.content_type_regex.match(value.content_type) is None:
            raise ValidationError(self.invalid_content_type.format(regex=self.content_type_regex.pattern))

        if not hasattr(value, 'filename') or self.filename_regex.match(value.filename) is None:
            raise ValidationError(self.invalid_filename.format(regex=self.filename_regex.pattern))

        if not (peek := value.file.peek()):
            raise ValidationError(self.file_is_empty.format(size=len(peek)))

        return value


ImageType = NewType("ImageType", str, field=fields.Raw, validate=ImageValidator())
