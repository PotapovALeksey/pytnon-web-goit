import pickle

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import src.repository.user as user_repository
from src.database.cache import get_cache
from src.database.db import get_db
from src.schemas.base import SingleResponseSchema, ListResponseSchema
from src.schemas.user import UserSchema
from src.entity.user import User
from src.services.auth import auth_service
from src.util.get_response_data import get_response_data
from src.config.config import config
import cloudinary
import cloudinary.uploader

users_router = APIRouter(prefix='/users', tags=['users'])

cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True
)


@users_router.get('/me', response_model=SingleResponseSchema[UserSchema])
async def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    return get_response_data(current_user)


@users_router.patch('/avatar', response_model=SingleResponseSchema[UserSchema])
async def upload_avatar(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user), db: AsyncSession = Depends(get_db)):
    public_id = f'fastapi/{current_user.email}'

    uploaded_avatar = cloudinary.uploader.upload(file=file.file, public_id=public_id, overwrite=True)
    avatar_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=uploaded_avatar.get('version'))
    updated_user = await user_repository.set_avatar(current_user.id, avatar_url, db)

    cache = get_cache()
    await cache.set(current_user.email, pickle.dumps(updated_user))
    await cache.expire(current_user.email, 300)

    return get_response_data(updated_user)