import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.multi_llm_orchestrator import (
    MultiLLMOrchestrator, 
    ConsensusMethod, 
    LLMAnalysisResult,
    OpenAIAgent,
    PerplexityAgent
)
from app.core.knowledge_graph_analyzer import (
    KnowledgeGraphAnalyzer,
    RelationshipType,
    GraphEntity,
    GraphRelationship,
    MarketInsight
)
from app.core.workflow import ValidatusWorkflow
from datetime import datetime

class TestMultiLLMOrchestrator:
    """Test suite for Multi-LLM Orchestrator"""
    
    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance for testing"""
        # Mock API keys to avoid actual API calls
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'PERPLEXITY_API_KEY': 'test_key'
        }):
            orchestrator = MultiLLMOrchestrator(ConsensusMethod.CONFIDENCE_BASED)
            yield orchestrator
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator is not None
        assert orchestrator.consensus_method == ConsensusMethod.CONFIDENCE_BASED
        assert len(orchestrator.llm_agents) > 0
    
    @pytest.mark.asyncio
    async def test_consensus_analysis(self, orchestrator):
        """Test consensus analysis functionality"""
        query = "Test strategic analysis query"
        context = {"industry": "Technology", "geography": ["North America"]}
        
        # Mock the agent analyze methods
        for agent in orchestrator.llm_agents.values():
            agent.analyze = AsyncMock(return_value=LLMAnalysisResult(
                model_name=agent.__class__.__name__,
                analysis="Test analysis with key insights and recommendations",
                confidence=0.8,
                key_insights=["Insight 1", "Insight 2", "Insight 3"],
                recommendations=["Recommendation 1", "Recommendation 2"],
                execution_time=1.5,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            ))
        
        result = await orchestrator.consensus_analysis(query, context)
        
        assert result is not None
        assert "consensus" in result
        assert "individual_results" in result
        assert "aggregate_metrics" in result
        assert result["consensus_method"] == "confidence_based"
    
    @pytest.mark.asyncio
    async def test_consensus_methods(self, orchestrator):
        """Test different consensus methods"""
        # Test confidence-based consensus
        orchestrator.consensus_method = ConsensusMethod.CONFIDENCE_BASED
        assert orchestrator.consensus_method == ConsensusMethod.CONFIDENCE_BASED
        
        # Test majority vote consensus
        orchestrator.consensus_method = ConsensusMethod.MAJORITY_VOTE
        assert orchestrator.consensus_method == ConsensusMethod.MAJORITY_VOTE
    
    @pytest.mark.asyncio
    async def test_health_check(self, orchestrator):
        """Test health check functionality"""
        # Mock the agent analyze methods for health check
        for agent in orchestrator.llm_agents.values():
            agent.analyze = AsyncMock(return_value=LLMAnalysisResult(
                model_name=agent.__class__.__name__,
                analysis="Health check passed",
                confidence=0.9,
                key_insights=[],
                recommendations=[],
                execution_time=0.1,
                cost=0.001,
                timestamp=datetime.now(),
                metadata={}
            ))
        
        health_status = await orchestrator.health_check()
        
        assert health_status is not None
        assert "overall_status" in health_status
        assert "agents" in health_status
        assert "timestamp" in health_status

class TestKnowledgeGraphAnalyzer:
    """Test suite for Knowledge Graph Analyzer"""
    
    @pytest.fixture
    async def kg_analyzer(self):
        """Create knowledge graph analyzer instance for testing"""
        # Mock Neo4j connection
        with patch('app.core.knowledge_graph_analyzer.GraphDatabase'):
            analyzer = KnowledgeGraphAnalyzer()
            yield analyzer
    
    @pytest.mark.asyncio
    async def test_analyzer_initialization(self, kg_analyzer):
        """Test analyzer initialization"""
        assert kg_analyzer is not None
        assert kg_analyzer.logger is not None
    
    @pytest.mark.asyncio
    async def test_relationship_analysis(self, kg_analyzer):
        """Test relationship analysis functionality"""
        entities = ["Company A", "Company B", "Company C"]
        
        # Mock the driver and session
        kg_analyzer.driver = MagicMock()
        mock_session = MagicMock()
        kg_analyzer.driver.session.return_value.__enter__.return_value = mock_session
        
        # Mock query results
        mock_session.run.return_value = MagicMock()
        mock_session.run.return_value.single.return_value = {"health_check": 1}
        
        result = await kg_analyzer.relationship_analysis(entities, depth=2)
        
        assert result is not None
        assert "entities" in result
        assert "graph_data" in result
        assert "relationship_insights" in result
        assert "strategic_insights" in result
    
    @pytest.mark.asyncio
    async def test_entity_creation(self, kg_analyzer):
        """Test entity creation functionality"""
        name = "Test Company"
        entity_type = "Company"
        properties = {"industry": "Technology", "size": "Large"}
        
        # Mock the driver and session
        kg_analyzer.driver = MagicMock()
        mock_session = MagicMock()
        kg_analyzer.driver.session.return_value.__enter__.return_value = mock_session
        
        # Mock query results
        mock_node = MagicMock()
        mock_node.id = "123"
        mock_node.labels = ["Entity"]
        mock_node.get.return_value = name
        mock_session.run.return_value.single.return_value = {"e": mock_node}
        
        result = await kg_analyzer.create_entity(name, entity_type, properties)
        
        assert result is not None
        assert "success" in result
        assert result["success"] is True
        assert "entity" in result
    
    @pytest.mark.asyncio
    async def test_relationship_creation(self, kg_analyzer):
        """Test relationship creation functionality"""
        source = "Company A"
        target = "Company B"
        relationship_type = RelationshipType.COMPETES_WITH
        properties = {"strength": 0.8, "confidence": 0.9}
        
        # Mock the driver and session
        kg_analyzer.driver = MagicMock()
        mock_session = MagicMock()
        kg_analyzer.driver.session.return_value.__enter__.return_value = mock_session
        
        # Mock query results
        mock_relationship = MagicMock()
        mock_relationship.id = "456"
        mock_relationship.get.return_value = relationship_type.value
        mock_session.run.return_value.single.return_value = {"r": mock_relationship}
        
        result = await kg_analyzer.create_relationship(source, target, relationship_type, properties)
        
        assert result is not None
        assert "success" in result
        assert result["success"] is True
        assert "relationship" in result
    
    @pytest.mark.asyncio
    async def test_health_check(self, kg_analyzer):
        """Test health check functionality"""
        # Mock the driver and session
        kg_analyzer.driver = MagicMock()
        mock_session = MagicMock()
        kg_analyzer.driver.session.return_value.__enter__.return_value = mock_session
        
        # Mock query results
        mock_session.run.return_value.single.return_value = {"health_check": 1}
        
        health_status = await kg_analyzer.health_check()
        
        assert health_status is not None
        assert "status" in health_status
        assert "timestamp" in health_status

class TestEnhancedWorkflow:
    """Test suite for enhanced workflow with new components"""
    
    @pytest.fixture
    async def enhanced_workflow(self):
        """Create enhanced workflow instance for testing"""
        workflow = ValidatusWorkflow()
        yield workflow
    
    @pytest.mark.asyncio
    async def test_enhanced_analysis(self, enhanced_workflow):
        """Test enhanced analysis functionality"""
        query = "Test strategic analysis query"
        context = {"industry": "Technology", "geography": ["North America"]}
        
        # Mock the multi-LLM orchestrator
        enhanced_workflow.multi_llm_orchestrator.consensus_analysis = AsyncMock(return_value={
            "consensus": {
                "consensus_insights": ["Insight 1", "Insight 2"],
                "consensus_recommendations": ["Recommendation 1"]
            },
            "individual_results": [
                {
                    "key_insights": ["Insight A", "Insight B"],
                    "recommendations": ["Recommendation A"]
                }
            ]
        })
        
        # Mock the knowledge graph analyzer
        enhanced_workflow.knowledge_graph_analyzer.relationship_analysis = AsyncMock(return_value={
            "opportunities_risks": {
                "recommendations": ["KG Recommendation 1", "KG Recommendation 2"]
            }
        })
        
        result = await enhanced_workflow.enhanced_analysis(query, context)
        
        assert result is not None
        assert "llm_consensus" in result
        assert "knowledge_graph_insights" in result
        assert "enhanced_recommendations" in result
        assert "analysis_timestamp" in result
    
    @pytest.mark.asyncio
    async def test_entity_extraction(self, enhanced_workflow):
        """Test entity extraction from consensus"""
        consensus = {
            "consensus": {
                "consensus_insights": ["Company A is leading the market", "Company B shows strong growth"]
            },
            "individual_results": [
                {
                    "key_insights": ["Company C has innovative technology", "Company D faces challenges"]
                }
            ]
        }
        
        entities = enhanced_workflow._extract_entities_from_consensus(consensus)
        
        assert entities is not None
        assert len(entities) > 0
        assert "Company" in entities[0]  # Should extract company names
    
    @pytest.mark.asyncio
    async def test_recommendation_combination(self, enhanced_workflow):
        """Test recommendation combination functionality"""
        llm_consensus = {
            "consensus": {
                "consensus_recommendations": ["LLM Rec 1", "LLM Rec 2"]
            }
        }
        
        kg_insights = {
            "opportunities_risks": {
                "recommendations": ["KG Rec 1", "KG Rec 2"]
            }
        }
        
        combined = enhanced_workflow._combine_recommendations(llm_consensus, kg_insights)
        
        assert combined is not None
        assert len(combined) > 0
        assert "LLM Rec 1" in combined
        assert "KG Rec 1" in combined

class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # This test would require actual API keys and database connections
        # For now, we'll test the integration points
        
        workflow = ValidatusWorkflow()
        
        # Test that all components are properly initialized
        assert hasattr(workflow, 'multi_llm_orchestrator')
        assert hasattr(workflow, 'knowledge_graph_analyzer')
        assert workflow.multi_llm_orchestrator is not None
        assert workflow.knowledge_graph_analyzer is not None
        
        # Test that the workflow can be built
        compiled_workflow = workflow.build_workflow()
        assert compiled_workflow is not None
    
    @pytest.mark.asyncio
    async def test_component_communication(self):
        """Test communication between components"""
        # Test that components can communicate through the workflow
        workflow = ValidatusWorkflow()
        
        # Mock the components to avoid actual API calls
        workflow.multi_llm_orchestrator.consensus_analysis = AsyncMock(return_value={
            "consensus": {"consensus_insights": ["Test"], "consensus_recommendations": ["Test"]}
        })
        
        workflow.knowledge_graph_analyzer.relationship_analysis = AsyncMock(return_value={
            "opportunities_risks": {"recommendations": ["Test"]}
        })
        
        # Test the integration
        result = await workflow.enhanced_analysis("Test query", {"test": True})
        
        assert result is not None
        assert "llm_consensus" in result
        assert "knowledge_graph_insights" in result

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
