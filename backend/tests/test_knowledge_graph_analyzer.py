import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import json

from app.core.knowledge_graph_analyzer import (
    KnowledgeGraphAnalyzer,
    RelationshipType,
    GraphEntity,
    GraphRelationship,
    MarketInsight
)


class TestGraphEntity:
    """Test the GraphEntity dataclass"""
    
    def test_graph_entity_creation(self):
        """Test creating a GraphEntity instance"""
        entity = GraphEntity(
            id="test-123",
            name="Test Company",
            type="company",
            properties={
                "industry": "technology",
                "size": "startup",
                "location": "San Francisco"
            },
            confidence=0.85,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert entity.id == "test-123"
        assert entity.name == "Test Company"
        assert entity.type == "company"
        assert entity.properties["industry"] == "technology"
        assert entity.properties["size"] == "startup"


class TestGraphRelationship:
    """Test the GraphRelationship dataclass"""
    
    def test_graph_relationship_creation(self):
        """Test creating a GraphRelationship instance"""
        relationship = GraphRelationship(
            id="rel-123",
            source_id="company-1",
            target_id="company-2",
            type=RelationshipType.COMPETES_WITH,
            properties={
                "intensity": "high",
                "since": "2023"
            },
            strength=0.8,
            confidence=0.85,
            created_at=datetime.now()
        )
        
        assert relationship.id == "rel-123"
        assert relationship.source_id == "company-1"
        assert relationship.target_id == "company-2"
        assert relationship.type == RelationshipType.COMPETES_WITH
        assert relationship.properties["intensity"] == "high"


class TestMarketInsight:
    """Test the MarketInsight dataclass"""
    
    def test_market_insight_creation(self):
        """Test creating a MarketInsight instance"""
        insight = MarketInsight(
            insight_type="competitive_analysis",
            description="Strong competition in the market",
            entities_involved=["Company A", "Company B"],
            confidence=0.85,
            supporting_evidence=["Market share data", "Customer surveys"],
            strategic_implications=["Focus on differentiation", "Improve customer service"],
            risk_level="medium",
            opportunity_level="high"
        )
        
        assert insight.insight_type == "competitive_analysis"
        assert insight.description == "Strong competition in the market"
        assert insight.confidence == 0.85
        assert len(insight.entities_involved) == 2
        assert len(insight.supporting_evidence) == 2


class TestKnowledgeGraphAnalyzer:
    """Test the Knowledge Graph Analyzer"""
    
    @pytest.fixture
    def mock_neo4j_driver(self):
        """Mock Neo4j driver"""
        with patch('neo4j.GraphDatabase') as mock:
            mock_driver = Mock()
            mock_driver.verify_connectivity = AsyncMock()
            mock_driver.close = Mock()
            
            # Mock session method
            mock_session = Mock()
            mock_session.run = Mock()
            mock_session.__enter__ = Mock(return_value=mock_session)
            mock_session.__exit__ = Mock(return_value=None)
            
            mock_driver.session = Mock(return_value=mock_session)
            mock.driver.return_value = mock_driver
            yield mock_driver
    
    @pytest.fixture
    def analyzer(self, mock_neo4j_driver):
        """Create analyzer instance"""
        return KnowledgeGraphAnalyzer()
    
    def test_relationship_type_enum(self):
        """Test all relationship types are available"""
        types = [rt.value for rt in RelationshipType]
        expected_types = [
            "COMPETES_WITH",
            "SUPPLIES_TO", 
            "PARTNERS_WITH",
            "ACQUIRES",
            "INVESTED_IN",
            "SIMILAR_TO",
            "OPPOSES",
            "INFLUENCES",
            "DEPENDS_ON",
            "EMERGES_FROM"
        ]
        
        for rt in expected_types:
            assert rt in types
    
    @pytest.mark.asyncio
    async def test_health_check(self, analyzer):
        """Test health check functionality"""
        # Mock the session.run method to return a successful health check
        mock_result = Mock()
        mock_result.single.return_value = {"health_check": 1}
        analyzer.driver.session.return_value.run = Mock(return_value=mock_result)
        
        health_status = await analyzer.health_check()
        
        assert "status" in health_status
        assert "timestamp" in health_status
        assert "neo4j_connection" in health_status
    
    @pytest.mark.asyncio
    async def test_relationship_analysis_success(self, analyzer):
        """Test successful relationship analysis"""
        # Mock Neo4j session and transaction
        mock_session = Mock()
        mock_transaction = Mock()
        mock_session.begin_transaction.return_value = mock_transaction
        
        # Mock query results
        mock_result = Mock()
        mock_result.data.return_value = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        mock_transaction.run.return_value = mock_result
        mock_transaction.commit = AsyncMock()
        mock_transaction.close = Mock()
        
        # Mock the driver session
        analyzer.driver.session.return_value.__aenter__.return_value = mock_session
        analyzer.driver.session.return_value.__aexit__.return_value = None
        
        result = await analyzer.relationship_analysis(
            query="Analyze competitive landscape",
            context={"industry": "technology", "geography": "US"}
        )
        
        assert "insights" in result
        assert "recommendations" in result
        assert "graph_data" in result
        assert "analysis_summary" in result
    
    @pytest.mark.asyncio
    async def test_relationship_analysis_failure(self, analyzer):
        """Test relationship analysis failure handling"""
        # Mock Neo4j session to fail
        mock_session = Mock()
        mock_session.begin_transaction.side_effect = Exception("Database connection failed")
        
        analyzer.driver.session.return_value.__aenter__.return_value = mock_session
        analyzer.driver.session.return_value.__aexit__.return_value = None
        
        result = await analyzer.relationship_analysis(
            query="Analyze competitive landscape",
            context={"industry": "technology"}
        )
        
        assert "error" in result
        assert "Database connection failed" in result["error"]
    
    def test_build_entity_graph(self, analyzer):
        """Test building entity graph from data"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        graph_data = analyzer._build_entity_graph(mock_data)
        
        assert "nodes" in graph_data
        assert "edges" in graph_data
        assert len(graph_data["nodes"]) == 2
        assert len(graph_data["edges"]) == 1
    
    def test_node_to_dict(self, analyzer):
        """Test converting Neo4j node to dictionary"""
        mock_node = Mock()
        mock_node.get.side_effect = lambda key: {
            "id": "test-123",
            "name": "Test Entity",
            "type": "company"
        }.get(key)
        mock_node.labels = ["Company"]
        
        result = analyzer._node_to_dict(mock_node)
        
        assert result["id"] == "test-123"
        assert result["name"] == "Test Entity"
        assert result["type"] == "company"
        assert "Company" in result["labels"]
    
    def test_analyze_relationships(self, analyzer):
        """Test relationship analysis logic"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        insights = analyzer._analyze_relationships(mock_data)
        
        assert len(insights) > 0
        assert any("competition" in insight.description.lower() for insight in insights)
    
    def test_generate_strategic_insights(self, analyzer):
        """Test strategic insight generation"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        insights = analyzer._generate_strategic_insights(mock_data)
        
        assert len(insights) > 0
        assert all(hasattr(insight, 'insight_type') for insight in insights)
        assert all(hasattr(insight, 'confidence') for insight in insights)
    
    def test_analyze_competitive_landscape(self, analyzer):
        """Test competitive landscape analysis"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        analysis = analyzer._analyze_competitive_landscape(mock_data)
        
        assert "competitive_intensity" in analysis
        assert "key_competitors" in analysis
        assert "competitive_advantages" in analysis
    
    def test_analyze_partnership_opportunities(self, analyzer):
        """Test partnership opportunity analysis"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "PARTNERS_WITH", "properties": {"strength": "strong"}}
            }
        ]
        
        opportunities = analyzer._analyze_partnership_opportunities(mock_data)
        
        assert "potential_partners" in opportunities
        assert "partnership_strengths" in opportunities
        assert "collaboration_areas" in opportunities
    
    def test_analyze_market_entry_barriers(self, analyzer):
        """Test market entry barrier analysis"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        barriers = analyzer._analyze_market_entry_barriers(mock_data)
        
        assert "barrier_types" in barriers
        assert "barrier_strength" in barriers
        assert "overcoming_strategies" in barriers
    
    def test_analyze_supply_chain(self, analyzer):
        """Test supply chain analysis"""
        mock_data = [
            {
                "source": {"id": "supplier-1", "name": "Supplier A", "type": "supplier"},
                "target": {"id": "company-1", "name": "Company A", "type": "company"},
                "relationship": {"type": "SUPPLIES_TO", "properties": {"reliability": "high"}}
            }
        ]
        
        supply_chain = analyzer._analyze_supply_chain(mock_data)
        
        assert "supplier_network" in supply_chain
        assert "supply_chain_strength" in supply_chain
        assert "risk_factors" in supply_chain
    
    def test_analyze_innovation_clusters(self, analyzer):
        """Test innovation cluster analysis"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "SIMILAR_TO", "properties": {"innovation_level": "high"}}
            }
        ]
        
        clusters = analyzer._analyze_innovation_clusters(mock_data)
        
        assert "innovation_hotspots" in clusters
        assert "cluster_strength" in clusters
        assert "collaboration_potential" in clusters
    
    def test_calculate_market_positioning(self, analyzer):
        """Test market positioning calculation"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "medium"}}
            }
        ]
        
        positioning = analyzer._calculate_market_positioning(mock_data)
        
        assert "positioning_score" in positioning
        assert "competitive_advantage" in positioning
        assert "market_share_estimate" in positioning
    
    def test_identify_opportunities_risks(self, analyzer):
        """Test opportunity and risk identification"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "PARTNERS_WITH", "properties": {"strength": "strong"}}
            }
        ]
        
        analysis = analyzer._identify_opportunities_risks(mock_data)
        
        assert "opportunities" in analysis
        assert "risks" in analysis
        assert "mitigation_strategies" in analysis
    
    def test_generate_recommendations(self, analyzer):
        """Test recommendation generation"""
        mock_data = [
            {
                "source": {"id": "company-1", "name": "Company A", "type": "company"},
                "target": {"id": "company-2", "name": "Company B", "type": "company"},
                "relationship": {"type": "COMPETES_WITH", "properties": {"intensity": "high"}}
            }
        ]
        
        recommendations = analyzer._generate_recommendations(mock_data)
        
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)
    
    @pytest.mark.asyncio
    async def test_create_entity(self, analyzer):
        """Test entity creation"""
        entity_data = {
            "name": "Test Company",
            "entity_type": "company",
            "properties": {"industry": "technology", "size": "startup"}
        }
        
        # Mock Neo4j session
        mock_session = Mock()
        mock_transaction = Mock()
        mock_result = Mock()
        mock_result.single.return_value = {"id": "new-entity-123"}
        
        mock_transaction.run.return_value = mock_result
        mock_transaction.commit = AsyncMock()
        mock_transaction.close = Mock()
        
        analyzer.driver.session.return_value.__aenter__.return_value = mock_session
        analyzer.driver.session.return_value.__aexit__.return_value = None
        mock_session.begin_transaction.return_value = mock_transaction
        
        result = await analyzer.create_entity(**entity_data)
        
        assert result["id"] == "new-entity-123"
    
    @pytest.mark.asyncio
    async def test_create_relationship(self, analyzer):
        """Test relationship creation"""
        relationship_data = {
            "source_id": "company-1",
            "target_id": "company-2",
            "relationship_type": RelationshipType.COMPETES_WITH,
            "properties": {"intensity": "high"}
        }
        
        # Mock Neo4j session
        mock_session = Mock()
        mock_transaction = Mock()
        mock_result = Mock()
        mock_result.single.return_value = {"id": "new-rel-123"}
        
        mock_transaction.run.return_value = mock_result
        mock_transaction.commit = AsyncMock()
        mock_transaction.close = Mock()
        
        analyzer.driver.session.return_value.__aenter__.return_value = mock_session
        analyzer.driver.session.return_value.__aexit__.return_value = None
        mock_session.begin_transaction.return_value = mock_transaction
        
        result = await analyzer.create_relationship(**relationship_data)
        
        assert result["id"] == "new-rel-123"
    
    @pytest.mark.asyncio
    async def test_search_entities(self, analyzer):
        """Test entity search"""
        search_params = {"entity_type": "company", "industry": "technology"}
        
        # Mock Neo4j session
        mock_session = Mock()
        mock_transaction = Mock()
        mock_result = Mock()
        mock_result.data.return_value = [
            {"entity": {"id": "company-1", "name": "Company A", "type": "company"}}
        ]
        
        mock_transaction.run.return_value = mock_result
        mock_transaction.commit = AsyncMock()
        mock_transaction.close = Mock()
        
        analyzer.driver.session.return_value.__aenter__.return_value = mock_session
        analyzer.driver.session.return_value.__aexit__.return_value = None
        mock_session.begin_transaction.return_value = mock_transaction
        
        results = await analyzer.search_entities(search_params)
        
        assert len(results) > 0
        assert results[0]["id"] == "company-1"
    
    @pytest.mark.asyncio
    async def test_get_entity_details(self, analyzer):
        """Test getting entity details"""
        entity_id = "company-123"
        
        # Mock Neo4j session
        mock_session = Mock()
        mock_transaction = Mock()
        mock_result = Mock()
        mock_result.single.return_value = {
            "entity": {"id": "company-123", "name": "Company A", "type": "company"},
            "relationships": []
        }
        
        mock_transaction.run.return_value = mock_result
        mock_transaction.commit = AsyncMock()
        mock_transaction.close = Mock()
        
        analyzer.driver.session.return_value.__aenter__.return_value = mock_session
        analyzer.driver.session.return_value.__aexit__.return_value = None
        mock_session.begin_transaction.return_value = mock_transaction
        
        result = await analyzer.get_entity_details(entity_id)
        
        assert result["entity"]["id"] == "company-123"
        assert "relationships" in result
    
    def test_close_connection(self, analyzer):
        """Test closing Neo4j connection"""
        analyzer.close()
        
        # Verify close was called (if driver exists)
        if hasattr(analyzer, 'driver') and analyzer.driver:
            analyzer.driver.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
