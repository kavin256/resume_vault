"""
Brick models - Reusable pieces of the Master Profile

These are the "building blocks" that get selected and combined
to create tailored resumes. Each brick is:
- Self-contained
- Truthful (from real experience)
- Reusable across multiple resumes
- Selectable by the AI based on job requirements
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
import enum


class SkillCategory(str, enum.Enum):
    """Skill categories for better organization"""
    TECHNICAL = "technical"
    SOFT = "soft"
    LANGUAGE = "language"
    TOOL = "tool"
    FRAMEWORK = "framework"
    OTHER = "other"


class Project(Base):
    """
    A single project - reusable brick.
    Can be personal, professional, open-source, etc.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Project Info
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)  # What it does
    technologies = Column(Text)  # Comma-separated or JSON list
    role = Column(String(255))  # Your role in the project
    link = Column(String(500))  # GitHub, live demo, etc.

    # Impact metrics (important for ATS)
    impact_metrics = Column(Text)  # e.g., "Increased efficiency by 40%"

    # Categorization
    is_featured = Column(Boolean, default=False)  # Star projects
    tags = Column(Text)  # Keywords for matching

    # Relationships
    user = relationship("User", back_populates="projects")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}')>"


class Skill(Base):
    """
    A single skill - reusable brick.
    Can be technical, soft skill, language, etc.
    """

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Skill Info
    name = Column(String(255), nullable=False)
    category = Column(Enum(SkillCategory), default=SkillCategory.OTHER)
    proficiency = Column(String(50))  # Beginner, Intermediate, Advanced, Expert
    years_of_experience = Column(Integer)

    # Synonyms for ATS matching
    synonyms = Column(Text)  # e.g., "JavaScript, JS, ECMAScript"

    # Verification
    is_certified = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="skills")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', category='{self.category}')>"


class ExperienceBullet(Base):
    """
    A single bullet point from work experience - reusable brick.
    These are the most important for tailoring.
    """

    __tablename__ = "experience_bullets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Company/Role Context
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    start_date = Column(String(50))  # "Jan 2020"
    end_date = Column(String(50))  # "Present" or "Dec 2022"

    # The Bullet Point (STAR format recommended)
    bullet_text = Column(Text, nullable=False)

    # Metrics/Impact (extracted)
    has_metrics = Column(Boolean, default=False)
    impact_keywords = Column(Text)  # e.g., "increased, reduced, led, managed"

    # Categorization
    is_leadership = Column(Boolean, default=False)
    is_technical = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)  # Best bullets

    # Tags for matching
    tags = Column(Text)  # Keywords that might match JD

    # Relationships
    user = relationship("User", back_populates="experience_bullets")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ExperienceBullet(id={self.id}, company='{self.company_name}', role='{self.job_title}')>"


class Achievement(Base):
    """
    A single achievement/award - reusable brick.
    """

    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Achievement Info
    title = Column(String(500), nullable=False)
    description = Column(Text)
    date_received = Column(String(50))  # "2023"
    issuing_organization = Column(String(255))

    # Relationships
    user = relationship("User", back_populates="achievements")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Achievement(id={self.id}, title='{self.title}')>"


class Education(Base):
    """
    Education entry - reusable brick.
    """

    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Education Info
    degree = Column(String(255), nullable=False)  # "Bachelor of Science"
    field_of_study = Column(String(255))  # "Computer Science"
    institution = Column(String(255), nullable=False)
    start_date = Column(String(50))
    end_date = Column(String(50))
    gpa = Column(String(50))
    honors = Column(Text)  # Dean's List, Cum Laude, etc.
    relevant_coursework = Column(Text)

    # Relationships
    user = relationship("User", back_populates="education_items")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Education(id={self.id}, degree='{self.degree}', institution='{self.institution}')>"


class Certification(Base):
    """
    Certification - reusable brick.
    """

    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Certification Info
    name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=False)
    issue_date = Column(String(50))
    expiry_date = Column(String(50))
    credential_id = Column(String(255))
    credential_url = Column(String(500))

    # Relationships
    user = relationship("User", back_populates="certifications")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Certification(id={self.id}, name='{self.name}')>"
