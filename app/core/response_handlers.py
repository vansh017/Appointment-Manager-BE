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


class TSResponse:

    def __init__(self, data=None, status_code: int = 200):
        """
        init method for class, status code will expose to client side
        :param data:
        :param status_code:
        """

        if data is None:
            data = {}

        self._data = data
        self._status_code = status_code
        self._background_task = []

    @property
    def data(self):
        """
        Property func for data
        :return:
        """
        return self._data

    @data.setter
    def data(self, val):
        """
        Setter func for setting values
        :param val:
        :return:
        """
        self._data = val

    @property
    def status_code(self):
        """
        Property func for status code
        :return:
        """
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        """
        Setter func for setting values
        :param val:
        :return:
        """
        self._status_code = val

    @property
    def background_task(self):
        """
        Property func for returning background task
        :return:
        """

        return self._background_task

    @background_task.setter
    def background_task(self, val):
        """
        setter for background that will also validate if argument
        passed is of correct type for running a background task
        :param val:
        :return:
        """
        if not isinstance(val, list):
            raise Exception("background task list should be a list of tuple, "
                            "each tuple should be a (func, kwargs)")

        for v in val:
            if not isinstance(v, tuple) or not len(v) == 2:
                raise Exception(
                    "invalid tuple for background task list, tuple should be (func, kwargs) "
                    "where func is function that need to be executed and kwargs is arguments for function")

            if v[1] is not None and not isinstance(v[1], dict):
                raise Exception(f"invalid kwargs type for: {v[0]}, type got: {type(v[1])}")

        self._background_task = val