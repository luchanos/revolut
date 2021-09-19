from sanic import Sanic
from sanic.exceptions import Unauthorized
from sanic.response import json

from revolut_api.handlers.nested_json import NestedJsonHandler


def register_errors(app: Sanic):
    @app.exception(Unauthorized)
    def _(request, exception: Unauthorized):
        return json({"success": False, "errors": [str(exception)]}, status=exception.status_code)


def create_app():
    from uuid import uuid4

    app = Sanic(f"revolut_application_{uuid4()}")
    app.add_route(NestedJsonHandler.as_view(), "/make_nested_json")
    register_errors(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
