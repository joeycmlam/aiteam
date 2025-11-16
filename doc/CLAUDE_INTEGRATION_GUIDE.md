# Claude Integration Guide for GitHub Copilot Users

## 🎯 Your Claude Access with GitHub Copilot License

You have **TWO ways** to use AI models with your GitHub Copilot subscription:

### Option 1: VS Code Chat Agents (Claude Sonnet 4) ⭐ RECOMMENDED FOR CLAUDE
**Location**: `.vscode/agents/*.agent.md`

**Available Agents:**
- `@architect` - Solution Architect (Claude Sonnet 4)
- `@lead` - Tech Lead (Claude Sonnet 4)
- `@ba` - Business Analyst (Claude Sonnet 4)
- `@developer` - Senior Developer (Claude Sonnet 4)

**How to Use:**
1. Open VS Code Chat panel: `Ctrl+Cmd+I` (Mac) or `Ctrl+I` (Windows/Linux)
2. Type `@architect` (or other agent name) followed by your request
3. The agent uses Claude Sonnet 4 automatically

**Examples:**
```
@architect Design a microservices architecture for payment processing

@lead Review this PR for security issues and code quality

@ba Analyze JIRA epic SCRUM-5 and break it into user stories

@developer Implement authentication using TDD approach with pytest
```

**Pros:**
- ✅ Claude Sonnet 4 access (best model from Anthropic)
- ✅ Context-aware (sees your code, files, workspace)
- ✅ Interactive conversation
- ✅ No additional API keys needed
- ✅ Included with Copilot license

**Cons:**
- ❌ Interactive only (not programmatic)
- ❌ Must be in VS Code

---

### Option 2: GitHub Models API (GPT-4o, Mistral) - For Automation

**Location**: `shared/llm_manager.py`

**Available Models:**
- `gpt-4o` - OpenAI's latest (recommended)
- `gpt-4o-mini` - Faster, cheaper
- `mistral-large` - Mistral AI
- `o1-preview` - Reasoning model
- ❌ **Claude NOT available**

**Setup:**
1. Get GitHub token: https://github.com/settings/tokens
2. Add to `.env`: `GITHUB_TOKEN=ghp_xxxxx`
3. Set: `LLM_PROVIDER=github_copilot_cli` and `GITHUB_MODEL=gpt-4o`

**Usage:**
```python
from shared.llm_manager import LLMManager

llm = LLMManager("github_copilot_cli")
response = llm.generate(
    "Generate Python code for user authentication",
    model="gpt-4o"
)
```

**Pros:**
- ✅ Programmatic access (scripts, automation)
- ✅ Batch processing
- ✅ Integration in workflows
- ✅ Included with Copilot license

**Cons:**
- ❌ No Claude models
- ❌ Rate limits (15 req/min, 150K tokens/day)

---

## 🏆 Recommended Hybrid Workflow

### Use VS Code Chat Agents (Claude) for:
1. **Architecture & Design**
   ```
   @architect Design API gateway pattern for microservices
   ```

2. **Code Review**
   ```
   @lead Review this implementation for security and best practices
   ```

3. **Requirements Analysis**
   ```
   @ba Convert this JIRA epic into detailed user stories with acceptance criteria
   ```

4. **Complex Problem Solving**
   ```
   @developer Help me refactor this legacy code using SOLID principles
   ```

### Use Python Agents (GPT-4o) for:
1. **Bulk Code Generation**
   ```python
   # workflows/initiative_pipeline.py
   developer = DeveloperAgent(llm_config)
   implementation = developer.implement_feature(requirements, guidelines)
   ```

2. **Automated Testing**
   ```python
   qa = QAAgent(llm_config)
   qa.create_feature_files(requirements, "tests/features/")
   ```

3. **Batch Processing**
   ```bash
   python3 workflows/initiative_pipeline.py SCRUM-5
   ```

---

## 📋 Quick Reference

| Feature | VS Code Chat Agents | Python Automation |
|---------|---------------------|-------------------|
| **Model** | Claude Sonnet 4 | GPT-4o / Ollama |
| **Access** | Interactive (`@agent`) | Programmatic (Python) |
| **Best For** | Design, Review, Complex | Bulk, Automation, Testing |
| **Rate Limits** | Generous | 15/min, 150K tokens/day |
| **Setup** | None (built-in) | GITHUB_TOKEN in .env |
| **Cost** | Included | Included (or free with Ollama) |

---

## 🔧 Agent Definitions

Each VS Code agent is defined in `.vscode/agents/*.agent.md`:

```yaml
---
name: Solution Architect
description: Designs system architecture and technical specifications
tools: ['read', 'search', 'fetch', 'usages']
model: Claude Sonnet 4
---

You are a Solution Architect working in financial services...
```

**Customize agents by:**
1. Editing `.vscode/agents/*.agent.md` files
2. Changing the prompt/instructions
3. Adding/removing tools
4. Adjusting the model (keep as Claude Sonnet 4 for best results)

---

## ⚡ Example Workflows

### Workflow 1: Feature Development with Claude
```
1. @ba Analyze requirements from JIRA-123
2. @architect Design the architecture for this feature
3. @developer Write the implementation with tests
4. @lead Review the code before PR
```

### Workflow 2: Legacy Code Migration (Hybrid)
```bash
# Step 1: Use @architect for design decisions (Claude)
@architect Analyze tests/fixtures/legacy_code.py and recommend modernization patterns

# Step 2: Run automated pipeline (GPT-4o/Ollama)
python3 workflows/initiative_pipeline.py SCRUM-5

# Step 3: Use @lead for review (Claude)
@lead Review the generated code in generated_code/SCRUM-5/
```

### Workflow 3: Architecture Documentation
```
@architect Review our current system architecture in the codebase and:
1. Identify microservices boundaries
2. Document API contracts
3. Suggest improvements for scalability
4. Create ADR (Architecture Decision Records)
```

---

## 🚫 Common Mistakes to Avoid

### ❌ Mistake 1: Trying to use Claude programmatically
```python
# This will FAIL - Claude not in GitHub Models API
llm = LLMManager("github_copilot_cli")
response = llm.generate(prompt, model="claude-3.5-sonnet")
```

**✅ Correct:**
```
# Use VS Code Chat instead
@architect [your request]
```

### ❌ Mistake 2: Not leveraging VS Code agents
```python
# Don't write complex LLM prompts manually if you need Claude
prompt = "You are an architect. Analyze this code..."
```

**✅ Correct:**
```
# Let the agent handle the prompt engineering
@architect Analyze this codebase structure
```

### ❌ Mistake 3: Using wrong model for task
```python
# Using local Ollama for critical architecture decisions
llm = LLMManager("ollama")  # Less capable
```

**✅ Correct:**
```
# Use Claude for important decisions
@architect Design the security architecture
```

---

## 📊 Model Capabilities Comparison

| Task | Claude Sonnet 4 | GPT-4o | Ollama (llama3.2) |
|------|----------------|--------|-------------------|
| Architecture Design | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Code Review | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Code Generation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Bulk Processing | ❌ N/A | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Complex Reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cost | Included | Included | Free |

---

## 🎓 Learning Resources

- **VS Code Agent Documentation**: See `.vscode/agents/README.md` (if exists)
- **GitHub Models API**: `doc/GITHUB_MODELS_SETUP.md`
- **Workflow Patterns**: `doc/FLEXIBLE_WORKFLOW_GUIDE.md`
- **Project Architecture**: `doc/PROJECT_ARCHITECTURE.md`

---

**🎉 Bottom Line**: With your GitHub Copilot license, use VS Code Chat Agents for Claude Sonnet 4 interactively, and Python automation with GPT-4o or Ollama for batch processing. This gives you the best of both worlds!
