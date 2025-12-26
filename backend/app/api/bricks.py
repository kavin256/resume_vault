"""
Bricks API endpoints

CRUD operations for all brick types:
- Projects
- Skills
- Experience Bullets
- Achievements
- Education
- Certifications
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import (
    Project,
    Skill,
    ExperienceBullet,
    Achievement,
    Education,
    Certification,
)
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    ExperienceBulletCreate,
    ExperienceBulletUpdate,
    ExperienceBulletResponse,
    AchievementCreate,
    AchievementUpdate,
    AchievementResponse,
    EducationCreate,
    EducationUpdate,
    EducationResponse,
    CertificationCreate,
    CertificationUpdate,
    CertificationResponse,
)

router = APIRouter()


# ============================================================================
# PROJECTS
# ============================================================================

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new project brick."""
    db_project = Project(**project.model_dump(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(user_id: int, featured_only: bool = False, db: Session = Depends(get_db)):
    """Get all projects for a user."""
    query = db.query(Project).filter(Project.user_id == user_id)
    if featured_only:
        query = query.filter(Project.is_featured == True)
    return query.all()


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    db.delete(db_project)
    db.commit()
    return None


# ============================================================================
# SKILLS
# ============================================================================

@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill: SkillCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new skill brick."""
    db_skill = Skill(**skill.model_dump(), user_id=user_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.get("/skills", response_model=List[SkillResponse])
def get_skills(
    user_id: int,
    category: str = None,
    certified_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all skills for a user."""
    query = db.query(Skill).filter(Skill.user_id == user_id)
    if category:
        query = query.filter(Skill.category == category)
    if certified_only:
        query = query.filter(Skill.is_certified == True)
    return query.all()


@router.get("/skills/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get a specific skill."""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return skill


@router.patch("/skills/{skill_id}", response_model=SkillResponse)
def update_skill(skill_id: int, skill_update: SkillUpdate, db: Session = Depends(get_db)):
    """Update a skill."""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

    update_data = skill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill, field, value)

    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    """Delete a skill."""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

    db.delete(db_skill)
    db.commit()
    return None


# ============================================================================
# EXPERIENCE BULLETS
# ============================================================================

@router.post("/experience", response_model=ExperienceBulletResponse, status_code=status.HTTP_201_CREATED)
def create_experience_bullet(bullet: ExperienceBulletCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new experience bullet brick."""
    db_bullet = ExperienceBullet(**bullet.model_dump(), user_id=user_id)
    db.add(db_bullet)
    db.commit()
    db.refresh(db_bullet)
    return db_bullet


@router.get("/experience", response_model=List[ExperienceBulletResponse])
def get_experience_bullets(
    user_id: int,
    company_name: str = None,
    featured_only: bool = False,
    leadership_only: bool = False,
    technical_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all experience bullets for a user."""
    query = db.query(ExperienceBullet).filter(ExperienceBullet.user_id == user_id)
    if company_name:
        query = query.filter(ExperienceBullet.company_name == company_name)
    if featured_only:
        query = query.filter(ExperienceBullet.is_featured == True)
    if leadership_only:
        query = query.filter(ExperienceBullet.is_leadership == True)
    if technical_only:
        query = query.filter(ExperienceBullet.is_technical == True)
    return query.all()


@router.get("/experience/{bullet_id}", response_model=ExperienceBulletResponse)
def get_experience_bullet(bullet_id: int, db: Session = Depends(get_db)):
    """Get a specific experience bullet."""
    bullet = db.query(ExperienceBullet).filter(ExperienceBullet.id == bullet_id).first()
    if not bullet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience bullet not found")
    return bullet


@router.patch("/experience/{bullet_id}", response_model=ExperienceBulletResponse)
def update_experience_bullet(bullet_id: int, bullet_update: ExperienceBulletUpdate, db: Session = Depends(get_db)):
    """Update an experience bullet."""
    db_bullet = db.query(ExperienceBullet).filter(ExperienceBullet.id == bullet_id).first()
    if not db_bullet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience bullet not found")

    update_data = bullet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bullet, field, value)

    db.commit()
    db.refresh(db_bullet)
    return db_bullet


@router.delete("/experience/{bullet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience_bullet(bullet_id: int, db: Session = Depends(get_db)):
    """Delete an experience bullet."""
    db_bullet = db.query(ExperienceBullet).filter(ExperienceBullet.id == bullet_id).first()
    if not db_bullet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience bullet not found")

    db.delete(db_bullet)
    db.commit()
    return None


# ============================================================================
# ACHIEVEMENTS
# ============================================================================

@router.post("/achievements", response_model=AchievementResponse, status_code=status.HTTP_201_CREATED)
def create_achievement(achievement: AchievementCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new achievement brick."""
    db_achievement = Achievement(**achievement.model_dump(), user_id=user_id)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


@router.get("/achievements", response_model=List[AchievementResponse])
def get_achievements(user_id: int, db: Session = Depends(get_db)):
    """Get all achievements for a user."""
    return db.query(Achievement).filter(Achievement.user_id == user_id).all()


@router.get("/achievements/{achievement_id}", response_model=AchievementResponse)
def get_achievement(achievement_id: int, db: Session = Depends(get_db)):
    """Get a specific achievement."""
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")
    return achievement


@router.patch("/achievements/{achievement_id}", response_model=AchievementResponse)
def update_achievement(achievement_id: int, achievement_update: AchievementUpdate, db: Session = Depends(get_db)):
    """Update an achievement."""
    db_achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not db_achievement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")

    update_data = achievement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_achievement, field, value)

    db.commit()
    db.refresh(db_achievement)
    return db_achievement


@router.delete("/achievements/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    """Delete an achievement."""
    db_achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not db_achievement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")

    db.delete(db_achievement)
    db.commit()
    return None


# ============================================================================
# EDUCATION
# ============================================================================

@router.post("/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
def create_education(education: EducationCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new education brick."""
    db_education = Education(**education.model_dump(), user_id=user_id)
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


@router.get("/education", response_model=List[EducationResponse])
def get_education(user_id: int, db: Session = Depends(get_db)):
    """Get all education entries for a user."""
    return db.query(Education).filter(Education.user_id == user_id).all()


@router.get("/education/{education_id}", response_model=EducationResponse)
def get_education_item(education_id: int, db: Session = Depends(get_db)):
    """Get a specific education entry."""
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
    return education


@router.patch("/education/{education_id}", response_model=EducationResponse)
def update_education(education_id: int, education_update: EducationUpdate, db: Session = Depends(get_db)):
    """Update an education entry."""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")

    update_data = education_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_education, field, value)

    db.commit()
    db.refresh(db_education)
    return db_education


@router.delete("/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(education_id: int, db: Session = Depends(get_db)):
    """Delete an education entry."""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")

    db.delete(db_education)
    db.commit()
    return None


# ============================================================================
# CERTIFICATIONS
# ============================================================================

@router.post("/certifications", response_model=CertificationResponse, status_code=status.HTTP_201_CREATED)
def create_certification(certification: CertificationCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new certification brick."""
    db_certification = Certification(**certification.model_dump(), user_id=user_id)
    db.add(db_certification)
    db.commit()
    db.refresh(db_certification)
    return db_certification


@router.get("/certifications", response_model=List[CertificationResponse])
def get_certifications(user_id: int, db: Session = Depends(get_db)):
    """Get all certifications for a user."""
    return db.query(Certification).filter(Certification.user_id == user_id).all()


@router.get("/certifications/{certification_id}", response_model=CertificationResponse)
def get_certification(certification_id: int, db: Session = Depends(get_db)):
    """Get a specific certification."""
    certification = db.query(Certification).filter(Certification.id == certification_id).first()
    if not certification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")
    return certification


@router.patch("/certifications/{certification_id}", response_model=CertificationResponse)
def update_certification(certification_id: int, certification_update: CertificationUpdate, db: Session = Depends(get_db)):
    """Update a certification."""
    db_certification = db.query(Certification).filter(Certification.id == certification_id).first()
    if not db_certification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")

    update_data = certification_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_certification, field, value)

    db.commit()
    db.refresh(db_certification)
    return db_certification


@router.delete("/certifications/{certification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(certification_id: int, db: Session = Depends(get_db)):
    """Delete a certification."""
    db_certification = db.query(Certification).filter(Certification.id == certification_id).first()
    if not db_certification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")

    db.delete(db_certification)
    db.commit()
    return None
