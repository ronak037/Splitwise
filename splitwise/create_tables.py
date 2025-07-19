from splitwise.models import expense, groups, group_balances, split, users, user_group
from splitwise.database import Base, engine

Base.metadata.create_all(bind=engine)
