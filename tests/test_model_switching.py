#!/usr/bin/env python3
"""
Test Model Switching with Enhanced LLM Manager

Demonstrates the ability to:
1. Initialize with a specific model
2. Override model per request
3. Switch between different models dynamically
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.llm_manager import LLMManager

def test_model_switching():
    """Test model switching capabilities"""
    
    print("=" * 70)
    print("🧪 Testing Model Switching with Enhanced LLM Manager")
    print("=" * 70)
    print()
    
    load_dotenv(override=True)
    
    # Test 1: Initialize with default model
    print("-" * 70)
    print("Test 1: Default Model (from .env or code default)")
    print("-" * 70)
    print()
    
    llm_default = LLMManager("github_copilot_cli")
    print()
    
    # Test 2: Initialize with custom model
    print("-" * 70)
    print("Test 2: Initialize with Custom Model (gpt-4o-mini)")
    print("-" * 70)
    print()
    
    llm_mini = LLMManager("github_copilot_cli", model="gpt-4o-mini")
    print()
    
    # Test 3: Override model per request
    print("-" * 70)
    print("Test 3: Override Model Per Request")
    print("-" * 70)
    print()
    
    llm = LLMManager("github_copilot_cli")
    print()
    
    # Test 3a: Use default model
    print("3a. Using default model (gpt-4o):")
    response1 = llm.generate(
        "Write a one-line Python function to reverse a string",
        model=None  # Use default
    )
    print(f"Response length: {len(response1)} characters")
    print(f"Preview: {response1[:100]}...")
    print()
    
    # Test 3b: Override with gpt-4o-mini
    print("3b. Override with gpt-4o-mini:")
    response2 = llm.generate(
        "Write a one-line Python function to reverse a string",
        model="gpt-4o-mini"  # Override
    )
    print(f"Response length: {len(response2)} characters")
    print(f"Preview: {response2[:100]}...")
    print()
    
    # Test 3c: Override with mistral-large
    print("3c. Override with mistral-large:")
    response3 = llm.generate(
        "Write a one-line Python function to reverse a string",
        model="mistral-large"  # Override
    )
    print(f"Response length: {len(response3)} characters")
    print(f"Preview: {response3[:100]}...")
    print()
    
    # Test 4: Test with Ollama models
    print("-" * 70)
    print("Test 4: Ollama Model Switching")
    print("-" * 70)
    print()
    
    # Test 4a: Default Ollama model
    print("4a. Default Ollama model (llama3.2):")
    ollama_llm = LLMManager("ollama")
    print()
    response4 = ollama_llm.generate("Say hello in Python")
    print(f"Response: {response4[:100]}...")
    print()
    
    # Test 4b: Override Ollama model (if you have other models)
    # print("4b. Override with different Ollama model:")
    # response5 = ollama_llm.generate("Say hello in Python", model="llama3.1")
    # print(f"Response: {response5[:100]}...")
    # print()
    
    # Test 5: Test analyze_code with model override
    print("-" * 70)
    print("Test 5: analyze_code() with Model Override")
    print("-" * 70)
    print()
    
    code_sample = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
    
    print("5a. Using default model:")
    analysis1 = llm.analyze_code(code_sample, "What improvements can be made?")
    print(f"Analysis length: {len(analysis1)} characters")
    print()
    
    print("5b. Using gpt-4o-mini:")
    analysis2 = llm.analyze_code(code_sample, "What improvements can be made?", model="gpt-4o-mini")
    print(f"Analysis length: {len(analysis2)} characters")
    print()
    
    # Test 6: Test generate_code with model override
    print("-" * 70)
    print("Test 6: generate_code() with Model Override")
    print("-" * 70)
    print()
    
    print("6a. Using default model:")
    code1 = llm.generate_code("Create a function to validate email addresses", model="gpt-4o")
    print(f"Code length: {len(code1)} characters")
    print()
    
    print("6b. Using gpt-4o-mini:")
    code2 = llm.generate_code("Create a function to validate email addresses", model="gpt-4o-mini")
    print(f"Code length: {len(code2)} characters")
    print()
    
    # Summary
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print()
    print("✅ All model switching tests completed!")
    print()
    print("🎯 Capabilities Demonstrated:")
    print("   1. Initialize LLM with specific model")
    print("   2. Override model per request")
    print("   3. Switch between multiple models (gpt-4o, gpt-4o-mini, mistral-large)")
    print("   4. Use model parameter in helper methods (analyze_code, generate_code)")
    print("   5. Fallback to Ollama with model selection")
    print()
    print("💡 Use Cases:")
    print("   • Use gpt-4o for complex tasks (architecture, reviews)")
    print("   • Use gpt-4o-mini for simple/fast tasks (formatting, simple queries)")
    print("   • Use mistral-large for alternative perspective")
    print("   • Use Ollama for unlimited local generation")
    print()

if __name__ == "__main__":
    try:
        test_model_switching()
        print("✅ All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
