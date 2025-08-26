import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import numpy as np

from app.core.multi_llm_orchestrator import (
    MultiLLMOrchestrator,
    ConsensusMethod,
    LLMAnalysisResult,
    OpenAIAgent,
    AnthropicAgent,
    GoogleGeminiAgent,
    PerplexityAgent
)


class TestLLMAnalysisResult:
    """Test the LLMAnalysisResult dataclass"""
    
    def test_llm_analysis_result_creation(self):
        """Test creating an LLMAnalysisResult instance"""
        result = LLMAnalysisResult(
            model_name="test-model",
            analysis="Test analysis content",
            confidence=0.85,
            key_insights=["Insight 1", "Insight 2"],
            recommendations=["Rec 1", "Rec 2"],
            execution_time=1.5,
            cost=0.01,
            timestamp=datetime.now(),
            metadata={"test": "data"}
        )
        
        assert result.model_name == "test-model"
        assert result.analysis == "Test analysis content"
        assert result.confidence == 0.85
        assert len(result.key_insights) == 2
        assert len(result.recommendations) == 2
        assert result.execution_time == 1.5
        assert result.cost == 0.01


class TestOpenAIAgent:
    """Test the OpenAI Agent"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client"""
        with patch('app.core.multi_llm_orchestrator.openai.AsyncOpenAI') as mock:
            mock_client = Mock()
            mock_client.chat.completions.create = AsyncMock()
            mock.return_value = mock_client
            yield mock_client
    
    @pytest.mark.asyncio
    async def test_openai_agent_analyze_success(self, mock_openai_client):
        """Test successful OpenAI analysis"""
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test analysis with insights and recommendations"
        mock_response.usage.total_tokens = 150
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        agent = OpenAIAgent()
        result = await agent.analyze("Test query")
        
        assert result.model_name.startswith("OpenAI-")
        assert "Test analysis" in result.analysis
        assert result.confidence > 0
        assert len(result.key_insights) > 0
        assert len(result.recommendations) > 0
        assert result.cost > 0
    
    @pytest.mark.asyncio
    async def test_openai_agent_analyze_failure(self, mock_openai_client):
        """Test OpenAI analysis failure handling"""
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        agent = OpenAIAgent()
        result = await agent.analyze("Test query")
        
        assert result.confidence == 0.0
        assert "Analysis failed" in result.analysis
        assert len(result.key_insights) == 0
        assert len(result.recommendations) == 0


class TestAnthropicAgent:
    """Test the Anthropic Agent"""
    
    @pytest.fixture
    def mock_anthropic_client(self):
        """Mock Anthropic client"""
        with patch('app.core.multi_llm_orchestrator.anthropic.AsyncAnthropic') as mock:
            mock_client = Mock()
            mock_client.messages.create = AsyncMock()
            mock.return_value = mock_client
            yield mock_client
    
    @pytest.mark.asyncio
    async def test_anthropic_agent_analyze_success(self, mock_anthropic_client):
        """Test successful Anthropic analysis"""
        # Mock response
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Claude analysis with strategic insights"
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 200
        mock_anthropic_client.messages.create.return_value = mock_response
        
        agent = AnthropicAgent()
        result = await agent.analyze("Test query")
        
        assert result.model_name.startswith("Anthropic-")
        assert "Claude analysis" in result.analysis
        assert result.confidence > 0
        assert result.cost > 0


class TestGoogleGeminiAgent:
    """Test the Google Gemini Agent"""
    
    @pytest.fixture
    def mock_gemini_model(self):
        """Mock Gemini model"""
        with patch('app.core.multi_llm_orchestrator.genai.GenerativeModel') as mock:
            mock_model = Mock()
            mock_model.agenerate_content = AsyncMock()
            mock.return_value = mock_model
            yield mock_model
    
    @pytest.mark.asyncio
    async def test_gemini_agent_analyze_success(self, mock_gemini_model):
        """Test successful Gemini analysis"""
        # Mock response
        mock_response = Mock()
        mock_response.text = "Gemini analysis with recommendations"
        mock_gemini_model.agenerate_content.return_value = mock_response
        
        agent = GoogleGeminiAgent()
        result = await agent.analyze("Test query")
        
        assert result.model_name.startswith("Google-")
        assert "Gemini analysis" in result.analysis
        assert result.confidence > 0
        assert result.cost > 0


class TestPerplexityAgent:
    """Test the Perplexity Agent"""
    
    @pytest.fixture
    def mock_httpx_client(self):
        """Mock httpx client"""
        with patch('httpx.AsyncClient') as mock:
            mock_client = Mock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.post = AsyncMock()
            mock.return_value = mock_client
            yield mock_client
    
    @pytest.mark.asyncio
    async def test_perplexity_agent_analyze_success(self, mock_httpx_client):
        """Test successful Perplexity analysis"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Perplexity analysis with insights'}}]
        }
        mock_httpx_client.post.return_value = mock_response
        
        agent = PerplexityAgent()
        result = await agent.analyze("Test query")
        
        assert result.model_name.startswith("Perplexity-")
        assert "Perplexity analysis" in result.analysis
        assert result.confidence > 0
        assert result.cost > 0


class TestMultiLLMOrchestrator:
    """Test the Multi-LLM Orchestrator"""
    
    @pytest.fixture
    def mock_settings(self):
        """Mock settings with API keys"""
        with patch('app.core.multi_llm_orchestrator.settings') as mock:
            mock.OPENAI_API_KEY = "test-openai-key"
            mock.ANTHROPIC_API_KEY = "test-anthropic-key"
            mock.GOOGLE_GEMINI_API_KEY = "test-gemini-key"
            mock.PERPLEXITY_API_KEY = "test-perplexity-key"
            yield mock
    
    @pytest.fixture
    def orchestrator(self, mock_settings):
        """Create orchestrator instance"""
        return MultiLLMOrchestrator(ConsensusMethod.CONFIDENCE_BASED)
    
    def test_orchestrator_initialization(self, mock_settings):
        """Test orchestrator initialization"""
        orchestrator = MultiLLMOrchestrator()
        
        assert len(orchestrator.llm_agents) > 0
        assert orchestrator.consensus_method == ConsensusMethod.CONFIDENCE_BASED
    
    def test_consensus_method_enum(self):
        """Test all consensus methods are available"""
        methods = [method.value for method in ConsensusMethod]
        expected_methods = [
            "majority_vote",
            "weighted_average", 
            "confidence_based",
            "expert_validation",
            "clustering_based"
        ]
        
        for method in expected_methods:
            assert method in methods
    
    @pytest.mark.asyncio
    async def test_consensus_analysis_success(self, orchestrator):
        """Test successful consensus analysis"""
        # Mock agent responses
        mock_result = LLMAnalysisResult(
            model_name="test-model",
            analysis="Test analysis",
            confidence=0.8,
            key_insights=["Insight 1", "Insight 2"],
            recommendations=["Rec 1"],
            execution_time=1.0,
            cost=0.01,
            timestamp=datetime.now(),
            metadata={}
        )
        
        # Mock all agents to return the same result
        for agent in orchestrator.llm_agents.values():
            agent.analyze = AsyncMock(return_value=mock_result)
        
        result = await orchestrator.consensus_analysis("Test query")
        
        assert "consensus" in result
        assert "individual_results" in result
        assert "aggregate_metrics" in result
        assert result["consensus_method"] == "confidence_based"
    
    @pytest.mark.asyncio
    async def test_consensus_analysis_all_failed(self, orchestrator):
        """Test consensus analysis when all agents fail"""
        # Mock all agents to fail
        for agent in orchestrator.llm_agents.values():
            agent.analyze = AsyncMock(side_effect=Exception("Agent failed"))
        
        result = await orchestrator.consensus_analysis("Test query")
        
        assert "error" in result
        assert "All LLM analyses failed" in result["error"]
    
    @pytest.mark.asyncio
    async def test_confidence_based_consensus(self, orchestrator):
        """Test confidence-based consensus method"""
        # Create test results with different confidence levels
        results = [
            LLMAnalysisResult(
                model_name="high-conf",
                analysis="High confidence analysis",
                confidence=0.9,
                key_insights=["Key insight"],
                recommendations=["Key rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            ),
            LLMAnalysisResult(
                model_name="low-conf",
                analysis="Low confidence analysis",
                confidence=0.3,
                key_insights=["Less important"],
                recommendations=["Less important rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            )
        ]
        
        consensus = orchestrator._confidence_based_consensus(results)
        
        assert "consensus_insights" in consensus
        assert "consensus_recommendations" in consensus
        assert consensus["confidence"] > 0.5
    
    @pytest.mark.asyncio
    async def test_majority_vote_consensus(self, orchestrator):
        """Test majority vote consensus method"""
        # Create test results with overlapping insights
        results = [
            LLMAnalysisResult(
                model_name="model1",
                analysis="Analysis 1",
                confidence=0.8,
                key_insights=["Common insight", "Unique 1"],
                recommendations=["Common rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            ),
            LLMAnalysisResult(
                model_name="model2",
                analysis="Analysis 2",
                confidence=0.7,
                key_insights=["Common insight", "Unique 2"],
                recommendations=["Common rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            )
        ]
        
        consensus = orchestrator._majority_vote_consensus(results)
        
        assert "consensus_insights" in consensus
        assert "consensus_recommendations" in consensus
        assert "Common insight" in consensus["consensus_insights"]
    
    @pytest.mark.asyncio
    async def test_weighted_average_consensus(self, orchestrator):
        """Test weighted average consensus method"""
        # Create test results with different confidence levels
        results = [
            LLMAnalysisResult(
                model_name="high-conf",
                analysis="High confidence analysis",
                confidence=0.9,
                key_insights=["Weighted insight"],
                recommendations=["Weighted rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            ),
            LLMAnalysisResult(
                model_name="low-conf",
                analysis="Low confidence analysis",
                confidence=0.3,
                key_insights=["Less weighted"],
                recommendations=["Less weighted rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            )
        ]
        
        consensus = orchestrator._weighted_average_consensus(results)
        
        assert "consensus_insights" in consensus
        assert "consensus_recommendations" in consensus
        assert consensus["weighting_method"] == "confidence_based"
    
    @pytest.mark.asyncio
    async def test_expert_validation_consensus(self, orchestrator):
        """Test expert validation consensus method"""
        # Create test results with one high-confidence expert
        results = [
            LLMAnalysisResult(
                model_name="expert",
                analysis="Expert analysis",
                confidence=0.95,
                key_insights=["Expert insight"],
                recommendations=["Expert rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            ),
            LLMAnalysisResult(
                model_name="validator",
                analysis="Validation analysis",
                confidence=0.7,
                key_insights=["Similar insight"],
                recommendations=["Similar rec"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            )
        ]
        
        consensus = orchestrator._expert_validation_consensus(results)
        
        assert "consensus_insights" in consensus
        assert "consensus_recommendations" in consensus
        assert consensus["expert_model"] == "expert"
        assert consensus["validation_method"] == "cross_model_similarity"
    
    @pytest.mark.asyncio
    async def test_clustering_based_consensus(self, orchestrator):
        """Test clustering-based consensus method"""
        # Create test results with similar insights
        results = [
            LLMAnalysisResult(
                model_name="model1",
                analysis="Analysis 1",
                confidence=0.8,
                key_insights=["Market growth", "Customer demand"],
                recommendations=["Expand operations"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            ),
            LLMAnalysisResult(
                model_name="model2",
                analysis="Analysis 2",
                confidence=0.7,
                key_insights=["Market expansion", "User needs"],
                recommendations=["Scale business"],
                execution_time=1.0,
                cost=0.01,
                timestamp=datetime.now(),
                metadata={}
            )
        ]
        
        # Mock sentence transformers and sklearn
        with patch('sentence_transformers.SentenceTransformer') as mock_transformer, \
             patch('sklearn.cluster.DBSCAN') as mock_dbscan:
            
            mock_model = Mock()
            mock_model.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])
            mock_transformer.return_value = mock_model
            
            mock_clustering = Mock()
            mock_clustering.labels_ = [0, 0]  # Same cluster
            mock_dbscan.return_value = mock_clustering
            
            consensus = await orchestrator._clustering_based_consensus(results)
            
            assert "consensus_insights" in consensus
            assert "consensus_recommendations" in consensus
            assert consensus["clustering_method"] == "sentence_embeddings_dbscan"
    
    def test_text_normalization(self, orchestrator):
        """Test text normalization for similarity calculation"""
        text1 = "Market growth and expansion!"
        text2 = "market growth & expansion"
        
        normalized1 = orchestrator._normalize_text(text1)
        normalized2 = orchestrator._normalize_text(text2)
        
        assert normalized1 == "market growth and expansion"
        assert normalized2 == "market growth expansion"
    
    def test_similarity_calculation(self, orchestrator):
        """Test similarity calculation between texts"""
        text1 = "Market growth and expansion"
        text2 = "Market expansion and growth"
        text3 = "Completely different topic"
        
        sim1 = orchestrator._calculate_similarity(text1, text2)
        sim2 = orchestrator._calculate_similarity(text1, text3)
        
        assert sim1 > 0.5  # High similarity
        assert sim2 < 0.3  # Low similarity
    
    @pytest.mark.asyncio
    async def test_get_available_models(self, orchestrator):
        """Test getting available models information"""
        models_info = await orchestrator.get_available_models()
        
        assert "available_models" in models_info
        assert "total_models" in models_info
        assert "consensus_methods" in models_info
        assert "current_method" in models_info
        assert models_info["current_method"] == "confidence_based"
    
    def test_set_consensus_method(self, orchestrator):
        """Test changing consensus method"""
        orchestrator.set_consensus_method(ConsensusMethod.MAJORITY_VOTE)
        
        assert orchestrator.consensus_method == ConsensusMethod.MAJORITY_VOTE
    
    @pytest.mark.asyncio
    async def test_health_check(self, orchestrator):
        """Test health check functionality"""
        # Mock agent health checks
        for agent in orchestrator.llm_agents.values():
            agent.analyze = AsyncMock(return_value=LLMAnalysisResult(
                model_name="test",
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
        
        assert "overall_status" in health_status
        assert "agents" in health_status
        assert "timestamp" in health_status


if __name__ == "__main__":
    pytest.main([__file__])
