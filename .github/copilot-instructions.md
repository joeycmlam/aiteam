# AI Team - Copilot Instructions

## Project Overview
Multi-agent AI system for legacy code migration with 6 specialized agents (Lead Orchestrator, Architect, BA, QA, Senior Dev, Developer) that analyze JIRA requirements, assess legacy code, and generate modernized implementations with tests.

**🎯 Dual Agent Strategy for Claude Access with GitHub Copilot License:**

### 1. VS Code Chat Agents (Interactive Claude Sonnet 4)
- Defined in `.vscode/agents/*.agent.md` - 4 specialized agents using Claude Sonnet 4
- **@lead** - Tech Lead for code reviews and team coordination
- **@architect** - Solution Architect for system design and patterns
- **@ba** - Business Analyst for requirements and user stories  
- **@developer** - Senior Developer for TDD implementation
- Invoke in VS Code Chat: `@architect Design API gateway pattern`
- **This is your primary Claude access method with Copilot license**

### 2. Python Automation Agents (Programmatic with GPT-4o/Ollama)
- Located in `agents/*.py` - 6 Python agents using LLMManager
- Use GitHub Models API (GPT-4o, Mistral) or Ollama (local models)
- Automated workflows via `workflows/initiative_pipeline.py`
- **Note**: Claude NOT available via GitHub Models API - use GPT-4o instead

## Architecture Essentials

### Agent Orchestration Pattern
- **LeadOrchestrator** (`agents/lead_orchestrator.py`) coordinates all agents using a flexible step-based workflow
- Register step handlers with `register_step_handler(step_key, handler_function)` 
- Create workflows with `create_workflow(steps=['ba', 'architect', ...])` - steps are optional, defaults to all 5
- Execute with `execute_workflow(workflow, pause_between_steps=False)`
- Context passed between steps automatically (e.g., `ba_result` → architect step)

### LLM Provider Abstraction
- **LLMManager** (`shared/llm_manager.py`) provides unified interface to multiple LLM providers
- Supports Ollama (local), GitHub Models API (cloud)
- Model override per-request: `llm.generate(prompt, model='gpt-4o')` or `llm.generate(prompt, model='llama3.2')`
- Automatic fallback: GitHub API → Ollama if connection fails
- **For Claude**: Use VS Code Chat Agents (@architect, @lead, etc.) instead of programmatic API

### Shared Memory Pattern
- **SharedMemory** (`shared/memory_store.py`) persists state as JSON at `./memory.json` (or custom path)
- All agents access same memory instance: `memory.store('key', value)` and `memory.get('key')`
- Automatically timestamps and type-tags all stored data

### YAML-based Prompt Configuration
- Agents load prompts from `config/prompts/{agent}_prompts.yaml` at initialization
- Supports template substitution: `{total_files}`, `{languages}`, etc.
- Falls back to inline defaults if YAML missing - no hard dependency
- See `architect_agent_prompts.yaml` for structure: `template`, `system_message`, `fallbacks`

## Critical Workflows

### VS Code Chat Agents (Interactive Claude Access)
```
# In VS Code Chat panel (Ctrl+Cmd+I or Cmd+I):
@lead Review this PR for security and coding standards
@architect Design microservices architecture for this feature
@ba Analyze JIRA epic SCRUM-5 and create user stories
@developer Implement authentication with TDD approach
```

### Environment Setup
```bash
# Required before running anything
source venv/bin/activate  # or use ${workspaceFolder}/venv/bin/python in tasks

# For GitHub Models API access (GPT-4o, Mistral)
# Add to .env: GITHUB_TOKEN=ghp_xxxxx (from https://github.com/settings/tokens)
```

### Running Pipelines
```bash
# Initiative pipeline (JIRA epic → code)
python3 workflows/initiative_pipeline.py SCRUM-5

# PPS workflow (requirements file → architecture)
cd ../pps && python3 ai_workflow_orchestrated.py requirements/user_requirement.md
```

### Testing
```bash
# All tests
pytest tests/ -v

# Specific test files
pytest tests/test_llm.py          # Test LLM connectivity
pytest tests/test_github_models.py # Test GitHub Models API (GPT-4o)
```

### VS Code Tasks (Ctrl+Shift+B)
- **Run Migration Pipeline** (default build): Starts Ollama + runs migration
- **Run Tests**: Execute pytest suite
- **Start Ollama Service**: Background service for local LLM

## Project Conventions

### Agent Implementation Pattern
Every agent follows this structure:
1. `__init__(llm_config, other_config)` - loads YAML prompts, initializes LLMManager
2. YAML prompts in `config/prompts/` with fallback to inline defaults
3. Public methods for agent's core responsibility (e.g., `analyze_codebase()`, `fetch_initiative()`)
4. Private `_load_prompts()` method with graceful fallback
5. Print statements use emoji prefixes (🏗️ Architect, 📋 BA, 🧪 QA, 💻 Dev, 👨‍💼 Senior Dev)

### File Output Conventions
- Tests → `tests/features/{ticket_id}.feature` (Gherkin/BDD format)
- Generated code → `generated_code/{ticket_id}/implementation.py`
- Analysis → `requirements/analysis/` or `architecture/` (project-dependent)
- Memory state → `memory.json` or `memory_initiative.json`

### Configuration Hierarchy
1. Environment variables (`.env`) - highest priority
2. YAML config (`config/agent_config.yaml`)
3. Inline defaults - fallback

Key .env variables:
- `LLM_PROVIDER` (ollama, github_copilot_cli)
- `GITHUB_TOKEN` (for GitHub Models API - GPT-4o, NOT Claude)
- `GITHUB_MODEL` (gpt-4o, gpt-4o-mini, mistral-large)
- `OLLAMA_MODEL` (llama3.2, qwen2.5, phi3)
- `JIRA_API_TOKEN`, `JIRA_SERVER`, `JIRA_USER`

### Error Handling Philosophy
- LLM failures → graceful fallback (e.g., stub code with TODO, template Gherkin)
- Missing config files → use inline defaults, log warning
- Connection errors → fallback provider (GitHub → Ollama)
- No exceptions for missing optional dependencies (JIRA token)

## Integration Points

### JIRA Integration (BAAgent)
- Fetches initiatives/epics with `fetch_initiative(issue_key)`
- Supports mock data when `JIRA_API_TOKEN` missing
- Returns structured dict: `{key, summary, description, type, status, priority, linked_issues: []}`

### PPS Project Workflow
- Separate repo at `/Users/joeylam/repo/pps`
- Uses `ai_workflow_orchestrated.py` with class-based PPSWorkflow
- Demonstrates BA → Architect integration with context passing
- Outputs to `requirements/analysis/` and `architecture/`

### GitHub Models API (Programmatic - GPT-4o Only)
- Endpoint: `https://models.inference.ai.azure.com/chat/completions`
- Requires GitHub Copilot subscription + GITHUB_TOKEN with `read:user` scope
- Rate limits: 15 req/min, 150K tokens/day
- **Available models**: gpt-4o, gpt-4o-mini, mistral-large, o1-preview
- **⚠️ Claude NOT available** - use VS Code Chat Agents (@architect, @lead) for Claude

### VS Code Chat Agents (Interactive - Claude Sonnet 4)
- Agent definitions in `.vscode/agents/*.agent.md`
- Use GitHub Copilot Chat interface with `@agent-name` syntax
- Available agents: lead, architect, ba, developer
- **This is your Claude access method** - leverages Copilot's chat feature
- Example agent definition format:
```yaml
---
name: Solution Architect
model: Claude Sonnet 4
tools: ['read', 'search', 'fetch', 'usages']
---
```

## Key Files Reference
- `doc/README_START_HERE.md` - Quick start, project structure
- `doc/PROJECT_ARCHITECTURE.md` - System diagrams (Mermaid)
- `doc/FLEXIBLE_WORKFLOW_GUIDE.md` - LeadOrchestrator usage patterns
- `doc/GITHUB_MODELS_SETUP.md` - GitHub Models API setup (GPT-4o)
- `config/agent_config.yaml` - Global config (LLM, JIRA, workflow stages)
- `.vscode/tasks.json` - Build/test/run tasks
- `.vscode/agents/*.agent.md` - VS Code Chat Agent definitions (Claude Sonnet 4)

## Technology Stack
- Primary languages: Python 3.12+, TypeScript/Node.js
- Testing frameworks: pytest, Jest, Cucumber
- API testing: Postman
- Project tracking: JIRA
- Cloud platform: Azure (AKS, API Management, ADX)
- LLM: Claude Sonnet 4 (via VS Code Chat), GPT-4o (via GitHub Models API), Ollama (local)

## Coding Standards
- All code must include comprehensive tests (TDD approach)
- Minimum 80% code coverage required
- Use type hints (Python) and strict TypeScript
- Follow BDD with Cucumber for acceptance tests
- All API endpoints must have Postman test collections

## Recommended Workflow for Claude Usage

### For Interactive Development (Claude Sonnet 4)
1. Open VS Code Chat panel (Ctrl+Cmd+I)
2. Use `@architect` for architectural decisions and design patterns
3. Use `@lead` for code reviews and team coordination
4. Use `@ba` for requirements analysis and user stories
5. Use `@developer` for TDD implementation guidance

### For Automated Pipelines (GPT-4o or Ollama)
1. Set `LLM_PROVIDER=github_copilot_cli` and `GITHUB_MODEL=gpt-4o` in .env
2. Run `python3 workflows/initiative_pipeline.py SCRUM-5`
3. For local/unlimited: Set `LLM_PROVIDER=ollama` and `OLLAMA_MODEL=llama3.2`

### Hybrid Strategy (Best of Both Worlds)
- **Architecture & Design**: Use `@architect` in VS Code Chat (Claude Sonnet 4)
- **Bulk Code Generation**: Use Python agents with GPT-4o or Ollama
- **Code Review**: Use `@lead` in VS Code Chat (Claude Sonnet 4)
- **Test Generation**: Use Python QAAgent with GPT-4o or Ollama

## Anti-Patterns to Avoid

### ❌ DON'T: Instantiate agents without LLMManager
```python
# Bad - direct Ollama call
import ollama
response = ollama.generate(model='llama3.2', prompt=text)
```
```python
# Good - use LLMManager abstraction
from shared.llm_manager import LLMManager
llm = LLMManager()
response = llm.generate(text, model='llama3.2')
```

### ❌ DON'T: Hardcode prompts in agent methods
```python
# Bad - inline prompt string
def analyze(self):
    prompt = "Analyze this code and recommend patterns..."
```
```python
# Good - load from YAML config with fallback
def analyze(self):
    template = self.prompts.get('analyze_codebase', {}).get('template', DEFAULT_TEMPLATE)
    prompt = template.format(total_files=files, languages=langs)
```

### ❌ DON'T: Call LLM libraries directly
```python
# Bad - bypasses fallback and model switching
import requests
response = requests.post("https://models.inference.ai.azure.com/...", ...)
```
```python
# Good - always use LLMManager for automatic fallback
response = self.llm.generate(prompt, model='gpt-4o')  # Falls back to Ollama if GitHub API fails
```

### ❌ DON'T: Assume JIRA credentials exist
```python
# Bad - crashes if JIRA_API_TOKEN missing
jira = JIRA(server=config['server'], basic_auth=(user, token))
```
```python
# Good - check and provide mock data fallback
if jira_config.get('token'):
    jira = JIRA(server=config['server'], basic_auth=(user, token))
else:
    print("⚠️ JIRA_API_TOKEN not found, using mock data")
    return self._load_mock_data()
```

### ❌ DON'T: Create workflows without proper handlers
```python
# Bad - no handlers registered
orchestrator = LeadOrchestrator(llm_config)
workflow = orchestrator.create_workflow(steps=['ba', 'architect'])
# Will fail - no ba_step_handler or architect_step_handler registered!
```
```python
# Good - register handlers before creating workflow
orchestrator = LeadOrchestrator(llm_config)
orchestrator.register_step_handler('ba', self._ba_handler)
orchestrator.register_step_handler('architect', self._architect_handler)
workflow = orchestrator.create_workflow(steps=['ba', 'architect'])
```

### ❌ DON'T: Try to use Claude via GitHub Models API
```python
# Bad - Claude NOT available in GitHub Models API
llm = LLMManager('github_copilot_cli')
response = llm.generate(prompt, model='claude-3.5-sonnet')  # Will fail!
```
```python
# Good - Use VS Code Chat Agents for Claude
# In VS Code Chat: @architect Design the authentication system
# OR use GPT-4o for programmatic access
llm = LLMManager('github_copilot_cli')
response = llm.generate(prompt, model='gpt-4o')  # Works!
```
