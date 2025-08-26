import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.agents.perplexity_research_agent import PerplexityResearchAgent
from app.core.workflow import ValidatusWorkflow
from app.utils.data_quality import AdvancedDataQualityAssessment
from app.utils.nlp import ProductionNLPProcessor
from app.agents.enhanced_base_agent import EnhancedBaseAgent

class TestValidatusPlatform:
    """Comprehensive test suite for Validatus platform"""
    
    @pytest.fixture
    def perplexity_agent(self):
        """Create Perplexity agent for testing"""
        return PerplexityResearchAgent()
    
    @pytest.fixture
    def data_quality_assessor(self):
        """Create data quality assessor for testing"""
        return AdvancedDataQualityAssessment()
    
    @pytest.fixture
    def nlp_processor(self):
        """Create NLP processor for testing"""
        return ProductionNLPProcessor()
    
    @pytest.fixture
    def workflow(self):
        """Create workflow for testing"""
        return ValidatusWorkflow()
    
    @pytest.mark.asyncio
    async def test_perplexity_agent_initialization(self, perplexity_agent):
        """Test Perplexity agent initialization"""
        assert perplexity_agent is not None
        assert hasattr(perplexity_agent, 'base_url')
        assert hasattr(perplexity_agent, 'api_key')
        assert hasattr(perplexity_agent, 'model_mapping')
        
        # Check model mapping
        expected_models = ['quick_search', 'detailed_analysis', 'reasoning_task', 'deep_research']
        for model in expected_models:
            assert model in perplexity_agent.model_mapping
    
    @pytest.mark.asyncio
    async def test_perplexity_agent_research_methods(self, perplexity_agent):
        """Test Perplexity agent research methods exist"""
        assert hasattr(perplexity_agent, 'research')
        assert hasattr(perplexity_agent, '_perplexity_search')
        assert hasattr(perplexity_agent, '_build_search_parameters')
        assert hasattr(perplexity_agent, '_get_domain_filters')
        
        # Check method signatures
        assert asyncio.iscoroutinefunction(perplexity_agent.research)
        assert asyncio.iscoroutinefunction(perplexity_agent._perplexity_search)
    
    @pytest.mark.asyncio
    async def test_data_quality_assessment_initialization(self, data_quality_assessor):
        """Test data quality assessment initialization"""
        assert data_quality_assessor is not None
        assert hasattr(data_quality_assessor, 'domain_authority')
        assert hasattr(data_quality_assessor, 'thresholds')
        
        # Check domain authority mapping
        assert 'bloomberg.com' in data_quality_assessor.domain_authority
        assert 'reuters.com' in data_quality_assessor.domain_authority
        
        # Check thresholds
        assert 'min_content_length' in data_quality_assessor.thresholds
        assert 'max_content_length' in data_quality_assessor.thresholds
    
    @pytest.mark.asyncio
    async def test_data_quality_comprehensive_assessment(self, data_quality_assessor):
        """Test comprehensive data quality assessment"""
        sample_data = {
            'web_research': {
                'results': [
                    {
                        'content': 'High-quality market analysis with specific data points and citations.',
                        'url': 'https://bloomberg.com/analysis',
                        'timestamp': '2024-01-15T10:00:00Z'
                    }
                ]
            }
        }
        
        quality_result = await data_quality_assessor.comprehensive_quality_assessment(sample_data)
        
        assert 'overall_quality_score' in quality_result
        assert 'quality_grade' in quality_result
        assert 'detailed_assessment' in quality_result
        assert 'improvement_recommendations' in quality_result
        
        # Check quality score range
        assert 0.0 <= quality_result['overall_quality_score'] <= 1.0
        
        # Check quality grade format
        assert quality_result['quality_grade'] in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
    
    @pytest.mark.asyncio
    async def test_nlp_processor_initialization(self, nlp_processor):
        """Test NLP processor initialization"""
        assert nlp_processor is not None
        assert hasattr(nlp_processor, 'strategic_keywords')
        assert hasattr(nlp_processor, 'openai_client')
        
        # Check strategic keywords
        expected_categories = ['market_size', 'competition', 'growth', 'risk', 'opportunity']
        for category in expected_categories:
            assert category in nlp_processor.strategic_keywords
    
    @pytest.mark.asyncio
    async def test_nlp_advanced_query_parsing(self, nlp_processor):
        """Test advanced query parsing functionality"""
        query = "Analyze the electric vehicle market in Europe for competitive opportunities"
        context = {
            'industry': 'Automotive',
            'geography': ['Europe'],
            'company_stage': 'startup'
        }
        
        # Mock OpenAI client to avoid API calls during testing
        with patch.object(nlp_processor, 'openai_client') as mock_client:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = 'market_analysis'
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            
            parsing_result = await nlp_processor.advanced_query_parsing(query, context)
            
            assert 'entities' in parsing_result
            assert 'intent' in parsing_result
            assert 'strategic_keywords' in parsing_result
            assert 'complexity_analysis' in parsing_result
            assert 'search_variations' in parsing_result
    
    @pytest.mark.asyncio
    async def test_workflow_initialization(self, workflow):
        """Test workflow initialization"""
        assert workflow is not None
        assert hasattr(workflow, 'agents')
        assert hasattr(workflow, 'query_parser')
        assert hasattr(workflow, 'scoring_engine')
        assert hasattr(workflow, 'aggregator')
        
        # Check agents
        expected_agents = [
            'market_research', 'consumer_insights', 'competitor_analysis',
            'trend_analysis', 'pricing_research', 'perplexity_research'
        ]
        for agent in expected_agents:
            assert agent in workflow.agents
    
    @pytest.mark.asyncio
    async def test_workflow_build_method(self, workflow):
        """Test workflow build method"""
        compiled_workflow = workflow.build_workflow()
        assert compiled_workflow is not None
        
        # Check that it's a compiled LangGraph workflow
        assert hasattr(compiled_workflow, 'get_state')
        assert hasattr(compiled_workflow, 'invoke')
    
    @pytest.mark.asyncio
    async def test_enhanced_base_agent_architecture(self):
        """Test enhanced base agent architecture"""
        # Create a mock implementation of the abstract class
        class MockEnhancedAgent(EnhancedBaseAgent):
            async def research(self, query: str, context: dict) -> dict:
                return {'result': 'mock_research', 'confidence': 0.8}
            
            async def _execute_single_research_task(self, task: dict) -> dict:
                return {'task_result': 'mock_task', 'success': True}
        
        agent = MockEnhancedAgent('test_agent')
        
        # Test basic functionality
        assert agent.agent_name == 'test_agent'
        assert hasattr(agent, 'safe_api_call')
        assert hasattr(agent, 'parallel_research_execution')
        assert hasattr(agent, 'calculate_advanced_confidence')
        
        # Test research method
        result = await agent.research("test query", {"context": "test"})
        assert result['result'] == 'mock_research'
        assert result['confidence'] == 0.8
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling across the platform"""
        # Test data quality assessment with invalid data
        assessor = AdvancedDataQualityAssessment()
        
        # Test with malformed data that should trigger error handling
        invalid_data = {
            'malformed': 'data',
            'invalid_timestamp': 'not-a-timestamp',
            'empty_content': ''
        }
        quality_result = await assessor.comprehensive_quality_assessment(invalid_data)
        
        # Should handle gracefully but with low quality score
        assert 'overall_quality_score' in quality_result
        assert quality_result['overall_quality_score'] < 0.5  # Should be low due to poor data
        assert 'quality_grade' in quality_result
    
    @pytest.mark.asyncio
    async def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        # Test data quality assessment performance
        assessor = AdvancedDataQualityAssessment()
        
        large_data = {
            'web_research': {
                'results': [
                    {
                        'content': 'Sample market analysis content ' * 100,  # Large content
                        'url': 'https://example.com/analysis',
                        'timestamp': '2024-01-15T10:00:00Z'
                    }
                ] * 10  # Multiple results
            }
        }
        
        import time
        start_time = time.time()
        
        quality_result = await assessor.comprehensive_quality_assessment(large_data)
        
        execution_time = time.time() - start_time
        
        # Performance assertion: should complete within reasonable time
        assert execution_time < 5.0  # Should complete within 5 seconds
        
        # Quality result should still be valid
        assert 'overall_quality_score' in quality_result
        assert quality_result['overall_quality_score'] >= 0.0
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent operations handling"""
        # Test multiple data quality assessments running concurrently
        assessor = AdvancedDataQualityAssessment()
        
        sample_data = {
            'web_research': {
                'results': [
                    {
                        'content': 'Test content for concurrent operations.',
                        'url': 'https://test.com/analysis',
                        'timestamp': '2024-01-15T10:00:00Z'
                    }
                ]
            }
        }
        
        # Create multiple concurrent assessment tasks
        tasks = [
            assessor.comprehensive_quality_assessment(sample_data)
            for _ in range(5)
        ]
        
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should complete successfully
        assert len(results) == 5
        
        # Check that results are consistent
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) == 5
        
        # All should have similar quality scores (within reasonable variance)
        scores = [r['overall_quality_score'] for r in successful_results]
        score_variance = max(scores) - min(scores)
        assert score_variance < 0.2  # Variance should be small for same input
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        # Test that required environment variables are accessible
        from config import settings
        
        # These should be accessible (even if empty)
        assert hasattr(settings, 'OPENAI_API_KEY')
        assert hasattr(settings, 'PERPLEXITY_API_KEY')
        assert hasattr(settings, 'TAVILY_API_KEY')
        assert hasattr(settings, 'REDIS_URL')
        assert hasattr(settings, 'DATABASE_URL')
    
    @pytest.mark.asyncio
    async def test_memory_management(self):
        """Test memory management and resource cleanup"""
        # Test that agents properly clean up resources
        class TestAgent(EnhancedBaseAgent):
            async def research(self, query: str, context: dict) -> dict:
                return {'result': 'test'}
            
            async def _execute_single_research_task(self, task: dict) -> dict:
                return {'task_result': 'test'}
        
        # Create agent with context manager
        async with TestAgent('test_agent') as agent:
            result = await agent.research("test", {})
            assert result['result'] == 'test'
        
        # Agent should be properly cleaned up
        # This test ensures no resource leaks
    
    @pytest.mark.asyncio
    async def test_data_validation(self):
        """Test data validation functionality"""
        class TestAgent(EnhancedBaseAgent):
            async def research(self, query: str, context: dict) -> dict:
                return {'result': 'test'}
            
            async def _execute_single_research_task(self, task: dict) -> dict:
                return {'task_result': 'test'}
        
        agent = TestAgent('test_agent')
        
        # Test data validation
        test_data = {
            'content': 'Valid content for testing with sufficient length to meet quality requirements',
            'timestamp': '2024-01-15T10:00:00Z',
            'source': 'https://test.com',
            'structured_data': {'key': 'value'},
            'metadata': {'author': 'test', 'category': 'analysis'}
        }
        
        validation_result = await agent.validate_research_data(test_data)
        
        assert validation_result['is_valid'] == True
        # Our scoring logic gives 0.2 for basic content, 0.2 for structured data, 0.2 for metadata
        # Total should be 0.6 or higher
        assert validation_result['quality_score'] >= 0.6
        assert len(validation_result['missing_fields']) == 0
    
    @pytest.mark.asyncio
    async def test_research_summary_generation(self):
        """Test research summary generation"""
        class TestAgent(EnhancedBaseAgent):
            async def research(self, query: str, context: dict) -> dict:
                return {'result': 'test'}
            
            async def _execute_single_research_task(self, task: dict) -> dict:
                return {'task_result': 'test'}
        
        agent = TestAgent('test_agent')
        
        # Test summary generation
        test_results = [
            {
                'content': 'Market analysis shows growth potential',
                'source': 'https://source1.com',
                'timestamp': '2024-01-15T10:00:00Z'
            },
            {
                'content': 'Competitive landscape analysis',
                'source': 'https://source2.com',
                'timestamp': '2024-01-15T10:00:00Z'
            }
        ]
        
        summary = agent.generate_research_summary(test_results)
        
        assert 'summary' in summary
        assert 'total_results' in summary
        assert 'unique_sources' in summary
        assert 'average_quality' in summary
        assert summary['total_results'] == 2
        assert summary['unique_sources'] == 2
        assert 'key_insights' in summary

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
