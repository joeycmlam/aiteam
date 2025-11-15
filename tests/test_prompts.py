#!/usr/bin/env python3
"""
Test script for BA Agent with externalized prompts

This script verifies that:
1. Prompts are loaded correctly from YAML
2. Templates work with variable substitution
3. Custom prompts can override defaults
"""

import os
import sys
import yaml

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ba_agent import BAAgent
from dotenv import load_dotenv

def test_prompts_loading():
    """Test that prompts load correctly"""
    print("="*70)
    print("🧪 Test 1: Prompts Loading")
    print("="*70)
    
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER', 'https://example.atlassian.net'),
        'user': os.getenv('JIRA_USER', 'user@example.com'),
        'token': os.getenv('JIRA_API_TOKEN', 'token')
    }
    
    # Test with default prompts path
    print("\n📋 Creating BA Agent with default prompts...")
    ba = BAAgent(llm_config, jira_config)
    
    # Check prompts loaded
    if ba.prompts:
        print("✅ Prompts loaded successfully")
        print(f"   Available prompts: {list(ba.prompts.keys())}")
    else:
        print("❌ No prompts loaded")
        return False
    
    # Verify key prompts exist
    required_prompts = ['extract_requirements', 'analyze_initiative', 'analyze_requirements', 'generate_scenarios']
    
    for prompt_name in required_prompts:
        if prompt_name in ba.prompts:
            print(f"   ✅ {prompt_name}: Found")
            
            # Check template exists
            if 'template' in ba.prompts[prompt_name]:
                template = ba.prompts[prompt_name]['template']
                print(f"      Template length: {len(template)} characters")
            else:
                print(f"      ⚠️  No template found")
        else:
            print(f"   ❌ {prompt_name}: Missing")
            return False
    
    print("\n✅ Test 1 PASSED\n")
    return True

def test_template_substitution():
    """Test that template variable substitution works"""
    print("="*70)
    print("🧪 Test 2: Template Variable Substitution")
    print("="*70)
    
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER', 'https://example.atlassian.net'),
        'user': os.getenv('JIRA_USER', 'user@example.com'),
        'token': os.getenv('JIRA_API_TOKEN', 'token')
    }
    
    ba = BAAgent(llm_config, jira_config)
    
    # Test extract_requirements template
    print("\n📝 Testing 'extract_requirements' template...")
    template = ba.prompts['extract_requirements']['template']
    
    # Substitute variables
    filled = template.format(
        ticket_id="TEST-123",
        summary="Test Feature",
        description="Test Description"
    )
    
    if "TEST-123" in filled and "Test Feature" in filled:
        print("✅ Variable substitution works")
        print(f"   Preview: {filled[:200]}...")
    else:
        print("❌ Variable substitution failed")
        return False
    
    # Test analyze_initiative template
    print("\n📝 Testing 'analyze_initiative' template...")
    template = ba.prompts['analyze_initiative']['template']
    
    filled = template.format(
        summary="Test Initiative",
        description="Test initiative description",
        issue_type="Epic",
        linked_count=5
    )
    
    if "Test Initiative" in filled and "5" in filled:
        print("✅ Variable substitution works")
        print(f"   Preview: {filled[:200]}...")
    else:
        print("❌ Variable substitution failed")
        return False
    
    print("\n✅ Test 2 PASSED\n")
    return True

def test_custom_prompts():
    """Test loading custom prompts file"""
    print("="*70)
    print("🧪 Test 3: Custom Prompts File")
    print("="*70)
    
    # Create a temporary custom prompts file
    custom_prompts = {
        'extract_requirements': {
            'template': 'CUSTOM TEMPLATE: Extract from {ticket_id}',
            'system_message': 'Custom system message'
        },
        'defaults': {
            'acceptance_criteria': ['Custom criterion 1', 'Custom criterion 2']
        }
    }
    
    custom_path = '/tmp/custom_ba_prompts.yaml'
    
    print(f"\n📝 Creating custom prompts file: {custom_path}")
    with open(custom_path, 'w') as f:
        yaml.dump(custom_prompts, f)
    
    print("✅ Custom file created")
    
    # Load BA Agent with custom prompts
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER', 'https://example.atlassian.net'),
        'user': os.getenv('JIRA_USER', 'user@example.com'),
        'token': os.getenv('JIRA_API_TOKEN', 'token')
    }
    
    print(f"\n📋 Loading BA Agent with custom prompts...")
    ba = BAAgent(llm_config, jira_config, prompts_config_path=custom_path)
    
    # Verify custom prompts loaded
    template = ba.prompts['extract_requirements']['template']
    
    if 'CUSTOM TEMPLATE' in template:
        print("✅ Custom prompts loaded successfully")
        print(f"   Template: {template}")
    else:
        print("❌ Custom prompts not loaded")
        return False
    
    # Check defaults
    criteria = ba.prompts['defaults']['acceptance_criteria']
    if 'Custom criterion 1' in criteria:
        print("✅ Custom defaults loaded")
        print(f"   Criteria: {criteria}")
    else:
        print("❌ Custom defaults not loaded")
        return False
    
    # Cleanup
    os.remove(custom_path)
    print(f"\n🧹 Cleaned up: {custom_path}")
    
    print("\n✅ Test 3 PASSED\n")
    return True

def test_fallback_to_defaults():
    """Test fallback when prompts file doesn't exist"""
    print("="*70)
    print("🧪 Test 4: Fallback to Default Prompts")
    print("="*70)
    
    load_dotenv(override=True)
    
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'model': os.getenv('OLLAMA_MODEL', 'llama3.2')
    }
    
    jira_config = {
        'server': os.getenv('JIRA_SERVER', 'https://example.atlassian.net'),
        'user': os.getenv('JIRA_USER', 'user@example.com'),
        'token': os.getenv('JIRA_API_TOKEN', 'token')
    }
    
    # Use non-existent path
    print("\n📋 Creating BA Agent with non-existent prompts file...")
    ba = BAAgent(llm_config, jira_config, prompts_config_path='/nonexistent/path.yaml')
    
    # Should fall back to defaults
    if ba.prompts and 'extract_requirements' in ba.prompts:
        print("✅ Fallback to default prompts successful")
        print(f"   Available prompts: {list(ba.prompts.keys())}")
    else:
        print("❌ Fallback failed")
        return False
    
    print("\n✅ Test 4 PASSED\n")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 BA Agent Prompts Configuration Tests")
    print("="*70 + "\n")
    
    tests = [
        ("Prompts Loading", test_prompts_loading),
        ("Template Substitution", test_template_substitution),
        ("Custom Prompts File", test_custom_prompts),
        ("Fallback to Defaults", test_fallback_to_defaults)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with exception:")
            print(f"   {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 Test Summary")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70 + "\n")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
