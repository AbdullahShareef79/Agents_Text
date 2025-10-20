from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.summarizer import summarize_text
from app.services.task_extractor import extract_and_prioritize_tasks

app = FastAPI(title="SmartOps API", version="1.0.0")

# CORS configuration for local frontend
# This must be added before any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["*"],
)


class TextInput(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str


class TaskResponse(BaseModel):
    tasks: list


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/api/summarize", response_model=SummaryResponse)
async def summarize(input_data: TextInput):
    """
    Summarize text into 5 sentences with PII redaction.
    
    - Redacts emails and phone numbers
    - Returns extractive summary (top 5 sentences)
    """
    summary = summarize_text(input_data.text)
    return {"summary": summary}


@app.post("/api/tasks/priority", response_model=TaskResponse)
async def prioritize_tasks(input_data: TextInput):
    """
    Extract and prioritize actionable tasks from text.
    
    - Identifies action verbs (do, create, review, etc.)
    - Extracts owners (@username)
    - Parses due dates (YYYY-MM-DD, tomorrow, EOD)
    - Assigns priority scores
    - Estimates effort (low, medium, high)
    """
    tasks = extract_and_prioritize_tasks(input_data.text)
    return {"tasks": tasks}
