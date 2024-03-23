from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.repository.contact as contact_repository
from src.database.db import get_db
from src.schemas.contacts import ContactSchema

contacts_router = APIRouter(prefix="/contacts", tags=["contacts"])


@contacts_router.get("", response_model=list[ContactSchema])
async def get_contacts(
    offset: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    contacts = await contact_repository.get_contacts(offset, limit, db)

    return contacts


@contacts_router.get("/{id}")
async def get_contact(
    id: int = Path(description="id of the contact", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact = await contact_repository.get_contact(id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return contact
