# -------------------------------------------------
############## Test user data dump ##############
# -------------------------------------------------

from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.service.user_service import UserService
userSvc = UserService(db)
from splitwise.dao.user import UserDAO
newUser = UserDAO(first_name="alice", last_name="bob", email="test2@gmail.com", password="test2")
userSvc.register_user(newUser)

# from splitwise.repository.users.user_repository import UserRepository
# userRepo = UserRepository(db)
# from splitwise.dto.user import UserDTO
# newUser = UserDTO(first_name="John", last_name="Doe", email="test@gmail.com", password="test")
# addedUser = userRepo.create_user(newUser)



# -------------------------------------------------
############## Test group data dump ##############
# -------------------------------------------------

from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.service.group_service import GroupService
grpSvc = GroupService(db)
from splitwise.dao.group import GroupRegisterDAO
group = GroupRegisterDAO(name="g2", allow_simplify_expense=False, members=["test@gmail.com"], group_id="67ad7133-fc66-4eb5-909c-14847970cfae")
addedGroup = grpSvc.create_group(group)

# from splitwise.repository.groups.group_repository import GroupRepository
# groupRepo = GroupRepository(db)
# from splitwise.dto.group import GroupDTO
# newGroup = GroupDTO(name="g1", allow_simplify_expense=False)
# addedGroup = groupRepo.create_group(newGroup)


# ----------------------------------------------------
#################### Fetch group by user #############
# ----------------------------------------------------
from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.service.group_service import GroupService
grpSvc = GroupService(db)
groups = grpSvc.fetch_groups_of_user("test@gmail.com")


# ----------------------------------------------------
#################### Add user to group ###############
# ----------------------------------------------------
from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.service.group_service import GroupService
grpSvc = GroupService(db)
groups = grpSvc.add_group_members('67ad7133-fc66-4eb5-909c-14847970cfae', ["test3@gmail.com"])



# ----------------------------------------------------
#################### Add expense to group ###############
# ----------------------------------------------------
from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.dao.expense import ExpenseDAO
expenseObj = ExpenseDAO(
    "67ad7133-fc66-4eb5-909c-14847970cfae",
    "expense 2",
    amount=50,
    created_by="test2@gmail.com"
)

from splitwise.dao.split import SplitDAO
splitObj1 = SplitDAO(
    user_id="test3@gmail.com",
    amount_paid=80,
    amount_owed=50
)
splitObj2 = SplitDAO("test2@gmail.com", 80, 120)
splitObj3 = SplitDAO("test@gmail.com", 0, 30)
splits = [splitObj1, splitObj3]

from splitwise.service.expense_service import ExpenseService
expenseSvc = ExpenseService(db)
expenseSvc.add_expense(expenseObj,splits)


# ----------------------------------------------------
#################### Get group balance ###############
# ----------------------------------------------------
from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.service.group_service import GroupService
grpSvc = GroupService(db)
balances = grpSvc.get_group_balance("67ad7133-fc66-4eb5-909c-14847970cfae")


# ----------------------------------------------------
#################### Pay debt ###############
# ----------------------------------------------------
from splitwise.database import SessionLocal
db = SessionLocal()

from splitwise.dao.group import DebtPayDAO
debt_dao = DebtPayDAO(
    "67ad7133-fc66-4eb5-909c-14847970cfae",
    "test3@gmail.com",
    "test2@gmail.com",
    10
)

from splitwise.service.group_service import GroupService
grpSvc = GroupService(db)
grpSvc.pay_debt(debt_dao)
