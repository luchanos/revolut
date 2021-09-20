import logging
import sys

from envparse import Env
from sanic.exceptions import Unauthorized


logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

env = Env()
TEST_MODE = env.bool("TEST_MODE", default=False)
SERVICE_TOKEN = env.str("SERVICE_TOKEN") if not TEST_MODE else "test_token"


def check_auth(f):
    def inner(request, *args, **kwargs):
        token = request.headers.get("X-TOKEN")
        if SERVICE_TOKEN is not None and SERVICE_TOKEN != token:
            logger.info("Attempt to use route without auth")
            raise Unauthorized("No token!")
        return f(request, *args, **kwargs)

    return inner
