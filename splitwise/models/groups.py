from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from splitwise.database import Base

class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    allow_simplify_expense = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    members = relationship("UserGroupModel", back_populates="group")
