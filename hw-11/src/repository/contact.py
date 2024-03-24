import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import Contact
from src.schemas.contacts import ContactBaseSchema, ContactSchema


async def get_contacts(
    offset: int, limit: int, db: AsyncSession
) -> (int, list[ContactSchema]):
    count_query = await db.execute(
        select(func.count(Contact.id)).filter_by(deleted_at=None)
    )
    count = count_query.scalar_one_or_none()

    query = select(Contact).filter_by(deleted_at=None).limit(limit).offset(offset)
    contacts = await db.execute(query)

    return contacts.scalars().all(), count


async def get_contact(contact_id: int, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id, deleted_at=None)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactBaseSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()

    return contact


async def update_contact(contact_id: int, body: ContactBaseSchema, db: AsyncSession):
    contact = await get_contact(contact_id, db)

    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        await db.commit()

    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    contact = await get_contact(contact_id, db)

    if contact:
        contact.deleted_at = datetime.datetime.utcnow()
        await db.commit()

    return contact
