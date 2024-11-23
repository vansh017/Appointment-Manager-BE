from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base
from models import UserModel


class ManualCustomerModel(Base):
    __tablename__ = 'manual_customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    created_by = Column(Integer, ForeignKey(UserModel.id), nullable=False)
