"""
Job Description schemas for API validation and serialization

This is Step 1 of the 1-2-3 workflow: Context Capture
"""

from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class JobDescriptionBase(BaseModel):
    """Base job description schema"""
    company_name: str
    job_title: str
    job_url: Optional[str] = None
    raw_description: str
    company_description: Optional[str] = None
    benefits: Optional[str] = None
    application_deadline: Optional[str] = None
    notes: Optional[str] = None


class JobDescriptionCreate(JobDescriptionBase):
    """
    Schema for creating a new job description.
    AI extraction will be performed server-side.
    """
    pass


class JobDescriptionUpdate(BaseModel):
    """Schema for updating a job description (all fields optional)"""
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    job_url: Optional[str] = None
    raw_description: Optional[str] = None
    company_description: Optional[str] = None
    benefits: Optional[str] = None
    application_deadline: Optional[str] = None
    application_status: Optional[str] = None
    notes: Optional[str] = None


class JobDescriptionResponse(JobDescriptionBase):
    """
    Schema for job description responses.
    Includes AI-extracted insights.
    """
    id: int

    # AI-Extracted Insights
    extracted_keywords: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    keyword_density: Optional[Dict[str, int]] = None
    action_verbs_used: Optional[List[str]] = None

    # Status
    application_status: Optional[str] = "saved"

    # Metadata
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobDescriptionWithStats(JobDescriptionResponse):
    """
    Extended schema with application statistics.
    Shows how many times this JD was used.
    """
    applications_count: int = 0
