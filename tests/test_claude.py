#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script to verify Anthropic Claude integration"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.llm_manager import LLMManager

def test_claude():
    """Test LLM Manager with Anthropic Claude"""
    
    load_dotenv()
    
    print("="*70)
    print("🧪 Testing Anthropic Claude Integration")
    print("="*70)
    
    # Check if API key is configured
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_anthropic_api_key_here':
        print("\n❌ ANTHROPIC_API_KEY not configured in .env file")
        print("\n📝 To use Claude Sonnet 4:")
        print("1. Get API key from: https://console.anthropic.com/")
        print("2. Add to .env file: ANTHROPIC_API_KEY=your_key_here")
        print("3. Update .env: LLM_PROVIDER=anthropic")
        return False
    
    # Test prompt
    test_prompt = "Write a simple Python function that adds two numbers. Just provide the code with a brief explanation."
    
    # Test with Anthropic provider
    print("\n1️⃣  Testing with Anthropic Claude...")
    llm = LLMManager(provider="anthropic")
    
    print(f"\n📝 Prompt: {test_prompt}")
    print("\n⏳ Generating response with Claude...")
    
    try:
        response = llm.generate(
            test_prompt, 
            system_message="You are a helpful coding assistant specialized in Python.",
            max_tokens=1000
        )
        print(f"\n✅ Response received ({len(response)} characters):")
        print("-"*70)
        print(response)
        print("-"*70)
        
        # Test with different model
        print("\n\n2️⃣  Testing with Claude 3.5 Sonnet...")
        response2 = llm.generate(
            "What are the key differences between Python lists and tuples? Give 3 main points.",
            system_message="You are a Python expert.",
            model="claude-3-5-sonnet-20241022",
            max_tokens=500
        )
        print(f"\n✅ Response received ({len(response2)} characters):")
        print("-"*70)
        print(response2)
        print("-"*70)
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ All Claude tests completed successfully!")
    print("="*70)
    return True

def test_model_switching():
    """Test switching between different providers"""
    
    print("\n\n" + "="*70)
    print("🧪 Testing Model Switching")
    print("="*70)
    
    test_prompt = "Say 'Hello from' followed by your model name in one short sentence."
    
    # Test with different providers
    providers = [
        ("anthropic", "claude-sonnet-4-20250514"),
        ("github_copilot_cli", "gpt-4o"),
        ("ollama", "llama3.2")
    ]
    
    for provider, model in providers:
        print(f"\n🔄 Testing {provider} with {model}...")
        try:
            llm = LLMManager(provider=provider, model=model)
            response = llm.generate(test_prompt, max_tokens=100)
            print(f"   Response: {response[:200]}")
        except Exception as e:
            print(f"   ⚠️  Skipped (not configured): {e}")

if __name__ == "__main__":
    # Run main Claude test
    success = test_claude()
    
    # Run model switching test if Claude works
    if success:
        test_model_switching()
    
    sys.exit(0 if success else 1)
