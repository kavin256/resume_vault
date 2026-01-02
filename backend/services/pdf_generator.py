"""
Professional PDF Generation Service
Creates polished, ATS-friendly resume and cover letter PDFs using LaTeX templates
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
from typing import Dict, Any
import logging

from services.latex_generator import LaTeXResumeGenerator
from services.latex_online_compiler import LaTeXOnlineCompiler

logger = logging.getLogger(__name__)


class ProfessionalPDFGenerator:
    """Generate professional-looking resume and cover letter PDFs using LaTeX"""

    def __init__(self):
        """Initialize PDF generator with LaTeX components"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Initialize LaTeX generator and compiler
        self.latex_generator = LaTeXResumeGenerator()
        self.latex_compiler = LaTeXOnlineCompiler()

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

    async def generate_resume(
        self,
        profile: Dict[str, Any],
        tailored_content: Dict[str, Any],
        job_info: Dict[str, str]
    ) -> bytes:
        """
        Generate professional resume PDF using LaTeX template.

        Args:
            profile: Master profile dictionary
            tailored_content: AI-tailored resume content
            job_info: Job application details

        Returns:
            PDF bytes
        """
        logger.info("Generating professional resume PDF using LaTeX")

        try:
            # Generate LaTeX source from template
            latex_source = self.latex_generator.generate_latex(
                profile=profile,
                tailored_content=tailored_content
            )
            
            logger.info("LaTeX source generated, compiling to PDF...")
            
            # Compile LaTeX to PDF using online compiler
            pdf_bytes = await self.latex_compiler.compile_to_pdf(latex_source)
            
            logger.info(f"Resume PDF generated successfully ({len(pdf_bytes)} bytes)")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Failed to generate LaTeX-based resume PDF: {e}", exc_info=True)
            raise Exception(f"LaTeX PDF generation failed: {str(e)}")

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

