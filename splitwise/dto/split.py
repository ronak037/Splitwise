from dataclasses import dataclass

@dataclass
class SplitDTO:
    expense_id: int
    user_id: str
    amount_paid: float
    amount_owed: float

@dataclass
class SplitResponseDTO:
    id: int
    expense_id: int
    user_id: str
    amount_paid: float
    amount_owed: float
