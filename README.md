# AITeam - Intelligent Agent Framework

An AI-powered agent framework for software development workflows, featuring Business Analyst, Tech Lead, Architect, and Developer agents working together.

## ✨ New: Claude Sonnet 4 Support!

Now supports **Claude Sonnet 4** (claude-sonnet-4-20250514) in addition to GPT-4o and local models!

🚀 **Quick Start**: See [CLAUDE_QUICKSTART.md](CLAUDE_QUICKSTART.md)

## Features

- 🤖 **Multiple AI Providers**
  - **Anthropic Claude** (Sonnet 4, 3.5, Opus, Haiku) ⭐ NEW
  - **GitHub Models** (GPT-4o, GPT-4o-mini)
  - **Ollama** (Local LLMs - llama3.2, qwen2.5, etc.)

- 👥 **Specialized Agents**
  - Business Analyst Agent - Requirements analysis
  - Tech Lead Agent - Technical design
  - Architect Agent - System architecture
  - Developer Agent - Code implementation

- 🔄 **Workflow Orchestration**
  - JIRA integration
  - Automated pipelines
  - Context passing between agents
  - Agent chaining

- 🛠 **Developer Experience**
  - VS Code integration
  - Custom chat agents
  - Python automation
  - Comprehensive testing

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Provider

#### Option A: Claude Sonnet 4 (Recommended)

```bash
# Get API key from https://console.anthropic.com/
# Edit .env file:
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
LLM_PROVIDER=anthropic
```

#### Option B: GitHub Models (GPT-4o)

```bash
# Edit .env file:
GITHUB_TOKEN=your_github_token
GITHUB_MODEL=gpt-4o
LLM_PROVIDER=github_copilot_cli
```

#### Option C: Local Ollama (Free)

```bash
# Edit .env file:
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
LLM_PROVIDER=ollama

# Start Ollama
ollama serve
```

### 3. Test

```bash
# Test Claude integration
python3 tests/test_claude.py

# Test general LLM
python3 tests/test_llm.py
```

### 4. Run Agents

```bash
# Business Analyst Agent
python3 agents/ba_agent.py --input requirements.md

# Complete workflow
python3 workflows/initiative_pipeline.py --jira PROJ-123
```

## Documentation

- 📖 [Claude Integration Guide](doc/CLAUDE_INTEGRATION.md) - Complete Claude setup and usage
- 🚀 [Claude Quick Start](CLAUDE_QUICKSTART.md) - Get started in 3 minutes
- 📝 [Implementation Summary](CLAUDE_IMPLEMENTATION_SUMMARY.md) - What changed
- 🏗 [Project Architecture](doc/PROJECT_ARCHITECTURE.md) - System design
- 🤖 [Agent Framework Guide](doc/AGENT_FRAMEWORK_GUIDE.md) - Agent development
- 🔧 [GenAI Agent Options](doc/GENAI_AGENT_OPTIONS.md) - Provider comparison

## Project Structure

```
aiteam/
├── agents/                  # AI agent implementations
│   ├── ba_agent.py         # Business Analyst
│   ├── tech_lead_agent.py  # Tech Lead
│   ├── architect_agent.py  # Architect
│   └── enhanced_developer_agent.py
├── workflows/               # Workflow orchestration
│   └── initiative_pipeline.py
├── shared/                  # Shared utilities
│   ├── llm_manager.py      # LLM provider management
│   └── agent_framework.py  # Base agent classes
├── config/                  # Configuration files
│   ├── agent_config.yaml   # Agent settings
│   └── agents/            # Individual agent configs
├── tests/                   # Test suite
│   ├── test_claude.py      # Claude integration tests
│   └── test_llm.py         # General LLM tests
└── doc/                     # Documentation
```

## Usage Examples

### Using Claude Sonnet 4

```python
from shared.llm_manager import LLMManager

# Initialize with Claude
llm = LLMManager(provider="anthropic")

# Generate response
response = llm.generate(
    prompt="Explain microservices architecture",
    system_message="You are a senior software architect.",
    max_tokens=2000
)

print(response)
```

### Running BA Agent with Claude

```python
import os
from agents.ba_agent import BusinessAnalystAgent

# Configure to use Claude
os.environ['LLM_PROVIDER'] = 'anthropic'
os.environ['ANTHROPIC_MODEL'] = 'claude-sonnet-4-20250514'

# Run agent
ba = BusinessAnalystAgent(output_dir="output")
result = ba.analyze_requirements("requirements.md")
```

### Model Switching

```bash
# Use Claude Sonnet 4 for complex analysis
export LLM_PROVIDER=anthropic
export ANTHROPIC_MODEL=claude-sonnet-4-20250514
python3 agents/architect_agent.py

# Use Claude Haiku for simple tasks (faster, cheaper)
export ANTHROPIC_MODEL=claude-3-haiku-20240307
python3 agents/ba_agent.py

# Use GPT-4o for code generation
export LLM_PROVIDER=github_copilot_cli
export GITHUB_MODEL=gpt-4o
python3 agents/enhanced_developer_agent.py

# Use local Ollama for development
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.2
python3 agents/ba_agent.py
```

## Available Models

### Anthropic Claude

| Model | Best For | Speed |
|-------|----------|-------|
| claude-sonnet-4-20250514 | Complex reasoning, production | Fast ⚡ |
| claude-3-5-sonnet-20241022 | Balanced performance | Very Fast ⚡⚡ |
| claude-3-haiku-20240307 | Simple tasks, high volume | Fastest ⚡⚡⚡ |

### GitHub Models

| Model | Best For |
|-------|----------|
| gpt-4o | General purpose, code generation |
| gpt-4o-mini | Faster responses, simpler tasks |

### Ollama (Local)

| Model | Best For |
|-------|----------|
| llama3.2 | General purpose |
| qwen2.5 | Code and reasoning |
| mistral | Balanced performance |

## Testing

```bash
# Test Claude integration
python3 tests/test_claude.py

# Test LLM manager
python3 tests/test_llm.py

# Run all tests
pytest tests/
```

## JIRA Integration

Configure JIRA in `.env`:

```bash
JIRA_SERVER=https://yourcompany.atlassian.net
JIRA_USER=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token
```

Run workflow with JIRA:

```bash
python3 workflows/initiative_pipeline.py \
  --jira PROJ-123 \
  --output-dir output
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Provider Comparison

| Feature | Claude | GitHub Models | Ollama |
|---------|--------|---------------|--------|
| **Cost** | Pay-per-use | Included w/ Copilot | Free |
| **Privacy** | Cloud API | Cloud API | 100% Local |
| **Setup** | API key | GitHub token | Local install |
| **Speed** | Fast | Fast | Hardware dependent |
| **Quality** | Excellent | Excellent | Good |
| **Best For** | Complex reasoning | Code generation | Development/Testing |

## Requirements

- Python 3.10+
- pip packages (see requirements.txt)
- API keys for cloud providers (optional)
- Ollama installed for local LLMs (optional)

## License

[Your License Here]

## Support

- 📖 Documentation in `doc/` directory
- 🧪 Test scripts in `tests/` directory
- 💬 Issues: [GitHub Issues]
- 📧 Contact: [Your Contact]

## Acknowledgments

- Anthropic for Claude API
- GitHub for Models API
- Ollama for local LLM support
- LangChain for LLM framework

---

**Status**: Production Ready ✅  
**Last Updated**: 2024  
**Version**: 2.0 (with Claude Sonnet 4 support)
