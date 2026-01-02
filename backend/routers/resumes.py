"""
Resume Generation Router
Handles HTML resume generation, editing, version management, and PDF conversion
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from auth import verify_clerk_token
from database import get_database
from services.ai_factory import AIProviderFactory
from services.html_converter import HTMLToPDFConverter
from services.content_extractor import ContentExtractor
import logging
import uuid
from io import BytesIO

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resumes", tags=["resumes"])


# Request/Response Models
class GenerateHTMLResumeRequest(BaseModel):
    job_description: str = Field(..., min_length=10)
    company_name: str = Field(..., min_length=1)
    position: str = Field(..., min_length=1)
    job_id: str = ""
    posting_link: str = ""


class GenerateHTMLResumeResponse(BaseModel):
    job_application_id: str
    version_number: int
    html_content: str
    cover_letter_html: str
    resume_ats_score: int
    cover_letter_ats_score: int
    tailored_data: Dict[str, Any]


class EditContentRequest(BaseModel):
    edited_content: Dict[str, Any]


class RegenerateResponse(BaseModel):
    job_application_id: str
    version_number: int
    html_content: str
    cover_letter_html: str


class ResumeVersion(BaseModel):
    version_number: int
    created_at: str
    is_edited: bool
    ats_scores: Dict[str, int]


class GetResumeResponse(BaseModel):
    job_application_id: str
    current_version: int
    versions: List[ResumeVersion]
    html_content: str
    cover_letter_html: str
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


@router.post("/generate-html", response_model=GenerateHTMLResumeResponse)
async def generate_html_resume(
    request: GenerateHTMLResumeRequest,
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Generate HTML resume (initial version).

    Process:
    1. Fetch user's master profile from database
    2. AI tailors content for the job
    3. AI generates HTML with professional styling
    4. Store in database with version history
    5. Return HTML and metadata
    """
    try:
        user_id = token_payload.get("sub")
        logger.info(f"Generating HTML resume for user {user_id}, company: {request.company_name}")

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

        # Generate HTML resume using AI
        job_info = {
            "company_name": request.company_name,
            "position": request.position,
            "job_id": request.job_id,
            "posting_link": request.posting_link
        }

        html_content = await ai_provider.generate_html_resume(
            master_profile=profile_dict,
            tailored_resume=tailored_resume,
            job_info=job_info
        )
        logger.info("HTML resume generation completed")

        # Generate cover letter (text)
        cover_letter_text = await ai_provider.generate_cover_letter(
            master_profile=profile_dict,
            job_description=request.job_description,
            company_name=request.company_name,
            position=request.position,
            tailored_resume=tailored_resume
        )
        logger.info("Cover letter generation completed")

        # For now, wrap cover letter in simple HTML
        # TODO: Create a proper HTML cover letter template
        cover_letter_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Cover Letter - {request.company_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 850px;
            margin: 40px auto;
            padding: 40px;
            line-height: 1.6;
            color: #2d3748;
        }}
        .cover-letter {{
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="cover-letter">{cover_letter_text}</div>
</body>
</html>"""

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
                    "htmlContent": html_content,
                    "coverLetterHtml": cover_letter_html,
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

        return GenerateHTMLResumeResponse(
            job_application_id=job_application_id,
            version_number=1,
            html_content=html_content,
            cover_letter_html=cover_letter_html,
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
            html_content=version_data["htmlContent"],
            cover_letter_html=version_data["coverLetterHtml"],
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
    Extract structured content from HTML for editing form.
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

        # Extract content from HTML
        extractor = ContentExtractor()
        extracted_content = extractor.extract_editable_content(version_data["htmlContent"])

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
    Regenerate HTML with edited content, preserving styling.
    Creates a new version in the versions array.
    """
    try:
        user_id = token_payload.get("sub")
        db = get_database()
        ai_provider = AIProviderFactory.get_provider()

        # Fetch resume
        doc = await db["resume_generations"].find_one({
            "jobApplicationId": job_application_id,
            "userId": user_id
        })

        if not doc:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Get current version HTML
        current_version = doc["currentVersion"]
        current_version_data = None
        for v in doc["versions"]:
            if v["versionNumber"] == current_version:
                current_version_data = v
                break

        if not current_version_data:
            raise HTTPException(status_code=500, detail="Current version not found")

        original_html = current_version_data["htmlContent"]
        job_info = doc["jobInfo"]

        # Regenerate HTML with AI
        logger.info(f"Regenerating HTML for {job_application_id} with edited content")
        new_html = await ai_provider.regenerate_html_with_edits(
            original_html=original_html,
            edited_content=request.edited_content,
            job_info=job_info
        )
        logger.info("HTML regeneration completed")

        # Create new version
        new_version_number = len(doc["versions"]) + 1

        new_version = {
            "versionNumber": new_version_number,
            "createdAt": datetime.utcnow().isoformat(),
            "htmlContent": new_html,
            "coverLetterHtml": current_version_data["coverLetterHtml"],  # Keep same cover letter
            "tailoredData": current_version_data["tailoredData"],  # Keep same tailored data
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
            html_content=new_html,
            cover_letter_html=current_version_data["coverLetterHtml"]
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
    Convert HTML resume to PDF and return for download.
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

        # Convert HTML to PDF
        converter = HTMLToPDFConverter()
        pdf_bytes = converter.convert(version_data["htmlContent"])

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
