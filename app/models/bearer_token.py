from sqlalchemy import Column, Integer, DateTime, VARCHAR, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from db import Base
from core import get_current_date_time
from models.user import UserModel


class BearerTokenModel(Base):

    __tablename__ = "bearer_token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=True)
    access_token = Column(LONGTEXT, unique=True, nullable=False)
    refresh_token = Column(VARCHAR(length=255), nullable=True, unique=True)
    expires_on = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    state = Column(VARCHAR(length=255), nullable=True)
    created_on = Column(DateTime, nullable=False, default=get_current_date_time())

