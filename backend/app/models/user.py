"""
User model - Basic user information (simplified for now)
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class User(Base):
    """
    Basic user information.
    In future: Add authentication, email verification, etc.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50))
    location = Column(String(255))

    # Links
    linkedin_url = Column(String(500))
    portfolio_url = Column(String(500))
    github_url = Column(String(500))

    # Professional Summary (short)
    professional_summary = Column(String(1000))

    # Relationships to "bricks"
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")
    experience_bullets = relationship("ExperienceBullet", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    education_items = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="user", cascade="all, delete-orphan")

    # Relationships to applications
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.full_name}')>"
