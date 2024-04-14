from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Boolean, Column, String, UUID
from app.utils.utils import get_password_hash, verify_password
from uuid import uuid4
from datetime import datetime, timedelta
from app.models.TeamModels import user_team_association

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(10), default="member")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
    # appointment = relationship("Appointment", back_populates="owner")
    verification_code = Column(String(150), default=str(uuid4()))
    user_appointments = relationship("UserAppointment", back_populates="users")
    is_verified = Column(Boolean, default=False)
    tokens = relationship("TokenModel", back_populates="user")
    teams = relationship(
        "Team",
        secondary=user_team_association,
        back_populates="users",
    )
    def __repr__(self):
        return f"<User {self.email}>"
    def verify_password(self, password):
        return verify_password(password, self.password)
    def set_password(self, password):
        self.password = get_password_hash(password)


class TokenModel(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires_at = Column(DateTime, default=datetime.now())
    revoked = Column(Boolean, default=False)
    user = relationship("User", back_populates="tokens")


