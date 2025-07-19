from splitwise.utils import singleton
from splitwise.repository.groups import group_repository

class GroupRepositoryFactory(metaclass=singleton.Singleton):
    """Factory class to abstract the use of group repositories implementation"""

    def get_group_repository(self, db_session, db_type="memory"):
        """Returns the group repository based on the db_type"""
        if db_type == "memory":
            return group_repository.GroupRepositoryInMemory()
        elif db_type == 'postgres':
            return group_repository.GroupRepository(db_session)
        else:
            raise Exception("Unsupported database type")
