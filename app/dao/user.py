from sqlalchemy.orm import Session

import crud
from core import TSServerError, get_current_date_time
from models import UserModel
from schemas.api_schemas import CreateUser
from utilities.methods import create_pwd_hash


def create_user_dao(db: Session,user_data: CreateUser):
    """

    :param db:
    :param user_data:
    :return:
    """
    try:

        user_info = crud.User.get_by_email(db=db,email=user_data.email)
        if user_info:
            raise TSServerError(
                status_code=200,
                error=TSServerError.USER_EXIST,
            )

        hashed_pwd = create_pwd_hash(user_data.password)
        user = UserModel(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=hashed_pwd,
            username=user_data.email,
            email=user_data.email,
            is_active=True,
            is_deleted=False,
            created_on=get_current_date_time(),
            modified_on=get_current_date_time()
        )
        db.add(user)
        db.flush([user])
        return user

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e