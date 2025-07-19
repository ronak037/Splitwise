from splitwise.utils.singleton import Singleton
from splitwise.dao.expense import ExpenseDAO, ExpenseResponseDAO
from splitwise.dao.split import SplitDAO
from splitwise.dto.expense import ExpenseDTO
from splitwise.dto.group_balance import GroupBalanceDTO
from splitwise.dto.split import SplitDTO
from splitwise.repository.expense_repository import ExpenseRepository
from splitwise.repository.group_balance_repository import GroupBalanceRepository
from splitwise.repository.split_repository import SplitRepository
# from splitwise.dao.split_dao import SplitDAO

from collections import defaultdict


class ExpenseService(metaclass=Singleton):
    def __init__(self, db_session):
        self.expense_repo = ExpenseRepository(db_session)
        self.split_repo = SplitRepository(db_session)
        self.balance_repo = GroupBalanceRepository(db_session)
    
    def _compute_balances(self, splits: list[SplitDAO])-> dict[str, dict[str, float]]:
        """Figure out the balances between the users for an expense to store
        Returns:
            {from_user: {to_user: amount}}
        """
        balances = {}
        for split in splits:
            balances[split.user_id]=round(split.amount_paid-split.amount_owed, 2)
        
        # creditors and debtors list
        creditors = {user_id: amount for user_id, amount in balances.items() if amount>0}
        debtors = {user_id: -amount for user_id, amount in balances.items() if amount<0}

        final_balances = defaultdict(lambda: defaultdict(float))
        for user_id, debt_amount in debtors.items():
            for creditor in list(creditors):
                if debt_amount == 0:
                    break
                amount_to_pay = min(creditors[creditor], debt_amount)
                final_balances[user_id][creditor] += round(amount_to_pay, 2)
                debt_amount -= amount_to_pay
                creditors[creditor] -= amount_to_pay
                if round(creditors[creditor],2) == 0:
                    del creditors[creditor]
        return final_balances

    def add_expense(self, expense_dao: ExpenseDAO, splits: list[SplitDAO]) -> ExpenseResponseDAO:
        expense_dto = ExpenseDTO(
            group_id=expense_dao.group_id,
            description=expense_dao.description,
            amount=expense_dao.amount,
            created_by=expense_dao.created_by,
        )

        print(f"Adding expense: {expense_dto}")
        expense_response_dto = self.expense_repo.add_expense(expense_dto)
        expense_id = expense_response_dto.id

        # Process each split
        print("Processing splits")
        for split_dao in splits:
            split_dto = SplitDTO(
                expense_id=expense_id,
                user_id=split_dao.user_id,
                amount_paid=split_dao.amount_paid,
                amount_owed=split_dao.amount_owed,
            )
            print(f"Adding split to db: {split_dto}")
            self.split_repo.add_split(split_dto)

        print("Computing balances for users")
        balances = self._compute_balances(splits)
        for from_user, to_user_mp in balances.items():
            for to_user, amt in to_user_mp.items():
                balance_dto = GroupBalanceDTO(
                    group_id=expense_dao.group_id,
                    from_user_id=from_user,
                    to_user_id=to_user,
                    amount_owed=amt
                )
                print(f"adding balance group: {balance_dto}")
                self.balance_repo.upsert_group_balance(balance_dto)

        return ExpenseResponseDAO(**expense_response_dto.__dict__)
