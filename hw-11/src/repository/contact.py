import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import Contact
from src.schemas.contacts import ContactBaseSchema


async def get_contacts(offset: int, limit: int, db: AsyncSession):
    query = select(Contact).limit(limit).offset(offset)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_contact(id: int, db: AsyncSession):
    query = select(Contact).filter_by(id=id, deleted_at=None)
    contact = await db.execute(query)
    return contact


async def create_contact(body: ContactBaseSchema, db: AsyncSession):
    contact = Contact(
        name=body.name,
        surname=body.surname,
        phone=body.phone,
        email=body.email,
        birthday=body.birthday,
    )
    db.add(contact)
    await db.commit()
    return contact


async def update_contact(id: int, body: ContactBaseSchema, db: AsyncSession):
    contact = await get_contact(id, db)

    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        db.add(contact)
        await db.commit()

    return contact


async def delete_contact(id: int, db: AsyncSession):
    contact = await get_contact(id, db)

    if contact:
        contact.deleted_at = datetime.datetime.utcnow()

        await db.commit()

    return contact
