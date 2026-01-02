"""
Resume Vault Backend - FastAPI
AI-powered resume and cover letter generation
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import base64
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
from services.pdf_generator import ProfessionalPDFGenerator

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

# Request/Response models for generate endpoint
class GenerateRequest(BaseModel):
    # No master_profile needed - backend fetches from DB using authenticated user
    job_description: str
    company_name: str
    position: str
    job_id: str = ""  # Optional field
    posting_link: str = ""  # Optional field


class GenerateResponse(BaseModel):
    resume_base64: str
    cover_letter_base64: str
    resume_ats_score: int
    cover_letter_ats_score: int


# Dependency injection for AI provider
async def get_ai_provider():
    """Dependency for AI provider - returns singleton instance"""
    return AIProviderFactory.get_provider()


def calculate_ats_score(tailored_resume: Any, profile: Dict[str, Any]) -> int:
    """
    Calculate estimated ATS score based on resume optimization.

    Score factors:
    - Keyword matches from job description (up to 30 points)
    - Tailored experience bullets (up to 10 points)
    - Base score: 60

    Returns:
        int: ATS score between 60-95
    """
    base_score = 60

    # Points for keyword matches (2 points per keyword, max 30)
    keyword_count = len(tailored_resume.keyword_matches)
    keyword_points = min(keyword_count * 2, 30)

    # Points for tailored experience (max 10)
    experience_count = len(tailored_resume.tailored_experience)
    experience_points = min(experience_count * 3, 10)

    total_score = base_score + keyword_points + experience_points

    # Log detailed breakdown
    logger.info(f"Resume ATS Score Breakdown:")
    logger.info(f"  - Base score: {base_score}")
    logger.info(f"  - Keyword matches ({keyword_count} keywords): +{keyword_points}")
    logger.info(f"  - Keywords: {tailored_resume.keyword_matches}")
    logger.info(f"  - Tailored experiences ({experience_count} roles): +{experience_points}")
    logger.info(f"  - Total: {total_score}")

    # Cap at 95 (never claim 100% to be realistic)
    return min(total_score, 95)


def calculate_cover_letter_ats_score(
    cover_letter_content: str,
    tailored_resume: Any,
    job_description: str,
    company_name: str
) -> int:
    """
    Calculate estimated ATS score for cover letter.

    Score factors:
    - Base score: 65 (cover letters generally score slightly lower)
    - Length appropriate (250-400 words): +10 points
    - Company name mentioned: +5 points
    - Keywords from resume present: +2 points each (max 15)

    Returns:
        int: ATS score between 65-92
    """
    base_score = 65

    # Check word count (250-400 is ideal)
    word_count = len(cover_letter_content.split())
    if 250 <= word_count <= 400:
        length_points = 10
    elif 200 <= word_count <= 500:
        length_points = 5
    else:
        length_points = 0

    # Company name mentioned
    company_points = 5 if company_name.lower() in cover_letter_content.lower() else 0

    # Keyword overlap with resume (top keywords)
    keyword_points = 0
    matched_keywords = []
    top_keywords = tailored_resume.keyword_matches[:8] if tailored_resume.keyword_matches else []
    for keyword in top_keywords:
        if keyword.lower() in cover_letter_content.lower():
            keyword_points += 2
            matched_keywords.append(keyword)
    keyword_points = min(keyword_points, 15)

    total_score = base_score + length_points + company_points + keyword_points

    # Log detailed breakdown
    logger.info(f"Cover Letter ATS Score Breakdown:")
    logger.info(f"  - Base score: {base_score}")
    logger.info(f"  - Word count ({word_count} words): +{length_points}")
    logger.info(f"  - Company mentioned: +{company_points}")
    logger.info(f"  - Keyword matches ({len(matched_keywords)}/{len(top_keywords)}): +{keyword_points}")
    logger.info(f"  - Matched keywords: {matched_keywords}")
    logger.info(f"  - Total: {total_score}")

    # Cap at 92 (cover letters typically score slightly lower than resumes)
    return min(total_score, 92)


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


@app.post("/generate", response_model=GenerateResponse)
async def generate(
    request: GenerateRequest,
    ai_provider=Depends(get_ai_provider),
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Generate AI-tailored resume and cover letter.

    This endpoint fetches the user's master profile from the database and uses AI
    to analyze the job description and create customized resume content.

    Args:
        request: Generate request containing job details
        ai_provider: AI provider instance (injected dependency)
        token_payload: Authenticated user token (injected dependency)

    Returns:
        GenerateResponse with base64-encoded PDF files

    Raises:
        HTTPException: If generation fails or profile not found
    """
    try:
        logger.info(f"Generating resume for {request.company_name} - {request.position}")

        # Get authenticated user ID
        user_id = token_payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id not found"
            )

        # Fetch master profile from database
        db = get_database()
        profile_doc = await db.master_profiles.find_one({"userId": user_id})

        if not profile_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Master profile not found. Please create your profile first."
            )

        # Remove MongoDB _id field
        profile_doc.pop("_id", None)

        # Use the comprehensive profile from DB
        profile_dict = profile_doc

        logger.info(f"Fetched profile from DB - has {len(profile_dict.get('workExperience', []))} work experiences, {len(profile_dict.get('skills', []))} skills")

        # AI tailoring - analyze job description and customize resume
        tailored_resume = await ai_provider.tailor_resume(
            master_profile=profile_dict,
            job_description=request.job_description,
            company_name=request.company_name,
            position=request.position
        )

        logger.info("Resume tailoring completed")

        # Generate cover letter using AI
        cover_letter_content = await ai_provider.generate_cover_letter(
            master_profile=profile_dict,
            job_description=request.job_description,
            company_name=request.company_name,
            position=request.position,
            tailored_resume=tailored_resume
        )

        logger.info("Cover letter generation completed")

        # Generate professional PDFs
        pdf_gen = ProfessionalPDFGenerator()

        # Generate resume PDF with tailored content
        resume_pdf = pdf_gen.generate_resume(
            profile=profile_dict,
            tailored_content=tailored_resume.dict(),
            job_info={
                "company": request.company_name,
                "position": request.position,
                "job_id": request.job_id,
                "posting_link": request.posting_link
            }
        )

        # Generate cover letter PDF
        cover_letter_pdf = pdf_gen.generate_cover_letter(
            profile=profile_dict,
            content=cover_letter_content,
            job_info={
                "company": request.company_name,
                "position": request.position,
                "job_id": request.job_id,
                "posting_link": request.posting_link
            }
        )

        logger.info("PDF generation completed")

        # Encode to base64
        resume_b64 = base64.b64encode(resume_pdf).decode('utf-8')
        cover_letter_b64 = base64.b64encode(cover_letter_pdf).decode('utf-8')

        # Calculate ATS scores
        resume_ats = calculate_ats_score(tailored_resume, profile_dict)
        cover_letter_ats = calculate_cover_letter_ats_score(
            cover_letter_content,
            tailored_resume,
            request.job_description,
            request.company_name
        )

        logger.info(f"Successfully generated resume and cover letter for {request.company_name}")
        logger.info(f"Resume ATS Score: {resume_ats}%, Cover Letter ATS Score: {cover_letter_ats}%")

        return GenerateResponse(
            resume_base64=resume_b64,
            cover_letter_base64=cover_letter_b64,
            resume_ats_score=resume_ats,
            cover_letter_ats_score=cover_letter_ats
        )

    except Exception as e:
        logger.error(f"Resume generation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate resume: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
