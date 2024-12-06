from sqlalchemy.dialects.mysql import VARCHAR

from models.date_class import TimestampMixin
from models.shop_master import ShopMasterModel
from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger
from db import Base

class CatalogModel(Base, TimestampMixin):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(VARCHAR(255), nullable=False)
    price = Column(Integer, nullable=False)
    expected_time = Column(Time, nullable=True)
    shop_id = Column(Integer, ForeignKey(ShopMasterModel.id), nullable=False)