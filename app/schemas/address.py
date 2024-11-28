from datetime import datetime

from pydantic import BaseModel

from core import get_current_date_time


class AddressSchema(BaseModel):

    address_line_1 : str
    address_line_2 : str = None
    city : str
    state : str
    zipcode : str
    created_on : datetime = get_current_date_time()
    modified_on : datetime = get_current_date_time()