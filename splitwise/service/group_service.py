from collections import defaultdict
from uuid import UUID

from splitwise.dao.group import DebtPayDAO, GroupRegisterDAO, GroupResponseDAO, GroupBalanceResponseDAO, PayDebtResponseDAO
from splitwise.dto.group import GroupDTO
from splitwise.dto.group_balance import GroupBalanceDTO
from splitwise.dto.user_group import UserGroupDTO
from splitwise.repository.groups.group_repository_factory import GroupRepositoryFactory
from splitwise.repository.group_balance_repository import GroupBalanceRepository
from splitwise.repository.user_group_repository import UserGroupRepository
from splitwise.service.user_service import UserService
from splitwise.utils.singleton import Singleton

class GroupService(metaclass=Singleton):
    """Service class for group-related operations."""

    def __init__(self, db_session):
        self.group_repository = GroupRepositoryFactory().get_group_repository(db_session, db_type="postgres")
        self.group_balance_repo = GroupBalanceRepository(db_session=db_session)
        self.user_group_repository = UserGroupRepository(db_session)
        self.user_svc = UserService(db_session=db_session)

    def create_group(self, group: GroupRegisterDAO) -> GroupResponseDAO:
        """Create a new group for the user with members"""
        print(f"Adding group: {group}")
        existing_group = self.group_repository.get_group_by_id(group.group_id)
        if existing_group:
            raise Exception("Group already exists")
        
        print("Validating users...")
        members = group.members
        for email in members:
            try:
                self.user_svc.fetch_user(email_id=email)
            except Exception as e:
                print("One of the user in group member is not registered")
                raise e

        group = self.group_repository.create_group(GroupDTO(
                                                name=group.name, 
                                                group_id=group.group_id,
                                                description=group.description,
                                                allow_simplify_expense=group.allow_simplify_expense))
        print(f"Group added: {group}")

        print("Updating user_group table...")
        for email in members:
            user = self.user_svc.fetch_user(email_id=email)
            self.user_group_repository.create_user_group_entry(UserGroupDTO(
                                                            user_id=user.email,
                                                            group_id=group.group_id))
        print("Association table updated")
        return GroupResponseDAO(
                                name=group.name, 
                                description=group.description,
                                allow_simplify_expense=group.allow_simplify_expense,
                                created_at=group.created_at,
                                group_id=group.group_id
                            )
    
    def fetch_group(self, group_id: UUID) -> GroupResponseDAO:
        """Fetch a group by its public ID"""
        print(f"Fetching group with ID: {group_id}")
        group = self.group_repository.get_group_by_id(group_id)
        if not group:
            raise Exception("Group not found")
        print(f"Group fetched: {group}")
        return GroupResponseDAO(
                                name=group.name, 
                                description=group.description,
                                allow_simplify_expense=group.allow_simplify_expense,
                                created_at=group.created_at,
                                group_id=group.group_id
                            )
    
    def fetch_groups_of_user(self, user_id) -> list[GroupResponseDAO]:
        """Fetch all groups that a user is part of"""
        print(f"Fetching groups for user ID: {user_id}")
        try:
            self.user_svc.fetch_user(email_id=user_id)
        except Exception as e:
            raise e

        groups = self.user_group_repository.get_group_ids_for_user(user_id)
        print(f"Fetched groups of user: {groups}")
        groups = [self.fetch_group(group_id=group.group_id) for group in groups]
        print(f"Fetched group info: {groups}")
        return groups
    
    def add_group_members(self, group_id: UUID, user_ids: list[str]):
        """Adds users to a group"""
        print(f"Adding users {user_ids} to group: {group_id}")
        try:
            for email_id in user_ids:
                self.user_svc.fetch_user(email_id=email_id)
        except Exception as e:
            raise e

        group = self.group_repository.get_group_by_id(group_id)
        if not group:
            raise Exception("Group not found")
        
        for email_id in user_ids:
            self.user_group_repository.create_user_group_entry(UserGroupDTO(
                user_id=email_id,
                group_id=group_id
            ))
            print(f"User {email_id} is added to group {group_id}")
        print(f"All user added to the group {group_id}")

    def get_group_balance(self, group_id: str) -> list[GroupBalanceResponseDAO]:
        """Get group balance for a group"""
        balances = self.group_balance_repo.fetch_group_balances(group_id)

        net_balance = defaultdict(lambda: defaultdict(float))
        for balance in balances:
            from_user = balance.from_user_id
            to_user = balance.to_user_id
            amnt = round(balance.amount_owed, 2)
            if amnt > 0 and from_user!=to_user:
                net_balance[from_user][to_user]+=amnt
        
        result=list()
        visited=set()
        
        for from_user in list(net_balance):
            for to_user in net_balance[from_user].keys():
                if (from_user, to_user) in visited:
                    continue

                amt_from_to = net_balance[from_user].get(to_user, 0)
                amt_to_from = net_balance[to_user].get(from_user, 0)

                if amt_from_to>amt_to_from:
                    result.append(GroupBalanceResponseDAO(
                        group_id=group_id,
                        from_user=from_user,
                        to_user=to_user,
                        amount=round(amt_from_to-amt_to_from,2)
                    ))
                elif amt_from_to<amt_to_from:
                    result.append(GroupBalanceResponseDAO(
                        group_id=group_id,
                        from_user=to_user,
                        to_user=from_user,
                        amount=round(amt_to_from-amt_from_to,2)
                    ))
                visited.add((from_user, to_user))
                visited.add((to_user, from_user))

        return result

    def pay_debt(self, debt_dao: DebtPayDAO):
        """Pay debt"""
        if debt_dao.amount <= 0:
            raise ValueError("Amount to pay must be greater than 0")

        group_balance = self.get_group_balance(group_id=debt_dao.group_id)
        required_balance = None

        for balance in group_balance:
            if balance.from_user == debt_dao.debt_reciever and balance.to_user == debt_dao.debt_payer:
                if balance.amount<debt_dao.amount:
                    raise ValueError("Can't allow to pay more than the debt amount")
                required_balance: GroupBalanceResponseDAO = balance
                break
        
        if required_balance is None:
            raise ValueError("No debt to pay")

        remaining_amnt = round(required_balance.amount - debt_dao.amount, 2)

        # Deleting both entries and simplifying by creating simplified new balance entry
        self.group_balance_repo.delete_balance(required_balance.group_id, required_balance.from_user, required_balance.to_user)
        self.group_balance_repo.delete_balance(required_balance.group_id, required_balance.to_user, required_balance.from_user)
        if remaining_amnt > 0:
            self.group_balance_repo.upsert_group_balance(
                GroupBalanceDTO(
                    group_id=required_balance.group_id,
                    from_user_id=required_balance.from_user,
                    to_user_id=required_balance.to_user,
                    amount_owed=remaining_amnt
                )
            )
        
        return PayDebtResponseDAO(
            group_id=required_balance.group_id,
            debt_reciever=required_balance.from_user,
            debt_payer=required_balance.to_user,
            remaining_amount=remaining_amnt
        )