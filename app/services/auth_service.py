from datetime import timedelta, datetime

from sqlalchemy.orm import Session

from constants import ACCESS_TOKEN_EXPIRE_MINUTES
from core import TSServerError
from dao.user import create_user_dao
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
        return {"access_token": access_token}

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e