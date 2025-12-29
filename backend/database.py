"""
MongoDB Database Connection Module
Handles connection lifecycle for Resume Vault application
"""

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Global client instance
mongo_client = None
database = None


async def connect_to_mongo():
    """Connect to MongoDB on app startup"""
    global mongo_client, database

    try:
        # Create client with TLS/SSL options
        mongo_client = AsyncIOMotorClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True  # For development; use proper certs in production
        )
        database = mongo_client[DATABASE_NAME]

        # Test connection
        await mongo_client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {DATABASE_NAME}")

    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection on app shutdown"""
    global mongo_client

    if mongo_client:
        mongo_client.close()
        print("✓ MongoDB connection closed")


def get_database():
    """Get database instance"""
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return database
