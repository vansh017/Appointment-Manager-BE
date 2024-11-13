from datetime import datetime

from pydantic import Field

from schemas._pydantic_config import PydanticBase
from core import get_current_date_time


class OneTimePasswordSchema(PydanticBase):

    otp: int
    user_id: int
    is_active: bool = True
    expires_on: datetime
    created_on: datetime = get_current_date_time()
