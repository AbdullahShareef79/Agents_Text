"""
Orchestrator: Coordinates multi-agent pipeline with parallel execution and feedback loop.
"""
import time
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from app.models import (
    SummarizeInput, ExtractInput, EvaluateInput,
    SummarizeOutput, ExtractOutput, EvaluateOutput,
    RunReport, AgentRunMetrics, TaskItem
)
from app.agents.summarize_agent import SummarizeAgent
from app.agents.extract_agent import ExtractAgent
from app.agents.evaluate_agent import EvaluateAgent


class Orchestrator:
    """
    Orchestrates the multi-agent pipeline:
    1. Run SummarizeAgent and ExtractAgent in parallel
    2. Run EvaluateAgent on results
    3. Optional: Retry loop if quality is low
    4. Generate comprehensive run report
    """
    
    MAX_RETRIES = 1  # Maximum retry attempts
    
    def __init__(self):
        self.summarize_agent = SummarizeAgent()
        self.extract_agent = ExtractAgent()
        self.evaluate_agent = EvaluateAgent()
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    async def process_text(
        self,
        text: str,
        num_sentences: int = 5
    ) -> RunReport:
        """
        Process text through the multi-agent pipeline.
        Returns a complete run report with timeline and metrics.
        """
        run_id = str(uuid.uuid4())
        start_timestamp = time.time()
        
        # Initialize report
        report = RunReport(
            run_id=run_id,
            timestamp=start_timestamp,
            input_text_length=len(text)
        )
        
        attempt = 1
        retry_needed = False
        
        while attempt <= self.MAX_RETRIES + 1:
            # Step 1: Run summarize and extract in parallel
            summary_output, extract_output, parallel_metrics = await self._run_parallel_agents(
                text, num_sentences, attempt
            )
            
            # Add parallel metrics to timeline
            report.agent_timeline.extend(parallel_metrics)
            
            # Step 2: Evaluate results
            evaluate_output, evaluate_metrics = await self._run_evaluate_agent(
                text, summary_output, extract_output, attempt
            )
            
            # Add evaluate metrics to timeline
            report.agent_timeline.append(evaluate_metrics)
            
            # Check if retry is needed
            if evaluate_output.needs_retry and attempt <= self.MAX_RETRIES:
                retry_needed = True
                report.retry_count += 1
                attempt += 1
                continue
            else:
                # Success or max retries reached
                report.summary = summary_output.summary if summary_output else None
                report.tasks = extract_output.tasks if extract_output else []
                report.quality_score = evaluate_output.quality_score
                report.feedback = evaluate_output.feedback
                break
        
        # Calculate total duration
        report.total_duration_ms = (time.time() - start_timestamp) * 1000
        report.success = not retry_needed or report.quality_score >= 0.3
        
        return report
    
    async def _run_parallel_agents(
        self,
        text: str,
        num_sentences: int,
        attempt: int
    ) -> tuple[Optional[SummarizeOutput], Optional[ExtractOutput], list[AgentRunMetrics]]:
        """
        Run SummarizeAgent and ExtractAgent in parallel using ThreadPoolExecutor.
        Returns (summary_output, extract_output, metrics_list)
        """
        loop = asyncio.get_event_loop()
        
        # Prepare inputs
        summarize_input = SummarizeInput(text=text, num_sentences=num_sentences)
        extract_input = ExtractInput(text=text)
        
        # Run agents in parallel
        start_time = time.time()
        
        try:
            # Execute both agents concurrently
            summary_future = loop.run_in_executor(
                self.executor,
                self._run_summarize_with_metrics,
                summarize_input,
                attempt
            )
            
            extract_future = loop.run_in_executor(
                self.executor,
                self._run_extract_with_metrics,
                extract_input,
                attempt
            )
            
            # Wait for both to complete
            summary_result, extract_result = await asyncio.gather(
                summary_future,
                extract_future,
                return_exceptions=True
            )
            
            # Unpack results
            if isinstance(summary_result, Exception):
                summary_output = None
                summary_metrics = self._create_error_metrics(
                    "SummarizeAgent", start_time, attempt, str(summary_result)
                )
            else:
                summary_output, summary_metrics = summary_result
            
            if isinstance(extract_result, Exception):
                extract_output = None
                extract_metrics = self._create_error_metrics(
                    "ExtractAgent", start_time, attempt, str(extract_result)
                )
            else:
                extract_output, extract_metrics = extract_result
            
            return summary_output, extract_output, [summary_metrics, extract_metrics]
        
        except Exception as e:
            # Fallback error handling
            error_metrics = self._create_error_metrics(
                "ParallelExecution", start_time, attempt, str(e)
            )
            return None, None, [error_metrics]
    
    def _run_summarize_with_metrics(
        self,
        input_data: SummarizeInput,
        attempt: int
    ) -> tuple[SummarizeOutput, AgentRunMetrics]:
        """Run SummarizeAgent and capture metrics."""
        start_time = time.time()
        
        try:
            output, duration_ms = self.summarize_agent.run(input_data)
            
            metrics = AgentRunMetrics(
                agent_name="SummarizeAgent",
                status="success",
                start_time=start_time,
                end_time=time.time(),
                duration_ms=duration_ms,
                attempt=attempt
            )
            
            return output, metrics
        
        except Exception as e:
            metrics = self._create_error_metrics(
                "SummarizeAgent", start_time, attempt, str(e)
            )
            raise
    
    def _run_extract_with_metrics(
        self,
        input_data: ExtractInput,
        attempt: int
    ) -> tuple[ExtractOutput, AgentRunMetrics]:
        """Run ExtractAgent and capture metrics."""
        start_time = time.time()
        
        try:
            output, duration_ms = self.extract_agent.run(input_data)
            
            metrics = AgentRunMetrics(
                agent_name="ExtractAgent",
                status="success",
                start_time=start_time,
                end_time=time.time(),
                duration_ms=duration_ms,
                attempt=attempt
            )
            
            return output, metrics
        
        except Exception as e:
            metrics = self._create_error_metrics(
                "ExtractAgent", start_time, attempt, str(e)
            )
            raise
    
    async def _run_evaluate_agent(
        self,
        text: str,
        summary_output: Optional[SummarizeOutput],
        extract_output: Optional[ExtractOutput],
        attempt: int
    ) -> tuple[EvaluateOutput, AgentRunMetrics]:
        """Run EvaluateAgent sequentially after parallel agents."""
        start_time = time.time()
        
        evaluate_input = EvaluateInput(
            original_text=text,
            summary_output=summary_output,
            extract_output=extract_output
        )
        
        try:
            output, duration_ms = self.evaluate_agent.run(evaluate_input)
            
            metrics = AgentRunMetrics(
                agent_name="EvaluateAgent",
                status="success",
                start_time=start_time,
                end_time=time.time(),
                duration_ms=duration_ms,
                attempt=attempt
            )
            
            return output, metrics
        
        except Exception as e:
            metrics = self._create_error_metrics(
                "EvaluateAgent", start_time, attempt, str(e)
            )
            # Return default output on error
            default_output = EvaluateOutput(
                quality_score=0.0,
                needs_retry=False,
                feedback={},
                issues=[f"EvaluateAgent error: {str(e)}"]
            )
            return default_output, metrics
    
    def _create_error_metrics(
        self,
        agent_name: str,
        start_time: float,
        attempt: int,
        error_msg: str
    ) -> AgentRunMetrics:
        """Create error metrics for failed agent execution."""
        return AgentRunMetrics(
            agent_name=agent_name,
            status="failed",
            start_time=start_time,
            end_time=time.time(),
            duration_ms=(time.time() - start_time) * 1000,
            attempt=attempt,
            error=error_msg
        )
