from typing import Generator
import contextlib

@contextlib.contextmanager
def get_db_context():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
