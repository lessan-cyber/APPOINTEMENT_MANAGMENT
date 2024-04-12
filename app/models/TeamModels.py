from sqlalchemy import Table, Column, Integer, ForeignKey, String, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timedelta

# Many-to-many association table
user_team_association = Table(
    'user_team',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('role', String(10), default="member")
)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), unique=True, index=True)
    admin_id = Column(Integer, ForeignKey('users.id'))
    admin = relationship("User")
    users = relationship("User", secondary=user_team_association, back_populates="teams")
    users = relationship(
        "User",
        secondary=user_team_association,
        back_populates="teams",
    )

    def __str__(self):
        return f"Team(id={self.id}, name={self.name}, admin_id={self.admin_id})"

class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    email = Column(String(60), unique=False, index=True)
    status = Column(Enum('pending', 'accepted', 'rejected', name='invitation_status'), default='pending')
    team = relationship("Team")
    expires_at = Column(DateTime, default=datetime.now() + timedelta(days=7))

    def __str__(self):
        return f"Invitation(id={self.id}, team_id={self.team_id}, email={self.email}, status={self.status})"