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
    offset: int, limit: int, search: str, user_id: str | None, db: AsyncSession
) -> (int, list[ContactSchema]):
    count_query = select(func.count(Contact.id)).filter_by(deleted_at=None)

    query = select(Contact).filter_by(deleted_at=None).limit(limit).offset(offset)

    if user_id is not None:
        query = query.filter_by(user_id=user_id)
        count_query = count_query.filter_by(user_id=user_id)
    else:
        query = query.filter(Contact.user_id.is_not(None))
        count_query = count_query.filter(Contact.user_id.is_not(None))

    if is_string(search):
        query = query.filter(
            Contact.name.ilike(f"%{search}%")
            | Contact.surname.ilike(f"%{search}%")
            | Contact.email.ilike(f"%{search}%")
        )

    count = await db.execute(count_query)
    contacts = await db.execute(query)

    return contacts.scalars().all(), count.scalar_one_or_none()


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
