from datetime import datetime

from core import get_current_date_time
from schemas._pydantic_config import PydanticBase


class BearerTokenSchema(PydanticBase):
    user_id: int = None
    access_token: str
    refresh_token: str = None  # refresh_token is not generated in Implicit Grant
    state: str = None
    is_revoked: bool = False
    expires_on: datetime
    created_on: datetime = get_current_date_time()

