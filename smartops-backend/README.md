# SmartOps Backend

Python FastAPI service for text summarization and task extraction/prioritization.

## Features

- **Text Summarization**: 5-sentence extractive summary with PII redaction (emails, phone numbers)
- **Task Extraction & Prioritization**: Extracts actionable items with owners, due dates, and priority scores

## Setup

### Prerequisites

- Python 3.8 or higher

### Installation

1. Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /api/health
```
Returns: `{"status": "ok"}`

### Summarize Text
```
POST /api/summarize
Content-Type: application/json

{
  "text": "Your text here..."
}
```
Returns: `{"summary": "5-sentence summary with PII redacted"}`

### Extract & Prioritize Tasks
```
POST /api/tasks/priority
Content-Type: application/json

{
  "text": "Your text with tasks here..."
}
```
Returns:
```json
{
  "tasks": [
    {
      "task": "Task description",
      "owner": "@username",
      "due_date": "2025-10-25",
      "priority_score": 85,
      "effort_estimate": "medium"
    }
  ]
}
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
