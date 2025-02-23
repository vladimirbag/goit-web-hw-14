from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Схема для створення контакту
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

# Схема для оновлення контакту
class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

# Схема для відповіді
class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True

# Схеми для користувачів (аутентифікація)
class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Видалено constr(), щоб уникнути помилки

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# Схеми для токенів
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
