from typing import Optional

from splitwise.dto.group import GroupDTO, GroupResponseDTO, UpdateGroupDTO
from splitwise.models.groups import GroupModel

class GroupRepositoryInMemory:
    def __init__(self):
        self.groups = []
        self.idToGroup = {}
    
    def add_group(self, group: GroupDTO) -> GroupDTO:
        self.groups.append(group)
        self.idToGroup[group.id] = group
        return group

    def get_group(self, group_id) -> GroupResponseDTO:
        group = self.idToGroup.get(group_id, None).__dict__
        return GroupResponseDTO(**group)

    def update_group(self, group_id, group: UpdateGroupDTO):
        self.idToGroup[group_id] = group
        for i, g in enumerate(self.groups):
            if g.id == group_id:
                self.groups[i] = group
                break
        
        updated_group_dict = self.idToGroup[group_id].__dict__
        return GroupResponseDTO(**updated_group_dict)

    def fetch_groups_of_user(self, user_id):
        return [group for group in self.groups if user_id in group.get('members', [])]


class GroupRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_group(self, group: GroupDTO) -> GroupDTO:
        new_group = GroupModel(
            name=group.name,
            description=group.description,
            allow_simplify_expense=group.allow_simplify_expense,
            public_id=group.group_id
        )
        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return GroupResponseDTO(
            id=new_group.id,
            name=new_group.name,
            description=new_group.description,
            allow_simplify_expense=new_group.allow_simplify_expense,
            created_at=new_group.created_at,
            group_id=new_group.public_id
        )

    def get_group_by_id(self, group_id: str) -> Optional[GroupDTO]:
        db_group: GroupModel = self.db.query(GroupModel).filter(GroupModel.public_id == group_id).first()
        if db_group:
            return GroupResponseDTO(
                id=db_group.id,
                name=db_group.name,
                description=db_group.description,
                allow_simplify_expense=db_group.allow_simplify_expense,
                created_at=db_group.created_at,
                group_id=db_group.public_id
            )
        return None
