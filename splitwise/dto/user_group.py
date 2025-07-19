from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class UserGroupDTO:
    user_id: str
    group_id: UUID

@dataclass
class UserGroupResponseDTO:
    user_id: str
    group_id: UUID
    joined_at: datetime
