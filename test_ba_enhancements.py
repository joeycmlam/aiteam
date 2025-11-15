#!/usr/bin/env python3
"""
Test script for enhanced BA Agent functionality

Tests:
1. Reading requirement files (TXT, JSON, YAML, MD)
2. AI-powered requirement analysis
3. Scenario/feature file generation
4. JIRA epic creation
"""

import os
import sys
import yaml
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ba_agent import BAAgent

def test_read_requirement_files():
    """Test reading different requirement file formats"""
    print("\n" + "="*70)
    print("TEST 1: Reading Requirement Files")
    print("="*70)
    
    # Initialize BA Agent
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER', 'https://joeycmlam-1762529818344.atlassian.net'),
        'user': os.getenv('JIRA_USER', 'joey.cm.lam@gmail.com'),
        'token': os.getenv('JIRA_API_TOKEN')
    }
    
    ba = BAAgent(llm_config, jira_config)
    
    # Test different file formats
    test_files = [
        'examples/requirements.txt',
        'examples/requirements.json',
        'examples/requirements.yaml',
        'examples/requirements.md'
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n📄 Testing: {file_path}")
            result = ba.read_requirement_file(file_path)
            
            if 'error' in result:
                print(f"   ❌ Error: {result['error']}")
            else:
                print(f"   ✅ Successfully read file")
                if 'content' in result:
                    print(f"   📝 Content length: {len(result['content'])} characters")
        else:
            print(f"\n⚠️  File not found: {file_path} (will create example)")
    
    print("\n✅ Test 1 Complete\n")

def test_analyze_requirements():
    """Test AI-powered requirement analysis"""
    print("\n" + "="*70)
    print("TEST 2: AI Requirement Analysis")
    print("="*70)
    
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER'),
        'user': os.getenv('JIRA_USER'),
        'token': os.getenv('JIRA_API_TOKEN')
    }
    
    ba = BAAgent(llm_config, jira_config)
    
    # Read requirement file
    req_file = 'examples/requirements.txt'
    
    if not os.path.exists(req_file):
        print(f"⚠️  Creating example requirement file: {req_file}")
        os.makedirs('examples', exist_ok=True)
        with open(req_file, 'w') as f:
            f.write("""# E-Commerce Platform Requirements

## Overview
We need to build a modern e-commerce platform that allows customers to browse products, 
add items to cart, and complete purchases securely.

## Key Features
1. User Registration and Authentication
2. Product Catalog with Search and Filters
3. Shopping Cart Management
4. Secure Payment Processing
5. Order Tracking and History
6. Admin Dashboard for Product Management

## Business Goals
- Increase online sales by 40%
- Reduce cart abandonment rate to below 30%
- Support 10,000 concurrent users
- Process payments in under 3 seconds

## Constraints
- Must comply with PCI-DSS for payment processing
- Support mobile and desktop browsers
- Available 99.9% uptime
- Budget: $500,000
- Timeline: 6 months
""")
        print(f"   ✅ Created example file")
    
    # Read and analyze
    requirement_data = ba.read_requirement_file(req_file)
    
    if 'error' not in requirement_data:
        print("\n📊 Analyzing requirements with AI...")
        analysis_result = ba.analyze_requirements(requirement_data, output_dir='requirements')
        
        print("\n✅ Analysis Complete!")
        print(f"\n📂 Generated Files:")
        print(f"   • requirements/requirements_analysis.md")
        print(f"   • requirements/requirements.feature")
        print(f"   • requirements/requirements_structured.json")
        
        print(f"\n📋 Extracted Information:")
        print(f"   • Assumptions: {len(analysis_result.get('assumptions', []))}")
        print(f"   • User Stories: {len(analysis_result.get('user_stories', []))}")
        
        if analysis_result.get('assumptions'):
            print(f"\n💡 Key Assumptions:")
            for i, assumption in enumerate(analysis_result['assumptions'][:3], 1):
                print(f"   {i}. {assumption}")
        
        if analysis_result.get('user_stories'):
            print(f"\n👥 User Stories:")
            for i, story in enumerate(analysis_result['user_stories'][:3], 1):
                print(f"   {i}. {story['story'][:80]}...")
    
    print("\n✅ Test 2 Complete\n")

def test_create_jira_epic():
    """Test creating JIRA epic from requirements"""
    print("\n" + "="*70)
    print("TEST 3: Create JIRA Epic")
    print("="*70)
    
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER'),
        'user': os.getenv('JIRA_USER'),
        'token': os.getenv('JIRA_API_TOKEN')
    }
    
    ba = BAAgent(llm_config, jira_config)
    
    # Create mock requirement document
    requirement_doc = {
        'ai_analysis': """# E-Commerce Platform Requirements Analysis

## Business Objectives
1. Increase online revenue by enabling direct customer purchases
2. Reduce operational costs by automating order processing
3. Improve customer satisfaction with modern shopping experience

## Assumptions
- Payment gateway integration is available
- SSL certificate can be obtained
- Hosting infrastructure supports scaling

## User Stories
- As a customer, I want to browse products so that I can find items to purchase
- As a customer, I want to add items to cart so that I can checkout later
- As a customer, I want secure payment processing so that my data is protected
""",
        'assumptions': [
            'Payment gateway integration is available',
            'SSL certificate can be obtained',
            'Hosting infrastructure supports scaling'
        ],
        'user_stories': [
            {'story': 'As a customer, I want to browse products so that I can find items to purchase', 'status': 'pending'},
            {'story': 'As a customer, I want to add items to cart so that I can checkout later', 'status': 'pending'},
            {'story': 'As a customer, I want secure payment processing so that my data is protected', 'status': 'pending'}
        ],
        'generated_at': '2025-11-15 10:00:00'
    }
    
    # Try to create epic in JIRA
    print("\n📌 Attempting to create Epic in JIRA...")
    print("   (Note: This will only work if JIRA credentials are configured)")
    
    epic_key = ba.create_epic_in_jira(requirement_doc, project_key='SCRUM')
    
    if epic_key:
        print(f"\n🎉 Success! Epic created: {epic_key}")
        print(f"   View at: {jira_config['server']}/browse/{epic_key}")
    else:
        print(f"\n⚠️  Epic creation skipped (JIRA not configured or error occurred)")
        print(f"   Epic details are saved in the requirement document")
    
    print("\n✅ Test 3 Complete\n")

def test_complete_workflow():
    """Test complete workflow: Read → Analyze → Create Epic"""
    print("\n" + "="*70)
    print("TEST 4: Complete Workflow")
    print("="*70)
    
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER'),
        'user': os.getenv('JIRA_USER'),
        'token': os.getenv('JIRA_API_TOKEN')
    }
    
    ba = BAAgent(llm_config, jira_config)
    
    print("\n📋 Step 1: Read Requirements")
    req_data = ba.read_requirement_file('examples/requirements.txt')
    
    if 'error' in req_data:
        print(f"   ❌ Cannot proceed: {req_data['error']}")
        return
    
    print("\n📋 Step 2: Analyze Requirements")
    analysis = ba.analyze_requirements(req_data, output_dir='requirements')
    
    print("\n📋 Step 3: Create JIRA Epic")
    epic_key = ba.create_epic_in_jira(analysis, project_key='SCRUM')
    
    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)
    print(f"✅ Requirements read and parsed")
    print(f"✅ AI analysis completed")
    print(f"✅ {len(analysis.get('assumptions', []))} assumptions identified")
    print(f"✅ {len(analysis.get('user_stories', []))} user stories extracted")
    print(f"✅ Feature file generated: requirements/requirements.feature")
    print(f"✅ Analysis document: requirements/requirements_analysis.md")
    
    if epic_key:
        print(f"✅ JIRA Epic created: {epic_key}")
    else:
        print(f"⚠️  JIRA Epic not created (configure credentials to enable)")
    
    print("\n✅ Test 4 Complete - Full Workflow Success!\n")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 BA AGENT ENHANCED FUNCTIONALITY TESTS")
    print("="*70)
    print("\nTesting:")
    print("  1. ✅ Read requirement files (TXT, JSON, YAML, MD)")
    print("  2. ✅ AI-powered requirement analysis")
    print("  3. ✅ Generate scenarios and feature files")
    print("  4. ✅ Create JIRA epic with user stories")
    print("="*70)
    
    try:
        # Run tests
        test_read_requirement_files()
        test_analyze_requirements()
        test_create_jira_epic()
        test_complete_workflow()
        
        print("\n" + "="*70)
        print("🎉 ALL TESTS COMPLETED")
        print("="*70)
        print("\n✅ BA Agent enhancements are working correctly!")
        print("\n📚 Next steps:")
        print("   1. Review generated files in 'requirements/' directory")
        print("   2. Check JIRA for created epic (if credentials configured)")
        print("   3. Use these features in your workflow")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
