"""
ExtractAgent: Extracts and prioritizes actionable tasks.
"""
import re
from datetime import datetime, timedelta
from typing import Optional
from app.agents import BaseAgent
from app.models import ExtractInput, ExtractOutput, TaskItem


class ExtractAgent(BaseAgent[ExtractInput, ExtractOutput]):
    """
    Agent that extracts actionable tasks with owners, due dates, and priorities.
    """
    
    ACTION_VERBS = [
        'do', 'create', 'review', 'update', 'fix', 'implement', 'test',
        'deploy', 'write', 'send', 'schedule', 'prepare', 'complete',
        'finish', 'submit', 'call', 'email', 'contact', 'meet', 'discuss',
        'analyze', 'research', 'investigate', 'design', 'build', 'setup',
        'configure', 'install', 'develop', 'refactor', 'optimize'
    ]
    
    def __init__(self):
        super().__init__(name="ExtractAgent")
    
    def process(self, input_data: ExtractInput) -> ExtractOutput:
        """
        Extract tasks from input text.
        """
        text = input_data.text
        lines = text.strip().split('\n')
        
        tasks = []
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            if not self._is_actionable(line):
                continue
            
            # Extract task components
            owner = self._extract_owner(line)
            due_date = self._extract_due_date(line)
            priority_score = self._calculate_priority(line, bool(owner), bool(due_date))
            effort = self._estimate_effort(line)
            
            # Clean task text
            task_text = self._clean_task_text(line)
            
            tasks.append(TaskItem(
                task=task_text,
                owner=owner,
                due_date=due_date,
                priority_score=priority_score,
                effort_estimate=effort
            ))
        
        # Sort by priority descending
        tasks.sort(key=lambda x: x.priority_score, reverse=True)
        
        return ExtractOutput(
            tasks=tasks,
            task_count=len(tasks)
        )
    
    def _is_actionable(self, line: str) -> bool:
        """Check if line contains actionable content."""
        line_lower = line.lower()
        for verb in self.ACTION_VERBS:
            if re.search(rf'\b{verb}\b', line_lower):
                return True
        return False
    
    def _extract_owner(self, line: str) -> Optional[str]:
        """Extract owner from @username."""
        match = re.search(r'@(\w+)', line)
        return f"@{match.group(1)}" if match else None
    
    def _extract_due_date(self, line: str) -> Optional[str]:
        """Extract due date in various formats."""
        line_lower = line.lower()
        
        # ISO date
        date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', line)
        if date_match:
            return date_match.group(1)
        
        # Relative dates
        if 'tomorrow' in line_lower:
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.strftime('%Y-%m-%d')
        
        if 'eod' in line_lower or 'end of day' in line_lower or 'today' in line_lower:
            return datetime.now().strftime('%Y-%m-%d')
        
        return None
    
    def _calculate_priority(self, line: str, has_owner: bool, has_due_date: bool) -> int:
        """Calculate priority score 0-100."""
        score = 50  # Base
        line_lower = line.lower()
        
        # Urgency keywords
        if any(word in line_lower for word in ['urgent', 'critical', 'asap', 'immediately']):
            score += 30
        elif any(word in line_lower for word in ['important', 'priority', 'high']):
            score += 20
        
        if has_owner:
            score += 10
        
        if has_due_date:
            score += 15
            if any(word in line_lower for word in ['today', 'eod', 'tomorrow']):
                score += 10
        
        # Strong action verbs
        if any(verb in line_lower for verb in ['fix', 'deploy', 'implement', 'complete', 'finish', 'submit']):
            score += 5
        
        return min(score, 100)
    
    def _estimate_effort(self, line: str) -> str:
        """Estimate effort: low, medium, or high."""
        line_lower = line.lower()
        
        high_effort = ['implement', 'develop', 'build', 'design', 'refactor', 'analyze', 'research']
        if any(word in line_lower for word in high_effort):
            return 'high'
        
        low_effort = ['send', 'email', 'call', 'review', 'update', 'fix small']
        if any(word in line_lower for word in low_effort):
            return 'low'
        
        return 'medium'
    
    def _clean_task_text(self, line: str) -> str:
        """Remove owner mentions and dates for cleaner display."""
        text = re.sub(r'@\w+', '', line)
        text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
