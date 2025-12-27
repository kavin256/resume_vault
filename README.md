# Resume Vault - UI Spike

**Throwaway prototype for flow validation only.**

---

## 🎯 What This Does

Two-page application with clean UI:

**Page 1: Master Profile** (`/profile`)
- Fill out your career information once
- Personal info, experience, skills, education

**Page 2: Generate Resume** (`/generate`)
- Paste job description
- Click Generate
- Download Resume + Cover Letter (PDFs)

**No AI. No database. No persistence. Dummy content only.**

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

## 🧪 Test It

1. Open **http://localhost:5176/profile** in browser
2. Fill in all Master Profile fields (required)
3. Click "Continue to Generate Resume →"
4. Paste any text as job description
5. Click **Generate Resume & Cover Letter**
6. Download both PDFs
7. Verify files contain dummy content
8. Use top navigation to switch between pages

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

## ⚙️ How It Works

### Backend
- `POST /generate` - Takes master profile + job description
- Generates PDFs in memory (ReportLab)
- Returns base64-encoded files in JSON

### Frontend
- Two-page Vue app with routing
- Master Profile page (`/profile`)
- Generate Resume page (`/generate`)
- Shared state via `provide/inject`
- Converts base64 to blob for download

---

## 🗑️ To Remove This Spike

```bash
cd ..
rm -rf resume_vault
```

---

## ✅ Validation Complete

- [x] Form captures data
- [x] Generate button works
- [x] PDFs download correctly
- [x] No database needed
- [x] No file storage

**Flow validated. Ready for real implementation.**
