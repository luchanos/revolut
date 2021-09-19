from marshmallow.fields import Dict, Str
from sanic import Sanic
from sanic.exceptions import Unauthorized
from sanic.response import json
from sanic.views import HTTPMethodView
from expiringdict import ExpiringDict
from marshmallow import Schema, fields, ValidationError, validates
import logging
import sys

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")


app = Sanic("revolut_application")
cache = ExpiringDict(max_len=1000, max_age_seconds=3600)


def check_auth(f):
    def inner(request, *args, **kwargs):
        token = request.headers.get('X-TOKEN')
        if token is None:
            logger.info("Attemption to use route without auth")
            raise Unauthorized("No token!")
        return f(request, *args, **kwargs)
    return inner


async def make_nested_json(sample_input, *args):
    result = {}
    _len = len(args)
    keys = sample_input[0].keys()
    # other keys
    other = {x for x in keys if x not in {*args}}  # set in better for searching
    for row in sample_input:
        cur = result
        for arg_i in range(_len):
            arg = args[arg_i]
            cur = cur.setdefault(row[arg], {} if arg_i != _len - 1 else [])
        cur.append({key: row[key] for key in other})
    return result


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


class ResultSchema(Schema):
    payload = fields.Dict(required=False, default={})
    errors = fields.Str(required=False, default=None)


class OutputSchema(Schema):
    success = fields.Bool(required=True, allow_none=False)
    result = fields.Nested(ResultSchema, required=True)
    status = fields.Int(required=True, default=200)


def create_response(result, status_code=200, error=None):
    schema = OutputSchema()
    success = True if not error else False
    response_data = {"success": success, "result": {"errors": str(error), "payload": result}, "status": status_code}
    return json(schema.dump(response_data))


class JsonNestedMethod(HTTPMethodView):
    decorators = [check_auth]
    input_schema = JsonNestedRequestSchema()
    output_schema = OutputSchema()

    async def post(self, request):
        try:
            data = self.input_schema.load(request.json)
        except ValidationError as err:
            err_msg = "Error due to validation of input data in request: %s" % (err, )
            logger.error(err_msg)
            return create_response(result=[], status_code=422, error=err)
        result = await make_nested_json(data["json_data"], *data["keys_priority"])
        return create_response(result)


app.add_route(JsonNestedMethod.as_view(), '/make_nested_json')


if __name__ == "__main__":
    app.run()
