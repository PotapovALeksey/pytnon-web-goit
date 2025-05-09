from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, Security, BackgroundTasks, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
import src.repository.user as user_repository
from src.database.db import get_db
from src.schemas.base import SingleResponseSchema
from src.schemas.user import UserInputSchema, UserSchema, ResetPasswordInputSchema, RequestEmailInputSchema
from src.schemas.auth import AuthTokenSchema
from src.services.auth import auth_service
from src.util.get_response_data import get_response_data
from src.services.mail import mail_service, EmailTypeEnum

auth_router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

TEMPLATE_DIRECTORY = Path(__file__).parent.parent / 'templates' / 'pages',
templates = Jinja2Templates(directory=TEMPLATE_DIRECTORY)


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str


def get_token_response(email: str):
    data = {"sub": email}

    access_token = auth_service.create_access_token(data)
    refresh_token = auth_service.create_refresh_token(data)

    return TokenResponse(access_token, refresh_token)


@auth_router.post(
    "/signup",
    response_model=SingleResponseSchema[UserSchema],
    status_code=status.HTTP_201_CREATED,
)
async def signup(body: UserInputSchema, request: Request, background_tasks: BackgroundTasks,
                 db: AsyncSession = Depends(get_db)):
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

    token = auth_service.create_email_token({"sub": new_user.email})
    body = {'host': str(request.base_url), 'token': token}
    background_tasks.add_task(func=mail_service.send_mail, subject='Confirm registration', email=new_user.email,
                              body=body, email_type=EmailTypeEnum.CONFIRM_EMAIL)

    return get_response_data(new_user, detail="User successfully created. Check your email for confirmation.")


@auth_router.post("/signin", response_model=SingleResponseSchema[AuthTokenSchema])
async def signin(body: UserInputSchema, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_email(body.email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
        )

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token_response = get_token_response(user.email)

    await user_repository.set_refresh_token(user, token_response.refresh_token, db)

    return get_response_data(token_response)


@auth_router.post(
    "/refresh-token", response_model=SingleResponseSchema[AuthTokenSchema]
)
async def refresh_token(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    email = auth_service.decode_refresh_token(token)
    user = await user_repository.get_user_by_email(email, db)

    if user is None or user.refresh_token != token:
        await user_repository.reset_refresh_token(user, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    token_response = get_token_response(user.email)

    await user_repository.set_refresh_token(user, token_response.refresh_token, db)

    return get_response_data(token_response)


@auth_router.get('/confirm-email/{token}')
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = await user_repository.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )

    if not user.is_confirmed:
        await user_repository.confirm_user(user, db)

    return get_response_data(None, detail="Email confirmed")


@auth_router.post('/request-confirm-email')
async def request_confirm_email(body: RequestEmailInputSchema, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_email(body.email, db)

    if user.is_confirmed:
        return get_response_data(None, detail="Your email is already confirmed")

    if user:
        token = auth_service.create_email_token({"sub": user.email})
        body = {'host': str(request.base_url), 'token': token}
        background_tasks.add_task(func=mail_service.send_mail, subject='Confirm registration', email=user.email,
                                  body=body, email_type=EmailTypeEnum.CONFIRM_EMAIL)

    return get_response_data(None, detail="Check your email for confirmation.")


@auth_router.post('/request-reset-password')
async def reset_password(body: RequestEmailInputSchema, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_email(body.email, db)

    if user is None or not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )

    token = auth_service.create_email_token({"sub": user.email})
    body = {'host': str(request.base_url), 'token': token}
    background_tasks.add_task(func=mail_service.send_mail, subject='Reset password', email=user.email,
                              body=body, email_type=EmailTypeEnum.RESET_PASSWORD)

    return get_response_data(None, detail="Check your email for resetting password")


@auth_router.post('/reset-password/{token}')
async def reset_password(token: str, body: ResetPasswordInputSchema, db: AsyncSession = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = await user_repository.get_user_by_email(email, db)

    if user is None or not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )

    hashed_password = auth_service.get_password_hash(body.password)
    await user_repository.set_password(user, hashed_password, db)

    return get_response_data(None, detail="Your password has been reset")


@auth_router.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    return templates.TemplateResponse("reset_password_page.html", {"request": request, "token": token})
