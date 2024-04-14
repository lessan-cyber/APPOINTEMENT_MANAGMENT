from sqlalchemy import Column, Integer, DateTime, String, ForeignKey,Time, Date
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from app.database import Base

class AppointmentBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(75), nullable=False)
    date = Column(Date, default=datetime.now().date())
    start_time = Column(Time)
    end_time = Column(Time)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

class UserAppointment(AppointmentBase):
    __tablename__ = "user_appointments"
    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="user_appointments")


class TeamAppointment(AppointmentBase):
    __tablename__ = "team_appointments"
    creator_id = Column(Integer, ForeignKey("users.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="appointments")
