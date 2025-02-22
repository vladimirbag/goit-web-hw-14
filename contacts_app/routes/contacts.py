from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import crud

from ..database import get_db
from .. import schemas, models
from ..auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=schemas.ContactResponse)
async def create_contact(
    contact: schemas.ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return await crud.create_contact(db, contact, current_user.id)

@router.get("/", response_model=List[schemas.ContactResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return await crud.get_contacts(db, current_user.id)

@router.get("/{contact_id}", response_model=schemas.ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    contact = await crud.get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=schemas.ContactResponse)
async def update_contact(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return await crud.update_contact(db, contact_id, contact, current_user.id)

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    await crud.delete_contact(db, contact_id, current_user.id)
    return {"message": "Contact deleted successfully"}
