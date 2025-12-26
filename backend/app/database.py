"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config.settings import settings
from app.models.base import Base

# TODO: Cloud Database Integration
# When migrating to production with a cloud database:
# 1. Update the DATABASE_URL in .env to point to your cloud database
# 2. Consider using connection pooling for better performance:
#    engine = create_engine(
#        settings.database_url,
#        pool_size=20,
#        max_overflow=0,
#        pool_pre_ping=True,  # Verify connections before using
#        pool_recycle=3600,   # Recycle connections after 1 hour
#    )
# 3. For PostgreSQL, consider using asyncpg for async support
# 4. Implement proper database migration strategy using Alembic
# 5. Set up database backups and disaster recovery
# 6. Configure SSL/TLS for secure connections

# Create database engine
# For SQLite, check_same_thread=False is needed for FastAPI
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    echo=True if settings.env == "development" else False,  # Log SQL queries in development
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    Yields a database session and ensures it's closed after use.

    Usage in FastAPI endpoints:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    This should be called on application startup.

    TODO: In production, use Alembic for database migrations instead of create_all()
    Alembic provides version control for your database schema.
    """
    # Import all models here to ensure they are registered with Base
    from app.models import (
        User,
        Project,
        Skill,
        ExperienceBullet,
        Achievement,
        Education,
        Certification,
        JobDescription,
        Application,
        ApplicationVersion,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_db() -> None:
    """
    Drop all database tables.
    WARNING: This will delete all data! Use only in development.
    """
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped!")


if __name__ == "__main__":
    # Run this file directly to initialize the database
    print("Initializing database...")
    init_db()
