import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base
import uuid, datetime

Base = declarative_base()

def uuid4():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.String, primary_key=True, default=uuid4)
    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    password_hash = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    id = sa.Column(sa.String, primary_key=True, default=uuid4)
    owner_id = sa.Column(sa.String, sa.ForeignKey("users.id"))
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="projects")
