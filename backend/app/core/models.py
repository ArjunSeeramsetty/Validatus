from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AnalysisContext(BaseModel):
    industry: str
    geography: List[str]
    company_stage: str
    target_audience: str = Field(min_length=5, max_length=200)
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    competitive_context: Optional[str] = None

class AnalysisRequest(BaseModel):
    query: str
    context: AnalysisContext

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    progress: int
    estimated_completion: Optional[str] = None
