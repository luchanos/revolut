import logging
import sys

from sanic.exceptions import Unauthorized


logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")


def check_auth(f):
    def inner(request, *args, **kwargs):
        token = request.headers.get("X-TOKEN")
        if token is None:
            logger.info("Attemption to use route without auth")
            raise Unauthorized("No token!")
        return f(request, *args, **kwargs)

    return inner
