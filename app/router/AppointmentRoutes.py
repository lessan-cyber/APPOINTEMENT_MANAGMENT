from fastapi import APIRouter
from app.models.AppointmentModels import Appointment

router = APIRouter(
    prefix="/appointments",
    tags=['Appointments']
)

@router.get("/{id}")
def get_appoitement(id:int):
    pass


@router.post("/")
def create_appointment(appointment: Appointment):
    pass

@router.put("/{id}")
def update_appointment(id:int, appointment: Appointment):
    pass

@router.delete("/{id}")
def delete_appointment(id : int):
    pass