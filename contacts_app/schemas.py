from pydantic import BaseModel, EmailStr
from typing import Optional, Annotated
from pydantic.types import constr
from datetime import date
from typing import Optional

# Схема для створення контакту
class ContactCreate(BaseModel):
    first_name: Annotated[str, constr(min_length=1, max_length=50)]
last_name: Annotated[str, constr(min_length=1, max_length=50)]
email: EmailStr
phone_number: Annotated[str, constr(min_length=10, max_length=15, regex="^\+?[0-9]+$")]
birthday: date
additional_info: Optional[str] = None

# Схема для оновлення контакту (дозволяє часткове оновлення)
class ContactUpdate(BaseModel):
    first_name: Optional[Annotated[str, constr(min_length=1, max_length=50)]] = None
    last_name: Optional[Annotated[str, constr(min_length=1, max_length=50)]] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[Annotated[str, constr(min_length=10, max_length=15, regex="^\+?[0-9]+$")]] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

# Схема для відповіді
class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True

# Схеми для користувача (аутентифікація)
class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=8, max_length=100)]

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
