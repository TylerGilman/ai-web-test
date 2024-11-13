from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Union
import uuid
import datetime

@dataclass
class TestStep:
    action_type: str
    selector: str
    selector_type: str = "xpath"
    input_value: Optional[str] = None
    expected_result: Optional[str] = None
    timeout: int = 10
    
    def to_dict(self):
        return asdict(self)

@dataclass
class TestCase:
    name: str
    description: str
    preconditions: List[str]
    steps: List[TestStep]
    expected_outcome: str
    id: str = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def to_dict(self):
        return asdict(self)
