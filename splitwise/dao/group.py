from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class GroupRegisterDAO:
    name: str
    members: list[str]
    description: str = ""
    allow_simplify_expense: bool = True
    group_id: Optional[UUID] = field(default_factory=uuid4)

@dataclass
class GroupResponseDAO:
    name: str
    description: str
    allow_simplify_expense: bool
    created_at: datetime
    group_id: UUID

@dataclass
class GroupBalanceResponseDAO:
    group_id: UUID
    from_user: str
    to_user: str
    amount: float

@dataclass
class DebtPayDAO:
    group_id: UUID
    debt_payer: str
    debt_reciever: str
    amount: float

@dataclass
class PayDebtResponseDAO:
    group_id: UUID
    debt_payer: str
    debt_reciever: str
    remaining_amount: float
