from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Render injects DATABASE_URL automatically for linked Postgres services.
    # Fall back to building the URL from individual vars for local development.
    _db_url = os.getenv("DATABASE_URL", "").strip()

    if not _db_url:
        DB_HOST     = os.getenv("DB_Host", "localhost").strip()
        DB_USER     = os.getenv("DB_User", "root").strip()
        DB_PASSWORD = os.getenv("DB_Password", "").strip()
        DB_NAME     = os.getenv("DB_Name", "").strip()
        _db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    # SQLAlchemy requires "postgresql+psycopg2://..." — Render may return
    # "postgres://..." (old Heroku-style), so normalise if needed.
    DATABASE_URL = _db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    SENDER_EMAIL = os.getenv("Sender_Email", "").strip()
    APP_PASSWORD  = os.getenv("App_Password", "").strip()