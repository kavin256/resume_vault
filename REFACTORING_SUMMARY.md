# Resume Vault - Brick-Based Architecture Refactoring

## Overview

The entire backend has been successfully refactored from a monolithic profile system to an intelligent brick-based architecture. This implements the core concept requested: a Master Profile made of reusable "bricks" that can be intelligently selected to create ATS-optimized, tailored resumes.

---

## What Was Completed

### 1. Database Schema Redesign ✅

**Old Architecture (Removed):**
- `user_master_profile.py` - Monolithic profile with large text fields
- `company.py` - Simple company storage
- `resume.py` - Basic resume tracking

**New Brick-Based Architecture:**

#### Core Models:
- **`user.py`** - Simplified user identity (name, email, contact info, professional summary)
- **`bricks.py`** - Reusable components:
  - `Project` - Individual projects with technologies, impact metrics, tags
  - `Skill` - Skills with categories (technical, soft, language, tool, framework)
  - `ExperienceBullet` - STAR-format bullets with metrics tracking
  - `Achievement` - Awards and recognition
  - `Education` - Degrees and coursework
  - `Certification` - Professional certifications
- **`job_description.py`** - JD storage with AI-extracted insights:
  - Extracted keywords
  - Required/preferred skills
  - Keyword density analysis
  - Action verbs tracking
- **`application.py`** - Application Vault:
  - Links JD + selected bricks + generated resume
  - Tracks match scores and ATS optimization
  - Version control with `ApplicationVersion` model

**Database Recreation:**
- Old `resume_vault.db` deleted
- New schema created with all 10 brick-based tables
- All tables properly indexed with foreign key relationships

---

### 2. Pydantic Schemas Created ✅

Created comprehensive schemas for validation and serialization:

#### User Schemas (`schemas/user.py`):
- `UserCreate`, `UserUpdate`, `UserResponse`

#### Brick Schemas (`schemas/bricks.py`):
- Project: `ProjectCreate`, `ProjectUpdate`, `ProjectResponse`
- Skill: `SkillCreate`, `SkillUpdate`, `SkillResponse`
- ExperienceBullet: `ExperienceBulletCreate`, `ExperienceBulletUpdate`, `ExperienceBulletResponse`
- Achievement: `AchievementCreate`, `AchievementUpdate`, `AchievementResponse`
- Education: `EducationCreate`, `EducationUpdate`, `EducationResponse`
- Certification: `CertificationCreate`, `CertificationUpdate`, `CertificationResponse`

#### Job Description Schemas (`schemas/job_description.py`):
- `JobDescriptionCreate`, `JobDescriptionUpdate`, `JobDescriptionResponse`
- `JobDescriptionWithStats` - Extended schema with application count

#### Application Schemas (`schemas/application.py`):
- `ApplicationCreate`, `ApplicationUpdate`, `ApplicationResponse`
- `ApplicationWithDetails` - Extended schema with JD details
- `ApplicationVersionCreate`, `ApplicationVersionResponse`
- **`TailorRequest`** - Schema for the 1-2-3 workflow
- **`TailorResponse`** - Response with match scores and suggestions

---

### 3. API Endpoints Implemented ✅

#### Users API (`api/users.py`):
- `POST /api/users` - Create user
- `GET /api/users` - List users
- `GET /api/users/{user_id}` - Get specific user
- `PATCH /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user (cascades to all bricks)

#### Bricks API (`api/bricks.py`):
Comprehensive CRUD for all 6 brick types:

**Projects:**
- `POST /api/bricks/projects?user_id=X` - Create project
- `GET /api/bricks/projects?user_id=X&featured_only=true` - List projects
- `GET /api/bricks/projects/{id}` - Get project
- `PATCH /api/bricks/projects/{id}` - Update project
- `DELETE /api/bricks/projects/{id}` - Delete project

**Skills:**
- `POST /api/bricks/skills?user_id=X` - Create skill
- `GET /api/bricks/skills?user_id=X&category=technical&certified_only=true` - List skills
- `GET /api/bricks/skills/{id}` - Get skill
- `PATCH /api/bricks/skills/{id}` - Update skill
- `DELETE /api/bricks/skills/{id}` - Delete skill

**Experience Bullets:**
- `POST /api/bricks/experience?user_id=X` - Create bullet
- `GET /api/bricks/experience?user_id=X&company_name=X&featured_only=true` - List bullets
- `GET /api/bricks/experience/{id}` - Get bullet
- `PATCH /api/bricks/experience/{id}` - Update bullet
- `DELETE /api/bricks/experience/{id}` - Delete bullet

**Achievements, Education, Certifications:**
- Similar CRUD patterns for each brick type

#### Job Descriptions API (`api/job_descriptions.py`):
- `POST /api/job-descriptions` - Create JD (Step 1 of workflow)
- `GET /api/job-descriptions?status_filter=X&company_filter=X` - List JDs
- `GET /api/job-descriptions/{id}` - Get JD
- `PATCH /api/job-descriptions/{id}` - Update JD
- `DELETE /api/job-descriptions/{id}` - Delete JD (cascades to applications)

#### Applications API (`api/applications.py`):
**Application Management:**
- `POST /api/applications?user_id=X` - Create application manually
- `GET /api/applications?user_id=X&status_filter=draft&archived=false` - List applications (Vault view)
- `GET /api/applications/{id}` - Get application with full details
- `PATCH /api/applications/{id}` - Update application (status, notes, etc.)
- `DELETE /api/applications/{id}` - Delete application

**Version Control:**
- `POST /api/applications/{id}/versions` - Create new version for A/B testing
- `GET /api/applications/{id}/versions` - List all versions

**1-2-3 Tailoring Workflow:**
- `POST /api/applications/tailor?user_id=X` - The core workflow endpoint
  - Takes `TailorRequest` with JD ID and optional brick selections
  - Returns `TailorResponse` with match scores, suggestions, and resume preview
  - Creates permanent Application record in the vault

---

## API Documentation

**Interactive Swagger UI:**
http://localhost:8000/docs

**API Base URL:**
http://localhost:8000/api

**Health Check:**
http://localhost:8000/health

---

## Architecture Highlights

### Brick-Based System
Each "brick" is:
- **Self-contained** - Complete information in one place
- **Truthful** - Based on real experience
- **Reusable** - Can be used across multiple resumes
- **Selectable** - Tagged for intelligent AI matching
- **Categorizable** - Flagged for filtering (featured, leadership, technical, etc.)

### Application Vault
Every tailored resume is permanently stored with:
- Snapshot of the job description
- Which bricks were selected
- Match score (0-100%)
- Keywords matched from JD
- ATS optimization score
- Template used
- Generated resume content
- File path to PDF
- Application tracking (dates, status, notes)

### 1-2-3 Workflow
1. **Context Capture**: User pastes job description → `/api/job-descriptions`
2. **Intelligent Mapping**: AI selects matching bricks → `/api/applications/tailor`
3. **Generate Resume**: Optimized resume created → Saved in Application Vault

---

## File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py              # User CRUD
│   │   ├── bricks.py             # All brick CRUD operations
│   │   ├── job_descriptions.py   # JD management
│   │   └── applications.py       # Tailoring workflow + Application Vault
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py               # User model
│   │   ├── bricks.py             # 6 brick models
│   │   ├── job_description.py    # JD with AI insights
│   │   └── application.py        # Application + Version models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bricks.py             # All brick schemas
│   │   ├── job_description.py
│   │   └── application.py        # Includes TailorRequest/Response
│   └── database.py               # Updated with new models
├── config/
│   └── settings.py
├── main.py                       # Updated with new routers
└── resume_vault.db              # New schema with 10 tables
```

---

## What's Next (TODO)

The foundation is now complete. Here's what needs to be implemented:

### 5. Intelligent Tailoring Engine 🔄
- **Keyword extraction** from job descriptions (NLP)
- **Brick selection algorithm** (match JD keywords to brick tags)
- **Match score calculation** (0-100% based on keyword coverage)
- **ATS optimization logic** (keyword density, action verbs, formatting)

### 6. Synonym Mapping 🔄
- Dictionary of technical term synonyms
- Replace user's terms with JD-preferred terms
- Example: "Team Coordination" → "Agile Management"

### 7. Frontend 1-2-3 Wizard 🔄
- Step 1: Paste JD form
- Step 2: Review/modify selected bricks
- Step 3: Preview and download resume

### 8. Template System 🔄
- ATS-optimized template (default, minimal formatting)
- Creative template
- Corporate template

### 9. PDF Generation 🔄
- Library selection (ReportLab, WeasyPrint, or similar)
- Clean, ATS-friendly export
- Include metadata

### 10. Application Vault UI 🔄
- List view with search/filter
- Folder organization (Company - Position - Date)
- Historical tracking

---

## Testing the New Backend

### 1. View API Documentation
Open http://localhost:8000/docs in your browser to see all endpoints.

### 2. Create a User
```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0100",
    "location": "San Francisco, CA",
    "professional_summary": "Full-stack developer with 5 years of experience"
  }'
```

### 3. Add Some Bricks
```bash
# Add a project
curl -X POST "http://localhost:8000/api/bricks/projects?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "E-commerce Platform",
    "description": "Built a scalable e-commerce platform",
    "technologies": "React, Node.js, PostgreSQL",
    "impact_metrics": "Increased sales by 40%",
    "tags": "react, nodejs, ecommerce, scalability"
  }'

# Add a skill
curl -X POST "http://localhost:8000/api/bricks/skills?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "React",
    "category": "framework",
    "proficiency": "Expert",
    "years_of_experience": 5
  }'
```

### 4. Create a Job Description
```bash
curl -X POST "http://localhost:8000/api/job-descriptions" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "job_title": "Senior Frontend Developer",
    "raw_description": "We are looking for a Senior Frontend Developer with React expertise..."
  }'
```

### 5. Generate Tailored Resume
```bash
curl -X POST "http://localhost:8000/api/applications/tailor?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description_id": 1,
    "template": "ats_optimized"
  }'
```

---

## Summary

✅ **Completed:**
- Database schema completely redesigned with brick-based architecture
- All old models removed and replaced with new brick models
- Comprehensive Pydantic schemas for all models
- Full CRUD API endpoints for all brick types
- Application Vault system implemented
- 1-2-3 tailoring workflow foundation created
- Backend server running successfully

🔄 **In Progress / TODO:**
- Intelligent tailoring engine (keyword extraction, brick selection)
- Synonym mapping for ATS optimization
- Frontend 1-2-3 wizard interface
- Template system
- PDF generation
- Application Vault UI

The foundation is now solid and ready for the intelligent AI features to be built on top of it!
