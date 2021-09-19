import pytest
from sanic import response
from sanic.websocket import WebSocketProtocol

from revolut_api.app import create_app


@pytest.yield_fixture
def app():
    app = create_app()

    @app.route("/test_get", methods=["GET"])
    async def test_get(request):
        return response.json({"GET": True})

    @app.route("/test_post", methods=["POST"])
    async def test_post(request):
        return response.json({"POST": True})

    yield app


@pytest.fixture()
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app, protocol=WebSocketProtocol))
