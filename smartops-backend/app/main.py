from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

from app.orchestrator import Orchestrator
from app.models import RunReport

app = FastAPI(title="SmartOps API - Multi-Agent", version="2.0.0")

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

# Initialize orchestrator
orchestrator = Orchestrator()

# Store latest run report (in-memory for simplicity)
latest_run_report: Dict[str, Any] = {}


class TextInput(BaseModel):
    text: str
    num_sentences: int = 5


class ProcessResponse(BaseModel):
    """Unified response for multi-agent processing"""
    summary: str | None
    tasks: list
    run_id: str
    quality_score: float
    total_duration_ms: float
    retry_count: int


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "2.0.0-multi-agent"}


@app.post("/api/process", response_model=ProcessResponse)
async def process_text(input_data: TextInput):
    """
    Process text through multi-agent pipeline:
    - SummarizeAgent (parallel)
    - ExtractAgent (parallel)
    - EvaluateAgent (feedback loop)
    
    Returns unified response with run metadata.
    """
    global latest_run_report
    
    # Run orchestrator
    run_report: RunReport = await orchestrator.process_text(
        text=input_data.text,
        num_sentences=input_data.num_sentences
    )
    
    # Store report for timeline endpoint
    latest_run_report = run_report.model_dump()
    
    # Return simplified response
    return ProcessResponse(
        summary=run_report.summary,
        tasks=[task.model_dump() for task in run_report.tasks],
        run_id=run_report.run_id,
        quality_score=run_report.quality_score,
        total_duration_ms=run_report.total_duration_ms,
        retry_count=run_report.retry_count
    )


@app.get("/api/run-report")
async def get_run_report():
    """
    Get the latest run report with full agent timeline.
    Used by frontend to display agent execution details.
    """
    if not latest_run_report:
        return {"error": "No run report available yet"}
    
    return latest_run_report


# Legacy endpoints for backward compatibility
@app.post("/api/summarize")
async def summarize_legacy(input_data: TextInput):
    """Legacy endpoint - redirects to new process endpoint"""
    result = await process_text(input_data)
    return {"summary": result.summary}


@app.post("/api/tasks/priority")
async def tasks_legacy(input_data: TextInput):
    """Legacy endpoint - redirects to new process endpoint"""
    result = await process_text(input_data)
    return {"tasks": result.tasks}
