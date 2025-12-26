"""
Brick schemas for API validation and serialization

Bricks are reusable pieces of the master profile that can be
selected and combined to create tailored resumes.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.bricks import SkillCategory


# ============================================================================
# PROJECT SCHEMAS
# ============================================================================

class ProjectBase(BaseModel):
    """Base project schema"""
    title: str
    description: str
    technologies: Optional[str] = None
    role: Optional[str] = None
    link: Optional[str] = None
    impact_metrics: Optional[str] = None
    is_featured: bool = False
    tags: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)"""
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    role: Optional[str] = None
    link: Optional[str] = None
    impact_metrics: Optional[str] = None
    is_featured: Optional[bool] = None
    tags: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Schema for project responses"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SKILL SCHEMAS
# ============================================================================

class SkillBase(BaseModel):
    """Base skill schema"""
    name: str
    category: SkillCategory = SkillCategory.OTHER
    proficiency: Optional[str] = None
    years_of_experience: Optional[int] = None
    synonyms: Optional[str] = None
    is_certified: bool = False


class SkillCreate(SkillBase):
    """Schema for creating a new skill"""
    pass


class SkillUpdate(BaseModel):
    """Schema for updating a skill (all fields optional)"""
    name: Optional[str] = None
    category: Optional[SkillCategory] = None
    proficiency: Optional[str] = None
    years_of_experience: Optional[int] = None
    synonyms: Optional[str] = None
    is_certified: Optional[bool] = None


class SkillResponse(SkillBase):
    """Schema for skill responses"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# EXPERIENCE BULLET SCHEMAS
# ============================================================================

class ExperienceBulletBase(BaseModel):
    """Base experience bullet schema"""
    company_name: str
    job_title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullet_text: str
    has_metrics: bool = False
    impact_keywords: Optional[str] = None
    is_leadership: bool = False
    is_technical: bool = False
    is_featured: bool = False
    tags: Optional[str] = None


class ExperienceBulletCreate(ExperienceBulletBase):
    """Schema for creating a new experience bullet"""
    pass


class ExperienceBulletUpdate(BaseModel):
    """Schema for updating an experience bullet (all fields optional)"""
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullet_text: Optional[str] = None
    has_metrics: Optional[bool] = None
    impact_keywords: Optional[str] = None
    is_leadership: Optional[bool] = None
    is_technical: Optional[bool] = None
    is_featured: Optional[bool] = None
    tags: Optional[str] = None


class ExperienceBulletResponse(ExperienceBulletBase):
    """Schema for experience bullet responses"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ACHIEVEMENT SCHEMAS
# ============================================================================

class AchievementBase(BaseModel):
    """Base achievement schema"""
    title: str
    description: Optional[str] = None
    date_received: Optional[str] = None
    issuing_organization: Optional[str] = None


class AchievementCreate(AchievementBase):
    """Schema for creating a new achievement"""
    pass


class AchievementUpdate(BaseModel):
    """Schema for updating an achievement (all fields optional)"""
    title: Optional[str] = None
    description: Optional[str] = None
    date_received: Optional[str] = None
    issuing_organization: Optional[str] = None


class AchievementResponse(AchievementBase):
    """Schema for achievement responses"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# EDUCATION SCHEMAS
# ============================================================================

class EducationBase(BaseModel):
    """Base education schema"""
    degree: str
    field_of_study: Optional[str] = None
    institution: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[str] = None
    relevant_coursework: Optional[str] = None


class EducationCreate(EducationBase):
    """Schema for creating a new education entry"""
    pass


class EducationUpdate(BaseModel):
    """Schema for updating an education entry (all fields optional)"""
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[str] = None
    relevant_coursework: Optional[str] = None


class EducationResponse(EducationBase):
    """Schema for education responses"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# CERTIFICATION SCHEMAS
# ============================================================================

class CertificationBase(BaseModel):
    """Base certification schema"""
    name: str
    issuing_organization: str
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class CertificationCreate(CertificationBase):
    """Schema for creating a new certification"""
    pass


class CertificationUpdate(BaseModel):
    """Schema for updating a certification (all fields optional)"""
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class CertificationResponse(CertificationBase):
    """Schema for certification responses"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
