#  Main log file, logs all the request received by the fast api server
import logging
import os

from fastapi import Request
from core.logging_utils import setup_log

# env = os.environ["env"]
#
# log_level = logging.INFO if

api_log = setup_log("ticket-booking")


async def api_logging(request: Request):
    api_log.info(f"request {request.method} - {request.url}")
    api_log.info(f"headers: {dict(request.headers)}")
    api_log.info(f"query params: {request.query_params}")
    api_log.info(f"path params: {request.path_params}")
