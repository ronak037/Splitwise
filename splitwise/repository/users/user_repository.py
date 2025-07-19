from splitwise.dto.user import UserDTO, UserResponseDTO
from splitwise.models.users import UserModel

from typing import Optional

class UserRepositoryInMemory:
    def __init__(self):
        self.users = []
        self.idToUser = {}
    
    def add_user(self, user):
        self.users.append(user)
        self.idToUser[user['user_id']] = user
        return user

    def get_user(self, user_id):
        return self.idToUser.get(user_id, None)


class UserRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_user(self, user: UserDTO) -> UserResponseDTO:
        new_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )
        self.db.add(new_user)
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("Some error occured while adding user to database")
            raise e
        self.db.refresh(new_user)
        return UserResponseDTO(id=new_user.id, 
                       first_name=new_user.first_name, 
                       last_name=new_user.last_name,
                       email=new_user.email)
    
    def get_user_by_id(self, user_id) -> Optional[UserResponseDTO]:
        db_user: UserModel = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            return UserResponseDTO(
                id=db_user.id,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                email=db_user.email
            )
        return None

    def get_user_by_email(self, email_id) -> Optional[UserResponseDTO]:
        db_user: UserModel = self.db.query(UserModel).filter(UserModel.email==email_id).first()
        if db_user:
            return UserResponseDTO(
                id=db_user.id,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                email=db_user.email
            )
        return None
    
    #TODO:
    # 1. update user method
    # 2. delete user method

