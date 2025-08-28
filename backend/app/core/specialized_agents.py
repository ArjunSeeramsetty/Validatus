#!/usr/bin/env python3
"""
Specialized Strategic Analysis Agents with Persona-Based Analysis
Each agent specializes in specific domains with expert personas for comprehensive analysis
Enhanced with hierarchical context (Segment → Factor → Layer) for precise analysis
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from app.core.multi_llm_orchestrator import MultiLLMOrchestrator

logger = logging.getLogger(__name__)

class AnalysisDomain(Enum):
    """Analysis domains for specialized agents"""
    CONSUMER_INSIGHTS = "consumer_insights"
    MARKET_RESEARCH = "market_research"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    PRODUCT_STRATEGY = "product_strategy"
    BRAND_STRATEGY = "brand_strategy"
    UX_STRATEGY = "ux_strategy"
    FINANCIAL_ANALYSIS = "financial_analysis"
    TECHNICAL_ANALYSIS = "technical_analysis"
    TREND_ANALYSIS = "trend_analysis"
    RISK_ASSESSMENT = "risk_assessment"

@dataclass
class AgentPersona:
    """Persona configuration for specialized agents"""
    name: str
    expertise: str
    background: str
    analysis_style: str
    key_questions: List[str]
    methodology: str

class BaseSpecializedAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, domain: AnalysisDomain, persona: AgentPersona):
        self.domain = domain
        self.persona = persona
        self.llm_orchestrator = MultiLLMOrchestrator()
        self.logger = logging.getLogger(f"agent.{domain.value}")
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Base analysis method to be overridden by specialized agents"""
        raise NotImplementedError
        
    def _create_persona_prompt(self, layer_name: str, idea_description: str, 
                              target_audience: str, context: Dict[str, Any]) -> str:
        """Create persona-specific analysis prompt with full hierarchical context"""
        
        # Extract hierarchical context from the framework
        hierarchical_context = self._get_hierarchical_context(layer_name)
        
        prompt = f"""
You are {self.persona.name}, a {self.persona.expertise} with {self.persona.background}.

ANALYSIS TASK:
Analyze the strategic layer: "{layer_name}" for the business idea: "{idea_description}"
Target Audience: {target_audience}

HIERARCHICAL CONTEXT (CRITICAL FOR ACCURATE ANALYSIS):
{hierarchical_context}

YOUR EXPERTISE:
- {self.persona.analysis_style}
- {self.persona.methodology}

KEY QUESTIONS TO CONSIDER:
{chr(10).join(f"- {q}" for q in self.persona.key_questions)}

CONTEXT: {context}

ANALYSIS REQUIREMENTS:
1. Provide a comprehensive analysis from your expert perspective
2. Consider the specific context of the layer within its factor and segment
3. Focus your analysis on the precise scope defined by the hierarchical context
4. Consider industry best practices and current trends
5. Evaluate risks and opportunities specific to this layer's context
6. Provide actionable insights relevant to this specific strategic dimension
7. End with "Score: X/10" where X is your assessment (1-10 scale)

IMPORTANT: Your analysis should be specifically tailored to the "{layer_name}" layer within the context of "{hierarchical_context}". Do not provide generic analysis - be precise and contextual.

Your analysis should reflect your specialized expertise and professional background.
"""
        return prompt.strip()
    
    def _get_hierarchical_context(self, layer_name: str) -> str:
        """Get the full hierarchical context for a layer (Segment → Factor → Layer)"""
        try:
            # Import the framework to get hierarchical information
            from .comprehensive_analytical_framework_fixed import ComprehensiveAnalyticalFramework
            framework = ComprehensiveAnalyticalFramework()
            
            # Find which segment and factor this layer belongs to
            for segment_name, segment_data in framework.analytical_framework.items():
                for factor_name, layers in segment_data["factors"].items():
                    if layer_name in layers:
                        return f"Segment: {segment_name} → Factor: {factor_name} → Layer: {layer_name}"
            
            # If not found, return basic context
            return f"Layer: {layer_name}"
            
        except Exception as e:
            # Fallback if framework import fails
            return f"Layer: {layer_name}"

class ConsumerInsightsAgent(BaseSpecializedAgent):
    """Specialized agent for consumer behavior, psychology, and market research"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Dr. Sarah Chen",
            expertise="Consumer Psychology & Behavioral Economics",
            background="PhD in Consumer Psychology, 15+ years in market research, former McKinsey consultant",
            analysis_style="Data-driven consumer behavior analysis with psychological insights",
            key_questions=[
                "What are the underlying psychological drivers for this need?",
                "How does this fit into current consumer behavior patterns?",
                "What are the emotional and rational decision factors?",
                "How does this align with demographic and psychographic trends?",
                "What are the adoption barriers and enablers?"
            ],
            methodology="Mixed-method research combining quantitative surveys, qualitative interviews, and behavioral analytics"
        )
        super().__init__(AnalysisDomain.CONSUMER_INSIGHTS, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze consumer-focused layers with psychological insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "consumer_insights", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Consumer insights analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Consumer insights analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class MarketResearchAgent(BaseSpecializedAgent):
    """Specialized agent for market dynamics, trends, and competitive landscape"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Marcus Rodriguez",
            expertise="Market Intelligence & Competitive Strategy",
            background="MBA from Harvard, 20+ years in market research, former Bain & Company partner",
            analysis_style="Strategic market analysis with competitive intelligence focus",
            key_questions=[
                "What is the current market size and growth trajectory?",
                "Who are the key players and what are their strategies?",
                "What market forces and trends are driving change?",
                "What are the barriers to entry and market risks?",
                "How does this fit into the broader industry ecosystem?"
            ],
            methodology="Comprehensive market analysis using Porter's Five Forces, PESTEL analysis, and competitive intelligence"
        )
        super().__init__(AnalysisDomain.MARKET_RESEARCH, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market-focused layers with strategic intelligence"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "market_research", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Market research analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Market research analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class CompetitorAnalysisAgent(BaseSpecializedAgent):
    """Specialized agent for competitive analysis and positioning"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Alexandra Kim",
            expertise="Competitive Intelligence & Strategic Positioning",
            background="Former competitive intelligence director at Google, 18+ years in tech strategy",
            analysis_style="Deep competitive analysis with strategic positioning insights",
            key_questions=[
                "Who are the direct and indirect competitors?",
                "What are their strengths, weaknesses, and strategies?",
                "How does this differentiate from existing solutions?",
                "What competitive advantages can be developed?",
                "How might competitors respond to this entry?"
            ],
            methodology="Competitive benchmarking, SWOT analysis, and strategic positioning frameworks"
        )
        super().__init__(AnalysisDomain.COMPETITOR_ANALYSIS, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor-focused layers with strategic positioning insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "competitor_analysis", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Competitor analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Competitor analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class ProductStrategyAgent(BaseSpecializedAgent):
    """Specialized agent for product strategy and innovation"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Dr. James Wilson",
            expertise="Product Strategy & Innovation Management",
            background="PhD in Engineering, former VP of Product at Tesla, 25+ years in product development",
            analysis_style="Technical product analysis with innovation strategy focus",
            key_questions=[
                "What is the technical feasibility and innovation level?",
                "How does this compare to existing product offerings?",
                "What are the key differentiators and unique features?",
                "How scalable and maintainable is this solution?",
                "What are the technical risks and mitigation strategies?"
            ],
            methodology="Product lifecycle analysis, innovation assessment, and technical feasibility evaluation"
        )
        super().__init__(AnalysisDomain.PRODUCT_STRATEGY, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze product-focused layers with technical and strategic insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "product_strategy", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Product strategy analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Product strategy analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class BrandStrategyAgent(BaseSpecializedAgent):
    """Specialized agent for brand strategy and positioning"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Isabella Santos",
            expertise="Brand Strategy & Marketing Communications",
            background="Former CMO at Nike, 22+ years in brand building, MBA from Stanford",
            analysis_style="Brand positioning analysis with marketing strategy insights",
            key_questions=[
                "What is the brand positioning and differentiation strategy?",
                "How does this align with target audience values?",
                "What are the brand equity and recognition opportunities?",
                "How can this build emotional connection and loyalty?",
                "What are the brand communication and marketing strategies?"
            ],
            methodology="Brand positioning frameworks, equity analysis, and marketing strategy development"
        )
        super().__init__(AnalysisDomain.BRAND_STRATEGY, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze brand-focused layers with strategic positioning insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "brand_strategy", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Brand strategy analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Brand strategy analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class UXStrategyAgent(BaseSpecializedAgent):
    """Specialized agent for user experience and design strategy"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Dr. Maya Patel",
            expertise="User Experience Design & Human-Computer Interaction",
            background="PhD in HCI, former Head of UX at Apple, 20+ years in design strategy",
            analysis_style="User-centered design analysis with experience strategy focus",
            key_questions=[
                "How intuitive and user-friendly is this solution?",
                "What are the key user touchpoints and journey mapping?",
                "How does this address user pain points and needs?",
                "What are the accessibility and inclusivity considerations?",
                "How can this create memorable and engaging experiences?"
            ],
            methodology="User research, journey mapping, usability testing, and design thinking frameworks"
        )
        super().__init__(AnalysisDomain.UX_STRATEGY, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze UX-focused layers with design strategy insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "ux_strategy", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"UX strategy analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"UX strategy analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class FinancialAnalysisAgent(BaseSpecializedAgent):
    """Specialized agent for financial analysis and business model evaluation"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Robert Chang",
            expertise="Financial Analysis & Business Model Strategy",
            background="CFA, former investment banker at Goldman Sachs, 18+ years in financial analysis",
            analysis_style="Financial modeling with business model strategy insights",
            key_questions=[
                "What is the revenue model and pricing strategy?",
                "What are the cost structure and profitability drivers?",
                "How scalable and sustainable is the business model?",
                "What are the key financial risks and opportunities?",
                "How does this compare to industry benchmarks?"
            ],
            methodology="Financial modeling, business model canvas, and investment analysis frameworks"
        )
        super().__init__(AnalysisDomain.FINANCIAL_ANALYSIS, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial-focused layers with business model insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "financial_analysis", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Financial analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Financial analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class TechnicalAnalysisAgent(BaseSpecializedAgent):
    """Specialized agent for technical feasibility and innovation assessment"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Dr. Elena Kovac",
            expertise="Technical Architecture & Innovation Assessment",
            background="PhD in Computer Science, former CTO at Microsoft, 25+ years in technology strategy",
            analysis_style="Technical feasibility analysis with innovation strategy focus",
            key_questions=[
                "What is the technical architecture and scalability?",
                "How innovative and cutting-edge is this technology?",
                "What are the technical risks and implementation challenges?",
                "How does this integrate with existing systems?",
                "What are the technology trends and future-proofing considerations?"
            ],
            methodology="Technical architecture review, innovation assessment, and risk analysis frameworks"
        )
        super().__init__(AnalysisDomain.TECHNICAL_ANALYSIS, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical-focused layers with innovation insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "technical_analysis", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Technical analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Technical analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class TrendAnalysisAgent(BaseSpecializedAgent):
    """Specialized agent for trend analysis and future forecasting"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Dr. Marcus Thompson",
            expertise="Trend Analysis & Future Forecasting",
            background="PhD in Futures Studies, former director at Institute for the Future, 20+ years in trend analysis",
            analysis_style="Future-oriented trend analysis with strategic foresight",
            key_questions=[
                "What are the current and emerging trends in this space?",
                "How does this align with future market directions?",
                "What are the disruptive forces and paradigm shifts?",
                "How can this future-proof the business strategy?",
                "What are the long-term sustainability and adaptation considerations?"
            ],
            methodology="Trend analysis, scenario planning, and strategic foresight frameworks"
        )
        super().__init__(AnalysisDomain.TREND_ANALYSIS, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trend-focused layers with future forecasting insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "trend_analysis", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Trend analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Trend analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class RiskAssessmentAgent(BaseSpecializedAgent):
    """Specialized agent for risk assessment and mitigation strategy"""
    
    def __init__(self):
        persona = AgentPersona(
            name="Dr. Sarah Johnson",
            expertise="Risk Management & Strategic Risk Assessment",
            background="PhD in Risk Management, former Chief Risk Officer at JPMorgan, 22+ years in risk strategy",
            analysis_style="Comprehensive risk analysis with mitigation strategy focus",
            key_questions=[
                "What are the key strategic, operational, and market risks?",
                "How likely and impactful are these risks?",
                "What are the risk mitigation and contingency strategies?",
                "How does this compare to industry risk benchmarks?",
                "What are the emerging and evolving risk factors?"
            ],
            methodology="Risk assessment frameworks, scenario analysis, and mitigation strategy development"
        )
        super().__init__(AnalysisDomain.RISK_ASSESSMENT, persona)
        
    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk-focused layers with mitigation strategy insights"""
        prompt = self._create_persona_prompt(layer_name, idea_description, target_audience, context)
        
        try:
            # Add timeout and better error handling
            analysis_result = await asyncio.wait_for(
                self.llm_orchestrator.consensus_analysis(
                    query=prompt,
                    context={"agent_type": "risk_assessment", "persona": self.persona.name}
                ),
                timeout=120.0  # 2 minute timeout
            )
            
            return {
                "agent": self.domain.value,
                "persona": self.persona.name,
                "analysis": analysis_result,
                "methodology": self.persona.methodology
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Risk assessment analysis timed out for {layer_name}")
            return {"error": "Analysis timed out", "agent": self.domain.value}
        except Exception as e:
            self.logger.error(f"Risk assessment analysis failed for {layer_name}: {e}")
            return {"error": str(e), "agent": self.domain.value}

class SpecializedAgentOrchestrator:
    """Orchestrates multiple specialized agents for comprehensive analysis"""
    
    def __init__(self):
        self.agents = {
            AnalysisDomain.CONSUMER_INSIGHTS: ConsumerInsightsAgent(),
            AnalysisDomain.MARKET_RESEARCH: MarketResearchAgent(),
            AnalysisDomain.COMPETITOR_ANALYSIS: CompetitorAnalysisAgent(),
            AnalysisDomain.PRODUCT_STRATEGY: ProductStrategyAgent(),
            AnalysisDomain.BRAND_STRATEGY: BrandStrategyAgent(),
            AnalysisDomain.UX_STRATEGY: UXStrategyAgent(),
            AnalysisDomain.FINANCIAL_ANALYSIS: FinancialAnalysisAgent(),
            AnalysisDomain.TECHNICAL_ANALYSIS: TechnicalAnalysisAgent(),
            AnalysisDomain.TREND_ANALYSIS: TrendAnalysisAgent(),
            AnalysisDomain.RISK_ASSESSMENT: RiskAssessmentAgent()
        }
        
        # Layer to agent mapping for optimal analysis
        self.layer_agent_mapping = {
            # Consumer layers
            "need_perception": AnalysisDomain.CONSUMER_INSIGHTS,
            "purchase_intent": AnalysisDomain.CONSUMER_INSIGHTS,
            "emotional_pull": AnalysisDomain.CONSUMER_INSIGHTS,
            "trust_level": AnalysisDomain.CONSUMER_INSIGHTS,
            "loyalty_metrics": AnalysisDomain.CONSUMER_INSIGHTS,
            "adoption_patterns": AnalysisDomain.CONSUMER_INSIGHTS,
            
            # Market layers
            "market_size": AnalysisDomain.MARKET_RESEARCH,
            "growth_rate": AnalysisDomain.MARKET_RESEARCH,
            "market_trends": AnalysisDomain.MARKET_RESEARCH,
            "regulatory_environment": AnalysisDomain.MARKET_RESEARCH,
            "economic_factors": AnalysisDomain.MARKET_RESEARCH,
            
            # Competitor layers
            "competitor_analysis": AnalysisDomain.COMPETITOR_ANALYSIS,
            "competitive_positioning": AnalysisDomain.COMPETITOR_ANALYSIS,
            "market_share": AnalysisDomain.COMPETITOR_ANALYSIS,
            "competitive_advantages": AnalysisDomain.COMPETITOR_ANALYSIS,
            
            # Product layers
            "product_features": AnalysisDomain.PRODUCT_STRATEGY,
            "innovation_level": AnalysisDomain.PRODUCT_STRATEGY,
            "technical_feasibility": AnalysisDomain.TECHNICAL_ANALYSIS,
            "quality_metrics": AnalysisDomain.PRODUCT_STRATEGY,
            "differentiation": AnalysisDomain.PRODUCT_STRATEGY,
            
            # Brand layers
            "brand_positioning": AnalysisDomain.BRAND_STRATEGY,
            "brand_equity": AnalysisDomain.BRAND_STRATEGY,
            "marketing_strategy": AnalysisDomain.BRAND_STRATEGY,
            "brand_awareness": AnalysisDomain.BRAND_STRATEGY,
            
            # Experience layers
            "user_experience": AnalysisDomain.UX_STRATEGY,
            "usability": AnalysisDomain.UX_STRATEGY,
            "design_quality": AnalysisDomain.UX_STRATEGY,
            "customer_satisfaction": AnalysisDomain.UX_STRATEGY,
            
            # Financial layers
            "revenue_model": AnalysisDomain.FINANCIAL_ANALYSIS,
            "cost_structure": AnalysisDomain.FINANCIAL_ANALYSIS,
            "profitability": AnalysisDomain.FINANCIAL_ANALYSIS,
            "financial_risks": AnalysisDomain.RISK_ASSESSMENT,
            
            # Risk layers
            "operational_risks": AnalysisDomain.RISK_ASSESSMENT,
            "market_risks": AnalysisDomain.RISK_ASSESSMENT,
            "strategic_risks": AnalysisDomain.RISK_ASSESSMENT,
            
            # Trend layers
            "industry_trends": AnalysisDomain.TREND_ANALYSIS,
            "technology_trends": AnalysisDomain.TREND_ANALYSIS,
            "consumer_trends": AnalysisDomain.TREND_ANALYSIS
        }
        
    def get_optimal_agent(self, layer_name: str) -> BaseSpecializedAgent:
        """Get the optimal agent for analyzing a specific layer"""
        # Try exact match first
        if layer_name in self.layer_agent_mapping:
            return self.agents[self.layer_agent_mapping[layer_name]]
        
        # Try partial matching based on keywords
        layer_lower = layer_name.lower()
        
        if any(keyword in layer_lower for keyword in ['consumer', 'user', 'customer', 'need', 'behavior']):
            return self.agents[AnalysisDomain.CONSUMER_INSIGHTS]
        elif any(keyword in layer_lower for keyword in ['market', 'industry', 'growth', 'trend']):
            return self.agents[AnalysisDomain.MARKET_RESEARCH]
        elif any(keyword in layer_lower for keyword in ['competitor', 'competition', 'positioning']):
            return self.agents[AnalysisDomain.COMPETITOR_ANALYSIS]
        elif any(keyword in layer_lower for keyword in ['product', 'feature', 'innovation']):
            return self.agents[AnalysisDomain.PRODUCT_STRATEGY]
        elif any(keyword in layer_lower for keyword in ['brand', 'marketing', 'awareness']):
            return self.agents[AnalysisDomain.BRAND_STRATEGY]
        elif any(keyword in layer_lower for keyword in ['experience', 'design', 'usability']):
            return self.agents[AnalysisDomain.UX_STRATEGY]
        elif any(keyword in layer_lower for keyword in ['financial', 'revenue', 'cost', 'profit']):
            return self.agents[AnalysisDomain.FINANCIAL_ANALYSIS]
        elif any(keyword in layer_lower for keyword in ['technical', 'technology', 'architecture']):
            return self.agents[AnalysisDomain.TECHNICAL_ANALYSIS]
        elif any(keyword in layer_lower for keyword in ['trend', 'future', 'forecast']):
            return self.agents[AnalysisDomain.TREND_ANALYSIS]
        elif any(keyword in layer_lower for keyword in ['risk', 'threat', 'vulnerability']):
            return self.agents[AnalysisDomain.RISK_ASSESSMENT]
        else:
            # Default to market research for general analysis
            return self.agents[AnalysisDomain.MARKET_RESEARCH]
    
    async def analyze_layer_with_optimal_agent(self, layer_name: str, idea_description: str,
                                              target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a layer using the optimal specialized agent"""
        agent = self.get_optimal_agent(layer_name)
        
        logger.info(f"🎯 Using {agent.persona.name} ({agent.domain.value}) for layer: {layer_name}")
        
        result = await agent.analyze_layer(layer_name, idea_description, target_audience, context)
        
        # Add agent metadata to result
        result["optimal_agent"] = {
            "domain": agent.domain.value,
            "persona": agent.persona.name,
            "expertise": agent.persona.expertise,
            "methodology": agent.persona.methodology
        }
        
        return result
    
    async def analyze_multiple_layers(self, layer_names: List[str], idea_description: str,
                                     target_audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze multiple layers using optimal agents in parallel"""
        tasks = []
        for layer_name in layer_names:
            task = self.analyze_layer_with_optimal_agent(layer_name, idea_description, target_audience, context)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle any exceptions
        processed_results = {}
        for i, result in enumerate(results):
            layer_name = layer_names[i]
            if isinstance(result, Exception):
                processed_results[layer_name] = {"error": str(result), "agent": "unknown"}
            else:
                processed_results[layer_name] = result
        
        return processed_results

# Convenience functions for easy access
def get_specialized_agent_orchestrator() -> SpecializedAgentOrchestrator:
    """Get a configured specialized agent orchestrator"""
    return SpecializedAgentOrchestrator()

def get_agent_by_domain(domain: AnalysisDomain) -> BaseSpecializedAgent:
    """Get a specific agent by domain"""
    orchestrator = get_specialized_agent_orchestrator()
    return orchestrator.agents[domain]
