from dataclasses import dataclass

@dataclass
class SplitDAO:
    user_id: str
    amount_paid: float
    amount_owed: float
