"""
    CRUD File for performing CRUD operation on Module Master
"""

from typing import List
from datetime import datetime, timedelta

from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from core import TSServerError, api_log
from crud import CRUDBase
from models import OneTimePasswordModel
from schemas import OneTimePasswordSchema


class CURDOtp(CRUDBase[OneTimePasswordModel, OneTimePasswordSchema, OneTimePasswordSchema]):

    @classmethod
    def get_otp_info(cls, db: Session, otp: int) -> List[OneTimePasswordModel]:
        """
        Gets OTP Info
        :param db:
        :param otp:
        :return:
        """
        try:
            query = select(OneTimePasswordModel).filter(OneTimePasswordModel.otp == otp)
            otp_info = db.execute(query).all()

            return list(otp_info) if len(otp_info) else []

        except TSServerError as err:
            raise err
        except Exception as e:
            api_log.error(f"exception in getting otp info: {e}", exc_info=True)
            raise TSServerError()

    @classmethod
    def get_all_otp(cls, db: Session, last_one_hr: bool = False, user_id: int = None) -> List[Row]:
        """
        Gets OTP Info
        :param last_one_hr:
        :param user_id:
        :param db:
        :return:
        """
        try:
            query = select(OneTimePasswordModel).order_by(OneTimePasswordModel.expires_on.desc())

            if user_id:
                query = query.filter(OneTimePasswordModel.user_id == user_id)

            if last_one_hr:
                query = query.filter(
                    OneTimePasswordModel.created_on <= datetime.now(),
                    OneTimePasswordModel.created_on >= (datetime.now() - timedelta(hours=1)))

            otp_ls = db.execute(query).all()

            otp_ls = [otp[0] for otp in otp_ls]

            return otp_ls

        except TSServerError as err:
            raise err
        except Exception as e:
            api_log.error(f"exception in getting otp info: {e}", exc_info=True)
            raise TSServerError()


OTP = CURDOtp(OneTimePasswordModel)


