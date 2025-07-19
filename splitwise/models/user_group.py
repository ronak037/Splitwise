from splitwise.database import Base

from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class UserGroupModel(Base):
    __tablename__ = "user_groups"
    
    user_id = Column(String, ForeignKey("users.email"), primary_key=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.public_id"), primary_key=True)
    joined_at = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship("UserModel", back_populates="groups")
    group = relationship("GroupModel", back_populates="members")
