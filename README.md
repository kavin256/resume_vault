# Resume Vault - Monorepo

Resume Vault is a full-stack application for managing your career profile and generating tailored resumes for different companies.

## Project Structure

This is a monorepo with separate frontend and backend applications:

```
resume_vault/
├── backend/           # FastAPI backend (Python)
│   ├── app/          # Application code
│   ├── config/       # Configuration
│   ├── main.py       # Entry point
│   └── README.md     # Backend documentation
├── frontend/          # Vue 3 frontend (TypeScript)
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── package.json  # NPM dependencies
├── templates/         # Legacy HTML templates (reference only)
├── static/           # Legacy static files (reference only)
└── README.md         # This file
```

## Quick Start

### Prerequisites

- **Python 3.9+** - For backend
- **Node.js 18+** - For frontend
- **npm** or **pnpm** - Package manager

### 1. Start the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Backend will be available at **http://localhost:8000**
- API Docs: http://localhost:8000/docs

### 2. Start the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

Frontend will be available at **http://localhost:5173**

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Local database (development)
- **Pydantic** - Data validation

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Next-generation frontend tooling
- **Vue Router** - Official routing library
- **Pinia** - State management
- **Axios** - HTTP client

## Features

### 1. Master Profile Management
- Store your complete, truthful career history
- Personal information, work experience, education
- Skills, certifications, projects, achievements
- The "No Lies" source of truth for all resumes

### 2. Company Vault
- Track companies and job opportunities
- Save job descriptions and requirements
- Monitor application status
- Store notes and relevant links

### 3. Resume Tailoring
- Generate tailored resumes with one click
- Mock tailor function (basic text merge)
- Track multiple resume versions per company
- View, copy, and print resumes

### 4. Mock Tailor Function
Currently uses a basic text merge algorithm:
- Combines master profile with job description
- Extracts keywords from job postings
- Creates structured markdown resumes
- Saves all versions to database

**Future Enhancement**: Will be replaced with AI-powered tailoring using OpenAI, Anthropic, or Google AI APIs.

## Development Workflow

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload

# Run tests (TODO)
pytest

# Format code
black .

# Type checking
mypy .
```

### Frontend Development

```bash
cd frontend

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint
npm run lint

# Type check
npm run type-check
```

## API Endpoints

### Profiles
- `GET /api/profiles` - List all profiles
- `POST /api/profiles` - Create profile
- `GET /api/profiles/{id}` - Get profile
- `PUT /api/profiles/{id}` - Update profile
- `DELETE /api/profiles/{id}` - Delete profile

### Companies
- `GET /api/companies` - List all companies
- `POST /api/companies` - Create company
- `GET /api/companies/{id}` - Get company
- `PUT /api/companies/{id}` - Update company
- `DELETE /api/companies/{id}` - Delete company

### Resumes
- `GET /api/resumes` - List all resumes
- `POST /api/resumes/tailor` - Generate tailored resume
- `GET /api/resumes/{id}` - Get resume
- `GET /api/resumes/company/{company_id}` - Get company resumes
- `DELETE /api/resumes/{id}` - Delete resume

## Environment Variables

### Backend (.env)
```bash
APP_NAME=Resume Vault
ENV=development
DATABASE_URL=sqlite:///./resume_vault.db

# Future AI Integration
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_AI_API_KEY=your_key_here

SECRET_KEY=your_secret_key
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

## Production Deployment

### Backend Deployment
The backend can be deployed to:
- Heroku
- AWS (ECS, Lambda)
- Google Cloud Run
- DigitalOcean App Platform
- Railway

### Frontend Deployment
The frontend can be deployed to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- GitHub Pages
- Cloudflare Pages

### Database Migration
For production, migrate from SQLite to:
- PostgreSQL (recommended)
- MySQL
- Cloud databases (AWS RDS, Google Cloud SQL)

## Future Enhancements

- [ ] AI-powered resume tailoring (OpenAI/Anthropic/Google AI)
- [ ] PDF export functionality
- [ ] Cloud database integration
- [ ] User authentication and multi-user support
- [ ] Resume templates and themes
- [ ] ATS optimization scoring
- [ ] Cover letter generation
- [ ] Interview preparation based on job descriptions
- [ ] Application tracking and reminders

## Contributing

1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions:
- Backend: See `backend/README.md`
- Frontend: See `frontend/README.md`
