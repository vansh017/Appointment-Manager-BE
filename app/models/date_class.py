from sqlalchemy import Column, Integer, String, ForeignKey, Time, BigInteger, DateTime
from datetime import datetime

class TimestampMixin:
    created_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    modified_date = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)