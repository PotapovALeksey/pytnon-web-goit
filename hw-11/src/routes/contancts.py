from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.repository.contact as contact_repository
from src.database.db import get_db
from src.schemas.base import SingleResponseSchema, ListResponseSchema
from src.schemas.contacts import ContactSchema, ContactBaseSchema
from src.util.get_response_data import get_response_data

contacts_router = APIRouter(prefix="/contacts", tags=["contacts"])


@contacts_router.get("", response_model=ListResponseSchema[ContactSchema])
async def get_contacts(
    offset: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    contacts, total = await contact_repository.get_contacts(offset, limit, db)

    return get_response_data(contacts, total)


@contacts_router.get(
    "/{contact_id}", response_model=SingleResponseSchema[ContactSchema]
)
async def get_contact(
    contact_id: int = Path(description="id of the contact", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact = await contact_repository.get_contact(contact_id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return get_response_data(contact)


@contacts_router.post("", response_model=ContactSchema)
async def create_contact(body: ContactBaseSchema, db: AsyncSession = Depends(get_db)):
    new_contact = await contact_repository.create_contact(body, db)

    return new_contact


@contacts_router.patch("/{contact_id}", response_model=ContactSchema)
async def updated_contact(
    body: ContactBaseSchema,
    contact_id: int = Path(description="id of the contact", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact = await contact_repository.update_contact(contact_id, body, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return contact


@contacts_router.delete("/{contact_id}", response_model=ContactSchema)
async def delete_contact(
    contact_id: int = Path(description="id of the contact", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact = await contact_repository.delete_contact(contact_id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return contact
