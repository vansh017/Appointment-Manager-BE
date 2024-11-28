"""
   Model for storing addresses for pharmacy and facilities
"""


from sqlalchemy import Column, Integer, VARCHAR, DateTime

from db import Base
from core import get_current_date_time


class AddressModel(Base):

    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_line_1 = Column(VARCHAR(length=255), nullable=True)
    address_line_2 = Column(VARCHAR(length=255), nullable=True)
    city = Column(VARCHAR(length=255), nullable=True)
    state = Column(VARCHAR(length=255), nullable=True)
    zipcode = Column(VARCHAR(length=255), nullable=True)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False, default=get_current_date_time())