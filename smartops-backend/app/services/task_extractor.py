import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# Action verbs that indicate tasks
ACTION_VERBS = [
    'do', 'create', 'review', 'update', 'fix', 'implement', 'test',
    'deploy', 'write', 'send', 'schedule', 'prepare', 'complete',
    'finish', 'submit', 'call', 'email', 'contact', 'meet', 'discuss',
    'analyze', 'research', 'investigate', 'design', 'build', 'setup',
    'configure', 'install', 'develop', 'refactor', 'optimize'
]


def extract_owner(line: str) -> Optional[str]:
    """Extract owner from @username mentions."""
    match = re.search(r'@(\w+)', line)
    return f"@{match.group(1)}" if match else None


def extract_due_date(line: str) -> Optional[str]:
    """
    Extract due date from various formats:
    - YYYY-MM-DD
    - tomorrow
    - EOD (end of day - today)
    - today
    """
    line_lower = line.lower()
    
    # Check for YYYY-MM-DD format
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', line)
    if date_match:
        return date_match.group(1)
    
    # Check for relative dates
    if 'tomorrow' in line_lower:
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.strftime('%Y-%m-%d')
    
    if 'eod' in line_lower or 'end of day' in line_lower or 'today' in line_lower:
        return datetime.now().strftime('%Y-%m-%d')
    
    return None


def calculate_priority_score(line: str, has_owner: bool, has_due_date: bool) -> int:
    """
    Calculate priority score (0-100) based on various factors.
    """
    score = 50  # Base score
    
    line_lower = line.lower()
    
    # Urgency keywords
    if any(word in line_lower for word in ['urgent', 'critical', 'asap', 'immediately']):
        score += 30
    elif any(word in line_lower for word in ['important', 'priority', 'high']):
        score += 20
    
    # Has owner
    if has_owner:
        score += 10
    
    # Has due date
    if has_due_date:
        score += 15
        # Check if due date is soon
        if any(word in line_lower for word in ['today', 'eod', 'tomorrow']):
            score += 10
    
    # Action verb strength
    strong_verbs = ['fix', 'deploy', 'implement', 'complete', 'finish', 'submit']
    if any(verb in line_lower for verb in strong_verbs):
        score += 5
    
    # Cap at 100
    return min(score, 100)


def estimate_effort(line: str) -> str:
    """
    Estimate effort level based on keywords and complexity indicators.
    """
    line_lower = line.lower()
    
    # High effort indicators
    high_effort = ['implement', 'develop', 'build', 'design', 'refactor', 'analyze', 'research']
    if any(word in line_lower for word in high_effort):
        return 'high'
    
    # Low effort indicators
    low_effort = ['send', 'email', 'call', 'review', 'update', 'fix small']
    if any(word in line_lower for word in low_effort):
        return 'low'
    
    # Default to medium
    return 'medium'


def is_actionable_line(line: str) -> bool:
    """
    Check if a line contains actionable content.
    """
    line_lower = line.lower()
    
    # Check for action verbs
    for verb in ACTION_VERBS:
        # Match verb at word boundary (not part of another word)
        if re.search(rf'\b{verb}\b', line_lower):
            return True
    
    # Check for imperative patterns (commands)
    if re.match(r'^[A-Z][a-z]+\s+', line):  # Starts with capital letter verb
        return True
    
    return False


def extract_and_prioritize_tasks(text: str) -> List[Dict]:
    """
    Extract actionable tasks from text and prioritize them.
    
    Returns:
        List of task dictionaries with task, owner, due_date, priority_score, and effort_estimate
    """
    # Split text into lines
    lines = text.strip().split('\n')
    
    tasks = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines or very short lines
        if not line or len(line) < 10:
            continue
        
        # Check if line is actionable
        if not is_actionable_line(line):
            continue
        
        # Extract task components
        owner = extract_owner(line)
        due_date = extract_due_date(line)
        
        # Calculate priority score
        priority_score = calculate_priority_score(line, bool(owner), bool(due_date))
        
        # Estimate effort
        effort = estimate_effort(line)
        
        # Clean up the task text (remove owner mentions and dates for cleaner display)
        task_text = line
        task_text = re.sub(r'@\w+', '', task_text)  # Remove @mentions
        task_text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '', task_text)  # Remove dates
        task_text = re.sub(r'\s+', ' ', task_text).strip()  # Clean whitespace
        
        tasks.append({
            'task': task_text,
            'owner': owner,
            'due_date': due_date,
            'priority_score': priority_score,
            'effort_estimate': effort
        })
    
    # Sort by priority score (descending)
    tasks.sort(key=lambda x: x['priority_score'], reverse=True)
    
    return tasks
