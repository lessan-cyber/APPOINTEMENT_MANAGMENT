from fastapi import BackgroundTasks
from app.config import settings, send_email
from app.models.UserModels import User
from app.utils.utils import hash_token, getRandomCode


async def send_account_verfication_email(user: User, background_tasks: BackgroundTasks):
    token = hash_token(user.verification_code)
    activeUrl = f"{settings.APP_URL}/MeetMate/auth/verify-account?token={token}"
    data = {
        "app_name": settings.APP_NAME,
        "name": user.name,
        "activeUrl": activeUrl
    }

    subject = f"Account Verification for {settings.APP_NAME}"
    await send_email(recipients=[user.email],
                     subject=subject,
                     data=data,
                     template_name="account_verification.html",
                     background_tasks=background_tasks,
                     context=data )