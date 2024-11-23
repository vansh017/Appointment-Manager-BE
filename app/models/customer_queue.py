from models import ManualCustomerModel
from models.date_class import TimestampMixin
from models.shop_master import ShopMasterModel
from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base
from models import UserModel


class CustomerQueueModel(Base, TimestampMixin):
    __tablename__ = 'customer_queue'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(UserModel.id),nullable=True)
    shop_id = Column(Integer, ForeignKey(ShopMasterModel.id), nullable=False)
    manual_id = Column(Integer, ForeignKey(ManualCustomerModel.id), nullable=True)
    status = Column(Integer, nullable=False)