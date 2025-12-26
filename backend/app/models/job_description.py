"""
Job Description model - Stores pasted JDs and extracted insights

This is Step 1 of the 1-2-3 workflow: Context Capture
"""

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class JobDescription(Base):
    """
    Stores a job description with AI-extracted keywords and requirements.
    This is the input that drives the tailoring process.
    """

    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)

    # Company & Position
    company_name = Column(String(255), nullable=False, index=True)
    job_title = Column(String(255), nullable=False)
    job_url = Column(String(500))

    # The Raw JD (what user pastes in)
    raw_description = Column(Text, nullable=False)

    # AI-Extracted Insights
    extracted_keywords = Column(JSON)  # List of important keywords
    required_skills = Column(JSON)  # Skills mentioned in JD
    preferred_skills = Column(JSON)  # Nice-to-have skills
    experience_level = Column(String(50))  # Junior, Mid, Senior, etc.
    salary_range = Column(String(100))  # If mentioned

    # ATS Optimization Data
    keyword_density = Column(JSON)  # Frequency of keywords
    action_verbs_used = Column(JSON)  # "Led", "Managed", "Developed"

    # Additional Context
    company_description = Column(Text)
    benefits = Column(Text)
    application_deadline = Column(String(50))

    # Status
    application_status = Column(String(50), default="saved")  # saved, applied, interviewing, etc.
    notes = Column(Text)

    # Relationships
    applications = relationship("Application", back_populates="job_description", cascade="all, delete-orphan")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<JobDescription(id={self.id}, company='{self.company_name}', title='{self.job_title}')>"
