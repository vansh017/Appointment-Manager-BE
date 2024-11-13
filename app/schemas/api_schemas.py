from pydantic import BaseModel, Field


class CreateUser(BaseModel):

    first_name : str
    last_name : str
    email : str
    password : str


class ValidateOTP(BaseModel):
    otp: int
    username: str = Field(min_length=1)