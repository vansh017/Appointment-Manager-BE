from typing import Generator
from db.session import SessionLocal
from fastapi import Request


def get_db(request: Request=None) -> Generator:
    db = None
    try:
        db = SessionLocal()
        # Since SQL Alchemy uses lazy initializing
        #   db connection is never opened here
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()

