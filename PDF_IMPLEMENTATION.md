
# PDF Resume Implementation with LaTeX

## Overview
This implementation uses LaTeX.Online API to generate PDF resumes from LaTeX templates, with a frontend PDF preview component.

## Components

### Backend (`backend/`)

#### 1. `services/latex_online_compiler.py`
- Uses LaTeX.Online free API (`https://latexonline.cc/compile`)
- Uploads LaTeX source file via multipart form
- Returns compiled PDF as bytes

#### 2. `services/latex_generator.py`
- Reads LaTeX template (`template/template2.tex`)
- Fills template with profile and tailored content
- Handles LaTeX escaping for special characters
- Formats experiences, education, skills, certifications

#### 3. `template/template2.tex`
- Minimal LaTeX template with standard packages
- Custom environments: `onecolentry`, `highlights`
- No external dependencies (fontawesome, charter, etc.)

#### 4. `routers/resumes.py`
- `POST /resumes/generate-pdf` endpoint
- Uses LaTeXOnlineCompiler for PDF generation
- Returns PDF as base64 + metadata (ATS scores)

### Frontend (`frontend/`)

#### 1. `components/PdfPreview.vue`
- Accepts PDF base64 as prop
- Displays PDF using `<embed>` tag
- Download button functionality
- Loading states and fallbacks

#### 2. `views/GenerateView.vue`
- Preview mode toggle (HTML vs PDF)
- Calls `/resumes/generate-pdf` for PDF mode
- Shows PdfPreview component

## API Flow

```
Frontend (GenerateView)
    ↓ POST /resumes/generate-pdf
Backend (resumes.py)
    ├─ Fetch user profile from MongoDB
    ├─ AI tailor resume content
    ├─ Generate LaTeX source (latex_generator.py)
    ├─ Compile to PDF (latex_online_compiler.py)
    └─ Return base64 PDF
    ↓
Frontend (PdfPreview)
    ├─ Convert base64 to blob URL
    ├─ Display in embed tag
    └─ Download functionality
```

## Environment Variables
- `VITE_API_URL`: Backend API URL (e.g., `https://resume-vault.fly.dev`)

## Notes
- LaTeX.Online is a free API with rate limits
- PDF compilation may take 10-30 seconds
- LaTeX template uses minimal packages for compatibility

