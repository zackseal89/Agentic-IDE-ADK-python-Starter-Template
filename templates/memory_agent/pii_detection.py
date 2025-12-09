"""
PII Detection and Redaction Utility for ADK Agents

This module provides utilities for detecting and redacting personally identifiable information (PII)
to ensure privacy and security in agent conversations.
"""

import re
from typing import List, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PiiDetector:
    """Utility for detecting and redacting personally identifiable information (PII)."""
    
    def __init__(self):
        # Common patterns for PII with their replacement values
        self.patterns = [
            # Email addresses
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
            # Phone numbers (US format)
            (r'\b\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b', '[PHONE]'),
            # Credit card numbers (with or without separators)
            (r'\b\d{4}[-\s]?(\d{4}[-\s]?){2}\d{4}\b', '[CREDIT_CARD]'),
            # SSN (US Social Security Number)
            (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]'),
            # IP addresses (IPv4)
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_ADDRESS]'),
            # Basic name pattern (to catch "Name: ..." constructs)
            (r'\b(Name|name)\s*[:\-]\s*([A-Z][a-z]+ [A-Z][a-z]+)', r'\1: [NAME]'),
        ]
        
        # Compile regex patterns for performance
        self.compiled_patterns = [(re.compile(pattern, re.IGNORECASE), replacement) 
                                  for pattern, replacement in self.patterns]
    
    def redact(self, text: str) -> str:
        """
        Redact PII from text.
        
        Args:
            text: The text to redact
            
        Returns:
            Text with PII redacted
        """
        result = text
        for pattern, replacement in self.compiled_patterns:
            result = pattern.sub(replacement, result)
        
        return result
    
    def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect PII in text without redacting.
        
        Args:
            text: The text to scan
            
        Returns:
            List of detected PII with positions and types
        """
        detected_items = []
        
        for i, (pattern, replacement) in enumerate(self.compiled_patterns):
            matches = pattern.finditer(text)
            for match in matches:
                detected_items.append({
                    'type': self._get_pii_type(i),
                    'value': match.group(),
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'replacement': replacement
                })
        
        return detected_items
    
    def _get_pii_type(self, pattern_index: int) -> str:
        """Get the PII type based on pattern index."""
        pii_types = [
            'EMAIL',
            'PHONE',
            'CREDIT_CARD',
            'SSN',
            'IP_ADDRESS',
            'NAME'
        ]
        
        if 0 <= pattern_index < len(pii_types):
            return pii_types[pattern_index]
        else:
            return 'UNKNOWN'


class AdvancedPiiDetector(PiiDetector):
    """Extended PII detector with more sophisticated patterns and validation."""
    
    def __init__(self):
        super().__init__()
        
        # Additional patterns for advanced PII detection
        advanced_patterns = [
            # Date of birth (various formats)
            (r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})\b', '[DOB]'),
            # Bank account numbers (simplified)
            (r'\b\d{8,12}\b', '[BANK_ACCOUNT]'),  # Basic pattern
            # License plates (simplified)
            (r'\b[A-Z]{1,3}\d{3,4}[A-Z]{0,3}\b', '[LICENSE_PLATE]'),  # Simplified pattern
        ]
        
        # Add advanced patterns to the compiled list
        for pattern, replacement in advanced_patterns:
            self.compiled_patterns.append((re.compile(pattern, re.IGNORECASE), replacement))
    
    def validate_context(self, text: str) -> bool:
        """
        Validate if text contains PII in sensitive contexts.
        
        Args:
            text: The text to validate
            
        Returns:
            True if PII is detected in sensitive context, False otherwise
        """
        # Check for direct mentions of sensitive data
        sensitive_indicators = [
            r'password[:\s]+[^\s]+',
            r'api[-_\s]?key[:\s]+[^\s]+',
            r'token[:\s]+[^\s]+',
            r'secret[:\s]+[^\s]+'
        ]
        
        for indicator in sensitive_indicators:
            if re.search(indicator, text, re.IGNORECASE):
                return True
        
        return False


# Singleton instance for use in agents
pii_detector = AdvancedPiiDetector()