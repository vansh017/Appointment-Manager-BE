from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey

from db import Base
from models.user import UserModel
from core import get_current_date_time


class OneTimePasswordModel(Base):

    __tablename__ = "one_time_password"

    id = Column(Integer, primary_key=True, autoincrement=True)
    otp = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    expires_on = Column(DateTime, nullable=False)
    created_on = Column(DateTime, nullable=False, default=get_current_date_time())
