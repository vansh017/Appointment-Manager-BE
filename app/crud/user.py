"""
Description: File contains Class for CRUD Operations for User Table.

    In case if no record is found empty list will be returned

    In case of any exception DpAuthError will be raised

    Since we can't pass our db: Session object to OAuth layer
    a new session is created everytime when OAuth calls any CRUD
    function that requires DB interaction
"""
from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_, or_
from pydantic import EmailStr

from core import TSServerError, api_log
from crud import CRUDBase
from db import SessionLocal
from models import UserModel
from schemas import UserSchema


class CRUDUser(CRUDBase[UserModel, UserSchema, UserSchema]):

    @classmethod
    def get_user_by_username(cls, username: str, db: Session, inactive=False) -> List[UserModel]:
        """
        Retrieves user data from Db using username
        :param inactive: If inactive is true then it show inactive user also.
        :param db:
        :param username: username
        :return: list[dict]
        """
        try:

            query = select(UserModel).filter(UserModel.username == username)

            if not inactive:
                query = query.filter(UserModel.is_deleted == False)

            user_list = db.execute(query).all()

            user = [user[0] for user in user_list]

            return user

        except Exception as e:
            api_log.error(f"error while fetching user data for user: {username}, {e}")
            raise TSServerError()

    @classmethod
    def get_by_email(cls, email: EmailStr, db: Session) -> List[UserModel]:
        """
        Retrieves user data from Db using username
        :param db:
        :param email
        :return: list[dict]
        """
        try:
            query = select(UserModel).filter(UserModel.email == email)
            user = db.execute(query).all()

            if not len(user):
                return []

            user_list = [us[0] for us in user]

            return user_list

        except Exception as e:
            api_log.error(f"failed to get user: {e}")
            raise TSServerError()

    @classmethod
    def reset_failed_login(cls, db: Session, user_id):
        """
        Reset failed login counts for user in case of successful login
        :param db:
        :param user_id:
        :return:
        """
        try:

            api_log.info(f"resetting failed login count for user_id: {user_id}")

            query = update(UserModel) \
                .filter(UserModel.id == user_id) \
                .values(failed_login_count=0)

            db.execute(query)

            db.flush()

        except TSServerError as err:
            raise err
        except Exception as e:
            api_log.exception(f"exception in reset_failed_login: {e}")
            raise TSServerError()



User = CRUDUser(UserModel)
