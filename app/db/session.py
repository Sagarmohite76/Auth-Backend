from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import Config

engine=create_engine(Config.DATABASE_URL,echo=True)

SessionLocal=sessionmaker(
    autoflush=False,
    bind=engine
)

