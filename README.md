# SmartOps Application

A simple local application for text summarization and task prioritization.

## What's Inside

This folder contains two projects:

- **smartops-backend**: Python FastAPI service
- **smartops-frontend**: Vue 3 + Vite web application

## Quick Start

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for complete setup instructions.

### TL;DR

**Terminal 1 - Backend:**
```powershell
cd smartops-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd smartops-frontend
npm install
npm run dev
```

Then open `http://localhost:5173` in your browser!

## Features

✅ **Summarization**: Get 5-sentence extractive summaries with PII redaction  
✅ **Task Extraction**: Find and prioritize actionable items  
✅ **Pure Python**: No LLMs, no external APIs, no cloud  
✅ **100% Local**: Runs entirely on your laptop  
✅ **Free**: No paid dependencies  

## Files

- `SETUP_GUIDE.md` - Complete setup and troubleshooting guide
- `sample_test_text.txt` - Sample text for testing
- `smartops-backend/` - Backend service
- `smartops-frontend/` - Web interface

## Technology Stack

**Backend:**
- Python 3.8+
- FastAPI
- Uvicorn

**Frontend:**
- Vue 3
- Vite
- Native JavaScript (no TypeScript complexity)

---

Built for local development only. No deployment, no CI/CD, no cloud services.
