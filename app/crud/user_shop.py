"""
"""
from crud import CRUDBase
from db import SessionLocal
from models import AddressModel, UserShopModel

from schemas import AddressSchema, UserShopSchema


class CRUDUserShop(CRUDBase[UserShopModel, UserShopSchema, UserShopSchema]):
    pass


UserShop = CRUDUserShop(UserShopModel)
