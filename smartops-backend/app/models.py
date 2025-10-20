"""
Agent I/O contracts using Pydantic models.
These models define the input and output structures for each agent.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# Agent Input/Output Models
# ============================================================================

class SummarizeInput(BaseModel):
    """Input for SummarizeAgent"""
    text: str = Field(..., description="Raw text to summarize")
    num_sentences: int = Field(default=5, description="Number of sentences in summary")


class SummarizeOutput(BaseModel):
    """Output from SummarizeAgent"""
    summary: str = Field(..., description="Generated summary with PII redacted")
    sentence_count: int = Field(..., description="Actual number of sentences")
    redacted_pii_count: int = Field(default=0, description="Number of PII items redacted")


class ExtractInput(BaseModel):
    """Input for ExtractAgent"""
    text: str = Field(..., description="Raw text to extract tasks from")


class TaskItem(BaseModel):
    """A single extracted task"""
    task: str = Field(..., description="Task description")
    owner: Optional[str] = Field(None, description="Task owner (@username)")
    due_date: Optional[str] = Field(None, description="Due date (ISO format or relative)")
    priority_score: int = Field(..., ge=0, le=100, description="Priority score 0-100")
    effort_estimate: str = Field(..., description="Effort level: low, medium, or high")


class ExtractOutput(BaseModel):
    """Output from ExtractAgent"""
    tasks: List[TaskItem] = Field(default_factory=list, description="Extracted tasks")
    task_count: int = Field(default=0, description="Total number of tasks found")


class EvaluateInput(BaseModel):
    """Input for EvaluateAgent"""
    original_text: str = Field(..., description="Original input text")
    summary_output: Optional[SummarizeOutput] = Field(None, description="Summary result")
    extract_output: Optional[ExtractOutput] = Field(None, description="Extraction result")


class EvaluateOutput(BaseModel):
    """Output from EvaluateAgent"""
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Overall quality score")
    needs_retry: bool = Field(default=False, description="Whether agents should re-run")
    feedback: Dict[str, str] = Field(default_factory=dict, description="Feedback for agents")
    issues: List[str] = Field(default_factory=list, description="List of identified issues")


# ============================================================================
# Orchestrator Models
# ============================================================================

class AgentRunMetrics(BaseModel):
    """Metrics for a single agent execution"""
    agent_name: str
    status: str = Field(..., description="success, failed, skipped, retrying")
    start_time: float
    end_time: float
    duration_ms: float
    attempt: int = Field(default=1, description="Attempt number (for retries)")
    error: Optional[str] = None


class RunReport(BaseModel):
    """Complete run report for orchestrator execution"""
    run_id: str = Field(..., description="Unique run identifier")
    timestamp: float = Field(..., description="Unix timestamp of run start")
    input_text_length: int = Field(..., description="Length of input text")
    
    # Agent execution timeline
    agent_timeline: List[AgentRunMetrics] = Field(default_factory=list)
    
    # Final outputs
    summary: Optional[str] = None
    tasks: List[TaskItem] = Field(default_factory=list)
    
    # Evaluation results
    quality_score: float = Field(default=0.0)
    feedback: Dict[str, str] = Field(default_factory=dict)
    
    # Aggregate metrics
    total_duration_ms: float = Field(default=0.0)
    retry_count: int = Field(default=0)
    success: bool = Field(default=True)
