from fastapi import APIRouter, BackgroundTasks, status, HTTPException, Depends, Query
from app.schemas.userSchemas import UserCreate, VerifyUserRequest,Token
from fastapi.responses import JSONResponse
from app.utils.email_service import send_account_verfication_email, activate_user_account
from app.utils.security import get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.UserModels import User, TokenModel
from app.utils.security import create_access_token, create_refresh_token, oauth2_scheme, verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.security import get_current_user

# router = APIRouter()
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # verfication de l'email de l'utilisateur
    user_email_exists = db.query(User).filter(User.email == user.email).first()
    if user_email_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    user_name_exists = db.query(User).filter(User.name == user.name).first()
    # verfication du nom de l'utilisateur
    if user_name_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user.password = get_password_hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await send_account_verfication_email(new_user, background_tasks=background_tasks)
    return {"users": new_user,
            "message": "un message de verification vient d'etre envoyé à votre adresse mail"}


# @router.post("/verify", status_code=status.HTTP_200_OK)
# async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_db)):
#     await activate_user_account(data, session, background_tasks)
#     return JSONResponse({"message": "Votre compte a été activé avec succès",
#                          "status": status.HTTP_200_OK})



@router.get("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(background_tasks: BackgroundTasks, session: Session = Depends(get_db), token: str = Query(...), email: str = Query(...)):
    data = VerifyUserRequest(token=token, email=email)
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"message": "Votre compte a été activé avec succès",
                         "status": status.HTTP_200_OK})

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    # Store the tokens in the database
    expires_at = datetime.now() + access_token_expires
    token_model = TokenModel(user_id=user.id, access_token=access_token, refresh_token=refresh_token, expires_at=expires_at)
    db.add(token_model)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.put("/tokens/revoke")
async def revoke_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_model = db.query(TokenModel).filter(TokenModel.access_token == token).first()
    if token_model is None:
        raise HTTPException(status_code=404, detail="Token not found")
    token_model.revoked = True
    db.commit()
    return {"message": "Token revoked"}


@router.put("/token/refresh")
def refresh_access_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_model = db.query(TokenModel).filter(TokenModel.refresh_token == refresh_token).first()
    if token_model is None or token_model.revoked:
        raise HTTPException(status_code=403, detail="Token is revoked or not found")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": token_model.users.email}, expires_delta=access_token_expires
    )
    token_model.access_token = access_token
    token_model.expires_at = datetime.now() + access_token_expires
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user

@router.delete("/me")
def delete_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/logout")
async def logout_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_model = db.query(TokenModel).filter(TokenModel.access_token == token).first()
    if token_model is None:
        raise HTTPException(status_code=404, detail="Token not found")
    token_model.revoked = True
    db.commit()
    return {"message": "Token revoked"}
