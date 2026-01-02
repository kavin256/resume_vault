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
- **Framework**: FastAPI for high-performance API
- **PDF Generation**: ReportLab for creating professional PDF documents
- **API Endpoint**: `POST /generate`
  - Accepts master profile data and job description
  - Generates resume and cover letter PDFs in memory
  - Returns base64-encoded files in JSON response
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

## 🎨 Recent Implementation: HTML Resume Generation with Preview & Editing

### What's New
We've transformed the resume generation from PDF-only to an **HTML-first approach** that enables live preview and iterative editing while maintaining AI control over styling.

### Implementation Checklist

#### ✅ Backend Implementation
- [x] **Add dependencies to requirements.txt** (weasyprint, beautifulsoup4, lxml)
- [x] **Add generate_html_resume() method to ClaudeProvider** - AI generates complete HTML with inline CSS
- [x] **Add regenerate_html_with_edits() method to ClaudeProvider** - Preserves styling while updating content
- [x] **Create html_converter.py service** - HTML→PDF conversion using WeasyPrint
- [x] **Create content_extractor.py service** - Extract editable content from HTML using BeautifulSoup
- [x] **Create resumes.py router** - Complete REST API with 6 endpoints
- [x] **Update main.py** - Include resumes router and DB indexes for resume_generations collection

#### ✅ Frontend Implementation
- [x] **Create ResumePreview.vue component** - Live HTML preview with download/edit buttons
- [x] **Create ResumeEditForm.vue component** - Form to edit resume content with structured sections
- [x] **Update GenerateView.vue** - Integrate HTML generation flow with preview and edit capabilities
- [x] **Update api.js** - Add new resume API methods (implied by component implementation)

#### 🧪 Testing Checklist
- [ ] **Test end-to-end flow** (generate → preview → download)
- [ ] **Test edit flow** (edit → regenerate → preview)

### New API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/resumes/generate-html` | POST | Generate HTML resume and store in DB |
| `/resumes/{id}` | GET | Get resume by ID (with version support) |
| `/resumes/{id}/extract` | GET | Extract editable content from HTML |
| `/resumes/{id}/regenerate` | POST | Regenerate HTML with edited content |
| `/resumes/{id}/pdf` | GET | Download resume as PDF |
| `/resumes/list/all` | GET | List all user's resumes |

### New User Flow

1. **Generate** - User fills job details → Gets HTML preview
2. **Preview** - User sees professional HTML resume in browser
3. **Choose Action**:
   - **Edit Content** → Form with all sections → Regenerate → Preview updated
   - **Download PDF** → HTML→PDF conversion → Browser download
4. **Multiple Iterations** - Edit and regenerate as many times as needed

### Database Schema

**New Collection: `resume_generations`**
```javascript
{
  "_id": ObjectId,
  "userId": "clerk_user_id",
  "jobApplicationId": "uuid",
  "jobInfo": {
    "companyName": str,
    "position": str,
    "jobDescription": str
  },
  "versions": [
    {
      "versionNumber": 1,
      "createdAt": ISO datetime,
      "htmlContent": str,
      "coverLetterHtml": str,
      "tailoredData": {...},
      "atsScores": {"resume": int, "coverLetter": int},
      "isEdited": bool
    }
  ],
  "currentVersion": 1
}
```

### Key Features
- ✨ **HTML-first generation** - AI creates complete styled HTML resumes
- 👁️ **Live preview** - See resume before downloading
- ✏️ **Content editing** - Modify text while preserving AI-generated styling
- 📚 **Version history** - Track multiple versions of each resume
- 🎨 **Style preservation** - AI maintains exact formatting when regenerating
- 📄 **On-demand PDF** - Convert to PDF only when needed

## 🔮 Future Enhancements

- **Cover Letter HTML Preview** - Extend preview functionality to cover letters
- **Version History UI** - Visual timeline of resume versions with comparison
- **Multiple Resume Templates** - Choose from different professional HTML designs
- **Resume Comparison View** - Side-by-side comparison of versions
- **Custom Styling Options** - User control over colors and fonts
- **Export Formats** - Support for DOCX and other formats

## 📝 License

This project is open source and available for personal and commercial use.

---

**Built with ❤️ for job seekers everywhere**
