from marshmallow import Schema, ValidationError, fields, validates
from marshmallow.fields import Dict, Str


class JsonNestedRequestSchema(Schema):
    json_data = fields.List(Dict, required=True)
    keys_priority = fields.List(Str, required=True, allow_none=False)

    @validates("json_data")
    def validate_json_data_keys(self, json_data):
        if not json_data:
            raise ValidationError("json_data field cannot be empty for that method!")
        init_keys = set(json_data[0].keys())
        for d in json_data:
            if set(d.keys()) != init_keys:
                raise ValidationError("Keys in different dictionaries must be the same!")

    @validates("keys_priority")
    def validate_keys_priority(self, keys_priority):
        if not keys_priority:
            raise ValidationError("keys_priority field cannot be empty for that method!")
