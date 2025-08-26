import asyncio
import openai
import anthropic
import google.generativeai as genai
import httpx
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import logging
from dataclasses import dataclass
from enum import Enum
import numpy as np
from config import settings

class ConsensusMethod(Enum):
    """Methods for building consensus across multiple LLMs"""
    MAJORITY_VOTE = "majority_vote"
    WEIGHTED_AVERAGE = "weighted_average"
    CONFIDENCE_BASED = "confidence_based"
    EXPERT_VALIDATION = "expert_validation"
    CLUSTERING_BASED = "clustering_based"

@dataclass
class LLMAnalysisResult:
    """Structured result from a single LLM analysis"""
    model_name: str
    analysis: str
    confidence: float
    key_insights: List[str]
    recommendations: List[str]
    execution_time: float
    cost: float
    timestamp: datetime
    metadata: Dict[str, Any]

class OpenAIAgent:
    """OpenAI GPT-4 agent for strategic analysis with current market focus"""
    
    def __init__(self, model: str = 'gpt-4o'):
        self.model = model
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.logger = logging.getLogger(f"llm.openai.{model}")
    
    async def analyze(self, query: str, context: Dict[str, Any] = None) -> LLMAnalysisResult:
        """Conduct strategic analysis using OpenAI with current market focus"""
        start_time = datetime.now()
        
        try:
            # Check if this is a strategic scoring request that needs JSON output
            if context and context.get("output_format") == "structured_json":
                system_prompt = self._build_json_prompt(query, context)
            else:
                system_prompt = self._build_system_prompt(context)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            execution_time = (datetime.now() - start_time).total_seconds()
            
            key_insights = self._extract_key_insights(analysis)
            recommendations = self._extract_recommendations(analysis)
            confidence = self._calculate_confidence(analysis, key_insights, recommendations)
            cost = self._estimate_cost(response.usage.total_tokens)
            
            return LLMAnalysisResult(
                model_name=f"OpenAI-{self.model}",
                analysis=analysis,
                confidence=confidence,
                key_insights=key_insights,
                recommendations=recommendations,
                execution_time=execution_time,
                cost=cost,
                timestamp=datetime.now(),
                metadata={"tokens_used": response.usage.total_tokens, "market_focus": "current"}
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI analysis failed: {str(e)}")
            return LLMAnalysisResult(
                model_name=f"OpenAI-{self.model}",
                analysis=f"Analysis failed: {str(e)}",
                confidence=0.0,
                key_insights=[],
                recommendations=[],
                execution_time=(datetime.now() - start_time).total_seconds(),
                cost=0.0,
                timestamp=datetime.now(),
                metadata={"error": str(e)}
            )
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Build system prompt for strategic analysis with current market focus"""
        base_prompt = """You are an expert strategic analyst specializing in business intelligence and market analysis. 
        
        CRITICAL: Focus on CURRENT market conditions and recent developments (last 6-12 months).
        Prioritize data recency and relevance to present market dynamics.
        
        Your analysis should include:
        1. Key strategic insights - Based on current market conditions
        2. Market implications - Recent developments and trends
        3. Risk assessment - Current market risks and volatility
        4. Actionable recommendations - Feasible in current market environment
        5. Confidence level (0-1 scale) - Reflect data recency and quality
        
        MARKET DATA REQUIREMENTS:
        - Use recent market data (last 6-12 months)
        - Consider current economic conditions and volatility
        - Factor in recent regulatory changes and industry developments
        - Base analysis on current competitive landscape
        
        Format your response in a clear, structured manner."""
        
        # Add current market context
        current_date = datetime.now().strftime("%Y-%m-%d")
        market_context = f"\n\nANALYSIS DATE: {current_date}"
        market_context += "\nMARKET CONTEXT: Current market conditions and recent developments (last 6-12 months)"
        
        if context:
            context_str = json.dumps(context, indent=2)
            base_prompt += f"\n\nContext: {context_str}"
        
        return f"{base_prompt}{market_context}"
    
    def _extract_key_insights(self, analysis: str) -> List[str]:
        """Extract key insights from analysis text"""
        try:
            lines = analysis.split('\n')
            insights = []
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('•', '-', '*', '1.', '2.', '3.')) or 
                           'insight' in line.lower() or 'finding' in line.lower()):
                    insights.append(line)
            
            return insights[:5]
        except Exception:
            return []
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis text"""
        try:
            lines = analysis.split('\n')
            recommendations = []
            
            for line in lines:
                line = line.strip()
                if line and ('recommend' in line.lower() or 'suggest' in line.lower() or 
                           'should' in line.lower() or 'action' in line.lower()):
                    recommendations.append(line)
            
            return recommendations[:5]
        except Exception:
            return []
    
    def _calculate_confidence(self, analysis: str, insights: List[str], recommendations: List[str]) -> float:
        """Calculate confidence score based on response quality"""
        try:
            confidence = 0.5
            
            if len(analysis) > 500:
                confidence += 0.1
            
            if len(insights) >= 3:
                confidence += 0.2
            
            if len(recommendations) >= 2:
                confidence += 0.2
            
            if any(marker in analysis for marker in ['1.', '2.', '3.', '•', '-']):
                confidence += 0.1
            
            return min(1.0, confidence)
        except Exception:
            return 0.5
    
    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost based on token usage"""
        cost_per_1k = 0.005  # $0.005 per 1K tokens
        return (tokens / 1000) * cost_per_1k
    
    def _build_json_prompt(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build a prompt specifically for JSON-structured strategic analysis"""
        return f"""You are an expert business strategist. Analyze: "{query}"

CRITICAL: Return ONLY valid JSON with this EXACT structure:

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
- NO text before or after JSON
- Use ONLY the structure above
- All scores must be integers 1-10
- All strings must be in quotes
- NO trailing commas

Return ONLY the JSON object."""

class AnthropicAgent:
    """Anthropic Claude agent for strategic analysis with current market focus"""
    
    def __init__(self, model: str = 'claude-3-5-sonnet-20241022'):
        self.model = model
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.logger = logging.getLogger(f"llm.anthropic.{model}")
    
    async def analyze(self, query: str, context: Dict[str, Any] = None) -> LLMAnalysisResult:
        """Conduct strategic analysis using Anthropic Claude with current market focus"""
        start_time = datetime.now()
        
        try:
            system_prompt = self._build_system_prompt(context)
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            
            analysis = response.content[0].text
            execution_time = (datetime.now() - start_time).total_seconds()
            
            key_insights = self._extract_key_insights(analysis)
            recommendations = self._extract_recommendations(analysis)
            confidence = self._calculate_confidence(analysis, key_insights, recommendations)
            cost = self._estimate_cost(response.usage.input_tokens + response.usage.output_tokens)
            
            return LLMAnalysisResult(
                model_name=f"Anthropic-{self.model}",
                analysis=analysis,
                confidence=confidence,
                key_insights=key_insights,
                recommendations=recommendations,
                execution_time=execution_time,
                cost=cost,
                timestamp=datetime.now(),
                metadata={"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens, "market_focus": "current"}
            )
            
        except Exception as e:
            self.logger.error(f"Anthropic analysis failed: {str(e)}")
            return LLMAnalysisResult(
                model_name=f"Anthropic-{self.model}",
                analysis=f"Analysis failed: {str(e)}",
                confidence=0.0,
                key_insights=[],
                recommendations=[],
                execution_time=(datetime.now() - start_time).total_seconds(),
                cost=0.0,
                timestamp=datetime.now(),
                metadata={"error": str(e)}
            )
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Build system prompt for strategic analysis with current market focus"""
        base_prompt = """You are an expert strategic analyst specializing in business intelligence and market analysis. 
        
        CRITICAL: Focus on CURRENT market conditions and recent developments (last 6-12 months).
        Prioritize data recency and relevance to present market dynamics.
        
        Your analysis should include:
        1. Key strategic insights - Based on current market conditions
        2. Market implications - Recent developments and trends
        3. Risk assessment - Current market risks and volatility
        4. Actionable recommendations - Feasible in current market environment
        5. Confidence level (0-1 scale) - Reflect data recency and quality
        
        MARKET DATA REQUIREMENTS:
        - Use recent market data (last 6-12 months)
        - Consider current economic conditions and volatility
        - Factor in recent regulatory changes and industry developments
        - Base analysis on current competitive landscape
        
        Format your response in a clear, structured manner."""
        
        # Add current market context
        current_date = datetime.now().strftime("%Y-%m-%d")
        market_context = f"\n\nANALYSIS DATE: {current_date}"
        market_context += "\nMARKET CONTEXT: Current market conditions and recent developments (last 6-12 months)"
        
        if context:
            context_str = json.dumps(context, indent=2)
            base_prompt += f"\n\nContext: {context_str}"
        
        return f"{base_prompt}{market_context}"
    
    def _extract_key_insights(self, analysis: str) -> List[str]:
        """Extract key insights from analysis text"""
        try:
            lines = analysis.split('\n')
            insights = []
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('•', '-', '*', '1.', '2.', '3.')) or 
                           'insight' in line.lower() or 'finding' in line.lower()):
                    insights.append(line)
            
            return insights[:5]
        except Exception:
            return []
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis text"""
        try:
            lines = analysis.split('\n')
            insights = []
            
            for line in lines:
                line = line.strip()
                if line and ('recommend' in line.lower() or 'suggest' in line.lower() or 
                           'should' in line.lower() or 'action' in line.lower()):
                    insights.append(line)
            
            return insights[:5]
        except Exception:
            return []
    
    def _calculate_confidence(self, analysis: str, insights: List[str], recommendations: List[str]) -> float:
        """Calculate confidence score based on response quality"""
        try:
            confidence = 0.5
            
            if len(analysis) > 500:
                confidence += 0.1
            
            if len(insights) >= 3:
                confidence += 0.2
            
            if len(recommendations) >= 2:
                confidence += 0.2
            
            if any(marker in analysis for marker in ['1.', '2.', '3.', '•', '-']):
                confidence += 0.1
            
            return min(1.0, confidence)
        except Exception:
            return 0.5
    
    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost based on token usage"""
        cost_per_1k = 0.003  # $0.003 per 1K tokens for Claude
        return (tokens / 1000) * cost_per_1k

class PerplexityAgent:
    """Perplexity Sonar agent for strategic analysis with current market focus"""
    
    def __init__(self, model: str = 'sonar-pro'):
        self.model = model
        self.base_url = "https://api.perplexity.ai"
        self.api_key = settings.PERPLEXITY_API_KEY
        self.logger = logging.getLogger(f"llm.perplexity.{model}")
    
    async def analyze(self, query: str, context: Dict[str, Any] = None) -> LLMAnalysisResult:
        """Conduct strategic analysis using Perplexity Sonar with current market focus"""
        start_time = datetime.now()
        
        try:
            import httpx
            
            enhanced_query = self._build_enhanced_query(query, context)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": self._build_system_prompt(context)
                            },
                            {
                                "role": "user",
                                "content": enhanced_query
                            }
                        ],
                        "max_tokens": 2000,
                        "temperature": 0.3
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                analysis = data['choices'][0]['message']['content']
                execution_time = (datetime.now() - start_time).total_seconds()
                
                key_insights = self._extract_key_insights(analysis)
                recommendations = self._extract_recommendations(analysis)
                confidence = self._calculate_confidence(analysis, key_insights, recommendations)
                cost = self._estimate_cost(len(analysis.split()))
                
                return LLMAnalysisResult(
                    model_name=f"Perplexity-{self.model}",
                    analysis=analysis,
                    confidence=confidence,
                    key_insights=key_insights,
                    recommendations=recommendations,
                    execution_time=execution_time,
                    cost=cost,
                    timestamp=datetime.now(),
                    metadata={"word_count": len(analysis.split()), "market_focus": "current"}
                )
                
        except Exception as e:
            self.logger.error(f"Perplexity analysis failed: {str(e)}")
            return LLMAnalysisResult(
                model_name=f"Perplexity-{self.model}",
                analysis=f"Analysis failed: {str(e)}",
                confidence=0.0,
                key_insights=[],
                recommendations=[],
                execution_time=(datetime.now() - start_time).total_seconds(),
                cost=0.0,
                timestamp=datetime.now(),
                metadata={"error": str(e)}
            )
    
    def _build_enhanced_query(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build enhanced query with current market context"""
        enhanced = f"Strategic Analysis Request: {query}"
        
        # Add current market context
        current_date = datetime.now().strftime("%Y-%m-%d")
        enhanced += f"\n\nANALYSIS DATE: {current_date}"
        enhanced += "\nMARKET CONTEXT: Current market conditions and recent developments (last 6-12 months)"
        
        if context:
            context_str = json.dumps(context, indent=2)
            enhanced += f"\n\nContext: {context_str}"
        
        enhanced += "\n\nPlease provide comprehensive strategic analysis including key insights, market implications, risk assessment, and actionable recommendations. Focus on CURRENT market conditions and recent developments."
        
        return enhanced
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Build system prompt for strategic analysis with current market focus"""
        base_prompt = """You are an expert strategic analyst specializing in business intelligence and market analysis. 
        
        CRITICAL: Focus on CURRENT market conditions and recent developments (last 6-12 months).
        Prioritize data recency and relevance to present market dynamics.
        
        Your analysis should include:
        1. Key strategic insights - Based on current market conditions
        2. Market implications - Recent developments and trends
        3. Risk assessment - Current market risks and volatility
        4. Actionable recommendations - Feasible in current market environment
        5. Confidence level (0-1 scale) - Reflect data recency and quality
        
        MARKET DATA REQUIREMENTS:
        - Use recent market data (last 6-12 months)
        - Consider current economic conditions and volatility
        - Factor in recent regulatory changes and industry developments
        - Base analysis on current competitive landscape
        
        Format your response in a clear, structured manner."""
        
        # Add current market context
        current_date = datetime.now().strftime("%Y-%m-%d")
        market_context = f"\n\nANALYSIS DATE: {current_date}"
        market_context += "\nMARKET CONTEXT: Current market conditions and recent developments (last 6-12 months)"
        
        if context:
            context_str = json.dumps(context, indent=2)
            base_prompt += f"\n\nContext: {context_str}"
        
        return f"{base_prompt}{market_context}"
    
    def _extract_key_insights(self, analysis: str) -> List[str]:
        """Extract key insights from analysis text"""
        try:
            lines = analysis.split('\n')
            insights = []
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('•', '-', '*', '1.', '2.', '3.')) or 
                           'insight' in line.lower() or 'finding' in line.lower()):
                    insights.append(line)
            
            return insights[:5]
        except Exception:
            return []
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis text"""
        try:
            lines = analysis.split('\n')
            recommendations = []
            
            for line in lines:
                line = line.strip()
                if line and ('recommend' in line.lower() or 'suggest' in line.lower() or 
                           'should' in line.lower() or 'action' in line.lower()):
                    recommendations.append(line)
            
            return recommendations[:5]
        except Exception:
            return []
    
    def _calculate_confidence(self, analysis: str, insights: List[str], recommendations: List[str]) -> float:
        """Calculate confidence score based on response quality"""
        try:
            confidence = 0.5
            
            if len(analysis) > 500:
                confidence += 0.1
            
            if len(insights) >= 3:
                confidence += 0.2
            
            if len(recommendations) >= 2:
                confidence += 0.2
            
            if any(marker in analysis for marker in ['1.', '2.', '3.', '•', '-']):
                confidence += 0.1
            
            return min(1.0, confidence)
        except Exception:
            return 0.5
    
    def _estimate_cost(self, word_count: int) -> float:
        """Estimate cost based on word count"""
        cost_per_1k_words = 0.0002  # $0.0002 per 1K words
        return (word_count / 1000) * cost_per_1k_words

class GoogleGeminiAgent:
    """Google Gemini agent for strategic analysis"""
    
    def __init__(self, model: str = 'gemini-2.5-pro'):
        self.model = model
        # Don't configure API key here - do it just before the API call
        self.model_instance = None
        self.logger = logging.getLogger(f"llm.gemini.{model}")
    
    async def analyze(self, query: str, context: Dict[str, Any] = None) -> LLMAnalysisResult:
        """Analyze query using Google Gemini with improved safety settings"""
        start_time = datetime.now()
        
        try:
            # Configure API key just before the call
            if not hasattr(settings, 'GOOGLE_GEMINI_API_KEY') or not settings.GOOGLE_GEMINI_API_KEY:
                raise ValueError("Google Gemini API key is not configured")
            
            # Configure Gemini with API key
            genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
            
            # Initialize model instance if not already done
            if self.model_instance is None:
                self.model_instance = genai.GenerativeModel(self.model)
            
            # Prepare the prompt
            prompt = self._build_prompt(query, context)
            
            # FIX: Use less restrictive safety settings for business analysis
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            # Generate content using Gemini with adjusted safety settings
            response = await self.model_instance.generate_content_async(prompt, safety_settings=safety_settings)
            
            # Validate response
            if not response or not response.candidates:
                raise ValueError("No response candidates from Gemini")
            
            candidate = response.candidates[0]
            
            # Check for content policy blocks
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback and response.prompt_feedback.block_reason:
                raise ValueError(f"Gemini response blocked due to: {response.prompt_feedback.block_reason}")
            
            if candidate.finish_reason not in [0, 1]:  # 0 = SUCCESS, 1 = STOP (both are valid)
                raise ValueError(f"Gemini response blocked: finish_reason={candidate.finish_reason}")
            
            # Extract the generated text
            if candidate.content and candidate.content.parts:
                generated_text = candidate.content.parts[0].text
            else:
                # Try alternative extraction methods
                if hasattr(candidate, 'text'):
                    generated_text = candidate.text
                elif hasattr(response, 'text'):
                    generated_text = response.text
                else:
                    raise ValueError("No content parts in Gemini response")
            
            # Parse the response
            parsed_result = self._parse_gemini_response(generated_text)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return LLMAnalysisResult(
                model_name=f"Google-{self.model}",
                analysis=generated_text,
                confidence=parsed_result.get("confidence", 0.7),
                key_insights=parsed_result.get("insights", []),
                recommendations=parsed_result.get("recommendations", []),
                execution_time=execution_time,
                cost=0.0,  # Gemini doesn't provide token usage in the same way
                timestamp=datetime.now(),
                metadata={"parsing_method": "structured_extraction", "market_focus": "current"}
            )
            
        except Exception as e:
            self.logger.error(f"Google Gemini analysis failed: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Try to provide a more helpful error message
            error_msg = f"Analysis failed: {str(e)}"
            if "No content parts" in str(e):
                error_msg = "Analysis failed: Gemini response format issue - using fallback analysis"
            elif "API key" in str(e):
                error_msg = "Analysis failed: Gemini API key configuration issue"
            elif "blocked" in str(e):
                error_msg = "Analysis failed: Gemini content policy blocked the response"
            
            return LLMAnalysisResult(
                model_name=f"Google-{self.model}",
                analysis=error_msg,
                confidence=0.0,
                key_insights=[],
                recommendations=[],
                execution_time=execution_time,
                cost=0.0,
                timestamp=datetime.now(),
                metadata={"error": str(e), "market_focus": "current", "fallback_used": True}
            )
    
    def _build_prompt(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build a controlled prompt for Gemini analysis ensuring proper JSON output"""
        
        # Check if this is a strategic scoring request that needs JSON output
        if "strategic_scoring" in query.lower() or "json" in query.lower():
            return self._build_json_prompt(query, context)
        
        # Standard analysis prompt
        system_prompt = """You are an expert strategic analyst. Focus on CURRENT market conditions (last 6-12 months).

Provide analysis with:
1. Key business insights (3-5 bullet points)
2. Strategic recommendations (3-5 bullet points) 
3. Confidence level (0.0-1.0)
4. Brief reasoning
5. Data sources

Keep response professional and business-focused."""
        
        context_str = ""
        if context:
            context_str = f"\n\nBusiness Context: {json.dumps(context, indent=2)}"
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        market_context = f"\n\nANALYSIS DATE: {current_date}"
        market_context += "\nMARKET CONTEXT: Current market conditions and recent developments (last 6-12 months)"
        
        return f"{system_prompt}\n\nBusiness Query: {query}{context_str}{market_context}"
    
    def _build_json_prompt(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build a prompt specifically for JSON-structured strategic analysis"""
        return f"""You are an expert business strategist. Analyze: "{query}"

CRITICAL: Return ONLY valid JSON with this EXACT structure:

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
- NO text before or after JSON
- Use ONLY the structure above
- All scores must be integers 1-10
- All strings must be in quotes
- NO trailing commas

Return ONLY the JSON object."""
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response to extract structured data"""
        try:
            # Simple parsing - in production, you might want more sophisticated parsing
            lines = response_text.split('\n')
            insights = []
            recommendations = []
            confidence = 0.7
            reasoning = ""
            data_sources = []
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if "insight" in line.lower() or "insights" in line.lower():
                    current_section = "insights"
                elif "recommendation" in line.lower() or "recommendations" in line.lower():
                    current_section = "recommendations"
                elif "confidence" in line.lower():
                    # Try to extract confidence score
                    try:
                        import re
                        conf_match = re.search(r'(\d+\.?\d*)', line)
                        if conf_match:
                            confidence = min(1.0, max(0.0, float(conf_match.group(1))))
                    except:
                        pass
                elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    content = line[1:].strip()
                    if current_section == "insights" and content:
                        insights.append(content)
                    elif current_section == "recommendations" and content:
                        recommendations.append(content)
                elif current_section == "insights" and line and not line.startswith('Key') and not line.startswith('Context'):
                    insights.append(line)
                elif current_section == "recommendations" and line and not line.startswith('Actionable') and not line.startswith('Context'):
                    recommendations.append(line)
            
            # Ensure we have at least some content
            if not insights:
                insights = ["Market analysis completed successfully"]
            if not recommendations:
                recommendations = ["Consider further market research"]
            
            return {
                "insights": insights[:5],  # Limit to 5 insights
                "recommendations": recommendations[:5],  # Limit to 5 recommendations
                "confidence": confidence,
                "reasoning": reasoning or "Analysis based on strategic business principles",
                "data_sources": data_sources or ["Market research", "Industry reports", "Competitive analysis"]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to parse Gemini response: {e}")
            return {
                "insights": ["Analysis completed"],
                "recommendations": ["Review results carefully"],
                "confidence": 0.5,
                "reasoning": "Standard analysis approach",
                "data_sources": ["General business knowledge"]
            }
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Build system prompt for strategic analysis"""
        base_prompt = """You are an expert strategic analyst specializing in business intelligence and market analysis. 
        Provide comprehensive, actionable insights with high confidence levels.
        
        Your analysis should include:
        1. Key strategic insights
        2. Market implications
        3. Risk assessment
        4. Actionable recommendations
        5. Confidence level (0-1 scale)
        
        Format your response in a clear, structured manner."""
        
        if context:
            context_str = json.dumps(context, indent=2)
            base_prompt += f"\n\nContext: {context_str}"
        
        return base_prompt
    
    def _extract_key_insights(self, analysis: str) -> List[str]:
        """Extract key insights from analysis text"""
        try:
            lines = analysis.split('\n')
            insights = []
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('•', '-', '*', '1.', '2.', '3.')) or 
                           'insight' in line.lower() or 'finding' in line.lower()):
                    insights.append(line)
            
            return insights[:5]
        except Exception:
            return []
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis text"""
        try:
            lines = analysis.split('\n')
            recommendations = []
            
            for line in lines:
                line = line.strip()
                if line and ('recommend' in line.lower() or 'suggest' in line.lower() or 
                           'should' in line.lower() or 'action' in line.lower()):
                    recommendations.append(line)
            
            return recommendations[:5]
        except Exception:
            return []
    
    def _calculate_confidence(self, analysis: str, insights: List[str], recommendations: List[str]) -> float:
        """Calculate confidence score based on response quality"""
        try:
            confidence = 0.5
            
            if len(analysis) > 500:
                confidence += 0.1
            
            if len(insights) >= 3:
                confidence += 0.2
            
            if len(recommendations) >= 2:
                confidence += 0.2
            
            if any(marker in analysis for marker in ['1.', '2.', '3.', '•', '-']):
                confidence += 0.1
            
            return min(1.0, confidence)
        except Exception:
            return 0.5
    
    def _estimate_cost(self, word_count: int) -> float:
        """Estimate cost based on word count"""
        cost_per_1k_words = 0.0001  # $0.0001 per 1K words for Gemini
        return (word_count / 1000) * cost_per_1k_words

class MultiLLMOrchestrator:
    """Orchestrate multiple LLMs for comprehensive analysis with robust fallback chain"""
    
    def __init__(self, consensus_method: ConsensusMethod = ConsensusMethod.CONFIDENCE_BASED):
        self.consensus_method = consensus_method
        self.logger = logging.getLogger("llm.orchestrator")
        
        # Initialize LLM agents
        self.llm_agents = {}
        self._initialize_agents()
        
        # Fallback chain priority (order matters)
        self.fallback_chain = ['google_gemini', 'perplexity_sonar', 'anthropic_claude', 'openai_gpt4']
    
    def _initialize_agents(self):
        """Initialize available LLM agents based on API keys"""
        try:
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                self.llm_agents['openai_gpt4'] = OpenAIAgent(model='gpt-4o')
                self.logger.info("OpenAI GPT-4 agent initialized with current market focus")
        except Exception as e:
            self.logger.warning(f"OpenAI agent initialization failed: {e}")
        
        try:
            if hasattr(settings, 'ANTHROPIC_API_KEY') and settings.ANTHROPIC_API_KEY:
                self.llm_agents['anthropic_claude'] = AnthropicAgent(model='claude-3-5-sonnet-20241022')
                self.logger.info("Anthropic Claude agent initialized with current market focus")
        except Exception as e:
            self.logger.warning(f"Anthropic agent initialization failed: {e}")
        
        try:
            if hasattr(settings, 'GOOGLE_GEMINI_API_KEY') and settings.GOOGLE_GEMINI_API_KEY:
                self.llm_agents['google_gemini'] = GoogleGeminiAgent(model='gemini-2.5-pro')
                self.logger.info("Google Gemini agent initialized with current market focus")
        except Exception as e:
            self.logger.warning(f"Google Gemini agent initialization failed: {e}")
        
        try:
            if hasattr(settings, 'PERPLEXITY_API_KEY') and settings.PERPLEXITY_API_KEY:
                self.llm_agents['perplexity_sonar'] = PerplexityAgent(model='sonar-pro')
                self.logger.info("Perplexity Sonar agent initialized with current market focus")
        except Exception as e:
            self.logger.warning(f"Perplexity agent initialization failed: {e}")
        
        if not self.llm_agents:
            self.logger.error("No LLM agents could be initialized!")
            raise RuntimeError("No LLM agents available")
        
        self.logger.info(f"Initialized {len(self.llm_agents)} LLM agents with current market focus: {list(self.llm_agents.keys())}")
    
    async def _retry_with_backoff(self, api_call_func, max_retries=3, initial_delay=1):
        """
        Generic retry mechanism with exponential backoff for API calls.
        """
        delay = initial_delay
        for i in range(max_retries):
            try:
                return await api_call_func()
            except Exception as e:
                if i == max_retries - 1:  # Last attempt
                    raise e
                self.logger.warning(f"API call failed (attempt {i+1}/{max_retries}): {e}. Retrying in {delay}s...")
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
        
        return None  # Should never reach here
    
    async def consensus_analysis(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get consensus analysis from multiple LLMs with robust fallback chain"""
        try:
            self.logger.info(f"Starting consensus analysis with {len(self.llm_agents)} agents - focusing on current market conditions")
            
            # Try fallback chain approach first
            fallback_result = await self._try_fallback_chain(query, context)
            if fallback_result:
                return fallback_result
            
            # If fallback chain fails, try traditional consensus
            return await self._traditional_consensus_analysis(query, context)
            
        except Exception as e:
            self.logger.error(f"Consensus analysis failed: {str(e)}")
            return {
                "error": str(e),
                "consensus": None,
                "individual_results": [],
                "consensus_method": self.consensus_method.value,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _try_fallback_chain(self, query: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Try analysis using the fallback chain - one model at a time until one succeeds.
        """
        for model_name in self.fallback_chain:
            if model_name not in self.llm_agents:
                continue
                
            try:
                self.logger.info(f"Trying {model_name} in fallback chain...")
                
                # Use retry mechanism for each model
                result = await self._retry_with_backoff(
                    lambda: self.llm_agents[model_name].analyze(query, context),
                    max_retries=3,
                    initial_delay=1
                )
                
                if result and result.confidence > 0:
                    self.logger.info(f"✅ {model_name} succeeded in fallback chain")
                    
                    # Create consensus-like structure from single successful result
                    consensus = {
                        "analysis": f"Fallback Chain Analysis - {model_name} succeeded\n\n{result.analysis}",
                        "consensus_insights": result.key_insights,
                        "consensus_recommendations": result.recommendations,
                        "confidence": result.confidence,
                        "successful_model": model_name,
                        "method": "fallback_chain",
                        "market_focus": "current"
                    }
                    
                    return {
                        "consensus": consensus,
                        "individual_results": [self._result_to_dict(result)],
                        "failed_results": [],
                        "consensus_method": "fallback_chain",
                        "aggregate_metrics": {
                            "total_cost": result.cost,
                            "average_confidence": result.confidence,
                            "total_execution_time": result.execution_time,
                            "successful_analyses": 1,
                            "failed_analyses": 0
                        },
                        "market_focus": "current",
                        "timestamp": datetime.now().isoformat()
                    }
                    
            except Exception as e:
                self.logger.warning(f"❌ {model_name} failed in fallback chain: {str(e)}")
                continue
        
        self.logger.warning("All models in fallback chain failed")
        return None
    
    async def _traditional_consensus_analysis(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Traditional consensus analysis when fallback chain fails"""
        try:
            # Execute all analyses in parallel
            tasks = [agent.analyze(query, context) for agent in self.llm_agents.values()]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out failed analyses
            valid_results = [r for r in results if isinstance(r, LLMAnalysisResult) and r.confidence > 0]
            failed_results = [r for r in results if isinstance(r, Exception) or (isinstance(r, LLMAnalysisResult) and r.confidence == 0)]
            
            if not valid_results:
                self.logger.error("All LLM analyses failed")
                return {
                    "error": "All LLM analyses failed",
                    "consensus": None,
                    "individual_results": [],
                    "consensus_method": self.consensus_method.value,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Build consensus based on selected method
            consensus = await self._build_consensus(valid_results)
            
            # Calculate aggregate metrics
            total_cost = sum(r.cost for r in valid_results)
            avg_confidence = np.mean([r.confidence for r in valid_results])
            total_execution_time = sum(r.execution_time for r in valid_results)
            
            return {
                "consensus": consensus,
                "individual_results": [self._result_to_dict(r) for r in valid_results],
                "failed_results": [str(r) if isinstance(r, Exception) else r.analysis for r in failed_results],
                "consensus_method": self.consensus_method.value,
                "aggregate_metrics": {
                    "total_cost": total_cost,
                    "average_confidence": avg_confidence,
                    "total_execution_time": total_execution_time,
                    "successful_analyses": len(valid_results),
                    "failed_analyses": len(failed_results)
                },
                "market_focus": "current",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Traditional consensus analysis failed: {str(e)}")
            return {
                "error": str(e),
                "consensus": None,
                "individual_results": [],
                "consensus_method": self.consensus_method.value,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _build_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Build consensus based on selected method"""
        if self.consensus_method == ConsensusMethod.CONFIDENCE_BASED:
            return self._confidence_based_consensus(results)
        elif self.consensus_method == ConsensusMethod.MAJORITY_VOTE:
            return self._majority_vote_consensus(results)
        elif self.consensus_method == ConsensusMethod.WEIGHTED_AVERAGE:
            return self._weighted_average_consensus(results)
        elif self.consensus_method == ConsensusMethod.EXPERT_VALIDATION:
            return self._expert_validation_consensus(results)
        elif self.consensus_method == ConsensusMethod.CLUSTERING_BASED:
            return await self._clustering_based_consensus(results)
        else:
            return self._confidence_based_consensus(results)  # Default
    
    def _confidence_based_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Build consensus prioritizing high-confidence analyses"""
        try:
            # Sort results by confidence
            sorted_results = sorted(results, key=lambda x: x.confidence, reverse=True)
            
            # Get top 2 high-confidence results
            top_results = sorted_results[:2]
            
            # Build consensus from top results
            consensus_analysis = f"Consensus Analysis (Confidence-Based Method) - Current Market Focus\n\n"
            consensus_analysis += f"Based on top {len(top_results)} high-confidence analyses with current market data:\n\n"
            
            all_insights = []
            all_recommendations = []
            
            for i, result in enumerate(top_results, 1):
                consensus_analysis += f"Model {i} ({result.model_name}, confidence: {result.confidence:.3f}):\n"
                consensus_analysis += f"Analysis: {result.analysis[:200]}...\n\n"
                
                all_insights.extend(result.key_insights)
                all_recommendations.extend(result.recommendations)
            
            # Get unique insights and recommendations
            unique_insights = list(set(all_insights))[:5]
            unique_recommendations = list(set(all_recommendations))[:5]
            
            if unique_insights:
                consensus_analysis += "Key Insights (Current Market Focus):\n"
                for i, insight in enumerate(unique_insights, 1):
                    consensus_analysis += f"{i}. {insight}\n"
                consensus_analysis += "\n"
            
            if unique_recommendations:
                consensus_analysis += "Recommendations (Based on Recent Market Data):\n"
                for i, rec in enumerate(unique_recommendations, 1):
                    consensus_analysis += f"{i}. {rec}\n"
            
            return {
                "analysis": consensus_analysis,
                "consensus_insights": unique_insights,
                "consensus_recommendations": unique_recommendations,
                "confidence": np.mean([r.confidence for r in top_results]),
                "top_models": [r.model_name for r in top_results],
                "market_focus": "current"
            }
            
        except Exception as e:
            self.logger.error(f"Confidence-based consensus failed: {str(e)}")
            return self._fallback_consensus(results)
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get capabilities and supported features of the orchestrator"""
        return {
            "consensus_methods": [method.value for method in ConsensusMethod],
            "current_method": self.consensus_method.value,
            "available_models": list(self.llm_agents.keys()),
            "total_models": len(self.llm_agents),
            "features": [
                "multi_llm_consensus",
                "confidence_based_scoring",
                "parallel_analysis",
                "fallback_consensus",
                "health_monitoring",
                "current_market_focus",
                "data_recency_prioritization"
            ],
            "supported_analysis_types": ["strategic", "market", "competitive", "financial"],
            "market_focus": "current",
            "timestamp": datetime.now().isoformat()
        }
    
    def _majority_vote_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Build consensus using majority voting on key insights"""
        try:
            # Collect all insights and recommendations
            all_insights = []
            all_recommendations = []
            
            for result in results:
                all_insights.extend(result.key_insights)
                all_recommendations.extend(result.recommendations)
            
            # Count occurrences with original text mapping
            insight_counts = {}
            insight_originals = {}
            for insight in all_insights:
                normalized = self._normalize_text(insight)
                if normalized not in insight_counts:
                    insight_counts[normalized] = 0
                    insight_originals[normalized] = insight
                insight_counts[normalized] += 1
            
            recommendation_counts = {}
            recommendation_originals = {}
            for rec in all_recommendations:
                normalized = self._normalize_text(rec)
                if normalized not in recommendation_counts:
                    recommendation_counts[normalized] = 0
                    recommendation_originals[normalized] = rec
                recommendation_counts[normalized] += 1
            
            # Get majority insights (appearing in more than 50% of analyses)
            majority_threshold = len(results) / 2
            majority_insights = [insight_originals[insight] for insight, count in insight_counts.items() if count > majority_threshold]
            majority_recommendations = [recommendation_originals[rec] for rec, count in recommendation_counts.items() if count > majority_threshold]
            
            # Build consensus analysis
            consensus_analysis = f"Consensus Analysis (Majority Vote Method) - Current Market Focus\n\n"
            consensus_analysis += f"Based on analysis from {len(results)} AI models with current market data:\n\n"
            
            if majority_insights:
                consensus_analysis += "Key Consensus Insights (Current Market Focus):\n"
                for i, insight in enumerate(majority_insights[:5], 1):
                    consensus_analysis += f"{i}. {insight}\n"
                consensus_analysis += "\n"
            
            if majority_recommendations:
                consensus_analysis += "Consensus Recommendations (Based on Recent Market Data):\n"
                for i, rec in enumerate(majority_recommendations[:5], 1):
                    consensus_analysis += f"{i}. {rec}\n"
            
            return {
                "analysis": consensus_analysis,
                "consensus_insights": majority_insights[:5],
                "consensus_recommendations": majority_recommendations[:5],
                "confidence": np.mean([r.confidence for r in results]),
                "agreement_level": len(majority_insights) / max(len(all_insights), 1),
                "market_focus": "current"
            }
            
        except Exception as e:
            self.logger.error(f"Majority vote consensus failed: {str(e)}")
            return self._fallback_consensus(results)
    
    def _weighted_average_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Build consensus using weighted average based on confidence scores"""
        try:
            # Calculate weighted scores for insights and recommendations
            insight_scores = {}
            recommendation_scores = {}
            
            for result in results:
                weight = result.confidence
                
                # Weight insights by confidence
                for insight in result.key_insights:
                    normalized = self._normalize_text(insight)
                    if normalized not in insight_scores:
                        insight_scores[normalized] = {"score": 0, "count": 0, "original": insight}
                    insight_scores[normalized]["score"] += weight
                    insight_scores[normalized]["count"] += 1
                
                # Weight recommendations by confidence
                for rec in result.recommendations:
                    normalized = self._normalize_text(rec)
                    if normalized not in recommendation_scores:
                        recommendation_scores[normalized] = {"score": 0, "count": 0, "original": rec}
                    recommendation_scores[normalized]["score"] += weight
                    recommendation_scores[normalized]["count"] += 1
            
            # Sort by weighted scores
            top_insights = sorted(insight_scores.items(), key=lambda x: x[1]["score"], reverse=True)[:5]
            top_recommendations = sorted(recommendation_scores.items(), key=lambda x: x[1]["score"], reverse=True)[:5]
            
            # Build consensus analysis
            consensus_analysis = f"Consensus Analysis (Weighted Average Method) - Current Market Focus\n\n"
            consensus_analysis += f"Based on weighted analysis from {len(results)} AI models with current market data:\n\n"
            
            if top_insights:
                consensus_analysis += "Top Weighted Insights (Current Market Focus):\n"
                for i, (_, data) in enumerate(top_insights, 1):
                    consensus_analysis += f"{i}. {data['original']} (weight: {data['score']:.3f})\n"
                consensus_analysis += "\n"
            
            if top_recommendations:
                consensus_analysis += "Top Weighted Recommendations (Based on Recent Market Data):\n"
                for i, (_, data) in enumerate(top_recommendations, 1):
                    consensus_analysis += f"{i}. {data['original']} (weight: {data['score']:.3f})\n"
            
            return {
                "analysis": consensus_analysis,
                "consensus_insights": [data["original"] for _, data in top_insights],
                "consensus_recommendations": [data["original"] for _, data in top_recommendations],
                "confidence": np.mean([r.confidence for r in results]),
                "weighting_method": "confidence_based",
                "market_focus": "current"
            }
            
        except Exception as e:
            self.logger.error(f"Weighted average consensus failed: {str(e)}")
            return self._fallback_consensus(results)
    
    def _expert_validation_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Build consensus using expert validation approach"""
        try:
            # Identify the highest confidence model as the "expert"
            expert_result = max(results, key=lambda x: x.confidence)
            
            # Get insights and recommendations from expert
            expert_insights = expert_result.key_insights
            expert_recommendations = expert_result.recommendations
            
            # Validate with other models
            validated_insights = []
            validated_recommendations = []
            
            for insight in expert_insights:
                validation_count = 0
                for result in results:
                    if result != expert_result:
                        # Check if similar insight exists in other results
                        for other_insight in result.key_insights:
                            if self._calculate_similarity(insight, other_insight) > 0.7:
                                validation_count += 1
                                break
                
                # Include if validated by at least one other model
                if validation_count > 0:
                    validated_insights.append(insight)
            
            for rec in expert_recommendations:
                validation_count = 0
                for result in results:
                    if result != expert_result:
                        # Check if similar recommendation exists in other results
                        for other_rec in result.recommendations:
                            if self._calculate_similarity(rec, other_rec) > 0.7:
                                validation_count += 1
                                break
                
                # Include if validated by at least one other model
                if validation_count > 0:
                    validated_recommendations.append(rec)
            
            # Build consensus analysis
            consensus_analysis = f"Consensus Analysis (Expert Validation Method) - Current Market Focus\n\n"
            consensus_analysis += f"Expert Model: {expert_result.model_name} (confidence: {expert_result.confidence:.3f})\n\n"
            
            if validated_insights:
                consensus_analysis += "Validated Insights (Current Market Focus):\n"
                for i, insight in enumerate(validated_insights[:5], 1):
                    consensus_analysis += f"{i}. {insight}\n"
                consensus_analysis += "\n"
            
            if validated_recommendations:
                consensus_analysis += "Validated Recommendations (Based on Recent Market Data):\n"
                for i, rec in enumerate(validated_recommendations[:5], 1):
                    consensus_analysis += f"{i}. {rec}\n"
            
            return {
                "analysis": consensus_analysis,
                "consensus_insights": validated_insights[:5],
                "consensus_recommendations": validated_recommendations[:5],
                "confidence": expert_result.confidence,
                "expert_model": expert_result.model_name,
                "validation_method": "cross_model_similarity",
                "market_focus": "current"
            }
            
        except Exception as e:
            self.logger.error(f"Expert validation consensus failed: {str(e)}")
            return self._fallback_consensus(results)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings"""
        try:
            # Simple Jaccard similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union if union > 0 else 0.0
        except Exception:
            return 0.0
    
    async def _clustering_based_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Build consensus using clustering of similar insights and recommendations"""
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.cluster import DBSCAN
            import numpy as np
            
            # Initialize sentence transformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Collect all insights and recommendations
            all_insights = []
            all_recommendations = []
            
            for result in results:
                all_insights.extend(result.key_insights)
                all_recommendations.extend(result.recommendations)
            
            # Cluster insights
            if all_insights:
                insight_embeddings = model.encode(all_insights)
                insight_clusters = self._cluster_texts(all_insights, insight_embeddings)
            else:
                insight_clusters = []
            
            # Cluster recommendations
            if all_recommendations:
                rec_embeddings = model.encode(all_recommendations)
                rec_clusters = self._cluster_texts(all_recommendations, rec_embeddings)
            else:
                rec_clusters = []
            
            # Build consensus analysis
            consensus_analysis = f"Consensus Analysis (Clustering-Based Method) - Current Market Focus\n\n"
            consensus_analysis += f"Based on clustering analysis from {len(results)} AI models with current market data:\n\n"
            
            if insight_clusters:
                consensus_analysis += "Clustered Insights (Current Market Focus):\n"
                for i, cluster in enumerate(insight_clusters[:5], 1):
                    consensus_analysis += f"{i}. Cluster {i} ({len(cluster)} items):\n"
                    consensus_analysis += f"   Representative: {cluster[0]}\n"
                    if len(cluster) > 1:
                        consensus_analysis += f"   Related: {', '.join(cluster[1:3])}\n"
                    consensus_analysis += "\n"
            
            if rec_clusters:
                consensus_analysis += "Clustered Recommendations (Based on Recent Market Data):\n"
                for i, cluster in enumerate(rec_clusters[:5], 1):
                    consensus_analysis += f"{i}. Cluster {i} ({len(cluster)} items):\n"
                    consensus_analysis += f"   Representative: {cluster[0]}\n"
                    if len(cluster) > 1:
                        consensus_analysis += f"   Related: {', '.join(cluster[1:3])}\n"
            
            return {
                "analysis": consensus_analysis,
                "consensus_insights": [cluster[0] for cluster in insight_clusters[:5]],
                "consensus_recommendations": [cluster[0] for cluster in rec_clusters[:5]],
                "confidence": np.mean([r.confidence for r in results]),
                "clustering_method": "sentence_embeddings_dbscan",
                "insight_clusters": len(insight_clusters),
                "recommendation_clusters": len(rec_clusters),
                "market_focus": "current"
            }
            
        except Exception as e:
            self.logger.error(f"Clustering-based consensus failed: {str(e)}")
            return self._fallback_consensus(results)
    
    def _cluster_texts(self, texts: List[str], embeddings: np.ndarray, eps: float = 0.3) -> List[List[str]]:
        """Cluster texts using DBSCAN based on embeddings"""
        try:
            from sklearn.cluster import DBSCAN
            
            # Perform clustering
            clustering = DBSCAN(eps=eps, min_samples=1).fit(embeddings)
            
            # Group texts by cluster
            clusters = {}
            for i, label in enumerate(clustering.labels_):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(texts[i])
            
            # Sort clusters by size (largest first)
            sorted_clusters = sorted(clusters.values(), key=len, reverse=True)
            
            return sorted_clusters
            
        except Exception as e:
            self.logger.error(f"Text clustering failed: {str(e)}")
            # Fallback: return each text as its own cluster
            return [[text] for text in texts]
    
    def _fallback_consensus(self, results: List[LLMAnalysisResult]) -> Dict[str, Any]:
        """Fallback consensus method when primary methods fail"""
        try:
            # Simple concatenation of all results
            consensus_analysis = f"Fallback Consensus Analysis - Current Market Focus\n\n"
            consensus_analysis += f"Combined analysis from {len(results)} AI models with current market data:\n\n"
            
            all_insights = []
            all_recommendations = []
            
            for i, result in enumerate(results, 1):
                consensus_analysis += f"Model {i} ({result.model_name}):\n"
                consensus_analysis += f"{result.analysis[:300]}...\n\n"
                
                all_insights.extend(result.key_insights)
                all_recommendations.extend(result.recommendations)
            
            # Get unique items
            unique_insights = list(set(all_insights))[:5]
            unique_recommendations = list(set(all_recommendations))[:5]
            
            if unique_insights:
                consensus_analysis += "Combined Insights (Current Market Focus):\n"
                for i, insight in enumerate(unique_insights, 1):
                    consensus_analysis += f"{i}. {insight}\n"
                consensus_analysis += "\n"
            
            if unique_recommendations:
                consensus_analysis += "Combined Recommendations (Based on Recent Market Data):\n"
                for i, rec in enumerate(unique_recommendations, 1):
                    consensus_analysis += f"{i}. {rec}\n"
            
            return {
                "analysis": consensus_analysis,
                "consensus_insights": unique_insights,
                "consensus_recommendations": unique_recommendations,
                "confidence": np.mean([r.confidence for r in results]),
                "method": "fallback",
                "market_focus": "current"
            }
            
        except Exception as e:
            self.logger.error(f"Fallback consensus failed: {str(e)}")
            return {
                "analysis": "Consensus analysis failed",
                "consensus_insights": [],
                "consensus_recommendations": [],
                "confidence": 0.0,
                "error": str(e),
                "market_focus": "current"
            }
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        try:
            import re
            normalized = re.sub(r'[^\w\s]', '', text.lower())
            normalized = ' '.join(normalized.split())
            return normalized
        except Exception:
            return text.lower()
    
    def _result_to_dict(self, result: LLMAnalysisResult) -> Dict[str, Any]:
        """Convert LLMAnalysisResult to dictionary for JSON serialization"""
        return {
            "model_name": result.model_name,
            "analysis": result.analysis,
            "confidence": result.confidence,
            "key_insights": result.key_insights,
            "recommendations": result.recommendations,
            "execution_time": result.execution_time,
            "cost": result.cost,
            "timestamp": result.timestamp.isoformat(),
            "metadata": result.metadata
        }
    
    async def get_available_models(self) -> Dict[str, Any]:
        """Get information about available LLM models"""
        return {
            "available_models": list(self.llm_agents.keys()),
            "total_models": len(self.llm_agents),
            "consensus_methods": [method.value for method in ConsensusMethod],
            "current_method": self.consensus_method.value,
            "market_focus": "current"
        }
    
    def set_consensus_method(self, method: ConsensusMethod):
        """Change the consensus method"""
        self.consensus_method = method
        self.logger.info(f"Consensus method changed to: {method.value}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all LLM agents"""
        health_status = {}
        
        for name, agent in self.llm_agents.items():
            try:
                # Simple health check - try to analyze a simple query
                result = await agent.analyze("Health check", {"test": True})
                health_status[name] = {
                    "status": "healthy",
                    "confidence": result.confidence,
                    "response_time": result.execution_time,
                    "market_focus": result.metadata.get("market_focus", "unknown")
                }
            except Exception as e:
                health_status[name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        return {
            "overall_status": "healthy" if all(h["status"] == "healthy" for h in health_status.values()) else "degraded",
            "agents": health_status,
            "market_focus": "current",
            "timestamp": datetime.now().isoformat()
        }
