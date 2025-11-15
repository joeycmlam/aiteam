#!/usr/bin/env python3
"""Test script to verify GitHub Copilot CLI integration"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.llm_manager import LLMManager

def test_llm_manager():
    """Test LLM Manager with different providers"""
    
    load_dotenv()
    
    print("="*60)
    print("🧪 Testing LLM Manager")
    print("="*60)
    
    # Test prompt
    test_prompt = "Write a simple Python function that adds two numbers. Just provide the code."
    
    # Test with configured provider
    print("\n1️⃣  Testing with configured provider...")
    llm = LLMManager("github_copilot_cli")  # Uses LLM_PROVIDER from .env (ollama)
    
    print(f"\n📝 Prompt: {test_prompt}")
    print("\n⏳ Generating response...")
    
    try:
        response = llm.generate(test_prompt, system_message="You are a helpful coding assistant.")
        print(f"\n✅ Response received ({len(response)} characters):")
        print("-"*60)
        print(response[:500])  # Print first 500 chars
        if len(response) > 500:
            print("...(truncated)")
        print("-"*60)
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return False
    
    print("\n✅ Test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_llm_manager()
    sys.exit(0 if success else 1)
