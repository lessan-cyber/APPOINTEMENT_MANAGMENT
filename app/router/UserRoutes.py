from fastapi import APIRouter, BackgroundTasks, status, HTTPException, Depends
from app.models.UserModels import User
from app.schemas.userSchemas import UserCreate
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.email_service import send_email

#router = APIRouter()
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    #verfications de l existance de l utilisateur
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = User.hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    send_email(email=user.email, username=user.username)
    return new_user

#
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