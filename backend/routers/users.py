"""
User Management Router
Handles user synchronization and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from database import get_database
from auth import verify_clerk_token
from models import UserSyncResponse
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


class UserSyncRequest(BaseModel):
    """Request body for user sync"""
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@router.post("/sync", response_model=UserSyncResponse)
async def sync_user(
    user_data: UserSyncRequest = Body(default=None),
    token_payload: dict = Depends(verify_clerk_token)
):
    """
    Sync user from Clerk to MongoDB.

    Creates user if doesn't exist, otherwise returns existing user.
    This endpoint should be called after user signs in on the frontend.

    The user data is extracted from the verified Clerk JWT token,
    ensuring security and preventing data tampering.

    Args:
        token_payload: Verified JWT token payload (injected by dependency)

    Returns:
        UserSyncResponse: Status and user information

    Raises:
        HTTPException: If token is invalid or database operation fails
    """
    db = get_database()
    users_collection = db["users"]

    # Extract user ID from verified Clerk token
    # Clerk stores user_id in 'sub' claim (standard JWT practice)
    clerk_user_id = token_payload.get("sub")

    if not clerk_user_id:
        logger.error(f"Invalid token: missing user ID. Token payload: {token_payload}")
        raise HTTPException(status_code=400, detail="Invalid token: missing user ID")

    # Get user data from request body (sent from frontend)
    email = user_data.email if user_data else None
    first_name = user_data.first_name if user_data else None
    last_name = user_data.last_name if user_data else None

    logger.info(f"Syncing user: {clerk_user_id}, email: {email}, name: {first_name} {last_name}")

    try:
        # Check if user already exists
        existing_user = await users_collection.find_one({"clerk_user_id": clerk_user_id})

        if existing_user:
            logger.info(f"User already exists: {clerk_user_id}")
            return UserSyncResponse(
                status="already_exists",
                user_id=clerk_user_id,
                message="User already synced"
            )

        # Create new user document
        user_doc = {
            "clerk_user_id": clerk_user_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insert into MongoDB
        result = await users_collection.insert_one(user_doc)

        logger.info(f"User created successfully: {clerk_user_id}")

        return UserSyncResponse(
            status="created",
            user_id=clerk_user_id,
            message="User created successfully"
        )

    except Exception as e:
        logger.error(f"User sync failed for {clerk_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during user sync"
        )
