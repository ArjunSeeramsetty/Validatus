import asyncio
from typing import Any, Dict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import openai
from datetime import datetime
import uuid

from .state import ValidatusState, AnalysisStatus, ResearchTask
from .analytical_structure import ANALYTICAL_FRAMEWORK, LAYER_TO_AGENT_MAP
from ..agents import (
    MarketResearchAgent, ConsumerInsightsAgent, CompetitorAnalysisAgent,
    TrendAnalysisAgent, PricingResearchAgent
)
from ..scoring.layer_scorers import LayerScoringEngine
from ..scoring.aggregators import ScoreAggregator
from ..utils.nlp import QueryParser
from config import settings

class ValidatusWorkflow:
    def __init__(self):
        self.agents = {
            'market_research': MarketResearchAgent(),
            'consumer_insights': ConsumerInsightsAgent(),
            'competitor_analysis': CompetitorAnalysisAgent(),
            'trend_analysis': TrendAnalysisAgent(),
            'pricing_research': PricingResearchAgent()
        }
        self.query_parser = QueryParser()
        self.scoring_engine = LayerScoringEngine()
        self.aggregator = ScoreAggregator()
        
    def build_workflow(self):
        """Build and return the complete Validatus workflow"""
        workflow = StateGraph(ValidatusState)
        
        # Add nodes
        workflow.add_node("parse_query", self.parse_query)
        workflow.add_node("plan_research", self.plan_research)
        workflow.add_node("execute_research", self.execute_research)
        workflow.add_node("score_layers", self.score_layers)
        workflow.add_node("aggregate_scores", self.aggregate_scores)
        workflow.add_node("generate_insights", self.generate_insights)
        workflow.add_node("create_dashboard", self.create_dashboard)
        
        # Add edges
        workflow.add_edge(START, "parse_query")
        workflow.add_edge("parse_query", "plan_research")
        workflow.add_edge("plan_research", "execute_research")
        workflow.add_edge("execute_research", "score_layers")
        workflow.add_edge("score_layers", "aggregate_scores")
        workflow.add_edge("aggregate_scores", "generate_insights")
        workflow.add_edge("generate_insights", "create_dashboard")
        workflow.add_edge("create_dashboard", END)
        
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    async def _update_state(self, state: ValidatusState, updates: Dict[str, Any]) -> ValidatusState:
        """Helper to update state and handle potential errors."""
        try:
            state.update(updates)
        except Exception as e:
            error_message = f"State update failed: {str(e)}"
            state["errors"] = state.get("errors", []) + [error_message]
            state["status"] = AnalysisStatus.FAILED
        return state

    async def parse_query(self, state: ValidatusState) -> Dict[str, Any]:
        """Parse user query and extract key entities"""
        try:
            interpretation = await self.query_parser.parse(
                query=state["user_query"],
                context=state["analysis_context"]
            )
            return {
                "query_interpretation": interpretation,
                "status": AnalysisStatus.PARSING,
                "progress": 10
            }
        except Exception as e:
            return {
                "errors": [f"Query parsing failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    async def plan_research(self, state: ValidatusState) -> Dict[str, Any]:
        """Create detailed research plan for all required layers"""
        try:
            research_tasks = []
            for segment, segment_data in ANALYTICAL_FRAMEWORK.items():
                for factor, layers in segment_data["factors"].items():
                    for layer in layers:
                        agent_type = LAYER_TO_AGENT_MAP.get(layer, segment_data["agent"])
                        task = ResearchTask(
                            agent_type=agent_type,
                            segment=segment,
                            factor=factor,
                            layer=layer,
                            query=self._create_layer_query(layer, state["query_interpretation"]),
                            context=state["analysis_context"]
                        )
                        research_tasks.append(task)
            
            return {
                "research_tasks": research_tasks,
                "status": AnalysisStatus.PLANNING,
                "progress": 20
            }
        except Exception as e:
            return {
                "errors": state.get("errors", []) + [f"Research planning failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    async def execute_research(self, state: ValidatusState) -> Dict[str, Any]:
        """Execute all research tasks in parallel"""
        try:
            research_tasks = state["research_tasks"]
            
            coroutines = []
            for task in research_tasks:
                agent = self.agents.get(task["agent_type"])
                if agent:
                    coroutine = agent.research(task["query"], task["context"])
                    coroutines.append(coroutine)
            
            results = await asyncio.gather(*coroutines, return_exceptions=True)
            
            research_results = {}
            errors = state.get("errors", [])
            for i, result in enumerate(results):
                task = research_tasks[i]
                layer_key = f"{task['segment']}.{task['factor']}.{task['layer']}"
                if isinstance(result, Exception):
                    errors.append(f"Research task for '{layer_key}' failed: {str(result)}")
                    research_results[layer_key] = {"data": None, "error": str(result)}
                else:
                    research_results[layer_key] = {
                        "data": result,
                        "agent": task["agent_type"],
                        "timestamp": datetime.utcnow().isoformat()
                    }
            
            return {
                "research_results": research_results,
                "status": AnalysisStatus.RESEARCHING,
                "progress": 50,
                "errors": errors
            }
        except Exception as e:
            return {
                "errors": state.get("errors", []) + [f"Research execution failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    async def score_layers(self, state: ValidatusState) -> Dict[str, Any]:
        """Calculate scores for all layers"""
        try:
            layer_scores = {}
            research_results = state["research_results"]
            errors = state.get("errors", [])
            
            for layer_key, research_data in research_results.items():
                if research_data.get("error"):
                    continue  # Skip scoring for failed research tasks

                segment, factor, layer = layer_key.split('.')
                
                score_result = await self.scoring_engine.calculate_layer_score(
                    layer_name=layer,
                    research_data=research_data.get("data", {}),
                    context=state["analysis_context"]
                )
                
                if "error" in score_result:
                    errors.append(f"Scoring for '{layer_key}' failed: {score_result['error']}")
                
                if segment not in layer_scores:
                    layer_scores[segment] = {}
                if factor not in layer_scores[segment]:
                    layer_scores[segment][factor] = {}
                    
                layer_scores[segment][factor][layer] = score_result
            
            return {
                "layer_scores": layer_scores,
                "status": AnalysisStatus.SCORING,
                "progress": 70,
                "errors": errors
            }
        except Exception as e:
            return {
                "errors": state.get("errors", []) + [f"Layer scoring failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    async def aggregate_scores(self, state: ValidatusState) -> Dict[str, Any]:
        """Aggregate layer scores into factor and segment scores"""
        try:
            factor_scores = await self.aggregator.aggregate_factors(state["layer_scores"])
            segment_scores = await self.aggregator.aggregate_segments(factor_scores)

            return {
                "factor_scores": factor_scores,
                "segment_scores": segment_scores,
                "status": AnalysisStatus.AGGREGATING,
                "progress": 85
            }
        except Exception as e:
            return {
                "errors": state.get("errors", []) + [f"Aggregation failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    async def generate_insights(self, state: ValidatusState) -> Dict[str, Any]:
        """Generate strategic insights and recommendations"""
        try:
            insights_prompt = self._create_insights_prompt(state)
            
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": insights_prompt}],
                temperature=0.5
            )
            
            insights = response.choices[0].message.content
            recommendations = self._parse_recommendations(insights)
            
            return {
                "recommendations": recommendations,
                "status": AnalysisStatus.SUMMARIZING,
                "progress": 95
            }
        except Exception as e:
            return {
                "errors": state.get("errors", []) + [f"Insights generation failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    async def create_dashboard(self, state: ValidatusState) -> Dict[str, Any]:
        """Create final dashboard data structure"""
        try:
            dashboard_data = {
                "analysis_id": state["analysis_id"],
                "query": state["user_query"],
                "context": state["analysis_context"],
                "segment_scores": state["segment_scores"],
                "factor_scores": state["factor_scores"],
                "layer_scores": state["layer_scores"],  # For drill-down
                "recommendations": state["recommendations"],
                "meta_scores": self._calculate_meta_scores(state),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return {
                "dashboard_data": dashboard_data,
                "status": AnalysisStatus.COMPLETED,
                "progress": 100
            }
        except Exception as e:
            return {
                "errors": state.get("errors", []) + [f"Dashboard creation failed: {str(e)}"],
                "status": AnalysisStatus.FAILED
            }

    def _create_layer_query(self, layer: str, interpretation: Dict) -> str:
        """Create a specific, detailed research query for a given layer."""
        product = interpretation.get("product_category", "the product")
        market = interpretation.get("geography", "the global market")
        audience = interpretation.get("target_audience", "consumers")
        
        # More detailed query generation
        query_templates = {
            "need_perception": f"Analyze consumer discussions, reviews, and forums to understand the perceived need for {product} among {audience} in {market}.",
            "purchase_intent": f"Investigate purchase intent signals for {product} targeting {audience}. Look for buying guides, 'best of' lists, and direct expressions of intent to buy.",
            "total_addressable_market": f"Estimate the Total Addressable Market (TAM) for {product} in {market}, including market size reports, and economic indicators.",
            "key_competitors": f"Identify the key competitors for {product} in {market}. Profile their main offerings, market positioning, and recent activities.",
            "unique_selling_proposition": f"Analyze the Unique Selling Proposition (USP) of {product}. What are its key differentiators compared to existing solutions for {audience}?",
            "onboarding_experience": f"Research user reviews and feedback on the onboarding experience for products similar to {product}."
        }
        return query_templates.get(layer, f"General market analysis for {layer.replace('_', ' ')} regarding {product} in {market}")

    def _parse_recommendations(self, insights: str) -> List[str]:
        """Parses LLM-generated text to extract a list of recommendations."""
        # Simple parsing logic; can be improved with more structured LLM output
        lines = insights.strip().split('\n')
        recommendations = [line.strip('- ').strip() for line in lines if line.strip().startswith('- ') or line.strip().startswith('* ')]
        return recommendations if recommendations else [insights]

    def _calculate_meta_scores(self, state: ValidatusState) -> Dict[str, float]:
        """Calculate high-level meta scores based on segment scores."""
        # This is a simplified example. A production system would use a more complex, weighted model.
        segment_scores = state.get("segment_scores", {})
        
        market_fit_score = (segment_scores.get("CONSUMER", {}).get("score", 50) + 
                            segment_scores.get("MARKET", {}).get("score", 50)) / 2
                            
        innovation_score = (segment_scores.get("PRODUCT", {}).get("score", 50) * 0.6 +
                            segment_scores.get("BRAND", {}).get("score", 50) * 0.4)

        return {
            "market_fit_score": round(market_fit_score, 2),
            "innovation_score": round(innovation_score, 2)
        }

    def _create_insights_prompt(self, state: ValidatusState) -> str:
        """Creates a detailed prompt for the final insights generation LLM call."""
        prompt = f"""
        Analyze the following strategic assessment for the user query: '{state['user_query']}' with context: {state['analysis_context']}.

        **Segment Scores:**
        {state.get('segment_scores', {})}

        **Factor Summaries:**
        """
        for segment, factors in state.get('factor_scores', {}).items():
            prompt += f"\n- {segment}:\n"
            for factor, data in factors.items():
                prompt += f"  - {factor}: {data.get('summary', 'N/A')}\n"

        prompt += """
        Based on this data, provide a concise executive summary and 3-5 actionable, strategic recommendations.
        Format the recommendations as a bulleted list starting with '- '.
        """
        return prompt
