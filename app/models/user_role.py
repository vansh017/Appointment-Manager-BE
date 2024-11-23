from sqlalchemy import Column, Integer, ForeignKey, DateTime

from core import get_current_date_time
from db import Base
from models.role import RoleModel
from models.user import UserModel


class UserRoleModel(Base):
    """
    UserRole Model for assigning different roles to the user
    """

    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    role_id = Column(Integer, ForeignKey(RoleModel.id), nullable=False)
    created_by = Column(Integer, ForeignKey(UserModel.id), nullable=False)

    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False, default=get_current_date_time())

