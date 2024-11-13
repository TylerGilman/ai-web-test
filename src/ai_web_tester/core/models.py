from dataclasses import dataclass
from typing import List, Optional, Dict
import json

@dataclass
class TestAction:
    """Represents a single test action"""
    element_type: str
    selector: str
    action: str
    value: Optional[str] = None
    timestamp: float = None
    
    def to_dict(self):
        return {
            'element_type': self.element_type,
            'selector': self.selector,
            'action': self.action,
            'value': self.value,
            'timestamp': self.timestamp
        }

@dataclass
class TestStep:
    """A step in a test case"""
    action: TestAction
    expected_state: dict
    
    def to_dict(self):
        return {
            'action': self.action.to_dict(),
            'expected_state': self.expected_state
        }

@dataclass
class TestCase:
    """A complete test case"""
    name: str
    url: str
    steps: List[TestStep]
    expected_outcomes: List[dict]
    
    def to_dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'steps': [step.to_dict() for step in self.steps],
            'expected_outcomes': self.expected_outcomes
        }
