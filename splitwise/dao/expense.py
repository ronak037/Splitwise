from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class ExpenseDAO:
    group_id: UUID
    description: str
    amount: float
    created_by: str

@dataclass
class ExpenseResponseDAO:
    id: int
    group_id: UUID
    description: str
    amount: float
    created_at: datetime
    created_by: str
