"""
Clerk Authentication Module
Handles JWT token verification for secured endpoints
"""

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
import os
import base64
import json
import certifi
from typing import Dict
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")


def decode_clerk_domain() -> str:
    """
    Decode Clerk domain from publishable key

    Clerk publishable keys are base64 encoded and contain the instance domain.
    Format: pk_test_<base64_encoded_data>

    Returns:
        str: Clerk instance domain (e.g., 'beloved-tiger-37.clerk.accounts.dev')
    """
    if not CLERK_PUBLISHABLE_KEY:
        raise RuntimeError("CLERK_PUBLISHABLE_KEY not found in environment variables")

    # Extract the base64 part after 'pk_test_' or 'pk_live_'
    if CLERK_PUBLISHABLE_KEY.startswith('pk_test_'):
        encoded_part = CLERK_PUBLISHABLE_KEY[8:]  # Remove 'pk_test_'
    elif CLERK_PUBLISHABLE_KEY.startswith('pk_live_'):
        encoded_part = CLERK_PUBLISHABLE_KEY[8:]  # Remove 'pk_live_'
    else:
        raise ValueError("Invalid Clerk publishable key format")

    try:
        # Decode base64
        decoded_bytes = base64.b64decode(encoded_part)
        decoded_str = decoded_bytes.decode('utf-8')

        # Remove trailing '$' if present
        domain = decoded_str.rstrip('$')

        return domain
    except Exception as e:
        raise ValueError(f"Failed to decode Clerk publishable key: {e}")


@lru_cache()
def get_jwks_client() -> PyJWKClient:
    """
    Get cached JWKS client for verifying Clerk JWT tokens

    Returns:
        PyJWKClient: Client configured with Clerk's JWKS endpoint
    """
    clerk_domain = decode_clerk_domain()
    jwks_url = f"https://{clerk_domain}/.well-known/jwks.json"

    print(f"Using Clerk JWKS URL: {jwks_url}")

    # Use certifi for SSL certificate verification to fix SSL errors on macOS
    import ssl
    import urllib.request
    
    # Create SSL context with certifi certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # Create a custom opener with the SSL context
    https_handler = urllib.request.HTTPSHandler(context=ssl_context)
    opener = urllib.request.build_opener(https_handler)
    urllib.request.install_opener(opener)

    return PyJWKClient(jwks_url)


async def verify_clerk_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict:
    """
    Verify Clerk JWT token and return decoded payload

    This function:
    1. Extracts the token from the Authorization header
    2. Fetches Clerk's public keys (JWKS)
    3. Verifies the token signature
    4. Validates token expiration
    5. Returns the decoded token payload

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        Dict: Decoded token payload containing user_id, email, etc.

    Raises:
        HTTPException: If token is invalid, expired, or verification fails
    """
    token = credentials.credentials

    try:
        jwks_client = get_jwks_client()

        # Get the signing key from the JWT
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Verify and decode token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True}
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Token verification failed: {str(e)}"
        )
