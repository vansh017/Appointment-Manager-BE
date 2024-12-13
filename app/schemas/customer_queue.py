from datetime import datetime, time
from enum import Enum

from pydantic import BaseModel, EmailStr

class CustomerStatusEnum(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED  = "completed"
    CANCELED = "canceled"


class CustomerQueueSchema(BaseModel):
    customer_id : int
    shop_id : int
    manual_id : int = None
    status : CustomerStatusEnum


