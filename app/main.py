# =========================
# Imports
# =========================
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, Float,
    Boolean, ForeignKey, TIMESTAMP, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
import enum

# =========================
# Config (Replace with your DB URL)
# =========================
class Config:
    DATABASE_URL = "sqlite:///./test.db"  # Example, replace with your DB URL

# =========================
# Base
# =========================
Base = declarative_base()

# =========================
# Enums
# =========================
class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

# =========================
# User Model
# =========================
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

# =========================
# Student Model
# =========================
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer)
    class_name = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="students")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete")
    performances = relationship("Performance", back_populates="student", cascade="all, delete")

# =========================
# Performance Model
# =========================
class Performance(Base):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    study_hours = Column(Float)
    attendance = Column(Float)
    previous_score = Column(Float)
    assignments_completed = Column(Integer)
    extracurricular = Column(Boolean)
    created_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="performances")
    predictions = relationship("Prediction", back_populates="performance", cascade="all, delete")

# =========================
# Prediction Model
# =========================
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    performance_id = Column(Integer, ForeignKey('performance.id', ondelete='CASCADE'), nullable=False)
    predicted_label = Column(Enum('Pass', 'Fail', name='prediction_label_enum'), nullable=False)
    probability_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="predictions")
    performance = relationship("Performance", back_populates="predictions")

# =========================
# Database
# =========================
engine = create_engine(
    Config.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create tables
Base.metadata.create_all(bind=engine)

# =========================
# FastAPI App
# =========================
app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# CRUD Functions
# =========================
def create_user(db: Session, name: str, email: str, password: str):
    user = User(name=name, email=email, password=password, role=RoleEnum.user)
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

# =========================
# API Endpoints
# =========================
@app.post("/users/")
def api_create_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, name, email, password)

@app.get("/users/")
def api_get_users(db: Session = Depends(get_db)):
    return get_users(db)

@app.put("/users/{email}/password")
def api_update_password(email: str, new_password: str, db: Session = Depends(get_db)):
    user = update_password(email, new_password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

print("🔥 APP STARTING...")