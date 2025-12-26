# Resume Vault - Backend API

FastAPI backend service for Resume Vault application.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Local database (production will use PostgreSQL/MySQL)
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── profiles.py   # Master Profile CRUD
│   │   ├── companies.py  # Company management
│   │   └── resumes.py    # Resume generation & retrieval
│   ├── models/           # SQLAlchemy database models
│   │   ├── user_master_profile.py
│   │   ├── company.py
│   │   └── resume.py
│   ├── schemas/          # Pydantic schemas for validation
│   ├── database.py       # Database connection setup
│   └── utils.py          # Utility functions (mock tailor)
├── config/
│   └── settings.py       # Application settings
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 4. Run the Application

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Master Profile
- `POST /api/profiles/` - Create a new master profile
- `GET /api/profiles/` - Get all profiles
- `GET /api/profiles/{id}` - Get a specific profile
- `PUT /api/profiles/{id}` - Update a profile
- `DELETE /api/profiles/{id}` - Delete a profile

### Companies
- `POST /api/companies/` - Add a new company
- `GET /api/companies/` - Get all companies
- `GET /api/companies/{id}` - Get a specific company
- `PUT /api/companies/{id}` - Update a company
- `DELETE /api/companies/{id}` - Delete a company

### Resumes
- `POST /api/resumes/tailor` - Generate a tailored resume
- `GET /api/resumes/` - Get all resumes
- `GET /api/resumes/{id}` - Get a specific resume
- `GET /api/resumes/company/{company_id}` - Get all resumes for a company
- `DELETE /api/resumes/{id}` - Delete a resume

### Utility
- `GET /` - API information
- `GET /health` - Health check with database status

## Mock Tailor Function

The backend includes a mock tailor function (`app/utils.py`) that:
- Takes the user's master profile
- Combines it with the company's job description
- Creates a structured markdown resume
- Extracts keywords from the job description
- Saves the tailored resume to the database

**Future Enhancement**: This will be replaced with AI-powered tailoring using OpenAI, Anthropic, or Google AI APIs.

## Database

The application uses SQLite for local development. The database file is `resume_vault.db`.

### Tables

1. **user_master_profile** - Complete career history
2. **companies** - Company and job description data
3. **resumes** - Generated tailored resumes

### Migrations

For production, use Alembic for database migrations:

```bash
# Initialize Alembic (already configured)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Development

### Running Tests

```bash
# TODO: Set up pytest
pytest
```

### Code Quality

```bash
# Format code with black
black .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .
```

## Environment Variables

- `APP_NAME` - Application name
- `ENV` - Environment (development/production)
- `DATABASE_URL` - Database connection string
- `OPENAI_API_KEY` - OpenAI API key (for future AI integration)
- `ANTHROPIC_API_KEY` - Anthropic API key (for future AI integration)
- `GOOGLE_AI_API_KEY` - Google AI API key (for future AI integration)
- `SECRET_KEY` - Application secret key
- `ALLOWED_ORIGINS` - CORS allowed origins

## Production Deployment

### Database Migration

Update `DATABASE_URL` in `.env` to point to PostgreSQL or MySQL:

```
DATABASE_URL=postgresql://user:password@host:port/database
```

### Deployment Platforms

The backend can be deployed to:
- **Heroku** - Simple deployment with Postgres add-on
- **AWS ECS/Lambda** - Scalable container/serverless deployment
- **Google Cloud Run** - Serverless containers
- **DigitalOcean App Platform** - Simple PaaS deployment
- **Railway** - Modern deployment platform

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## License

[Add your license here]
