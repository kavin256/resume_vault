"""
Anthropic Claude AI Provider Implementation
Uses Claude API for resume tailoring and cover letter generation
"""

import httpx
import json
import os
from typing import Dict, Any
from .ai_provider import BaseAIProvider, TailoredResume, TailoredExperience
import logging

logger = logging.getLogger(__name__)


class ClaudeProvider(BaseAIProvider):
    """Anthropic Claude implementation of AI provider"""

    BASE_URL = "https://api.anthropic.com/v1/messages"
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

    def __init__(self, api_key: str, model: str = None):
        """
        Initialize Claude provider.

        Args:
            api_key: Anthropic API key
            model: Claude model to use (defaults to claude-3-5-sonnet-20241022)
        """
        super().__init__(api_key, model or self.DEFAULT_MODEL)
        timeout = float(os.getenv("AI_TIMEOUT", "60"))
        
        # Create client with SSL verification disabled if needed (for development)
        # In production, you should fix SSL certificate issues properly
        verify_ssl = os.getenv("VERIFY_SSL", "true").lower() != "false"
        
        self.client = httpx.AsyncClient(
            timeout=timeout,
            verify=verify_ssl
        )
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "4096"))
        
        if not verify_ssl:
            logger.warning("SSL verification is disabled - this should only be used in development!")

    async def tailor_resume(
        self,
        master_profile: Dict[str, Any],
        job_description: str,
        company_name: str,
        position: str
    ) -> TailoredResume:
        """
        Tailor resume using Claude AI.

        Args:
            master_profile: Complete user profile dictionary
            job_description: Full text of the job posting
            company_name: Name of the company
            position: Job title/position

        Returns:
            TailoredResume object with customized content
        """
        logger.info(f"Tailoring resume for {company_name} - {position}")

        prompt = self._build_tailoring_prompt(
            master_profile, job_description, company_name, position
        )

        try:
            response = await self._call_api(prompt)
            tailored = self._parse_tailoring_response(response)
            logger.info(f"Successfully tailored resume with {len(tailored.tailored_experience)} experiences")
            return tailored
        except Exception as e:
            logger.error(f"Error tailoring resume: {str(e)}", exc_info=True)
            raise

    async def generate_cover_letter(
        self,
        master_profile: Dict[str, Any],
        job_description: str,
        company_name: str,
        position: str,
        tailored_resume: TailoredResume
    ) -> str:
        """
        Generate cover letter using Claude AI.

        Args:
            master_profile: Complete user profile dictionary
            job_description: Full text of the job posting
            company_name: Name of the company
            position: Job title/position
            tailored_resume: The tailored resume content for context

        Returns:
            Cover letter content as a string
        """
        logger.info(f"Generating cover letter for {company_name} - {position}")

        prompt = self._build_cover_letter_prompt(
            master_profile, job_description, company_name, position, tailored_resume
        )

        try:
            response = await self._call_api(prompt)
            cover_letter = self._parse_text_response(response)
            logger.info("Successfully generated cover letter")
            return cover_letter
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}", exc_info=True)
            raise

    async def health_check(self) -> bool:
        """
        Verify API connectivity and credentials.

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            test_prompt = "Respond with 'OK' if you can read this message."
            response = await self._call_api(test_prompt, max_tokens=10)
            return response is not None
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False

    def _build_tailoring_prompt(
        self,
        profile: Dict[str, Any],
        jd: str,
        company: str,
        position: str
    ) -> str:
        """Construct detailed prompt for resume tailoring"""

        # Extract profile data
        personal_info = profile.get('personalInfo', {})
        first_name = personal_info.get('firstName', '')
        last_name = personal_info.get('lastName', '')
        summary = profile.get('summary', '')
        headline = profile.get('professionalHeadline', '')

        # Format work experience
        experiences = profile.get('workExperience', [])
        experience_text = self._format_work_experiences(experiences)

        # Format skills
        skills = profile.get('skills', [])
        skills_text = ', '.join([s.get('name', '') for s in skills]) if skills else 'Not specified'

        # Format education
        education = profile.get('education', [])
        education_text = self._format_education(education)

        # Format certifications
        certifications = profile.get('certifications', [])
        cert_text = self._format_certifications(certifications)

        return f"""You are an expert resume writer and ATS optimization specialist. Analyze this job description and tailor the candidate's resume content to maximize their chances of success.

JOB POSTING:
Company: {company}
Position: {position}
Description: {jd}

CANDIDATE PROFILE:
Name: {first_name} {last_name}
Professional Headline: {headline}
Current Summary: {summary}

Work Experience:
{experience_text}

Skills: {skills_text}

Education:
{education_text}

Certifications:
{cert_text}

TASK:
1. PROFESSIONAL SUMMARY (3-4 sentences):
   - Rewrite to emphasize the most relevant qualifications for THIS specific role
   - Include 2-3 key achievements with metrics if possible
   - Incorporate critical keywords from the job description naturally
   - Match the tone and language used in the job posting

2. WORK EXPERIENCE OPTIMIZATION:
   For each work experience role, rewrite the bullet points to:
   - Start with strong action verbs (Led, Developed, Implemented, Architected, etc.)
   - Quantify achievements wherever possible (percentages, dollar amounts, time saved, team size, etc.)
   - Highlight skills, technologies, and experiences mentioned in the job description
   - Focus on outcomes and business impact, not just responsibilities
   - Keep bullets concise (1-2 lines maximum)
   - Ensure bullets are relevant to the target position

3. KEYWORD ANALYSIS:
   Identify 10-15 critical keywords, skills, and technologies from the job description that should be emphasized in the resume.

4. STRATEGIC RECOMMENDATIONS:
   Provide 2-3 specific, actionable suggestions to strengthen this application based on gaps or opportunities you've identified.

CRITICAL TEXT FORMATTING RULES:
- AVOID these LaTeX special characters in your output: ampersand, percent, dollar, hash, underscore, braces, tilde, caret, backslash
- Use "and" instead of ampersand symbol
- Use "percent" or write out percentages as "50 percent" instead of using percent symbol
- Use regular quotes instead of special quote characters
- Use plain hyphens for ranges (2020-2023) not em-dashes
- Do NOT use any markup, markdown, or special formatting
- Write in plain text only

CRITICAL: Return ONLY valid JSON matching this exact structure (no markdown, no code blocks, just pure JSON):
{{
    "tailored_summary": "The rewritten professional summary optimized for this role",
    "tailored_experience": [
        {{
            "jobTitle": "exact job title from candidate profile",
            "companyName": "exact company name from candidate profile",
            "tailored_bullets": ["bullet point 1", "bullet point 2", "bullet point 3"]
        }}
    ],
    "keyword_matches": ["keyword1", "keyword2", "keyword3"],
    "recommendations": "Strategic recommendations as a single string with newlines for separation"
}}"""

    def _build_cover_letter_prompt(
        self,
        profile: Dict[str, Any],
        jd: str,
        company: str,
        position: str,
        tailored_resume: TailoredResume
    ) -> str:
        """Construct prompt for cover letter generation"""

        personal_info = profile.get('personalInfo', {})
        first_name = personal_info.get('firstName', '')
        last_name = personal_info.get('lastName', '')

        # Get key achievements from tailored resume
        key_points = tailored_resume.keyword_matches[:5] if tailored_resume.keyword_matches else []

        return f"""You are an expert cover letter writer. Create a compelling, personalized cover letter for this job application.

JOB POSTING:
Company: {company}
Position: {position}
Description: {jd}

CANDIDATE:
Name: {first_name} {last_name}
Tailored Summary: {tailored_resume.tailored_summary}
Key Strengths: {', '.join(key_points)}

INSTRUCTIONS:
Write a professional cover letter (3-4 paragraphs) that:
1. Opens with a strong hook that shows genuine interest in the role and company
2. Highlights 2-3 most relevant achievements or experiences (be specific and quantitative)
3. Demonstrates understanding of the company's needs and how the candidate can address them
4. Closes with enthusiasm and a clear call to action
5. Maintains a professional yet personable tone
6. Keeps total length to 300-400 words

CRITICAL FORMATTING REQUIREMENTS:
- Use "Dear Hiring Manager," as the salutation
- End with "Sincerely," followed by the candidate's ACTUAL name: {first_name} {last_name}
- DO NOT use placeholders like "[Your Name]" - use the real name provided above
- DO NOT include any brackets, placeholders, or generic text

CRITICAL TEXT FORMATTING RULES:
- AVOID these LaTeX special characters: ampersand, percent, dollar, hash, underscore, braces, tilde, caret, backslash
- Use "and" instead of ampersand symbol
- Use "percent" or write out percentages as "50 percent" instead of using percent symbol
- Use regular quotes instead of special quote characters
- Use plain hyphens for ranges (2020-2023) not em-dashes
- Do NOT use any markup, markdown, or special formatting
- Write in plain text only

Return ONLY the cover letter text, no JSON, no additional commentary."""

    async def _call_api(self, prompt: str, max_tokens: int = None) -> Dict[str, Any]:
        """
        Make API request to Claude.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate (optional)

        Returns:
            API response as dictionary
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = await self.client.post(
                self.BASE_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise Exception("AI service rate limit exceeded - please wait and retry")
            elif e.response.status_code == 401:
                raise Exception("AI service authentication failed - check ANTHROPIC_API_KEY")
            else:
                raise Exception(f"AI service error: {e.response.status_code} - {e.response.text}")
        except httpx.TimeoutException:
            raise Exception("AI service timeout - please try again")
        except Exception as e:
            raise Exception(f"Failed to call AI service: {str(e)}")

    def _parse_tailoring_response(self, response: Dict) -> TailoredResume:
        """
        Extract tailored content from Claude's response.

        Args:
            response: Raw API response

        Returns:
            TailoredResume object
        """
        try:
            content = response['content'][0]['text']

            # Claude might wrap JSON in markdown code blocks, so let's extract it
            if '```json' in content:
                # Extract JSON from markdown code block
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                content = content[json_start:json_end].strip()
            elif '```' in content:
                # Extract from generic code block
                json_start = content.find('```') + 3
                json_end = content.find('```', json_start)
                content = content[json_start:json_end].strip()

            # Clean control characters from JSON string
            # Replace problematic control characters while preserving valid JSON structure
            import re
            # Remove or replace invalid control characters (except \n, \r, \t which are valid when escaped)
            content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', content)
            
            # Parse JSON with strict=False to be more lenient
            data = json.loads(content, strict=False)

            # Convert to TailoredResume model
            tailored_exp = [
                TailoredExperience(**exp) for exp in data.get('tailored_experience', [])
            ]

            return TailoredResume(
                tailored_summary=data.get('tailored_summary', ''),
                tailored_experience=tailored_exp,
                keyword_matches=data.get('keyword_matches', []),
                recommendations=data.get('recommendations', '')
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            logger.error(f"Response content: {response}")
            raise Exception(f"Invalid response from AI service: {str(e)}")

    def _parse_text_response(self, response: Dict) -> str:
        """Extract plain text from Claude's response"""
        try:
            return response['content'][0]['text'].strip()
        except (KeyError, TypeError) as e:
            raise Exception(f"Invalid response from AI service: {str(e)}")

    def _format_work_experiences(self, experiences: list) -> str:
        """Format work experiences for prompt"""
        if not experiences:
            return "No work experience provided"

        formatted = []
        for exp in experiences:
            job_title = exp.get('jobTitle', 'Unknown Position')
            company = exp.get('companyName', 'Unknown Company')
            start = exp.get('startDate', '')
            end = exp.get('endDate', 'Present') if not exp.get('currentlyWorking', False) else 'Present'

            exp_text = f"- {job_title} at {company} ({start} - {end})"

            # Add responsibilities
            responsibilities = exp.get('responsibilities', [])
            if responsibilities:
                exp_text += "\n  Responsibilities: " + "; ".join(responsibilities)

            # Add achievements
            achievements = exp.get('achievements', [])
            if achievements:
                exp_text += "\n  Achievements: " + "; ".join(achievements)

            # Add technologies
            technologies = exp.get('technologies', [])
            if technologies:
                exp_text += "\n  Technologies: " + ", ".join(technologies)

            formatted.append(exp_text)

        return "\n\n".join(formatted)

    def _format_education(self, education: list) -> str:
        """Format education for prompt"""
        if not education:
            return "No education provided"

        formatted = []
        for edu in education:
            degree = edu.get('degree', '')
            field = edu.get('fieldOfStudy', '')
            institution = edu.get('institution', '')
            year = edu.get('endYear', '')

            edu_text = f"- {degree} in {field}, {institution}"
            if year:
                edu_text += f" ({year})"

            formatted.append(edu_text)

        return "\n".join(formatted)

    def _format_certifications(self, certifications: list) -> str:
        """Format certifications for prompt"""
        if not certifications:
            return "No certifications"

        formatted = []
        for cert in certifications:
            name = cert.get('name', '')
            org = cert.get('issuingOrganization', '')
            cert_text = f"- {name}"
            if org:
                cert_text += f" ({org})"
            formatted.append(cert_text)

        return "\n".join(formatted)

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close HTTP client"""
        await self.client.aclose()
