from sanic import Sanic
from sanic.exceptions import Unauthorized
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_jwt import Initialize
from sanic_jwt.decorators import protected


async def authenticate(request, *args, **kwargs):
    return {}

app = Sanic("revolut_application")
Initialize(app, authenticate=authenticate)


def check_auth(f):
    def inner(request, *args, **kwargs):
        token = request.headers.get('X-TOKEN')
        if token is None:
            raise Unauthorized
        return f(request, *args, **kwargs)
    return inner


class JsonNestedMethod(HTTPMethodView):
    decorators = [check_auth]

    async def post(self, request):
        data = request.json
        args = data['keys_priority']
        sample_input = data['json_data']
        result = {}
        _len = len(args)
        keys = sample_input[0].keys()
        # оставшиеся ключи
        other = {x for x in keys if x not in {*args}}  # множество работает быстрее
        for row in sample_input:
            cur = result
            for arg_i in range(_len):
                arg = args[arg_i]
                cur = cur.setdefault(row[arg], {} if arg_i != _len - 1 else [])
            cur.append({key: row[key] for key in other})
        return json({"success": True, "result": result})


app.add_route(JsonNestedMethod.as_view(), '/make_nested_json')


if __name__ == "__main__":
    app.run()
