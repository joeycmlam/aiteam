#!/usr/bin/env python3
"""
Example: Using Claude 3.5 Sonnet via GitHub Models API

This demonstrates how to use Claude 3.5 Sonnet with your GitHub Copilot license
through the GitHub Models API.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.llm_manager import LLMManager

def example_claude_usage():
    """Show different ways to use Claude 3.5 Sonnet"""
    
    load_dotenv()
    
    print("🎯 Claude 3.5 Sonnet Usage Examples")
    print("=" * 70)
    print()
    
    # Check if GitHub token is configured
    if not os.getenv('GITHUB_TOKEN'):
        print("⚠️  GITHUB_TOKEN not configured")
        print("   See GITHUB_MODELS_SETUP.md for setup instructions")
        print()
        print("   Using Ollama as fallback for this demo...")
        provider = "ollama"
    else:
        provider = "github_copilot_cli"  # This now uses GitHub Models API
    
    # Initialize LLM with Claude 3.5 Sonnet
    llm = LLMManager(provider)
    print()
    
    # Example 1: Code generation
    print("-" * 70)
    print("Example 1: Generate Python Code")
    print("-" * 70)
    print()
    
    code = llm.generate_code(
        requirements="""
        Create a Python class called 'TaskManager' that:
        - Stores a list of tasks with priority levels
        - Can add, remove, and list tasks
        - Can filter tasks by priority
        - Includes type hints and docstrings
        """,
        language="python"
    )
    
    print("Generated Code:")
    print(code)
    print()
    
    # Example 2: Code review
    print("-" * 70)
    print("Example 2: Code Review")
    print("-" * 70)
    print()
    
    legacy_code = """
def calc(x, y, op):
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y
"""
    
    review = llm.analyze_code(
        legacy_code,
        "Review this code and suggest improvements for production use"
    )
    
    print("Code Review:")
    print(review)
    print()
    
    # Example 3: Architecture analysis
    print("-" * 70)
    print("Example 3: Architecture Analysis")
    print("-" * 70)
    print()
    
    architecture_prompt = """
    We're migrating a monolithic Django application to microservices.
    
    Current system:
    - 50,000 lines of Python code
    - PostgreSQL database with 40 tables
    - 15 API endpoints
    - Mix of REST and legacy SOAP services
    
    Suggest a microservices architecture with:
    1. Service boundaries
    2. Communication patterns
    3. Data migration strategy
    4. Risk assessment
    """
    
    architecture = llm.generate(
        architecture_prompt,
        system_message="You are a senior software architect with expertise in microservices migration."
    )
    
    print("Architecture Recommendations:")
    print(architecture)
    print()
    
    # Example 4: Compare with Ollama
    print("-" * 70)
    print("Example 4: Hybrid Strategy (Claude + Ollama)")
    print("-" * 70)
    print()
    
    print("💡 Best Practice: Use the right tool for each task!")
    print()
    
    # Complex decision → Claude 3.5 Sonnet
    if os.getenv('GITHUB_TOKEN'):
        print("🧠 Using Claude 3.5 Sonnet for: Architecture decision")
        claude = LLMManager("github_copilot_cli")
        decision = claude.generate(
            "Should we use GraphQL or REST for our new API?",
            system_message="You are a technical architect."
        )
        print(f"Decision analysis: {decision[:150]}...")
        print()
    
    # Bulk generation → Ollama (local)
    print("⚡ Using Ollama for: Bulk code generation")
    ollama = LLMManager("ollama")
    test_data = ollama.generate(
        "Generate 3 sample user records in JSON format",
        system_message="You are a data generator."
    )
    print(f"Test data: {test_data[:150]}...")
    print()
    
    print("=" * 70)
    print("✅ Examples complete!")
    print()
    print("💡 Key Takeaways:")
    print("   - Claude 3.5 Sonnet: Complex tasks, architecture, reviews")
    print("   - Ollama: Bulk generation, testing, experimentation")
    print("   - Both work seamlessly with the same LLMManager interface")

if __name__ == "__main__":
    example_claude_usage()
