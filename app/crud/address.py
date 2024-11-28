"""
"""

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from core import TSServerError, api_log
from crud import CRUDBase
from db import SessionLocal
from models import  AddressModel

from schemas import AddressSchema


class CRUDAddress(CRUDBase[AddressModel, AddressSchema, AddressSchema]):
    pass


Address = CRUDAddress(AddressModel)
