import re
from typing import List


def redact_pii(text: str) -> str:
    """
    Redact PII (emails and phone numbers) from text.
    """
    # Redact email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
    
    # Redact phone numbers (various formats)
    # Matches: (123) 456-7890, 123-456-7890, 123.456.7890, +1 123 456 7890, etc.
    text = re.sub(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', '[PHONE_REDACTED]', text)
    text = re.sub(r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', '[PHONE_REDACTED]', text)
    
    return text


def score_sentence(sentence: str) -> float:
    """
    Score a sentence based on importance indicators.
    Higher scores = more important sentences.
    """
    score = 0.0
    
    # Length: prefer medium-length sentences
    word_count = len(sentence.split())
    if 10 <= word_count <= 30:
        score += 2.0
    elif 5 <= word_count < 10 or 30 < word_count <= 40:
        score += 1.0
    
    # Keywords indicating importance
    importance_keywords = [
        'important', 'critical', 'key', 'significant', 'essential',
        'must', 'should', 'need', 'required', 'priority',
        'objective', 'goal', 'result', 'conclusion', 'summary'
    ]
    
    sentence_lower = sentence.lower()
    for keyword in importance_keywords:
        if keyword in sentence_lower:
            score += 1.5
    
    # Position bonus (first and last sentences often important)
    # This will be applied in summarize_text function
    
    # Sentence completeness
    if sentence.strip().endswith(('.', '!', '?')):
        score += 0.5
    
    return score


def summarize_text(text: str, num_sentences: int = 5) -> str:
    """
    Create an extractive summary by selecting the most important sentences.
    
    Args:
        text: Input text to summarize
        num_sentences: Number of sentences to include in summary (default: 5)
    
    Returns:
        A summary string with PII redacted
    """
    # Redact PII first
    text = redact_pii(text)
    
    # Split into sentences
    # Simple sentence splitting (can be improved with NLTK if needed, but keeping it simple)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    
    # Score each sentence
    sentence_scores = []
    for idx, sentence in enumerate(sentences):
        score = score_sentence(sentence)
        
        # Position bonus
        if idx == 0:  # First sentence
            score += 1.0
        elif idx == len(sentences) - 1:  # Last sentence
            score += 0.5
        
        sentence_scores.append((score, idx, sentence))
    
    # Sort by score (descending) and take top N
    sentence_scores.sort(reverse=True, key=lambda x: x[0])
    top_sentences = sentence_scores[:num_sentences]
    
    # Re-order by original position to maintain flow
    top_sentences.sort(key=lambda x: x[1])
    
    # Extract just the sentences
    summary_sentences = [sent for _, _, sent in top_sentences]
    
    return ' '.join(summary_sentences)
