from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from werkzeug.security import check_password_hash, generate_password_hash
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(10), default="member")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
    modified = Column(DateTime, server_default=text('now()'))
    is_active = Column(Boolean, default=True)
    appointment = relationship("Appointment", back_populates="owner")
    # Hash password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    # Check password
    def check_password(self, password):
        return check_password_hash(self.password, password)