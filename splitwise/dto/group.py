from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class GroupDTO:
    name: str
    group_id: UUID
    description: str = ""
    allow_simplify_expense: bool = True

@dataclass
class GroupResponseDTO:
    id: str
    name: str
    description: str
    allow_simplify_expense: bool
    created_at: datetime
    group_id: UUID

@dataclass
class UpdateGroupDTO:
    name: Optional[str] = None
    description: Optional[str] = None
