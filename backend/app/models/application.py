"""
Application model - Links JD, selected bricks, and generated resume

This is the "Application Vault" - the record-keeping system
"""

from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Application(Base):
    """
    An application record that ties together:
    - The job description
    - Which bricks were selected
    - The generated resume
    - Application tracking info

    This is what makes Resume Vault a "vault" - permanent record keeping.
    """

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False, index=True)

    # Application Tracking
    application_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="draft")  # draft, submitted, interviewing, offer, rejected
    applied_via = Column(String(100))  # LinkedIn, Indeed, Company Website, etc.

    # Selected Bricks (IDs of bricks used in this resume)
    selected_projects = Column(JSON)  # List of project IDs
    selected_skills = Column(JSON)  # List of skill IDs
    selected_experience_bullets = Column(JSON)  # List of bullet IDs
    selected_achievements = Column(JSON)  # List of achievement IDs
    selected_education = Column(JSON)  # List of education IDs
    selected_certifications = Column(JSON)  # List of certification IDs

    # Tailoring Metadata
    match_score = Column(Float)  # 0-100% match with JD
    keywords_matched = Column(JSON)  # Which keywords from JD were matched
    template_used = Column(String(100))  # Which template (ATS, Creative, etc.)

    # Generated Resume
    resume_content_markdown = Column(Text)  # The generated content
    resume_file_path = Column(String(500))  # Path to PDF file
    resume_file_name = Column(String(255))  # e.g., "Google-Senior_Developer-2025-01-15.pdf"

    # ATS Optimization Report
    ats_score = Column(Float)  # 0-100
    ats_suggestions = Column(JSON)  # AI suggestions for improvement

    # Follow-up Tracking
    follow_up_date = Column(DateTime(timezone=True))
    interview_date = Column(DateTime(timezone=True))
    notes = Column(Text)

    # Archive Flag
    is_archived = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="applications")
    job_description = relationship("JobDescription", back_populates="applications")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Application(id={self.id}, company='{self.job_description.company_name if self.job_description else 'Unknown'}', status='{self.status}')>"


class ApplicationVersion(Base):
    """
    Stores versions of an application if the user regenerates/tweaks it.
    This allows them to A/B test different approaches.
    """

    __tablename__ = "application_versions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)

    version_number = Column(Integer, nullable=False)  # 1, 2, 3, etc.
    resume_content_markdown = Column(Text)
    resume_file_path = Column(String(500))
    changes_made = Column(Text)  # Description of what changed
    is_sent = Column(Boolean, default=False)  # Was this version actually sent?

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ApplicationVersion(id={self.id}, application_id={self.application_id}, version={self.version_number})>"
