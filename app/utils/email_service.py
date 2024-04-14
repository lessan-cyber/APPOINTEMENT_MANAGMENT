from fastapi import BackgroundTasks,HTTPException
from app.models.UserModels import User
from fastapi import BackgroundTasks,HTTPException
from app.config import settings, send_email
from app.models.UserModels import User
from app.models.TeamModels import Invitation, Team
from app.utils.utils import hash_token, getRandomCode, verify_token_validity


async def send_account_verfication_email(user: User, background_tasks: BackgroundTasks):
    token = hash_token(user.verification_code)
    activeUrl = f"{settings.APP_URL}/users/verify?token={token}&email={user.email}"
    data = {
        "app_name": settings.APPLICATION_NANE,
        "name": user.name,
        "activeUrl": activeUrl
    }

    subject = f"Account Verification for {settings.APPLICATION_NANE}"
    await send_email(recipients=[user.email],
                     subject=subject,
                     template_name="account_activation.html",
                     background_tasks=background_tasks,
                     context=data )

async def account_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        "app_name": settings.APPLICATION_NANE,
        "name": user.name,
        "loginUrl": f"{settings.APP_URL}/login"
    }
    subject = f"WELCOME TO  {settings.APPLICATION_NANE} FAMILY Happy to see you"
    await send_email(recipients=[user.email],
                     subject=subject,
                     template_name="account_confirmation.html",
                     background_tasks=background_tasks,
                     context=data
                     )




async def activate_user_account(data, session, background_tasks):
    user = session.query(User).filter_by(email=data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Tis link is invalid")

    if hash_token(user.verification_code) != data.token:
        raise HTTPException(status_code=400, detail="This link in expired or invalid")
    user.is_active = True
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    # inform the users that his account has been activated
    await account_confirmation_email(user, background_tasks)
    return user

# ... existing code ...

async def send_team_invitation_email(email: str, background_tasks, team_name:str,code:str):
    #accept_url = f"{settings.APP_URL}/teams/invitations/{invitation_id}/accept"
    data = {
        "team_name": team_name,
        "code": code,
        "app_name": settings.APPLICATION_NANE,
        # extract the name from the email
        "name": email.split("@")[0],
    }
    subject = f"Invitation to join {team_name}"
    await send_email(recipients=[email],
                     subject=subject,
                     template_name="team_invitation.html",
                     background_tasks=background_tasks,
                     context=data)



async def send_test_email(email, background_tasks):
    print("sending email")
    await send_email(recipients=email,
                     subject="Test email",
                     template_name="test.html",
                     background_tasks=background_tasks,
                     context={})