import pickle

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

import src.repository.user as user_repository
from src.config.config import config
from src.config.constants import APIRoutes
from src.database.cache import get_cache
from src.database.db import get_db
from src.entity.user import User
from src.schemas.base import SingleResponseSchema
from src.schemas.user import UserSchema
from src.services.auth import auth_service
from src.util.get_response_data import get_response_data

users_router = APIRouter(prefix=APIRoutes.API_USERS_ROUTE_PREFIX, tags=['users'])

cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True
)


@users_router.get('/me', response_model=SingleResponseSchema[UserSchema])
async def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves the currently authenticated user's information.

    :return: The current user's data.
    :rtype: SingleResponseSchema[UserSchema]
    """
    return get_response_data(current_user)


@users_router.patch('/avatar', response_model=SingleResponseSchema[UserSchema])
async def upload_avatar(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Uploads and sets a new avatar for the current user.

    Uploads the provided image file to Cloudinary, generates a URL for the resized avatar,
    updates the user's avatar URL in the database, and updates the user data in the cache.

    :param file: The image file to upload as the avatar.
    :type file: UploadFile
    :raises HTTPException: 500 Internal Server Error if Cloudinary upload fails (implicitly handled by Cloudinary library).
    :return: The updated user data with the new avatar URL.
    :rtype: SingleResponseSchema[UserSchema]
    """
    public_id = f'fastapi/{current_user.email}'

    uploaded_avatar = cloudinary.uploader.upload(file=file.file, public_id=public_id, overwrite=True)
    avatar_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=uploaded_avatar.get('version'))
    updated_user = await user_repository.set_avatar(current_user.id, avatar_url, db)

    cache = get_cache()
    await cache.set(current_user.email, pickle.dumps(updated_user))
    await cache.expire(current_user.email, 300)

    return get_response_data(updated_user)