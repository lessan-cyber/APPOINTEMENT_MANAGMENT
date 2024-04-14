from fastapi import APIRouter, HTTPException,Depends,status
from app.models.AppointmentModels import AppointmentBase, UserAppointment,TeamAppointment
from app.database import get_db
from app.models.UserModels import User
from app.models.TeamModels import Team,user_team_association
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.utils.security import get_current_user
from app.schemas.appoitementShemas import UserAppointmentCreate, UserAppointmentUpdate,TeamAppointmentCreate,TeamAppointmentUpdate
router = APIRouter(
    prefix="/appointment",
    tags=['Appointment']
)

@router.post("/user", status_code=200)
def create_user_appointment(appointment: UserAppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if appointment.start_time >= appointment.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    overlapping_appointments = db.query(UserAppointment).filter(
        UserAppointment.user_id == current_user.id,
        UserAppointment.date == appointment.date,
        and_(
            UserAppointment.start_time < appointment.end_time,
            UserAppointment.end_time > appointment.start_time
        )
    ).first()
    if appointment.date < date.today():
        raise HTTPException(status_code=400, detail="Appointment date cannot be in the past")
    if overlapping_appointments:
        raise HTTPException(status_code=400, detail="You already have an appointment at that time")

    db_appointment = UserAppointment(**appointment.dict(), user_id=current_user.id)

    # Add the new appointment to the database
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {
        "message": "Appointment created successfully",
        "appointment": db_appointment
    }


@router.put('/user/{appointment_id}', status_code=200)
def update_user_Appointment(appointment: UserAppointmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the appointment exists
    db_appointment = db.query(UserAppointment).filter(UserAppointment.id == appointment.id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found verify the id and try again")

    # Check if the user is the owner of the appointment
    if db_appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this appointment")

    # check if the user is trying to update the date to a past date
    if appointment.date < date.today():
        raise HTTPException(status_code=400, detail="Appointment date cannot be in the past")

    #check if the user does not have an appointment at that time
    overlapping_appointments = db.query(UserAppointment).filter(
        UserAppointment.user_id == current_user.id,
        UserAppointment.date == appointment.date,
        and_(
            UserAppointment.start_time < appointment.end_time,
            UserAppointment.end_time > appointment.start_time
        )
    ).first()

    if overlapping_appointments:
        raise HTTPException(status_code=400, detail="You already have an appointment at that time")

    # Check if the new start time is before the end time
    if appointment.start_time >= appointment.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    # Update the appointment
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)
    return {
        "message": "Appointment updated successfully",
        "appointment": db_appointment
    }


@router.delete('/user/{appointment_id}', status_code=200)
def delete_user_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_appointment = db.query(UserAppointment).filter(UserAppointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found verify the id and try again")
    if db_appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this appointment")
    db.delete(db_appointment)
    db.commit()
    return {
        "message": "Appointment deleted successfully"
    }


@router.post("/team", status_code=status.HTTP_200_OK)
def create_team_appointment(appointment: TeamAppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # check if the team exists
    team = db.query(Team).filter(Team.id == appointment.team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found verify the id and try again")

    # check if the user is the admin of the team
    if team.admin_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to create an appointment for this team")

    # check if the team  doesn't have an appointment at that time
    overlapping_appointments = db.query(TeamAppointment).filter(
        TeamAppointment.team_id == appointment.team_id,
        TeamAppointment.date == appointment.date,
        and_(
            TeamAppointment.start_time < appointment.end_time,
            TeamAppointment.end_time > appointment.start_time
        )
    ).first()
    if overlapping_appointments:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team already have an appointment at that time")

    db_appointment = TeamAppointment(**appointment.dict(), creator_id=current_user.id)

    # Add the new appointment to the database
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {
        "message": "Appointment created successfully and added to the team's calendar",
        "appointment": db_appointment,

    }


@router.put('/team/{appointment_id}', status_code=200)
def update_team_appointment(appointment: TeamAppointmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the appointment exists
    db_appointment = db.query(TeamAppointment).filter(TeamAppointment.id == appointment.id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found verify the id and try again")

    # check if the appointment is for the team
    if db_appointment.team_id != appointment.team_id:
        raise HTTPException(status_code=400, detail="This appointment is not for the team")

    # Check if the user is the admin of the team
    team = db.query(Team).filter(Team.id == appointment.team_id).first()
    if team.admin_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this appointment")

    # check if the team  doesn't have an appointment at that time
    overlapping_appointments = db.query(TeamAppointment).filter(
        TeamAppointment.team_id == appointment.team_id,
        TeamAppointment.date == appointment.date,
        and_(
            TeamAppointment.start_time < appointment.end_time,
            TeamAppointment.end_time > appointment.start_time
        )
    ).first()
    if overlapping_appointments:
        raise HTTPException(status_code=400, detail="Team already have an appointment at that time")

    # Update the appointment
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)
    return {
        "message": "Appointment updated successfully",
        "appointment": db_appointment
    }


@router.delete('/team/{appointment_id}', status_code=200)
def delete_team_appointement(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the appointment exists
    db_appointment = db.query(TeamAppointment).filter(TeamAppointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found verify the id and try again")

    # check if the user is the admin of the team
    team = db.query(Team).filter(Team.id == db_appointment.team_id).first()
    if team.admin_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this appointment")

    # Delete the appointment
    db.delete(db_appointment)
    db.commit()
    return {
        "message": "Appointment deleted successfully"
    }

# Get team appointements
@router.get('/team/{team_id}', status_code=200)
def get_team_appointments(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found verify the id and try again")

    # Check if the user is a member of the team
    if current_user not in team.users or team.admin_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not a member of this team")



    # Get the team's appointments
    appointments = db.query(TeamAppointment).filter(TeamAppointment.team_id == team_id).all()
    return {
        "appointments": appointments
    }

# get info about a specific team appointment
@router.get('/team/{team_id}/{appointment_id}', status_code=200)
def get_team_appointment(team_id: int, appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found verify the id and try again")

    # Check if the user is a member of the team
    if current_user not in team.users or current_user not in team.users:
        raise HTTPException(status_code=403, detail="You are not a member of this team")

    # Check if the appointment exists
    appointment = db.query(TeamAppointment).filter(TeamAppointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found verify the id and try again")

    return {
        "appointment": appointment
    }

# Get  info about a specific userappointment
@router.get('/user/{appointment_id}', status_code=200)
def get_user_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the appointment exists
    appointment = db.query(UserAppointment).filter(UserAppointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found verify the id and try again")
    # check if the user is the owner of the appointment
    if appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this appointment")

    return {
        "appointment": appointment
    }

# Get all user appointments
@router.get('/user', status_code=200)
def get_user_appointments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    appointments = db.query(UserAppointment).filter(UserAppointment.user_id == current_user.id).all()
    # get the user team appointments
    user_teams = db.query(user_team_association).filter(user_team_association.c.user_id == current_user.id).all()
    user_team_appointements = []
    for team in user_teams:
        team_appointments = db.query(TeamAppointment).filter(TeamAppointment.team_id == team.team_id).all()
        user_team_appointements += team_appointments



    return {
        "user_appointments": appointments,
        "team_appointments": user_team_appointements
    }


