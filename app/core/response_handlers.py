import time
from typing import Union

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, RedirectResponse

import core


def get_current_date_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def create_response(data, status_code: int = 200) -> \
        Union[JSONResponse, RedirectResponse]:

    response = {"status": "success", "data": data}
    headers = {
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Resource-Policy": "same-site",
        "Permissions-Policy": "geolocation=(self)",
        "Pragma": "no-cache",
        "X-Permitted-Cross-Domain-Policies": "none",
        "Cross-Origin-Embedder-Policy": "require-corp",
        # "Clear-Site-Data": '"cache","cookies","storage"',
        "Referrer-Policy": 	"no-referrer"
    }
    core.api_log.info(f"api response: {response}")
    return JSONResponse(content=jsonable_encoder(response, by_alias=True),
                        status_code=status_code, headers=headers)


def create_error_response(err_dict: dict = None, status_code: int = 500) -> JSONResponse:
    if err_dict is None:
        err_dict = core.TSServerError.INTERNAL_SV_ERROR
    status_code = status_code
    response = {"status": "failure", "data": err_dict}
    core.api_log.exception(f"api response: {response}")
    return JSONResponse(content=jsonable_encoder(response, by_alias=True),
                        status_code=status_code)