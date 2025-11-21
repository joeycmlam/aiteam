```markdown
# AITeam - AI-Powered Software Development Team Automation

> **Multi-agent orchestration system that simulates a complete software development team using AI agents**

Transform your development workflow with an automated team of specialized AI agents that handle requirements analysis, architecture design, development, testing, and code review - powered by Claude Sonnet 4, GitHub Models, or local LLMs.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Claude Sonnet 4](https://img.shields.io/badge/Claude-Sonnet%204-orange.svg)](https://www.anthropic.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Overview

AITeam orchestrates specialized AI agents through a complete Software Development Lifecycle (SDLC), from JIRA ticket to production-ready code. Each agent has a defined role (Business Analyst, Architect, Tech Lead, Developer, QA) and collaborates through a shared workflow to deliver comprehensive, documented implementations.

### Key Highlights

- **🤖 6 Specialized AI Agents**: BA, Architect, Tech Lead, Developer, Senior Dev, QA
- **🔄 Complete SDLC Automation**: Requirements → Architecture → Implementation → Testing → Review
- **🎯 JIRA Integration**: Fetch and process initiatives, epics, and user stories
- **🧠 Multi-LLM Support**: Claude Sonnet 4, GitHub Models (GPT-4o), or Ollama (local)
- **📊 Comprehensive Documentation**: Auto-generates architecture docs, technical specs, BDD scenarios
- **🧪 TDD/BDD Approach**: Pytest unit tests + Cucumber/Gherkin feature files
- **👥 Team Collaboration**: Standups, sprint planning, retrospectives via Team Coordinator

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- One of: Anthropic API key, GitHub Copilot subscription, or Ollama installed
- Optional: JIRA account for ticket integration

### Installation

```bash
# Clone the repository
git clone https://github.com/joeycmlam/aiteam.git
cd aiteam

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create a .env file with your LLM provider credentials:

```bash
# Choose ONE provider
LLM_PROVIDER=anthropic  # Options: anthropic, github_copilot_cli, ollama

# Anthropic Claude (Recommended for quality)
ANTHROPIC_API_KEY=sk-ant-api03-xxx
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# GitHub Models (Requires GitHub Copilot)
GITHUB_TOKEN=ghp_xxx
GITHUB_MODEL=gpt-4o

# Ollama (Local/Free)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# JIRA Integration (Optional)
JIRA_SERVER=https://yourcompany.atlassian.net
JIRA_USER=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token
```

### Running the System

```bash
# Option 1: Automated startup (includes Ollama server)
./start.sh

# Option 2: Manual execution
python workflows/initiative_pipeline.py

# Option 3: With JIRA ticket
python workflows/initiative_pipeline.py --jira PROJ-123
```

### Quick Test

```bash
# Test Claude integration
python tests/test_claude.py

# Test LLM manager
python tests/test_llm.py

# Run BA agent
python agents/ba_agent.py --input requirements.md
```

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Lead Orchestrator                        │
│              (Workflow Coordination & State)                 │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  BA Agent    │  │   Architect  │  │  Tech Lead   │
│ Requirements │  │   Design     │  │  Structure   │
└──────────────┘  └──────────────┘  └──────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                 ┌──────────────────┐
                 │  Developer Agent │
                 │  Implementation  │
                 └──────────────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
         ┌──────────────┐    ┌──────────────┐
         │  QA Agent    │    │  Tech Lead   │
         │  Testing     │    │ Code Review  │
         └──────────────┘    └──────────────┘
```

### Agent Roles & Outputs

| Agent | Responsibility | Key Features | Outputs |
|-------|---------------|--------------|---------|
| **Business Analyst** | Requirements analysis, user story creation | JIRA integration, BDD scenario generation, acceptance criteria | `requirements_analysis.md`, `requirements.feature`, `requirements_structured.json` |
| **Architect** | System design, pattern recommendations | Architecture design, tech stack selection, risk analysis | `system_architecture.md`, `architecture_structured.json` |
| **Tech Lead** | Technical structure, code review | Detailed specs, task breakdown, quality review | `technical_structure.md`, `technical_structure.json` |
| **Developer** | Feature implementation, unit testing | TDD approach, type hints, security best practices | `implementation.py`, `test_implementation.py` |
| **QA Agent** | Test scenario creation, BDD | Comprehensive test coverage, Gherkin scenarios | Cucumber `.feature` files |
| **Team Coordinator** | Scrum Master, team facilitation | Standups, sprint planning, retrospectives | Sprint metrics, team dashboard |

---

## 🎯 Workflow Execution

### Full Pipeline Mode

```bash
# Complete SDLC workflow
python workflows/initiative_pipeline.py --jira PROJ-123

# With custom output directory
python workflows/initiative_pipeline.py --jira PROJ-123 --output-dir custom_output
```

**Execution Flow:**
1. **JIRA Fetch** → Retrieve initiative/epic with linked issues
2. **BA Analysis** → Extract requirements, create user stories with acceptance criteria
3. **Architecture Design** → System design, patterns, tech stack recommendations
4. **Technical Structure** → Detailed specs, project structure, implementation checklist
5. **Development** → Code generation with tests (TDD approach)
6. **QA** → BDD scenarios, comprehensive test coverage analysis
7. **Code Review** → Quality, security, architecture alignment verification

### Step-by-Step Execution

```python
from agents.lead_orchestrator import LeadOrchestrator

orchestrator = LeadOrchestrator()

# Run specific steps with pause between
orchestrator.execute_workflow(
    jira_ticket_id="PROJ-123",
    steps=["ba", "architect", "tech_lead"],  # Only these steps
    pause_between_steps=True                  # Manual review between steps
)

# Available steps: ba, architect, tech_lead, developer, senior_dev, qa
```

### Individual Agent Usage

```python
# BA Agent - Analyze requirements from JIRA
from agents.ba_agent import BusinessAnalystAgent

ba = BusinessAnalystAgent()
analysis = ba.analyze_jira_initiative("PROJ-123")

# Or analyze from file
analysis = ba.analyze_requirements_file("requirements/user_01.md")

# Architect Agent - Design system architecture
from agents.architect_agent import ArchitectAgent

architect = ArchitectAgent()
architecture = architect.design_system(ba_analysis=analysis)

# Tech Lead Agent - Create technical structure
from agents.tech_lead_agent import TechLeadAgent

tech_lead = TechLeadAgent()
structure = tech_lead.design_technical_structure(
    architecture=architecture,
    ba_analysis=analysis
)

# Developer Agent - Generate implementation
from agents.developer_agent import DeveloperAgent

dev = DeveloperAgent()
code = dev.generate_implementation(
    requirements=analysis,
    architecture=architecture,
    tech_structure=structure
)

# QA Agent - Create BDD scenarios
from agents.qa_agent import QAAgent

qa = QAAgent()
scenarios = qa.create_bdd_scenarios(user_stories=analysis['user_stories'])

# Code Review
review = tech_lead.review_code("generated_code/implementation.py")
```

---

## 🧠 LLM Provider Support

### Provider Comparison

| Provider | Cost | Quality | Privacy | Speed | Best For |
|----------|------|---------|---------|-------|----------|
| **Claude Sonnet 4** | $$$ | ⭐⭐⭐⭐⭐ | Cloud | Fast ⚡ | Production, complex reasoning, architecture |
| **Claude 3.5 Sonnet** | $$ | ⭐⭐⭐⭐⭐ | Cloud | Very Fast ⚡⚡ | Balanced performance |
| **Claude Haiku** | $ | ⭐⭐⭐⭐ | Cloud | Fastest ⚡⚡⚡ | Simple tasks, high volume, cost optimization |
| **GPT-4o** | $$ | ⭐⭐⭐⭐⭐ | Cloud | Fast ⚡ | Code generation, GitHub workflows |
| **GPT-4o-mini** | $ | ⭐⭐⭐⭐ | Cloud | Very Fast ⚡⚡ | Faster responses, simpler tasks |
| **Ollama (llama3.2)** | Free | ⭐⭐⭐ | Local | Medium | Development, testing, sensitive data |
| **Ollama (qwen2.5)** | Free | ⭐⭐⭐ | Local | Medium | Code and reasoning |

### Available Models

#### Anthropic Claude

```bash
# Claude Sonnet 4 (Latest, Best)
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Claude 3.5 Sonnet (Fast, Excellent)
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Claude Opus (Powerful)
ANTHROPIC_MODEL=claude-3-opus-20240229

# Claude Haiku (Fast, Cost-effective)
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

#### GitHub Models

```bash
# GPT-4o (Best for code)
GITHUB_MODEL=gpt-4o

# GPT-4o-mini (Faster)
GITHUB_MODEL=gpt-4o-mini

# Mistral Large
GITHUB_MODEL=mistral-large
```

#### Ollama (Local)

```bash
# General purpose
OLLAMA_MODEL=llama3.2

# Code specialist
OLLAMA_MODEL=qwen2.5

# Balanced
OLLAMA_MODEL=mistral

# Small & fast
OLLAMA_MODEL=phi3
```

### Provider Switching

```bash
# Switch to Claude Sonnet 4 for complex analysis
export LLM_PROVIDER=anthropic
export ANTHROPIC_MODEL=claude-sonnet-4-20250514
python agents/architect_agent.py

# Switch to Claude Haiku for simple tasks (faster, cheaper)
export ANTHROPIC_MODEL=claude-3-haiku-20240307
python agents/ba_agent.py

# Switch to GitHub Models for code generation
export LLM_PROVIDER=github_copilot_cli
export GITHUB_MODEL=gpt-4o
python agents/developer_agent.py

# Switch to local Ollama for development
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.2
python agents/ba_agent.py
```

### Dynamic Model Selection in Code

```python
from shared.llm_manager import LLMManager

# Initialize with provider from environment
llm = LLMManager()

# Override model per request for cost optimization
quick_response = llm.generate(
    prompt="Summarize this code...",
    model="claude-3-haiku-20240307"  # Fast & cheap
)

# Use best model for complex analysis
architecture = llm.generate(
    prompt="Design a microservices architecture for...",
    model="claude-sonnet-4-20250514"  # Best quality
)

# Code analysis with specialized model
code_review = llm.analyze_code(
    code=source_code,
    questions=["Is this secure?", "Any performance issues?"],
    model="gpt-4o"  # Best for code
)
```

### Automatic Fallback Strategy

The system automatically falls back to Ollama if cloud providers fail:

```python
# LLMManager handles fallback automatically
llm = LLMManager(provider="anthropic")  # Primary: Claude

# If API fails → automatically tries Ollama
response = llm.generate(prompt="...")
# No code changes needed!
```

---

## 👥 Team Collaboration Features

### Team Coordinator Agent

Acts as a Scrum Master, facilitating team rituals and tracking progress:

```python
from agents.team_coordinator import TeamCoordinator

coordinator = TeamCoordinator()

# Daily Standup
standup = coordinator.daily_standup()
print(standup)  # Shows: completed, in-progress, blockers per agent

# Sprint Planning
plan = coordinator.sprint_planning(user_stories=[...])
print(plan)  # Shows: story points, task assignments

# Team Discussion
discussion = coordinator.facilitate_discussion(
    topic="API design approach",
    participants=["architect", "tech_lead", "developer"]
)

# Retrospective
retro = coordinator.retrospective()
print(retro)  # Shows: what went well, issues, action items

# Team Dashboard
dashboard = coordinator.get_team_dashboard()
print(dashboard)  # Shows: sprint status, blockers, decisions, metrics
```

### Team Structure

The coordinator manages 5 specialized agents:

- **BA Agent**: Requirements analysis, user stories
- **Architect Agent**: System design, patterns
- **Tech Lead Agent**: Technical leadership, code review
- **Developer Agent**: Implementation, unit testing
- **QA Agent**: Test design, BDD scenarios

---

## 📊 Output & Documentation

### Generated Artifacts

All outputs are saved in structured formats (Markdown + JSON):

```
output/
├── requirements_analysis.md          # BA: User stories, acceptance criteria
├── requirements.feature               # BA: BDD scenarios in Gherkin
├── requirements_structured.json       # BA: Structured requirements data
├── system_architecture.md            # Architect: System design document
├── architecture_structured.json       # Architect: Architecture data
├── technical_structure.md            # Tech Lead: Technical specifications
├── technical_structure.json          # Tech Lead: Implementation details
├── database_migrations.json          # DBA: Database schema changes
├── Dockerfile                        # DevOps: Container configuration
└── features/                         # QA: Cucumber test scenarios
    ├── login.feature
    └── checkout.feature

generated_code/
├── implementation.py                 # Developer: Production code
└── test_implementation.py            # Developer: Unit tests (pytest)
```

### Documentation Content

#### Requirements Analysis (BA)
- User stories with acceptance criteria (Given-When-Then format)
- Functional and non-functional requirements
- Assumptions and constraints
- BDD scenarios for testing
- Structured JSON for automation

#### System Architecture (Architect)
- System overview and architecture style
- Component diagram and responsibilities
- Technology stack recommendations
- Data model (entities, relationships)
- API design specifications
- Design patterns to apply
- Project structure
- Implementation phases
- Risk analysis and mitigation strategies

#### Technical Structure (Tech Lead)
- Complete project structure (directories, files)
- Module design with responsibilities
- Class diagrams and relationships
- Database schema (tables, columns, relationships)
- API specifications (endpoints, payloads)
- Configuration files needed
- Implementation checklist
- Code templates and examples
- Testing strategy
- DevOps setup instructions

#### Implementation (Developer)
- Type-hinted production code
- Error handling and validation
- Security considerations
- PEP 8 compliant (Python)
- Comprehensive pytest unit tests
- 80%+ code coverage
- Edge case handling

#### Test Scenarios (QA)
- Cucumber/Gherkin feature files
- Happy path scenarios
- Error handling scenarios
- Edge case coverage
- Background setup when applicable
- Clear, business-readable language

---

## 🔧 Configuration

### Main Configuration (agent_config.yaml)

```yaml
llm:
  provider: "anthropic"  # Options: anthropic, github_copilot_cli, ollama
  model: "claude-sonnet-4-20250514"
  temperature: 0.3
  max_tokens: 4096

jira:
  server: "https://yourcompany.atlassian.net"
  user: "email@company.com"
  use_mock_data: false  # Use mock data when JIRA unavailable

workflow:
  stages:
    - architecture
    - requirements
    - testing
    - development
    - review
  parallel_processing: false
  max_retries: 3
  retry_delay: 5  # seconds
  use_copilot_for_review: true
  generate_copilot_prompts: true

agents:
  ba:
    config_file: "config/agents/ba.yaml"
    prompts_file: "config/prompts/ba_agent_prompts.yaml"
  architect:
    config_file: "config/agents/architect.yaml"
    prompts_file: "config/prompts/architect_agent_prompts.yaml"
  tech_lead:
    config_file: "config/agents/tech_lead.yaml"
    prompts_file: "config/prompts/tech_lead_agent_prompts.yaml"
  developer:
    config_file: "config/agents/developer_pool_config.yaml"
  devops:
    config_file: "config/agents/devops_config.yaml"
  dba:
    config_file: "config/agents/dba_config.yaml"
```

### Agent-Specific Configuration

#### BA Agent (ba.yaml)
```yaml
name: "Business Analyst"
role: "Requirements Analysis"
capabilities:
  - jira_integration
  - requirements_extraction
  - user_story_creation
  - acceptance_criteria
  - bdd_scenario_generation
output_formats:
  - markdown
  - json
  - gherkin
```

#### Architect Agent (architect.yaml)
```yaml
name: "System Architect"
role: "Architecture Design"
specialization: "Financial Services, Azure Cloud, Microservices"
capabilities:
  - system_design
  - pattern_recommendation
  - tech_stack_selection
  - risk_analysis
output_formats:
  - markdown
  - json
```

### Custom Prompts (prompts)

Customize agent behavior by editing YAML prompt files:

```yaml
# config/prompts/ba_agent_prompts.yaml
system_message: |
  You are an expert Business Analyst with 15+ years of experience in enterprise software development.
  You excel at extracting clear, actionable requirements and creating detailed user stories.

analyze_jira_prompt: |
  Analyze the following JIRA initiative and extract:
  1. Functional requirements
  2. User stories with acceptance criteria (Given-When-Then)
  3. Technical constraints and assumptions
  4. BDD scenarios for testing
  
  JIRA Data:
  {jira_data}

create_user_story_prompt: |
  Create a user story from the following requirement:
  {requirement}
  
  Include:
  - User story (As a... I want... So that...)
  - Acceptance criteria (Given-When-Then)
  - Technical notes
  - Estimated complexity
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=agents --cov=shared --cov-report=html

# Run specific test file
pytest tests/test_llm.py -v

# Run specific test
pytest tests/test_claude.py::test_claude_generate -v

# Run BDD tests
pytest tests/features/ --gherkin-terminal-reporter

# View coverage report
open htmlcov/index.html
```

### Test Structure

```
tests/
├── __init__.py
├── test_llm.py                    # LLM Manager integration tests
├── test_claude.py                 # Claude-specific tests
├── fixtures/                      # Test data and fixtures
│   └── legacy_code.py
└── features/                      # BDD tests (Cucumber)
    ├── requirements.feature
    ├── architecture.feature
    └── steps/
        └── test_steps.py          # Step definitions
```

### Writing Tests

```python
# Unit test example
import pytest
from agents.ba_agent import BusinessAnalystAgent

def test_ba_analyze_requirements():
    ba = BusinessAnalystAgent()
    result = ba.analyze_requirements_file("tests/fixtures/sample_requirements.md")
    
    assert "user_stories" in result
    assert len(result["user_stories"]) > 0
    assert "acceptance_criteria" in result["user_stories"][0]

# BDD test example (Gherkin)
# tests/features/ba_analysis.feature
Feature: Business Analyst Requirements Analysis
  
  Scenario: Analyze requirements from markdown file
    Given a requirements file "sample_requirements.md"
    When the BA agent analyzes the requirements
    Then user stories should be generated
    And each story should have acceptance criteria
    And BDD scenarios should be created
```

---

## 🔌 VS Code Integration

AITeam integrates seamlessly with VS Code and GitHub Copilot:

### Create VS Code Agent Definitions

```python
from shared.agent_framework import VSCodeAgentIntegration

# Create VS Code agent definitions for all agents
vscode = VSCodeAgentIntegration()

# BA Agent
ba_config = {
    "name": "Business Analyst",
    "description": "Analyzes requirements and creates user stories",
    "instructions": "..."
}
vscode.create_agent_definition("ba_agent", ba_config)

# Architect Agent
architect_config = {
    "name": "System Architect",
    "description": "Designs system architecture",
    "instructions": "..."
}
vscode.create_agent_definition("architect_agent", architect_config)
```

### Use in VS Code

Generated files in agents:
- `ba_agent.agent.md`
- `architect_agent.agent.md`
- `tech_lead_agent.agent.md`

Use in VS Code chat:
```
@ba_agent Analyze these requirements and create user stories

@architect_agent Design a microservices architecture for this system

@tech_lead_agent Review this implementation for security issues
```

---

## 📦 Dependencies

### Core Dependencies

```python
# LLM Providers
anthropic==0.39.0              # Claude integration
ollama==0.3.3                  # Local LLMs
langchain==0.3.3               # LLM framework
langchain-community==0.3.2     # Community integrations

# GitHub Integration
PyGithub==2.4.0                # GitHub API
requests==2.32.3               # HTTP requests

# JIRA Integration
jira==3.8.0                    # JIRA API

# Testing
pytest==8.3.3                  # Test framework
pytest-bdd==7.3.0              # BDD testing
gherkin-official==4.1.3        # Gherkin parser

# Code Analysis
radon==6.0.1                   # Code metrics
lizard==1.17.10                # Code complexity

# Utilities
pyyaml==6.0.3                  # YAML parsing
python-dotenv==1.0.1           # Environment variables
pydantic==2.9.2                # Data validation
flask==3.0.3                   # Web framework (for API endpoints)
```

See requirements.txt for complete list with exact versions.

### Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Install for development (includes linters, formatters)
pip install -r requirements-dev.txt

# Install specific provider
pip install anthropic  # Claude only
pip install ollama     # Ollama only
```

---

## 🎓 Use Cases

### 1. Legacy Code Migration

Analyze legacy system and design modern architecture:

```bash
# Full migration workflow
python workflows/initiative_pipeline.py --jira MIGRATION-001

# Step by step
python agents/ba_agent.py --input legacy_requirements.md
python agents/architect_agent.py --input output/requirements_analysis.md
python agents/developer_agent.py --architecture output/system_architecture.md
```

### 2. New Feature Development

Complete SDLC for new feature from JIRA story:

```bash
# Automated workflow
python workflows/initiative_pipeline.py --jira FEATURE-123 --output-dir feature_output

# Manual steps
python agents/ba_agent.py --jira FEATURE-123
python agents/architect_agent.py
python agents/tech_lead_agent.py
python agents/developer_agent.py
python agents/qa_agent.py
```

### 3. Requirements Analysis Only

Extract and structure requirements from various sources:

```python
from agents.ba_agent import BusinessAnalystAgent

ba = BusinessAnalystAgent()

# From JIRA
analysis = ba.analyze_jira_initiative("PROJ-123")

# From file
analysis = ba.analyze_requirements_file("requirements/user_01.md")

# From text
analysis = ba.analyze_requirements_text("""
As a user, I want to login with email and password
so that I can access my account securely.
""")
```

### 4. Architecture Review

Review and improve existing architecture:

```python
from agents.architect_agent import ArchitectAgent

architect = ArchitectAgent()

# Analyze codebase
analysis = architect.analyze_codebase("path/to/project")

# Get recommendations
recommendations = architect.recommend_patterns(analysis)

# Generate documentation
architect.document_architecture(recommendations)
```

### 5. Code Review Automation

Automated code quality and security review:

```python
from agents.tech_lead_agent import TechLeadAgent

tech_lead = TechLeadAgent()

# Review implementation
review = tech_lead.review_code("generated_code/implementation.py")

print(review["quality_score"])
print(review["security_issues"])
print(review["recommendations"])
```

### 6. Test Generation

Generate comprehensive test suites:

```python
from agents.qa_agent import QAAgent

qa = QAAgent()

# Generate BDD scenarios
scenarios = qa.create_bdd_scenarios(user_stories)

# Generate unit tests
unit_tests = qa.generate_unit_tests(implementation_code)

# Both saved to output directory
```

---

## 🛠️ Advanced Usage

### Custom Workflow Handlers

Create custom workflow steps:

```python
from agents.lead_orchestrator import LeadOrchestrator

orchestrator = LeadOrchestrator()

# Define custom handler
def security_audit_handler(context):
    """Custom security audit step"""
    code = context.get("implementation")
    
    # Run security checks
    vulnerabilities = scan_for_vulnerabilities(code)
    
    # Add to context
    context["security_audit"] = vulnerabilities
    return context

# Register handler
orchestrator.register_handler("security_audit", security_audit_handler)

# Execute workflow with custom step
orchestrator.execute_workflow(
    steps=["ba", "architect", "developer", "security_audit", "qa"]
)
```

### Parallel Agent Execution

Speed up workflow with parallel processing:

```yaml
# config/agent_config.yaml
workflow:
  parallel_processing: true
  parallel_agents:
    - ["ba", "dba"]           # Run BA and DBA in parallel
    - ["developer", "devops"]  # Then Developer and DevOps in parallel
```

```python
# Or programmatically
orchestrator.execute_workflow(
    steps=["ba", "architect", "tech_lead"],
    parallel_processing=True
)
```

### Error Handling & Retries

Configure automatic retries and fallbacks:

```yaml
workflow:
  max_retries: 3
  retry_delay: 5  # seconds
  retry_backoff: 2  # exponential backoff multiplier
  fallback_model: "ollama:llama3.2"
  continue_on_error: false
```

```python
# Or in code
orchestrator.execute_workflow(
    steps=["ba", "architect"],
    max_retries=3,
    fallback_model="ollama:llama3.2"
)
```

### Custom Memory Store

Implement custom persistence:

```python
from shared.memory_store import MemoryStore

class RedisMemoryStore(MemoryStore):
    """Redis-backed memory store"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def set(self, key, value):
        self.redis.set(key, json.dumps(value))
    
    def get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value else None

# Use custom store
orchestrator = LeadOrchestrator(memory_store=RedisMemoryStore(redis_client))
```

---

## 🐛 Troubleshooting

### LLM Connection Issues

```bash
# Test Anthropic connection
python -c "from shared.llm_manager import LLMManager; llm = LLMManager(provider='anthropic'); print(llm.generate('Hello'))"

# Test GitHub Models
export LLM_PROVIDER=github_copilot_cli
python tests/test_llm.py

# Test Ollama (ensure server running)
ollama serve  # In separate terminal
ollama list   # Check available models
ollama pull llama3.2  # Pull model if missing
```

### Common Errors

#### API Key Issues
```bash
# Check environment variables
echo $ANTHROPIC_API_KEY
echo $GITHUB_TOKEN

# Verify .env file is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

#### Model Not Found
```bash
# Ollama: Pull the model
ollama pull llama3.2
ollama list

# Anthropic: Check model name
# Valid: claude-sonnet-4-20250514, claude-3-5-sonnet-20241022, etc.
```

#### JIRA Connection
```bash
# Test JIRA connection
python -c "from agents.jira_agent import JIRAAgent; j = JIRAAgent(); print(j.get_initiative('PROJ-123'))"

# Use mock data if JIRA unavailable
export USE_MOCK_JIRA=true
# or in config/agent_config.yaml:
# jira:
#   use_mock_data: true
```

#### Permission Errors
```bash
# Check file permissions
chmod +x start.sh

# Check output directory permissions
mkdir -p output generated_code
chmod 755 output generated_code
```

### Debugging

Enable debug logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run agent with debug output
ba = BusinessAnalystAgent()
ba.analyze_requirements_file("requirements.md")
```

Or via environment variable:

```bash
export LOG_LEVEL=DEBUG
python agents/ba_agent.py
```

---

## 📚 Documentation

### Available Documentation

- 📖 **[Claude Integration Guide](doc/CLAUDE_INTEGRATION.md)** - Complete Claude setup and usage
- 🚀 **[Claude Quick Start](CLAUDE_QUICKSTART.md)** - Get started with Claude in 3 minutes
- 📝 **[Implementation Summary](CLAUDE_IMPLEMENTATION_SUMMARY.md)** - What changed in Claude integration
- 🏗 **[Project Architecture](doc/PROJECT_ARCHITECTURE.md)** - System design and architecture
- 🤖 **[Agent Framework Guide](doc/AGENT_FRAMEWORK_GUIDE.md)** - Agent development guide
- 🔧 **[GenAI Agent Options](doc/GENAI_AGENT_OPTIONS.md)** - LLM provider comparison

### Agent-Specific Documentation

- **BA Agent**: See ba.yaml and ba_agent_prompts.yaml
- **Architect Agent**: See architect.yaml and architect_agent_prompts.yaml
- **Tech Lead Agent**: See `config/agents/tech_lead.yaml` and tech_lead_agent_prompts.yaml

### Configuration Reference

- **Main Config**: agent_config.yaml - System-wide settings
- **Agent Configs**: agents - Individual agent configurations
- **Prompts**: prompts - Customizable agent prompts

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/aiteam.git
cd aiteam

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linters
black agents/ shared/
flake8 agents/ shared/
mypy agents/ shared/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for function signatures
- Write docstrings for classes and functions
- Keep functions focused and single-purpose
- Add unit tests for new features
- Update documentation as needed

### Pull Request Guidelines

- Provide clear description of changes
- Reference related issues
- Include test coverage
- Update README if adding features
- Ensure CI passes

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude API and excellent LLM capabilities
- **GitHub** for Models API and Copilot integration
- **Ollama** for local LLM support and privacy-focused inference
- **LangChain** for LLM framework and abstractions
- **JIRA** for project management integration
- **Python Community** for excellent libraries and tools

---

## 📞 Support

### Getting Help

- **📖 Documentation**: Check the `doc/` directory for detailed guides
- **🐛 Issues**: [GitHub Issues](https://github.com/joeycmlam/aiteam/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/joeycmlam/aiteam/discussions)
- **📧 Email**: your-email@example.com

### Reporting Bugs

Please include:
1. Python version
2. LLM provider and model
3. Error message and stack trace
4. Steps to reproduce
5. Expected vs actual behavior

### Feature Requests

Open an issue with:
1. Clear description of the feature
2. Use case and benefits
3. Proposed implementation (optional)
4. Any related issues or PRs

---

## 🗺️ Roadmap

### Current Version (2.0)
- ✅ Multi-LLM support (Claude, GitHub Models, Ollama)
- ✅ 6 specialized AI agents
- ✅ Complete SDLC workflow
- ✅ JIRA integration
- ✅ BDD/TDD support
- ✅ Team collaboration features

### Upcoming Features
- 🔜 Database migration agent
- 🔜 DevOps automation agent
- 🔜 API documentation generator
- 🔜 Performance testing agent
- 🔜 Security scanning integration
- 🔜 CI/CD pipeline templates
- 🔜 Multi-language support (TypeScript, Java, Go)
- 🔜 Web UI for workflow visualization
- 🔜 Slack integration for notifications
- 🔜 GitLab support

---

## 📊 Project Status

**Status**: ✅ Production Ready  
**Version**: 2.0.0  
**Last Updated**: November 22, 2025  
**Python**: 3.10+  
**Stability**: Stable  

---
