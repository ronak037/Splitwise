from splitwise.dto.group_balance import GroupBalanceDTO, GroupBalanceResponseDTO
from splitwise.models.group_balances import GroupBalanceModel
from splitwise.utils.singleton import Singleton

from typing import Optional
from uuid import UUID

class GroupBalanceRepository(metaclass=Singleton):
    def __init__(self, db_session):
        self.db = db_session

    def upsert_group_balance(self, group_balance_dto: GroupBalanceDTO) -> GroupBalanceResponseDTO:
        """
        Inserts or updates a balance between from_user and to_user for a group.
        If an entry already exists, increment the amount_owed.
        """
        try:
            group_balance = (
                self.db.query(GroupBalanceModel)
                        .filter(
                            GroupBalanceModel.group_id==group_balance_dto.group_id,
                            GroupBalanceModel.from_user_id==group_balance_dto.from_user_id,
                            GroupBalanceModel.to_user_id==group_balance_dto.to_user_id
                        )
                        .one_or_none()
            )
            if group_balance:
                group_balance.amount_owed+=group_balance_dto.amount_owed
            else:
                group_balance = GroupBalanceModel(
                    group_id=group_balance_dto.group_id,
                    from_user_id=group_balance_dto.from_user_id,
                    to_user_id=group_balance_dto.to_user_id,
                    amount_owed=group_balance_dto.amount_owed
                )
            self.db.add(group_balance)
            self.db.commit()
            self.db.refresh(group_balance)
            return GroupBalanceResponseDTO(
                group_balance_id=group_balance.id,
                group_id=group_balance.group_id,
                from_user_id=group_balance.from_user_id,
                to_user_id=group_balance.to_user_id,
                amount_owed=group_balance.amount_owed
            )
        except Exception as e:
            self.db.rollback()
            raise e

    def fetch_group_balances(self, group_id: UUID) -> list[GroupBalanceResponseDTO]:
        balances = (
            self.db.query(GroupBalanceModel)
                    .filter(GroupBalanceModel.group_id==group_id)
                    .all()
        )
        for i in range(0, len(balances)):
            balance: GroupBalanceModel = balances[i]
            balances[i] = GroupBalanceResponseDTO(
                group_balance_id=balance.id,
                group_id=balance.group_id,
                from_user_id=balance.from_user_id,
                to_user_id=balance.to_user_id,
                amount_owed=balance.amount_owed
            )
        return balances

    def fetch_group_balance_for_user_in_group(self, group_id: UUID, from_user_id: str, to_user_id: str) -> Optional[GroupBalanceResponseDTO]:
        balance: GroupBalanceModel = (
            self.db.query(GroupBalanceModel)
                    .filter(
                        GroupBalanceModel.group_id==group_id,
                        GroupBalanceModel.from_user_id==from_user_id,
                        GroupBalanceModel.to_user_id==to_user_id
                    )
                    .first()
        )
        if balance:
            return GroupBalanceResponseDTO(
                group_balance_id=balance.id,
                group_id=balance.group_id,
                from_user_id=balance.from_user_id,
                to_user_id=balance.to_user_id,
                amount_owed=balance.amount_owed
            )
        else:
            return None

    def delete_balance(self, group_id: UUID, from_user_id: str, to_user_id: str):
        balance = (
            self.db.query(GroupBalanceModel)
                    .filter(
                        GroupBalanceModel.group_id==group_id,
                        GroupBalanceModel.from_user_id==from_user_id,
                        GroupBalanceModel.to_user_id==to_user_id
                    )
                    .first()
        )
        if balance:
            self.db.delete(balance)
            self.db.commit()
