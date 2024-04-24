from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
import src.repository.user as user_repository
from src.database.db import get_db
from src.entity import User
from src.schemas.base import SingleResponseSchema
from src.schemas.user import UserInputSchema, UserSchema
from src.schemas.auth import AuthTokenSchema
from src.services.auth import auth_service
from src.util.get_response_data import get_response_data

auth_router = APIRouter(tags=["auth"])

security = HTTPBearer()


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str


def get_token_response(email: str):
    data = {"sub": email}

    access_token = auth_service.create_access_token(data)
    refresh_token = auth_service.create_refresh_token(data)
    print("access_token: ", access_token)
    print("refresh_token: ", refresh_token)
    return TokenResponse(access_token, refresh_token)


@auth_router.post("/signup", response_model=SingleResponseSchema[UserSchema])
async def signup(body: UserInputSchema, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_email(body.email, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account is already exist"
        )

    new_user = await user_repository.create_user(
        {
            "email": body.email,
            "password": auth_service.get_password_hash(body.password),
        },
        db,
    )

    return get_response_data(jsonable_encoder(new_user))


@auth_router.post("/signin", response_model=SingleResponseSchema[AuthTokenSchema])
async def signin(body: UserInputSchema, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_email(body.email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token_response = get_token_response(user.email)

    user.refresh_token = token_response.refresh_token
    await db.commit()
    await db.refresh(user)

    return get_response_data(token_response)


@auth_router.post(
    "/refresh_token", response_model=SingleResponseSchema[AuthTokenSchema]
)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    email = auth_service.decode_refresh_token(token)
    user = await user_repository.get_user_by_email(email, db)

    if user is None or user.refresh_token != token:
        user.refresh_token = None
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    token_response = get_token_response(user.email)

    user.refresh_token = token_response.refresh_token
    await db.commit()
    await db.refresh(user)

    return get_response_data(token_response)


@auth_router.get("/secret")
async def read_item(current_user: User = Depends(auth_service.get_current_user)):
    return {"message": "secret router", "owner": current_user.password}
