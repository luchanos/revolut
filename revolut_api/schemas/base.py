from marshmallow import Schema, fields


class ResultSchema(Schema):
    payload = fields.Dict(required=False, default={})
    errors = fields.Str(required=False, default=None)


class OutputSchema(Schema):
    success = fields.Bool(required=True, allow_none=False)
    result = fields.Nested(ResultSchema, required=True)
    status = fields.Int(required=True, default=200)
