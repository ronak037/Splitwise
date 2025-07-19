from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from splitwise.database import Base

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.public_id"), nullable=False)
    description = Column(String, nullable=False, default="")
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    created_by = Column(String, ForeignKey("users.email"), nullable=False)

    splits = relationship("SplitModel", back_populates="expense")

    @validates("amount")
    def validate_amt(self, _, val):
        if val<=0:
            raise ValueError("Expense amount must be greater than 0")
        return val
