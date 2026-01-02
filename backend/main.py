"""
Resume Vault Backend - FastAPI
AI-powered resume and cover letter generation
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import os
import logging
from contextlib import asynccontextmanager

# Import database and router modules
from database import connect_to_mongo, close_mongo_connection, get_database
from routers import users, profiles, resumes
from routers.profiles import MasterProfile  # Use comprehensive MasterProfile model
from auth import verify_clerk_token  # Import authentication

# Import AI services
from services.ai_factory import AIProviderFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    print("Starting Resume Vault Backend...")
    await connect_to_mongo()

    # Create MongoDB indexes
    db = get_database()
    await db["users"].create_index("clerk_user_id", unique=True)
    await db["users"].create_index("email")  # For orphaned account lookups
    await db["master_profiles"].create_index("userId", unique=True)  # Master profile index
    await db["resume_generations"].create_index("userId")  # Resume generations by user
    await db["resume_generations"].create_index("jobApplicationId", unique=True)  # Unique job application ID
    print("✓ MongoDB indexes created")

    # Validate AI provider
    print("Validating AI provider...")
    ai_valid = await AIProviderFactory.validate_provider()
    if ai_valid:
        provider_name = os.getenv("AI_PROVIDER", "claude")
        print(f"✓ AI provider ({provider_name}) validated")
    else:
        print("⚠ AI provider validation failed - check configuration")
        print("  Resume generation will use fallback mode")

    yield

    # Shutdown
    print("Shutting down Resume Vault Backend...")
    await close_mongo_connection()


app = FastAPI(title="Resume Vault Spike", lifespan=lifespan)

# CORS configuration from environment
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(resumes.router)


# Simple MasterProfile for backwards compatibility with existing frontend
class SimpleMasterProfile(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    professionalExperience: str
    skills: str
    education: str
    licenses: str = ""


# Dependency injection for AI provider
async def get_ai_provider():
    """Dependency for AI provider - returns singleton instance"""
    return AIProviderFactory.get_provider()


def convert_simple_to_comprehensive_profile(simple_profile: SimpleMasterProfile) -> Dict[str, Any]:
    """
    Convert simple flat profile format to comprehensive nested format for AI processing.

    The frontend sends a simple format, but AI services expect the comprehensive format
    with nested objects and arrays.
    """
    # Parse skills from comma-separated string to array
    skills_list = [{"name": skill.strip(), "level": ""} for skill in simple_profile.skills.split(",") if skill.strip()]

    # Parse education from text block
    education_list = []
    if simple_profile.education:
        education_list.append({
            "institution": "",
            "degree": "",
            "fieldOfStudy": simple_profile.education,
            "startYear": "",
            "endYear": "",
            "grade": "",
            "description": ""
        })

    # Parse work experience from text block into structured format
    work_experience = []
    if simple_profile.professionalExperience:
        # Split by double newlines or similar patterns
        experience_blocks = simple_profile.professionalExperience.split("\n\n")
        for block in experience_blocks:
            if block.strip():
                lines = [line.strip() for line in block.split("\n") if line.strip()]
                work_experience.append({
                    "jobTitle": lines[0] if len(lines) > 0 else "Position",
                    "companyName": "Company",
                    "employmentType": "",
                    "location": "",
                    "startDate": "",
                    "endDate": "",
                    "currentlyWorking": False,
                    "responsibilities": lines[1:] if len(lines) > 1 else [],
                    "achievements": [],
                    "technologies": []
                })

    # Parse certifications from licenses field
    certifications = []
    if simple_profile.licenses:
        cert_lines = [line.strip() for line in simple_profile.licenses.split("\n") if line.strip()]
        for cert in cert_lines:
            certifications.append({
                "name": cert,
                "issuingOrganization": "",
                "issueDate": "",
                "expirationDate": "",
                "credentialId": "",
                "credentialUrl": ""
            })

    return {
        "personalInfo": {
            "firstName": simple_profile.name.split()[0] if simple_profile.name else "",
            "lastName": " ".join(simple_profile.name.split()[1:]) if len(simple_profile.name.split()) > 1 else "",
            "email": simple_profile.email,
            "phone": simple_profile.phone,
            "location": {"city": "", "country": ""},
            "linkedinUrl": "",
            "portfolioUrl": ""
        },
        "professionalHeadline": "",
        "summary": simple_profile.summary,
        "workExperience": work_experience,
        "education": education_list,
        "skills": skills_list,
        "certifications": certifications,
        "projects": [],
        "volunteering": [],
        "languages": [],
        "publications": [],
        "jobPreferences": {
            "desiredRoles": [],
            "desiredLocations": [],
            "employmentTypes": [],
            "remotePreference": "",
            "salaryExpectation": {"min": 0, "max": 0, "currency": "USD", "period": "yearly"},
            "willingToRelocate": False,
            "availabilityDate": ""
        }
    }


@app.get("/")
def root():
    return {
        "message": "Resume Vault Backend - AI-Powered Resume Generation",
        "status": "running",
        "ai_provider": os.getenv("AI_PROVIDER", "claude")
    }


@app.get("/debug/my-ip")
async def get_my_ip():
    """Debug endpoint to check what IP this server uses for outbound connections"""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try multiple IP detection services
            ipv4_response = await client.get("https://api.ipify.org?format=json")
            ipv6_response = await client.get("https://api64.ipify.org?format=json")

            return {
                "ipv4": ipv4_response.json() if ipv4_response.status_code == 200 else None,
                "ipv6": ipv6_response.json() if ipv6_response.status_code == 200 else None,
                "fly_region": os.getenv("FLY_REGION", "unknown"),
                "fly_app_name": os.getenv("FLY_APP_NAME", "unknown")
            }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
