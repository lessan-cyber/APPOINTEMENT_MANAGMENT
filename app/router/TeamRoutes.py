from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.TeamModels import Team, user_team_association, Invitation
from app.models.UserModels import User
from app.schemas.teamSchemas import TeamCreate, AddMembers,  GetTeamInfo, TeamUpdate, RemoveMembers
from app.utils.security import get_current_user
from app.utils.email_service import send_team_invitation_email, send_test_email
from app.utils.utils import display_members
from sqlalchemy import insert, delete

from datetime import datetime
import logging

router = APIRouter(
    prefix="/teams",
    tags=['Team']
)


@router.post("/")
async def create_team(team: TeamCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    if background_tasks is None:
        background_tasks = BackgroundTasks()
    not_registered_emails = []
    # Check if team already exists
    team_exists = db.query(Team).filter(Team.name == team.name).first()
    if team_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team already exists")

    new_team = Team(name=team.name, admin_id=current_user.id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    print(new_team)

    # Add the current user as an admin in the user_team_association table
    stmt = insert(user_team_association).values(user_id=current_user.id, team_id=new_team.id, role='admin')
    db.execute(stmt)
    registred_users = [current_user.email]
    # Send invitations to the members
    for email in team.member_emails:
        user = db.query(User).filter(User.email == email).first()
        if user is not None:
            registred_users.append(email)
            # Check if an invitation for this team and email already exists
            existing_invitation = db.query(Invitation).filter(Invitation.team_id == new_team.id,
                                                              Invitation.email == email).first()
            if existing_invitation is None:
                # Create a new invitation and add it to the database
                invitation = Invitation(team_id=new_team.id, email=email, status='pending')
                db.add(invitation)
                db.commit()
                db.refresh(invitation)
            #     # Handle the case where an invitation already exists (e.g., update the existing invitation, skip sending a new one, etc.)
            #     pass
        else:

            not_registered_emails.append(email)

    db.commit()
    await send_team_invitation_email(registred_users, background_tasks=background_tasks, team_name=new_team.name, invitation_id=invitation.id)
    return {"team": {
        "id": new_team.id,
        "name": new_team.name,
        "admin_id": new_team.admin_id,
        "registred_members": registred_users,
    },
        "not_registered_emails": not_registered_emails,
        "message": "un lien d'invitation seront envoyés aux membres du groupe"}

@router.get("/invitations/{invitation_id}/accept")
def accept_invitation(invitation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get the invitation from the database
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    # Check if the invitation has expired
    if datetime.now() > invitation.expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This invitation has expired")

    if not invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")

    # Check if the current user is the one who was invited
    if current_user.email != invitation.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to accept this invitation")

    # Update the status of the invitation
    invitation.status = 'accepted'
    db.add(invitation)

    # Add the user to the team
    stmt = insert(user_team_association).values(user_id=current_user.id, team_id=invitation.team_id, role='member')
    db.execute(stmt)
    db.commit()
    #db.refresh(stmt)

    return {"message": "You have successfully joined the team"}


@router.put("/add_members")
async def add_members(added_members: AddMembers, current_user: User = Depends(get_current_user),  db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    not_registered_emails = []
    if background_tasks is None:
        background_tasks = BackgroundTasks()

    # verifier si la team existe
    team_exists = db.query(Team).filter(Team.name == added_members.team_name).first()
    if team_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team doesn't exist, verify the name and try later")

    # verifier si le current_user est l'admin de cette team
    if current_user.id != team_exists.admin_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")
    registred_users = []
    for email in added_members.added_members_emails:
        user = db.query(User).filter(User.email == email).first()
        if user is not None:
            registred_users.append(email)
            # Check if an invitation for this team and email already exists
            existing_invitation = db.query(Invitation).filter(Invitation.team_id == team_exists.id,
                                                              Invitation.email == email).first()
            if existing_invitation is None:
                # Create a new invitation and add it to the database
                invitation = Invitation(team_id=team_exists.id, email=email, status='pending')
                db.add(invitation)
                db.commit()
                db.refresh(invitation)
        else:
            not_registered_emails.append(email)

    db.commit()
    await send_team_invitation_email(registred_users, background_tasks=background_tasks, team_name=team_exists.name, invitation_id=invitation.id)
    return {
        "team name": team_exists.name,
        "added members": registred_users,
        "not added members": not_registered_emails,
        "message": "an invitation link will be sent to added members"
    }


@router.post("/team_info")
def getTeamInfo(team: GetTeamInfo, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # verifier si la team existe
    team_exists = db.query(Team).filter(Team.name == team.team_name).first()
    if team_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Team doesn't exist, verify the name and try later")

    # verify that the user is member of the team
    user_team = db.query(user_team_association).filter(user_team_association.c.user_id == current_user.id,
                                                      user_team_association.c.team_id == team_exists.id).first()

    if user_team is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")


    team_members = db.query(User).join(user_team_association).filter(user_team_association.c.team_id == team_exists.id).all()
    #team_members = db.query(user_team_association).filter(user_team_association.c.team_id == team_exists.id).all()
    print(team_members)
    return {
        "team name": team_exists.name,
        "team members": team_members
    }


@router.put("/{team_id}")
async def update_team(team_id: int, team_data: TeamUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch the team from the database
    team = db.query(Team).filter(Team.id == team_id).first()

    # If the team doesn't exist, return a 404 error
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # If the current user is not the admin of the team, return a 403 error
    if current_user.id != team.admin_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Update the team data
    if team_data.name is not None:
        team.name = team_data.name

    db.commit()

    return {"message": "Team updated successfully"}


@router.delete("/{team_id}")
async def delete_team(team_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch the team from the database
    team = db.query(Team).filter(Team.id == team_id).first()

    # If the team doesn't exist, return a 404 error
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    # If the current user is not the admin of the team, return a 403 error
    if current_user.id != team.admin_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    # delete the team from the database and the user_team_association
    stmt = user_team_association.delete().where(user_team_association.c.team_id == team_id)
    db.execute(stmt)
    db.commit()
    stmt_invitations = delete(Invitation).where(Invitation.team_id == team_id)
    db.execute(stmt_invitations)
    db.commit()
    # Now delete
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}


@router.delete("/{team_id}/members")
async def remove_members(team_id: int, remove_data: RemoveMembers, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch the team from the database
    team = db.query(Team).filter(Team.id == team_id).first()

    # If the team doesn't exist, return a 404 error
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    # If the current user is not the admin of the team, return a 403 error
    if current_user.id != team.admin_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    for user_email in remove_data.user_emails:
        users = []
        # Fetch the user from the database
        user = db.query(User).filter(User.email == user_email).first()

        # If the user doesn't exist, return a 404 error
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with with {user_email} not found the {team.name} team  verify the email and try again later")
        stmt = user_team_association.delete().where(user_team_association.c.user_id == user.id)
        db.execute(stmt)
    #     users.append(user)
    # for elt in users:
    #     # Remove the user from the team
    #     stmt = user_team_association.delete().where(user_team_association.c.user_id == elt.id)
    #     db.execute(stmt)
    # db.commit()

    return {"message": "Users removed from team successfully"}

@router.get("/{team_name}/info")
def get_team_info(team_name: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verify if the team exists
    team_exists = db.query(Team).filter(Team.name == team_name).first()
    if team_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Team doesn't exist, verify the name and try later")

    # Verify that the user is a member of the team
    user_team = db.query(user_team_association).filter(user_team_association.c.user_id == current_user.id,
                                                      user_team_association.c.team_id == team_exists.id).first()
    if user_team is None and current_user.id != team_exists.admin_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")

    team_members = db.query(User).join(user_team_association).filter(user_team_association.c.team_id == team_exists.id).all()
    detailed_members = display_members(team_members)
    return {
        "team name": team_exists.name,
        "admin": team_exists.admin.email,
        "team_members": detailed_members
    }



