#!/usr/bin/env python3
"""
Strategic Scoring System V4 - LLM-Based Qualitative Strategic Analysis
Uses LLM to perform comprehensive strategic analysis mimicking human analyst reasoning
"""

import asyncio
import json
import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class StrategicDimension(Enum):
    """Strategic dimensions for comprehensive analysis"""
    OVERALL_VIABILITY = "overall_viability"
    MARKET_POTENTIAL = "market_potential"
    COMPETITIVE_LANDSCAPE = "competitive_landscape"
    CONSUMER_ALIGNMENT = "consumer_alignment"
    INNOVATION_UNIQUENESS = "innovation_uniqueness"
    FINANCIAL_VIABILITY = "financial_viability"
    OPERATIONAL_FEASIBILITY = "operational_feasibility"
    RISK_MITIGATION = "risk_mitigation"

@dataclass
class StrategicDimensionScore:
    """Score and rationale for a strategic dimension"""
    dimension: StrategicDimension
    score: int  # 1-10 scale
    rationale: str
    key_factors: List[str]
    supporting_evidence: List[str]
    confidence: float  # 0.0 to 1.0
    timestamp: datetime

@dataclass
class StrategicAnalysisResultV4:
    """Complete strategic analysis result with LLM-based reasoning"""
    query: str
    context: Dict[str, Any]
    dimension_scores: List[StrategicDimensionScore]
    overall_viability_score: int
    overall_rationale: str
    key_strengths: List[str]
    key_weaknesses: List[str]
    strategic_recommendations: List[str]
    risk_assessment: Dict[str, Any]
    opportunity_analysis: Dict[str, Any]
    market_positioning: str
    competitive_advantage: str
    success_factors: List[str]
    critical_risks: List[str]
    timestamp: datetime
    processing_time: float
    analysis_method: str = "LLM-Based Qualitative Analysis"

class StrategicScoringV4:
    """
    An improved strategic scoring module that uses an LLM to perform a qualitative
    and quantitative analysis, mimicking a traditional strategic review.
    """

    def __init__(self, llm_orchestrator):
        """
        Initializes the scoring module with an LLM orchestrator.
        
        Args:
            llm_orchestrator: MultiLLMOrchestrator instance for LLM calls
        """
        self.llm_orchestrator = llm_orchestrator
        self.logger = logging.getLogger(__name__)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the strategic scoring process.

        Args:
            state: The current state containing all the collected data.

        Returns:
            A dictionary with the comprehensive scoring analysis.
        """
        self.logger.info("🚀 Running Strategic Scoring V4 - LLM-Based Analysis...")
        start_time = datetime.now()
        
        try:
            # Consolidate all research data from the state into a single context string
            full_context = self._create_full_context(state)
            
            if not full_context:
                return {"error": "Not enough data to perform strategic scoring."}

            # Get the business idea description
            idea_description = state.get("idea_description", "Business opportunity analysis")
            
            # The core of the new approach: a detailed prompt asking the LLM to act as an analyst
            prompt = self._create_scoring_prompt(full_context, idea_description)

            # Call the LLM to get the structured analysis
            self.logger.info("📊 Requesting strategic analysis from LLM...")
            
            # Use the LLM orchestrator to get consensus analysis
            llm_response = await self.llm_orchestrator.consensus_analysis(prompt, {
                "analysis_type": "strategic_scoring",
                "framework": "comprehensive_business_analysis",
                "output_format": "structured_json"
            })
            
            if "error" in llm_response:
                self.logger.error(f"LLM analysis failed: {llm_response['error']}")
                return {"error": f"LLM analysis failed: {llm_response['error']}"}

            # Extract the analysis from the consensus response
            consensus_analysis = llm_response.get("consensus", {})
            if not consensus_analysis:
                self.logger.error("No consensus analysis received from LLM")
                return {"error": "No consensus analysis received from LLM"}

            # Parse the LLM response to extract structured data
            analysis_result = await self._parse_llm_response(consensus_analysis, prompt)
            
            # Add processing metadata
            processing_time = (datetime.now() - start_time).total_seconds()
            analysis_result["processing_time"] = processing_time
            analysis_result["timestamp"] = datetime.now().isoformat()
            analysis_result["analysis_method"] = "LLM-Based Qualitative Analysis"
            
            # Add the detailed analysis to the state
            state["strategic_analysis_v4"] = analysis_result
            
            self.logger.info(f"✅ Strategic scoring completed in {processing_time:.2f}s")
            return analysis_result

        except Exception as e:
            self.logger.error(f"Strategic scoring failed: {str(e)}")
            return {"error": f"Strategic scoring failed: {str(e)}"}

    def _create_full_context(self, state: Dict[str, Any]) -> str:
        """
        Gathers all research data from the state into a single string.
        """
        context_parts = []
        
        # Extract data from various agents' results stored in the state
        research_data = state.get("perplexity_research_results", {})
        market_data = state.get("market_analysis", {})
        competitor_data = state.get("competitor_analysis", {})
        consumer_data = state.get("consumer_analysis", {})
        trend_data = state.get("trend_analysis", {})
        pricing_data = state.get("pricing_analysis", {})
        
        if research_data:
            context_parts.append(f"### General Research:\n{json.dumps(research_data, indent=2)}")
        if market_data:
            context_parts.append(f"### Market Analysis:\n{json.dumps(market_data, indent=2)}")
        if competitor_data:
            context_parts.append(f"### Competitor Analysis:\n{json.dumps(competitor_data, indent=2)}")
        if consumer_data:
            context_parts.append(f"### Consumer Insights:\n{json.dumps(consumer_data, indent=2)}")
        if trend_data:
            context_parts.append(f"### Trend Analysis:\n{json.dumps(trend_data, indent=2)}")
        if pricing_data:
            context_parts.append(f"### Pricing Analysis:\n{json.dumps(pricing_data, indent=2)}")
            
        return "\n\n".join(context_parts)

    def _create_scoring_prompt(self, context: str, idea: str) -> str:
        """
        Creates a highly controlled prompt for the LLM to generate properly formatted JSON.
        """
        return f"""You are an expert business strategist. Analyze this business idea: "{idea}"

RESEARCH DATA:
{context}

CRITICAL INSTRUCTIONS:
- Return ONLY valid JSON - no text before or after
- Use exact field names and structure shown below
- All scores must be integers 1-10
- All text fields must be strings (use quotes)
- All arrays must contain only strings

REQUIRED JSON STRUCTURE:
{{
  "overall_viability_score": {{
    "score": 7,
    "rationale": "Your assessment here"
  }},
  "market_potential": {{
    "score": 8,
    "rationale": "Market analysis here"
  }},
  "competitive_landscape": {{
    "score": 6,
    "rationale": "Competitive analysis here"
  }},
  "consumer_alignment": {{
    "score": 8,
    "rationale": "Consumer insights here"
  }},
  "innovation_uniqueness": {{
    "score": 7,
    "rationale": "Innovation assessment here"
  }},
  "financial_viability": {{
    "score": 7,
    "rationale": "Financial analysis here"
  }},
  "operational_feasibility": {{
    "score": 6,
    "rationale": "Operational assessment here"
  }},
  "risk_mitigation": {{
    "score": 6,
    "rationale": "Risk analysis here"
  }},
  "key_strengths": [
    "Strength 1 with evidence",
    "Strength 2 with evidence",
    "Strength 3 with evidence"
  ],
  "key_weaknesses": [
    "Weakness 1 with evidence",
    "Weakness 2 with evidence",
    "Weakness 3 with evidence"
  ],
  "strategic_recommendations": [
    "Recommendation 1",
    "Recommendation 2",
    "Recommendation 3"
  ],
  "market_positioning": "Positioning strategy",
  "competitive_advantage": "Competitive advantage description",
  "success_factors": [
    "Success factor 1",
    "Success factor 2",
    "Success factor 3"
  ],
  "critical_risks": [
    "Risk 1",
    "Risk 2",
    "Risk 3"
  ]
}}

VALIDATION RULES:
1. Start with {{ and end with }}
2. All field names must be in double quotes
3. All string values must be in double quotes
4. All scores must be integers without quotes
5. No trailing commas
6. No comments or explanations outside JSON

Generate ONLY the JSON object above."""

    async def _parse_llm_response(self, consensus_analysis: Dict[str, Any], original_prompt: str) -> Dict[str, Any]:
        """
        Parses the LLM response with retry mechanism for proper JSON generation.
        """
        try:
            # Extract the analysis text from consensus
            analysis_text = consensus_analysis.get("analysis", "")
            
            # Try to extract JSON from the analysis text
            json_data = self._extract_json_from_text(analysis_text)
            
            if json_data:
                # Validate and structure the JSON data
                structured_result = self._validate_and_structure_json(json_data)
                return structured_result
            
            # If JSON extraction fails, try to get a better response from the LLM
            self.logger.warning("JSON extraction failed, attempting to get better formatted response...")
            return await self._retry_with_better_prompt(consensus_analysis, original_prompt)
            
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response: {str(e)}")
            return await self._retry_with_better_prompt(consensus_analysis, original_prompt)
    
    async def _retry_with_better_prompt(self, consensus_analysis: Dict[str, Any], original_prompt: str) -> Dict[str, Any]:
        """
        Retries the analysis with a more explicit JSON formatting prompt.
        """
        try:
            # Create a more explicit prompt for JSON generation
            retry_prompt = self._create_json_fix_prompt(consensus_analysis, original_prompt)
            
            # Get a new response from the LLM
            llm_response = await self.llm_orchestrator.consensus_analysis(retry_prompt, {
                "analysis_type": "json_formatting_fix",
                "framework": "structured_json_only",
                "output_format": "pure_json"
            })
            
            if "error" in llm_response:
                raise Exception(f"LLM retry failed: {llm_response['error']}")
            
            # Extract and parse the new response
            new_analysis_text = llm_response.get("consensus", {}).get("analysis", "")
            json_data = self._extract_json_from_text(new_analysis_text)
            
            if json_data:
                structured_result = self._validate_and_structure_json(json_data)
                structured_result["analysis_method"] = "LLM-Based Qualitative Analysis (Retry)"
                return structured_result
            
            # If still no valid JSON, create a minimal structured result
            return self._create_minimal_structured_result(consensus_analysis)
            
        except Exception as e:
            self.logger.error(f"Retry mechanism failed: {str(e)}")
            return self._create_minimal_structured_result(consensus_analysis)
    
    def _create_json_fix_prompt(self, consensus_analysis: Dict[str, Any], original_prompt: str) -> str:
        """
        Creates a prompt specifically for fixing JSON formatting issues.
        """
        return f"""CRITICAL: Your previous response was not valid JSON. 

You MUST return ONLY a valid JSON object with this EXACT structure:

{{
  "overall_viability_score": {{"score": 7, "rationale": "Your assessment"}},
  "market_potential": {{"score": 8, "rationale": "Market analysis"}},
  "competitive_landscape": {{"score": 6, "rationale": "Competitive analysis"}},
  "consumer_alignment": {{"score": 8, "rationale": "Consumer insights"}},
  "innovation_uniqueness": {{"score": 7, "rationale": "Innovation assessment"}},
  "financial_viability": {{"score": 7, "rationale": "Financial analysis"}},
  "operational_feasibility": {{"score": 6, "rationale": "Operational assessment"}},
  "risk_mitigation": {{"score": 6, "rationale": "Risk analysis"}},
  "key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "key_weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3"],
  "strategic_recommendations": ["Rec 1", "Rec 2", "Rec 3"],
  "market_positioning": "Positioning strategy",
  "competitive_advantage": "Competitive advantage",
  "success_factors": ["Factor 1", "Factor 2", "Factor 3"],
  "critical_risks": ["Risk 1", "Risk 2", "Risk 3"]
}}

RULES:
- NO text before or after the JSON
- Use ONLY the structure above
- All scores must be integers 1-10
- All strings must be in quotes
- NO trailing commas

Return ONLY the JSON object."""
    
    def _create_minimal_structured_result(self, consensus_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a minimal structured result when all JSON parsing attempts fail.
        """
        return {
            "query": "Strategic Business Analysis (Minimal)",
            "context": {},
            "dimension_scores": [],
            "overall_viability_score": 5,
            "overall_rationale": "Analysis completed with minimal structure due to JSON parsing limitations",
            "key_strengths": ["Business opportunity identified"],
            "key_weaknesses": ["Limited analysis depth due to technical constraints"],
            "strategic_recommendations": ["Manual review of analysis results recommended"],
            "risk_assessment": {"overall_risk_level": "medium", "critical_risks": ["Technical limitations"]},
            "opportunity_analysis": {"overall_opportunity_level": "medium", "key_opportunities": ["Business potential identified"]},
            "market_positioning": "Standard positioning",
            "competitive_advantage": "Standard advantages",
            "success_factors": ["Strategic planning"],
            "critical_risks": ["Technical constraints"],
            "analysis_method": "LLM-Based Qualitative Analysis (Minimal Structure)"
        }

    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Robustly extracts and validates JSON data from LLM response.
        """
        try:
            # Clean the text - remove common LLM artifacts
            cleaned_text = text.strip()
            
            # Remove markdown code blocks if present
            cleaned_text = re.sub(r'```json\s*', '', cleaned_text)
            cleaned_text = re.sub(r'```\s*', '', cleaned_text)
            
            # Find the first complete JSON object
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                
                # Validate JSON structure before parsing
                if self._validate_json_structure(json_str):
                    return json.loads(json_str)
            
            # If no complete JSON found, try to find partial JSON and fix it
            partial_match = re.search(r'\{.*', cleaned_text, re.DOTALL)
            if partial_match:
                partial_json = partial_match.group(0)
                fixed_json = self._fix_partial_json(partial_json)
                if fixed_json and self._validate_json_structure(fixed_json):
                    return json.loads(fixed_json)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"JSON extraction failed: {str(e)}")
            return None
    
    def _validate_json_structure(self, json_str: str) -> bool:
        """
        Validates that the JSON string has the expected structure.
        """
        try:
            # Check basic JSON syntax
            json.loads(json_str)
            
            # Check for required fields
            data = json.loads(json_str)
            required_fields = [
                "overall_viability_score", "market_potential", "competitive_landscape",
                "consumer_alignment", "innovation_uniqueness", "key_strengths",
                "key_weaknesses", "strategic_recommendations"
            ]
            
            for field in required_fields:
                if field not in data:
                    return False
            
            # Check that scores are integers
            score_fields = [
                "overall_viability_score", "market_potential", "competitive_landscape",
                "consumer_alignment", "innovation_uniqueness", "financial_viability",
                "operational_feasibility", "risk_mitigation"
            ]
            
            for field in score_fields:
                if field in data:
                    if isinstance(data[field], dict) and "score" in data[field]:
                        if not isinstance(data[field]["score"], int) or data[field]["score"] < 1 or data[field]["score"] > 10:
                            return False
            
            return True
            
        except Exception:
            return False
    
    def _fix_partial_json(self, partial_json: str) -> Optional[str]:
        """
        Attempts to fix common JSON formatting issues.
        """
        try:
            # Remove trailing commas
            fixed = re.sub(r',\s*}', '}', partial_json)
            fixed = re.sub(r',\s*]', ']', fixed)
            
            # Ensure proper closing braces
            open_braces = fixed.count('{')
            close_braces = fixed.count('}')
            open_brackets = fixed.count('[')
            close_brackets = fixed.count(']')
            
            # Add missing closing braces/brackets
            while close_braces < open_braces:
                fixed += '}'
                close_braces += 1
            
            while close_brackets < open_brackets:
                fixed += ']'
                close_brackets += 1
            
            # Try to parse the fixed JSON
            json.loads(fixed)
            return fixed
            
        except Exception:
            return None

    def _validate_and_structure_json(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and structures the extracted JSON data.
        """
        # Ensure all required fields are present with defaults
        structured = {
            "query": "Strategic Business Analysis",
            "context": {},
            "dimension_scores": [],
            "overall_viability_score": json_data.get("overall_viability_score", {}).get("score", 5),
            "overall_rationale": json_data.get("overall_viability_score", {}).get("rationale", "Analysis completed"),
            "key_strengths": json_data.get("key_strengths", []),
            "key_weaknesses": json_data.get("key_weaknesses", []),
            "strategic_recommendations": json_data.get("strategic_recommendations", []),
            "risk_assessment": {},
            "opportunity_analysis": {},
            "market_positioning": json_data.get("market_positioning", "Standard positioning"),
            "competitive_advantage": json_data.get("competitive_advantage", "Standard advantages"),
            "success_factors": json_data.get("success_factors", []),
            "critical_risks": json_data.get("critical_risks", [])
        }
        
        # Build dimension scores
        dimensions = [
            ("market_potential", StrategicDimension.MARKET_POTENTIAL),
            ("competitive_landscape", StrategicDimension.COMPETITIVE_LANDSCAPE),
            ("consumer_alignment", StrategicDimension.CONSUMER_ALIGNMENT),
            ("innovation_uniqueness", StrategicDimension.INNOVATION_UNIQUENESS),
            ("financial_viability", StrategicDimension.FINANCIAL_VIABILITY),
            ("operational_feasibility", StrategicDimension.OPERATIONAL_FEASIBILITY),
            ("risk_mitigation", StrategicDimension.RISK_MITIGATION)
        ]
        
        for key, dimension in dimensions:
            if key in json_data:
                data = json_data[key]
                score = StrategicDimensionScore(
                    dimension=dimension,
                    score=data.get("score", 5),
                    rationale=data.get("rationale", f"Analysis for {dimension.value}"),
                    key_factors=[],
                    supporting_evidence=[],
                    confidence=0.8,
                    timestamp=datetime.now()
                )
                structured["dimension_scores"].append(score)
        
        # Add risk and opportunity analysis
        structured["risk_assessment"] = {
            "overall_risk_level": "medium",
            "critical_risks": structured["critical_risks"],
            "mitigation_strategies": []
        }
        
        structured["opportunity_analysis"] = {
            "overall_opportunity_level": "medium",
            "key_opportunities": structured["key_strengths"],
            "capture_strategies": []
        }
        
        return structured

    def _create_fallback_analysis(self, consensus_analysis: Dict[str, Any], original_prompt: str) -> Dict[str, Any]:
        """
        Creates a fallback analysis when JSON parsing fails.
        """
        self.logger.warning("Using fallback analysis due to JSON parsing failure")
        
        # Extract insights from the consensus analysis
        analysis_text = consensus_analysis.get("analysis", "")
        individual_results = consensus_analysis.get("individual_results", [])
        
        # Create basic structure
        fallback_result = {
            "query": "Strategic Business Analysis (Fallback)",
            "context": {},
            "dimension_scores": [],
            "overall_viability_score": 5,
            "overall_rationale": "Analysis completed using fallback method",
            "key_strengths": ["Analysis completed successfully"],
            "key_weaknesses": ["Using fallback analysis method"],
            "strategic_recommendations": ["Review analysis results carefully"],
            "risk_assessment": {
                "overall_risk_level": "medium",
                "critical_risks": ["Analysis method limitations"],
                "mitigation_strategies": ["Manual review recommended"]
            },
            "opportunity_analysis": {
                "overall_opportunity_level": "medium",
                "key_opportunities": ["Business potential identified"],
                "capture_strategies": ["Further analysis recommended"]
            },
            "market_positioning": "Standard positioning",
            "competitive_advantage": "Standard advantages",
            "success_factors": ["Strategic planning", "Market research"],
            "critical_risks": ["Limited analysis depth"],
            "analysis_method": "LLM-Based Qualitative Analysis (Fallback)"
        }
        
        # Try to extract some insights from the text
        if analysis_text:
            # Try to extract JSON-like content first
            import re
            json_pattern = r'"([^"]+)"\s*:\s*"([^"]+)"'
            json_matches = re.findall(json_pattern, analysis_text)
            
            if json_matches:
                # Extract meaningful content from JSON-like structure
                insights = []
                recommendations = []
                
                for key, value in json_matches:
                    if key.lower() in ['rationale', 'insight', 'strength', 'advantage']:
                        if len(value) > 20:
                            insights.append(value)
                    elif key.lower() in ['recommendation', 'suggestion', 'action']:
                        if len(value) > 20:
                            recommendations.append(value)
                
                # If we found structured content, use it
                if insights or recommendations:
                    fallback_result["key_strengths"] = insights[:3] if insights else ["Analysis completed successfully"]
                    fallback_result["strategic_recommendations"] = recommendations[:3] if recommendations else ["Review results carefully"]
                    
                    # Create better rationale
                    if insights:
                        fallback_result["overall_rationale"] = f"Analysis completed using structured data. Key insights: {insights[0][:100]}..."
                    return fallback_result
            
            # Fallback to line-by-line analysis
            lines = analysis_text.split('\n')
            insights = []
            for line in lines[:20]:  # Take first 20 lines for better coverage
                line = line.strip()
                # Filter out JSON syntax and model references
                if (line and len(line) > 20 and 
                    not line.startswith('Model') and 
                    not line.startswith('"') and
                    not line.startswith('{') and
                    not line.startswith('}') and
                    not line.startswith('[') and
                    not line.startswith(']')):
                    insights.append(line)
            
            if insights:
                # Split insights into strengths and recommendations
                mid_point = len(insights) // 2
                fallback_result["key_strengths"] = insights[:mid_point]
                fallback_result["strategic_recommendations"] = insights[mid_point:] if mid_point < len(insights) else ["Further analysis needed"]
                
                # Try to extract a better overall rationale
                if insights:
                    fallback_result["overall_rationale"] = f"Analysis completed using consensus data. Key insights: {insights[0][:100]}..."
        
        # If no meaningful insights extracted, provide default insights based on the idea
        if not fallback_result.get("key_strengths") or len(fallback_result["key_strengths"]) <= 1:
            fallback_result["key_strengths"] = [
                "Business opportunity identified and analyzed",
                "Multiple AI models provided consensus analysis",
                "Strategic framework applied successfully"
            ]
            fallback_result["strategic_recommendations"] = [
                "Review detailed analysis results carefully",
                "Consider market research for validation",
                "Develop implementation strategy based on insights"
            ]
        
        return fallback_result

    async def get_analysis_summary(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a summary of the strategic analysis results.
        """
        try:
            summary = {
                "overall_score": analysis_result.get("overall_viability_score", 0),
                "score_breakdown": {},
                "top_strengths": analysis_result.get("key_strengths", [])[:3],
                "top_weaknesses": analysis_result.get("key_weaknesses", [])[:3],
                "key_recommendations": analysis_result.get("strategic_recommendations", [])[:3],
                "risk_level": analysis_result.get("risk_assessment", {}).get("overall_risk_level", "unknown"),
                "opportunity_level": analysis_result.get("opportunity_analysis", {}).get("overall_opportunity_level", "unknown"),
                "analysis_timestamp": analysis_result.get("timestamp", ""),
                "processing_time": analysis_result.get("processing_time", 0)
            }
            
            # Add dimension score breakdown
            for score in analysis_result.get("dimension_scores", []):
                summary["score_breakdown"][score.dimension.value] = {
                    "score": score.score,
                    "confidence": score.confidence
                }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate analysis summary: {str(e)}")
            return {"error": f"Summary generation failed: {str(e)}"}

    def export_analysis_report(self, analysis_result: Dict[str, Any], format: str = "json") -> str:
        """
        Exports the analysis result in the specified format.
        """
        try:
            if format.lower() == "json":
                return json.dumps(analysis_result, indent=2, default=str)
            elif format.lower() == "text":
                return self._format_as_text(analysis_result)
            else:
                return json.dumps(analysis_result, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return f"Export failed: {str(e)}"

    def _format_as_text(self, analysis_result: Dict[str, Any]) -> str:
        """
        Formats the analysis result as readable text.
        """
        text_parts = []
        
        text_parts.append("=" * 60)
        text_parts.append("STRATEGIC BUSINESS ANALYSIS REPORT")
        text_parts.append("=" * 60)
        text_parts.append("")
        
        # Overall score
        text_parts.append(f"OVERALL VIABILITY SCORE: {analysis_result.get('overall_viability_score', 0)}/10")
        text_parts.append(f"Rationale: {analysis_result.get('overall_rationale', 'N/A')}")
        text_parts.append("")
        
        # Dimension scores
        text_parts.append("DIMENSION SCORES:")
        text_parts.append("-" * 30)
        for score in analysis_result.get("dimension_scores", []):
            text_parts.append(f"{score.dimension.value.replace('_', ' ').title()}: {score.score}/10")
            text_parts.append(f"  {score.rationale}")
            text_parts.append("")
        
        # Key insights
        text_parts.append("KEY STRENGTHS:")
        text_parts.append("-" * 20)
        for strength in analysis_result.get("key_strengths", []):
            text_parts.append(f"• {strength}")
        text_parts.append("")
        
        text_parts.append("KEY WEAKNESSES:")
        text_parts.append("-" * 20)
        for weakness in analysis_result.get("key_weaknesses", []):
            text_parts.append(f"• {weakness}")
        text_parts.append("")
        
        # Recommendations
        text_parts.append("STRATEGIC RECOMMENDATIONS:")
        text_parts.append("-" * 30)
        for rec in analysis_result.get("strategic_recommendations", []):
            text_parts.append(f"• {rec}")
        text_parts.append("")
        
        # Risk assessment
        risk_assessment = analysis_result.get("risk_assessment", {})
        text_parts.append(f"RISK ASSESSMENT: {risk_assessment.get('overall_risk_level', 'N/A').upper()}")
        text_parts.append("-" * 30)
        for risk in risk_assessment.get("critical_risks", []):
            text_parts.append(f"⚠️  {risk}")
        text_parts.append("")
        
        # Analysis metadata
        text_parts.append("ANALYSIS METADATA:")
        text_parts.append("-" * 20)
        text_parts.append(f"Analysis Method: {analysis_result.get('analysis_method', 'N/A')}")
        text_parts.append(f"Processing Time: {analysis_result.get('processing_time', 0):.2f}s")
        text_parts.append(f"Timestamp: {analysis_result.get('timestamp', 'N/A')}")
        
        return "\n".join(text_parts)
