from splitwise.dto.split import SplitDTO, SplitResponseDTO
from splitwise.models.split import SplitModel
from splitwise.utils.singleton import Singleton

class SplitRepository(metaclass=Singleton):
    def __init__(self, db_session):
        self.db = db_session

    def add_split(self, split: SplitDTO) -> SplitResponseDTO:
        """Add split to the database"""
        split = SplitModel(
            expense_id=split.expense_id,
            user_id=split.user_id,
            amount_paid=split.amount_paid,
            amount_owed=split.amount_owed
        )
        self.db.add(split)
        self.db.commit()
        self.db.refresh(split)
        return SplitResponseDTO(
            id=split.id,
            expense_id=split.expense_id,
            user_id=split.user_id,
            amount_paid=split.amount_paid,
            amount_owed=split.amount_owed
        )
