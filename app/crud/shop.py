"""
"""

from crud import CRUDBase
from models import ShopMasterModel

from schemas import ContactSchema, ShopSchema


class CRUDShop(CRUDBase[ShopMasterModel, ShopSchema,ShopSchema]):
    pass


Shop = CRUDShop(ShopMasterModel)
