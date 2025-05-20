from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from pathlib import Path
from fastapi_mail import ConnectionConfig
from enum import Enum
from src.config.config import config


class EmailTypeEnum(str, Enum):
    CONFIRM_EMAIL = 'confirm_email'
    RESET_PASSWORD = 'reset_password'


email_templates = {
    EmailTypeEnum.CONFIRM_EMAIL: 'confirm_user_email.html',
    EmailTypeEnum.RESET_PASSWORD: 'reset_password_email.html',
}

mail_config = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_USERNAME,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME="FASTAPI Application",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates' / 'emails',
)


class Mail:
    @staticmethod
    async def send_mail(subject: str, email: EmailStr, body: dict, email_type: EmailTypeEnum):
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[email],
                template_body=body,
                subtype=MessageType.html
            )

            fm = FastMail(mail_config)

            await fm.send_message(message, template_name=email_templates[email_type])
        except ConnectionError as error:
            print(error)


mail_service = Mail()