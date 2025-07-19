from dataclasses import dataclass

from uuid import UUID

# This class represents the balance sheet of a user in a group
@dataclass
class GroupBalanceDTO:
    group_id: UUID
    from_user_id: str
    to_user_id: str
    amount_owed: float

@dataclass
class GroupBalanceResponseDTO:
    group_balance_id: str
    group_id: UUID
    from_user_id: str
    to_user_id: str
    amount_owed: float
