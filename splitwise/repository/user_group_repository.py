from typing import Optional

from splitwise.models.user_group import UserGroupModel
from splitwise.dto.user_group import UserGroupDTO, UserGroupResponseDTO

class UserGroupRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create_user_group_entry(self, user_group_key_pair: UserGroupDTO):
        user_group_key_mapping = UserGroupModel(
            user_id=user_group_key_pair.user_id,
            group_id=user_group_key_pair.group_id
        )
        self.db.add(user_group_key_mapping)
        self.db.commit()
        self.db.refresh(user_group_key_mapping)

    def get_group_ids_for_user(self, user_id: str) -> Optional[list[UserGroupResponseDTO]]:
        user_groups: list[UserGroupModel] = self.db.query(UserGroupModel).filter(UserGroupModel.user_id==user_id)
        result = list()
        for user_group in user_groups:
            result.append(UserGroupResponseDTO(
                            user_id=user_group.user_id,
                            group_id=user_group.group_id,
                            joined_at=user_group.joined_at
                        ))
        return result
