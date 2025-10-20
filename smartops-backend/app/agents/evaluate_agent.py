"""
EvaluateAgent: Evaluates results and provides feedback for retry logic.
"""
from app.agents import BaseAgent
from app.models import EvaluateInput, EvaluateOutput


class EvaluateAgent(BaseAgent[EvaluateInput, EvaluateOutput]):
    """
    Agent that evaluates the quality of summarization and extraction results.
    Provides feedback and determines if re-run is needed.
    """
    
    # Quality thresholds
    MIN_SUMMARY_LENGTH = 50  # characters
    MIN_TASK_COUNT = 0  # Allow 0 tasks (empty is valid)
    MAX_PRIORITY_SCORE = 100
    MIN_PRIORITY_SCORE = 0
    
    def __init__(self):
        super().__init__(name="EvaluateAgent")
    
    def process(self, input_data: EvaluateInput) -> EvaluateOutput:
        """
        Evaluate the quality of agent outputs.
        """
        issues = []
        feedback = {}
        quality_score = 1.0  # Start with perfect score
        
        original_text_len = len(input_data.original_text)
        
        # Evaluate summarization
        if input_data.summary_output:
            summary_quality, summary_issues, summary_feedback = self._evaluate_summary(
                input_data.summary_output,
                original_text_len
            )
            quality_score *= summary_quality
            issues.extend(summary_issues)
            feedback.update(summary_feedback)
        
        # Evaluate extraction
        if input_data.extract_output:
            extract_quality, extract_issues, extract_feedback = self._evaluate_extraction(
                input_data.extract_output,
                original_text_len
            )
            quality_score *= extract_quality
            issues.extend(extract_issues)
            feedback.update(extract_feedback)
        
        # Determine if retry is needed
        # For simplicity, we don't retry in v1 (could add threshold logic later)
        needs_retry = quality_score < 0.3  # Only retry if severely bad
        
        return EvaluateOutput(
            quality_score=quality_score,
            needs_retry=needs_retry,
            feedback=feedback,
            issues=issues
        )
    
    def _evaluate_summary(
        self, 
        summary_output, 
        original_len: int
    ) -> tuple[float, list[str], dict[str, str]]:
        """
        Evaluate summary quality.
        Returns (quality_score, issues, feedback)
        """
        quality = 1.0
        issues = []
        feedback = {}
        
        summary_len = len(summary_output.summary)
        
        # Check minimum length
        if summary_len < self.MIN_SUMMARY_LENGTH:
            quality *= 0.7
            issues.append("Summary is too short")
            feedback["SummarizeAgent"] = "Consider including more context"
        
        # Check if summary is too long (shouldn't exceed 80% of original)
        if summary_len > original_len * 0.8:
            quality *= 0.8
            issues.append("Summary is too long relative to original")
            feedback["SummarizeAgent"] = "Summary should be more concise"
        
        # Check sentence count
        if summary_output.sentence_count < 3:
            quality *= 0.9
            issues.append("Summary has very few sentences")
        
        # Positive feedback for PII redaction
        if summary_output.redacted_pii_count > 0:
            feedback["SummarizeAgent"] = f"Good: Redacted {summary_output.redacted_pii_count} PII items"
        
        return quality, issues, feedback
    
    def _evaluate_extraction(
        self,
        extract_output,
        original_len: int
    ) -> tuple[float, list[str], dict[str, str]]:
        """
        Evaluate extraction quality.
        Returns (quality_score, issues, feedback)
        """
        quality = 1.0
        issues = []
        feedback = {}
        
        task_count = extract_output.task_count
        
        # Validate tasks
        if task_count > 0:
            for idx, task in enumerate(extract_output.tasks):
                # Check priority score range
                if not (self.MIN_PRIORITY_SCORE <= task.priority_score <= self.MAX_PRIORITY_SCORE):
                    quality *= 0.9
                    issues.append(f"Task {idx+1} has invalid priority score: {task.priority_score}")
                
                # Check effort estimate
                if task.effort_estimate not in ['low', 'medium', 'high']:
                    quality *= 0.9
                    issues.append(f"Task {idx+1} has invalid effort estimate: {task.effort_estimate}")
                
                # Check task description length
                if len(task.task.strip()) < 10:
                    quality *= 0.95
                    issues.append(f"Task {idx+1} has very short description")
            
            # Positive feedback
            owners_count = sum(1 for t in extract_output.tasks if t.owner)
            dates_count = sum(1 for t in extract_output.tasks if t.due_date)
            
            if owners_count > 0:
                feedback["ExtractAgent"] = f"Good: Found {owners_count} tasks with owners"
            if dates_count > 0:
                feedback["ExtractAgent"] = f"Good: Found {dates_count} tasks with due dates"
        
        return quality, issues, feedback
