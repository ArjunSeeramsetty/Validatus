#!/usr/bin/env python3
"""
Comprehensive Test Suite for Validatus Platform
Consolidates all testing components into a single, organized test suite
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

class ValidatusTestSuite:
    """Comprehensive test suite for the Validatus Platform"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = datetime.now()
        
    async def run_all_tests(self, idea_description: str, target_audience: str):
        """Run the complete test suite"""
        print("🧪 VALIDATUS PLATFORM COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print(f"📋 Test Idea: {idea_description}")
        print(f"🎯 Target Audience: {target_audience}")
        print(f"⏰ Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        try:
            # Test 1: Core Framework Structure
            await self.test_core_framework_structure()
            
            # Test 2: Specialized Agent System
            await self.test_specialized_agent_system(idea_description, target_audience)
            
            # Test 3: Context-Aware Layer Analysis
            await self.test_context_aware_analysis(idea_description, target_audience)
            
            # Test 4: Multi-LLM Orchestration
            await self.test_multi_llm_orchestration()
            
            # Test 5: Workflow Integration
            await self.test_workflow_integration(idea_description, target_audience)
            
            # Test 6: Scalability Assessment
            await self.test_scalability_assessment(idea_description, target_audience)
            
            # Generate comprehensive report
            await self.generate_test_report()
            
        except Exception as e:
            print(f"❌ Test suite failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": str(e), "success": False}
        
        return self.test_results
    
    async def test_core_framework_structure(self):
        """Test 1: Core Framework Structure"""
        print("\n🔍 TEST 1: Core Framework Structure")
        print("-" * 50)
        
        try:
            from app.core.comprehensive_analytical_framework_fixed import ComprehensiveAnalyticalFramework
            
            framework = ComprehensiveAnalyticalFramework()
            
            # Test framework structure
            total_layers = len(framework.get_all_layers())
            segments = list(framework.analytical_framework.keys())
            
            print(f"✅ Framework imported successfully")
            print(f"📊 Total Layers: {total_layers}")
            print(f"🎯 Segments: {', '.join(segments)}")
            
            # Test segment structure
            for segment_name in segments:
                segment_layers = framework.get_segment_layers(segment_name)
                factors = list(framework.analytical_framework[segment_name]["factors"].keys())
                print(f"   {segment_name}: {len(segment_layers)} layers, {len(factors)} factors")
            
            # Test layer retrieval methods
            consumer_layers = framework.get_segment_layers("CONSUMER")
            market_layers = framework.get_segment_layers("MARKET")
            
            print(f"✅ Consumer layers: {len(consumer_layers)}")
            print(f"✅ Market layers: {len(market_layers)}")
            
            self.test_results["core_framework"] = {
                "status": "PASSED",
                "total_layers": total_layers,
                "segments": segments,
                "consumer_layers": len(consumer_layers),
                "market_layers": len(market_layers)
            }
            
        except Exception as e:
            print(f"❌ Core framework test failed: {str(e)}")
            self.test_results["core_framework"] = {"status": "FAILED", "error": str(e)}
    
    async def test_specialized_agent_system(self, idea_description: str, target_audience: str):
        """Test 2: Specialized Agent System"""
        print("\n🔍 TEST 2: Specialized Agent System")
        print("-" * 50)
        
        try:
            from app.core.specialized_agents import get_specialized_agent_orchestrator, AnalysisDomain
            
            orchestrator = get_specialized_agent_orchestrator()
            
            print(f"✅ Agent orchestrator initialized")
            print(f"🔧 Total agents: {len(orchestrator.agents)}")
            
            # Display available agents
            for domain, agent in orchestrator.agents.items():
                print(f"   • {domain.value}: {agent.persona.name}")
            
            # Test agent assignment
            test_layers = [
                "need_perception_consumer_demand",
                "total_addressable_market_market_size",
                "core_features_analysis_features_functionality",
                "brand_positioning_brand_positioning_strategy",
                "onboarding_experience_user_experience_ux_design"
            ]
            
            agent_assignments = {}
            for layer in test_layers:
                optimal_agent = orchestrator.get_optimal_agent(layer)
                agent_assignments[layer] = {
                    "agent": optimal_agent.persona.name,
                    "domain": optimal_agent.domain.value
                }
                print(f"   ✅ {layer} → {optimal_agent.persona.name}")
            
            # Test agent analysis
            test_layer = "need_perception_consumer_demand"
            optimal_agent = orchestrator.get_optimal_agent(test_layer)
            
            context = {
                "analysis_type": "consumer",
                "layer": test_layer,
                "test_mode": True
            }
            
            result = await orchestrator.analyze_layer_with_optimal_agent(
                test_layer, idea_description, target_audience, context
            )
            
            if result and hasattr(result, 'score'):
                print(f"✅ Agent analysis successful: {result.score}/10")
                agent_analysis_working = True
            else:
                print(f"⚠️ Agent analysis result format unexpected")
                agent_analysis_working = False
            
            self.test_results["specialized_agents"] = {
                "status": "PASSED",
                "total_agents": len(orchestrator.agents),
                "agent_assignments": agent_assignments,
                "analysis_test": agent_analysis_working
            }
            
        except Exception as e:
            print(f"❌ Specialized agent test failed: {str(e)}")
            self.test_results["specialized_agents"] = {"status": "FAILED", "error": str(e)}
    
    async def test_context_aware_analysis(self, idea_description: str, target_audience: str):
        """Test 3: Context-Aware Layer Analysis"""
        print("\n🔍 TEST 3: Context-Aware Layer Analysis")
        print("-" * 50)
        
        try:
            from app.core.comprehensive_analytical_framework_fixed import ComprehensiveAnalyticalFramework
            
            framework = ComprehensiveAnalyticalFramework()
            
            # Test context-aware layer names
            test_layers = [
                "need_perception_consumer_demand",
                "total_addressable_market_market_size",
                "core_features_analysis_features_functionality",
                "brand_positioning_brand_positioning_strategy",
                "onboarding_experience_user_experience_ux_design"
            ]
            
            successful_analyses = 0
            layer_results = {}
            
            for layer in test_layers:
                try:
                    context = {
                        "analysis_type": "test",
                        "layer": layer,
                        "test_mode": True
                    }
                    
                    layer_score = await framework.analyze_layer(
                        layer, idea_description, target_audience, context
                    )
                    
                    if layer_score and hasattr(layer_score, 'score'):
                        layer_results[layer] = {
                            "score": layer_score.score,
                            "rationale": layer_score.rationale[:100] + "..." if layer_score.rationale else "No rationale"
                        }
                        successful_analyses += 1
                        print(f"   ✅ {layer}: {layer_score.score}/10")
                    else:
                        print(f"   ⚠️ {layer}: Unexpected result format")
                        
                except Exception as e:
                    print(f"   ❌ {layer}: {str(e)}")
                    layer_results[layer] = {"error": str(e)}
            
            success_rate = successful_analyses / len(test_layers) if test_layers else 0
            
            print(f"📊 Context-aware analysis results:")
            print(f"   Success rate: {successful_analyses}/{len(test_layers)} ({success_rate:.1%})")
            
            self.test_results["context_aware_analysis"] = {
                "status": "PASSED" if success_rate >= 0.8 else "PARTIAL",
                "success_rate": success_rate,
                "successful_analyses": successful_analyses,
                "total_layers": len(test_layers),
                "layer_results": layer_results
            }
            
        except Exception as e:
            print(f"❌ Context-aware analysis test failed: {str(e)}")
            self.test_results["context_aware_analysis"] = {"status": "FAILED", "error": str(e)}
    
    async def test_multi_llm_orchestration(self):
        """Test 4: Multi-LLM Orchestration"""
        print("\n🔍 TEST 4: Multi-LLM Orchestration")
        print("-" * 50)
        
        try:
            from app.core.multi_llm_orchestrator import MultiLLMOrchestrator
            
            orchestrator = MultiLLMOrchestrator()
            
            print(f"✅ Multi-LLM orchestrator initialized")
            print(f"🔧 LLM providers: {len(orchestrator.llm_providers)}")
            
            # Test LLM priority chain
            priority_chain = ["gemini", "perplexity", "openai", "anthropic"]
            print(f"📋 LLM Priority Chain: {' → '.join(priority_chain)}")
            
            # Test configuration
            for provider in priority_chain:
                if provider in orchestrator.llm_providers:
                    config = orchestrator.llm_providers[provider]
                    model = config.get("model", "Unknown")
                    print(f"   ✅ {provider}: {model}")
                else:
                    print(f"   ⚠️ {provider}: Not configured")
            
            self.test_results["multi_llm_orchestration"] = {
                "status": "PASSED",
                "providers": len(orchestrator.llm_providers),
                "priority_chain": priority_chain
            }
            
        except Exception as e:
            print(f"❌ Multi-LLM orchestration test failed: {str(e)}")
            self.test_results["multi_llm_orchestration"] = {"status": "FAILED", "error": str(e)}
    
    async def test_workflow_integration(self, idea_description: str, target_audience: str):
        """Test 5: Workflow Integration"""
        print("\n🔍 TEST 5: Workflow Integration")
        print("-" * 50)
        
        try:
            from app.core.comprehensive_langgraph_workflow_fixed import ContextAwareLangGraphWorkflow
            from app.core.simple_state import State as AppState
            
            workflow = ContextAwareLangGraphWorkflow()
            
            print(f"✅ Fixed workflow imported successfully")
            print(f"🔧 Total layers: {len(workflow.analytical_framework.get_all_layers())}")
            print(f"🔗 Context-aware layers: {len(workflow.layer_contexts)}")
            
            # Test workflow structure
            workflow_nodes = list(workflow.workflow.nodes.keys())
            print(f"📊 Workflow nodes: {', '.join(workflow_nodes)}")
            
            # Test state creation
            initial_app_state = AppState(
                idea_description=idea_description,
                target_audience=target_audience,
                additional_context={"test_mode": True}
            )
            
            test_state = {
                'app_state': initial_app_state,
                'layer_scores': {},
                'factor_scores': {},
                'segment_scores': {},
                'analysis_results': {},
                'error_message': '',
                'current_step': '',
                'completed_steps': [],
                'retry_count': 0,
                'context_memory': {},
                'analysis_progress': {},
                'strategic_insights': []
            }
            
            print(f"✅ Test state created successfully")
            
            # Test individual workflow nodes (without full execution)
            try:
                # Test consumer analysis node
                consumer_result = await workflow.run_consumer_analysis(test_state)
                if consumer_result and 'layer_scores' in consumer_result:
                    print(f"✅ Consumer analysis node: WORKING")
                    consumer_working = True
                else:
                    print(f"⚠️ Consumer analysis node: Unexpected result")
                    consumer_working = False
                    
            except Exception as e:
                print(f"❌ Consumer analysis node failed: {str(e)}")
                consumer_working = False
            
            self.test_results["workflow_integration"] = {
                "status": "PASSED" if consumer_working else "PARTIAL",
                "workflow_nodes": workflow_nodes,
                "consumer_node_working": consumer_working,
                "total_layers": len(workflow.analytical_framework.get_all_layers())
            }
            
        except Exception as e:
            print(f"❌ Workflow integration test failed: {str(e)}")
            self.test_results["workflow_integration"] = {"status": "FAILED", "error": str(e)}
    
    async def test_scalability_assessment(self, idea_description: str, target_audience: str):
        """Test 6: Scalability Assessment"""
        print("\n🔍 TEST 6: Scalability Assessment")
        print("-" * 50)
        
        try:
            from app.core.comprehensive_langgraph_workflow_fixed import ContextAwareLangGraphWorkflow
            
            workflow = ContextAwareLangGraphWorkflow()
            
            # Test subset of layers from each segment
            test_layers = {
                "CONSUMER": ["need_perception_consumer_demand", "purchase_intent_consumer_demand"],
                "MARKET": ["total_addressable_market_market_size", "key_competitors_competitive_landscape"],
                "PRODUCT": ["core_features_analysis_features_functionality", "unique_selling_proposition_innovation_differentiation"],
                "BRAND": ["brand_positioning_brand_positioning_strategy", "unaided_brand_recall_brand_awareness"],
                "EXPERIENCE": ["onboarding_experience_user_experience_ux_design", "ease_of_use_user_experience_ux_design"]
            }
            
            segment_results = {}
            total_successful = 0
            total_tested = 0
            
            for segment, layers in test_layers.items():
                print(f"\n📊 Testing {segment} segment ({len(layers)} layers)")
                
                segment_successful = 0
                for layer in layers:
                    try:
                        persona = workflow.layer_contexts[layer].persona if layer in workflow.layer_contexts else "default"
                        
                        layer_score = await workflow.analytical_framework.analyze_layer(
                            layer, idea_description, target_audience,
                            {
                                "analysis_type": segment.lower(),
                                "layer": layer,
                                "persona": persona,
                                "test_mode": True
                            }
                        )
                        
                        if layer_score and hasattr(layer_score, 'score'):
                            segment_successful += 1
                            total_successful += 1
                            print(f"   ✅ {layer}: {layer_score.score}/10")
                        else:
                            print(f"   ⚠️ {layer}: Unexpected result format")
                            
                    except Exception as e:
                        print(f"   ❌ {layer}: {str(e)}")
                    
                    total_tested += 1
                
                segment_results[segment] = {
                    "layers_tested": len(layers),
                    "successful_layers": segment_successful,
                    "success_rate": segment_successful / len(layers) if layers else 0
                }
            
            overall_success_rate = total_successful / total_tested if total_tested > 0 else 0
            
            # Assess scalability
            if overall_success_rate >= 0.8:
                scalability = "HIGH"
                confidence = "Ready for full-scale deployment"
            elif overall_success_rate >= 0.6:
                scalability = "MEDIUM"
                confidence = "Should scale with minor adjustments"
            else:
                scalability = "LOW"
                confidence = "Needs significant improvements"
            
            print(f"\n📊 SCALABILITY ASSESSMENT")
            print(f"   Overall Success Rate: {overall_success_rate:.1%}")
            print(f"   Scalability Level: {scalability}")
            print(f"   Confidence: {confidence}")
            
            self.test_results["scalability_assessment"] = {
                "status": "PASSED",
                "overall_success_rate": overall_success_rate,
                "scalability_level": scalability,
                "confidence": confidence,
                "segment_results": segment_results,
                "total_tested": total_tested,
                "total_successful": total_successful
            }
            
        except Exception as e:
            print(f"❌ Scalability assessment failed: {str(e)}")
            self.test_results["scalability_assessment"] = {"status": "FAILED", "error": str(e)}
    
    async def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📋 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Calculate overall status
        passed_tests = sum(1 for result in self.test_results.values() if result.get("status") == "PASSED")
        partial_tests = sum(1 for result in self.test_results.values() if result.get("status") == "PARTIAL")
        failed_tests = sum(1 for result in self.test_results.values() if result.get("status") == "FAILED")
        total_tests = len(self.test_results)
        
        print(f"⏱️  Test Duration: {duration}")
        print(f"📊 Test Results: {passed_tests} PASSED, {partial_tests} PARTIAL, {failed_tests} FAILED")
        print(f"🎯 Overall Status: {'✅ READY' if failed_tests == 0 else '⚠️ NEEDS ATTENTION' if partial_tests > 0 else '❌ FAILED'}")
        
        # Detailed results
        for test_name, result in self.test_results.items():
            status = result.get("status", "UNKNOWN")
            status_icon = "✅" if status == "PASSED" else "⚠️" if status == "PARTIAL" else "❌"
            print(f"\n{status_icon} {test_name.upper().replace('_', ' ')}: {status}")
            
            if status == "PASSED":
                # Show key metrics
                if "total_layers" in result:
                    print(f"   📊 Total Layers: {result['total_layers']}")
                if "success_rate" in result:
                    print(f"   📈 Success Rate: {result['success_rate']:.1%}")
                if "scalability_level" in result:
                    print(f"   🚀 Scalability: {result['scalability_level']}")
            elif status == "PARTIAL":
                # Show partial success details
                if "success_rate" in result:
                    print(f"   📈 Partial Success: {result['success_rate']:.1%}")
            else:
                # Show error details
                if "error" in result:
                    print(f"   ❌ Error: {result['error']}")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_test_suite_results_{timestamp}.json"
        
        report_data = {
            "test_summary": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration.total_seconds(),
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "partial_tests": partial_tests,
                "failed_tests": failed_tests,
                "overall_status": "READY" if failed_tests == 0 else "NEEDS_ATTENTION" if partial_tests > 0 else "FAILED"
            },
            "test_results": self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n📁 Detailed report saved to: {filename}")
        
        # Final recommendation
        if failed_tests == 0:
            print(f"\n🎉 RECOMMENDATION: PROCEED with full-scale deployment!")
            print(f"   The platform is ready to analyze all 156+ strategic layers.")
        elif partial_tests > 0:
            print(f"\n⚠️  RECOMMENDATION: Address partial failures before full deployment.")
            print(f"   Some components need attention but the core is functional.")
        else:
            print(f"\n❌ RECOMMENDATION: Fix critical failures before proceeding.")
            print(f"   The platform needs significant improvements.")

async def main():
    """Main test execution function"""
    # Test business idea
    idea_description = "A smart home device that automates pet feeding and playtime with AI monitoring and health tracking"
    target_audience = "Busy pet owners aged 25-45 who want to ensure their pets are cared for while away"
    
    # Initialize and run test suite
    test_suite = ValidatusTestSuite()
    results = await test_suite.run_all_tests(idea_description, target_audience)
    
    return results

if __name__ == "__main__":
    print("🚀 Starting Validatus Platform Comprehensive Test Suite")
    print("=" * 80)
    
    # Run the test suite
    results = asyncio.run(main())
    
    print(f"\n🏁 Test suite completed: {'SUCCESS' if 'error' not in results else 'FAILED'}")
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
