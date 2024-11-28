from datetime import datetime, time

from pydantic import BaseModel, EmailStr



class UserShopSchema(BaseModel):
    shop_id : int
    user_id : int


