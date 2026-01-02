"""
HTML Resume Template Generator
Creates print-ready HTML resumes matching the exact layout and styling requirements
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class HTMLResumeTemplateGenerator:
    """Generate print-ready HTML resume templates"""

    def __init__(self):
        """Initialize HTML template generator"""
        pass

    def generate_resume_html(
        self,
        profile: Dict[str, Any],
        tailored_content: Dict[str, Any] = None,
        job_info: Dict[str, str] = None
    ) -> str:
        """
        Generate complete HTML resume with print-ready styling.
        
        Args:
            profile: Master profile dictionary
            tailored_content: AI-tailored resume content (optional)
            job_info: Job application details (optional)
            
        Returns:
            Complete HTML document string with embedded CSS
        """
        logger.info("Generating print-ready HTML resume")
        
        # Extract profile data
        personal_info = profile.get('personalInfo', {})
        work_experience = profile.get('workExperience', [])
        education = profile.get('education', [])
        skills = profile.get('skills', [])
        certifications = profile.get('certifications', [])
        
        # Use tailored content if provided, otherwise use original
        summary = tailored_content.get('tailored_summary', '') if tailored_content else profile.get('professionalSummary', '')
        
        # Merge tailored experience with original to preserve all data
        experiences = work_experience
        if tailored_content and 'tailored_experience' in tailored_content:
            tailored_exp = tailored_content['tailored_experience']
            # Merge tailored responsibilities with original experience data
            for i, exp in enumerate(experiences):
                if i < len(tailored_exp):
                    # Keep all original data but use tailored responsibilities if available
                    if isinstance(tailored_exp[i], dict):
                        experiences[i] = {**exp, **tailored_exp[i]}
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume - {personal_info.get('firstName', '')} {personal_info.get('lastName', '')}</title>
    <style>
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        @page {{
            size: A4;
            margin: 0.75in;
        }}
        
        body {{
            font-family: 'Times New Roman', Georgia, serif;
            font-size: 11pt;
            line-height: 1.3;
            color: #000000;
            background: white;
            margin: 0;
            padding: 0.75in;
            width: 210mm;
            min-height: 297mm;
        }}
        
        .resume-container {{
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            padding: 0;
        }}
        
        /* Header Section */
        .header {{
            text-align: center;
            margin-bottom: 12px;
            page-break-inside: avoid;
        }}
        
        .header h1 {{
            font-size: 20pt;
            font-weight: 400;
            margin: 0 0 8px 0;
            color: #000000;
        }}
        
        .contact-info {{
            font-size: 10pt;
            line-height: 1.4;
            color: #000000;
        }}
        
        .contact-info a {{
            color: #000000;
            text-decoration: none;
        }}
        
        /* Section Headers */
        .section {{
            margin-top: 10px;
            margin-bottom: 6px;
        }}
        
        .section-title {{
            font-size: 12pt;
            font-weight: 700;
            color: #000000;
            margin-bottom: 4px;
            padding-bottom: 1px;
            border-bottom: 1px solid #000000;
        }}
        
        /* Objective/Summary */
        .summary {{
            font-size: 10pt;
            line-height: 1.3;
            text-align: justify;
            color: #000000;
            margin-bottom: 4px;
        }}
        
        /* Technologies/Skills Section */
        .tech-section {{
            margin-bottom: 4px;
        }}
        
        .tech-category {{
            font-size: 10pt;
            margin-bottom: 3px;
            line-height: 1.3;
        }}
        
        .tech-category strong {{
            font-weight: 700;
        }}
        
        /* Experience Section */
        .experience-item {{
            margin-bottom: 8px;
            page-break-inside: avoid;
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 2px;
        }}
        
        .job-title {{
            font-size: 11pt;
            font-weight: 700;
            color: #000000;
        }}
        
        .date-range {{
            font-size: 10pt;
            font-weight: 400;
            color: #000000;
        }}
        
        .company-info {{
            font-size: 10pt;
            font-style: italic;
            margin-bottom: 4px;
            color: #000000;
        }}
        
        .project-info {{
            font-size: 10pt;
            margin-bottom: 3px;
            color: #000000;
        }}
        
        .project-info strong {{
            font-weight: 700;
        }}
        
        /* Bullet Points */
        .responsibilities {{
            margin-left: 20px;
            padding-left: 0;
            margin-top: 3px;
        }}
        
        .responsibilities li {{
            font-size: 10pt;
            line-height: 1.25;
            color: #000000;
            margin-bottom: 2px;
            list-style-type: disc;
        }}
        
        /* Education Section */
        .education-item {{
            margin-bottom: 6px;
            page-break-inside: avoid;
        }}
        
        .degree {{
            font-size: 11pt;
            font-weight: 700;
            color: #000000;
            margin-bottom: 2px;
        }}
        
        .institution {{
            font-size: 10pt;
            color: #000000;
        }}
        
        /* Skills - inline format */
        .skills-inline {{
            font-size: 10pt;
            line-height: 1.3;
            color: #000000;
        }}
        
        .skills-inline strong {{
            font-weight: 700;
        }}
        
        /* Certifications */
        .certification-item {{
            margin-bottom: 4px;
            page-break-inside: avoid;
        }}
        
        .cert-name {{
            font-size: 10pt;
            font-weight: 700;
            color: #000000;
        }}
        
        .cert-issuer {{
            font-size: 10pt;
            color: #000000;
        }}
        
        /* Print Styles */
        @media print {{
            body {{
                margin: 0;
                padding: 0.75in;
                width: 210mm;
                min-height: 297mm;
            }}
            
            .resume-container {{
                max-width: none;
                width: 100%;
            }}
            
            .section {{
                page-break-inside: avoid;
            }}
            
            .experience-item,
            .education-item {{
                page-break-inside: avoid;
            }}
            
            @page {{
                size: A4;
                margin: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="resume-container">
        {self._build_header_section(personal_info)}
        
        {self._build_summary_section(summary)}
        
        {self._build_skills_section(skills)}
        
        {self._build_experience_section(experiences)}
        
        {self._build_education_section(education)}
        
        {self._build_certifications_section(certifications)}
    </div>
</body>
</html>"""
        
        logger.info("Successfully generated HTML resume")
        return html

    def _build_header_section(self, personal_info: Dict) -> str:
        """Build header section with name and contact info"""
        first_name = personal_info.get('firstName', '')
        last_name = personal_info.get('lastName', '')
        email = personal_info.get('email', '')
        phone = personal_info.get('phone', '')
        location = personal_info.get('location', {})
        linkedin = personal_info.get('linkedinUrl', '')
        github = personal_info.get('githubUrl', '')
        portfolio = personal_info.get('portfolioUrl', '')
        
        # Build location string
        location_parts = []
        if isinstance(location, dict):
            if location.get('city'):
                location_parts.append(location['city'])
            if location.get('state'):
                location_parts.append(location['state'])
            location_str = ', '.join(location_parts)
            if location.get('country'):
                location_str += f" ({location['country']})"
        else:
            location_str = str(location) if location else ''
        
        # Build contact line
        contact_parts = []
        if location_str:
            contact_parts.append(location_str)
        if email:
            contact_parts.append(f'<a href="mailto:{email}">{email}</a>')
        if phone:
            contact_parts.append(phone)
        
        # Build links line
        links_parts = []
        if linkedin:
            links_parts.append(f'<a href="{linkedin}">{linkedin}</a>')
        if github:
            links_parts.append(f'<a href="{github}">{github}</a>')
        if portfolio:
            links_parts.append(f'<a href="{portfolio}">{portfolio}</a>')
        
        contact_line = ' | '.join(contact_parts)
        links_line = ' | '.join(links_parts) if links_parts else ''
        
        return f"""
        <div class="header">
            <h1>{first_name} {last_name}</h1>
            <div class="contact-info">
                {contact_line}
                {('<br>' + links_line) if links_line else ''}
            </div>
        </div>
        """

    def _build_summary_section(self, summary: str) -> str:
        """Build objective/summary section."""
        if not summary:
            return ""
        
        return f"""
        <div class="section">
            <div class="section-title">Objective</div>
            <p class="summary">{summary}</p>
        </div>
        """

    def _build_experience_section(self, experiences: List[Dict]) -> str:
        """Build work experience section"""
        if not experiences:
            return ''
        
        html = '<div class="section"><div class="section-title">Professional Experience</div>'
        
        for exp in experiences:
            job_title = exp.get('jobTitle', '')
            company = exp.get('company', '')
            location = exp.get('location', '')
            start_date = exp.get('startDate', '')
            end_date = exp.get('endDate', 'Present')
            description = exp.get('description', '')
            responsibilities = exp.get('responsibilities', [])
            
            # Use tailored responsibilities if available
            if 'tailored_responsibilities' in exp:
                responsibilities = exp['tailored_responsibilities']
            
            # Build date range
            date_range = f"{start_date} – {end_date}"
            
            # Build company info with location
            company_info = company
            if location:
                company_info += f" ({location})"
            
            html += f"""
            <div class="experience-item">
                <div class="job-header">
                    <div class="job-title">{job_title}</div>
                    <div class="date-range">{date_range}</div>
                </div>
                <div class="company-info">{company_info}</div>
            """
            
            # Add project description if available
            if description:
                html += f'<div class="project-info"><strong>Project:</strong> {description}</div>'
            
            # Add responsibilities
            if responsibilities:
                html += '<ul class="responsibilities">'
                for resp in responsibilities:
                    html += f'<li>{resp}</li>'
                html += '</ul>'
            
            html += '</div>'
        
        html += '</div>'
        return html

    def _build_education_section(self, education: List[Dict]) -> str:
        """Build education section"""
        if not education:
            return ''
        
        html = '<div class="section"><div class="section-title">Education</div>'
        
        for edu in education:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            graduation_date = edu.get('graduationDate', '')
            location = edu.get('location', '')
            gpa = edu.get('gpa', '')
            
            html += '<div class="education-item">'
            html += f'<div class="degree">{degree}</div>'
            
            # Build institution line
            institution_parts = [institution]
            if location:
                institution_parts[0] += f' ({location})'
            if graduation_date:
                institution_parts.append(f'Graduated: {graduation_date}')
            if gpa:
                institution_parts.append(f'GPA: {gpa}')
            
            html += f'<div class="institution">{" | ".join(institution_parts)}</div>'
            html += '</div>'
        
        html += '</div>'
        return html

    def _build_skills_section(self, skills: List) -> str:
        """Build Technologies section with categorized skills"""
        if not skills:
            return ''
        
        html = '<div class="section"><div class="section-title">Technologies</div>'
        html += '<div class="tech-section">'
        
        # Group skills by category
        categorized = {}
        uncategorized = []
        
        for skill in skills:
            # Handle both string and dict formats
            if isinstance(skill, dict):
                skill_name = skill.get('name', '') or skill.get('skill', '')
                category = skill.get('category', '')
                
                if category:
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(skill_name)
                else:
                    if skill_name:
                        uncategorized.append(skill_name)
            elif isinstance(skill, str):
                if ':' in skill:
                    category, items = skill.split(':', 1)
                    categorized[category.strip()] = items.strip()
                else:
                    uncategorized.append(skill)
        
        # Add categorized skills
        for category, items in categorized.items():
            if isinstance(items, list):
                items_str = ', '.join(items)
            else:
                items_str = items
            html += f'<div class="tech-category"><strong>{category}:</strong> {items_str}</div>'
        
        # Add uncategorized skills if any
        if uncategorized:
            html += f'<div class="tech-category"><strong>Tech Stack & Soft Skills:</strong> {", ".join(uncategorized)}</div>'
        
        html += '</div></div>'
        return html

    def _build_certifications_section(self, certifications: List[Dict]) -> str:
        """Build certifications section"""
        if not certifications:
            return ''
        
        html = '<div class="section"><div class="section-title">Certifications</div>'
        
        for cert in certifications:
            name = cert.get('name', '')
            issuer = cert.get('issuer', '')
            date = cert.get('issueDate', '') or cert.get('date', '')
            
            html += '<div class="certification-item">'
            html += f'<div class="cert-name">{name}</div>'
            
            # Show date on separate line like in template
            if date:
                html += f'<div class="cert-issuer">{date}</div>'
            elif issuer:
                html += f'<div class="cert-issuer">{issuer}</div>'
            
            html += '</div>'
        
        html += '</div>'
        return html
