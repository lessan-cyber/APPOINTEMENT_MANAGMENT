from fastapi import APIRouter
from app.models.TeamModels import Team

router = APIRouter(
    prefix="/teams",
    tags=['Team']
)


@router.get("/{id}")
def getTeam():
    pass


@router.post("/")
def create_team(team:Team):
    pass

@router.put("/{id}")
def update_team(team_id: int, team: Team):
    pass

@router.delete("/{id}")
def delete_team(team_id: int):
    pass
