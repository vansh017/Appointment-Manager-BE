from datetime import datetime, time
from pydantic import BaseModel, EmailStr


class CatalogSchema(BaseModel):
    item_name : str
    price : int
    expected_time : time = None


