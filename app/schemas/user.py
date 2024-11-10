from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from core import get_current_date_time
from schemas._pydantic_config import PydanticBase


class UserSchema(PydanticBase):
    """
    Pydantic Schema for User
    """

    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    contact_number: Optional[str] = None
    fax_number: Optional[str] = None
    last_pwd_change: datetime = None
    is_active: bool = False
    details_verified: bool = False

    failed_login_count: int = 0
    invalid_otp_count: int = 0

    created_on: datetime
    modified_on: datetime = get_current_date_time()