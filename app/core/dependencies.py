from typing import Generator

def get_db() -> Generator:
    from db import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()