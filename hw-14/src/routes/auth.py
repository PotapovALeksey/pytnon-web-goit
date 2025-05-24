from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, Security, BackgroundTasks, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
import src.repository.user as user_repository
from src.config.constants import APIRoutes, Messages
from src.database.db import get_db
from src.schemas.base import SingleResponseSchema
from src.schemas.user import UserInputSchema, UserSchema, ResetPasswordInputSchema, RequestEmailInputSchema
from src.schemas.auth import AuthTokenSchema
from src.services.auth import auth_service
from src.util.get_response_data import get_response_data
from src.services.mail import mail_service, EmailTypeEnum

auth_router = APIRouter(prefix=APIRoutes.API_AUTH_ROUTE_PREFIX, tags=["auth"])
security = HTTPBearer()

TEMPLATE_DIRECTORY = Path(__file__).parent.parent / 'templates' / 'pages',
templates = Jinja2Templates(directory=TEMPLATE_DIRECTORY)


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str


def get_token_response(email: str):
    """
    Generates access and refresh tokens for a given email.

    :param email: The email address to encode in the tokens.
    :type email: str
    :return: An object containing the generated access and refresh tokens.
    :rtype: TokenResponse
    """
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
    """
    Registers a new user.

    Checks if a user with the given email already exists. If not, creates a new user,
    hashes the password, generates an email confirmation token, and sends a confirmation email
    using background tasks.

    :param body: The input data for user registration.
    :type body: UserInputSchema
    :raises HTTPException: 409 Conflict if the email already exists.
    :return: The newly created user data with a success message.
    :rtype: SingleResponseSchema[UserSchema]
    """
    user = await user_repository.get_user_by_email(body.email, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=Messages.ACCOUNT_EXIST
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
    """
    Authenticates a user and provides access and refresh tokens.

    Verifies the user's email and password. If valid and confirmed, generates JWT access and refresh tokens
    and stores the refresh token in the database.

    :param body: The input data for user sign-in (email and password).
    :type body: UserInputSchema
    :raises HTTPException: 401 Unauthorized if credentials are invalid or user is not confirmed.
    :return: An object containing access and refresh tokens.
    :rtype: SingleResponseSchema[AuthTokenSchema]
    """
    user = await user_repository.get_user_by_email(body.email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=Messages.INVALID_CREDENTIALS
        )

    if not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=Messages.EMAIL_NOT_CONFIRMED
        )

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=Messages.INVALID_CREDENTIALS
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
    """
    Refreshes access and refresh tokens using a valid refresh token.

    Validates the provided refresh token. If valid, generates new access and refresh tokens
    and updates the refresh token in the database.

    :raises HTTPException: 401 Unauthorized if the refresh token is invalid or expired.
    :return: An object containing new access and refresh tokens.
    :rtype: SingleResponseSchema[AuthTokenSchema]
    """
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
    """
    Confirms a user's email address using a confirmation token.

    Validates the email confirmation token. If valid, confirms the user's account.

    :param token: The email confirmation token from the verification link.
    :type token: str
    :raises HTTPException: 400 Bad Request if the token is invalid or the user is not found.
    :return: A message indicating successful email confirmation.
    :rtype: SingleResponseSchema[None]
    """
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
    """
    Requests a new email confirmation link for a user.

    Checks if a user with the given email exists and is not already confirmed. If so, generates a new
    email confirmation token and sends a confirmation email using background tasks.

    :param body: The schema containing the user's email.
    :type body: RequestEmailInputSchema
    :return: A message indicating that the confirmation link has been sent or that the email is already confirmed.
    :rtype: SingleResponseSchema[None]
    """
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
    """
    Requests a password reset link for a user.

    Checks if a user with the given email exists and is confirmed. If so, generates a password reset token
    and sends a reset password email using background tasks.

    :param body: The schema containing the user's email.
    :type body: RequestEmailInputSchema
    :raises HTTPException: 400 Bad Request if the user is not found or not confirmed.
    :return: A message indicating that the reset link has been sent.
    :rtype: SingleResponseSchema[None]
    """
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
    """
    Resets the user's password using a reset token.

    Validates the password reset token and the new password. If valid and the user is confirmed, updates the user's password.

    :param token: The password reset token from the reset link.
    :type token: str
    :param body: The schema containing the new password and password confirmation.
    :type body: ResetPasswordInputSchema
    :raises HTTPException: 400 Bad Request if passwords do not match, the token is invalid, or the user is not found/not confirmed.
    :return: A message indicating successful password reset.
    :rtype: SingleResponseSchema[None]
    """
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
    """
    Renders the password reset HTML page.

    Provides the HTML form for the user to enter their new password.

    :param token: The password reset token to include in the page context.
    :type token: str
    :return: The HTML response for the password reset page.
    :rtype: HTMLResponse
    """
    return templates.TemplateResponse("reset_password_page.html", {"request": request, "token": token})
