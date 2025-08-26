#!/usr/bin/env python3
"""
Simple State class for LangGraph workflow
Provides basic state management functionality
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class State:
    """Simple state management for LangGraph workflow"""
    
    # Core data
    idea_description: str
    target_audience: str = "General market"
    additional_context: Dict[str, Any] = field(default_factory=dict)
    
    # Analysis results
    market_analysis: Optional[Dict[str, Any]] = None
    competitor_analysis: Optional[Dict[str, Any]] = None
    consumer_analysis: Optional[Dict[str, Any]] = None
    trend_analysis: Optional[Dict[str, Any]] = None
    pricing_analysis: Optional[Dict[str, Any]] = None
    strategic_analysis_v4: Optional[Dict[str, Any]] = None
    knowledge_graph_analysis: Optional[Dict[str, Any]] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the state"""
        if hasattr(self, key):
            setattr(self, key, value)
            self.updated_at = datetime.now()
        else:
            # Store in additional_context if key doesn't exist
            self.additional_context[key] = value
            self.updated_at = datetime.now()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state"""
        if hasattr(self, key):
            value = getattr(self, key)
            return value if value is not None else default
        return self.additional_context.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        state_dict = {
            "idea_description": self.idea_description,
            "target_audience": self.target_audience,
            "additional_context": self.additional_context,
            "market_analysis": self.market_analysis,
            "competitor_analysis": self.competitor_analysis,
            "consumer_analysis": self.consumer_analysis,
            "trend_analysis": self.trend_analysis,
            "pricing_analysis": self.pricing_analysis,
            "strategic_analysis_v4": self.strategic_analysis_v4,
            "knowledge_graph_analysis": self.knowledge_graph_analysis,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        return state_dict
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple values at once"""
        for key, value in updates.items():
            self.set(key, value)
    
    def is_complete(self) -> bool:
        """Check if all required analysis is complete"""
        required_fields = [
            "market_analysis", "competitor_analysis", "consumer_analysis",
            "trend_analysis", "pricing_analysis", "strategic_analysis_v4"
        ]
        return all(self.get(field) is not None for field in required_fields)
    
    def get_progress(self) -> float:
        """Get completion progress as percentage"""
        total_fields = 6  # Total required fields
        completed_fields = sum(1 for field in [
            "market_analysis", "competitor_analysis", "consumer_analysis",
            "trend_analysis", "pricing_analysis", "strategic_analysis_v4"
        ] if self.get(field) is not None)
        return (completed_fields / total_fields) * 100
