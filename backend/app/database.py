"""
Database setup using SQLAlchemy.

Data is stored in a real database (SQLite by default) so farmers, farms, soil
records and pest reports survive server restarts. Switch to PostgreSQL later by
changing DATABASE_URL in .env -- no code changes needed.
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

# SQLite needs this flag when used with FastAPI's threaded request handling.
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_db():
    """FastAPI dependency that yields a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables if they don't exist yet."""
    # Import models so they're registered on Base before create_all.
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
