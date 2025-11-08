#!/usr/bin/env python3
"""
Test script for GitHub Copilot integration via VS Code

Note: GitHub Copilot doesn't provide a public API for programmatic access.
This script demonstrates how to:
1. Test if Copilot is available
2. Use alternative methods to leverage Copilot
3. Provide instructions for interactive Copilot usage
"""

import os
import sys
import subprocess
import json
from typing import Dict, Optional

def check_vscode_installed() -> bool:
    """Check if VS Code is installed"""
    try:
        result = subprocess.run(['code', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ VS Code installed: {version}")
            return True
        else:
            print("❌ VS Code not found")
            return False
    except FileNotFoundError:
        print("❌ VS Code 'code' command not found")
        print("   Install VS Code or add it to PATH")
        return False

def check_copilot_extension() -> bool:
    """Check if GitHub Copilot extension is installed"""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True,
            text=True
        )
        
        extensions = result.stdout.split('\n')
        
        has_copilot = 'github.copilot' in extensions
        has_copilot_chat = 'github.copilot-chat' in extensions
        
        if has_copilot:
            print("✅ GitHub Copilot extension installed")
        else:
            print("❌ GitHub Copilot extension not installed")
            print("   Install: code --install-extension github.copilot")
        
        if has_copilot_chat:
            print("✅ GitHub Copilot Chat extension installed")
        else:
            print("❌ GitHub Copilot Chat extension not installed")
            print("   Install: code --install-extension github.copilot-chat")
        
        return has_copilot or has_copilot_chat
        
    except Exception as e:
        print(f"❌ Error checking extensions: {e}")
        return False

def check_github_cli() -> bool:
    """Check if GitHub CLI is installed"""
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ GitHub CLI installed: {version_line}")
            
            # Check for Copilot extension
            ext_result = subprocess.run(['gh', 'extension', 'list'], capture_output=True, text=True)
            if 'gh-copilot' in ext_result.stdout or 'copilot' in ext_result.stdout:
                print("✅ GitHub Copilot CLI extension installed")
                print("   Note: gh copilot extension has been deprecated")
            else:
                print("ℹ️  GitHub Copilot CLI extension not installed")
            
            return True
        else:
            print("❌ GitHub CLI not working properly")
            return False
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not found")
        print("   Install: brew install gh")
        return False

def demonstrate_copilot_usage():
    """Demonstrate how to use GitHub Copilot"""
    
    print("\n" + "="*70)
    print("📚 How to Use GitHub Copilot for Your AI Agents")
    print("="*70)
    
    print("""
GitHub Copilot is designed for interactive use in VS Code, not programmatic API calls.
Here's how to effectively use it with your AI agent project:

1️⃣  INLINE SUGGESTIONS
   - Open any Python file in VS Code
   - Start typing a comment or function
   - Copilot will suggest completions (press Tab to accept)
   
   Example:
   ```python
   # Function to analyze code complexity
   def analyze_complexity(code):
       # Copilot will suggest the implementation
   ```

2️⃣  COPILOT CHAT (Cmd+I or Ctrl+I)
   - Press Cmd+I (Mac) or Ctrl+I (Windows/Linux)
   - Ask questions like:
     * "Explain this code"
     * "Refactor this to use dependency injection"
     * "Add error handling to this function"
     * "Generate unit tests for this class"

3️⃣  COPILOT SIDEBAR
   - Click Copilot icon in sidebar
   - Chat with Copilot about your entire project
   - Ask architecture questions
   - Get code suggestions

4️⃣  USING WITH YOUR AI AGENTS
   
   Hybrid Approach (Recommended):
   
   a) Use Ollama for automated agent tasks:
      - Batch processing multiple files
      - Automated code analysis
      - Initial code generation
   
   b) Use GitHub Copilot for refinement:
      - Review Ollama-generated code
      - Refactor and improve
      - Add edge cases
      - Write better tests

5️⃣  WORKFLOW EXAMPLE
   
   Step 1: Let Ollama agents generate code
   $ python workflows/migration_pipeline.py
   
   Step 2: Open generated code in VS Code
   $ code generated_code/
   
   Step 3: Use Copilot to review and improve
   - Press Cmd+I
   - Type: "Review this code for security and best practices"
   
   Step 4: Apply suggestions and commit
   $ git add .
   $ git commit -m "AI-assisted migration"

6️⃣  COPILOT COMMANDS IN VS CODE
   
   Right-click on code:
   • Explain This
   • Fix This
   • Generate Docs
   • Generate Tests
   
   Or use Command Palette (Cmd+Shift+P):
   • GitHub Copilot: Explain
   • GitHub Copilot: Fix
   • GitHub Copilot: Generate Docs
   • GitHub Copilot: Generate Tests

7️⃣  AVAILABLE MODELS IN COPILOT
   
   Your Copilot subscription includes access to:
   • GPT-4 Turbo
   • Claude 3.5 Sonnet (in Copilot Chat)
   • GPT-3.5 Turbo
   
   You can select models in Copilot Chat settings.
""")

def create_copilot_demo_file():
    """Create a demo file to test Copilot with"""
    
    demo_code = '''"""
Demo file for testing GitHub Copilot

Open this file in VS Code with Copilot enabled and try:
1. Uncommenting the prompts below
2. Letting Copilot suggest implementations
3. Using Cmd+I to chat with Copilot
"""

# TODO: Uncomment the prompts below and let Copilot suggest the implementation

# Prompt 1: Function to validate email addresses
# def validate_email(email: str) -> bool:


# Prompt 2: Class for managing a priority queue
# class PriorityQueue:


# Prompt 3: Async function to fetch data from API with retry logic
# async def fetch_with_retry(url: str, max_retries: int = 3):


# Prompt 4: Generator function for fibonacci sequence
# def fibonacci_generator():


# Try Copilot Chat:
# 1. Select any function above
# 2. Press Cmd+I (Mac) or Ctrl+I (Windows)
# 3. Ask: "Add comprehensive error handling and logging"
# 4. Ask: "Generate pytest unit tests for this"
# 5. Ask: "Explain the time complexity"

# Example of using Copilot for code review:
def process_data(data):
    """Process incoming data"""
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Select the function above and ask Copilot:
# "Review this code and suggest improvements for performance and readability"
'''
    
    demo_file = 'copilot_demo.py'
    with open(demo_file, 'w') as f:
        f.write(demo_code)
    
    print(f"\n✅ Created demo file: {demo_file}")
    print(f"   Open it with: code {demo_file}")
    print("   Then try the exercises in the file!")

def test_copilot_alternatives():
    """Test alternatives that work programmatically"""
    
    print("\n" + "="*70)
    print("🔄 Alternative: Using Ollama (Programmatic)")
    print("="*70)
    
    try:
        # Test Ollama connection
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"\n✅ Ollama is running with {len(models)} model(s):")
            for model in models:
                print(f"   • {model['name']}")
            
            print("\n💡 Recommendation:")
            print("   Use Ollama for automated agent tasks")
            print("   Use GitHub Copilot in VS Code for interactive refinement")
            
        else:
            print("⚠️  Ollama is not responding properly")
            
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running")
        print("   Start it with: ollama serve")
    except ImportError:
        print("⚠️  requests library not installed")
        print("   Install: pip install requests")
    except Exception as e:
        print(f"⚠️  Error checking Ollama: {e}")

def main():
    """Main test function"""
    
    print("="*70)
    print("🧪 GitHub Copilot Integration Test")
    print("="*70)
    
    print("\n📋 Checking Prerequisites...\n")
    
    # Check installations
    vscode_ok = check_vscode_installed()
    copilot_ok = check_copilot_extension() if vscode_ok else False
    gh_ok = check_github_cli()
    
    # Show usage instructions
    demonstrate_copilot_usage()
    
    # Create demo file
    create_copilot_demo_file()
    
    # Test alternatives
    test_copilot_alternatives()
    
    # Final summary
    print("\n" + "="*70)
    print("📊 Summary")
    print("="*70)
    
    if copilot_ok:
        print("\n✅ GitHub Copilot is ready to use in VS Code!")
        print("\nNext steps:")
        print("1. Open VS Code: code .")
        print("2. Try Copilot inline suggestions")
        print("3. Use Cmd+I for Copilot Chat")
        print("4. Review generated code from Ollama agents")
    else:
        print("\n⚠️  GitHub Copilot is not fully set up")
        print("\nTo install:")
        print("1. Install extensions:")
        print("   code --install-extension github.copilot")
        print("   code --install-extension github.copilot-chat")
        print("2. Restart VS Code")
        print("3. Sign in to GitHub Copilot")
    
    print("\n💡 For automated tasks, use Ollama:")
    print("   python workflows/migration_pipeline.py")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
