"""
Resume Vault - Backend API

FastAPI backend for managing career profiles and generating tailored resumes.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from config.settings import settings
from app.database import get_db, init_db
from app.api import users, bricks, job_descriptions, applications

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Manage your master career profile and generate tailored resumes for different companies",
    version="0.1.0",
)

# Configure CORS - Allow frontend to communicate with backend
allowed_origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative frontend dev server
    "http://localhost:8080",  # Alternative frontend dev server
]

# Add additional origins from settings if needed
if settings.allowed_origins:
    allowed_origins.extend(settings.allowed_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize the database on application startup.

    TODO: In production, use Alembic migrations instead of init_db()
    """
    print(f"Starting {settings.app_name}...")
    print(f"Environment: {settings.env}")
    print(f"Database: {settings.database_url}")
    init_db()


# Include API routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(bricks.router, prefix="/api/bricks", tags=["bricks"])
app.include_router(job_descriptions.router, prefix="/api/job-descriptions", tags=["job-descriptions"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])


@app.get("/")
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "api_prefix": "/api"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint with database connectivity test.
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "environment": settings.env,
    }


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.env == "development" else False,
    )
