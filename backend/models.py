"""
Pydantic Models for Resume Vault
Defines data schemas for API requests and responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User model for MongoDB storage"""
    clerk_user_id: str = Field(..., description="Clerk's unique user ID")
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "clerk_user_id": "user_2abc123def456",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class UserSyncResponse(BaseModel):
    """Response model for user sync endpoint"""
    status: str = Field(..., description="Status: 'created' or 'already_exists'")
    user_id: str = Field(..., description="Clerk user ID")
    message: str = Field(..., description="Human-readable message")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "created",
                "user_id": "user_2abc123def456",
                "message": "User created successfully"
            }
        }
