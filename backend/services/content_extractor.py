"""
Content Extraction Service
Extracts structured, editable content from HTML resumes
"""

from bs4 import BeautifulSoup
from typing import Dict, Any, List
import logging
import re

logger = logging.getLogger(__name__)


class ContentExtractor:
    """Extract editable content from HTML resumes"""

    def __init__(self):
        """Initialize content extractor"""
        pass

    def extract_editable_content(self, html_content: str) -> Dict[str, Any]:
        """
        Parse HTML resume and extract structured editable content.

        Args:
            html_content: Complete HTML document string

        Returns:
            Dictionary with structured content:
            {
                "summary": "Professional summary text",
                "experiences": [
                    {
                        "jobTitle": "Title",
                        "company": "Company Name",
                        "bullets": ["bullet 1", "bullet 2", ...]
                    }
                ],
                "skills": "Comma-separated skills",
                "education": "Education text"
            }

        Raises:
            Exception: If HTML parsing fails
        """
        try:
            logger.info("Extracting editable content from HTML")

            soup = BeautifulSoup(html_content, 'lxml')

            # Extract summary
            summary = self._extract_summary(soup)

            # Extract experiences
            experiences = self._extract_experiences(soup)

            # Extract skills
            skills = self._extract_skills(soup)

            # Extract education
            education = self._extract_education(soup)

            result = {
                "summary": summary,
                "experiences": experiences,
                "skills": skills,
                "education": education
            }

            logger.info(f"Successfully extracted content: {len(experiences)} experiences")
            return result

        except Exception as e:
            logger.error(f"Failed to extract content from HTML: {str(e)}", exc_info=True)
            raise Exception(f"Content extraction failed: {str(e)}")

    def _extract_summary(self, soup: BeautifulSoup) -> str:
        """Extract professional summary from HTML"""
        summary_section = soup.find(attrs={"data-section": "summary"})
        if summary_section:
            # Get text content, removing the section header
            text = summary_section.get_text(separator=" ", strip=True)
            # Remove common headers like "Professional Summary", "Summary", etc.
            text = re.sub(r'^(Professional\s+)?Summary:?\s*', '', text, flags=re.IGNORECASE)
            return text.strip()
        return ""

    def _extract_experiences(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract work experiences from HTML"""
        experiences = []

        # Find all experience sections
        experience_sections = soup.find_all(attrs={"data-section": "experience"})

        for exp_section in experience_sections:
            # Try to extract job title (usually in h3 or strong tag)
            job_title_elem = exp_section.find(['h3', 'h4', 'strong'])
            job_title = job_title_elem.get_text(strip=True) if job_title_elem else "Unknown Position"

            # Extract company name and dates (usually in a paragraph or span with class)
            company_info = ""
            company_elem = exp_section.find(class_=re.compile(r'company|info|meta'))
            if company_elem:
                company_info = company_elem.get_text(strip=True)
            else:
                # Fallback: look for paragraphs
                p_tags = exp_section.find_all('p')
                if p_tags:
                    company_info = p_tags[0].get_text(strip=True)

            # Parse company name from company_info
            # Format might be: "Company Name | Dates" or "Company Name, Dates"
            company = company_info.split('|')[0].split(',')[0].strip() if company_info else "Unknown Company"

            # Extract bullet points (usually in <li> tags)
            bullets = []
            ul_tag = exp_section.find('ul')
            if ul_tag:
                li_tags = ul_tag.find_all('li')
                bullets = [li.get_text(strip=True) for li in li_tags]
            else:
                # Fallback: look for paragraphs that might contain bullet content
                p_tags = exp_section.find_all('p')
                for p in p_tags[1:]:  # Skip first p (company info)
                    text = p.get_text(strip=True)
                    if text and not text.startswith(company):
                        bullets.append(text)

            experiences.append({
                "jobTitle": job_title,
                "company": company,
                "bullets": bullets
            })

        return experiences

    def _extract_skills(self, soup: BeautifulSoup) -> str:
        """Extract skills from HTML"""
        skills_section = soup.find(attrs={"data-section": "skills"})
        if skills_section:
            # Get text content, removing the section header
            text = skills_section.get_text(separator=" ", strip=True)
            # Remove common headers
            text = re.sub(r'^Skills:?\s*', '', text, flags=re.IGNORECASE)
            return text.strip()
        return ""

    def _extract_education(self, soup: BeautifulSoup) -> str:
        """Extract education from HTML"""
        education_section = soup.find(attrs={"data-section": "education"})
        if education_section:
            # Get text content, removing the section header
            text = education_section.get_text(separator="\n", strip=True)
            # Remove common headers
            text = re.sub(r'^Education:?\s*', '', text, flags=re.IGNORECASE)
            return text.strip()
        return ""

    def extract_plain_text(self, html_content: str) -> str:
        """
        Extract all text content from HTML for simple display.

        Args:
            html_content: Complete HTML document string

        Returns:
            Plain text version of the resume
        """
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            # Remove style and script tags
            for tag in soup(['style', 'script', 'head']):
                tag.decompose()

            # Get text
            text = soup.get_text(separator='\n', strip=True)

            # Clean up multiple newlines
            text = re.sub(r'\n\s*\n', '\n\n', text)

            return text.strip()

        except Exception as e:
            logger.error(f"Failed to extract plain text: {str(e)}")
            return ""
