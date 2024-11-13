import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from sqlalchemy import and_, select, update, delete


import crud
from constants import OTP_EXPIRATION_TIME
from core import TSServerError, api_log
from models import OneTimePasswordModel
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