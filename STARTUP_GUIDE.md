# Resume Vault - Startup Guide

## 🚀 Quick Start

Your Resume Vault prototype is now **fully functional** and ready to use!

## ✅ What's Working

- ✅ **Backend API** (FastAPI + SQLite)
- ✅ **Frontend UI** (Vue 3 + TypeScript)
- ✅ **Master Profile Management**
- ✅ **Company Vault**
- ✅ **Mock Resume Tailor Function**
- ✅ **Database Persistence**

## 🏃 Running the Application

### Option 1: Start Both Servers (Recommended)

Open **two terminal windows**:

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```
✅ Backend runs at: **http://localhost:8000**

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
✅ Frontend runs at: **http://localhost:5173**

### Option 2: Background Processes (Currently Running)

**Both servers are already running!**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## 📱 Using the Application

### 1. Create Your Master Profile

1. Open http://localhost:5173
2. Click **"Master Profile"** in navigation
3. Fill in your information:
   - Personal details (name, email, location)
   - Work experience
   - Education
   - Skills
   - Projects, certifications, etc.
4. Click **"Save Profile"**

### 2. Add Companies

1. Click **"Company Vault"** in navigation
2. Click **"Show Form"**
3. Enter company details:
   - Company name
   - Job title
   - Job description (paste the full posting)
4. Click **"Add Company"**

### 3. Generate Tailored Resumes

1. In the Company Vault, find your company
2. Click **"Tailor Resume"**
3. The Mock Tailor will create a merged resume
4. You'll be redirected to view it
5. Click **"Copy Text"** to copy the resume
6. Click **"Print"** for a printer-friendly view

## 🔍 Features Demo

### Master Profile
- **Comprehensive form** for all career information
- **Auto-save** and reload functionality
- **Persistent storage** in SQLite

### Company Vault
- **Track unlimited companies**
- **Store job descriptions**
- **Application status tracking**
- **Notes and links** for each opportunity

### Resume Generation
- **Mock Tailor function** (basic text merge)
- **Keyword extraction** from job descriptions
- **Version tracking** (v1, v2, v3...)
- **Multiple formats** (currently markdown)

## 🗄️ Database

All data is stored in:
```
backend/resume_vault.db
```

**Tables:**
- `user_master_profile` - Your career history
- `companies` - Job opportunities
- `resumes` - Generated resume versions

## 📡 API Documentation

Visit **http://localhost:8000/docs** for interactive API documentation (Swagger UI)

### Key Endpoints

**Profiles:**
- `GET /api/profiles` - List all profiles
- `POST /api/profiles` - Create profile
- `PUT /api/profiles/{id}` - Update profile

**Companies:**
- `GET /api/companies` - List all companies
- `POST /api/companies` - Create company
- `DELETE /api/companies/{id}` - Delete company

**Resumes:**
- `POST /api/resumes/tailor` - Generate tailored resume
- `GET /api/resumes/{id}` - Get resume
- `GET /api/resumes/company/{company_id}` - Get all resumes for company

## 🎨 UI Features

### Navigation
- Clean, modern interface
- Responsive design (works on mobile)
- Smooth transitions

### Forms
- **Validation** on required fields
- **Auto-focus** on form elements
- **Clear feedback** with alerts

### Alerts
- Success (green)
- Error (red)
- Info (blue)

## 🧪 Testing the Mock Tailor

1. Create a profile with sample data:
   ```
   Name: John Doe
   Email: john@example.com
   Work Experience: Software Engineer at TechCorp
   Skills: Python, JavaScript, React
   ```

2. Add a company:
   ```
   Company: Amazing Company
   Job Title: Senior Software Engineer
   Job Description: We're looking for a senior engineer...
   ```

3. Click "Tailor Resume"

4. The mock tailor will:
   - Merge your profile with job info
   - Extract keywords from the description
   - Create a structured markdown resume
   - Save it to the database

## 🔧 Troubleshooting

### Backend won't start
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### Database issues
```bash
cd backend
rm resume_vault.db
python main.py  # Will recreate tables
```

### CORS errors
- Make sure backend is running on port 8000
- Make sure frontend is running on port 5173
- Check backend/main.py CORS settings

## 📊 Data Flow

```
User Input → Frontend (Vue) → API Call (Axios) → Backend (FastAPI) → Database (SQLite)
                                     ↓
User Views ← Frontend ← API Response ← Backend ← Database
```

## 🎯 Next Steps (Future Enhancements)

Current prototype uses **mock data** and a **basic text merge** function.

Future enhancements can include:
- ✨ AI integration (OpenAI, Anthropic, Google AI)
- 📄 PDF export
- 🎨 Resume templates
- 🔐 User authentication
- ☁️ Cloud database (PostgreSQL)
- 📧 Email sending
- 📈 ATS optimization scoring
- 💼 Cover letter generation

## 🛑 Stopping the Servers

### If running in foreground:
Press `Ctrl+C` in each terminal

### If running in background:
```bash
# Find process IDs
ps aux | grep "python main.py"
ps aux | grep "vite"

# Kill them
kill <PID>
```

Or use the task IDs:
- Backend: `bd3b2f5`
- Frontend: `bf767c2`

## 📝 Notes

- **Database**: All data persists between sessions
- **Hot reload**: Both servers auto-reload on code changes
- **Ports**: Backend=8000, Frontend=5173
- **Environment**: Development mode (not production-ready)

---

## 🎉 You're Ready!

Your Resume Vault prototype is fully functional. Start by creating your master profile and adding companies!

**Access the app:** http://localhost:5173
**API docs:** http://localhost:8000/docs

Enjoy building your resume vault!
