from sqlalchemy import Column, Integer, VARCHAR

from db import Base


class RoleModel(Base):
    """
    Contains pre-defined role for the user
    -   Pharmacy Admin
    -   Pharmacy Staff
    -   Pharmacy Tech
    -   Facility Admin
    -   Facility Staff
     ... etc
    """

    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=255), unique=True, nullable=False)

