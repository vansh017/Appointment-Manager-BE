from datetime import timedelta, datetime
from typing import Optional

import bcrypt
import jwt

from constants import ACCESS_TOKEN_EXPIRE_MINUTES

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