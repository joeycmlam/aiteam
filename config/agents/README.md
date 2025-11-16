# Unified Agent Configurations

This directory contains unified configuration files for all AI agents in the aiteam project. Each YAML file serves as the **single source of truth** for both VS Code GitHub Copilot Chat agents (Claude Sonnet 4) and Python automation agents (GPT-4o/Ollama).

## 📁 Directory Structure

```
config/agents/
├── README.md              ← This file
├── architect.yaml         ✅ Solution Architect agent config
├── ba.yaml                ✅ Business Analyst agent config
├── developer.yaml         ⏳ Senior Developer agent config (TODO)
├── qa.yaml                ⏳ QA Engineer agent config (TODO)
└── lead.yaml              ⏳ Lead Orchestrator agent config (TODO)
```

## 🎯 Purpose

### Before Unified Configs
- Agent personas defined in `.vscode/agents/*.agent.md`
- Agent prompts defined in `config/prompts/*_agent_prompts.yaml`
- **Problem**: Configuration duplicated, risk of inconsistency

### After Unified Configs
- **Single YAML file** per agent in this directory
- Contains: metadata, persona, VS Code settings, Python prompts
- **Benefit**: One source of truth, guaranteed consistency

## 📄 Configuration Format

Each `{agent}.yaml` file follows this structure:

```yaml
metadata:
  name: agent_name           # Unique identifier
  role: Agent Role           # Display name
  description: What it does  # Purpose description
  version: 1.0.0             # Semantic version
  author: AI Team            # Maintainer

persona:
  title: Professional Title
  
  expertise:
    - Area 1
    - Area 2
  
  focus_areas:
    - Focus 1
    - Focus 2
  
  technology_stack:
    languages: [Python, TypeScript]
    frameworks: [FastAPI, Flask]
    cloud: Azure (AKS, API Management)
  
  considerations:
    - Best practice 1
    - Guideline 2

vscode_agent:
  model: Claude Sonnet 4     # LLM model for VS Code Chat
  tools:                     # VS Code agent tools
    - read
    - search
    - fetch
    - usages
  handoffs:                  # Agents to collaborate with
    - developer
    - lead
  capabilities:              # What the agent can do
    - Capability 1
    - Capability 2

prompts:
  prompt_name:
    template: |
      Prompt text with {placeholders}
    system_message: |
      System message for LLM context
    # Optional parameters
    max_content_length: 3000
    max_analysis_length: 2000

fallbacks:
  # Templates used when LLM unavailable
  fallback_name: |
    Fallback template text
```

## 🔧 Usage

### In Python Agents

```python
from shared.agent_config_loader import AgentConfigLoader

class MyAgent:
    def __init__(self):
        loader = AgentConfigLoader()
        
        # Load full config
        self.config = loader.load_agent_config('architect')
        
        # Or get specific sections
        self.persona = loader.get_persona('architect')
        self.prompts = loader.get_prompts('architect')
        
        # Auto-generated system message from persona
        system_msg = loader.get_system_message('architect')
```

### In VS Code Chat Agents

Currently `.vscode/agents/*.agent.md` files reference these configs implicitly. Future enhancement will add explicit references:

```yaml
---
config: ../../config/agents/architect.yaml
---
```

## 🧪 Testing

### Test All Configs
```bash
python3 tests/test_unified_config.py
```

### Test Specific Agent
```python
from shared.agent_config_loader import AgentConfigLoader

loader = AgentConfigLoader()

# Load and validate
config = loader.load_agent_config('architect')
result = loader.validate_config('architect')

print(f"Valid: {result['valid']}")
print(f"Errors: {result['errors']}")
```

### List Available Agents
```python
from shared.agent_config_loader import AgentConfigLoader

agents = AgentConfigLoader().list_available_agents()
print(agents)  # ['architect', 'ba', 'developer', 'qa', 'lead']
```

## 📝 Creating New Configs

### Step 1: Copy Template
```bash
cp config/agents/architect.yaml config/agents/my_agent.yaml
```

### Step 2: Customize Sections

1. **metadata**: Update name, role, description
2. **persona**: Define title, expertise, focus_areas, technology_stack
3. **vscode_agent**: Set model, tools, handoffs, capabilities
4. **prompts**: Create prompt templates with system messages
5. **fallbacks**: Add templates for when LLM unavailable

### Step 3: Validate
```bash
python3 -c "from shared.agent_config_loader import AgentConfigLoader; \
  print(AgentConfigLoader().validate_config('my_agent'))"
```

### Step 4: Test
```bash
python3 tests/test_unified_config.py
```

## ✅ Agent Status

| Agent | Config File | Status | Python Agent | VS Code Agent |
|-------|-------------|--------|--------------|---------------|
| Solution Architect | `architect.yaml` | ✅ Complete | `agents/architect_agent.py` | `.vscode/agents/architect.agent.md` |
| Business Analyst | `ba.yaml` | ✅ Complete | `agents/ba_agent.py` | `.vscode/agents/ba.agent.md` |
| Senior Developer | `developer.yaml` | ⏳ TODO | `agents/developer_agent.py` | `.vscode/agents/developer.agent.md` |
| QA Engineer | `qa.yaml` | ⏳ TODO | `agents/qa_agent.py` | ⚠️ Missing |
| Lead Orchestrator | `lead.yaml` | ⏳ TODO | `agents/lead_orchestrator.py` | `.vscode/agents/lead.agent.md` |

**Legend**:
- ✅ Complete - Unified config exists and tested
- ⏳ TODO - Needs unified config creation
- ⚠️ Missing - Component doesn't exist yet

## 🔄 Migration Checklist

For each agent, complete these steps:

### 1. Create Unified Config
- [ ] Copy template from `architect.yaml`
- [ ] Extract persona from `.vscode/agents/{agent}.agent.md`
- [ ] Extract prompts from `config/prompts/{agent}_agent_prompts.yaml`
- [ ] Add metadata, expertise, technology_stack
- [ ] Define VS Code agent settings
- [ ] Add fallback templates

### 2. Validate Config
- [ ] Run: `loader.validate_config('{agent}')`
- [ ] Fix any validation errors
- [ ] Verify all required sections present

### 3. Update Python Agent
- [ ] Import `AgentConfigLoader`
- [ ] Replace `self._load_prompts()` with loader calls
- [ ] Update `__init__` to use unified config
- [ ] Test agent in workflow

### 4. Test Both Interfaces
- [ ] Test VS Code Chat: `@{agent} <request>`
- [ ] Test Python automation: Run workflow script
- [ ] Verify consistent behavior

### 5. Archive Legacy Config
- [ ] Move old YAML to `config/prompts/legacy/`
- [ ] Update documentation
- [ ] Remove deprecated code

## 🐛 Validation Rules

The `AgentConfigLoader` validates:

### Required Sections
- ✅ `metadata` (name, role, description)
- ✅ `persona` (title, expertise, focus_areas)
- ✅ `prompts` (at least one prompt defined)

### Optional Sections
- `vscode_agent` (model, tools, handoffs)
- `fallbacks` (templates for LLM unavailable)

### Validation Example
```python
from shared.agent_config_loader import AgentConfigLoader

result = AgentConfigLoader().validate_config('architect')

# Result structure:
{
  'valid': True/False,
  'errors': [...],      # Critical issues
  'warnings': [...]     # Non-critical issues
}
```

## 📊 Benefits

### 1. Single Source of Truth
- One file per agent vs. two separate configs
- Update once → affects both VS Code and Python

### 2. Consistency
- Same persona in interactive Chat and automation
- Guaranteed alignment between interfaces

### 3. Maintainability
- Clear structure with validation
- Easy to add new agents or prompts
- Version controlled

### 4. Flexibility
- Use Claude Sonnet 4 in VS Code Chat
- Use GPT-4o or Ollama in Python automation
- Same configuration, different execution

### 5. Backward Compatibility
- Legacy configs still work via fallback
- Gradual migration path
- No breaking changes

## 📚 Documentation

- **Quick Start**: `doc/UNIFIED_CONFIG_QUICKSTART.md`
- **Strategy**: `doc/UNIFIED_AGENT_CONFIG_STRATEGY.md`
- **Implementation**: `doc/UNIFIED_CONFIG_IMPLEMENTATION.md`
- **Summary**: `doc/UNIFIED_CONFIG_SUMMARY.md`
- **Copilot Guide**: `.github/copilot-instructions.md`

## 🔗 Related Files

- **Config Loader**: `shared/agent_config_loader.py`
- **Test Suite**: `tests/test_unified_config.py`
- **VS Code Agents**: `.vscode/agents/*.agent.md`
- **Python Agents**: `agents/*_agent.py`
- **Legacy Prompts**: `config/prompts/*_agent_prompts.yaml`

## 💡 Best Practices

### 1. Keep Prompts DRY
Reuse common system messages across prompts:
```yaml
prompts:
  analyze_code:
    template: "..."
    system_message: &system_msg |
      You are a Solution Architect...
  
  recommend_patterns:
    template: "..."
    system_message: *system_msg  # Reuse
```

### 2. Use Placeholders
Make templates flexible with placeholders:
```yaml
template: |
  Analyze {file_count} files written in {languages}.
  Focus on {aspect}.
```

### 3. Document Considerations
Add important guidelines in `persona.considerations`:
```yaml
considerations:
  - Always validate input parameters
  - Consider scalability and performance
  - Document security implications
```

### 4. Define Clear Expertise
Be specific in `persona.expertise`:
```yaml
expertise:
  - RESTful API design and versioning
  - Event-driven architecture patterns
  - Microservices communication (gRPC, message queues)
```

### 5. Add Fallbacks
Provide templates for when LLM unavailable:
```yaml
fallbacks:
  analysis: |
    # AI Analysis Unavailable
    Please manually review: {content}
```

## 🚀 Quick Commands

```bash
# Validate all configs
for agent in architect ba developer qa lead; do
  python3 -c "from shared.agent_config_loader import AgentConfigLoader; \
    print(f'{$agent}: {AgentConfigLoader().validate_config('$agent')}')"
done

# List available agents
python3 -c "from shared.agent_config_loader import AgentConfigLoader; \
  print(AgentConfigLoader().list_available_agents())"

# Test unified configs
python3 tests/test_unified_config.py

# View agent persona
python3 -c "from shared.agent_config_loader import AgentConfigLoader; \
  import json; print(json.dumps(AgentConfigLoader().get_persona('architect'), indent=2))"
```

## 📞 Support

For questions or issues:
1. Check `doc/UNIFIED_CONFIG_QUICKSTART.md` for common tasks
2. Review example configs: `architect.yaml`, `ba.yaml`
3. Run tests: `python3 tests/test_unified_config.py`
4. See loader implementation: `shared/agent_config_loader.py`

---

**Last Updated**: 2025-01-24  
**Status**: 2/5 agents complete (architect ✅, ba ✅)  
**Next Milestone**: Create developer.yaml, qa.yaml, lead.yaml
