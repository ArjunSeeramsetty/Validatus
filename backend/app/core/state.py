from typing import TypedDict, Dict, Any, List, Optional
from enum import Enum

class AnalysisStatus(str, Enum):
    INITIATED = "initiated"
    PARSING = "parsing"
    PLANNING = "planning"
    RESEARCHING = "researching"
    SCORING = "scoring"
    AGGREGATING = "aggregating"
    SUMMARIZING = "summarizing"
    COMPLETED = "completed"
    FAILED = "failed"

class LayerScoreResult(TypedDict):
    score: float  # 0-100
    confidence: float  # 0-1
    calculation_method: str
    supporting_data: Dict[str, Any]
    data_sources: List[str]
    summary: str

class FactorScoreResult(TypedDict):
    score: float
    confidence: float
    summary: str

class SegmentScoreResult(TypedDict):
    score: float
    confidence: float
    summary: str

class ValidatusState(TypedDict):
    # Input
    user_query: str
    analysis_context: Dict[str, Any]
    analysis_id: str
    
    # Processing state
    query_interpretation: Dict[str, Any]
    research_tasks: List[Dict[str, Any]]
    research_results: Dict[str, Any]
    
    # Scoring state
    layer_scores: Dict[str, Any]
    factor_scores: Dict[str, Any]
    segment_scores: Dict[str, Any]
    
    # Output
    dashboard_data: Dict[str, Any]
    recommendations: List[str]
    
    # Metadata
    status: AnalysisStatus
    progress: int
    errors: List[str]
    timestamp: str

class ResearchTask(TypedDict):
    agent_type: str
    segment: str
    factor: str
    layer: str
    query: str
    context: Dict[str, Any]
