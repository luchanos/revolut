import logging
import sys

from marshmallow import ValidationError
from sanic.views import HTTPMethodView

from revolut_api.decorators import check_auth
from revolut_api.methods.response_funcs import create_response
from revolut_api.schemas.base import OutputSchema
from revolut_api.schemas.nested_json_schemas import JsonNestedRequestSchema


logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")


class NestedJsonHandler(HTTPMethodView):
    decorators = [check_auth]
    input_schema = JsonNestedRequestSchema()
    output_schema = OutputSchema()

    @staticmethod
    def make_nested_json(sample_input, *args):
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

    async def post(self, request):
        try:
            data = self.input_schema.load(request.json)
        except ValidationError as err:
            err_msg = "Error due to validation of input data in request: %s" % (err,)
            logger.error(err_msg)
            return create_response(result=[], status_code=422, error=err)
        result = self.make_nested_json(data["json_data"], *data["keys_priority"])
        return create_response(result)
