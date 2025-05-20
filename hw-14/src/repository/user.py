from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.entity import User
from src.schemas.user import UserInputSchema


async def create_user(body: UserInputSchema, db: AsyncSession):
    """
    Creates a new user record in the database.

    :param body: The Pydantic schema containing user data.
    :type body: UserInputSchema
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The newly created User database model.
    :rtype: User
    """
    user = User(**body)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user(id: str, db: AsyncSession):
    """
    Retrieves a user record from the database by user ID.

    :param id: The ID of the user to retrieve.
    :type id: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The User database model if found and not deleted, otherwise None.
    :rtype: Optional[User]
    """
    query = select(User).filter_by(id=id, deleted_at=None)
    user = await db.execute(query)

    return user.scalar_one_or_none()


async def get_user_by_email(email: str, db: AsyncSession):
    """
    Retrieves a user record from the database by email address.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    :return: The User database model if found and not deleted, otherwise None.
    :rtype: Optional[User]
    """
    query = select(User).filter_by(email=email, deleted_at=None)
    user = await db.execute(query)

    return user.scalar_one_or_none()


async def set_refresh_token(user: User, refresh_token: str, db: AsyncSession):
    """
    Sets the refresh token for a user.

    :param user: The User database model to update.
    :type user: User
    :param refresh_token: The refresh token string.
    :type refresh_token: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    """
    user.refresh_token = refresh_token
    await db.commit()
    await db.refresh(user)


async def reset_refresh_token(user: User, db: AsyncSession):
    """
    Resets (sets to None) the refresh token for a user.

    :param user: The User database model to update.
    :type user: User
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    """
    user.refresh_token = None
    await db.commit()
    await db.refresh(user)


async def confirm_user(user: User, db: AsyncSession):
    """
    Confirms a user's account by setting the is_confirmed flag to True.

    :param user: The User database model to confirm.
    :type user: User
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    """
    user.is_confirmed = True
    await db.commit()
    await db.refresh(user)

    return user


async def set_password(user: User, password: str, db: AsyncSession):
    """
    Sets the password for a user.

    :param user: The User database model to update.
    :type user: User
    :param password: The new password (should be hashed before passing).
    :type password: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    """
    user.password = password
    await db.commit()
    await db.refresh(user)

    return user


async def set_avatar(id: str, avatar: str, db: AsyncSession):
    """
    Sets the avatar URL for a user.

    :param id: The ID of the user to update.
    :type id: str
    :param avatar: The URL of the avatar image.
    :type avatar: str
    :param db: The SQLAlchemy asynchronous database session.
    :type db: AsyncSession
    """
    user = await get_user(id, db)
    user.avatar = avatar
    await db.commit()
    await db.refresh(user)

    return user
