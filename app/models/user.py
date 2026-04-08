from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from models import Base
from sqlalchemy.orm import Session, relationship
import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum, name="user_role"), default=RoleEnum.user, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship(
        "Student",
        back_populates="user",
        cascade="all, delete"
    )


def create_user(db: Session, name: str, email: str, password: str):
    user = User(
        name=name,
        email=email,
        password=password,
        role=RoleEnum.user
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def update_password(email: str, new_password_hash: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    user.password = new_password_hash
    db.commit()
    db.refresh(user)

    return user