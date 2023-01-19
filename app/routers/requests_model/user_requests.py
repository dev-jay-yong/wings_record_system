import datetime
from typing import Optional

from pydantic import BaseModel


class RegisterRequestModel(BaseModel):
    user_id: str
    password: str
    password_check: str
    name: str
    birth_day: datetime.date
    age: int
    number: int = -1
    position: str = None


class LoginRequestModel(BaseModel):
    user_id: str
    password: str
