from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr
from fastapi.background import BackgroundTasks
load_dotenv()
import os

class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    APP_NANE: str
    DEBUG: bool
    SECRET_KEY: str
    ALGORITHM: str
    POSTGRES_PASSWORD: str
    #POSTGRES_USER: str
    POSTGRES_DB: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    USE_CREDENTIALS: bool
    class Config:
        env_file = Path(".") / ".env"
        env_file_encoding = 'utf-8'


settings = Settings()


conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", ""),
    MAIL_PORT=os.environ.get("MAIL_PORT", 1025),
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", False),
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", False),
    MAIL_DEBUG=True,
    MAIL_FROM=os.environ.get("MAIL_FROM", 'noreply@test.com'),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", "MeetMate"),
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", True)
)


# class EmailSchema(BaseModel):
#     email: List[EmailStr]

fm = FastMail(conf)

async def send_email(recipients: list, subject: str, context: dict, template_name: str,background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)