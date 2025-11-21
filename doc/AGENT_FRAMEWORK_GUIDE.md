# Agent Framework Development Guide

## Overview

This guide explains how to develop custom agents using VS Code, GitHub Copilot, and our agent framework for automated workflow orchestration.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   VS Code GitHub Copilot                    │
│                      (Interactive Chat)                     │
│                                                             │
│   @BA          @TechLead          @Developer               │
│   (Claude)     (Claude)           (Claude)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Complements
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               Python Agent Framework                        │
│                 (Automated Workflows)                       │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ BA Agent │───▶│TechLead  │───▶│Developer │            │
│  │ (GPT-4o) │    │ Agent    │    │ Agent    │            │
│  └──────────┘    │(GPT-4o)  │    │(GPT-4o)  │            │
│                  └──────────┘    └──────────┘            │
│                                                             │
│  ┌──────────────────────────────────────┐                 │
│  │       AgentChain Orchestrator        │                 │
│  │  (Context passing, execution log)    │                 │
│  └──────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Optional
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     JIRA Integration                        │
│              (Fetch issues, validate completeness)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Components Created

### 1. Agent Framework (`shared/agent_framework.py`)

**Base Classes:**

#### `Agent` (Abstract Base Class)
- Common functionality for all agents
- Context management
- File I/O operations
- Action logging
- History tracking

**Key Methods:**
```python
class Agent(ABC):
    def __init__(self, name, role, output_dir, config_path)
    def set_context(key, value)  # Store agent context
    def get_context(key, default)  # Retrieve context
    def save_output(filename, content, subdir)  # Save files
    def load_input(filepath)  # Load input files
    def log_action(action, details)  # Log actions
    @abstractmethod
    def process(input_data)  # Must implement
```

#### `AgentChain`
- Orchestrates multiple agents sequentially
- Passes context between agents
- Tracks execution time and status
- Generates execution logs

**Key Methods:**
```python
class AgentChain:
    def add_agent(agent)  # Add agent to chain
    def set_shared_context(key, value)  # Shared context
    def execute(initial_input)  # Run all agents
    def get_execution_log()  # Get execution details
```

#### `VSCodeAgentIntegration`
- Creates VS Code custom agent definitions
- Syncs Python and VS Code agent configs
- Utilities for VS Code integration

---

### 2. Enhanced Agents

#### **BA Agent** (`agents/enhanced_ba_agent.py`)
- Extends `Agent` base class
- Analyzes requirements
- Generates user stories
- Creates structured output

**Usage:**
```python
from agents.enhanced_ba_agent import EnhancedBAAgent

ba = EnhancedBAAgent(output_dir="requirements/analysis")
results = ba.process("requirements/user_requirement.md")

# Results include:
# - requirements_analysis.md
# - user_stories.feature
# - requirements_structured.json
```

**CLI:**
```bash
python agents/enhanced_ba_agent.py \
  --input requirements/user_requirement.md \
  --output-dir requirements/analysis
```

#### **Tech Lead Agent** (`agents/enhanced_tech_lead_agent.py`)
- Extends `Agent` base class
- Designs technical architecture
- Creates implementation plans
- Generates coding guidelines

**Usage:**
```python
from agents.enhanced_tech_lead_agent import EnhancedTechLeadAgent

tech_lead = EnhancedTechLeadAgent(output_dir="technical")
results = tech_lead.process({
    'architecture': 'architecture.md',
    'ba_analysis': 'requirements_analysis.md'
})

# Results include:
# - technical_structure.md
# - development_tasks.md
# - implementation_guidelines.md
# - technical_structure.json
```

**CLI:**
```bash
python agents/enhanced_tech_lead_agent.py \
  --ba-analysis requirements/analysis/requirements_analysis.md \
  --output-dir technical
```

#### **Developer Agent** (`agents/enhanced_developer_agent.py`)
- Extends `Agent` base class
- Generates production code
- Creates unit tests
- Writes documentation

**Usage:**
```python
from agents.enhanced_developer_agent import EnhancedDeveloperAgent

developer = EnhancedDeveloperAgent(output_dir="implementation")
results = developer.process({
    'technical_structure': 'technical/technical_structure.md',
    'tasks': 'technical/development_tasks.md'
})

# Results include:
# - src/portfolio_manager.py
# - src/transaction_handler.py
# - src/data_models.py
# - tests/test_*.py
# - docs/README.md
```

**CLI:**
```bash
python agents/enhanced_developer_agent.py \
  --technical-structure technical/technical_structure.md \
  --output-dir implementation
```

---

### 3. Complete Workflow Orchestrator

#### `workflows/complete_workflow.py`

Orchestrates the entire BA → Tech Lead → Developer workflow using `AgentChain`.

**Features:**
- Optional JIRA integration
- Sequential agent execution
- Context passing between agents
- Execution logging
- Comprehensive summary

**Usage:**

```bash
# From requirements file
python workflows/complete_workflow.py \
  --requirements requirements/user_requirement.md \
  --output workflow_output

# From JIRA issue
python workflows/complete_workflow.py \
  --jira PROJ-123 \
  --jira-url https://yourcompany.atlassian.net \
  --jira-email your@email.com \
  --jira-token YOUR_TOKEN \
  --output workflow_output
```

**Output Structure:**
```
workflow_output/
├── requirements/
│   └── analysis/
│       ├── requirements_analysis.md
│       ├── user_stories.feature
│       └── requirements_structured.json
├── technical/
│   ├── technical_structure.md
│   ├── development_tasks.md
│   ├── implementation_guidelines.md
│   └── technical_structure.json
├── implementation/
│   ├── src/
│   │   ├── portfolio_manager.py
│   │   ├── transaction_handler.py
│   │   └── data_models.py
│   ├── tests/
│   │   ├── test_portfolio_manager.py
│   │   ├── test_transaction_handler.py
│   │   └── test_data_models.py
│   └── docs/
│       └── README.md
└── execution_log.json
```

---

## VS Code Custom Agents

### Already Created

✅ `/Users/joeylam/repo/pps/.github/agents/BA.agent.md`  
✅ `/Users/joeylam/repo/pps/.github/agents/TechLead.agent.md`  
✅ `/Users/joeylam/repo/pps/.github/agents/Developer.agent.md`

### Usage in VS Code Chat

Open VS Code Chat (`Cmd+Shift+I`) and use:

```
@BA analyze #file:requirements/user_requirement.md

@TechLead design system based on the BA analysis above

@Developer implement authentication module following tech lead design
```

---

## Complete Workflow Examples

### Example 1: From Requirements File

```bash
# Step 1: Run complete workflow
cd /Users/joeylam/repo/aiteam
python workflows/complete_workflow.py \
  --requirements /Users/joeylam/repo/pps/requirements/user_01.md \
  --output /Users/joeylam/repo/pps/workflow_output

# Output:
# ✅ BA Agent completed
# ✅ Tech Lead Agent completed
# ✅ Developer Agent completed
# ⏱️  Total execution time: 45.23 seconds

# Step 2: Review outputs
cd /Users/joeylam/repo/pps/workflow_output
ls -R

# Step 3: Run tests
cd implementation
pytest tests/ -v
```

### Example 2: From JIRA Issue

```bash
# Set JIRA credentials
export JIRA_URL="https://yourcompany.atlassian.net"
export JIRA_EMAIL="your@email.com"
export JIRA_API_TOKEN="your_api_token"

# Run workflow
python workflows/complete_workflow.py \
  --jira PROJ-123 \
  --output workflow_output

# Automatically:
# 1. Fetches JIRA issue
# 2. Validates completeness
# 3. Runs BA → Tech Lead → Developer
# 4. Generates all artifacts
```

### Example 3: Hybrid Approach

```bash
# Step 1: Fetch from JIRA
python agents/jira_agent.py PROJ-123

# Step 2: Run automated workflow
python workflows/complete_workflow.py \
  --requirements requirements/PROJ_123_requirement.md \
  --output workflow_output

# Step 3: Review in VS Code Chat
# Open VS Code Chat (Cmd+Shift+I)
@BA review #file:workflow_output/requirements/analysis/requirements_analysis.md

@TechLead suggest improvements to #file:workflow_output/technical/technical_structure.md

@Developer review this code #file:workflow_output/implementation/src/portfolio_manager.py
```

---

## Creating Custom Agents

### Step 1: Extend Agent Base Class

```python
from shared.agent_framework import Agent
from shared.llm_manager import LLMManager

class MyCustomAgent(Agent):
    def __init__(self, output_dir="output"):
        super().__init__(
            name="MyAgent",
            role="My custom agent role",
            output_dir=output_dir
        )
        self.llm_manager = LLMManager()
    
    def process(self, input_data):
        """Implement your agent logic"""
        self.log_action("start_processing")
        
        # Load input
        if isinstance(input_data, str) and os.path.exists(input_data):
            content = self.load_input(input_data)
        else:
            content = str(input_data)
        
        # Process with LLM
        result = self.llm_manager.generate(
            prompt=f"Process this: {content}",
            temperature=0.7
        )
        
        # Save output
        output_file = self.save_output("output.md", result)
        
        self.log_action("completed")
        
        return {'output': result, 'file': output_file}
```

### Step 2: Add to Agent Chain

```python
from shared.agent_framework import AgentChain
from agents.my_custom_agent import MyCustomAgent

chain = AgentChain("My Workflow")
chain.add_agent(MyCustomAgent())
results = chain.execute("input.txt")
```

### Step 3: Create VS Code Agent

```python
from shared.agent_framework import VSCodeAgentIntegration

VSCodeAgentIntegration.create_agent_definition(
    name="MyAgent",
    description="My custom agent for X",
    role="Expert in Y",
    responsibilities=[
        "Does X",
        "Handles Y"
    ],
    use_cases=[
        "When you need X",
        "When working with Y"
    ],
    examples=[
        "@myagent do something #file:input.md"
    ],
    output_path=".github/agents/MyAgent.agent.md"
)
```

---

## Testing

### Test Individual Agents

```bash
# Test BA Agent
python agents/enhanced_ba_agent.py --input requirements/user_01.md

# Test Tech Lead Agent
python agents/enhanced_tech_lead_agent.py \
  --ba-analysis requirements/analysis/requirements_analysis.md

# Test Developer Agent
python agents/enhanced_developer_agent.py \
  --technical-structure technical/technical_structure.md
```

### Test Complete Workflow

```bash
# Run complete workflow
python workflows/complete_workflow.py \
  --requirements requirements/user_01.md \
  --output test_output

# Verify outputs
ls -R test_output/

# Run generated tests
cd test_output/implementation
pytest tests/ -v --cov=src
```

---

## Key Benefits

### Agent Framework Benefits
✅ **Reusable**: Base `Agent` class for all agents  
✅ **Standardized**: Consistent interface and behavior  
✅ **Observable**: Action logging and execution tracking  
✅ **Chainable**: Easy orchestration with `AgentChain`  
✅ **Testable**: Each agent can be tested independently  

### VS Code Integration Benefits
✅ **Interactive**: Chat-based exploration with Claude  
✅ **Complementary**: Works alongside Python automation  
✅ **Flexible**: Choose automation or interaction per task  
✅ **User-Friendly**: Natural language interface  

### Complete Workflow Benefits
✅ **End-to-End**: JIRA → Implementation in one command  
✅ **Automated**: No manual handoffs  
✅ **Traceable**: Full execution logs  
✅ **Production-Ready**: Generates actual code + tests  

---

## Next Steps

1. **Test the framework:**
   ```bash
   cd /Users/joeylam/repo/aiteam
   python workflows/complete_workflow.py \
     --requirements /Users/joeylam/repo/pps/requirements/user_01.md \
     --output /Users/joeylam/repo/pps/framework_test
   ```

2. **Try VS Code agents:**
   - Open VS Code Chat (`Cmd+Shift+I`)
   - Type: `@BA analyze #file:requirements/user_01.md`

3. **Create custom agents:**
   - Extend `Agent` base class
   - Implement `process()` method
   - Add to `AgentChain`

4. **Set up JIRA integration:**
   - Configure JIRA credentials
   - Test: `python agents/jira_agent.py YOUR-KEY`
   - Run workflow with `--jira` flag

---

## Files Created

✅ **Framework:**
- `/Users/joeylam/repo/aiteam/shared/agent_framework.py`

✅ **Agents:**
- `/Users/joeylam/repo/aiteam/agents/enhanced_ba_agent.py`
- `/Users/joeylam/repo/aiteam/agents/enhanced_tech_lead_agent.py`
- `/Users/joeylam/repo/aiteam/agents/enhanced_developer_agent.py`

✅ **Workflows:**
- `/Users/joeylam/repo/aiteam/workflows/complete_workflow.py`

✅ **VS Code Agents:**
- `/Users/joeylam/repo/pps/.github/agents/BA.agent.md`
- `/Users/joeylam/repo/pps/.github/agents/TechLead.agent.md`
- `/Users/joeylam/repo/pps/.github/agents/Developer.agent.md`

✅ **Documentation:**
- `/Users/joeylam/repo/aiteam/doc/AGENT_FRAMEWORK_GUIDE.md` (this file)

Ready to build your agent workflows! 🚀
