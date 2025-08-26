import asyncio
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime
import json
import logging
from dataclasses import dataclass
from enum import Enum
import numpy as np
from config import settings

class RelationshipType(Enum):
    """Types of relationships in the knowledge graph"""
    COMPETES_WITH = "COMPETES_WITH"
    SUPPLIES_TO = "SUPPLIES_TO"
    PARTNERS_WITH = "PARTNERS_WITH"
    ACQUIRES = "ACQUIRES"
    INVESTED_IN = "INVESTED_IN"
    SIMILAR_TO = "SIMILAR_TO"
    OPPOSES = "OPPOSES"
    INFLUENCES = "INFLUENCES"
    DEPENDS_ON = "DEPENDS_ON"
    EMERGES_FROM = "EMERGES_FROM"

@dataclass
class GraphEntity:
    """Entity in the knowledge graph"""
    id: str
    name: str
    type: str
    properties: Dict[str, Any]
    confidence: float
    created_at: datetime
    updated_at: datetime

@dataclass
class GraphRelationship:
    """Relationship between entities in the knowledge graph"""
    id: str
    source_id: str
    target_id: str
    type: RelationshipType
    properties: Dict[str, Any]
    strength: float
    confidence: float
    created_at: datetime

@dataclass
class MarketInsight:
    """Market insight derived from graph analysis"""
    insight_type: str
    description: str
    entities_involved: List[str]
    confidence: float
    supporting_evidence: List[str]
    strategic_implications: List[str]
    risk_level: str
    opportunity_level: str

class KnowledgeGraphAnalyzer:
    """Use graph database for relationship analysis and strategic insights"""
    
    def __init__(self):
        self.logger = logging.getLogger("knowledge_graph.analyzer")
        self.neo4j_uri = getattr(settings, 'NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = getattr(settings, 'NEO4J_USER', 'neo4j')
        self.neo4j_password = getattr(settings, 'NEO4J_PASSWORD', 'password')
        self.driver = None
        
        # Initialize connection
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize Neo4j connection"""
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            self.logger.info("Neo4j connection established")
        except ImportError:
            self.logger.warning("Neo4j driver not available. Install with: pip install neo4j")
            self.driver = None
        except Exception as e:
            self.logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None
    
    async def relationship_analysis(self, entities: List[str], depth: int = 2) -> Dict[str, Any]:
        """Analyze relationships between entities in the knowledge graph"""
        try:
            if not self.driver:
                self.logger.warning("Neo4j connection not available - using fallback analysis")
                return await self._fallback_relationship_analysis(entities)
            
            # Build knowledge graph for the entities
            graph_data = await self._build_entity_graph(entities, depth)
            
            # Analyze relationships
            relationship_insights = await self._analyze_relationships(graph_data)
            
            # Generate strategic insights
            strategic_insights = await self._generate_strategic_insights(graph_data, relationship_insights)
            
            # Calculate market positioning
            market_positioning = await self._calculate_market_positioning(graph_data)
            
            # Identify opportunities and risks
            opportunities_risks = await self._identify_opportunities_risks(graph_data, strategic_insights)
            
            return {
                "entities": entities,
                "graph_data": graph_data,
                "relationship_insights": relationship_insights,
                "strategic_insights": strategic_insights,
                "market_positioning": market_positioning,
                "opportunities_risks": opportunities_risks,
                "analysis_depth": depth,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Relationship analysis failed: {str(e)}")
            self.logger.info("Falling back to basic entity analysis")
            return await self._fallback_relationship_analysis(entities)
    
    async def _build_entity_graph(self, entities: List[str], depth: int) -> Dict[str, Any]:
        """Build a subgraph around the specified entities"""
        try:
            with self.driver.session() as session:
                # Cypher query to build the subgraph
                query = """
                MATCH (e:Entity)
                WHERE e.name IN $entities
                WITH e
                CALL apoc.path.subgraphNodes(e, {
                    maxLevel: $depth,
                    relationshipFilter: 'COMPETES_WITH|SUPPLIES_TO|PARTNERS_WITH|ACQUIRES|INVESTED_IN|SIMILAR_TO|OPPOSES|INFLUENCES|DEPENDS_ON|EMERGES_FROM'
                })
                YIELD node
                RETURN DISTINCT node
                """
                
                result = session.run(query, entities=entities, depth=depth)
                nodes = [record["node"] for record in result]
                
                # Get relationships between these nodes
                relationship_query = """
                MATCH (source:Entity)-[r]->(target:Entity)
                WHERE source.name IN $entities OR target.name IN $entities
                RETURN source.name as source, type(r) as type, target.name as target, r.strength as strength, r.confidence as confidence
                """
                
                rel_result = session.run(relationship_query, entities=entities)
                relationships = [dict(record) for record in rel_result]
                
                return {
                    "nodes": [self._node_to_dict(node) for node in nodes],
                    "relationships": relationships,
                    "total_nodes": len(nodes),
                    "total_relationships": len(relationships)
                }
                
        except Exception as e:
            self.logger.error(f"Failed to build entity graph: {e}")
            return {"nodes": [], "relationships": [], "error": str(e)}
    
    def _node_to_dict(self, node):
        """Convert Neo4j node to dictionary"""
        try:
            return {
                "id": node.id,
                "labels": list(node.labels),
                "properties": dict(node),
                "name": node.get("name", "Unknown")
            }
        except Exception:
            return {"id": "unknown", "labels": [], "properties": {}, "name": "Unknown"}
    
    async def _analyze_relationships(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the relationships in the graph"""
        try:
            relationships = graph_data.get("relationships", [])
            
            if not relationships:
                return {"error": "No relationships found"}
            
            # Analyze relationship types
            relationship_types = {}
            for rel in relationships:
                rel_type = rel.get("type", "UNKNOWN")
                if rel_type not in relationship_types:
                    relationship_types[rel_type] = []
                relationship_types[rel_type].append(rel)
            
            # Calculate relationship strength distribution
            strengths = [rel.get("strength", 0.5) for rel in relationships]
            avg_strength = np.mean(strengths) if strengths else 0.5
            
            # Calculate confidence distribution
            confidences = [rel.get("confidence", 0.5) for rel in relationships]
            avg_confidence = np.mean(confidences) if confidences else 0.5
            
            # Identify key relationships
            key_relationships = sorted(
                relationships,
                key=lambda x: (x.get("strength", 0) * x.get("confidence", 0)),
                reverse=True
            )[:10]
            
            return {
                "relationship_types": {k: len(v) for k, v in relationship_types.items()},
                "total_relationships": len(relationships),
                "average_strength": avg_strength,
                "average_confidence": avg_confidence,
                "key_relationships": key_relationships,
                "strength_distribution": {
                    "high": len([r for r in relationships if r.get("strength", 0) > 0.7]),
                    "medium": len([r for r in relationships if 0.3 <= r.get("strength", 0) <= 0.7]),
                    "low": len([r for r in relationships if r.get("strength", 0) < 0.3])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Relationship analysis failed: {e}")
            return {"error": str(e)}
    
    async def _generate_strategic_insights(self, graph_data: Dict[str, Any], relationship_insights: Dict[str, Any]) -> List[MarketInsight]:
        """Generate strategic insights from graph analysis"""
        try:
            insights = []
            nodes = graph_data.get("nodes", [])
            relationships = graph_data.get("relationships", [])
            
            if not nodes or not relationships:
                return insights
            
            # Insight 1: Competitive Landscape
            competitive_insight = self._analyze_competitive_landscape(nodes, relationships)
            if competitive_insight:
                insights.append(competitive_insight)
            
            # Insight 2: Partnership Opportunities
            partnership_insight = self._analyze_partnership_opportunities(nodes, relationships)
            if partnership_insight:
                insights.append(partnership_insight)
            
            # Insight 3: Market Entry Barriers
            barrier_insight = self._analyze_market_entry_barriers(nodes, relationships)
            if barrier_insight:
                insights.append(barrier_insight)
            
            # Insight 4: Supply Chain Analysis
            supply_chain_insight = self._analyze_supply_chain(nodes, relationships)
            if supply_chain_insight:
                insights.append(supply_chain_insight)
            
            # Insight 5: Innovation Clusters
            innovation_insight = self._analyze_innovation_clusters(nodes, relationships)
            if innovation_insight:
                insights.append(innovation_insight)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Strategic insight generation failed: {e}")
            return []
    
    def _analyze_competitive_landscape(self, nodes: List[Dict], relationships: List[Dict]) -> Optional[MarketInsight]:
        """Analyze competitive landscape from graph data"""
        try:
            # Find competitive relationships
            competitive_rels = [r for r in relationships if r.get("type") == "COMPETES_WITH"]
            
            if not competitive_rels:
                return None
            
            # Identify key competitors
            competitors = set()
            for rel in competitive_rels:
                competitors.add(rel.get("source"))
                competitors.add(rel.get("target"))
            
            # Calculate competitive intensity
            competitive_intensity = len(competitive_rels) / max(len(nodes), 1)
            
            # Determine risk level
            if competitive_intensity > 0.5:
                risk_level = "High"
            elif competitive_intensity > 0.2:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            return MarketInsight(
                insight_type="Competitive Landscape",
                description=f"Identified {len(competitors)} competitors with {len(competitive_rels)} competitive relationships",
                entities_involved=list(competitors),
                confidence=0.8,
                supporting_evidence=[f"Found {len(competitive_rels)} competitive relationships"],
                strategic_implications=[
                    "High competitive intensity requires differentiation strategy",
                    "Monitor competitor movements closely",
                    "Consider strategic partnerships to reduce competition"
                ],
                risk_level=risk_level,
                opportunity_level="Medium" if risk_level == "High" else "High"
            )
            
        except Exception as e:
            self.logger.error(f"Competitive landscape analysis failed: {e}")
            return None
    
    def _analyze_partnership_opportunities(self, nodes: List[Dict], relationships: List[Dict]) -> Optional[MarketInsight]:
        """Analyze partnership opportunities from graph data"""
        try:
            # Find partnership relationships
            partnership_rels = [r for r in relationships if r.get("type") == "PARTNERS_WITH"]
            
            if not partnership_rels:
                return None
            
            # Identify potential partners
            partners = set()
            for rel in partnership_rels:
                partners.add(rel.get("source"))
                partners.add(rel.get("target"))
            
            # Calculate partnership density
            partnership_density = len(partnership_rels) / max(len(nodes), 1)
            
            return MarketInsight(
                insight_type="Partnership Opportunities",
                description=f"Identified {len(partners)} entities with {len(partnership_rels)} partnership relationships",
                entities_involved=list(partners),
                confidence=0.7,
                supporting_evidence=[f"Found {len(partnership_rels)} partnership relationships"],
                strategic_implications=[
                    "High partnership density indicates collaborative ecosystem",
                    "Consider strategic alliances with key partners",
                    "Leverage existing partnerships for market expansion"
                ],
                risk_level="Low",
                opportunity_level="High"
            )
            
        except Exception as e:
            self.logger.error(f"Partnership analysis failed: {e}")
            return None
    
    def _analyze_market_entry_barriers(self, nodes: List[Dict], relationships: List[Dict]) -> Optional[MarketInsight]:
        """Analyze market entry barriers from graph data"""
        try:
            # Find strong relationships that might indicate barriers
            strong_rels = [r for r in relationships if r.get("strength", 0) > 0.7]
            
            if not strong_rels:
                return None
            
            # Identify barrier types
            barrier_indicators = {
                "high_strength_relationships": len(strong_rels),
                "established_players": len(set([r.get("source") for r in strong_rels] + [r.get("target") for r in strong_rels]))
            }
            
            # Determine barrier level
            if barrier_indicators["high_strength_relationships"] > 10:
                barrier_level = "High"
            elif barrier_indicators["high_strength_relationships"] > 5:
                barrier_level = "Medium"
            else:
                barrier_level = "Low"
            
            return MarketInsight(
                insight_type="Market Entry Barriers",
                description=f"Identified {barrier_indicators['high_strength_relationships']} strong relationships indicating potential entry barriers",
                entities_involved=list(set([r.get("source") for r in strong_rels] + [r.get("target") for r in strong_rels])),
                confidence=0.6,
                supporting_evidence=[
                    f"Found {barrier_indicators['high_strength_relationships']} high-strength relationships",
                    f"Identified {barrier_indicators['established_players']} established players"
                ],
                strategic_implications=[
                    "High barriers require significant resources for market entry",
                    "Consider acquisition strategy to overcome barriers",
                    "Focus on underserved market segments"
                ],
                risk_level=barrier_level,
                opportunity_level="Low" if barrier_level == "High" else "Medium"
            )
            
        except Exception as e:
            self.logger.error(f"Market entry barrier analysis failed: {e}")
            return None
    
    def _analyze_supply_chain(self, nodes: List[Dict], relationships: List[Dict]) -> Optional[MarketInsight]:
        """Analyze supply chain from graph data"""
        try:
            # Find supply relationships
            supply_rels = [r for r in relationships if r.get("type") == "SUPPLIES_TO"]
            
            if not supply_rels:
                return None
            
            # Identify supply chain structure
            suppliers = set([r.get("source") for r in supply_rels])
            customers = set([r.get("target") for r in supply_rels])
            
            # Calculate supply chain complexity
            complexity = len(supply_rels) / max(len(nodes), 1)
            
            return MarketInsight(
                insight_type="Supply Chain Analysis",
                description=f"Identified {len(suppliers)} suppliers and {len(customers)} customers in supply chain",
                entities_involved=list(suppliers | customers),
                confidence=0.7,
                supporting_evidence=[f"Found {len(supply_rels)} supply relationships"],
                strategic_implications=[
                    "Complex supply chain requires robust risk management",
                    "Consider vertical integration opportunities",
                    "Diversify supplier base to reduce dependency"
                ],
                risk_level="Medium" if complexity > 0.3 else "Low",
                opportunity_level="Medium"
            )
            
        except Exception as e:
            self.logger.error(f"Supply chain analysis failed: {e}")
            return None
    
    def _analyze_innovation_clusters(self, nodes: List[Dict], relationships: List[Dict]) -> Optional[MarketInsight]:
        """Analyze innovation clusters from graph data"""
        try:
            # Find innovation-related relationships
            innovation_rels = [r for r in relationships if r.get("type") in ["INFLUENCES", "EMERGES_FROM", "DEPENDS_ON"]]
            
            if not innovation_rels:
                return None
            
            # Identify innovation clusters
            innovation_entities = set()
            for rel in innovation_rels:
                innovation_entities.add(rel.get("source"))
                innovation_entities.add(rel.get("target"))
            
            # Calculate innovation density
            innovation_density = len(innovation_rels) / max(len(nodes), 1)
            
            return MarketInsight(
                insight_type="Innovation Clusters",
                description=f"Identified {len(innovation_entities)} entities in innovation ecosystem",
                entities_involved=list(innovation_entities),
                confidence=0.6,
                supporting_evidence=[f"Found {len(innovation_rels)} innovation-related relationships"],
                strategic_implications=[
                    "High innovation density indicates growth potential",
                    "Consider R&D partnerships with innovation leaders",
                    "Monitor emerging technologies and trends"
                ],
                risk_level="Low",
                opportunity_level="High" if innovation_density > 0.2 else "Medium"
            )
            
        except Exception as e:
            self.logger.error(f"Innovation cluster analysis failed: {e}")
            return None
    
    async def _calculate_market_positioning(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market positioning metrics"""
        try:
            nodes = graph_data.get("nodes", [])
            relationships = graph_data.get("relationships", [])
            
            if not nodes:
                return {"error": "No nodes available for positioning analysis"}
            
            # Calculate centrality metrics
            centrality_scores = {}
            for node in nodes:
                node_name = node.get("name", "Unknown")
                
                # Calculate degree centrality (number of connections)
                connections = len([r for r in relationships 
                                if r.get("source") == node_name or r.get("target") == node_name])
                
                # Calculate strength centrality (sum of relationship strengths)
                strength_sum = sum([r.get("strength", 0) for r in relationships 
                                  if r.get("source") == node_name or r.get("target") == node_name])
                
                centrality_scores[node_name] = {
                    "degree_centrality": connections,
                    "strength_centrality": strength_sum,
                    "normalized_centrality": connections / max(len(nodes) - 1, 1)
                }
            
            # Identify market leaders
            market_leaders = sorted(
                centrality_scores.items(),
                key=lambda x: x[1]["strength_centrality"],
                reverse=True
            )[:5]
            
            return {
                "centrality_scores": centrality_scores,
                "market_leaders": market_leaders,
                "total_entities": len(nodes),
                "average_centrality": np.mean([score["normalized_centrality"] for score in centrality_scores.values()])
            }
            
        except Exception as e:
            self.logger.error(f"Market positioning calculation failed: {e}")
            return {"error": str(e)}
    
    async def _identify_opportunities_risks(self, graph_data: Dict[str, Any], strategic_insights: List[MarketInsight]) -> Dict[str, Any]:
        """Identify opportunities and risks from analysis"""
        try:
            opportunities = []
            risks = []
            
            # Extract opportunities and risks from strategic insights
            for insight in strategic_insights:
                if insight.opportunity_level == "High":
                    opportunities.append({
                        "type": insight.insight_type,
                        "description": insight.description,
                        "confidence": insight.confidence,
                        "implications": insight.strategic_implications
                    })
                
                if insight.risk_level in ["High", "Medium"]:
                    risks.append({
                        "type": insight.insight_type,
                        "description": insight.description,
                        "confidence": insight.confidence,
                        "mitigation": insight.strategic_implications
                    })
            
            # Calculate overall opportunity and risk scores
            opportunity_score = len([o for o in opportunities if o["confidence"] > 0.7]) / max(len(opportunities), 1)
            risk_score = len([r for r in risks if r["confidence"] > 0.7]) / max(len(risks), 1)
            
            return {
                "opportunities": opportunities,
                "risks": risks,
                "opportunity_score": opportunity_score,
                "risk_score": risk_score,
                "total_opportunities": len(opportunities),
                "total_risks": len(risks),
                "recommendations": self._generate_recommendations(opportunities, risks)
            }
            
        except Exception as e:
            self.logger.error(f"Opportunity/risk identification failed: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, opportunities: List[Dict], risks: List[Dict]) -> List[str]:
        """Generate strategic recommendations based on opportunities and risks"""
        recommendations = []
        
        # High opportunity recommendations
        if len(opportunities) > 3:
            recommendations.append("Market shows high growth potential - consider aggressive expansion strategy")
        
        if any(o["confidence"] > 0.8 for o in opportunities):
            recommendations.append("High-confidence opportunities identified - prioritize resource allocation")
        
        # Risk mitigation recommendations
        if len(risks) > 5:
            recommendations.append("High risk environment - implement comprehensive risk management strategy")
        
        if any(r["risk_level"] == "High" for r in risks):
            recommendations.append("Critical risks identified - develop contingency plans and mitigation strategies")
        
        # Balanced approach
        if len(opportunities) > 0 and len(risks) > 0:
            recommendations.append("Balanced approach recommended - pursue opportunities while managing risks")
        
        return recommendations
    
    async def create_entity(self, name: str, entity_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entity in the knowledge graph"""
        try:
            if not self.driver:
                return {"error": "Neo4j connection not available"}
            
            with self.driver.session() as session:
                query = """
                CREATE (e:Entity {
                    name: $name,
                    type: $type,
                    properties: $properties,
                    created_at: datetime(),
                    updated_at: datetime(),
                    confidence: $confidence
                })
                RETURN e
                """
                
                result = session.run(
                    query,
                    name=name,
                    type=entity_type,
                    properties=json.dumps(properties),
                    confidence=properties.get("confidence", 0.8)
                )
                
                node = result.single()["e"]
                return {
                    "success": True,
                    "entity": self._node_to_dict(node),
                    "message": f"Entity '{name}' created successfully"
                }
                
        except Exception as e:
            self.logger.error(f"Entity creation failed: {e}")
            return {"error": str(e)}
    
    async def create_relationship(self, source: str, target: str, relationship_type: RelationshipType, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a relationship between two entities"""
        try:
            if not self.driver:
                return {"error": "Neo4j connection not available"}
            
            with self.driver.session() as session:
                query = """
                MATCH (source:Entity {name: $source})
                MATCH (target:Entity {name: $target})
                CREATE (source)-[r:RELATIONSHIP {
                    type: $type,
                    properties: $properties,
                    strength: $strength,
                    confidence: $confidence,
                    created_at: datetime()
                }]->(target)
                RETURN r
                """
                
                result = session.run(
                    query,
                    source=source,
                    target=target,
                    type=relationship_type.value,
                    properties=json.dumps(properties),
                    strength=properties.get("strength", 0.5),
                    confidence=properties.get("confidence", 0.8)
                )
                
                relationship = result.single()["r"]
                return {
                    "success": True,
                    "relationship": {
                        "id": relationship.id,
                        "type": relationship.get("type"),
                        "properties": dict(relationship)
                    },
                    "message": f"Relationship created between '{source}' and '{target}'"
                }
                
        except Exception as e:
            self.logger.error(f"Relationship creation failed: {e}")
            return {"error": str(e)}
    
    async def search_entities(self, query: str, entity_type: str = None, limit: int = 10) -> Dict[str, Any]:
        """Search for entities in the knowledge graph"""
        try:
            if not self.driver:
                return {"error": "Neo4j connection not available"}
            
            with self.driver.session() as session:
                if entity_type:
                    search_query = """
                    MATCH (e:Entity)
                    WHERE e.name CONTAINS $query AND e.type = $entity_type
                    RETURN e
                    LIMIT $limit
                    """
                    result = session.run(search_query, query=query, entity_type=entity_type, limit=limit)
                else:
                    search_query = """
                    MATCH (e:Entity)
                    WHERE e.name CONTAINS $query
                    RETURN e
                    LIMIT $limit
                    """
                    result = session.run(search_query, query=query, limit=limit)
                
                entities = [self._node_to_dict(record["e"]) for record in result]
                
                return {
                    "query": query,
                    "entity_type": entity_type,
                    "results": entities,
                    "total_found": len(entities)
                }
                
        except Exception as e:
            self.logger.error(f"Entity search failed: {e}")
            return {"error": str(e)}
    
    async def get_entity_details(self, entity_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific entity"""
        try:
            if not self.driver:
                return {"error": "Neo4j connection not available"}
            
            with self.driver.session() as session:
                # Get entity details
                entity_query = """
                MATCH (e:Entity {name: $name})
                RETURN e
                """
                entity_result = session.run(entity_query, name=entity_name)
                entity = entity_result.single()
                
                if not entity:
                    return {"error": f"Entity '{entity_name}' not found"}
                
                # Get incoming relationships
                incoming_query = """
                MATCH (source:Entity)-[r]->(target:Entity {name: $name})
                RETURN source.name as source, type(r) as type, r.strength as strength
                """
                incoming_result = session.run(incoming_query, name=entity_name)
                incoming_rels = [dict(record) for record in incoming_result]
                
                # Get outgoing relationships
                outgoing_query = """
                MATCH (source:Entity {name: $name})-[r]->(target:Entity)
                RETURN target.name as target, type(r) as type, r.strength as strength
                """
                outgoing_result = session.run(outgoing_query, name=entity_name)
                outgoing_rels = [dict(record) for record in outgoing_result]
                
                return {
                    "entity": self._node_to_dict(entity["e"]),
                    "incoming_relationships": incoming_rels,
                    "outgoing_relationships": outgoing_rels,
                    "total_relationships": len(incoming_rels) + len(outgoing_rels)
                }
                
        except Exception as e:
            self.logger.error(f"Entity details retrieval failed: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of the knowledge graph system"""
        try:
            if not self.driver:
                return {
                    "status": "unhealthy",
                    "error": "Neo4j connection not available",
                    "timestamp": datetime.now().isoformat()
                }
            
            with self.driver.session() as session:
                # Simple health check query
                result = session.run("RETURN 1 as health_check")
                health_result = result.single()
                
                if health_result and health_result["health_check"] == 1:
                    return {
                        "status": "healthy",
                        "neo4j_connection": "active",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "degraded",
                        "neo4j_connection": "unstable",
                        "timestamp": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _fallback_relationship_analysis(self, entities: List[str]) -> Dict[str, Any]:
        """Fallback analysis when Neo4j is not available"""
        try:
            self.logger.info("Performing fallback relationship analysis without Neo4j")
            
            # Basic entity analysis
            entity_insights = []
            for entity in entities:
                entity_insights.append({
                    "entity": entity,
                    "type": "business_entity",
                    "confidence": 0.7,
                    "source": "fallback_analysis"
                })
            
            # Generate basic strategic insights
            strategic_insights = [
                "Entity relationships analyzed using fallback method",
                "Consider implementing Neo4j for enhanced relationship mapping",
                "Basic entity analysis completed successfully"
            ]
            
            # Basic market positioning
            market_positioning = {
                "position": "analyzed",
                "confidence": 0.6,
                "method": "fallback_analysis"
            }
            
            # Basic opportunities and risks
            opportunities_risks = {
                "opportunities": ["Enhanced analysis available with Neo4j implementation"],
                "risks": ["Limited relationship depth without graph database"],
                "confidence": 0.5
            }
            
            return {
                "entities": entities,
                "graph_data": {"status": "fallback_mode", "nodes": entity_insights},
                "relationship_insights": {"method": "fallback", "insights": entity_insights},
                "strategic_insights": strategic_insights,
                "market_positioning": market_positioning,
                "opportunities_risks": opportunities_risks,
                "analysis_depth": 1,
                "fallback_mode": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Fallback analysis failed: {str(e)}")
            return {
                "error": f"Both primary and fallback analysis failed: {str(e)}",
                "entities": entities,
                "timestamp": datetime.now().isoformat()
            }
    
    async def close(self):
        """Close the Neo4j connection"""
        if self.driver:
            self.driver.close()
            self.logger.info("Neo4j connection closed")
