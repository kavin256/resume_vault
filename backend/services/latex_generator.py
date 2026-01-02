"""
LaTeX Resume Generator Service
Fills LaTeX template with tailored resume content
"""

import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class LaTeXResumeGenerator:
    """Generate LaTeX resume from template and profile data"""

    def __init__(self, template_path: str = None):
        """
        Initialize LaTeX generator.

        Args:
            template_path: Path to LaTeX template file
        """
        if template_path is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_path = os.path.join(current_dir, 'template', 'template1.tex')

        self.template_path = template_path
        logger.info(f"LaTeX generator initialized with template: {template_path}")

    def generate_latex(
        self,
        profile: Dict[str, Any],
        tailored_content: Dict[str, Any] = None
    ) -> str:
        """
        Generate filled LaTeX resume.

        Args:
            profile: Master profile dictionary
            tailored_content: AI-tailored resume content (optional)

        Returns:
            Filled LaTeX source code as string
        """
        logger.info("Generating LaTeX resume")

        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        personal_info = profile.get('personalInfo', {})
        work_experience = profile.get('workExperience', [])
        education = profile.get('education', [])
        skills = profile.get('skills', [])
        certifications = profile.get('certifications', [])

        summary = tailored_content.get('tailored_summary', '') if tailored_content else profile.get('professionalSummary', '')

        experiences = work_experience
        if tailored_content and 'tailored_experience' in tailored_content:
            tailored_exp = tailored_content['tailored_experience']
            for i, exp in enumerate(experiences):
                if i < len(tailored_exp):
                    if isinstance(tailored_exp[i], dict):
                        experiences[i] = {**exp, **tailored_exp[i]}

        latex_content = template

        # Header
        full_name = f"{personal_info.get('firstName', '')} {personal_info.get('lastName', '')}"
        location = f"{personal_info.get('location', {}).get('city', '')}, {personal_info.get('location', {}).get('country', '')}"
        
        latex_content = latex_content.replace('{{FULL_NAME}}', self._escape_latex(full_name))
        latex_content = latex_content.replace('{{LOCATION}}', self._escape_latex(location))
        latex_content = latex_content.replace('{{EMAIL}}', self._escape_latex(personal_info.get('email', '')))
        latex_content = latex_content.replace('{{PHONE}}', self._escape_latex(personal_info.get('phone', '')))
        latex_content = latex_content.replace('{{LINKEDIN}}', self._format_url(personal_info.get('linkedinUrl', '')))
        latex_content = latex_content.replace('{{PORTFOLIO}}', self._format_url(personal_info.get('portfolioUrl', '')))

        # Summary
        latex_content = latex_content.replace('{{PROFESSIONAL_SUMMARY}}', self._escape_latex(summary))

        # Skills
        latex_content = latex_content.replace('{{SKILLS}}', self._format_skills(skills))

        # Experiences
        latex_content = latex_content.replace('{{EXPERIENCES}}', self._format_experiences(experiences))

        # Education
        latex_content = latex_content.replace('{{EDUCATION}}', self._format_education(education))

        # Certifications
        latex_content = latex_content.replace('{{CERTIFICATIONS}}', self._format_certifications(certifications))

        logger.info("Successfully generated LaTeX resume")
        return latex_content

    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters using simple replacement"""
        if not text:
            return ''

        # CRITICAL: Backslash must be escaped FIRST before other characters
        # Otherwise, the backslashes we add for escaping will themselves get escaped
        text = text.replace('\\', r'\textbackslash{}')

        # Now escape other special characters
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\string~',
            '^': r'\string^',
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        return text

    def _format_url(self, url: str) -> str:
        """Format URL for LaTeX hyperlink - returns just the URL, not wrapped in href"""
        if not url:
            return ''
        # Just return the URL itself, the template will handle the href wrapping
        return self._escape_latex(url)

    def _format_skills(self, skills: List) -> str:
        """Format skills section for template1"""
        if not skills:
            return '\\textbf{Skills}{: No skills listed}'
        
        # Group skills by category if available, otherwise list all
        skill_names = [self._escape_latex(s.get('name', '')) for s in skills]
        skills_text = ', '.join(skill_names)
        
        return f"\\textbf{{Skills}}{{: {skills_text}}}"

    def _format_experiences(self, experiences: List) -> str:
        """Format work experience section for template1"""
        if not experiences:
            return '    % No work experience listed'

        exp_blocks = []

        for exp in experiences:
            job_title = self._escape_latex(exp.get('jobTitle', ''))
            company = self._escape_latex(exp.get('companyName', ''))
            location = self._escape_latex(exp.get('location', ''))
            start_date = exp.get('startDate', '')
            end_date = exp.get('endDate', 'Present')
            date_range = f"{start_date} -- {end_date}" if start_date else end_date

            bullets = exp.get('tailored_bullets', exp.get('responsibilities', []))

            # Use template1's resumeSubheading format
            block = f"    \\resumeSubheading\n"
            block += f"      {{{job_title}}}{{{date_range}}}\n"
            block += f"      {{{company}}}{{{location}}}\n"
            block += f"      \\resumeItemListStart\n"
            for bullet in bullets:
                block += f"        \\resumeItem{{{self._escape_latex(bullet)}}}\n"
            block += f"      \\resumeItemListEnd\n"
            exp_blocks.append(block)

        return '\n'.join(exp_blocks)

    def _format_education(self, education: List) -> str:
        """Format education section for template1"""
        if not education:
            return '    % No education listed'

        edu_blocks = []

        for edu in education:
            degree = self._escape_latex(edu.get('degree', ''))
            field = self._escape_latex(edu.get('fieldOfStudy', ''))
            school = self._escape_latex(edu.get('institution', ''))
            location = self._escape_latex(edu.get('location', ''))
            start_year = edu.get('startYear', '')
            end_year = edu.get('endYear', '')
            date_range = f"{start_year} -- {end_year}" if start_year and end_year else end_year

            # Combine degree and field
            degree_text = f"{degree} in {field}" if field else degree

            # Use template1's resumeSubheading format
            block = f"    \\resumeSubheading\n"
            block += f"      {{{school}}}{{{location}}}\n"
            block += f"      {{{degree_text}}}{{{date_range}}}\n"
            edu_blocks.append(block)

        return '\n'.join(edu_blocks)

    def _format_certifications(self, certifications: List) -> str:
        """Format certifications section for template1"""
        if not certifications:
            return '\\textbf{Certifications}{: No certifications listed}'

        cert_list = []
        for cert in certifications:
            name = self._escape_latex(cert.get('name', ''))
            org = self._escape_latex(cert.get('issuingOrganization', ''))
            year = cert.get('issueYear', '')
            
            cert_text = f"{name} ({org})"
            if year:
                cert_text += f" - {year}"
            cert_list.append(cert_text)

        return '\\textbf{Certifications}{: ' + ', '.join(cert_list) + '}'

