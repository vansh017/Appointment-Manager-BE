from datetime import datetime, time
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from schemas import AddressSchema, ContactSchema, CatalogSchema
from schemas.customer_queue import CustomerStatusEnum


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-Binary"
    OTHER = "Other"

class CreateUser(BaseModel):

    first_name : str
    last_name : str
    gender : GenderEnum
    email : str
    password : str
    contact_number : str


class UpdateStatus(BaseModel):

    shop_id : int
    customer_id : int
    status : CustomerStatusEnum
class CreateShop(BaseModel):

    shop_name: str
    start_time : time
    end_time : time
    address : AddressSchema
    contact_details: ContactSchema
    catalog_list : List[CatalogSchema]



class ValidateOTP(BaseModel):
    otp: int
    username: str = Field(min_length=1)