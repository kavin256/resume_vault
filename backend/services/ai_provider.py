"""
Abstract Base Class for AI Providers
Defines the contract that all AI providers must implement
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class TailoredExperience(BaseModel):
    """Tailored work experience entry"""
    jobTitle: str
    companyName: str
    tailored_bullets: List[str] = Field(default_factory=list)


class TailoredResume(BaseModel):
    """Data model for AI-tailored resume content"""
    tailored_summary: str = Field(..., description="Rewritten professional summary optimized for the role")
    tailored_experience: List[TailoredExperience] = Field(
        default_factory=list,
        description="List of work experiences with tailored bullet points"
    )
    keyword_matches: List[str] = Field(
        default_factory=list,
        description="Key keywords from job description that match candidate profile"
    )
    recommendations: str = Field(
        default="",
        description="Strategic recommendations for this application"
    )


class BaseAIProvider(ABC):
    """
    Abstract base class for AI providers.

    All AI provider implementations (Claude, OpenAI, etc.) must inherit from this
    class and implement the required methods.
    """

    def __init__(self, api_key: str, model: str = None):
        """
        Initialize AI provider.

        Args:
            api_key: API key for the AI service
            model: Model identifier (optional, provider-specific)
        """
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def tailor_resume(
        self,
        master_profile: Dict[str, Any],
        job_description: str,
        company_name: str,
        position: str
    ) -> TailoredResume:
        """
        Analyze job description and tailor resume content.

        This method should:
        1. Analyze the job description to identify key requirements
        2. Rewrite the professional summary to emphasize relevant skills
        3. Rewrite work experience bullets to highlight relevant achievements
        4. Identify keywords that should be emphasized
        5. Provide strategic recommendations

        Args:
            master_profile: Complete user profile dictionary
            job_description: Full text of the job posting
            company_name: Name of the company
            position: Job title/position

        Returns:
            TailoredResume object with customized content
        """
        pass

    @abstractmethod
    async def generate_cover_letter(
        self,
        master_profile: Dict[str, Any],
        job_description: str,
        company_name: str,
        position: str,
        tailored_resume: TailoredResume
    ) -> str:
        """
        Generate a personalized cover letter.

        Args:
            master_profile: Complete user profile dictionary
            job_description: Full text of the job posting
            company_name: Name of the company
            position: Job title/position
            tailored_resume: The tailored resume content for context

        Returns:
            Cover letter content as a string
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify API connectivity and credentials.

        Returns:
            True if API is accessible and credentials are valid, False otherwise
        """
        pass
