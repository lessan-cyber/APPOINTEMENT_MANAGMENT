from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class UserAppointmentBase(BaseModel):
    title: str
    date: date
    start_time: time
    end_time: time
    description: Optional[str] = None
class UserAppointmentCreate(UserAppointmentBase):
    pass
class UserAppointmentResponse(UserAppointmentBase):
    id: int
    title: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    class Config:
        from_attributes = True
class UserAppointmentUpdate(UserAppointmentBase):
    id: int
class TeamAppointmentCreate(BaseModel):
    team_id: int
    title: str
    date: date
    start_time: time
    end_time: time
    description: Optional[str] = None

class TeamAppointmentUpdate(BaseModel):
    team_id: int
    id: int
    title: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None