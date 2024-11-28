from datetime import datetime

from pydantic import BaseModel, EmailStr

from core import get_current_date_time


class ContactSchema(BaseModel):
    email : EmailStr
    cellphone : str
    workphone : str = None
    fax : str = None
    website : str = None
    created_on: datetime = get_current_date_time()
    modified_on: datetime = get_current_date_time()


