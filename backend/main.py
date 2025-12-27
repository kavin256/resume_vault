"""
UI Spike Backend - FastAPI
Generates dummy resume and cover letter files in memory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = FastAPI(title="Resume Vault Spike")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MasterProfile(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    professionalExperience: str
    skills: str
    education: str
    licenses: str = ""  # Optional field


class GenerateRequest(BaseModel):
    master_profile: MasterProfile
    job_description: str
    company_name: str
    position: str
    job_id: str = ""  # Optional field
    posting_link: str = ""  # Optional field


class GenerateResponse(BaseModel):
    resume_base64: str
    cover_letter_base64: str


def generate_dummy_pdf(content: str, title: str) -> bytes:
    """Generate a simple PDF in memory with dummy content"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Add title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, title)

    # Add content
    pdf.setFont("Helvetica", 12)
    y_position = 700
    for line in content.split('\n'):
        pdf.drawString(100, y_position, line)
        y_position -= 20
        if y_position < 100:
            pdf.showPage()
            y_position = 750

    pdf.save()
    buffer.seek(0)
    return buffer.read()


@app.get("/")
def root():
    return {"message": "Resume Vault UI Spike Backend", "status": "running"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    """
    Generate dummy resume and cover letter based on master profile and JD.
    Returns both files as base64-encoded PDFs.
    """
    profile = request.master_profile
    jd = request.job_description

    # Generate dummy resume content
    licenses_section = f"\n\nLICENSES & CERTIFICATIONS\n{profile.licenses}" if profile.licenses else ""
    job_id_section = f" | Job ID: {request.job_id}" if request.job_id else ""
    posting_link_section = f"\nPosting: {request.posting_link}" if request.posting_link else ""

    resume_content = f"""RESUME

{profile.name}
{profile.email} | {profile.phone}

APPLYING FOR: {request.position} at {request.company_name}{job_id_section}{posting_link_section}

PROFESSIONAL SUMMARY
{profile.summary}

PROFESSIONAL EXPERIENCE
{profile.professionalExperience}

SKILLS
{profile.skills}

EDUCATION
{profile.education}{licenses_section}

TARGETED JD (First 100 chars):
{jd[:100]}...

This is a placeholder resume generated for testing.
"""

    # Generate dummy cover letter content
    cover_letter_content = f"""COVER LETTER

{profile.name}
{profile.email} | {profile.phone}

Dear Hiring Manager at {request.company_name},

I am writing to express my interest in the {request.position} position{job_id_section}.

{profile.summary}

Key skills: {profile.skills}

This is a placeholder cover letter generated for testing.

Sincerely,
{profile.name}
"""

    # Generate PDFs in memory
    resume_pdf = generate_dummy_pdf(resume_content, "RESUME")
    cover_letter_pdf = generate_dummy_pdf(cover_letter_content, "COVER LETTER")

    # Encode to base64
    resume_b64 = base64.b64encode(resume_pdf).decode('utf-8')
    cover_letter_b64 = base64.b64encode(cover_letter_pdf).decode('utf-8')

    return GenerateResponse(
        resume_base64=resume_b64,
        cover_letter_base64=cover_letter_b64
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
