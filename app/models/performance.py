from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from models import Base
from sqlalchemy.sql import func

class Performance(Base):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True, autoincrement=True)

    student_id = Column(
        Integer,
        ForeignKey('students.id', ondelete='CASCADE'),
        nullable=False
    )

    study_hours = Column(Float)
    attendance = Column(Float)
    previous_score = Column(Float)
    assignments_completed = Column(Integer)
    extracurricular = Column(Boolean)

    created_at = Column(TIMESTAMP, server_default=func.now())

    students = relationship("Student", back_populates="performances")
    predictions = relationship(
        "Prediction",
        back_populates="performance",
        cascade="all, delete"
    )