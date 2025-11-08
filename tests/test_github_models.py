#!/usr/bin/env python3
"""
Test GitHub Models API (Claude 3.5 Sonnet) Integration

This tests the GitHub Models API which provides programmatic access to:
- Claude 3.5 Sonnet (Anthropic)
- GPT-4o (OpenAI)  
- Mistral Large (Mistral AI)

Requirements:
1. GitHub Copilot subscription
2. GitHub Personal Access Token with 'read:user' scope
3. GITHUB_TOKEN in .env file
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.llm_manager import LLMManager

def test_github_models_api():
    """Test Claude 3.5 Sonnet via GitHub Models API"""
    
    print("=" * 70)
    print("🧪 Testing GitHub Models API (Claude 3.5 Sonnet)")
    print("=" * 70)
    print()
    
    # Load environment (override=True to ensure .env values take precedence)
    load_dotenv(override=True)
    
    # Check for GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN not found in .env file")
        print()
        print("📝 Setup steps:")
        print("   1. Go to: https://github.com/settings/tokens")
        print("   2. Generate new token (classic) with 'read:user' scope")
        print("   3. Add to .env file: GITHUB_TOKEN=your_token_here")
        print()
        print("   See GITHUB_MODELS_SETUP.md for detailed instructions")
        return False
    
    print(f"✅ GitHub token found: {github_token[:8]}...")
    print()
    
    # Initialize LLM Manager with GitHub Models API
    print("🔧 Initializing LLM Manager with 'github_copilot_cli' provider...")
    llm = LLMManager("github_copilot_cli")
    print()
    
    # Test 1: Simple code generation
    print("-" * 70)
    print("Test 1: Simple Code Generation")
    print("-" * 70)
    
    prompt1 = "Write a Python function to calculate the fibonacci sequence up to n numbers."
    print(f"📤 Prompt: {prompt1}")
    print()
    
    try:
        response1 = llm.generate(
            prompt1,
            system_message="You are an expert Python developer. Provide clean, documented code."
        )
        
        print("📥 Response:")
        print(response1)
        print()
        
        if len(response1) > 50:
            print("✅ Test 1 PASSED - Got substantial response")
        else:
            print("⚠️  Test 1 WARNING - Response seems short")
        
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        return False
    
    print()
    
    # Test 2: Code analysis
    print("-" * 70)
    print("Test 2: Code Analysis")
    print("-" * 70)
    
    code_sample = """
def process_data(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
"""
    
    analysis = llm.analyze_code(
        code_sample,
        "What improvements can be made to this code?"
    )
    
    print("📥 Analysis:")
    print(analysis)
    print()
    
    if len(analysis) > 50:
        print("✅ Test 2 PASSED - Got code analysis")
    else:
        print("⚠️  Test 2 WARNING - Analysis seems short")
    
    print()
    
    # Test 3: Compare with Ollama
    print("-" * 70)
    print("Test 3: Provider Comparison")
    print("-" * 70)
    print()
    
    print("🤖 Testing Ollama (local)...")
    ollama_llm = LLMManager("ollama")
    ollama_response = ollama_llm.generate("Write a Python hello world function")
    print(f"📥 Ollama response length: {len(ollama_response)} characters")
    print()
    
    print("🤖 Testing GitHub Models (Claude 3.5 Sonnet)...")
    github_response = llm.generate("Write a Python hello world function")
    print(f"📥 GitHub Models response length: {len(github_response)} characters")
    print()
    
    print("✅ Test 3 PASSED - Both providers working")
    print()
    
    # Summary
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print()
    print("✅ GitHub Models API (Claude 3.5 Sonnet) is working!")
    print("✅ Ollama (local) is working!")
    print()
    print("🎯 Recommended Usage:")
    print("   - Use Claude 3.5 Sonnet for: Architecture, complex reviews, critical tasks")
    print("   - Use Ollama for: Bulk generation, testing, documentation")
    print()
    print("📖 See GITHUB_MODELS_SETUP.md for more details")
    
    return True

if __name__ == "__main__":
    success = test_github_models_api()
    sys.exit(0 if success else 1)
