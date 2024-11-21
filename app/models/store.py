import time

from sqlalchemy import Column, Integer, DateTime, VARCHAR,Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from db import Base



class UserModel(Base):
    """
    User Model for storing for storing user info
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(LONGTEXT, nullable=False)

    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

