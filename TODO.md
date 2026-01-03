# Resume Vault - Development TODO

**Last Updated**: January 2, 2026

---

## 🎯 Current Sprint - Cover Letter Features

### **Priority 1: Cover Letter Preview & Download** ⭐
**Goal**: Enable users to download cover letter as PDF

#### Backend Tasks
- [ ] Create LaTeX template for cover letter (`template/cover_letter.tex`)
  - Simple, professional layout
  - Reuse header styling from resume template
  - Support for multi-paragraph content
  - Proper date formatting

- [ ] Add cover letter PDF generation service
  - Create `services/cover_letter_generator.py`
  - Implement `generate_cover_letter_latex()` method
  - Use existing cover letter text from database
  - Handle LaTeX character escaping

- [ ] Create cover letter PDF endpoint
  - Add `GET /resumes/{id}/cover-letter/pdf`
  - Fetch cover letter content from database
  - Generate LaTeX from template
  - Compile to PDF and return for download
  - Add error handling for missing cover letter

#### Frontend Tasks
- [ ] Create `CoverLetterPreview.vue` component
  - Display formatted cover letter text
  - Add download button
  - Show ATS score
  - Match resume preview styling

- [ ] Update `GenerateView.vue`
  - Show both resume and cover letter previews
  - Add tabs or split view
  - Consistent download actions

- [ ] Update `ResumePreview.vue` (if needed)
  - Add "View Cover Letter" link/button
  - Navigate between resume and cover letter

**Estimated Time**: 4-6 hours

---

### **Priority 2: Cover Letter Editing** ⭐
**Goal**: Allow users to edit and regenerate cover letter

#### Backend Tasks
- [ ] Extend extract endpoint for cover letter
  - Update `GET /resumes/{id}/extract`
  - Return cover letter content separately
  - Include in response schema

- [ ] Update regenerate endpoint
  - Modify `POST /resumes/{id}/regenerate`
  - Accept cover letter edits in request body
  - Create new version with updated cover letter
  - Preserve cover letter version history

- [ ] Add cover letter regeneration logic
  - Store edited cover letter in new version
  - Update ATS score (optional)
  - Link to resume version

#### Frontend Tasks
- [ ] Create `CoverLetterEditForm.vue` component
  - Textarea for cover letter editing
  - Character count (aim for 250-400 words)
  - Save/Cancel buttons
  - Loading state during regeneration

- [ ] Add edit functionality to cover letter preview
  - Add "Edit" button in `CoverLetterPreview.vue`
  - Toggle between preview and edit modes
  - Show success message after save

- [ ] Update version history UI
  - Show which versions have edited cover letters
  - Allow switching between resume/cover letter in history

**Estimated Time**: 6-8 hours

---

## 🔄 Ongoing Maintenance

### Code Quality
- [ ] Add JSDoc comments to new Vue components
- [ ] Add Python docstrings to new services
- [ ] Update TypeScript types (if using TS)

### Testing
- [ ] Test cover letter PDF generation locally
- [ ] Test cover letter editing flow
- [ ] Test version history with cover letter edits
- [ ] Cross-browser testing (Chrome, Firefox, Safari)

### Documentation
- [x] Create STATUS.md with current implementation status ✅
- [ ] Update README.md with LaTeX architecture
- [ ] Document cover letter endpoints in API docs
- [ ] Add screenshots/GIFs to documentation

---

## 📋 Backlog - Future Enhancements

### Resume Editing Enhancements
- [ ] Add education section editing
- [ ] Add skills editing (add/remove/reorder)
- [ ] Add certifications editing
- [ ] Rich text editor with markdown support
- [ ] Drag-and-drop reordering of experiences

### Version History & Comparison
- [ ] Visual timeline of versions
- [ ] Side-by-side version comparison
- [ ] Restore previous version
- [ ] Add notes/tags to versions
- [ ] Track downloaded versions

### Template System
- [ ] Create template2.tex (modern design)
- [ ] Create template3.tex (traditional design)
- [ ] Template selection UI
- [ ] Switch template for existing resume
- [ ] Template preview gallery

### Advanced Features
- [ ] Real-time collaboration
- [ ] AI suggestions during editing
- [ ] Grammar and spell-check integration
- [ ] Export to DOCX format
- [ ] Multiple language support
- [ ] Custom LaTeX template upload
- [ ] Resume analytics dashboard

---

## 🐛 Known Issues

### Critical
- None currently

### Minor
- [ ] LaTeX compilation might fail on very long bullet points (>500 chars)
  - **Fix**: Add validation/warning in frontend
  - **Alternative**: Auto-wrap long text in LaTeX template

- [ ] Special characters in URLs might break LaTeX hyperlinks
  - **Fix**: Improve URL escaping in `latex_generator.py`

### Enhancement Requests
- [ ] Add "Copy to Clipboard" for LaTeX source
- [ ] Add keyboard shortcuts for common actions
- [ ] Improve mobile editing experience

---

## ✅ Recently Completed

### January 2, 2026
- [x] Migrated from HTML to LaTeX-based resume generation
- [x] Removed all HTML/WeasyPrint dependencies
- [x] Implemented local PDF compilation using pdflatex
- [x] Updated Dockerfile for Fly.io deployment with LaTeX
- [x] Fixed LaTeX character escaping (backslashes, ampersands, etc.)
- [x] Added auto-scroll to generated content
- [x] Cleaned up unused services and code
- [x] Updated Fly.io memory allocation to 512MB
- [x] Created comprehensive STATUS.md documentation

### December 2025
- [x] Implemented resume version history
- [x] Created resume editing flow
- [x] Added LaTeX content extraction
- [x] Integrated Clerk authentication
- [x] Set up MongoDB with Motor (async)
- [x] Created master profile management

---

## 📝 Development Notes

### LaTeX Template Guidelines
- Keep templates simple and maintainable
- Use consistent variable naming: `{{VARIABLE_NAME}}`
- Test with various content lengths
- Ensure mobile-friendly PDF output
- Follow ATS-friendly design principles

### Cover Letter Best Practices
- Target length: 250-400 words
- 3-4 paragraphs recommended
- Match tone to job description
- Highlight relevant keywords from resume
- Professional closing

### Version Control Strategy
- Create new version only when user saves edits
- Auto-save is not implemented (intentional)
- Each version is immutable once created
- `currentVersion` always points to latest

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Run local tests with Docker
- [ ] Verify all environment variables
- [ ] Check LaTeX installation in Docker image
- [ ] Test PDF generation in container
- [ ] Review Fly.io configuration

### Deployment Steps
```bash
cd backend
flyctl deploy
flyctl logs  # Monitor deployment
flyctl status  # Verify running
```

### Post-Deployment
- [ ] Test resume generation on production
- [ ] Test PDF download on production
- [ ] Test editing and regeneration
- [ ] Monitor memory usage
- [ ] Check LaTeX compilation logs
- [ ] Verify API response times

---

## 💡 Ideas for Future Consideration

- **AI-powered cover letter generation from resume**: Automatically generate cover letter based on resume content
- **Cover letter templates**: Multiple professional cover letter formats
- **Smart suggestions**: AI suggests improvements while editing
- **Batch generation**: Generate resumes for multiple jobs at once
- **Resume scoring**: Show detailed ATS compatibility breakdown
- **Company research integration**: Pull company info to customize cover letter
- **Interview prep**: Generate interview questions based on resume/job

---

**Priority Legend**:
- ⭐ High priority - Current sprint
- 🔵 Medium priority - Next sprint
- 🟢 Low priority - Backlog
- ❌ Blocked or deprecated

**Status Legend**:
- [ ] Not started
- [x] Completed
- [~] In progress
- [-] Blocked
