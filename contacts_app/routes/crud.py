from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status
from ..models import Contact, User
from ..schemas import ContactCreate, ContactUpdate, UserCreate
from .security import get_password_hash

# CRUD для контактів
async def create_contact(db: AsyncSession, contact: ContactCreate, user_id: int):
    new_contact = Contact(**contact.model_dump(), owner_id=user_id)
    db.add(new_contact)
    try:
        await db.commit()
        await db.refresh(new_contact)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact with this email or phone already exists")
    return new_contact

async def get_contacts(db: AsyncSession, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> List[Contact]:
    query = select(Contact).where(Contact.owner_id == user_id)
    if name:
        query = query.filter((Contact.first_name.ilike(f"%{name}%")) | (Contact.last_name.ilike(f"%{name}%")))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    result = await db.execute(query)
    return result.scalars().all()

async def get_contact(db: AsyncSession, contact_id: int, user_id: int) -> Optional[Contact]:
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.owner_id == user_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

async def update_contact(db: AsyncSession, contact_id: int, contact: ContactUpdate, user_id: int) -> Contact:
    db_contact = await get_contact(db, contact_id, user_id)
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def delete_contact(db: AsyncSession, contact_id: int, user_id: int):
    db_contact = await get_contact(db, contact_id, user_id)
    await db.delete(db_contact)
    await db.commit()
    return {"message": "Contact deleted successfully"}

# CRUD для користувачів
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    return new_user

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
