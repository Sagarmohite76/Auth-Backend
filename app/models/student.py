from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from models import Base,User
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    full_name = Column(String(100), nullable=False)
    age = Column(Integer)
    class_name = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="students")
    predictions = relationship(
        "Prediction",
        back_populates="students",
        cascade="all, delete"
    )
    performances = relationship(
        "Performance",
        back_populates="students",
        cascade="all, delete"
    )

