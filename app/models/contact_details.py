from sqlalchemy import Column, VARCHAR, Integer, DateTime

from core import get_current_date_time
from db.base_class import Base


class ContactDetailsModel(Base):

    __tablename__ = "contact_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(length=255), nullable=True)
    cellphone = Column(VARCHAR(length=255), nullable=True)
    workphone = Column(VARCHAR(length=255), nullable=True)
    fax = Column(VARCHAR(length=255), nullable=True)
    website = Column(VARCHAR(length=255), nullable=True)

    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False, default=get_current_date_time())

