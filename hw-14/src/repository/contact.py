import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import Contact
from src.schemas.contacts import ContactBaseSchema, ContactSchema
from src.util.is_string import is_string


async def get_contacts_birthday(
    birthday_days: int, user_id: str, db: AsyncSession
) -> list[ContactSchema]:
    """
    Retrieves contacts with birthdays occurring within the next specified number of days for a given user.

    :param birthday_days: The number of days from today to check for birthdays.
    :type birthday_days: int
    :param user_id: The ID of the user whose contacts to retrieve.
    :type user_id: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: A list of ContactSchema objects representing contacts with upcoming birthdays.
    :rtype: list[ContactSchema]
    """
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
    """
    Retrieves a list of contacts with pagination and optional search filtering.

    Allows filtering by user ID and searching across name, surname, and email.

    :param offset: The number of records to skip (for pagination).
    :type offset: int
    :param limit: The maximum number of records to return (for pagination).
    :type limit: int
    :param search: Optional search string to filter contacts by name, surname, or email.
    :type search: str
    :param user_id: The ID of the user whose contacts to retrieve, or None for all contacts (admin).
    :type user_id: str | None
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: A tuple containing the total count of matching contacts and a list of ContactSchema objects.
    :rtype: (int, list[ContactSchema])
    """
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
    """
    Retrieves a single contact by its ID and associated user ID.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user_id: The ID of the user who owns the contact.
    :type user_id: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The Contact database model if found and not deleted, otherwise None.
    :rtype: Optional[Contact]
    """
    query = select(Contact).filter_by(id=contact_id, user_id=user_id, deleted_at=None)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactBaseSchema, user_id: str, db: AsyncSession):
    """
    Creates a new contact record in the database for a specific user.

    :param body: The Pydantic schema containing contact data.
    :type body: ContactBaseSchema
    :param user_id: The ID of the user who will own the contact.
    :type user_id: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The newly created Contact database model.
    :rtype: Contact
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user_id=user_id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    return contact


async def update_contact(
    body: ContactBaseSchema, contact_id: int, user_id: str, db: AsyncSession
):
    """
    Updates an existing contact record in the database for a specific user.

    :param body: The Pydantic schema containing updated contact data.
    :type body: ContactBaseSchema
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param user_id: The ID of the user who owns the contact.
    :type user_id: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The updated Contact database model if found and updated, otherwise None.
    :rtype: Optional[Contact]
    """
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
    """
    Performs a soft delete on a contact record by setting the deleted_at timestamp.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param user_id: The ID of the user who owns the contact.
    :type user_id: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The deleted Contact database model if found and marked as deleted, otherwise None.
    :rtype: Optional[Contact]
    """
    contact = await get_contact(contact_id, user_id, db)

    if contact:
        contact.deleted_at = datetime.datetime.utcnow()
        await db.commit()
        await db.refresh(contact)

    return contact
