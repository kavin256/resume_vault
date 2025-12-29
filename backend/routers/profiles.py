"""
Master Profile Router
Handles master profile CRUD operations for authenticated users
"""

from fastapi import APIRouter, Depends, HTTPException, status
from database import get_database
from auth import verify_clerk_token
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profiles", tags=["profiles"])


# Pydantic models for Master Profile
class Location(BaseModel):
    city: str = ""
    country: str = ""


class PersonalInfo(BaseModel):
    firstName: str = ""
    lastName: str = ""
    email: str = ""
    phone: str = ""
    location: Location = Field(default_factory=Location)
    linkedinUrl: str = ""
    portfolioUrl: str = ""


class WorkExperience(BaseModel):
    jobTitle: str = ""
    companyName: str = ""
    employmentType: str = ""
    location: str = ""
    startDate: str = ""
    endDate: str = ""
    currentlyWorking: bool = False
    responsibilities: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: str = ""
    degree: str = ""
    fieldOfStudy: str = ""
    startYear: str = ""
    endYear: str = ""
    grade: str = ""
    description: str = ""


class Skill(BaseModel):
    name: str = ""
    level: str = ""


class Certification(BaseModel):
    name: str = ""
    issuingOrganization: str = ""
    issueDate: str = ""
    expirationDate: str = ""
    credentialId: str = ""
    credentialUrl: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    role: str = ""
    technologies: List[str] = Field(default_factory=list)
    startDate: str = ""
    endDate: str = ""
    url: str = ""
    highlights: List[str] = Field(default_factory=list)


class Volunteering(BaseModel):
    role: str = ""
    organization: str = ""
    startDate: str = ""
    endDate: str = ""
    description: str = ""


class Language(BaseModel):
    language: str = ""
    proficiency: str = ""


class Publication(BaseModel):
    title: str = ""
    publisher: str = ""
    date: str = ""
    url: str = ""
    description: str = ""


class SalaryExpectation(BaseModel):
    min: int = 0
    max: int = 0
    currency: str = "USD"
    period: str = "yearly"


class JobPreferences(BaseModel):
    desiredRoles: List[str] = Field(default_factory=list)
    desiredLocations: List[str] = Field(default_factory=list)
    employmentTypes: List[str] = Field(default_factory=list)
    remotePreference: str = ""
    salaryExpectation: SalaryExpectation = Field(default_factory=SalaryExpectation)
    willingToRelocate: bool = False
    availabilityDate: str = ""


class MasterProfile(BaseModel):
    userId: str
    personalInfo: PersonalInfo = Field(default_factory=PersonalInfo)
    professionalHeadline: str = ""
    summary: str = ""
    workExperience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    volunteering: List[Volunteering] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    publications: List[Publication] = Field(default_factory=list)
    jobPreferences: JobPreferences = Field(default_factory=JobPreferences)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class MasterProfileResponse(BaseModel):
    status: str
    profile: MasterProfile


def create_default_profile(user_id: str, first_name: str = "", last_name: str = "", email: str = "") -> dict:
    """
    Create a default master profile structure based on MasterProfile.json
    Pre-populates with user's basic information from their account
    """
    return {
        "userId": user_id,
        "personalInfo": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": "",
            "location": {
                "city": "",
                "country": ""
            },
            "linkedinUrl": "",
            "portfolioUrl": ""
        },
        "professionalHeadline": "",
        "summary": "",
        "workExperience": [],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": [],
        "volunteering": [],
        "languages": [],
        "publications": [],
        "jobPreferences": {
            "desiredRoles": [],
            "desiredLocations": [],
            "employmentTypes": [],
            "remotePreference": "",
            "salaryExpectation": {
                "min": 0,
                "max": 0,
                "currency": "USD",
                "period": "yearly"
            },
            "willingToRelocate": False,
            "availabilityDate": ""
        },
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }


@router.get("/me", response_model=MasterProfileResponse)
async def get_my_profile(token_payload: dict = Depends(verify_clerk_token)):
    """
    Get the authenticated user's master profile.
    
    If the profile doesn't exist, automatically creates one with default values
    populated from the user's account (firstName, lastName, email).
    
    Returns:
        MasterProfileResponse: The user's master profile
    """
    db = get_database()
    user_id = token_payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user_id not found"
        )
    
    # Try to get existing profile
    profile = await db.master_profiles.find_one({"userId": user_id})
    
    if profile:
        logger.info(f"✓ Loaded existing profile for user: {user_id}")
        profile.pop("_id", None)  # Remove MongoDB's _id field
        return MasterProfileResponse(
            status="loaded",
            profile=MasterProfile(**profile)
        )
    
    # Profile doesn't exist - get user info and create default profile
    logger.info(f"✓ Profile not found for user: {user_id}, creating default profile")
    
    # Get user info from users collection
    user = await db.users.find_one({"clerk_user_id": user_id})
    
    first_name = ""
    last_name = ""
    email = ""
    
    if user:
        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")
        email = user.get("email", "")
    else:
        # Fallback to token data if user not in DB yet
        email = token_payload.get("email", "")
        first_name = token_payload.get("given_name", "")
        last_name = token_payload.get("family_name", "")
    
    # Create default profile
    default_profile = create_default_profile(user_id, first_name, last_name, email)
    
    # Save to database
    await db.master_profiles.insert_one(default_profile.copy())
    
    logger.info(f"✓ Created default profile for user: {user_id}")
    
    default_profile.pop("_id", None)
    return MasterProfileResponse(
        status="created",
        profile=MasterProfile(**default_profile)
    )


@router.put("/me")
async def update_my_profile(
    profile_update: dict,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Update the authenticated user's master profile.
    
    Args:
        profile_update: Dictionary containing fields to update
        
    Returns:
        Updated profile
    """
    db = get_database()
    user_id = token_payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user_id not found"
        )
    
    # Update timestamp
    profile_update["updatedAt"] = datetime.utcnow()
    
    # Update profile
    result = await db.master_profiles.update_one(
        {"userId": user_id},
        {"$set": profile_update}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    logger.info(f"✓ Updated profile for user: {user_id}")
    
    # Return updated profile
    updated_profile = await db.master_profiles.find_one({"userId": user_id})
    updated_profile.pop("_id", None)
    
    return MasterProfileResponse(
        status="updated",
        profile=MasterProfile(**updated_profile)
    )


@router.delete("/me")
async def delete_my_profile(token_payload: dict = Depends(verify_clerk_token)):
    """
    Delete the authenticated user's master profile.
    
    Returns:
        Success message
    """
    db = get_database()
    user_id = token_payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user_id not found"
        )
    
    result = await db.master_profiles.delete_one({"userId": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    logger.info(f"✓ Deleted profile for user: {user_id}")
    
    return {
        "status": "deleted",
        "message": "Profile deleted successfully"
    }
