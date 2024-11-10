"""
Description: File contains error classes for handling errors in entire code
    If any error occurs in the entire code whether related to authorizing client or
    authenticating user, these defined Custom Exceptions will be raised and further
    execution will be stopped
"""

from fastapi import HTTPException

from core.error_code import ErrorMessages


class TSServerError(ErrorMessages, Exception):
    """
    Custom Error class defined for catching all the errors,
    all error codes are defined in ErrorMessage Class
    """

    def __init__(
            self, error: dict = None, status_code: int = 500,
            additional_info: dict = None, custom_description: str = None, background_task=None):
        """
        :param error: Class Variables defined in ErrorMessages Class
        :param additional_info: Additional info need to pass
        :param custom_description: for overwriting default error description for error
        :return:
        """
        if background_task is None:
            background_task = []

        if error is None:
            # setting default to Internal Server Error
            error = TSServerError.INTERNAL_SV_ERROR

        super().__init__(error["description"])

        self.error_code = error["code"]
        self.description = custom_description or error["description"]
        self.error_dict = additional_info
        self.status_code = status_code
        self.background_task = self.validate_background_task_args(background_task)

    @classmethod
    def validate_background_task_args(cls, val):
        """
        validates if argument passed is of correct type
        for running a background task
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
                    "where func is function that need to be executed and kwargs is argument for function")

            if not isinstance(v[1], dict):
                raise Exception(f"invalid kwargs type for: {v[0]}, type got: {type(v[1])}")

        return val

    def __str__(self):
        """
        Dunder Method for printing the error message
        :return:
        """

        msg = f"ERROR({self.error_code}): {self.description}"
        return msg

    def __dict__(self):
        """
        Dunder method for returning the dict of the required info
        :return:
        """

        error_dict = dict(
            error_code=self.error_code,
            error_description=self.description
        )

        if self.error_dict:
            error_dict.update(self.error_dict)

        return error_dict
