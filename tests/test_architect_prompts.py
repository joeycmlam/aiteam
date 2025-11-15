#!/usr/bin/env python3
"""
Test Architect Agent Prompts Configuration

Validates:
1. Default prompts load correctly
2. Custom prompts override defaults
3. Prompt template substitution works
4. Fallback to inline prompts when config missing
"""

import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.architect_agent import ArchitectAgent

def test_default_prompts():
    """Test loading default prompts configuration"""
    print("\n" + "="*60)
    print("TEST 1: Default Prompts Loading")
    print("="*60)
    
    llm_config = {'provider': 'github_copilot_cli', 'model': 'gpt-4o'}
    agent = ArchitectAgent(llm_config)
    
    assert 'recommend_patterns' in agent.prompts
    assert 'fallbacks' in agent.prompts
    
    print("✅ Default prompts loaded successfully")
    print(f"   Prompts keys: {list(agent.prompts.keys())}")

def test_custom_prompts():
    """Test loading custom prompts file"""
    print("\n" + "="*60)
    print("TEST 2: Custom Prompts Loading")
    print("="*60)
    
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'config', 'prompts', 'examples', 'architect_agent_prompts_microservices.yaml'
    )
    
    llm_config = {'provider': 'github_copilot_cli', 'model': 'gpt-4o'}
    agent = ArchitectAgent(llm_config, prompts_config_path=custom_path)
    
    # Check if microservices-specific patterns are loaded
    patterns = agent.prompts['fallbacks']['default_patterns']
    assert any('microservices' in p.lower() or 'saga' in p.lower() for p in patterns)
    
    print("✅ Custom prompts loaded successfully")
    print(f"   Microservices patterns: {len(patterns)}")

def test_template_substitution():
    """Test that template variables are substituted correctly"""
    print("\n" + "="*60)
    print("TEST 3: Template Variable Substitution")
    print("="*60)
    
    llm_config = {'provider': 'github_copilot_cli', 'model': 'gpt-4o'}
    agent = ArchitectAgent(llm_config)
    
    template = agent.prompts['recommend_patterns']['template']
    
    # Simulate template substitution
    test_data = {
        'total_files': 42,
        'languages': {'.py': 30, '.js': 12},
        'complexity': 'high'
    }
    
    formatted = template.format(**test_data)
    
    assert '42' in formatted
    assert 'high' in formatted
    
    print("✅ Template substitution works correctly")
    print(f"   Sample output:\n{formatted[:150]}...")

def test_fallback_prompts():
    """Test fallback to inline prompts when config not found"""
    print("\n" + "="*60)
    print("TEST 4: Fallback to Inline Prompts")
    print("="*60)
    
    # Use non-existent config path
    llm_config = {'provider': 'github_copilot_cli', 'model': 'gpt-4o'}
    agent = ArchitectAgent(llm_config, prompts_config_path='/nonexistent/path.yaml')
    
    # When config not found, prompts dict is empty, but recommend_patterns has inline defaults
    assert agent.prompts == {}
    
    # Test that recommend_patterns still works with inline defaults
    analysis = {
        'total_files': 10,
        'languages': {'.py': 10},
        'complexity': 'low'
    }
    patterns = agent.recommend_patterns(analysis)
    
    # Should return 5 default patterns
    assert len(patterns) == 5
    
    print("✅ Fallback prompts work correctly")
    print(f"   Inline default patterns used: {len(patterns)}")

def test_pattern_recommendation():
    """Test actual pattern recommendation with mock data"""
    print("\n" + "="*60)
    print("TEST 5: Pattern Recommendation Flow")
    print("="*60)
    
    llm_config = {'provider': 'github_copilot_cli', 'model': 'gpt-4o'}
    agent = ArchitectAgent(llm_config)
    
    # Mock codebase analysis
    analysis = {
        'total_files': 150,
        'languages': {'.py': 100, '.js': 30, '.sql': 20},
        'complexity': 'high'
    }
    
    # Note: This will attempt to call LLM, but will use fallback if it fails
    patterns = agent.recommend_patterns(analysis)
    
    assert isinstance(patterns, list)
    assert len(patterns) > 0
    
    print("✅ Pattern recommendation works")
    print(f"   Recommended {len(patterns)} patterns")

def main():
    """Run all tests"""
    print("\n" + "🧪 ARCHITECT AGENT PROMPTS TESTS")
    print("="*60)
    
    try:
        test_default_prompts()
        test_custom_prompts()
        test_template_substitution()
        test_fallback_prompts()
        test_pattern_recommendation()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        
        return 0
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
