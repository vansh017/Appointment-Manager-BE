from datetime import datetime, time

from pydantic import BaseModel, EmailStr

from core import get_current_date_time


class ShopSchema(BaseModel):
    shop_name : str
    start_time : time = None
    end_time : time = None
    address_id : int
    contact_id : int
    created_date: datetime = get_current_date_time()
    modified_date: datetime = get_current_date_time()


