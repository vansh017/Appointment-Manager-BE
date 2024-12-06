import random
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from sqlalchemy import and_, select, update, delete


import crud
from constants import OTP_EXPIRATION_TIME, MAX_UNSUCCESSFUL_OTP_SUBMISSION
from core import TSServerError, api_log
from models import OneTimePasswordModel, UserModel
from schemas import OneTimePasswordSchema
from utilities.methods import log_method_resp_time


@log_method_resp_time(msg="getting total otp request for the user")
def total_otp_request(db, user_id):
    """
    Returns total otp request for the user
    :param db:
    :param user_id:
    :return:
    """
    otp_ls = crud.OTP.get_all_otp(db=db, user_id=user_id, last_one_hr=True)
    total_request = len(otp_ls)
    return total_request

@log_method_resp_time(msg="getting unlock time for the user")
def get_unlock_time(db: Session, user_id):
    """
    Gets otp unlock time for the user
    :param db:
    :param user_id:
    :return:
    """
    try:
        query = select(OneTimePasswordModel)\
            .filter(OneTimePasswordModel.user_id == user_id)

        # getting all otp for last one hour
        # ... below function will return rows with descending order on created_on
        otp_ls = crud.OTP.get_all_otp(db=db, user_id=user_id, last_one_hr=True)

        current_time = datetime.now().timestamp()

        if not len(otp_ls):
            return 0  # very unlikely to get this case

        otp_obj = otp_ls[0]
        last_otp_time = otp_obj.created_on

        unlock_time = (last_otp_time + timedelta(hours=1)).timestamp()
        unlock_time = unlock_time - current_time
        return unlock_time

    except TSServerError as err:
        raise err
    except Exception as e:
        api_log.exception(f"exception in :{e}")
        raise TSServerError()

@log_method_resp_time(msg="invalidating previously assigned otp(s) for user")
def invalidate_previous_otp(db: Session, user_id: int):
    """
    Invalidates previously assigned OTP
    :param db:
    :param user_id:
    :return:
    """
    query = update(OneTimePasswordModel) \
        .filter(OneTimePasswordModel.user_id == user_id) \
        .values(is_active=False)

    db.execute(query)

def generate_otp():
    return random.randint(100000, 999999)


def create_unique_otp(db: Session):
    """
    Creates unique OTP for the user
    :param db:
    :return:
    """

    # otp_ls = crud.OTP.get_all_otp(db)
    # if len(otp_ls):
    #     otp_ls = otp_ls[0]

    otp = generate_otp()
    otp = 123456

    # while otp in [ot.otp for ot in otp_ls]:
    #     otp = generate_otp()

    return otp

@log_method_resp_time(msg="creating otp for user")
def create_otp(db: Session, user_id: int) -> OneTimePasswordModel:
    """
    Creates Unique one time login password for user login
    :param db:
    :param user_id:
    :return:
    """
    try:

        # invalidating previously assigned otp for the user
        # ... this makes sure that user always uses the latest otp sent
        # ... not the old ones
        invalidate_previous_otp(db=db, user_id=user_id)

        otp = create_unique_otp(db)

        expires_on = datetime.now() + timedelta(seconds=OTP_EXPIRATION_TIME)
        otp_schema = OneTimePasswordSchema(
            otp=otp, user_id=user_id, expires_on=expires_on,
            created_on=datetime.now()
        )

        otp_: OneTimePasswordModel = crud.OTP.create(db=db, record=otp_schema)

        return otp_
    except TSServerError as err:
        raise err
    except Exception as e:
        api_log.error(f"exception in creating otp for user: {e}", exc_info=True)
        raise TSServerError()

@log_method_resp_time(msg="getting otp user")
def get_otp_user(db: Session, otp: int, username: str) -> List[OneTimePasswordModel]:
    """
    Gets OTP user
    :param username:
    :param db:
    :param otp:
    :return:
    """
    try:
        query = select(OneTimePasswordModel) \
            .join(UserModel, and_(UserModel.id == OneTimePasswordModel.user_id)) \
            .filter(and_(OneTimePasswordModel.otp == otp, OneTimePasswordModel.is_active == 1,
                         UserModel.username == username))

        otp_info = db.execute(query).all()
        otp_info = [user[0] for user in otp_info]

        return otp_info

    except TSServerError as err:
        raise err
    except Exception as e:
        api_log.error(f"exception i getting OTP user: {e}", exc_info=True)
        raise TSServerError()

@log_method_resp_time(msg="deleting previously assigned otp(s) for the user")
def delete_previous_otp(db: Session, user_id: int):
    """
    Deletes Previously assigned OTPs for the user
    :param db:
    :param user_id:
    :return:
    """
    try:
        query = delete(OneTimePasswordModel) \
            .filter(OneTimePasswordModel.user_id == user_id)

        db.execute(query)
        db.flush()

    except TSServerError as err:
        api_log.info(str(err))
    except Exception as e:
        api_log.info(f"exception in deleting OTPs: {e}")

@log_method_resp_time(msg="validating otp request for the user")
def validate_otp_request(db: Session, otp, username):
    """
    Validates OTP request for the user
     - if user entered wrong otp its invalid otp count will be incremented and if the count is
     reached to its max limit ... user has to reset its password
    :param username:
    :param otp:
    :param db:
    :return:
    """
    try:

        user = crud.User.get_user_by_username(db=db, username=username)
        if not len(user):
            api_log.info(f"invalid username: {username}")
            raise TSServerError(
                error=TSServerError.INVALID_USERNAME,
                status_code=200
            )
        user = user[0]

        # checking is user is active or not before generating OTP
        if not user.is_active:
            api_log.info(f"user is inactive: {username}")
            raise TSServerError(
                error=TSServerError.USER_ACC_INACTIVE,
                status_code=200
            )

        if user.is_deleted:
            api_log.info(f"user is inactive: {username}")
            raise TSServerError(
                error=TSServerError.ACCOUNT_INACTIVE,
                status_code=200
            )

        otp_info = get_otp_user(db=db, otp=otp, username=username)

        if not len(otp_info):
            # updating invalid otp count for user ...
            invalid_otp_count = crud.User.update_invalid_otp_count(db=db, user_id=user.id)

            # max count for invalid otp reached for user
            # ... marking user as inactive to prevent from logging further
            if invalid_otp_count >= MAX_UNSUCCESSFUL_OTP_SUBMISSION:
                api_log.info(f"otp submission limit exceeded for user: {username}")
                crud.User.mark_user_in_active(db=db, username=username)

                db.commit()  # issuing session commit to persist invalid otp count for the user

                raise TSServerError(
                    error=TSServerError.INVALID_OTP_LIMIT_EXCEEDED,
                    status_code=200,
                    additional_info={"otp_submission_attempt_left": MAX_UNSUCCESSFUL_OTP_SUBMISSION-invalid_otp_count}
                )

            api_log.info(f"invalid otp: {otp} from user: {username}")

            db.commit()

            raise TSServerError(
                error=TSServerError.INVALID_OTP,
                status_code=200,
                additional_info={"otp_submit_attempt_left": MAX_UNSUCCESSFUL_OTP_SUBMISSION - invalid_otp_count}
            )

        otp_info = otp_info[0]

        otp_obj: OneTimePasswordModel = otp_info
        otp_user: UserModel = user

        # sending expired otp code in response for front end representation
        if otp_obj.expires_on <= datetime.now():
            api_log.info(f"otp expired: {otp} for username: {username}")
            raise TSServerError(
                error=TSServerError.OTP_EXPIRED,
                status_code=200
            )

        # resetting invalid otp count for the user
        crud.User.reset_invalid_otp_count(db=db, username=username)

        # deleting all previously assigned otp of the user,
        # on successful otp validation
        delete_previous_otp(db=db, user_id=otp_user.id)

        # invalid otp count and delete otp changes

        return otp_user

    except TSServerError as err:
        # no rollback here as in case of invalid otp ... custom error is raised, after saving invalid attempts
        raise err
    except Exception as e:
        db.rollback()  # issuing rollback in case of code failure
        api_log.exception(f"exception in validate_otp_request: {e}")
        raise TSServerError()