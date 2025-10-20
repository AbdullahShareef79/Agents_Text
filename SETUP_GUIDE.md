# SmartOps - Complete Setup Guide

This guide will help you set up and run both the backend and frontend locally.

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and npm (for frontend)

## Quick Start

### 1. Backend Setup (smartops-backend)

Open a terminal in the `smartops-backend` folder:

```powershell
cd "C:\Users\shareefa7450\OneDrive - Revantage Europe\Documents\Research\BACK UP\SDG\Agents_Text\smartops-backend"
```

Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the backend server:

```powershell
uvicorn app.main:app --reload
```

✅ Backend is now running at `http://localhost:8000`
- API docs: http://localhost:8000/docs

### 2. Frontend Setup (smartops-frontend)

Open a **new** terminal in the `smartops-frontend` folder:

```powershell
cd "C:\Users\shareefa7450\OneDrive - Revantage Europe\Documents\Research\BACK UP\SDG\Agents_Text\smartops-frontend"
```

Install dependencies:

```powershell
npm install
```

Run the frontend dev server:

```powershell
npm run dev
```

✅ Frontend is now running at `http://localhost:5173`

### 3. Test the Application

Open your browser and navigate to `http://localhost:5173`

**Sample Test Text:**

```
We need to urgently fix the login bug today @john. 
Create a new API endpoint for user management by 2025-10-25 @sarah.
Review the pull request from the frontend team tomorrow @mike.
Send the weekly report to stakeholders via email EOD.
Implement the new payment integration system @david.
Update documentation for the new features.
Schedule a meeting with the design team to discuss UI improvements.
Analyze user feedback from last sprint and prepare insights @emma.
```

Try both features:
1. Click **Summarize** - You'll get a 5-sentence summary
2. Click **Extract & Prioritize Tasks** - You'll see a prioritized task table

## Project Structure

```
Agents_Text/
├── smartops-backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── services/
│   │   │   ├── summarizer.py  # Text summarization logic
│   │   │   └── task_extractor.py  # Task extraction logic
│   │   └── main.py            # FastAPI application
│   ├── requirements.txt
│   └── README.md
│
└── smartops-frontend/         # Vue 3 + Vite frontend
    ├── src/
    │   ├── components/
    │   │   ├── SummaryList.vue
    │   │   └── TaskTable.vue
    │   ├── services/
    │   │   └── api.ts         # API client
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    └── README.md
```

## Features

### Backend (Python FastAPI)
- ✅ GET `/api/health` - Health check
- ✅ POST `/api/summarize` - 5-sentence extractive summary with PII redaction
- ✅ POST `/api/tasks/priority` - Extract and prioritize tasks

### Frontend (Vue 3)
- ✅ Simple text input area
- ✅ Summarization display
- ✅ Prioritized task table with:
  - Priority scores (color-coded)
  - Owners (@mentions)
  - Due dates (formatted)
  - Effort estimates (low/medium/high)

## Troubleshooting

### Backend Issues

**Port already in use:**
```powershell
# Change the port
uvicorn app.main:app --reload --port 8001
# Then update frontend src/services/api.ts API_BASE_URL
```

**Module not found:**
```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\Activate.ps1
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Port already in use:**
Edit `vite.config.js` and change the port number

**Dependencies not installed:**
```powershell
npm install
```

**CORS errors:**
Make sure backend is running and CORS is configured for `http://localhost:5173`

## Stopping the Servers

- Backend: Press `Ctrl+C` in the backend terminal
- Frontend: Press `Ctrl+C` in the frontend terminal

## Next Steps

- Both projects are ready for local development
- No deployment configured (local only)
- No external APIs or paid services
- All logic is pure Python (no LLMs)

Enjoy using SmartOps! 🚀
