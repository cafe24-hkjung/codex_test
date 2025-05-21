from typing import TypeVar, Generic, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

T = TypeVar('T')

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ComplexityLevel(Enum):
    O_1 = "O(1)"
    O_LOG_N = "O(log n)"
    O_N = "O(n)"
    O_N_LOG_N = "O(n log n)"
    O_N_2 = "O(n²)"

@dataclass
class SecurityIssue:
    severity: SecurityLevel
    description: str
    location: str
    timestamp: datetime

class PerformanceMetrics(BaseModel):
    time_complexity: ComplexityLevel
    space_complexity: ComplexityLevel
    optimization_suggestions: List[str]
    memory_usage: float
    execution_time: float

class CodeAnalysisResult(BaseModel):
    complexity_score: float
    suggestions: List[str]
    security_issues: List[SecurityIssue]
    performance: PerformanceMetrics
    code_quality_score: float

class AsyncResult(Generic[T]):
    def __init__(self, value: Optional[T] = None, error: Optional[Exception] = None):
        self.value = value
        self.error = error
        self.timestamp = datetime.now() 
