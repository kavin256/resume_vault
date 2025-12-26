"""
Pydantic schemas for API validation and serialization
"""

# User schemas
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
)

# Brick schemas
from .bricks import (
    # Projects
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    # Skills
    SkillBase,
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    # Experience Bullets
    ExperienceBulletBase,
    ExperienceBulletCreate,
    ExperienceBulletUpdate,
    ExperienceBulletResponse,
    # Achievements
    AchievementBase,
    AchievementCreate,
    AchievementUpdate,
    AchievementResponse,
    # Education
    EducationBase,
    EducationCreate,
    EducationUpdate,
    EducationResponse,
    # Certifications
    CertificationBase,
    CertificationCreate,
    CertificationUpdate,
    CertificationResponse,
)

# Job Description schemas
from .job_description import (
    JobDescriptionBase,
    JobDescriptionCreate,
    JobDescriptionUpdate,
    JobDescriptionResponse,
    JobDescriptionWithStats,
)

# Application schemas
from .application import (
    ApplicationVersionBase,
    ApplicationVersionCreate,
    ApplicationVersionResponse,
    ApplicationBase,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithDetails,
    TailorRequest,
    TailorResponse,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Projects
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    # Skills
    "SkillBase",
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    # Experience Bullets
    "ExperienceBulletBase",
    "ExperienceBulletCreate",
    "ExperienceBulletUpdate",
    "ExperienceBulletResponse",
    # Achievements
    "AchievementBase",
    "AchievementCreate",
    "AchievementUpdate",
    "AchievementResponse",
    # Education
    "EducationBase",
    "EducationCreate",
    "EducationUpdate",
    "EducationResponse",
    # Certifications
    "CertificationBase",
    "CertificationCreate",
    "CertificationUpdate",
    "CertificationResponse",
    # Job Descriptions
    "JobDescriptionBase",
    "JobDescriptionCreate",
    "JobDescriptionUpdate",
    "JobDescriptionResponse",
    "JobDescriptionWithStats",
    # Applications
    "ApplicationVersionBase",
    "ApplicationVersionCreate",
    "ApplicationVersionResponse",
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationWithDetails",
    "TailorRequest",
    "TailorResponse",
]
