from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base
from models import UserModel
from models.shop_master import ShopMasterModel


class UserShopModel(Base):
    __tablename__ = 'user_shop'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    shop_id = Column(Integer, ForeignKey(ShopMasterModel.id), nullable=False)