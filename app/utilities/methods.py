import time
from datetime import timedelta, datetime
from functools import wraps
from typing import Optional

import bcrypt
import jwt

from constants import ACCESS_TOKEN_EXPIRE_MINUTES
from core import api_log, TSServerError

SECRET_KEY = "ghjlknmsftyugyiu"

def validate_strong_password(password: str):
    """
    Validates if password
    :param password:
    :return:
    """

    special_char_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '\\', '-', '+', '=', '<', '>', '?', ':', " "]

    l, u, p, d = 0, 0, 0, 0
    if len(password) >= 8 and len(password)<=12:
        for i in password:
            if i.islower():
                l += 1
            if i.isupper():
                u += 1
            if i.isdigit():
                d += 1
            if i in special_char_list:
                p += 1
    if l >= 1 and u >= 1 and p >= 1 and d >= 1 and l + p + u + d == len(password):
        return True


def create_pwd_hash(val: str) -> str:
    """
    Creates Hash from given string
    :param val:
    :return:
    """
    val = val.encode('utf-8')
    salt = bcrypt.gensalt()
    val_hash = bcrypt.hashpw(val, salt)
    return val_hash.decode()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def log_method_resp_time(msg: str, log_args=True):
    """
    Decorator prints args, response and time taken to execute for functions
    :param msg: meaning message to print for target function
    :param log_args: Set to false for not logging args passed to functions
    :return:
    """

    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                api_log.info(f"{msg}")
                st = time.time()
                if log_args:
                    api_log.info(f"{func.__name__}; args: {args}, kwargs: {kwargs}")
                resp = func(*args, **kwargs)
                execution_time = time.time() - st
                api_log.info(f"total time for {func.__name__}: {execution_time}")
                str_resp = str(resp)
                str_resp = str_resp[1:1000] if len(str_resp) > 1000 else str_resp
                api_log.info(f"response from function: {func.__name__}: {str_resp}")
                return resp
            except TSServerError as err:
                raise err
            except Exception as e:
                api_log.exception(f"exception in log_method_resp_time: {e}")
                raise TSServerError()

        return wrapper

    return outer