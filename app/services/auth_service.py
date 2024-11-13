import base64
from datetime import timedelta, datetime

from sqlalchemy.orm import Session

import crud
from constants import ACCESS_TOKEN_EXPIRE_MINUTES, MAX_OTP_REQUEST_PER_HR
from core import TSServerError, api_log
from dao.user import create_user_dao, validate_user_login_and_create_otp
from models import UserModel
from schemas.api_schemas import CreateUser
from utilities.methods import validate_strong_password, create_access_token


def create_user(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    try:
        db : Session = kwargs['db']
        user_data : CreateUser = kwargs['user_data']

        if not validate_strong_password(user_data.password):
            raise TSServerError(error=TSServerError.INVALID_PASSWORD,
                status_code=200)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        current_time = datetime.now()

        # Add 30 minutes
        expires_at = current_time + timedelta(minutes=30)
        expires_at = expires_at.strftime("%Y-%m-%d %H:%M:%S")
        user : UserModel = create_user_dao(db,user_data)
        access_token = create_access_token(
            data={"sub": str(user.id),
                  "expires_at": expires_at }, expires_delta=access_token_expires
        )
        db.commit()
        return {"user_id": user.id}

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


def login_user(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """

    try:
        db : Session = kwargs['db']
        user = kwargs["user"]

        user = user["user"]
        try:
            user = base64.b64decode(user).decode()
            if ":" not in user:
                raise Exception("invalid base64 format for credentials")
            username, password = user.split(":")

        except Exception as e:
            api_log.info(f"invalid base64 for credentials decode: {e}")
            raise TSServerError(
                error=TSServerError.BAD_REQUEST,
                status_code=200,
                custom_description="invalid base64 value"
            )

        valid_user =_authenticate_user(
            username=username, password=password, db=db)

        attempts_left = max((MAX_OTP_REQUEST_PER_HR - valid_user["total_otp_attempts"]), 0)

        return {"otp_attempts_left": attempts_left}


    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


def _authenticate_user(username, password, db: Session):
    """
    Authenticates user using username and password and creates otp for login
    :param username:
    :param password:
    :param db:
    :return:
    """
    try:
        user = crud.User.get_user_by_username(username=username, db=db,inactive=True)
        if not len(user):
            api_log.info(f"invalid username: {username}")
            raise TSServerError(
                error=TSServerError.INVALID_USER_CRED,
                status_code=200
            )

        user = user[0]
        if user.is_deleted:
            api_log.info(f"invalid username: {username}")
            raise TSServerError(
                error=TSServerError.ACCOUNT_INACTIVE,
                status_code=200
            )

        otp, total_attempts = validate_user_login_and_create_otp(db=db, user=user, password=password)

        user_info = {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "user_otp": otp.otp,
            "total_otp_attempts": total_attempts
        }

        return user_info

    except TSServerError as dp_err:
        raise dp_err
    except Exception as e:
        api_log.error(f"failed to authenticate user: {e}", exc_info=True)
        raise TSServerError()