from fastapi import APIRouter
from app.models.UserModels import User

#router = APIRouter()
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/")
def create_user(user: User):
    pass

@router.get("/{user_id}")
def get_user(user_id: int):
    pass

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    pass

@router.delete("/{user_id}")
def delete_user(user_id: int):
    pass