from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from db import Base
from models.address import AddressModel
from models.contact_details import  ContactDetailsModel
from models.date_class import TimestampMixin


class ShopMasterModel(Base, TimestampMixin):
    __tablename__ = 'shop_master'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(VARCHAR(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    address_id = Column(Integer, ForeignKey(AddressModel.id) ,nullable=False)
    contact_id = Column(Integer, ForeignKey(ContactDetailsModel.id) ,nullable=False)
