from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import src.repository.contact as contact_repository
from src.database.db import get_db
from src.database.cache import get_cache
from src.entity import User
from src.entity.user import Role
from src.schemas.base import SingleResponseSchema, ListResponseSchema
from src.schemas.contacts import ContactSchema, ContactBaseSchema, ContactAdminSchema
from src.services.access import Access
from src.util.get_response_data import get_response_data
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

contacts_router = APIRouter(prefix="/contacts", tags=["contacts"])
is_user_admin = Access([Role.admin])


@contacts_router.get("/birthday", response_model=ListResponseSchema[ContactSchema],
                     dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def get_contacts_birthday(
        birthday_days: int = Query(description="Number of days"),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
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
    contact = await contact_repository.get_contact(contact_id, current_user.id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return get_response_data(contact)


@contacts_router.post(
    "", response_model=ContactSchema, status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=15, seconds=30))]
)
async def create_contact(
        body: ContactBaseSchema,
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    new_contact = await contact_repository.create_contact(body, current_user.id, db)

    return new_contact


@contacts_router.patch("/{contact_id}", response_model=ContactSchema,
                       dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def updated_contact(
        body: ContactBaseSchema,
        contact_id: int = Path(description="id of the contact", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    contact = await contact_repository.update_contact(
        body, contact_id, current_user.id, db
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return contact


@contacts_router.delete("/{contact_id}", response_model=ContactSchema,
                        dependencies=[Depends(RateLimiter(times=15, seconds=30))])
async def delete_contact(
        contact_id: int = Path(description="id of the contact", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    contact = await contact_repository.delete_contact(contact_id, current_user.id, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found"
        )

    return contact
