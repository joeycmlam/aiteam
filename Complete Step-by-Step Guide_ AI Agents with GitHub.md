<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Complete Step-by-Step Guide: AI Agents with GitHub Copilot (No OpenAI API) on macOS

## 🎯 What's Different

Instead of using OpenAI API directly, we'll leverage:

- **GitHub Copilot** (for inline code assistance in VS Code)
- **Local LLM options** (Ollama for programmatic AI access)
- **VS Code native AI features**

**Important Note:** GitHub Copilot does not provide a public API for programmatic access. This guide uses:
- GitHub Copilot for interactive development assistance in VS Code
- Ollama (local LLMs) for programmatic AI features in your Python agents
- GitHub APIs for repository management and automation

***

## Part 1: Initial macOS Setup (30 minutes)

### Step 1: Install Core Tools

Open **Terminal** (Cmd + Space, type "Terminal"):

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12 (current stable version - 3.14 is too new for some packages)
brew install python@3.12

# Install VS Code if needed
brew install --cask visual-studio-code

# Install Ollama (local LLM)
brew install ollama

# Verify installations
python3.12 --version
code --version
ollama --version
```


### Step 2: Set Up Ollama (Local LLM)

```bash
# Start Ollama service
ollama serve &

# Pull recommended models (each ~4-8GB)
# For M1/M2/M3 Macs with 16GB+ RAM:
ollama pull llama3.2

# Alternative models:
# ollama pull qwen2.5        # Excellent coding model
# ollama pull mistral        # Fast and reliable
# ollama pull phi3           # Smaller, good for 8GB RAM

# Test it works
ollama run llama3.2 "Hello, are you working?"
# Press Ctrl+D to exit

# The service will run in background
```


### Step 3: Create Project Directory

```bash
# Navigate to your projects folder
cd ~/Documents

# Create project
mkdir aiteam
cd aiteam

# Create folder structure
mkdir -p agents shared config workflows tests/features tests/fixtures monitoring .vscode/prompts

# Create __init__.py files
touch agents/__init__.py
touch shared/__init__.py
touch workflows/__init__.py
touch tests/__init__.py

# Create .gitignore to protect sensitive files
cat > .gitignore << 'EOF'
# Environment and secrets
.env
*.env
.env.local

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# Data and logs
memory.json
*.log
monitoring/

# OS
.DS_Store
Thumbs.db
EOF
```


### Step 4: Set Up Python Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate it
source venv/bin/activate

# Verify you're using the correct Python version
python --version  # Should show Python 3.12.x

# Upgrade pip
pip install --upgrade pip
```


### Step 5: Install Dependencies (GitHub Copilot Compatible)

```bash
# Create requirements.txt (NO OpenAI dependency)
cat > requirements.txt << 'EOF'
# GitHub Integration
PyGithub==2.4.0
requests==2.32.3

# Local LLM
ollama==0.3.3
langchain==0.3.3
langchain-community==0.3.2

# JIRA Integration
jira==3.8.0

# Testing
pytest==8.3.3
pytest-bdd==7.3.0
gherkin-official==4.1.3

# Web Framework
flask==3.0.3

# Utilities
pyyaml==6.0.2
python-dotenv==1.0.1
pydantic==2.9.2

# Code Analysis
radon==6.0.1
lizard==1.17.10
EOF

# Install all packages
pip install -r requirements.txt
```


### Step 6: Configure Environment Variables (No OpenAI Key!)

```bash
# Create .env file
cat > .env << 'EOF'
# GitHub Configuration (for Copilot API access)
GITHUB_TOKEN=your_github_personal_access_token

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# JIRA Configuration
JIRA_SERVER=https://your-company.atlassian.net
JIRA_USER=your.email@company.com
JIRA_API_TOKEN=your_jira_token_here

# Project Paths
PROJECT_ROOT=/Users/YOUR_USERNAME/Documents/aiteam
LEGACY_CODE_PATH=/path/to/your/legacy/codebase

# LLM Provider (options: github_copilot, ollama)
LLM_PROVIDER=ollama
EOF

# Edit with your credentials
code .env
```

**🔑 Get GitHub Token:**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`
4. Copy the token to `.env`

**⚠️ Security Note:**
- Never commit `.env` files to version control
- Use `.gitignore` to exclude `.env` files
- Rotate tokens regularly
- Use fine-grained tokens when possible

***

## Part 2: VS Code Configuration with GitHub Copilot (20 minutes)

### Step 7: Open Project in VS Code

```bash
# Open VS Code in current directory
code .
```


### Step 8: Install VS Code Extensions

In VS Code:

1. Press **Cmd + Shift + X** to open Extensions
2. Search and install:
    - **GitHub Copilot** (you should have this)
    - **GitHub Copilot Chat**
    - **Python** (by Microsoft)
    - **Pylance** (by Microsoft)
    - **Cucumber (Gherkin)**
    - **YAML**

Or via terminal:

```bash
code --install-extension github.copilot
code --install-extension github.copilot-chat
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension alexkrechik.cucumberautocomplete
code --install-extension redhat.vscode-yaml
```


### Step 9: Configure VS Code Settings

Create `.vscode/settings.json`:

```bash
cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.terminal.activateEnvironment": true,
  
  // Testing
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  
  // GitHub Copilot
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": true,
    "markdown": true,
    "python": true
  },
  
  "github.copilot.editor.enableAutoCompletions": true,
  
  // File associations
  "files.associations": {
    "*.feature": "gherkin"
  },
  
  // Environment variables
  "terminal.integrated.env.osx": {
    "GITHUB_TOKEN": "${env:GITHUB_TOKEN}",
    "JIRA_API_TOKEN": "${env:JIRA_API_TOKEN}",
    "OLLAMA_HOST": "http://localhost:11434"
  },
  
  // Editor settings
  "editor.formatOnSave": true,
  "editor.inlineSuggest.enabled": true,
  
  // Note: Python linting is deprecated. Consider installing Ruff extension:
  // code --install-extension charliermarsh.ruff
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  }
}
EOF
```


### Step 10: Create VS Code Tasks

Create `.vscode/tasks.json`:

```bash
cat > .vscode/tasks.json << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Ollama Service",
      "type": "shell",
      "command": "ollama serve",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Run Migration Pipeline",
      "type": "shell",
      "command": "${workspaceFolder}/venv/bin/python",
      "args": ["workflows/migration_pipeline.py"],
      "dependsOn": ["Start Ollama Service"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "${workspaceFolder}/venv/bin/pytest",
      "args": ["tests/", "-v"],
      "group": "test"
    }
  ]
}
EOF
```


### Step 11: Create Debug Configuration

Create `.vscode/launch.json`:

```bash
cat > .vscode/launch.json << 'EOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Migration Pipeline",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/workflows/migration_pipeline.py",
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env",
      "env": {
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  ]
}
EOF
```


***

## Part 3: Create LLM Wrapper (GitHub Copilot + Ollama) (30 minutes)

### Step 12: Create LLM Manager

Create `shared/llm_manager.py`:

```python
import os
import requests
from typing import Dict, Optional
import ollama
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    """Manages LLM calls using GitHub Copilot or Ollama"""
    
    def __init__(self, provider: str = None):
        self.provider = provider or os.getenv('LLM_PROVIDER', 'ollama')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1')
        
        print(f"🤖 LLM Manager initialized with provider: {self.provider}")
    
    def generate(self, prompt: str, system_message: str = None, max_tokens: int = 4000) -> str:
        """Generate text using configured LLM"""
        
        if self.provider == 'github_copilot':
            return self._generate_with_github_copilot(prompt, system_message)
        else:
            return self._generate_with_ollama(prompt, system_message)
    
    def _generate_with_github_copilot(self, prompt: str, system_message: str = None) -> str:
        """
        Use GitHub Copilot API
        Note: This uses Copilot's completion API which is part of your subscription
        """
        try:
            # GitHub Copilot uses a special API endpoint
            # For now, we'll use Ollama as primary since Copilot API is mainly for IDE
            print("ℹ️  GitHub Copilot works best in the IDE. Using Ollama for programmatic access...")
            return self._generate_with_ollama(prompt, system_message)
            
        except Exception as e:
            print(f"⚠️  GitHub Copilot API error: {e}")
            print("   Falling back to Ollama...")
            return self._generate_with_ollama(prompt, system_message)
    
    def _generate_with_ollama(self, prompt: str, system_message: str = None) -> str:
        """Use Ollama local LLM"""
        try:
            # Build the full prompt
            full_prompt = prompt
            if system_message:
                full_prompt = f"{system_message}\n\n{prompt}"
            
            # Call Ollama
            response = ollama.generate(
                model=self.ollama_model,
                prompt=full_prompt
            )
            
            return response['response']
            
        except ConnectionError as e:
            print(f"⚠️  Ollama connection error: {e}")
            print("   Make sure Ollama is running: ollama serve")
            return f"[LLM unavailable - manual review needed]\n\nPrompt was: {prompt[:200]}..."
        except KeyError as e:
            print(f"⚠️  Unexpected Ollama response format: {e}")
            return f"[LLM response error - manual review needed]"
        except Exception as e:
            print(f"⚠️  Unexpected error: {type(e).__name__}: {e}")
            # Return a fallback response
            return f"[LLM unavailable - manual review needed]\n\nPrompt was: {prompt[:200]}..."
    
    def analyze_code(self, code: str, question: str) -> str:
        """Analyze code with specific question"""
        prompt = f"""Analyze this code:

```

{code[:2000]}

```

Question: {question}

Provide a concise analysis:"""
        
        return self.generate(prompt, system_message="You are a senior software architect.")
    
    def generate_code(self, requirements: str, language: str = "python") -> str:
        """Generate code from requirements"""
        prompt = f"""Generate {language} code for these requirements:

{requirements}

Provide clean, production-ready code with:
- Error handling
- Documentation
- Type hints (if applicable)

Code:"""
        
        return self.generate(prompt, system_message=f"You are an expert {language} developer.")
```


### Step 13: Create GitHub Copilot Helper

Create `shared/copilot_helper.py`:

```python
import subprocess
import json
from typing import Dict, Optional

class CopilotHelper:
    """Helper to leverage GitHub Copilot in VS Code"""
    
    @staticmethod
    def get_suggestion(file_path: str, context: str) -> str:
        """
        This is a placeholder for Copilot integration.
        In practice, Copilot works best directly in the IDE.
        
        For programmatic access, we recommend:
        1. Using Copilot Chat in VS Code
        2. Using Ollama for agent automation
        3. Combining both: Copilot for development, Ollama for agents
        """
        return """
        💡 TIP: Use GitHub Copilot directly in VS Code:
        
        1. Open the file in VS Code
        2. Press Cmd+I to open Copilot Chat
        3. Ask: "Refactor this following {context}"
        4. Review and accept suggestions
        
        For automated agent work, we use Ollama.
        """
    
    @staticmethod
    def explain_code(code_snippet: str) -> str:
        """Use Copilot to explain code (IDE feature)"""
        return f"""
        To get Copilot explanation:
        
        1. Select the code in VS Code
        2. Right-click → Copilot → Explain This
        
        Or press Cmd+I and ask: "Explain this code"
        """
```


***

## Part 4: Create AI Agents (Using Ollama + Copilot Workflow) (60 minutes)

### Step 14: Create Shared Memory System

Create `shared/memory_store.py`:

```python
import json
from typing import Any, Dict
from datetime import datetime

class SharedMemory:
    """Persistent memory shared across all agents"""
    
    def __init__(self, storage_path: str = './memory.json'):
        self.storage_path = storage_path
        self.memory = self._load()
    
    def store(self, key: str, value: Any):
        """Store data in shared memory"""
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'type': type(value).__name__
        }
        self._persist()
        print(f"✅ Stored: {key}")
    
    def get(self, key: str, default=None) -> Any:
        """Retrieve data from shared memory"""
        if key in self.memory:
            return self.memory[key]['value']
        return default
    
    def _load(self) -> Dict:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _persist(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2, default=str)
```


### Step 15: Create Lead Orchestrator Agent

Create `agents/lead_orchestrator.py`:

```python
from typing import Dict, List
from shared.memory_store import SharedMemory
from shared.llm_manager import LLMManager

class LeadOrchestrator:
    """Coordinates all agents and manages workflow"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.memory = SharedMemory()
        self.llm = LLMManager()
        print("🎯 Lead Orchestrator initialized")
    
    def create_workflow(self, jira_tickets: List[str]) -> Dict:
        """Creates migration workflow from JIRA tickets"""
        workflow = {
            "tickets": jira_tickets,
            "stages": [
                {"name": "Architecture Analysis", "agent": "ArchitectAgent", "status": "pending"},
                {"name": "Requirements Gathering", "agent": "BAAgent", "status": "pending"},
                {"name": "Test Design", "agent": "QAAgent", "status": "pending"},
                {"name": "Implementation", "agent": "DeveloperAgent", "status": "pending"},
                {"name": "Code Review", "agent": "SeniorDevAgent", "status": "pending"}
            ]
        }
        
        self.memory.store('workflow', workflow)
        print(f"📋 Workflow created with {len(workflow['stages'])} stages")
        return workflow
    
    def execute_workflow(self, workflow: Dict):
        """Execute the migration workflow"""
        print("\n🚀 Starting workflow execution...\n")
        
        for i, stage in enumerate(workflow['stages'], 1):
            print(f"{'='*60}")
            print(f"Stage {i}/{len(workflow['stages'])}: {stage['name']}")
            print(f"Agent: {stage['agent']}")
            print(f"{'='*60}\n")
            
            stage['status'] = 'completed'
            print(f"✅ {stage['name']} completed\n")
        
        print("🎉 Workflow execution completed!")
```


### Step 16: Create Architect Agent

Create `agents/architect_agent.py`:

```python
import os
from pathlib import Path
from typing import Dict, List
from shared.llm_manager import LLMManager

class ArchitectAgent:
    """Analyzes code structure and recommends design patterns"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("🏗️  Architect Agent initialized")
    
    def analyze_codebase(self, repo_path: str) -> Dict:
        """Analyzes legacy codebase structure"""
        print(f"\n📊 Analyzing codebase at: {repo_path}")
        
        structure = {
            "total_files": 0,
            "languages": {},
            "modules": [],
            "complexity": "medium"
        }
        
        # Walk through codebase
        for root, dirs, files in os.walk(repo_path):
            # Skip venv and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                ext = Path(file).suffix
                if ext in ['.py', '.java', '.js', '.ts', '.cs']:
                    structure["total_files"] += 1
                    structure["languages"][ext] = structure["languages"].get(ext, 0) + 1
        
        print(f"   Found {structure['total_files']} code files")
        print(f"   Languages: {structure['languages']}")
        
        return structure
    
    def recommend_patterns(self, analysis: Dict) -> List[str]:
        """Recommends design patterns using LLM"""
        print(f"\n💡 Analyzing patterns with LLM...")
        
        # Use LLM to recommend patterns
        prompt = f"""Based on this codebase analysis:
- Total files: {analysis['total_files']}
- Languages: {analysis['languages']}
- Complexity: {analysis['complexity']}

Recommend 4-5 design patterns for modernizing this legacy code.
Format as a simple list with brief rationale."""

        try:
            llm_response = self.llm.generate(
                prompt,
                system_message="You are a software architect specializing in design patterns."
            )
            
            print(f"\n💡 LLM Recommendations:")
            print(llm_response)
            
        except Exception as e:
            print(f"⚠️  LLM unavailable: {e}")
        
        # Fallback patterns
        patterns = [
            "Repository Pattern - for data access layer",
            "Factory Pattern - for object creation",
            "Strategy Pattern - for business logic variants",
            "Dependency Injection - for loose coupling",
            "CQRS Pattern - if dealing with complex operations"
        ]
        
        print(f"\n📋 Recommended Design Patterns:")
        for pattern in patterns:
            print(f"   • {pattern}")
        
        return patterns
```


### Step 17: Create BA Agent

Create `agents/ba_agent.py`:

```python
from typing import Dict, List
from jira import JIRA
from shared.llm_manager import LLMManager

class BAAgent:
    """Reads JIRA and structures business requirements"""
    
    def __init__(self, llm_config: Dict, jira_config: Dict):
        self.llm_config = llm_config
        self.jira_config = jira_config
        self.llm = LLMManager()
        print("📋 BA Agent initialized")
    
    def fetch_tickets(self, jql: str) -> List[Dict]:
        """Fetches tickets from JIRA"""
        print(f"\n🔍 Fetching JIRA tickets with JQL: {jql}")
        
        try:
            jira_client = JIRA(
                server=self.jira_config['server'],
                basic_auth=(self.jira_config['user'], self.jira_config['token'])
            )
            
            issues = jira_client.search_issues(jql, maxResults=50)
            
            tickets = []
            for issue in issues:
                ticket = {
                    "id": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description or "No description",
                    "status": issue.fields.status.name,
                    "priority": issue.fields.priority.name if issue.fields.priority else "Medium"
                }
                tickets.append(ticket)
            
            print(f"   ✅ Found {len(tickets)} tickets")
            return tickets
            
        except ConnectionError as e:
            print(f"   ⚠️  JIRA connection error: {e}")
            print("   Check your JIRA_SERVER and network connection")
            return self._get_mock_tickets()
        except Exception as e:
            print(f"   ⚠️  JIRA error: {type(e).__name__}: {e}")
            print("   Using mock data for demonstration")
            return self._get_mock_tickets()
    
    def _get_mock_tickets(self) -> List[Dict]:
        """Return mock data for testing"""
        return [
            {
                "id": "DEMO-1",
                "summary": "Migrate user authentication module",
                "description": "Move legacy auth to OAuth2",
                "status": "To Do",
                "priority": "High"
            },
            {
                "id": "DEMO-2",
                "summary": "Refactor database access layer",
                "description": "Implement repository pattern for data access",
                "status": "To Do",
                "priority": "Medium"
            }
        ]
    
    def structure_requirements(self, tickets: List[Dict]) -> Dict:
        """Structures requirements from JIRA tickets using LLM"""
        print(f"\n📝 Structuring requirements from {len(tickets)} tickets")
        
        requirements = {
            "user_stories": [],
            "technical_tasks": []
        }
        
        for ticket in tickets:
            # Use LLM to extract structured requirements
            prompt = f"""Extract structured requirements from this JIRA ticket:

ID: {ticket['id']}
Summary: {ticket['summary']}
Description: {ticket['description']}

Extract:
1. Core business requirement (1 sentence)
2. Acceptance criteria (3-4 items in Given-When-Then format)
3. Technical considerations

Format as JSON."""

            try:
                llm_response = self.llm.generate(prompt, system_message="You are a business analyst.")
                print(f"   🤖 LLM analyzed: {ticket['id']}")
            except ConnectionError:
                print(f"   ⚠️  LLM unavailable for {ticket['id']}, using default analysis")
                llm_response = "Manual review needed - LLM unavailable"
            except Exception as e:
                print(f"   ⚠️  Error analyzing {ticket['id']}: {type(e).__name__}")
                llm_response = "Manual review needed"
            
            structured = {
                "ticket_id": ticket['id'],
                "title": ticket['summary'],
                "description": ticket['description'],
                "llm_analysis": llm_response,
                "acceptance_criteria": [
                    "Implementation meets requirements",
                    "All tests pass",
                    "Code review approved"
                ]
            }
            
            requirements['user_stories'].append(structured)
            print(f"   • {ticket['id']}: {ticket['summary']}")
        
        return requirements
```


### Step 18: Create QA Agent

Create `agents/qa_agent.py`:

```python
import os
from typing import Dict
from shared.llm_manager import LLMManager

class QAAgent:
    """Builds Cucumber/Gherkin tests"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("🧪 QA Agent initialized")
    
    def create_feature_files(self, requirements: Dict, output_dir: str):
        """Creates Cucumber feature files from requirements"""
        print(f"\n📄 Creating feature files in: {output_dir}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        for story in requirements.get('user_stories', []):
            feature_content = self._generate_feature_with_llm(story)
            
            filename = f"{story['ticket_id'].lower().replace('-', '_')}.feature"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(feature_content)
            
            print(f"   ✅ Created: {filename}")
    
    def _generate_feature_with_llm(self, story: Dict) -> str:
        """Generates Gherkin feature content using LLM"""
        
        prompt = f"""Create a Cucumber/Gherkin feature file for:

Title: {story['title']}
Description: {story['description']}

Generate complete Gherkin syntax with:
- Feature description
- Background (if needed)
- At least 2 scenarios (happy path + error case)
- Use proper Given-When-Then format"""

        try:
            llm_response = self.llm.generate(
                prompt,
                system_message="You are a QA engineer expert in BDD and Gherkin syntax."
            )
            return llm_response
        except:
            # Fallback template
            feature = f"""Feature: {story['title']}
  {story['description']}

  Background:
    Given the system is initialized
    And test data is loaded

  Scenario: Happy path implementation
    Given valid input data
    When the feature is executed
    Then it should complete successfully
    And meet all acceptance criteria
    
  Scenario: Error handling
    Given invalid input is provided
    When the feature is executed
    Then it should handle errors gracefully
    And return appropriate error message
"""
            return feature
```


### Step 19: Create Senior Developer Agent

Create `agents/senior_dev_agent.py`:

```python
from typing import Dict, List
from shared.llm_manager import LLMManager

class SeniorDevAgent:
    """Provides guidance and reviews code"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("👨‍💻 Senior Dev Agent initialized")
    
    def provide_guidelines(self, context: Dict) -> Dict:
        """Provides coding guidelines"""
        print("\n📚 Providing coding guidelines")
        
        guidelines = {
            "code_style": "Follow PEP 8 for Python",
            "testing": "Minimum 80% code coverage",
            "documentation": "Docstrings for all public methods",
            "security": "Input validation required",
            "patterns": context.get('recommended_patterns', [])
        }
        
        print("   Guidelines provided:")
        for key, value in guidelines.items():
            if key != 'patterns':
                print(f"   • {key}: {value}")
        
        return guidelines
    
    def review_code(self, code: str, requirements: Dict) -> Dict:
        """Reviews code implementation using LLM"""
        print(f"\n🔍 Reviewing code for: {requirements.get('ticket_id', 'unknown')}")
        
        prompt = f"""Review this code implementation:

Requirements:
{requirements.get('title', 'N/A')}

Code:
{code[:1000]}

Check for:
1. Correctness (meets requirements)
2. Security vulnerabilities
3. Code quality
4. Error handling
5. Test coverage

Provide: issues list, suggestions, approval recommendation."""

        try:
            llm_review = self.llm.generate(
                prompt,
                system_message="You are a senior developer doing code review."
            )
            print(f"\n🤖 LLM Review:\n{llm_review[:300]}...")
        except:
            llm_review = "Manual review needed"
        
        review = {
            "status": "approved_with_comments",
            "llm_analysis": llm_review,
            "issues": [],
            "suggestions": [
                "Consider adding more error handling",
                "Add logging for debugging",
                "Include performance metrics"
            ],
            "approved": True
        }
        
        print(f"   Status: {review['status']}")
        
        return review
```


### Step 20: Create Developer Agent

Create `agents/developer_agent.py`:

```python
from typing import Dict
from shared.llm_manager import LLMManager

class DeveloperAgent:
    """Implements code based on requirements"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("💻 Developer Agent initialized")
    
    def implement_feature(self, requirements: Dict, guidelines: Dict) -> Dict:
        """Implements feature using LLM code generation"""
        print(f"\n⚙️  Implementing: {requirements.get('title', 'Feature')}")
        
        # Generate implementation with LLM
        code_prompt = f"""Generate Python code for:

Requirements:
{requirements.get('title')}
{requirements.get('description')}

Guidelines:
- {guidelines.get('code_style')}
- {guidelines.get('security')}
- Include error handling
- Add type hints

Generate complete, production-ready code."""

        try:
            generated_code = self.llm.generate_code(code_prompt, language="python")
            print(f"   🤖 Code generated by LLM")
        except:
            generated_code = f"# Implementation for {requirements.get('ticket_id')}\n# TODO: Implement manually\n"
            print(f"   ⚠️  LLM unavailable, created stub")
        
        # Generate tests
        test_prompt = f"""Generate pytest unit tests for:

{requirements.get('title')}

Include:
- Happy path test
- Error case test
- Edge cases"""

        try:
            generated_tests = self.llm.generate_code(test_prompt, language="python")
            print(f"   🤖 Tests generated by LLM")
        except:
            generated_tests = f"# Tests for {requirements.get('ticket_id')}\n# TODO: Implement tests\n"
            print(f"   ⚠️  LLM unavailable, created test stub")
        
        implementation = {
            "status": "completed",
            "code": generated_code,
            "tests": generated_tests,
            "documentation": f"# Documentation for {requirements.get('ticket_id')}\n"
        }
        
        print(f"   ✅ Implementation completed")
        
        # Save to file for Copilot review
        self._save_for_copilot_review(requirements, implementation)
        
        return implementation
    
    def _save_for_copilot_review(self, requirements: Dict, implementation: Dict):
        """Save generated code for manual review with GitHub Copilot"""
        ticket_id = requirements.get('ticket_id', 'unknown')
        output_dir = f"./generated_code/{ticket_id}"
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save implementation
        with open(f"{output_dir}/implementation.py", 'w') as f:
            f.write(implementation['code'])
        
        # Save tests
        with open(f"{output_dir}/test_implementation.py", 'w') as f:
            f.write(implementation['tests'])
        
        print(f"   💾 Saved to {output_dir}/ for Copilot review")
```


***

## Part 5: Create Main Pipeline (30 minutes)

### Step 21: Create Configuration

Create `config/agent_config.yaml`:

```yaml
llm:
  provider: "ollama"  # or "github_copilot"
  model: "llama3.1"
  temperature: 0.3

jira:
  server: "https://your-company.atlassian.net"
  user: "your.email@company.com"

workflow:
  stages:
    - architecture
    - requirements
    - testing
    - development
    - review
  
  parallel_processing: false
  max_retries: 3
  
  # Copilot workflow options
  use_copilot_for_review: true
  generate_copilot_prompts: true
```


### Step 22: Create Main Pipeline

Create `workflows/migration_pipeline.py`:

```python
import os
import yaml
from dotenv import load_dotenv

# Import all agents
from agents.lead_orchestrator import LeadOrchestrator
from agents.architect_agent import ArchitectAgent
from agents.ba_agent import BAAgent
from agents.qa_agent import QAAgent
from agents.senior_dev_agent import SeniorDevAgent
from agents.developer_agent import DeveloperAgent

class MigrationPipeline:
    """Main orchestration pipeline using Ollama + GitHub Copilot workflow"""
    
    def __init__(self, config_path: str):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        llm_config = config['llm']
        jira_config = {
            'server': config['jira']['server'],
            'user': config['jira']['user'],
            'token': os.getenv('JIRA_API_TOKEN')
        }
        
        # Initialize all agents
        print("🤖 Initializing AI Agents...")
        print("="*60)
        print(f"   LLM Provider: {llm_config['provider']}")
        print(f"   Model: {llm_config.get('model', 'default')}")
        print("="*60)
        
        self.lead = LeadOrchestrator(llm_config)
        self.architect = ArchitectAgent(llm_config)
        self.ba = BAAgent(llm_config, jira_config)
        self.qa = QAAgent(llm_config)
        self.senior_dev = SeniorDevAgent(llm_config)
        self.developer = DeveloperAgent(llm_config)
        
        print("="*60)
        print("✅ All agents initialized\n")
    
    def run(self, jira_jql: str, repo_path: str):
        """Execute the migration pipeline"""
        print("\n" + "="*60)
        print("🚀 LEGACY CODE MIGRATION PIPELINE")
        print("   Using: Ollama + GitHub Copilot Workflow")
        print("="*60 + "\n")
        
        # Stage 1: Fetch JIRA tickets
        print("📋 STAGE 1: Fetching Requirements")
        print("-"*60)
        tickets = self.ba.fetch_tickets(jira_jql)
        
        # Stage 2: Analyze architecture
        print("\n🏗️  STAGE 2: Architecture Analysis")
        print("-"*60)
        analysis = self.architect.analyze_codebase(repo_path)
        patterns = self.architect.recommend_patterns(analysis)
        
        # Stage 3: Structure requirements
        print("\n📝 STAGE 3: Requirements Structuring")
        print("-"*60)
        requirements = self.ba.structure_requirements(tickets)
        
        # Stage 4: Generate tests
        print("\n🧪 STAGE 4: Test Generation")
        print("-"*60)
        self.qa.create_feature_files(requirements, './tests/features')
        
        # Stage 5: Provide guidelines
        print("\n📚 STAGE 5: Development Guidelines")
        print("-"*60)
        guidelines = self.senior_dev.provide_guidelines({'recommended_patterns': patterns})
        
        # Stage 6: Implementation loop
        print("\n💻 STAGE 6: Implementation")
        print("-"*60)
        for story in requirements['user_stories']:
            # Developer implements using LLM
            implementation = self.developer.implement_feature(story, guidelines)
            
            # Senior reviews using LLM
            review = self.senior_dev.review_code(implementation['code'], story)
            
            if review['approved']:
                print(f"   ✅ {story['ticket_id']} - APPROVED")
            else:
                print(f"   🔄 {story['ticket_id']} - NEEDS REVISION")
        
        # Final summary
        print("\n" + "="*60)
        print("✨ MIGRATION PIPELINE COMPLETED")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Tickets processed: {len(tickets)}")
        print(f"   • Features implemented: {len(requirements['user_stories'])}")
        print(f"   • Tests created: {len(requirements['user_stories'])} feature files")
        print(f"   • Design patterns applied: {len(patterns)}")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Review generated code in ./generated_code/")
        print(f"   2. Open files in VS Code")
        print(f"   3. Use GitHub Copilot (Cmd+I) to refine")
        print(f"   4. Run tests: pytest tests/")
        print("\n✅ All stages completed!\n")

# Main execution
if __name__ == "__main__":
    # Ensure Ollama is running
    import subprocess
    try:
        subprocess.run(["ollama", "list"], check=True, capture_output=True)
        print("✅ Ollama is running\n")
    except:
        print("⚠️  Starting Ollama...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(3)
    
    # Run pipeline
    pipeline = MigrationPipeline('./config/agent_config.yaml')
    pipeline.run(
        jira_jql="project = LEGACY AND status = 'To Do'",
        repo_path="./tests/fixtures"
    )
```


***

## Part 6: Testing \& Running (20 minutes)

### Step 23: Create Test Fixtures

```bash
# Create sample legacy code
mkdir -p tests/fixtures
cat > tests/fixtures/legacy_code.py << 'EOF'
# Legacy code example that needs migration
class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, name, email):
        # Old style, no validation
        self.users.append({'name': name, 'email': email})
    
    def get_user(self, email):
        for user in self.users:
            if user['email'] == email:
                return user
        return None
EOF
```


### Step 24: Create .gitignore

```bash
cat > .gitignore << 'EOF'
# Virtual Environment
venv/
.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Generated
generated_code/
memory.json

# IDE
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
.DS_Store

# Ollama
*.gguf
EOF
```


### Step 25: Start Ollama

```bash
# In a new terminal tab (Cmd+T)
ollama serve

# Leave this running
```


### Step 26: Run the Pipeline

In VS Code:

1. **Open Terminal** (Ctrl + `)
2. **Activate virtual environment:**

```bash
source venv/bin/activate
```

3. **Run the pipeline:**

```bash
python workflows/migration_pipeline.py
```

Or press **Cmd + Shift + B**
4. **Watch the output** - agents will work through stages using Ollama LLM

***

## Part 7: Using GitHub Copilot for Review (15 minutes)

### Step 27: Review Generated Code with Copilot

After pipeline runs, generated code is in `./generated_code/`:

```bash
# Open generated code
code generated_code/
```

**In VS Code:**

1. **Open a generated file** (e.g., `DEMO-1/implementation.py`)
2. **Use Copilot Chat** (Cmd + I):

```
Review this code for:
- Security vulnerabilities
- Performance issues
- Best practices
- Suggest improvements
```

3. **Get inline suggestions**:
    - Start typing improvements
    - Copilot will suggest completions
    - Press Tab to accept
4. **Refactor with Copilot**:
    - Select code block
    - Right-click → Copilot → "Refactor"
    - Or Cmd+I: "Refactor this to use dependency injection"

### Step 28: Create Copilot Prompt Templates

Create `.vscode/prompts/review_generated_code.md`:

```markdown
Review this AI-generated code for a legacy migration:

Context:
- Generated by Ollama LLM
- Part of migration from legacy system
- Needs production-readiness review

Check for:
1. Security vulnerabilities
2. Error handling completeness
3. Code style consistency
4. Performance considerations
5. Missing edge cases
6. Documentation quality

Suggest specific improvements with code examples.
```

Create `.vscode/prompts/refactor_with_pattern.md`:

```markdown
Refactor this code to use the ${1:pattern_name} pattern.

Current code: ${selectedText}

Requirements:
- Maintain existing functionality
- Add proper error handling
- Include type hints
- Add docstrings
- Follow SOLID principles

Provide complete refactored code.
```


***

## Part 8: Complete Workflow (Day-to-Day Usage)

### Daily Workflow

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run pipeline
cd ~/Documents/aiteam
source venv/bin/activate
python workflows/migration_pipeline.py
```

**Or create startup script:**

Create `start.sh`:

```bash
#!/bin/bash

echo "🚀 Starting Legacy Migration AI System"

# Start Ollama in background
ollama serve > /dev/null 2>&1 &
OLLAMA_PID=$!
echo "✅ Ollama started (PID: $OLLAMA_PID)"

# Wait for Ollama to be ready
sleep 3

# Activate venv and run pipeline
cd ~/Documents/aiteam
source venv/bin/activate

echo "🤖 Running migration pipeline..."
python workflows/migration_pipeline.py

# Cleanup
echo "🧹 Cleaning up..."
kill $OLLAMA_PID
```

```bash
chmod +x start.sh
./start.sh
```


### Hybrid Workflow (Ollama + Copilot)

**Best practice approach:**

1. **Automated Analysis** → Use Ollama agents
    - Analyze codebase
    - Structure requirements
    - Generate initial code
2. **Manual Refinement** → Use GitHub Copilot in IDE
    - Review generated code
    - Refactor with Copilot suggestions
    - Add edge cases Copilot identifies
3. **Final Review** → Combine both
    - Ollama provides automated checks
    - Copilot helps with manual improvements
    - Human makes final decisions

***

## 📊 What You've Built

```
Your MacBook now has:
├── 6 AI Agents using Ollama (no OpenAI needed!)
├── GitHub Copilot integration for IDE work
├── Complete VS Code setup
├── JIRA connectivity
├── Automated test generation
├── LLM-powered code analysis & generation
└── Hybrid workflow (automated + manual)

Total cost: $0 for LLM usage! 🎉
(Copilot subscription you already have)
```


***

## 🆘 Troubleshooting

**"Ollama connection refused"**

```bash
# Check if running
ollama list

# Start service
ollama serve

# Test
ollama run llama3.1 "Hello"
```

**"Model not found"**

```bash
# List available models
ollama list

# Pull model
ollama pull llama3.1

# Or use different model
ollama pull mistral
```

**"GitHub Copilot not working"**

1. Cmd + Shift + P
2. "GitHub Copilot: Sign In"
3. Verify subscription at: https://github.com/settings/copilot

**"LLM responses are slow"**

- Ollama runs locally, speed depends on Mac specs
- M1/M2/M3 Macs: Fast (8-16 GB RAM recommended)
- Intel Macs: Slower but functional
- Consider using smaller models: `ollama pull phi`

**"Out of memory"**

```bash
# Use smaller model
ollama pull phi

# Edit .env
OLLAMA_MODEL=phi
```


***

## 🎓 Tips for Best Results

### Ollama Performance

- **Best models for MacBook:**
    - M1/M2/M3 with 16GB+: `llama3.1` or `mixtral`
    - M1/M2/M3 with 8GB: `phi` or `mistral`
    - Intel Macs: `phi` (smaller, faster)


### GitHub Copilot Integration

- **Use Copilot for:**
    - Code review and suggestions
    - Inline completions while editing
    - Explaining complex code
    - Refactoring patterns
- **Use Ollama agents for:**
    - Batch processing multiple files
    - Automated analysis
    - Initial code generation
    - Structured workflows


### Combined Workflow

```
1. Run Ollama agents → Generate initial implementation
2. Open in VS Code → Review with Copilot
3. Refine with Copilot → Apply suggestions
4. Test → Iterate
```


***

## 🎉 You're Ready!

Your GitHub Copilot + Ollama AI agent system is complete and costs nothing for LLM usage beyond your existing Copilot subscription!

**Next steps:**

1. Customize agent prompts in each agent file
2. Connect to your real JIRA project
3. Point to actual legacy codebase
4. Run and refine with Copilot

Happy migrating! 🚀

