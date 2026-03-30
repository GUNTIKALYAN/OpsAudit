# app/schemas/issue_schema.py

from typing import TypedDict, Optional


class BaseIssue(TypedDict, total=False):
    type: str


class DuplicateIssue(BaseIssue, total=False):
    type: str  # "duplicate"
    level: str  # "row" or "column"
    column: Optional[str]
    count: int


class MissingIssue(BaseIssue, total=False):
    type: str  # "missing"
    column: str
    missing_count: int
    missing_percentage: float


class LogicIssue(BaseIssue, total=False):
    type: str  # "logic_error"
    rule: str
    violations: int


class AnomalyIssue(BaseIssue, total=False):
    type: str  # "anomaly"
    column: str
    outliers: int