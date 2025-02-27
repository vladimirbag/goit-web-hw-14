from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from contacts_app.database import get_db
from contacts_app.models import Contact, User
from contacts_app.schemas import ContactCreate, ContactUpdate, ContactResponse
from contacts_app.auth import get_current_user

from fastapi_limiter.depends import RateLimiter

contacts_router = APIRouter()

# Створення контакту (тільки для авторизованого користувача)
@contacts_router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_contact(
    contact_data: ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_contact = Contact(**contact_data.model_dump(), owner_id=current_user.id)
    db.add(new_contact)
    
    try:
        await db.commit()
        await db.refresh(new_contact)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact with this email or phone already exists")
    
    return new_contact

# Отримання всіх контактів авторизованого користувача
@contacts_router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    name: Optional[str] = None,
    email: Optional[str] = None
):
    query = select(Contact).where(Contact.owner_id == current_user.id)
    
    if name:
        query = query.filter((Contact.first_name.ilike(f"%{name}%")) | (Contact.last_name.ilike(f"%{name}%")))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    
    result = await db.execute(query)
    return result.scalars().all()

# Отримання конкретного контакту авторизованого користувача
@contacts_router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.owner_id == current_user.id))
    contact = result.scalar_one_or_none()
    
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    return contact

# Оновлення контакту (тільки власник може оновлювати)
@contacts_router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_contact = await get_contact(contact_id, db, current_user)
    
    for key, value in contact_data.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    
    await db.commit()
    await db.refresh(db_contact)
    
    return db_contact

# Видалення контакту (тільки власник може видаляти)
@contacts_router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_contact = await get_contact(contact_id, db, current_user)
    
    await db.delete(db_contact)
    await db.commit()
    
    return {"message": "Contact deleted successfully"}
