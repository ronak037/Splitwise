from splitwise.repository.users.user_repository_factory import UserRepositoryFactory
from splitwise.dao.user import UserDAO, UserResponseDAO
from splitwise.dto.user import UserDTO
from splitwise.utils.singleton import Singleton

class UserService(metaclass=Singleton):
    """Service class for user-related operations."""

    def __init__(self, db_session):
        self.user_repository = UserRepositoryFactory().get_user_repository(db_session, db_type="postgres")
    
    def register_user(self, user: UserDAO) -> UserResponseDAO:
        """Register a new user to the repository"""
        print(f"Adding user: {user}")
        db_user = self.user_repository.get_user_by_email(user.email)
        if db_user:
            raise Exception("User already exists")
        user = self.user_repository.create_user(UserDTO(**user.__dict__))
        print(f"User added: {user}")
        return UserResponseDAO(**user.__dict__)
    
    def fetch_user(self, email_id: str) -> UserResponseDAO:
        """Fetch a user by their email ID"""
        print(f"Fetching user with ID: {email_id}")
        user = self.user_repository.get_user_by_email(email_id)
        if not user:
            raise Exception(f"User not found with email: {email_id}")
        print(f"User fetched: {user}")
        return UserResponseDAO(**user.__dict__)
    