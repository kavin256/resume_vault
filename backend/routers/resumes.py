"""
Resume Generation Router
Handles LaTeX resume generation, editing, version management, and PDF conversion
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from auth import verify_clerk_token
from database import get_database
from services.ai_factory import AIProviderFactory
from services.latex_generator import LaTeXResumeGenerator
from services.latex_local_compiler import LaTeXLocalCompiler
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resumes", tags=["resumes"])


# Request/Response Models
class GenerateLatexResumeRequest(BaseModel):
    job_description: str = Field(..., min_length=10)
    company_name: str = Field(..., min_length=1)
    position: str = Field(..., min_length=1)
    job_id: str = ""
    posting_link: str = ""


class GenerateLatexResumeResponse(BaseModel):
    job_application_id: str
    version_number: int
    latex_content: str
    cover_letter_content: str
    resume_ats_score: int
    cover_letter_ats_score: int
    tailored_data: Dict[str, Any]


class EditContentRequest(BaseModel):
    edited_content: Dict[str, Any]


class RegenerateResponse(BaseModel):
    job_application_id: str
    version_number: int
    latex_content: str
    cover_letter_content: str


class ResumeVersion(BaseModel):
    version_number: int
    created_at: str
    is_edited: bool
    ats_scores: Dict[str, int]


class GetResumeResponse(BaseModel):
    job_application_id: str
    current_version: int
    versions: List[ResumeVersion]
    latex_content: str
    cover_letter_content: str
    job_info: Dict[str, str]


# Helper function to calculate ATS scores (copied from main.py)
def calculate_resume_ats_score(tailored_resume: Any, profile: Dict[str, Any]) -> int:
    """Calculate estimated ATS score for resume"""
    base_score = 60
    keyword_count = len(tailored_resume.keyword_matches) if hasattr(tailored_resume, 'keyword_matches') else 0
    experience_count = len(tailored_resume.tailored_experience) if hasattr(tailored_resume, 'tailored_experience') else 0

    keyword_bonus = min(keyword_count * 2, 15)
    experience_bonus = min(experience_count * 3, 15)

    has_summary = bool(tailored_resume.tailored_summary) if hasattr(tailored_resume, 'tailored_summary') else False
    summary_bonus = 5 if has_summary else 0

    total_score = base_score + keyword_bonus + experience_bonus + summary_bonus
    return min(total_score, 95)


def calculate_cover_letter_ats_score(tailored_resume: Any, cover_letter: str) -> int:
    """Calculate estimated ATS score for cover letter"""
    base_score = 65
    keyword_count = len(tailored_resume.keyword_matches[:8]) if hasattr(tailored_resume, 'keyword_matches') else 0
    keyword_bonus = min(keyword_count * 2, 16)

    has_content = len(cover_letter) > 100
    content_bonus = 8 if has_content else 0

    is_proper_length = 200 <= len(cover_letter) <= 600
    length_bonus = 3 if is_proper_length else 0

    total_score = base_score + keyword_bonus + content_bonus + length_bonus
    return min(total_score, 92)


@router.post("/generate-latex", response_model=GenerateLatexResumeResponse)
async def generate_latex_resume(
    request: GenerateLatexResumeRequest,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Generate LaTeX resume (initial version).

    Process:
    1. Fetch user's master profile from database
    2. AI tailors content for the job
    3. Fill LaTeX template with tailored content
    4. Store in database with version history
    5. Return LaTeX source and metadata
    """
    try:
        user_id = token_payload.get("sub")
        logger.info(f"Generating LaTeX resume for user {user_id}, company: {request.company_name}")

        # Get database and AI provider
        db = get_database()
        ai_provider = AIProviderFactory.get_provider()

        # Fetch master profile
        profile = await db["master_profiles"].find_one({"userId": user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Master profile not found. Please complete your profile first.")

        # Convert MongoDB _id to string for JSON serialization
        profile_dict = {k: str(v) if k == "_id" else v for k, v in profile.items()}

        # AI tailoring (existing flow)
        tailored_resume = await ai_provider.tailor_resume(
            master_profile=profile_dict,
            job_description=request.job_description,
            company_name=request.company_name,
            position=request.position
        )
        logger.info("Resume tailoring completed")

        # Generate LaTeX resume using template
        latex_generator = LaTeXResumeGenerator()
        latex_content = latex_generator.generate_latex(
            profile=profile_dict,
            tailored_content=tailored_resume.dict()
        )
        logger.info("LaTeX resume generation completed")

        # Generate cover letter (text)
        cover_letter_text = await ai_provider.generate_cover_letter(
            master_profile=profile_dict,
            job_description=request.job_description,
            company_name=request.company_name,
            position=request.position,
            tailored_resume=tailored_resume
        )
        logger.info("Cover letter generation completed")

        # Calculate ATS scores
        resume_ats_score = calculate_resume_ats_score(tailored_resume, profile_dict)
        cover_letter_ats_score = calculate_cover_letter_ats_score(tailored_resume, cover_letter_text)

        # Create job application ID
        job_application_id = str(uuid.uuid4())

        # Store in database
        resume_generation_doc = {
            "userId": user_id,
            "jobApplicationId": job_application_id,
            "jobInfo": {
                "companyName": request.company_name,
                "position": request.position,
                "jobId": request.job_id,
                "postingLink": request.posting_link,
                "jobDescription": request.job_description
            },
            "versions": [
                {
                    "versionNumber": 1,
                    "createdAt": datetime.utcnow().isoformat(),
                    "latexContent": latex_content,
                    "coverLetterContent": cover_letter_text,
                    "tailoredData": {
                        "tailored_summary": tailored_resume.tailored_summary,
                        "tailored_experience": [exp.dict() for exp in tailored_resume.tailored_experience],
                        "keyword_matches": tailored_resume.keyword_matches,
                        "recommendations": tailored_resume.recommendations
                    },
                    "atsScores": {
                        "resume": resume_ats_score,
                        "coverLetter": cover_letter_ats_score
                    },
                    "isEdited": False
                }
            ],
            "currentVersion": 1,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }

        await db["resume_generations"].insert_one(resume_generation_doc)
        logger.info(f"Stored resume generation with ID: {job_application_id}")

        return GenerateLatexResumeResponse(
            job_application_id=job_application_id,
            version_number=1,
            latex_content=latex_content,
            cover_letter_content=cover_letter_text,
            resume_ats_score=resume_ats_score,
            cover_letter_ats_score=cover_letter_ats_score,
            tailored_data=tailored_resume.dict()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate resume: {str(e)}")


@router.get("/{job_application_id}", response_model=GetResumeResponse)
async def get_resume(
    job_application_id: str,
    version: Optional[int] = None,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Get resume by ID, optionally specific version.
    If version not specified, returns latest version.
    """
    try:
        user_id = token_payload.get("sub")
        db = get_database()

        # Fetch resume generation document
        doc = await db["resume_generations"].find_one({
            "jobApplicationId": job_application_id,
            "userId": user_id
        })

        if not doc:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Get the requested version or current version
        version_to_get = version if version else doc["currentVersion"]

        # Find the version in the versions array
        version_data = None
        for v in doc["versions"]:
            if v["versionNumber"] == version_to_get:
                version_data = v
                break

        if not version_data:
            raise HTTPException(status_code=404, detail=f"Version {version_to_get} not found")

        # Build response
        versions_list = [
            ResumeVersion(
                version_number=v["versionNumber"],
                created_at=v["createdAt"],
                is_edited=v.get("isEdited", False),
                ats_scores=v["atsScores"]
            )
            for v in doc["versions"]
        ]

        return GetResumeResponse(
            job_application_id=job_application_id,
            current_version=doc["currentVersion"],
            versions=versions_list,
            latex_content=version_data.get("latexContent", ""),
            cover_letter_content=version_data.get("coverLetterContent", ""),
            job_info=doc["jobInfo"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get resume: {str(e)}")


@router.get("/{job_application_id}/extract")
async def extract_editable_content(
    job_application_id: str,
    version: Optional[int] = None,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Extract structured content from LaTeX/tailored data for editing form.
    Returns editable sections: summary, experiences, skills, education.
    """
    try:
        user_id = token_payload.get("sub")
        db = get_database()

        # Fetch resume
        doc = await db["resume_generations"].find_one({
            "jobApplicationId": job_application_id,
            "userId": user_id
        })

        if not doc:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Get version
        version_to_get = version if version else doc["currentVersion"]
        version_data = None
        for v in doc["versions"]:
            if v["versionNumber"] == version_to_get:
                version_data = v
                break

        if not version_data:
            raise HTTPException(status_code=404, detail=f"Version {version_to_get} not found")

        # Extract content from tailored data (already structured)
        tailored_data = version_data.get("tailoredData", {})
        
        extracted_content = {
            "summary": tailored_data.get("tailored_summary", ""),
            "experiences": tailored_data.get("tailored_experience", []),
            "keyword_matches": tailored_data.get("keyword_matches", []),
            "recommendations": tailored_data.get("recommendations", [])
        }

        logger.info(f"Extracted content from resume {job_application_id} version {version_to_get}")
        return extracted_content

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to extract content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to extract content: {str(e)}")


@router.post("/{job_application_id}/regenerate", response_model=RegenerateResponse)
async def regenerate_with_edits(
    job_application_id: str,
    request: EditContentRequest,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Regenerate LaTeX with edited content.
    Creates a new version in the versions array.
    """
    try:
        user_id = token_payload.get("sub")
        db = get_database()

        # Fetch resume
        doc = await db["resume_generations"].find_one({
            "jobApplicationId": job_application_id,
            "userId": user_id
        })

        if not doc:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Get current version
        current_version = doc["currentVersion"]
        current_version_data = None
        for v in doc["versions"]:
            if v["versionNumber"] == current_version:
                current_version_data = v
                break

        if not current_version_data:
            raise HTTPException(status_code=500, detail="Current version not found")

        # Get master profile for regeneration
        profile = await db["master_profiles"].find_one({"userId": user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Master profile not found")
        
        profile_dict = {k: str(v) if k == "_id" else v for k, v in profile.items()}

        # Merge edited content with existing tailored data
        tailored_data = current_version_data.get("tailoredData", {})
        edited_content = request.edited_content
        
        # Update tailored data with edits
        if "summary" in edited_content:
            tailored_data["tailored_summary"] = edited_content["summary"]
        if "experiences" in edited_content:
            tailored_data["tailored_experience"] = edited_content["experiences"]

        # Regenerate LaTeX with updated content
        logger.info(f"Regenerating LaTeX for {job_application_id} with edited content")
        latex_generator = LaTeXResumeGenerator()
        new_latex = latex_generator.generate_latex(
            profile=profile_dict,
            tailored_content=tailored_data
        )
        logger.info("LaTeX regeneration completed")

        # Create new version
        new_version_number = len(doc["versions"]) + 1

        new_version = {
            "versionNumber": new_version_number,
            "createdAt": datetime.utcnow().isoformat(),
            "latexContent": new_latex,
            "coverLetterContent": current_version_data.get("coverLetterContent", ""),
            "tailoredData": tailored_data,
            "atsScores": current_version_data["atsScores"],  # Keep same scores for now
            "isEdited": True
        }

        # Update document
        await db["resume_generations"].update_one(
            {"jobApplicationId": job_application_id, "userId": user_id},
            {
                "$push": {"versions": new_version},
                "$set": {
                    "currentVersion": new_version_number,
                    "updatedAt": datetime.utcnow().isoformat()
                }
            }
        )

        logger.info(f"Created new version {new_version_number} for resume {job_application_id}")

        return RegenerateResponse(
            job_application_id=job_application_id,
            version_number=new_version_number,
            latex_content=new_latex,
            cover_letter_content=current_version_data.get("coverLetterContent", "")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to regenerate resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to regenerate resume: {str(e)}")


@router.get("/{job_application_id}/pdf")
async def download_resume_pdf(
    job_application_id: str,
    version: Optional[int] = None,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Convert LaTeX resume to PDF and return for download.
    """
    try:
        user_id = token_payload.get("sub")
        db = get_database()

        # Fetch resume
        doc = await db["resume_generations"].find_one({
            "jobApplicationId": job_application_id,
            "userId": user_id
        })

        if not doc:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Get version
        version_to_get = version if version else doc["currentVersion"]
        version_data = None
        for v in doc["versions"]:
            if v["versionNumber"] == version_to_get:
                version_data = v
                break

        if not version_data:
            raise HTTPException(status_code=404, detail=f"Version {version_to_get} not found")

        # Get LaTeX content
        latex_content = version_data.get("latexContent", "")

        if not latex_content:
            raise HTTPException(status_code=500, detail="No LaTeX content found")

        # Compile LaTeX to PDF using local pdflatex
        compiler = LaTeXLocalCompiler()
        pdf_bytes = await compiler.compile_to_pdf(latex_content)

        logger.info(f"Converted resume {job_application_id} v{version_to_get} to PDF")

        # Return PDF as downloadable file
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=resume_{doc['jobInfo']['companyName'].replace(' ', '_')}.pdf"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to convert to PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to convert to PDF: {str(e)}")


@router.get("/list/all")
async def list_my_resumes(
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    List all resumes for the authenticated user.
    Returns summary information about each resume.
    """
    try:
        user_id = token_payload.get("sub")
        db = get_database()

        # Fetch all resumes for this user
        cursor = db["resume_generations"].find({"userId": user_id})
        resumes = await cursor.to_list(length=100)

        # Build summary list
        summary_list = []
        for doc in resumes:
            summary_list.append({
                "jobApplicationId": doc["jobApplicationId"],
                "companyName": doc["jobInfo"]["companyName"],
                "position": doc["jobInfo"]["position"],
                "currentVersion": doc["currentVersion"],
                "totalVersions": len(doc["versions"]),
                "createdAt": doc["createdAt"],
                "updatedAt": doc["updatedAt"]
            })

        logger.info(f"Retrieved {len(summary_list)} resumes for user {user_id}")
        return {"resumes": summary_list, "total": len(summary_list)}

    except Exception as e:
        logger.error(f"Failed to list resumes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list resumes: {str(e)}")
