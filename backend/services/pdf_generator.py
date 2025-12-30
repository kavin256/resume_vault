"""
Professional PDF Generation Service
Creates polished, ATS-friendly resume and cover letter PDFs
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ProfessionalPDFGenerator:
    """Generate professional-looking resume and cover letter PDFs"""

    def __init__(self):
        """Initialize PDF generator with custom styles"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Create custom paragraph styles for resume sections"""

        # Helper function to add style only if it doesn't exist
        def add_style(style):
            if style.name not in self.styles:
                self.styles.add(style)

        # Name/Header style
        add_style(ParagraphStyle(
            name='ResumeName',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            leading=26
        ))

        # Contact info style
        add_style(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4a4a4a'),
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica'
        ))

        # Section header style
        add_style(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#2c5aa0'),
            fontName='Helvetica-Bold',
            spaceBefore=14,
            spaceAfter=6,
            borderWidth=0,
            borderPadding=0,
            borderColor=colors.HexColor('#2c5aa0'),
            leftIndent=0
        ))

        # Job title style
        add_style(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            spaceBefore=8,
            spaceAfter=2,
            textColor=colors.HexColor('#1a1a1a')
        ))

        # Company/Dates style
        add_style(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=4,
            textColor=colors.HexColor('#4a4a4a')
        ))

        # Body text style (use custom name to avoid conflict)
        add_style(ParagraphStyle(
            name='ResumeBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=8,
            textColor=colors.HexColor('#2a2a2a'),
            alignment=TA_JUSTIFY,
            leading=14
        ))

        # Bullet point style
        add_style(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            leftIndent=0,
            spaceAfter=3,
            textColor=colors.HexColor('#2a2a2a'),
            leading=13
        ))

    def generate_resume(
        self,
        profile: Dict[str, Any],
        tailored_content: Dict[str, Any],
        job_info: Dict[str, str]
    ) -> bytes:
        """
        Generate professional resume PDF.

        Args:
            profile: Master profile dictionary
            tailored_content: AI-tailored resume content
            job_info: Job application details

        Returns:
            PDF bytes
        """
        logger.info("Generating professional resume PDF")

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch
        )

        story = []

        # Header with name and contact info
        story.extend(self._build_header(profile))

        # Professional summary (tailored)
        story.extend(self._build_summary_section(tailored_content.get('tailored_summary', '')))

        # Work experience (tailored)
        story.extend(self._build_experience_section(
            tailored_content.get('tailored_experience', []),
            profile.get('workExperience', [])
        ))

        # Skills section
        story.extend(self._build_skills_section(profile.get('skills', [])))

        # Education
        story.extend(self._build_education_section(profile.get('education', [])))

        # Certifications (if any)
        certifications = profile.get('certifications', [])
        if certifications:
            story.extend(self._build_certifications_section(certifications))

        # Build PDF
        doc.build(story)
        buffer.seek(0)

        logger.info("Resume PDF generated successfully")
        return buffer.read()

    def generate_cover_letter(
        self,
        profile: Dict[str, Any],
        content: str,
        job_info: Dict[str, str]
    ) -> bytes:
        """
        Generate professional cover letter PDF.

        Args:
            profile: Master profile dictionary
            content: Cover letter content from AI
            job_info: Job application details

        Returns:
            PDF bytes
        """
        logger.info("Generating professional cover letter PDF")

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=1.0 * inch,
            leftMargin=1.0 * inch,
            topMargin=1.0 * inch,
            bottomMargin=1.0 * inch
        )

        story = []

        # Header
        personal_info = profile.get('personalInfo', {})
        first_name = personal_info.get('firstName', '')
        last_name = personal_info.get('lastName', '')
        email = personal_info.get('email', '')
        phone = personal_info.get('phone', '')

        # Your contact info (top right)
        contact_text = f"{first_name} {last_name}<br/>{email}"
        if phone:
            contact_text += f" | {phone}"

        story.append(Paragraph(contact_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))

        # Date
        from datetime import datetime
        date_text = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(date_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Company info
        company_name = job_info.get('company', '')
        position = job_info.get('position', '')

        company_text = f"{company_name}<br/>Hiring Manager"
        story.append(Paragraph(company_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Subject line
        subject = f"Re: Application for {position}"
        story.append(Paragraph(f"<b>{subject}</b>", self.styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Cover letter content
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), self.styles['ResumeBodyText']))
                story.append(Spacer(1, 0.1 * inch))

        # Build PDF
        doc.build(story)
        buffer.seek(0)

        logger.info("Cover letter PDF generated successfully")
        return buffer.read()

    def _build_header(self, profile: Dict) -> List:
        """Build resume header with contact information"""
        elements = []
        personal_info = profile.get('personalInfo', {})

        # Name
        first_name = personal_info.get('firstName', '')
        last_name = personal_info.get('lastName', '')
        name = f"{first_name} {last_name}".strip()

        if name:
            elements.append(Paragraph(name, self.styles['ResumeName']))

        # Contact info
        contact_parts = []
        email = personal_info.get('email', '')
        phone = personal_info.get('phone', '')
        location = personal_info.get('location', {})
        linkedin = personal_info.get('linkedinUrl', '')
        portfolio = personal_info.get('portfolioUrl', '')

        if email:
            contact_parts.append(email)
        if phone:
            contact_parts.append(phone)

        city = location.get('city', '')
        country = location.get('country', '')
        if city and country:
            contact_parts.append(f"{city}, {country}")
        elif city:
            contact_parts.append(city)

        if linkedin:
            contact_parts.append(f"LinkedIn: {linkedin}")
        if portfolio:
            contact_parts.append(f"Portfolio: {portfolio}")

        if contact_parts:
            contact_text = " | ".join(contact_parts)
            elements.append(Paragraph(contact_text, self.styles['ContactInfo']))

        elements.append(Spacer(1, 0.1 * inch))

        return elements

    def _build_summary_section(self, summary: str) -> List:
        """Build professional summary section"""
        elements = []

        if summary:
            elements.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
            elements.append(Paragraph(summary, self.styles['ResumeBodyText']))
            elements.append(Spacer(1, 0.05 * inch))

        return elements

    def _build_experience_section(
        self,
        tailored_experiences: List[Dict],
        original_experiences: List[Dict]
    ) -> List:
        """Build work experience section with tailored bullets"""
        elements = []

        # Use tailored experiences if available, otherwise use original
        experiences_to_show = tailored_experiences if tailored_experiences else original_experiences

        if not experiences_to_show:
            return elements

        elements.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))

        # Display each tailored experience
        for exp in experiences_to_show:
            job_title = exp.get('jobTitle', 'Position')
            company_name = exp.get('companyName', 'Company')

            # Match with original experience to get dates and location
            original_exp = None
            if tailored_experiences:
                # Find matching original experience by job title and company
                logger.info(f"Looking for match: '{job_title}' at '{company_name}'")
                for orig in original_experiences:
                    orig_title = orig.get('jobTitle', '').strip()
                    orig_company = orig.get('companyName', '').strip()
                    logger.info(f"  Comparing with: '{orig_title}' at '{orig_company}'")
                    if (orig_title == job_title.strip() and
                        orig_company == company_name.strip()):
                        original_exp = orig
                        logger.info(f"  ✓ Match found! Dates: {orig.get('startDate')} - {orig.get('endDate')}")
                        break

                if not original_exp:
                    logger.warning(f"  ✗ No match found for '{job_title}' at '{company_name}'")

            # Get dates from original experience if found, otherwise from exp itself
            if original_exp:
                start_date = original_exp.get('startDate', '')
                end_date = original_exp.get('endDate', '')
                currently_working = original_exp.get('currentlyWorking', False)
                location = original_exp.get('location', '')
            else:
                start_date = exp.get('startDate', '')
                end_date = exp.get('endDate', '')
                currently_working = exp.get('currentlyWorking', False)
                location = exp.get('location', '')

            # Set end date to Present if currently working
            if currently_working or not end_date:
                end_date = 'Present'

            logger.info(f"Final dates for '{job_title}': start={start_date}, end={end_date}, currently_working={currently_working}")

            # Job title
            elements.append(Paragraph(job_title, self.styles['JobTitle']))

            # Company and dates
            company_line = company_name
            if start_date or end_date:
                company_line += f" | {start_date} - {end_date}"
            if location:
                company_line += f" | {location}"

            logger.info(f"Company line: {company_line}")

            elements.append(Paragraph(company_line, self.styles['CompanyInfo']))

            # Get bullets - prefer tailored_bullets, fallback to achievements/responsibilities
            bullets = exp.get('tailored_bullets', [])
            if not bullets:
                bullets = exp.get('achievements', []) or exp.get('responsibilities', [])

            # Add bullets
            if bullets:
                bullet_items = []
                for bullet in bullets:
                    if bullet.strip():
                        bullet_items.append(ListItem(
                            Paragraph(bullet.strip(), self.styles['BulletPoint']),
                            leftIndent=0
                        ))

                if bullet_items:
                    bullet_list = ListFlowable(
                        bullet_items,
                        bulletType='bullet',
                        leftIndent=18,
                        bulletFontSize=8,
                        bulletOffsetY=-1
                    )
                    elements.append(bullet_list)

            elements.append(Spacer(1, 0.08 * inch))

        return elements

    def _build_skills_section(self, skills: List[Dict]) -> List:
        """Build skills section"""
        elements = []

        if not skills:
            return elements

        elements.append(Paragraph("SKILLS", self.styles['SectionHeader']))

        # Group skills by level if available
        skill_names = [s.get('name', '') for s in skills if s.get('name')]

        if skill_names:
            skills_text = " • ".join(skill_names)
            elements.append(Paragraph(skills_text, self.styles['ResumeBodyText']))

        return elements

    def _build_education_section(self, education: List[Dict]) -> List:
        """Build education section"""
        elements = []

        if not education:
            return elements

        elements.append(Paragraph("EDUCATION", self.styles['SectionHeader']))

        for edu in education:
            degree = edu.get('degree', '')
            field_of_study = edu.get('fieldOfStudy', '')
            institution = edu.get('institution', '')
            start_year = edu.get('startYear', '')
            end_year = edu.get('endYear', '')
            grade = edu.get('grade', '')

            # Build education entry
            if degree and field_of_study:
                edu_title = f"{degree} in {field_of_study}"
            elif degree:
                edu_title = degree
            else:
                edu_title = field_of_study or "Degree"

            elements.append(Paragraph(edu_title, self.styles['JobTitle']))

            # Institution and dates
            inst_line = institution if institution else ""
            if start_year and end_year:
                inst_line += f" | {start_year} - {end_year}"
            elif end_year:
                inst_line += f" | {end_year}"

            if inst_line:
                elements.append(Paragraph(inst_line, self.styles['CompanyInfo']))

            # Grade if available
            if grade:
                elements.append(Paragraph(f"Grade: {grade}", self.styles['BulletPoint']))

            elements.append(Spacer(1, 0.08 * inch))

        return elements

    def _build_certifications_section(self, certifications: List[Dict]) -> List:
        """Build certifications section"""
        elements = []

        if not certifications:
            return elements

        elements.append(Paragraph("CERTIFICATIONS", self.styles['SectionHeader']))

        for cert in certifications:
            name = cert.get('name', '')
            org = cert.get('issuingOrganization', '')
            issue_date = cert.get('issueDate', '')
            credential_id = cert.get('credentialId', '')

            if name:
                cert_text = f"<b>{name}</b>"
                if org:
                    cert_text += f" - {org}"
                if issue_date:
                    cert_text += f" ({issue_date})"

                elements.append(Paragraph(cert_text, self.styles['BulletPoint']))

        elements.append(Spacer(1, 0.08 * inch))

        return elements
