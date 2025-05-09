from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import User
from src.schemas.user import UserInputSchema


async def create_user(body: UserInputSchema, db: AsyncSession):
    user = User(**body)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user(id: str, db: AsyncSession):
    query = select(User).filter_by(id=id, deleted_at=None)
    user = await db.execute(query)

    return user.scalar_one_or_none()


async def get_user_by_email(email: str, db: AsyncSession):
    query = select(User).filter_by(email=email, deleted_at=None)
    user = await db.execute(query)

    return user.scalar_one_or_none()


async def set_refresh_token(user: User, refresh_token: str, db: AsyncSession):
    user.refresh_token = refresh_token
    await db.commit()
    await db.refresh(user)


async def reset_refresh_token(user: User, db: AsyncSession):
    user.refresh_token = None
    await db.commit()
    await db.refresh(user)


async def confirm_user(user: User, db: AsyncSession):
    user.is_confirmed = True
    await db.commit()
    await db.refresh(user)

    return user


async def set_password(user: User, password: str, db: AsyncSession):
    user.password = password
    await db.commit()
    await db.refresh(user)

    return user


async def set_avatar(id: str, avatar: str, db: AsyncSession):
    user = await get_user(id, db)
    user.avatar = avatar
    await db.commit()
    await db.refresh(user)

    return user
