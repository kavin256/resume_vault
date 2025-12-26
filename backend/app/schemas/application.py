"""
Application schemas for API validation and serialization

This is the Application Vault - the record-keeping system
that ties together JD, selected bricks, and generated resume.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


# ============================================================================
# APPLICATION VERSION SCHEMAS
# ============================================================================

class ApplicationVersionBase(BaseModel):
    """Base application version schema"""
    version_number: int
    resume_content_markdown: Optional[str] = None
    resume_file_path: Optional[str] = None
    changes_made: Optional[str] = None
    is_sent: bool = False


class ApplicationVersionCreate(ApplicationVersionBase):
    """Schema for creating a new application version"""
    application_id: int


class ApplicationVersionResponse(ApplicationVersionBase):
    """Schema for application version responses"""
    id: int
    application_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# APPLICATION SCHEMAS
# ============================================================================

class ApplicationBase(BaseModel):
    """Base application schema"""
    job_description_id: int
    status: str = "draft"
    applied_via: Optional[str] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """
    Schema for creating a new application.
    This is triggered by the 1-2-3 workflow.
    """
    # Selected brick IDs
    selected_projects: Optional[List[int]] = None
    selected_skills: Optional[List[int]] = None
    selected_experience_bullets: Optional[List[int]] = None
    selected_achievements: Optional[List[int]] = None
    selected_education: Optional[List[int]] = None
    selected_certifications: Optional[List[int]] = None


class ApplicationUpdate(BaseModel):
    """Schema for updating an application (all fields optional)"""
    status: Optional[str] = None
    applied_via: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    is_archived: Optional[bool] = None


class ApplicationResponse(ApplicationBase):
    """
    Schema for application responses.
    Includes all metadata and selected bricks.
    """
    id: int
    user_id: int

    # Application tracking
    application_date: datetime

    # Selected bricks (IDs)
    selected_projects: Optional[List[int]] = None
    selected_skills: Optional[List[int]] = None
    selected_experience_bullets: Optional[List[int]] = None
    selected_achievements: Optional[List[int]] = None
    selected_education: Optional[List[int]] = None
    selected_certifications: Optional[List[int]] = None

    # Tailoring metadata
    match_score: Optional[float] = None
    keywords_matched: Optional[List[str]] = None
    template_used: Optional[str] = None

    # Generated resume
    resume_content_markdown: Optional[str] = None
    resume_file_path: Optional[str] = None
    resume_file_name: Optional[str] = None

    # ATS optimization
    ats_score: Optional[float] = None
    ats_suggestions: Optional[List[str]] = None

    # Follow-up tracking
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None

    # Archive flag
    is_archived: bool = False

    # Metadata
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApplicationWithDetails(ApplicationResponse):
    """
    Extended schema with full JD details.
    Used for detailed views.
    """
    company_name: Optional[str] = None
    job_title: Optional[str] = None


class TailorRequest(BaseModel):
    """
    Schema for the 1-2-3 tailoring workflow.

    Step 1: User pastes JD (creates JobDescription)
    Step 2: AI selects bricks (this request)
    Step 3: Generate resume (this returns Application)
    """
    job_description_id: int

    # Optional: User can override AI selections
    selected_projects: Optional[List[int]] = None
    selected_skills: Optional[List[int]] = None
    selected_experience_bullets: Optional[List[int]] = None
    selected_achievements: Optional[List[int]] = None
    selected_education: Optional[List[int]] = None
    selected_certifications: Optional[List[int]] = None

    # Template selection
    template: str = "ats_optimized"  # ats_optimized, creative, corporate


class TailorResponse(BaseModel):
    """
    Response from the tailoring engine.

    Contains the application ID and preview of selected bricks.
    """
    application_id: int
    match_score: float
    keywords_matched: List[str]
    ats_score: float

    # Preview of selected bricks
    selected_bricks_count: Dict[str, int]  # {"projects": 3, "skills": 12, etc.}

    # Suggestions for improvement
    suggestions: List[str]

    # Generated resume preview
    resume_preview: str
