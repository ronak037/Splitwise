from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from splitwise.database import Base

class GroupBalanceModel(Base):
    __tablename__ = "group_balances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.public_id"), nullable=False)
    from_user_id = Column(String, ForeignKey("users.email"), primary_key=True)  # payer
    to_user_id = Column(String, ForeignKey("users.email"), primary_key=True)    # owes
    amount_owed = Column(Float, nullable=False, default=0)

    @validates("total_paid")
    def validate_total_paid(self, _, val):
        if val<0:
            raise ValueError("Paid amount must be greater than or equal to 0")
        return val
