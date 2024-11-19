from enum import Enum

from pydantic import BaseModel, Field


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


class ValidateOTP(BaseModel):
    otp: int
    username: str = Field(min_length=1)