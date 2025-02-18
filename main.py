from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import date, timedelta
from pydantic import BaseModel, EmailStr
from typing import List, Optional

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/contacts_db"

# Підключення до БД
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Модель SQLAlchemy
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)

# Pydantic-схема для вхідних даних
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

# Pydantic-схема для відповіді
class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True

# Ініціалізація БД
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Отримання сесії БД
async def get_db():
    async with SessionLocal() as session:
        yield session

# Ініціалізація FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

# Додавання контакту
@app.post("/contacts/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

# Отримання списку контактів
@app.get("/contacts/", response_model=List[ContactResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None)
):
    query = "SELECT * FROM contacts"
    if name:
        query += f" WHERE first_name LIKE '%{name}%' OR last_name LIKE '%{name}%'"
    if email:
        query += f" AND email LIKE '%{email}%'"
    result = await db.execute(query)
    return result.scalars().all()

# Отримання одного контакту
@app.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(f"SELECT * FROM contacts WHERE id = {contact_id}")
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Оновлення контакту
@app.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(f"SELECT * FROM contacts WHERE id = {contact_id}")
    db_contact = result.scalar_one_or_none()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)
    
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

# Видалення контакту
@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(f"SELECT * FROM contacts WHERE id = {contact_id}")
    db_contact = result.scalar_one_or_none()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    await db.delete(db_contact)
    await db.commit()
    return {"message": "Contact deleted successfully"}

# Найближчі дні народження
@app.get("/contacts/upcoming-birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)

    result = await db.execute(f"SELECT * FROM contacts WHERE birthday BETWEEN '{today}' AND '{next_week}'")
    return result.scalars().all()
