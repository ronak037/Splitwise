from splitwise.database import Base

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    # 'users' table ka relation 'groups' table k sath
    # i.e. below 'groups' key will store the groups to which user belongs
    # groups = relationship("GroupModel", secondary="user_groups", back_populates="members")
    groups = relationship("UserGroupModel", back_populates="user")
