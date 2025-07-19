from splitwise.utils import singleton
from splitwise.repository.users import user_repository

class UserRepositoryFactory(metaclass=singleton.Singleton):
    """Factory class to abstract the use of user repositories implementation"""

    def get_user_repository(self, db_session, db_type="memory"):
        """Returns the user repository based on the db_type"""
        if db_type == "memory":
            return user_repository.UserRepositoryInMemory()
        elif db_type == 'postgres':
            return user_repository.UserRepository(db_session=db_session)
        else:
            raise Exception("Unsupported database type")
