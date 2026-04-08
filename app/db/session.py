from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import Config

engine = create_engine(
    Config.DATABASE_URL,
    echo=False,           # set True only for local debugging
    pool_pre_ping=True,   # reconnect if an idle connection was dropped (critical on Render free tier)
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
