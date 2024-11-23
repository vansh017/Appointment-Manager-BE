from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base

class ShopMasterModel(Base):
    __tablename__ = 'shop_master'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(VARCHAR(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    address_id = Column(Integer, nullable=False)
    contact_id = Column(Integer, nullable=False)
