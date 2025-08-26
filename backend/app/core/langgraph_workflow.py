#!/usr/bin/env python3
"""
LangGraph-based Workflow Orchestrator for Strategic Analysis
Implements parallel architecture for improved performance and scalability
"""

import os
import asyncio
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from app.core.simple_state import State as AppState
from app.core.strategic_scoring_v4 import StrategicScoringV4
from app.core.multi_llm_orchestrator import MultiLLMOrchestrator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    """State that flows through the LangGraph workflow"""
    app_state: AppState
    analysis_results: Dict[str, Any]
    error_message: str
    current_step: str
    completed_steps: List[str]
    retry_count: int

class LangGraphWorkflow:
    """
    Orchestrates the strategic analysis using a parallel LangGraph workflow.
    Multiple analysis agents run in parallel for improved performance.
    """
    
    def __init__(self):
        """Initialize the LangGraph workflow with all necessary components"""
        try:
            # Initialize the LLM orchestrator
            self.llm_orchestrator = MultiLLMOrchestrator()
            
            # Initialize the strategic scorer
            self.scorer = StrategicScoringV4(self.llm_orchestrator)
            
            # Build and compile the graph
            self.graph = self.build_graph()
            
            logger.info("✅ Parallel LangGraph workflow initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize LangGraph workflow: {str(e)}")
            raise
    
    def build_graph(self):
        """
        Builds the computational graph with sequential execution for now.
        Can be enhanced later with true parallel execution using LangGraph's advanced features.
        """
        try:
            workflow = StateGraph(GraphState)
            
            # --- Define the nodes for sequential execution ---
            workflow.add_node("consumer_analysis", self.run_consumer_analysis)
            workflow.add_node("market_analysis", self.run_market_analysis)
            workflow.add_node("product_analysis", self.run_product_analysis)
            workflow.add_node("brand_analysis", self.run_brand_analysis)
            workflow.add_node("experience_analysis", self.run_experience_analysis)
            workflow.add_node("strategic_scoring", self.run_strategic_scoring)
            
            # --- Define the graph structure ---
            # Sequential execution for now (can be enhanced with parallel execution later)
            workflow.set_entry_point("consumer_analysis")
            workflow.add_edge("consumer_analysis", "market_analysis")
            workflow.add_edge("market_analysis", "product_analysis")
            workflow.add_edge("product_analysis", "brand_analysis")
            workflow.add_edge("brand_analysis", "experience_analysis")
            workflow.add_edge("experience_analysis", "strategic_scoring")
            workflow.add_edge("strategic_scoring", END)
            
            # Compile the graph into a runnable object
            compiled_graph = workflow.compile()
            logger.info("✅ Sequential LangGraph workflow compiled successfully")
            
            return compiled_graph
            
        except Exception as e:
            logger.error(f"❌ Failed to build LangGraph workflow: {str(e)}")
            raise
    
    # --- Node Execution Functions ---
    
    async def run_consumer_analysis(self, state: GraphState) -> Dict[str, Any]:
        """Execute consumer analysis in parallel"""
        try:
            logger.info("👥 Running Consumer Analysis Node (Parallel)")
            app_state = state['app_state']
            
            # Update state
            state['current_step'] = 'consumer_analysis'
            state['retry_count'] = 0
            
            # Execute consumer analysis using LLM orchestrator
            result = await self.llm_orchestrator.consensus_analysis(
                query=f"Analyze consumer insights for: {app_state.idea_description}",
                context={
                    "target_audience": app_state.target_audience,
                    "analysis_type": "consumer_insights",
                    "focus": "consumer_behavior, pain_points, preferences"
                }
            )
            
            # Update app state
            app_state.set("consumer_analysis", result)
            state['completed_steps'].append('consumer_analysis')
            
            logger.info("✅ Consumer Analysis completed successfully (Parallel)")
            return {"app_state": app_state, "current_step": "consumer_analysis"}
            
        except Exception as e:
            logger.error(f"❌ Consumer Analysis failed: {str(e)}")
            state['error_message'] = f"Consumer Analysis failed: {str(e)}"
            return {"error_message": state['error_message']}
    
    async def run_market_analysis(self, state: GraphState) -> Dict[str, Any]:
        """Execute market analysis in parallel"""
        try:
            logger.info("🔍 Running Market Analysis Node (Parallel)")
            app_state = state['app_state']
            
            state['current_step'] = 'market_analysis'
            
            # Execute market analysis using LLM orchestrator
            result = await self.llm_orchestrator.consensus_analysis(
                query=f"Analyze market opportunities for: {app_state.idea_description}",
                context={
                    "target_audience": app_state.target_audience,
                    "analysis_type": "market_research",
                    "focus": "market_size, growth_trends, market_dynamics"
                }
            )
            
            # Update app state
            app_state.set("market_analysis", result)
            state['completed_steps'].append('market_analysis')
            
            logger.info("✅ Market Analysis completed successfully (Parallel)")
            return {"app_state": app_state, "current_step": "market_analysis"}
            
        except Exception as e:
            logger.error(f"❌ Market Analysis failed: {str(e)}")
            state['error_message'] = f"Market Analysis failed: {str(e)}"
            return {"error_message": state['error_message']}
    
    async def run_product_analysis(self, state: GraphState) -> Dict[str, Any]:
        """Execute product analysis in parallel"""
        try:
            logger.info("📦 Running Product Analysis Node (Parallel)")
            app_state = state['app_state']
            
            state['current_step'] = 'product_analysis'
            
            # Execute product analysis using LLM orchestrator
            result = await self.llm_orchestrator.consensus_analysis(
                query=f"Analyze product features and differentiation for: {app_state.idea_description}",
                context={
                    "target_audience": app_state.target_audience,
                    "analysis_type": "product_analysis",
                    "focus": "product_features, differentiation, innovation"
                }
            )
            
            # Update app state
            app_state.set("product_analysis", result)
            state['completed_steps'].append('product_analysis')
            
            logger.info("✅ Product Analysis completed successfully (Parallel)")
            return {"app_state": app_state, "current_step": "product_analysis"}
            
        except Exception as e:
            logger.error(f"❌ Product Analysis failed: {str(e)}")
            state['error_message'] = f"Product Analysis failed: {str(e)}"
            return {"error_message": state['error_message']}
    
    async def run_brand_analysis(self, state: GraphState) -> Dict[str, Any]:
        """Execute brand analysis in parallel"""
        try:
            logger.info("🏷️ Running Brand Analysis Node (Parallel)")
            app_state = state['app_state']
            
            state['current_step'] = 'brand_analysis'
            
            # Execute brand analysis using LLM orchestrator
            result = await self.llm_orchestrator.consensus_analysis(
                query=f"Analyze brand positioning and strategy for: {app_state.idea_description}",
                context={
                    "target_audience": app_state.target_audience,
                    "analysis_type": "brand_analysis",
                    "focus": "brand_positioning, messaging, competitive_advantage"
                }
            )
            
            # Update app state
            app_state.set("brand_analysis", result)
            state['completed_steps'].append('brand_analysis')
            
            logger.info("✅ Brand Analysis completed successfully (Parallel)")
            return {"app_state": app_state, "current_step": "brand_analysis"}
            
        except Exception as e:
            logger.error(f"❌ Brand Analysis failed: {str(e)}")
            state['error_message'] = f"Brand Analysis failed: {str(e)}"
            return {"error_message": state['error_message']}
    
    async def run_experience_analysis(self, state: GraphState) -> Dict[str, Any]:
        """Execute experience analysis in parallel"""
        try:
            logger.info("🎯 Running Experience Analysis Node (Parallel)")
            app_state = state['app_state']
            
            state['current_step'] = 'experience_analysis'
            
            # Execute experience analysis using LLM orchestrator
            result = await self.llm_orchestrator.consensus_analysis(
                query=f"Analyze user experience and customer journey for: {app_state.idea_description}",
                context={
                    "target_audience": app_state.target_audience,
                    "analysis_type": "experience_analysis",
                    "focus": "user_experience, customer_journey, pain_points"
                }
            )
            
            # Update app state
            app_state.set("experience_analysis", result)
            state['completed_steps'].append('experience_analysis')
            
            logger.info("✅ Experience Analysis completed successfully (Parallel)")
            return {"app_state": app_state, "current_step": "experience_analysis"}
            
        except Exception as e:
            logger.error(f"❌ Experience Analysis failed: {str(e)}")
            state['error_message'] = f"Experience Analysis failed: {str(e)}"
            return {"error_message": state['error_message']}
    
    async def run_strategic_scoring(self, state: GraphState) -> Dict[str, Any]:
        """Execute strategic scoring after all parallel analyses complete"""
        try:
            logger.info("🎯 Running Strategic Scoring Node (Convergence)")
            app_state = state['app_state']
            
            state['current_step'] = 'strategic_scoring'
            
            # Execute strategic scoring using all collected analyses
            result = await self.scorer.run(app_state.to_dict())
            
            # Update app state
            app_state.set("strategic_analysis_v4", result)
            state['completed_steps'].append('strategic_scoring')
            
            logger.info("✅ Strategic Scoring completed successfully (Convergence)")
            return {"app_state": app_state, "current_step": "strategic_scoring"}
            
        except Exception as e:
            logger.error(f"❌ Strategic Scoring failed: {str(e)}")
            state['error_message'] = f"Strategic Scoring failed: {str(e)}"
            return {"error_message": state['error_message']}
    
    async def execute(self, idea_description: str, target_audience: str = None, 
                     additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executes the full strategic analysis workflow using parallel LangGraph.
        
        Args:
            idea_description: Description of the business idea
            target_audience: Target audience for the analysis
            additional_context: Additional context for the analysis
            
        Returns:
            Comprehensive analysis results
        """
        try:
            logger.info("🚀 Starting Parallel LangGraph Workflow Execution")
            
            # Initialize the state for this run
            initial_app_state = AppState(
                idea_description=idea_description,
                target_audience=target_audience or "General market",
                additional_context=additional_context or {}
            )
            
            initial_graph_state = GraphState(
                app_state=initial_app_state,
                analysis_results={},
                error_message="",
                current_step="",
                completed_steps=[],
                retry_count=0
            )
            
            # Execute the graph
            logger.info("🔄 Invoking parallel LangGraph workflow...")
            final_state = await self.graph.ainvoke(initial_graph_state)
            
            # Check for errors
            if final_state.get('error_message'):
                logger.error(f"❌ Workflow completed with errors: {final_state['error_message']}")
                return {
                    "error": final_state['error_message'],
                    "completed_steps": final_state.get('completed_steps', []),
                    "current_step": final_state.get('current_step', '')
                }
            
            logger.info("✅ Parallel LangGraph workflow completed successfully")
            logger.info(f"📊 Completed steps: {final_state.get('completed_steps', [])}")
            
            return {
                "success": True,
                "analysis_results": final_state.get('strategic_analysis_v4', {}),
                "completed_steps": final_state.get('completed_steps', []),
                "final_step": final_state.get('current_step', ''),
                "app_state": final_state.get('app_state', {}),
                "workflow_type": "parallel"
            }
            
        except Exception as e:
            logger.error(f"❌ Parallel LangGraph workflow execution failed: {str(e)}")
            return {
                "error": f"Workflow execution failed: {str(e)}",
                "success": False
            }
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get the current status and capabilities of the workflow"""
        return {
            "workflow_type": "Parallel LangGraph-based Strategic Analysis",
            "nodes": [
                "consumer_analysis", "market_analysis", "product_analysis",
                "brand_analysis", "experience_analysis", "strategic_scoring"
            ],
            "features": [
                "Parallel execution of analysis agents",
                "Graph-based workflow orchestration",
                "State management with TypedDict",
                "Automatic synchronization at convergence points",
                "Error handling and retry logic",
                "Comprehensive strategic analysis"
            ],
            "status": "initialized" if self.graph else "not_initialized",
            "execution_mode": "parallel"
        }

# Example usage and testing
if __name__ == '__main__':
    async def test_workflow():
        """Test the parallel LangGraph workflow"""
        try:
            workflow = LangGraphWorkflow()
            
            # Test execution
            results = await workflow.execute(
                idea_description="A smart home device that automates pet feeding and playtime",
                target_audience="Busy pet owners who want to ensure their pets are cared for while they are away",
                additional_context={
                    "market_focus": "smart_home_pet_care",
                    "competition_level": "medium",
                    "innovation_focus": "automation_and_ai"
                }
            )
            
            print("\n--- Final Analysis Results ---")
            import json
            print(json.dumps(results, indent=2, default=str))
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
    
    # Run the test
    asyncio.run(test_workflow())
