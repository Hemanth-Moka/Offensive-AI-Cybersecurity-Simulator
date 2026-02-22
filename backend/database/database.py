"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os

from config import DATABASE_URL
from database.models import Base

# Create database engine
# Use StaticPool for SQLite testing
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def drop_db():
    """Drop all tables - use with caution"""
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped!")
