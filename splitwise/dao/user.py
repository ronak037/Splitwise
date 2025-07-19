from dataclasses import dataclass

@dataclass
class UserDAO:
    first_name: str
    last_name: str
    email: str
    password: str

@dataclass
class UserResponseDAO:
    id: int
    first_name: str
    last_name: str
    email: str
