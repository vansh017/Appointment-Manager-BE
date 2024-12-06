"""
"""

from crud import CRUDBase
from models import ShopMasterModel, CatalogModel

from schemas import ContactSchema, ShopSchema, CatalogSchema


class CRUDCatalog(CRUDBase[CatalogModel, CatalogSchema,CatalogSchema]):
    pass


Catalog = CRUDCatalog(CatalogModel)
