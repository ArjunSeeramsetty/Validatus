#!/usr/bin/env python3
"""
Test Script: Market Data Enhancements Verification
Tests all LLM agents to ensure they work with current market focus and standardized formats.
"""

import asyncio
import json
import logging
from datetime import datetime
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.multi_llm_orchestrator import (
    MultiLLMOrchestrator, 
    OpenAIAgent, 
    AnthropicAgent, 
    PerplexityAgent, 
    GoogleGeminiAgent,
    ConsensusMethod
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketDataEnhancementTester:
    """Test class for verifying market data enhancements across all LLM agents"""
    
    def __init__(self):
        self.test_results = {}
        self.test_query = "Analyze the current market opportunities for electric vehicle adoption in emerging markets"
        self.test_context = {
            "industry": "automotive",
            "focus": "emerging_markets",
            "technology": "electric_vehicles",
            "timeframe": "current_market_conditions"
        }
    
    async def test_individual_agents(self):
        """Test each LLM agent individually"""
        logger.info("🧪 Testing Individual LLM Agents...")
        
        agents_to_test = [
            ("OpenAI", OpenAIAgent),
            ("Anthropic", AnthropicAgent),
            ("Perplexity", PerplexityAgent),
            ("Google Gemini", GoogleGeminiAgent)
        ]
        
        for agent_name, agent_class in agents_to_test:
            try:
                logger.info(f"Testing {agent_name} agent...")
                agent = agent_class()
                
                # Test the agent
                result = await agent.analyze(self.test_query, self.test_context)
                
                # Verify the result structure
                validation_result = self._validate_agent_result(result, agent_name)
                
                self.test_results[agent_name] = {
                    "status": "success" if validation_result["valid"] else "failed",
                    "validation": validation_result,
                    "result": result
                }
                
                logger.info(f"✅ {agent_name} agent test completed: {validation_result['valid']}")
                
            except Exception as e:
                logger.error(f"❌ {agent_name} agent test failed: {str(e)}")
                self.test_results[agent_name] = {
                    "status": "error",
                    "error": str(e),
                    "validation": {"valid": False, "issues": [f"Exception: {str(e)}"]}
                }
    
    def _validate_agent_result(self, result, agent_name):
        """Validate that an agent result meets all requirements"""
        issues = []
        
        # Check basic structure
        if not hasattr(result, 'model_name'):
            issues.append("Missing model_name attribute")
        if not hasattr(result, 'analysis'):
            issues.append("Missing analysis attribute")
        if not hasattr(result, 'confidence'):
            issues.append("Missing confidence attribute")
        if not hasattr(result, 'key_insights'):
            issues.append("Missing key_insights attribute")
        if not hasattr(result, 'recommendations'):
            issues.append("Missing recommendations attribute")
        if not hasattr(result, 'metadata'):
            issues.append("Missing metadata attribute")
        
        # Check metadata for market focus
        if hasattr(result, 'metadata') and result.metadata:
            if 'market_focus' not in result.metadata:
                issues.append("Missing market_focus in metadata")
            elif result.metadata['market_focus'] != 'current':
                issues.append(f"Expected market_focus='current', got '{result.metadata['market_focus']}'")
        
        # Check analysis content for current market focus
        if hasattr(result, 'analysis') and result.analysis:
            analysis_lower = result.analysis.lower()
            current_market_indicators = [
                'current', 'recent', 'present', 'today', 'now', 'latest',
                '2024', '2025', 'emerging', 'trending', 'volatility',
                'market conditions', 'economic conditions'
            ]
            
            if not any(indicator in analysis_lower for indicator in current_market_indicators):
                issues.append("Analysis doesn't appear to focus on current market conditions")
        
        # Check confidence score
        if hasattr(result, 'confidence'):
            if not isinstance(result.confidence, (int, float)):
                issues.append("Confidence score is not numeric")
            elif result.confidence < 0 or result.confidence > 1:
                issues.append(f"Confidence score {result.confidence} is outside valid range [0,1]")
        
        # Check insights and recommendations
        if hasattr(result, 'key_insights') and result.key_insights:
            if not isinstance(result.key_insights, list):
                issues.append("key_insights is not a list")
            elif len(result.key_insights) == 0:
                issues.append("key_insights list is empty")
        
        if hasattr(result, 'recommendations') and result.recommendations:
            if not isinstance(result.recommendations, list):
                issues.append("recommendations is not a list")
            elif len(result.recommendations) == 0:
                issues.append("recommendations list is empty")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "score": max(0, 10 - len(issues))  # 10 points, -1 for each issue
        }
    
    async def test_multi_llm_orchestrator(self):
        """Test the MultiLLMOrchestrator with all agents"""
        logger.info("🧪 Testing MultiLLM Orchestrator...")
        
        try:
            orchestrator = MultiLLMOrchestrator(consensus_method=ConsensusMethod.CONFIDENCE_BASED)
            
            # Test capabilities
            capabilities = await orchestrator.get_capabilities()
            logger.info(f"Orchestrator capabilities: {capabilities}")
            
            # Test consensus analysis
            consensus_result = await orchestrator.consensus_analysis(self.test_query, self.test_context)
            
            # Validate consensus result
            validation_result = self._validate_consensus_result(consensus_result)
            
            self.test_results["MultiLLM_Orchestrator"] = {
                "status": "success" if validation_result["valid"] else "failed",
                "validation": validation_result,
                "capabilities": capabilities,
                "consensus_result": consensus_result
            }
            
            logger.info(f"✅ MultiLLM Orchestrator test completed: {validation_result['valid']}")
            
        except Exception as e:
            logger.error(f"❌ MultiLLM Orchestrator test failed: {str(e)}")
            self.test_results["MultiLLM_Orchestrator"] = {
                "status": "error",
                "error": str(e),
                "validation": {"valid": False, "issues": [f"Exception: {str(e)}"]}
            }
    
    def _validate_consensus_result(self, consensus_result):
        """Validate the consensus analysis result"""
        issues = []
        
        # Check basic structure
        required_fields = ['consensus', 'individual_results', 'consensus_method', 'timestamp']
        for field in required_fields:
            if field not in consensus_result:
                issues.append(f"Missing required field: {field}")
        
        # Check market focus
        if 'market_focus' in consensus_result:
            if consensus_result['market_focus'] != 'current':
                issues.append(f"Expected market_focus='current', got '{consensus_result['market_focus']}'")
        else:
            issues.append("Missing market_focus in consensus result")
        
        # Check individual results
        if 'individual_results' in consensus_result and consensus_result['individual_results']:
            for i, result in enumerate(consensus_result['individual_results']):
                if 'model_name' not in result:
                    issues.append(f"Individual result {i} missing model_name")
                if 'confidence' not in result:
                    issues.append(f"Individual result {i} missing confidence")
        
        # Check consensus analysis content
        if 'consensus' in consensus_result and consensus_result['consensus']:
            consensus_text = consensus_result['consensus'].get('analysis', '')
            if 'current market' not in consensus_text.lower() and 'current market focus' not in consensus_text.lower():
                issues.append("Consensus analysis doesn't emphasize current market focus")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "score": max(0, 10 - len(issues))
        }
    
    async def test_system_integration(self):
        """Test the complete system integration"""
        logger.info("🧪 Testing Complete System Integration...")
        
        try:
            # Test with a different query to ensure variety
            test_query_2 = "What are the current strategic implications of AI regulation in the financial services sector?"
            test_context_2 = {
                "sector": "financial_services",
                "technology": "artificial_intelligence",
                "focus": "regulatory_impact",
                "timeframe": "current_conditions"
            }
            
            orchestrator = MultiLLMOrchestrator(consensus_method=ConsensusMethod.MAJORITY_VOTE)
            
            # Test different consensus methods
            consensus_result = await orchestrator.consensus_analysis(test_query_2, test_context_2)
            
            # Validate the result
            validation_result = self._validate_consensus_result(consensus_result)
            
            self.test_results["System_Integration"] = {
                "status": "success" if validation_result["valid"] else "failed",
                "validation": validation_result,
                "query": test_query_2,
                "context": test_context_2,
                "consensus_result": consensus_result
            }
            
            logger.info(f"✅ System Integration test completed: {validation_result['valid']}")
            
        except Exception as e:
            logger.error(f"❌ System Integration test failed: {str(e)}")
            self.test_results["System_Integration"] = {
                "status": "error",
                "error": str(e),
                "validation": {"valid": False, "issues": [f"Exception: {str(e)}"]}
            }
    
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        logger.info("📊 Generating Test Report...")
        
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "test_query": self.test_query,
            "test_context": self.test_context,
            "overall_status": "PASS" if all(r["status"] == "success" for r in self.test_results.values()) else "FAIL",
            "test_results": self.test_results,
            "summary": {}
        }
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results.values() if r["status"] == "success")
        failed_tests = sum(1 for r in self.test_results.values() if r["status"] == "failed")
        error_tests = sum(1 for r in self.test_results.values() if r["status"] == "error")
        
        report["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "success_rate": f"{(successful_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%"
        }
        
        # Save report to file
        report_filename = f"market_data_enhancement_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"📄 Test report saved to: {report_filename}")
        
        return report
    
    def print_test_summary(self):
        """Print a summary of test results"""
        print("\n" + "="*80)
        print("🧪 MARKET DATA ENHANCEMENT TEST RESULTS")
        print("="*80)
        
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "success" else "❌" if result["status"] == "failed" else "⚠️"
            print(f"{status_emoji} {test_name}: {result['status'].upper()}")
            
            if "validation" in result and "score" in result["validation"]:
                print(f"   Score: {result['validation']['score']}/10")
            
            if "validation" in result and "issues" in result["validation"] and result["validation"]["issues"]:
                print(f"   Issues: {', '.join(result['validation']['issues'])}")
            
            if "error" in result:
                print(f"   Error: {result['error']}")
            
            print()
        
        # Overall summary
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results.values() if r["status"] == "success")
        success_rate = (successful_tests/total_tests)*100 if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {successful_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate == 100:
            print("🎉 ALL TESTS PASSED! Market data enhancements are working correctly.")
        elif success_rate >= 80:
            print("👍 Most tests passed. Some minor issues to address.")
        else:
            print("⚠️  Multiple test failures detected. Review and fix issues.")
        
        print("="*80)

async def main():
    """Main test execution function"""
    logger.info("🚀 Starting Market Data Enhancement Testing...")
    
    tester = MarketDataEnhancementTester()
    
    try:
        # Run all tests
        await tester.test_individual_agents()
        await tester.test_multi_llm_orchestrator()
        await tester.test_system_integration()
        
        # Generate and display results
        report = tester.generate_test_report()
        tester.print_test_summary()
        
        logger.info("🏁 Testing completed!")
        
        return report
        
    except Exception as e:
        logger.error(f"❌ Testing failed with exception: {str(e)}")
        return None

if __name__ == "__main__":
    # Run the tests
    try:
        report = asyncio.run(main())
        if report:
            print(f"\n📄 Detailed test report available in the generated JSON file.")
        else:
            print("\n❌ Testing failed. Check logs for details.")
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
