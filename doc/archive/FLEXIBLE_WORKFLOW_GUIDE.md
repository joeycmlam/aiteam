# Lead Orchestrator - Flexible Workflow Guide

## Overview

The refactored `LeadOrchestrator` now supports flexible workflow execution, allowing you to:
- Run the full end-to-end pipeline
- Execute single steps for review
- Run partial pipelines
- Pause between steps for validation

## Available Workflow Steps

| Step Key | Agent | Description |
|----------|-------|-------------|
| `ba` | BAAgent | Requirements gathering and analysis |
| `architect` | ArchitectAgent | Architecture design and pattern recommendations |
| `qa` | QAAgent | Test design and quality assurance |
| `developer` | DeveloperAgent | Code implementation |
| `senior_dev` | SeniorDevAgent | Code review and validation |

## Key Features

### 1. Flexible Step Selection

```python
# Single step
orchestrator.create_workflow(steps=['ba'])

# Partial pipeline
orchestrator.create_workflow(steps=['ba', 'architect'])

# Full pipeline
orchestrator.create_workflow(steps=['ba', 'architect', 'qa', 'developer', 'senior_dev'])

# Default (all steps)
orchestrator.create_workflow()
```

### 2. Step Handlers

Register custom handlers for each step:

```python
def my_ba_handler(context):
    # Your BA agent logic
    ba = BAAgent(llm_config, jira_config)
    result = ba.analyze_requirements(...)
    return {'status': 'success', 'data': result}

orchestrator.register_step_handler('ba', my_ba_handler)
```

### 3. Context Passing

Pass data between steps using context:

```python
workflow = orchestrator.create_workflow(
    steps=['ba', 'architect'],
    context={
        'requirements_file': 'requirements/user_requirement.md',
        'codebase_path': 'src/'
    }
)
```

Results from each step are automatically added to context:
- `ba_result` - BA Agent output
- `architect_result` - Architect Agent output
- etc.

### 4. Step-by-Step Execution

Pause between steps for review:

```python
result = orchestrator.execute_workflow(
    workflow, 
    pause_between_steps=True  # Pauses after each step
)
```

### 5. Single Step Execution

Execute a single step independently:

```python
result = orchestrator.execute_single_step(
    'ba',
    context={'requirements_file': 'path/to/requirements.md'}
)
```

## PPS Workflow Usage

### Quick Start

```bash
# Run both BA and Architect (default)
python3 ai_workflow_orchestrated.py requirements/user_requirement.md

# Run only BA Agent
python3 ai_workflow_orchestrated.py requirements/user_requirement.md --steps ba

# Run with custom codebase
python3 ai_workflow_orchestrated.py requirements/user_requirement.md --codebase backend/

# Step-by-step mode
python3 ai_workflow_orchestrated.py requirements/user_requirement.md --step-by-step
```

### Command-Line Options

```
positional arguments:
  requirements_file     Requirements file to analyze

optional arguments:
  --codebase PATH      Codebase path to analyze (default: src)
  --steps STEP [...]   Workflow steps: ba, architect, qa, developer, senior_dev
  --step-by-step       Pause between steps for review
```

## Use Cases

### 1. Review Requirements Only

```bash
python3 ai_workflow_orchestrated.py requirements/user_requirement.md --steps ba
```

**When to use:**
- Initial requirements review
- Validating user stories before design
- Quick requirements check

### 2. Requirements + Architecture

```bash
python3 ai_workflow_orchestrated.py requirements/user_requirement.md --steps ba architect
```

**When to use:**
- Design phase
- Architecture review
- Pattern recommendation

### 3. Full Pipeline (Future)

```bash
python3 ai_workflow_orchestrated.py requirements/user_requirement.md \
  --steps ba architect qa developer senior_dev
```

**When to use:**
- Complete end-to-end automation
- Full CI/CD integration
- Comprehensive code migration

### 4. Step-by-Step Review

```bash
python3 ai_workflow_orchestrated.py requirements/user_requirement.md \
  --steps ba architect --step-by-step
```

**When to use:**
- Learning/training
- Detailed validation
- Manual approval gates

## Workflow Results

Each workflow execution returns:

```python
{
    'status': 'completed',  # or 'failed'
    'stages': [
        {
            'key': 'ba',
            'name': 'Requirements Gathering',
            'agent': 'BAAgent',
            'status': 'completed',
            'result': { ... }
        },
        ...
    ],
    'context': {
        'ba_result': { ... },
        'architect_result': { ... }
    }
}
```

## Error Handling

- **Invalid step**: Raises `ValueError` with available steps
- **Step failure**: Workflow stops unless `pause_between_steps=True`
- **No handler**: Step is marked as 'skipped'

## Advanced: Custom Workflows

Create your own workflow script:

```python
from agents.lead_orchestrator import LeadOrchestrator

# Initialize
orchestrator = LeadOrchestrator(llm_config, jira_config)

# Register your custom handlers
orchestrator.register_step_handler('ba', my_ba_handler)
orchestrator.register_step_handler('architect', my_architect_handler)

# Create custom workflow
workflow = orchestrator.create_workflow(
    steps=['ba', 'architect'],
    jira_tickets=['PROJ-123', 'PROJ-124'],
    context={'custom_data': 'value'}
)

# Execute
result = orchestrator.execute_workflow(workflow)

# Access results
for stage in result['stages']:
    print(f"{stage['name']}: {stage['status']}")
```

## Benefits

1. **Flexibility**: Run only what you need
2. **Iterative Development**: Review and validate step-by-step
3. **Cost Control**: Execute expensive AI steps selectively
4. **Debugging**: Easier to isolate and fix issues
5. **Extensibility**: Easy to add new steps/agents

## Migration from Old Version

### Before (Fixed Pipeline)

```python
workflow = orchestrator.create_workflow(jira_tickets)
orchestrator.execute_workflow(workflow)
```

### After (Flexible)

```python
# Same behavior
workflow = orchestrator.create_workflow(
    jira_tickets=jira_tickets,
    steps=None  # All steps
)
orchestrator.execute_workflow(workflow)

# Or selective
workflow = orchestrator.create_workflow(
    jira_tickets=jira_tickets,
    steps=['ba', 'architect']  # Only these
)
```

## Examples

See complete examples in:
- `/Users/joeylam/repo/aiteam/examples/flexible_workflow_example.py`
- `/Users/joeylam/repo/pps/ai_workflow_orchestrated.py`

Run example scenarios:

```bash
cd /Users/joeylam/repo/aiteam
python3 examples/flexible_workflow_example.py 1  # Full workflow
python3 examples/flexible_workflow_example.py 2  # Single step
python3 examples/flexible_workflow_example.py 3  # Partial pipeline
python3 examples/flexible_workflow_example.py 4  # Step-by-step
python3 examples/flexible_workflow_example.py all  # All examples
```

## Next Steps

1. Review requirements with `--steps ba`
2. Validate output in `requirements/analysis/`
3. Run architecture design with `--steps ba architect`
4. Review architecture recommendations
5. Implement based on validated design

---

**Pro Tip**: Start with single steps during development, then use full pipeline in CI/CD!
