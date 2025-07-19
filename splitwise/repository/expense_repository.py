from splitwise.dto.expense import ExpenseDTO, ExpenseResponseDTO
from splitwise.models.expense import ExpenseModel
from splitwise.utils.singleton import Singleton

class ExpenseRepository(metaclass=Singleton):
    def __init__(self, db_session):
        self.db = db_session

    def add_expense(self, expense: ExpenseDTO) -> ExpenseResponseDTO:
        "Add an expense to db"
        expense = ExpenseModel(
            group_id=expense.group_id,
            description=expense.description,
            amount=expense.amount,
            created_by=expense.created_by
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return ExpenseResponseDTO(
            id=expense.id,
            group_id=expense.group_id,
            description=expense.description,
            amount=expense.amount,
            created_at=expense.created_at,
            created_by=expense.created_by
        )
