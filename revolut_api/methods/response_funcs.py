from sanic.response import json

from revolut_api.schemas.base import OutputSchema


def create_response(result, status_code=200, error=None):
    schema = OutputSchema()
    success = True if not error else False
    response_data = {
        "success": success,
        "result": {"errors": str(error), "payload": result},
        "status": status_code,
    }
    return json(schema.dump(response_data), status=status_code)
