"""
Applications API endpoints

This is the Application Vault and the core 1-2-3 tailoring workflow.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import (
    Application,
    ApplicationVersion,
    JobDescription,
    User,
)
from app.schemas import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithDetails,
    ApplicationVersionCreate,
    ApplicationVersionResponse,
    TailorRequest,
    TailorResponse,
)

router = APIRouter()


# ============================================================================
# APPLICATION CRUD
# ============================================================================

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create a new application manually.

    Note: Most applications will be created via the /tailor endpoint.
    """
    # Verify JD exists
    jd = db.query(JobDescription).filter(JobDescription.id == application.job_description_id).first()
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    db_application = Application(**application.model_dump(), user_id=user_id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.get("/", response_model=List[ApplicationResponse])
def get_applications(
    user_id: int,
    status_filter: str = None,
    archived: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all applications for a user.
    This is the Application Vault view.
    """
    query = db.query(Application).filter(Application.user_id == user_id)

    if status_filter:
        query = query.filter(Application.status == status_filter)
    if not archived:
        query = query.filter(Application.is_archived == False)

    return query.offset(skip).limit(limit).all()


@router.get("/{application_id}", response_model=ApplicationWithDetails)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """
    Get a specific application with full details.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    # Add JD details
    response = ApplicationWithDetails(**application.__dict__)
    if application.job_description:
        response.company_name = application.job_description.company_name
        response.job_title = application.job_description.job_title

    return response


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, application_update: ApplicationUpdate, db: Session = Depends(get_db)):
    """
    Update an application (e.g., change status, add notes).
    """
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    update_data = application_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_application, field, value)

    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """
    Delete an application.
    """
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    db.delete(db_application)
    db.commit()
    return None


# ============================================================================
# APPLICATION VERSIONS
# ============================================================================

@router.post("/{application_id}/versions", response_model=ApplicationVersionResponse, status_code=status.HTTP_201_CREATED)
def create_version(application_id: int, version: ApplicationVersionCreate, db: Session = Depends(get_db)):
    """
    Create a new version of an application for A/B testing.
    """
    # Verify application exists
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    db_version = ApplicationVersion(**version.model_dump())
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


@router.get("/{application_id}/versions", response_model=List[ApplicationVersionResponse])
def get_versions(application_id: int, db: Session = Depends(get_db)):
    """
    Get all versions of an application.
    """
    versions = db.query(ApplicationVersion).filter(
        ApplicationVersion.application_id == application_id
    ).order_by(ApplicationVersion.version_number).all()
    return versions


# ============================================================================
# TAILORING WORKFLOW (1-2-3)
# ============================================================================

@router.post("/tailor", response_model=TailorResponse)
def tailor_resume(request: TailorRequest, user_id: int, db: Session = Depends(get_db)):
    """
    The core 1-2-3 workflow: Generate a tailored resume.

    Step 1: User has already pasted JD (job_description_id)
    Step 2: AI selects bricks (or user can override)
    Step 3: Generate optimized resume

    TODO: Implement the intelligent tailoring engine.
    For now, this is a placeholder that creates an application.
    """
    # Verify JD exists
    jd = db.query(JobDescription).filter(JobDescription.id == request.job_description_id).first()
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # TODO: Implement intelligent brick selection
    # If user didn't provide selections, use AI to select bricks
    selected_projects = request.selected_projects or []
    selected_skills = request.selected_skills or []
    selected_experience_bullets = request.selected_experience_bullets or []
    selected_achievements = request.selected_achievements or []
    selected_education = request.selected_education or []
    selected_certifications = request.selected_certifications or []

    # TODO: Calculate match score based on JD keywords and selected bricks
    match_score = 0.0  # Placeholder

    # TODO: Calculate ATS score
    ats_score = 0.0  # Placeholder

    # TODO: Generate resume content
    resume_content = f"""
# {user.full_name}
{user.email} | {user.phone or ''} | {user.location or ''}

## Professional Summary
{user.professional_summary or 'No summary provided'}

## Skills
TODO: List selected skills

## Experience
TODO: List selected experience bullets

## Projects
TODO: List selected projects

## Education
TODO: List selected education

## Certifications
TODO: List selected certifications

## Achievements
TODO: List selected achievements
"""

    # Create application record
    db_application = Application(
        user_id=user_id,
        job_description_id=request.job_description_id,
        selected_projects=selected_projects,
        selected_skills=selected_skills,
        selected_experience_bullets=selected_experience_bullets,
        selected_achievements=selected_achievements,
        selected_education=selected_education,
        selected_certifications=selected_certifications,
        match_score=match_score,
        keywords_matched=[],  # TODO: Extract from JD
        template_used=request.template,
        resume_content_markdown=resume_content,
        resume_file_name=f"{jd.company_name}-{jd.job_title.replace(' ', '_')}.pdf",
        ats_score=ats_score,
        ats_suggestions=[],  # TODO: Generate suggestions
        status="draft",
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    # Prepare response
    response = TailorResponse(
        application_id=db_application.id,
        match_score=match_score,
        keywords_matched=[],
        ats_score=ats_score,
        selected_bricks_count={
            "projects": len(selected_projects),
            "skills": len(selected_skills),
            "experience_bullets": len(selected_experience_bullets),
            "achievements": len(selected_achievements),
            "education": len(selected_education),
            "certifications": len(selected_certifications),
        },
        suggestions=[
            "TODO: Add more quantifiable achievements",
            "TODO: Include more keywords from job description",
            "TODO: Highlight leadership experience",
        ],
        resume_preview=resume_content[:500] + "...",
    )

    return response
