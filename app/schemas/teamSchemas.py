from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional,List

class TeamCreate(BaseModel):
    name: str
    member_emails: List[EmailStr]

class AddMembers(BaseModel):
    team_name: str
    added_members_emails: List[EmailStr]
class Invitation(BaseModel):
    email: EmailStr
    team_id: int

class GetTeamInfo(BaseModel):
    team_name: str

class TeamUpdate(BaseModel):
    name: Optional[str] = None

class RemoveMembers(BaseModel):
    user_emails: List[EmailStr]