# Quick Start: Multi-Agent Team System

## 🚀 Get Started in 5 Minutes

### 1. Test the New Agents

```bash
# Test all new functionality
python3 tests/test_multi_agent_system.py
```

Expected output:
```
🧪 RUNNING MULTI-AGENT SYSTEM TESTS
======================================================================

Testing DBA Agent...
✅ DBA Agent initialized
✅ Schema designed with 1 tables
✅ Generated 1 migrations

Testing DevOps Agent...
✅ DevOps Agent initialized
✅ Pipeline designed with 3 stages
✅ Dockerfile generated

Testing Developer Pool...
✅ Developer pool initialized with 5 developers
✅ Task assigned to Dev-Frontend-1
✅ Team status retrieved

Testing Task Queue...
✅ Task queue initialized
✅ Task added: TASK-0001
✅ Task dependencies working correctly
✅ Priority ordering working correctly
✅ Queue statistics retrieved

Testing Agent Collaboration...
✅ Collaboration system initialized
✅ Pair programming session started: PAIR-0001
✅ Code review session started: REVIEW-0001
✅ Cross-functional review started: XREVIEW-0001
✅ Contribution added to session
✅ Session ended successfully

======================================================================
✅ ALL TESTS PASSED
======================================================================
```

### 2. Try Individual Agents

#### DBA Agent

```python
from agents.dba_agent import DBAAgent

dba = DBAAgent({'provider': 'ollama', 'model': 'llama3.2'})

# Design database schema
schema = dba.design_schema(
    requirements={'features': ['User auth', 'Products']},
    architecture={'tech_stack': {'database': 'postgresql'}}
)

print(f"Created {len(schema['tables'])} tables")
```

#### DevOps Agent

```python
from agents.devops_agent import DevOpsAgent

devops = DevOpsAgent({'provider': 'ollama', 'model': 'llama3.2'})

# Design CI/CD pipeline
pipeline = devops.design_cicd_pipeline({
    'technology_stack': {'language': 'python', 'framework': 'fastapi'},
    'requirements': {'environments': ['dev', 'prod']}
})

# Generate Dockerfile
dockerfile = devops.generate_dockerfile({
    'language': 'python',
    'framework': 'fastapi'
})

print(f"Pipeline with {len(pipeline['stages'])} stages created")
```

#### Developer Pool

```python
from agents.developer_pool import DeveloperPool

config = {
    'frontend': {'count': 2},
    'backend': {'count': 2},
    'fullstack': {'count': 1}
}

pool = DeveloperPool({'provider': 'ollama', 'model': 'llama3.2'}, config)

# Show team status
pool.print_team_status()

# Assign task
task = {
    'name': 'Create login UI',
    'type': 'frontend',
    'required_skills': ['react', 'typescript']
}

developer = pool.assign_task(task)
print(f"Task assigned to: {developer.developer_id}")
```

### 3. Run Enhanced Pipeline

```bash
# Process JIRA initiative with full team
python3 workflows/initiative_pipeline.py PROJ-123
```

The pipeline will:
1. ✅ Initialize 11 AI agents (BA, Architect, Tech Lead, QA, DBA, DevOps, 5 Developers)
2. ✅ Fetch JIRA initiative and structure requirements
3. ✅ Design system architecture
4. ✅ **NEW**: Design database schema with migrations
5. ✅ Generate comprehensive test cases
6. ✅ **NEW**: Distribute work across developer pool
7. ✅ **NEW**: Set up CI/CD pipeline and infrastructure
8. ✅ Perform code reviews
9. ✅ **NEW**: Coordinate team with standup and sprint planning

### 4. Use Task Queue

```python
from shared.task_queue import TaskQueue, TaskPriority

queue = TaskQueue()

# Add tasks with priorities and dependencies
task1 = queue.add_task(
    "Design database",
    "Create schema for users",
    priority=TaskPriority.HIGH,
    required_skills=['database']
)

task2 = queue.add_task(
    "Implement API",
    "Create authentication endpoints",
    priority=TaskPriority.HIGH,
    required_skills=['backend'],
    dependencies=[task1]  # Depends on task1
)

# Get next task for an agent
next_task = queue.get_next_task(['backend', 'api'], 'Backend-Dev')
print(f"Next task: {next_task.name}")

# Track progress
queue.start_task(next_task.task_id)
queue.complete_task(next_task.task_id)

# Monitor queue
queue.print_status()
```

### 5. Enable Agent Collaboration

```python
from shared.agent_collaboration import get_collaboration_manager

collab = get_collaboration_manager()

# Pair programming session
session = collab.start_pair_programming(
    "Dev-Frontend-1",
    "Dev-Frontend-2",
    task={'name': 'User dashboard', 'complexity': 'high'}
)

# Add contributions
collab.add_contribution_to_session(
    session.session_id,
    "Dev-Frontend-1",
    {'code': 'Dashboard component implemented'}
)

# Record decision
collab.record_decision(
    session.session_id,
    "Use Material-UI for components"
)

# End session
collab.end_collaboration(session.session_id, "Dashboard completed")

# Code review cycle
review = collab.start_code_review(
    "Dev-Backend-1",
    "Tech Lead",
    {'files': ['auth.py', 'users.py']}
)

print(f"Review session: {review.session_id}")
```

## 📋 What's New

### New Agents (3)
- 🗄️ **DBA Agent**: Database design, migrations, optimization
- 🚀 **DevOps Agent**: CI/CD, Docker, Kubernetes, monitoring
- 👥 **Developer Pool**: 5 specialized developers (2 frontend, 2 backend, 1 full-stack)

### New Systems (2)
- 📋 **Task Queue**: Priority-based task distribution with dependencies
- 🤝 **Agent Collaboration**: Pair programming, code reviews, cross-functional reviews

### Enhanced Components (3)
- ✏️ **Team Coordinator**: Now manages 11 agents
- ✏️ **Initiative Pipeline**: Includes database and infrastructure stages
- ✏️ **Configuration**: Comprehensive team and agent settings

## 🎯 Common Use Cases

### Use Case 1: New Web Application

```bash
# Set project type
export PROJECT_TYPE=greenfield

# Process initiative
python3 workflows/initiative_pipeline.py NEW-APP-001
```

**Outputs:**
- Database schema design
- React + FastAPI implementation
- Docker and Kubernetes configs
- GitHub Actions CI/CD pipeline
- Comprehensive test suite

### Use Case 2: Add Database to Existing App

```python
from agents.dba_agent import DBAAgent

dba = DBAAgent(llm_config)

# Design schema
schema = dba.design_schema(requirements, architecture)

# Generate migrations
migrations = dba.generate_migrations(current_schema, requirements)

# Review for optimization
review = dba.review_data_model(schema)
```

### Use Case 3: Set Up CI/CD Pipeline

```python
from agents.devops_agent import DevOpsAgent

devops = DevOpsAgent(llm_config)

# Design pipeline
pipeline = devops.design_cicd_pipeline(project_info)

# Generate configs
workflow = devops.generate_github_actions_workflow(pipeline)
dockerfile = devops.generate_dockerfile(tech_stack)
k8s = devops.create_kubernetes_manifests(architecture)
```

### Use Case 4: Parallel Development Tasks

```python
from agents.developer_pool import DeveloperPool

pool = DeveloperPool(llm_config, config)

# Create multiple tasks
tasks = [
    {'name': 'Login UI', 'type': 'frontend'},
    {'name': 'Auth API', 'type': 'backend'},
    {'name': 'User profile', 'type': 'frontend'},
    {'name': 'User service', 'type': 'backend'}
]

# Distribute across team
results = pool.distribute_tasks(tasks, context)

# Check status
pool.print_team_status()
```

## ⚙️ Configuration

### Enable/Disable Agents

Edit `config/agent_config.yaml`:

```yaml
team:
  specialists:
    dba:
      enabled: true  # Set to false to disable
    devops:
      enabled: true  # Set to false to disable
    
  developers:
    frontend:
      count: 2  # Adjust team size
    backend:
      count: 2
    fullstack:
      count: 1
```

### Adjust Workflow

```yaml
workflow:
  parallel_processing: true  # Enable parallel work
  max_concurrent_agents: 5   # Max agents working simultaneously
  
  # Collaboration features
  enable_pair_programming: false
  enable_code_review_cycles: true
  enable_cross_functional_reviews: true
  enable_architecture_review_board: true
```

## 🧪 Verify Installation

```bash
# 1. Test all agents
python3 tests/test_multi_agent_system.py

# 2. Test individual components
python3 agents/dba_agent.py
python3 agents/devops_agent.py
python3 agents/developer_pool.py

# 3. Test shared systems
python3 shared/task_queue.py
python3 shared/agent_collaboration.py

# 4. Test full pipeline
python3 workflows/initiative_pipeline.py --help
```

## 📚 Learn More

- **Full Documentation**: See `MULTI_AGENT_IMPLEMENTATION.md`
- **Agent Configs**: Check `config/agents/` directory
- **Examples**: Look for `if __name__ == "__main__"` sections in agent files
- **Tests**: Review `tests/test_multi_agent_system.py` for usage patterns

## 🎉 You're Ready!

The multi-agent team system is fully operational with:
- ✅ 11 specialized AI agents
- ✅ Parallel processing capabilities
- ✅ Task distribution and collaboration
- ✅ Database design automation
- ✅ CI/CD and infrastructure generation
- ✅ Comprehensive testing

Start by running:
```bash
python3 tests/test_multi_agent_system.py
```

Happy coding with your AI team! 🚀
