from sqlalchemy import Column, Integer , String,ForeignKey,Enum,Float,TIMESTAMP
from sqlalchemy.sql import func
from models import Base
from sqlalchemy.orm import relationship

class Prediction(Base):
    __tablename__="predictions"

    id=Column(Integer,primary_key=True,autoincrement=True)
    student_id = Column(
        Integer,
        ForeignKey('students.id', ondelete='CASCADE'),
        nullable=False
    )
    performance_id = Column(
        Integer,
        ForeignKey('performance.id', ondelete='CASCADE'),
        nullable=False
    )
    predicted_label = Column(
        Enum('Pass', 'Fail', name='prediction_label_enum'),
        nullable=False
    )

    probability_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())

    students = relationship("Student", back_populates="predictions")
    performance = relationship("Performance", back_populates="predictions")
