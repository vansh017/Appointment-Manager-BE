"""
"""

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from core import TSServerError, api_log
from crud import CRUDBase
from db import SessionLocal
from models import AddressModel, ContactDetailsModel

from schemas import AddressSchema, ContactSchema


class CRUDContactDetails(CRUDBase[ContactDetailsModel, ContactSchema, ContactSchema]):
    pass


ContactDetails = CRUDContactDetails(ContactDetailsModel)
