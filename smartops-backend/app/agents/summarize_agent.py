"""
SummarizeAgent: Extracts key sentences and redacts PII.
"""
import re
from app.agents import BaseAgent
from app.models import SummarizeInput, SummarizeOutput


class SummarizeAgent(BaseAgent[SummarizeInput, SummarizeOutput]):
    """
    Agent that creates extractive summaries with PII redaction.
    """
    
    def __init__(self):
        super().__init__(name="SummarizeAgent")
    
    def process(self, input_data: SummarizeInput) -> SummarizeOutput:
        """
        Generate summary from input text.
        """
        text = input_data.text
        num_sentences = input_data.num_sentences
        
        # Redact PII and count redactions
        redacted_text, pii_count = self._redact_pii(text)
        
        # Extract sentences
        sentences = self._split_sentences(redacted_text)
        
        if len(sentences) <= num_sentences:
            summary = ' '.join(sentences)
            actual_count = len(sentences)
        else:
            # Score and select top sentences
            scored_sentences = self._score_sentences(sentences)
            top_sentences = scored_sentences[:num_sentences]
            
            # Re-order by original position
            top_sentences.sort(key=lambda x: x[1])
            summary = ' '.join([sent for _, _, sent in top_sentences])
            actual_count = num_sentences
        
        return SummarizeOutput(
            summary=summary,
            sentence_count=actual_count,
            redacted_pii_count=pii_count
        )
    
    def _redact_pii(self, text: str) -> tuple[str, int]:
        """Redact emails and phone numbers. Returns (redacted_text, count)."""
        count = 0
        
        # Count and redact emails
        email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        count += len(email_matches)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
        
        # Count and redact phone numbers
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phone_matches = re.findall(phone_pattern, text)
        count += len(phone_matches)
        text = re.sub(phone_pattern, '[PHONE_REDACTED]', text)
        
        return text, count
    
    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    def _score_sentences(self, sentences: list[str]) -> list[tuple[float, int, str]]:
        """
        Score sentences by importance.
        Returns list of (score, original_index, sentence) sorted by score desc.
        """
        scored = []
        
        importance_keywords = [
            'important', 'critical', 'key', 'significant', 'essential',
            'must', 'should', 'need', 'required', 'priority',
            'objective', 'goal', 'result', 'conclusion', 'summary'
        ]
        
        for idx, sentence in enumerate(sentences):
            score = 0.0
            word_count = len(sentence.split())
            sentence_lower = sentence.lower()
            
            # Length score
            if 10 <= word_count <= 30:
                score += 2.0
            elif 5 <= word_count < 10 or 30 < word_count <= 40:
                score += 1.0
            
            # Keyword score
            for keyword in importance_keywords:
                if keyword in sentence_lower:
                    score += 1.5
            
            # Position bonus
            if idx == 0:
                score += 1.0
            elif idx == len(sentences) - 1:
                score += 0.5
            
            # Completeness
            if sentence.strip().endswith(('.', '!', '?')):
                score += 0.5
            
            scored.append((score, idx, sentence))
        
        # Sort by score descending
        scored.sort(reverse=True, key=lambda x: x[0])
        return scored
