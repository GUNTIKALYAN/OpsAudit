from pydantic import BaseModel, Field
from typing import List, Optional


class ReportItem(BaseModel):
    type: str
    column: Optional[str]
    impact: str
    severity: str
    suggestion: str
    confidence: float = Field(ge=0, le=1)
    impact_score: float = Field(ge=0, le=1)


class Summary(BaseModel):
    total_issues: int
    high: int
    medium: int
    low: int


class FinalReport(BaseModel):
    summary: Summary
    details: List[ReportItem]