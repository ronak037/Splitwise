from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDTO:
    first_name: str
    last_name: str
    email: str
    password: str
    id: Optional[int] = None

@dataclass
class UserResponseDTO:
    id: int
    first_name: str
    last_name: str
    email: str
