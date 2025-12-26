"""
Job Description API endpoints

This is Step 1 of the 1-2-3 workflow: Context Capture
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import JobDescription
from app.schemas import (
    JobDescriptionCreate,
    JobDescriptionUpdate,
    JobDescriptionResponse,
)

router = APIRouter()


@router.post("/", response_model=JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_job_description(jd: JobDescriptionCreate, db: Session = Depends(get_db)):
    """
    Create a new job description.

    Step 1 of the 1-2-3 workflow: User pastes a JD here.
    TODO: Add AI keyword extraction logic here.
    """
    # TODO: Implement AI-based keyword extraction
    # For now, create JD with raw data only
    db_jd = JobDescription(**jd.model_dump())

    # TODO: Extract keywords, skills, and other insights
    # db_jd.extracted_keywords = extract_keywords(jd.raw_description)
    # db_jd.required_skills = extract_skills(jd.raw_description)
    # db_jd.keyword_density = calculate_density(jd.raw_description)
    # db_jd.action_verbs_used = extract_action_verbs(jd.raw_description)

    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)
    return db_jd


@router.get("/", response_model=List[JobDescriptionResponse])
def get_job_descriptions(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    company_filter: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all job descriptions with optional filtering.
    """
    query = db.query(JobDescription)

    if status_filter:
        query = query.filter(JobDescription.application_status == status_filter)
    if company_filter:
        query = query.filter(JobDescription.company_name.contains(company_filter))

    return query.offset(skip).limit(limit).all()


@router.get("/{jd_id}", response_model=JobDescriptionResponse)
def get_job_description(jd_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job description by ID.
    """
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )
    return jd


@router.patch("/{jd_id}", response_model=JobDescriptionResponse)
def update_job_description(jd_id: int, jd_update: JobDescriptionUpdate, db: Session = Depends(get_db)):
    """
    Update a job description.
    """
    db_jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not db_jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    update_data = jd_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_jd, field, value)

    db.commit()
    db.refresh(db_jd)
    return db_jd


@router.delete("/{jd_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_description(jd_id: int, db: Session = Depends(get_db)):
    """
    Delete a job description.
    WARNING: This will also delete all associated applications.
    """
    db_jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not db_jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    db.delete(db_jd)
    db.commit()
    return None
