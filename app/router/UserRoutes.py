from fastapi import APIRouter, BackgroundTasks, status, HTTPException, Depends
from app.models.UserModels import User
from app.schemas.userSchemas import UserCreate, VerifyUserRequest
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.database import get_db
from app.utils.email_service import send_account_verfication_email, activate_user_account

# router = APIRouter()
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # verfications de l existance de l utilisateur
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = User.set_password(user, user.password)
    user.password = hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await send_account_verfication_email(new_user, background_tasks=background_tasks)
    return new_user


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks,
                              session: Session = Depends(get_db)):
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"message": "Account is activated successfully."})


@router.post("/login")
async def login_user():
    pass
#
# @router.get("/{user_id}")
# def get_user(user_id: int):
#     pass
#
# @router.put("/{user_id}")
# def update_user(user_id: int, user: User):
#     pass
#
# @router.delete("/{user_id}")
# def delete_user(user_id: int):
#     pass
