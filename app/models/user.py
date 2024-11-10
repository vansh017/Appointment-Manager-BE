import time

from sqlalchemy import Column, Integer, DateTime, VARCHAR,Boolean

from db import Base



class UserModel(Base):
    """
    User Model for storing for storing user info
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(VARCHAR(length=150), nullable=False)
    last_name = Column(VARCHAR(length=150), nullable=True)
    username = Column(VARCHAR(length=150), nullable=False, unique=True)
    email = Column(VARCHAR(length=150), nullable=False, unique=True)
    password = Column(VARCHAR(length=255), nullable=False)
    contact_number = Column(VARCHAR(length=255), nullable=True)
    fax_number = Column(VARCHAR(length=255), nullable=True)
    details_verified = Column(Boolean, nullable=True, default=False)

    # TODO confirm for last pwd change
    last_pwd_change = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)  # user will be activated when password
    is_deleted = Column(Boolean, nullable=False, server_default="0")
    # will be changed for first time

    failed_login_count = Column(Integer, nullable=True, default=0)
    invalid_otp_count = Column(Integer, nullable=True, default=0)

    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

