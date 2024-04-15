from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from app.models.AppointmentModels import UserAppointment,TeamAppointment
from app.utils.email_service import send_notification_for_appointment
from app.app import app  # Assuming your FastAPI app is named "app" and is in the "main.py" file
from fastapi import BackgroundTasks

scheduler = AsyncIOScheduler()

async def send_notification():
    # Get all appointments starting in the next 15 minutes
    upcoming_appointments = UserAppointment.query.filter(
        UserAppointment.start_time.between(
            datetime.now(),
            datetime.now() + timedelta(minutes=15)
        )
    ).all()

    for appointment in upcoming_appointments:
        # Get the user associated with the appointment
        user = appointment.users[0]
        send_notification_for_appointment(user, background_tasks=BackgroundTasks, appointment=appointment)


async def send_team_notification():
    # Get all team appointments starting in the next 15 minutes  
    upcoming_team_appointments = TeamAppointment.query.filter(
        TeamAppointment.start_time.between(
            datetime.now(),
            datetime.now() + timedelta(minutes=15)
        )
    ).all()

    for appointment in upcoming_team_appointments:
        # Get the team associated with the appointment
        team = appointment.team
        # Get all members of the team
        team_members = team.members
        for member in team_members:
            # Send notification to each member
            await send_notification_for_appointment(member, background_tasks=BackgroundTasks(), appointment=appointment)

@app.on_event("startup")
async def start_scheduler():
    scheduler.add_job(send_notification, IntervalTrigger(minutes=15))
    scheduler.add_job(send_team_notification, IntervalTrigger(minutes=15))
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()