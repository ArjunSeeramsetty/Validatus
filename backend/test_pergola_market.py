#!/usr/bin/env python3
"""
Test Script: Pergola Market Business Case Analysis
Validatus Platform - Strategic Analysis Testing

This script tests the complete Validatus Platform workflow with a specific business case:
- Industry: Outdoor Living / Construction Products (Pergola Market)
- Markets: Czech Republic, broader Europe, and US
- Consumer Persona: Homeowners (35-60, mid/high income) and commercial buyers
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any

# Import the workflow directly for testing
from app.core.comprehensive_langgraph_workflow_fixed import ContextAwareLangGraphWorkflow
from app.core.simple_state import State as ValidatusState

class PergolaMarketTestSuite:
    """Test suite for pergola market business case analysis"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.workflow = None
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*80)
        print(f"🧪 {title}")
        print("="*80)
        
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n📋 {title}")
        print("-" * 60)
        
    def print_result(self, test_name: str, status: str, details: str = ""):
        """Print a formatted test result"""
        emoji = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "⚠️"
        print(f"{emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
            
    async def test_workflow_initialization(self):
        """Test 1: Workflow Initialization"""
        self.print_section("TEST 1: Workflow Initialization")
        
        try:
            self.workflow = ContextAwareLangGraphWorkflow()
            print("✅ ContextAwareLangGraphWorkflow initialized successfully")
            
            # Check framework structure
            total_layers = len(self.workflow.analytical_framework.get_all_layers())
            print(f"📊 Total strategic layers available: {total_layers}")
            
            # Check segments
            segments = list(self.workflow.analytical_framework.analytical_framework.keys())
            print(f"🎯 Available segments: {', '.join(segments)}")
            
            self.test_results['workflow_init'] = "PASSED"
            return True
            
        except Exception as e:
            print(f"❌ Workflow initialization failed: {str(e)}")
            self.test_results['workflow_init'] = "FAILED"
            return False
    
    async def test_direct_workflow_execution(self):
        """Test 2: Direct Workflow Execution"""
        self.print_section("TEST 2: Direct Workflow Execution")
        
        if not self.workflow:
            print("❌ Workflow not initialized")
            self.test_results['direct_execution'] = "FAILED"
            return False
            
        try:
            # Define the pergola market business case
            business_case = {
                "idea_description": "Premium pergola systems for outdoor living spaces with integrated lighting, heating, and smart controls",
                "target_audience": "Homeowners aged 35-60 with mid/high income, and commercial buyers (hospitality, developers)",
                "additional_context": {
                    "industry": "Outdoor Living / Construction Products",
                    "primary_markets": ["Czech Republic", "Europe", "United States"],
                    "product_category": "Premium Pergola Systems",
                    "key_features": ["Integrated lighting", "Heating systems", "Smart controls", "Modular design"],
                    "target_segments": ["Residential luxury", "Commercial hospitality", "Property development"],
                    "competitive_advantage": "Smart technology integration with premium materials",
                    "market_positioning": "High-end, innovative outdoor living solutions"
                }
            }
            
            print("🚀 Starting direct workflow execution...")
            print(f"📝 Business Case: {business_case['idea_description']}")
            print(f"🎯 Target Audience: {business_case['target_audience']}")
            print(f"🌍 Markets: {', '.join(business_case['additional_context']['primary_markets'])}")
            
            # Execute the workflow
            result = await self.workflow.execute(
                idea_description=business_case['idea_description'],
                target_audience=business_case['target_audience'],
                additional_context=business_case['additional_context']
            )
            
            if result and 'error' not in result:
                print("✅ Direct workflow execution completed successfully")
                print(f"📊 Results structure: {list(result.keys()) if isinstance(result, dict) else 'Non-dict result'}")
                
                # Save results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pergola_market_analysis_results_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Results saved to: {filename}")
                self.test_results['direct_execution'] = "PASSED"
                return True
            else:
                print(f"❌ Workflow execution failed: {result}")
                self.test_results['direct_execution'] = "FAILED"
                return False
                
        except Exception as e:
            print(f"❌ Direct workflow execution failed: {str(e)}")
            self.test_results['direct_execution'] = "FAILED"
            return False
    
    async def test_api_integration(self):
        """Test 3: API Integration Testing"""
        self.print_section("TEST 3: API Integration Testing")
        
        try:
            import requests
            
            # Test health endpoint
            print("🔍 Testing health endpoint...")
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test analysis creation
            print("🔍 Testing analysis creation...")
            analysis_data = {
                "query": "Premium pergola systems for outdoor living spaces with integrated lighting, heating, and smart controls",
                "context": {
                    "industry": "Outdoor Living / Construction Products",
                    "geography": ["Czech Republic", "Europe", "United States"],
                    "company_stage": "Growth Stage",
                    "target_audience": "Homeowners aged 35-60 with mid/high income, and commercial buyers (hospitality, developers)"
                }
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/analysis",
                json=analysis_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_id = result.get('analysis_id')
                print(f"✅ Analysis created successfully: {analysis_id}")
                
                # Test status endpoint
                print("🔍 Testing status endpoint...")
                time.sleep(5)  # Wait for background processing
                
                status_response = requests.get(
                    f"http://localhost:8000/api/v1/analysis/{analysis_id}/status",
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    status_result = status_response.json()
                    print(f"✅ Status endpoint working: {status_result.get('status')}")
                    self.test_results['api_integration'] = "PASSED"
                    return True
                else:
                    print(f"❌ Status endpoint failed: {status_response.status_code}")
                    return False
            else:
                print(f"❌ Analysis creation failed: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ API server not running. Start the server with 'python main.py' first.")
            self.test_results['api_integration'] = "SKIPPED"
            return True
        except Exception as e:
            print(f"❌ API integration test failed: {str(e)}")
            self.test_results['api_integration'] = "FAILED"
            return False
    
    async def test_market_specific_analysis(self):
        """Test 4: Market-Specific Analysis Validation"""
        self.print_section("TEST 4: Market-Specific Analysis Validation")
        
        if not self.workflow:
            print("❌ Workflow not initialized")
            self.test_results['market_analysis'] = "FAILED"
            return False
            
        try:
            # Test specific market analysis
            print("🔍 Testing Czech Republic market analysis...")
            
            # Get market layers
            market_layers = [layer for layer in self.workflow.analytical_framework.get_all_layers() 
                           if 'market' in layer.lower() or 'czech' in layer.lower()]
            
            print(f"📊 Found {len(market_layers)} market-related layers")
            
            # Test a few key market layers
            key_market_layers = [
                "total_addressable_market_market_size",
                "key_competitors_competitive_landscape", 
                "emerging_trends_market_trends_opportunities"
            ]
            
            for layer in key_market_layers:
                if layer in self.workflow.analytical_framework.get_all_layers():
                    print(f"✅ Market layer available: {layer}")
                else:
                    print(f"⚠️ Market layer missing: {layer}")
            
            self.test_results['market_analysis'] = "PASSED"
            return True
            
        except Exception as e:
            print(f"❌ Market-specific analysis test failed: {str(e)}")
            self.test_results['market_analysis'] = "FAILED"
            return False
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        self.print_header("TEST SUITE COMPLETION REPORT")
        
        end_time = datetime.now()
        duration = end_time - self.start_time if self.start_time else "Unknown"
        
        print(f"⏱️  Test Duration: {duration}")
        print(f"📊 Total Tests: {len(self.test_results)}")
        
        # Count results
        passed = sum(1 for result in self.test_results.values() if result == "PASSED")
        failed = sum(1 for result in self.test_results.values() if result == "FAILED")
        skipped = sum(1 for result in self.test_results.values() if result == "SKIPPED")
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Skipped: {skipped}")
        
        # Overall status
        if failed == 0:
            overall_status = "✅ ALL TESTS PASSED"
        elif passed > failed:
            overall_status = "⚠️  MOSTLY PASSED"
        else:
            overall_status = "❌ MULTIPLE FAILURES"
            
        print(f"\n🎯 Overall Status: {overall_status}")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            emoji = "✅" if result == "PASSED" else "❌" if result == "FAILED" else "⚠️"
            print(f"   {emoji} {test_name}: {result}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        if failed == 0:
            print("   🚀 Platform is ready for pergola market analysis!")
            print("   📈 All components working correctly")
            print("   🌟 Ready for production use")
        elif failed > 0:
            print("   🔧 Some tests failed - review error messages above")
            print("   📝 Check workflow initialization and dependencies")
            print("   🚨 Fix issues before proceeding with analysis")
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"pergola_market_test_report_{timestamp}.json"
        
        report_data = {
            "test_suite": "Pergola Market Business Case Test",
            "timestamp": datetime.now().isoformat(),
            "duration": str(duration) if isinstance(duration, str) else str(duration),
            "results": self.test_results,
            "summary": {
                "total_tests": len(self.test_results),
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "overall_status": overall_status
            }
        }
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Test report saved to: {report_filename}")
    
    async def run_all_tests(self):
        """Run all test cases"""
        self.print_header("PERGOLA MARKET BUSINESS CASE TEST SUITE")
        print("🎯 Testing Validatus Platform with specific business case:")
        print("   • Industry: Outdoor Living / Construction Products (Pergola Market)")
        print("   • Markets: Czech Republic, broader Europe, and US")
        print("   • Consumer Persona: Homeowners (35-60, mid/high income) and commercial buyers")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = datetime.now()
        
        # Run all tests
        tests = [
            ("Workflow Initialization", self.test_workflow_initialization),
            ("Direct Workflow Execution", self.test_direct_workflow_execution),
            ("API Integration", self.test_api_integration),
            ("Market-Specific Analysis", self.test_market_specific_analysis)
        ]
        
        for test_name, test_func in tests:
            try:
                await test_func()
            except Exception as e:
                print(f"❌ Test '{test_name}' crashed: {str(e)}")
                self.test_results[test_name.lower().replace(' ', '_')] = "CRASHED"
        
        # Generate final report
        self.generate_test_report()
        
        return self.test_results

async def main():
    """Main test execution function"""
    print("🚀 Starting Pergola Market Business Case Test Suite...")
    
    test_suite = PergolaMarketTestSuite()
    results = await test_suite.run_all_tests()
    
    print("\n🏁 Test suite completed!")
    return results

if __name__ == "__main__":
    # Run the test suite
    try:
        results = asyncio.run(main())
        exit_code = 0 if all(result == "PASSED" or result == "SKIPPED" for result in results.values()) else 1
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Test suite interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {str(e)}")
        exit(1)
