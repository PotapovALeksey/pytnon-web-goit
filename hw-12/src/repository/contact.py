import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import Contact
from src.schemas.contacts import ContactBaseSchema, ContactSchema
from src.util.is_string import is_string


async def get_contacts_birthday(
    birthday_days: int, user_id: str, db: AsyncSession
) -> list[ContactSchema]:
    today = datetime.date.today()

    query = (
        select(Contact)
        .filter_by(user_id=user_id, deleted_at=None)
        .filter(
            Contact.birthday.between(
                today, today + datetime.timedelta(days=birthday_days)
            )
        )
    )

    contacts = await db.execute(query)

    return contacts.scalars().all()


async def get_contacts(
    offset: int, limit: int, search: str, user_id: str, db: AsyncSession
) -> (int, list[ContactSchema]):
    count_query = await db.execute(
        select(func.count(Contact.id)).filter_by(user_id=user_id, deleted_at=None)
    )
    count = count_query.scalar_one_or_none()

    query = (
        select(Contact)
        .filter_by(user_id=user_id, deleted_at=None)
        .limit(limit)
        .offset(offset)
    )

    if is_string(search):
        query = query.filter(
            Contact.name.ilike(f"%{search}%")
            | Contact.surname.ilike(f"%{search}%")
            | Contact.email.ilike(f"%{search}%")
        )

    contacts = await db.execute(query)

    return contacts.scalars().all(), count


async def get_contact(contact_id: int, user_id: str, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id, user_id=user_id, deleted_at=None)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactBaseSchema, user_id: str, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True), user_id=user_id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    return contact


async def update_contact(
    body: ContactBaseSchema, contact_id: int, user_id: str, db: AsyncSession
):
    contact = await get_contact(contact_id, user_id, db)

    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)

    return contact


async def delete_contact(contact_id: int, user_id: str, db: AsyncSession):
    contact = await get_contact(contact_id, user_id, db)

    if contact:
        contact.deleted_at = datetime.datetime.utcnow()
        await db.commit()
        await db.refresh(contact)

    return contact
