# Resume Vault

**Your personal resume generation assistant - create tailored resumes and cover letters in seconds.**

---

## 📖 Introduction

Resume Vault is a web application that helps job seekers create customized resumes and cover letters tailored to specific job postings. Instead of manually editing your resume for each application, Resume Vault streamlines the process:

1. **Build your Master Profile once** - Store all your professional information in one place
2. **Paste any job description** - Just copy the job posting you're applying for
3. **Generate instantly** - Get a tailored resume and cover letter as downloadable PDFs

### Why Resume Vault?

- **Save time** - No more manual resume editing for every application
- **Stay organized** - Keep all your professional information in one master profile
- **Professional output** - Generate polished PDF documents ready to submit
- **Easy workflow** - Simple two-step process: profile → generate

### How It Works (User Perspective)

**Step 1: Create Your Master Profile**
- Navigate to the "Master Profile" page
- Fill in your personal information (name, email, phone)
- Write your professional summary
- Add your work experience with detailed accomplishments
- List your technical skills
- Include your education and certifications

**Step 2: Generate Documents**
- Go to the "Generate Resume" page
- Enter the job details (company name, position, job ID, posting link)
- Paste the full job description
- Click "Generate Resume & Cover Letter"
- Download both PDFs and submit your application

The application uses your master profile and analyzes the job description to create customized documents that highlight the most relevant aspects of your experience.

---

## 🎯 Key Features

- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Vertical Sidebar Navigation** - Easy navigation between pages
- **Form Validation** - Ensures all required information is provided
- **Test Data Buttons** - Quickly fill forms with sample data for testing
- **Clean Professional UI** - Modern, distraction-free interface
- **Instant PDF Generation** - Download your documents immediately

---

## 🚀 How to Start

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Runs on: **http://localhost:8000**

### Frontend (Vue 3)
```bash
cd frontend
npm install
npm run dev
```
Runs on: **http://localhost:5176** (or next available port)

---

## 🧪 Quick Start Guide

1. **Open the application** - Navigate to **http://localhost:5175/profile** in your browser
2. **Fill your Master Profile**:
   - Click "Fill with Test Data" button for quick demo (or enter your real information)
   - Complete all required fields (marked with *)
   - Click "Continue to Generate Resume →"
3. **Generate your documents**:
   - Click "Fill with Test JD" button to populate job details (or enter real job info)
   - Enter company name, position, and optionally job ID and posting link
   - Paste the job description
   - Click "Generate Resume & Cover Letter"
4. **Download** - Click the download buttons to save your resume and cover letter as PDFs
5. **Navigate** - Use the sidebar navigation to switch between "Master Profile" and "Generate Resume"

---

## 📁 Project Structure

```
resume_vault/
├── backend/
│   ├── main.py              # FastAPI with /generate endpoint
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.vue                    # Router container
│       ├── router/
│       │   └── index.js               # Route config
│       ├── views/
│       │   ├── ProfileView.vue        # Master Profile page
│       │   └── GenerateView.vue       # Generate Resume page
│       └── components/
│           └── AppNav.vue             # Top navigation
└── README.md
```

---

## ⚙️ Technical Overview

### Backend (FastAPI + Python)
- **Framework**: FastAPI for high-performance async API
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: Clerk integration for secure user management
- **AI Integration**: Claude/OpenAI for intelligent resume tailoring
- **PDF Generation**: LaTeX → pdflatex → PDF (local compilation)
- **Key Services**:
  - `latex_generator.py` - Generates LaTeX from profile data
  - `latex_local_compiler.py` - Compiles LaTeX to PDF using pdflatex
  - `claude_provider.py` - AI-powered content tailoring
- **API Endpoints**:
  - `POST /resumes/generate-latex` - Generate LaTeX resume with AI
  - `GET /resumes/{id}/pdf` - Download resume as PDF
  - `POST /resumes/{id}/regenerate` - Regenerate with edits
  - `GET /resumes/list/all` - List all user resumes
- **CORS enabled** for local development

### Frontend (Vue 3 + Vite)
- **Framework**: Vue 3 with Composition API
- **Routing**: Vue Router for navigation between pages
- **State Management**: Provide/Inject for sharing master profile data
- **Responsive Design**: Mobile-first CSS with breakpoints
- **Components**:
  - `AppNav.vue` - Vertical sidebar navigation with mobile hamburger menu
  - `ProfileView.vue` - Master profile form with validation
  - `GenerateView.vue` - Job details and document generation
- **PDF Download**: Converts base64 to Blob for browser download

---

## 🎨 UI/UX Features

- **Vertical Sidebar Navigation** - Fixed sidebar on desktop, collapsible hamburger menu on mobile
- **Responsive Layout** - Adapts to all screen sizes (mobile, tablet, desktop)
- **Form Validation** - Real-time validation prevents incomplete submissions
- **Test Data Helpers** - One-click buttons to populate forms with sample data
- **Professional Typography** - Clean, readable fonts and spacing
- **Card-Based Design** - Organized sections with clear visual hierarchy
- **Full-Width Layout** - Efficient use of screen space
- **Active Navigation States** - Visual feedback showing current page

## 🎨 Current Implementation: LaTeX-Based Resume Generation

### Architecture Overview
We use a **LaTeX-first approach** for professional, ATS-friendly resume generation with full editing capabilities.

### Key Features
- ✨ **LaTeX-based generation** - Professional typography and formatting
- 🤖 **AI-powered tailoring** - Claude/OpenAI analyzes job descriptions
- 📝 **Content editing** - Modify resume content and regenerate
- 📚 **Version history** - Track all changes with version control
- 📄 **Local PDF compilation** - Fast, reliable using pdflatex
- 🚀 **Auto-scroll** - Automatically scrolls to generated content

### User Flow

1. **Create Master Profile** - Store all professional information once
2. **Generate Resume** - AI tailors content to job description
3. **Preview** - See LaTeX content with formatting
4. **Choose Action**:
   - **Edit Content** → Modify summary/experiences → Regenerate
   - **Download PDF** → LaTeX→PDF compilation → Browser download
5. **Version Control** - All edits create new versions

### Database Schema

**Collection: `resume_generations`**
```javascript
{
  "_id": ObjectId,
  "userId": "clerk_user_id",
  "jobApplicationId": "uuid",
  "jobInfo": {
    "companyName": str,
    "position": str,
    "jobId": str,
    "postingLink": str,
    "jobDescription": str
  },
  "versions": [
    {
      "versionNumber": 1,
      "createdAt": ISO datetime,
      "latexContent": str,
      "coverLetterContent": str,
      "tailoredData": {
        "tailored_summary": str,
        "tailored_experience": [...],
        "keyword_matches": [...],
        "recommendations": [...]
      },
      "atsScores": {"resume": int, "coverLetter": int},
      "isEdited": bool
    }
  ],
  "currentVersion": 1,
  "createdAt": ISO datetime,
  "updatedAt": ISO datetime
}
```

### Why LaTeX?
- ✅ **Professional output** - Industry-standard typography
- ✅ **ATS-friendly** - Clean, parseable structure
- ✅ **No external dependencies** - Local compilation
- ✅ **Fast** - 2-3 seconds per PDF
- ✅ **Reliable** - No URL length limits, no API quotas

## 🔮 Next Steps

See [STATUS.md](STATUS.md) and [TODO.md](TODO.md) for detailed roadmap.

### Immediate Priorities
- **Cover Letter Preview & Download** - PDF generation for cover letters
- **Cover Letter Editing** - Edit and regenerate cover letters
- **Enhanced Resume Editing** - Education, skills, certifications

### Future Enhancements
- **Multiple LaTeX Templates** - Choose from different professional designs
- **Version History UI** - Visual timeline with comparison
- **Template Customization** - User control over styling
- **Export Formats** - Support for DOCX and other formats

## 📝 License

This project is open source and available for personal and commercial use.

---

**Built with ❤️ for job seekers everywhere**
