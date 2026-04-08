from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from models import Base
from sqlalchemy.orm import Session,relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "student"), default="student")
    created_at = Column(DateTime, default=datetime.utcnow)
    students = relationship(
        "Student",
        back_populates="user",
        cascade="all, delete"
    )


def create_user(db: Session, name: str, email: str, password: str):
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":"user added successfully."}

def get_users(db):
    return db.query(User).all()

def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user

def update_password(email: str, new_password_hash: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    user.password= new_password_hash
    db.commit()
    db.refresh(user)
    
    return user