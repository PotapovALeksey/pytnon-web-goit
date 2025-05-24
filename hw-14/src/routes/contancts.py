from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

import src.repository.contact as contact_repository
from src.config.constants import APIRoutes
from src.database.db import get_db
from src.entity import User
from src.entity.user import Role
from src.schemas.base import SingleResponseSchema, ListResponseSchema
from src.schemas.contacts import ContactSchema, ContactBaseSchema, ContactAdminSchema
from src.services.access import Access
from src.services.auth import auth_service
from src.util.get_response_data import get_response_data

contacts_router = APIRouter(prefix=APIRoutes.API_CONTACTS_ROUTE_PREFIX, tags=["contacts"])
is_user_admin = Access([Role.admin])


@contacts_router.get("/birthday", response_model=ListResponseSchema[ContactSchema],
                     dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def get_contacts_birthday(
        birthday_days: int = Query(description="Number of days"),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieves contacts with upcoming birthdays for the current user.

    Filters contacts whose birthdays fall within the next specified number of days.

    :param birthday_days: The number of days from today to check for birthdays.
    :type birthday_days: int
    :return: A list of contacts with upcoming birthdays and their total count.
    :rtype: ListResponseSchema[ContactSchema]
    """
    contacts = await contact_repository.get_contacts_birthday(
        birthday_days, current_user.id, db
    )

    return get_response_data(contacts, total=len(contacts))


@contacts_router.get("", response_model=ListResponseSchema[ContactSchema],
                     dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def get_contacts(
        search: str = Query(
            description="Search by text in - name, surname, email", default=""
        ),
        offset: int = 0,
        limit: int = 50,
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieves a list of contacts for the current user with pagination and search capabilities.

    Allows filtering contacts by name, surname, or email using the search query parameter.

    :param search: Optional search string to filter contacts.
    :type search: str
    :param offset: The number of records to skip (for pagination).
    :type offset: int
    :param limit: The maximum number of records to return (for pagination).
    :type limit: int
    :return: A list of contacts with total count for pagination.
    :rtype: ListResponseSchema[ContactSchema]
    """
    contacts, total = await contact_repository.get_contacts(
        offset, limit, search, current_user.id, db
    )

    return get_response_data(contacts, total=total)


@contacts_router.get(
    "/all",
    response_model=ListResponseSchema[ContactAdminSchema],
    dependencies=[Depends(auth_service.get_current_user), Depends(is_user_admin),
                  Depends(RateLimiter(times=15, seconds=30))],
)
async def get_contacts_all(
        search: str = Query(
            description="Search by text in - name, surname, email", default=""
        ),
        offset: int = 0,
        limit: int = 50,
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieves a list of all contacts (admin access required) with pagination and search capabilities.

    Allows filtering contacts by name, surname, or email using the search query parameter.
    Requires admin role.

    :param search: Optional search string to filter contacts.
    :type search: str
    :param offset: The number of records to skip (for pagination).
    :type offset: int
    :param limit: The maximum number of records to return (for pagination).
    :type limit: int
    :return: A list of all contacts with total count for pagination.
    :rtype: ListResponseSchema[ContactAdminSchema]
    """
    contacts, total = await contact_repository.get_contacts(
        offset, limit, search, None, db
    )

    return get_response_data(contacts, total=total)


@contacts_router.get(
    "/{contact_id}", response_model=SingleResponseSchema[ContactSchema],
    dependencies=[Depends(RateLimiter(times=15, seconds=30))]
)
async def get_contact(
        contact_id: int = Path(description="id of the contact", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieves a single contact by its ID for the current user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :raises HTTPException: 404 Not Found if the contact is not found or does not belong to the user.
    :return: The requested contact data.
    :rtype: SingleResponseSchema[ContactSchema]
    """
    contact = await contact_repository.get_contact(contact_id, current_user.id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return get_response_data(contact)


@contacts_router.post(
    "", response_model=SingleResponseSchema[ContactSchema], status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=15, seconds=30))]
)
async def create_contact(
        body: ContactBaseSchema,
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Creates a new contact for the current user.

    :param body: The data for the new contact.
    :type body: ContactBaseSchema
    :return: The newly created contact data.
    :rtype: ContactSchema
    """
    new_contact = await contact_repository.create_contact(body, current_user.id, db)

    return get_response_data(new_contact)


@contacts_router.patch("/{contact_id}", response_model=SingleResponseSchema[ContactSchema],
                       dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def updated_contact(
        body: ContactBaseSchema,
        contact_id: int = Path(description="id of the contact", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Updates an existing contact for the current user.

    :param body: The updated data for the contact.
    :type body: ContactBaseSchema
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :raises HTTPException: 404 Not Found if the contact is not found or does not belong to the user.
    :return: The updated contact data.
    :rtype: ContactSchema
    """
    contact = await contact_repository.update_contact(
        body, contact_id, current_user.id, db
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return get_response_data(contact)


@contacts_router.delete("/{contact_id}", response_model=SingleResponseSchema[ContactSchema],
                        dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def delete_contact(
        contact_id: int = Path(description="id of the contact", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Deletes a contact for the current user (soft delete).

    Marks the contact as deleted by setting the `deleted_at` timestamp.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :raises HTTPException: 404 Not Found if the contact is not found or does not belong to the user.
    :return: The deleted contact data.
    :rtype: ContactSchema
    """
    contact = await contact_repository.delete_contact(contact_id, current_user.id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return get_response_data(contact)
