from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, validates

from splitwise.database import Base

class SplitModel(Base):
    __tablename__ = "splits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.email"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    amount_owed = Column(Float, nullable=False)

    expense = relationship("ExpenseModel", back_populates="splits")

    @validates("amount_paid")
    def validate_amnt_paid(self, _, val):
        if val<0:
            raise ValueError("Amount paid must be greater than or equal 0")
        return val
