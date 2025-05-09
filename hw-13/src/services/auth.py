import pickle
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import src.repository.user as user_repository
from src.config.config import config
from src.database.cache import get_cache
from src.database.db import get_db


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = config.JWT_SECRET_KEY
    ALGORITHM = config.JWT_ALGORITHM
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    def create_access_token(self, data: dict, expires_delta_seconds: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta_seconds:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta_seconds)
        else:
            expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )

        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    # define a function to generate a new refresh token
    def create_refresh_token(self, data: dict, expires_delta_seconds: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta_seconds:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta_seconds)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )

        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_email_token(self, data: dict, expires_delta_seconds: Optional[float] = None):
        to_encode = data.copy()
        if  expires_delta_seconds:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta_seconds)
        else:
            expire = datetime.utcnow() + timedelta(seconds=300)

        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire}
        )

        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        cache = get_cache()

        cached_user = await cache.get(email)

        if cached_user:
            print(pickle.loads(cached_user).avatar)
            return pickle.loads(cached_user);

        user = await user_repository.get_user_by_email(email, db)

        if user is None:
            raise credentials_exception

        await cache.set(email, pickle.dumps(user))
        await cache.expire(email, 300)

        return user

    def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)
            return payload["sub"]
        except JWTError:
            HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          detail="Invalid token for email verification")


auth_service = Auth()
