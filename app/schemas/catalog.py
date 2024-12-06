from datetime import datetime, time

from pydantic import BaseModel, EmailStr


class CatalogSchema(BaseModel):
    shop_id : int = None
    item_name : str
    expected_time : time = None
    price : int


