from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Render injects DATABASE_URL automatically when a Postgres DB is linked.
    # Normalize postgres:// → postgresql+psycopg2:// for SQLAlchemy compatibility.
    _raw_url = os.getenv("DATABASE_URL", "").strip()
    DATABASE_URL = _raw_url.replace("postgres://", "postgresql+psycopg2://", 1)

    SENDER_EMAIL = os.getenv("Sender_Email", "").strip()
    APP_PASSWORD  = os.getenv("App_Password", "").strip()
