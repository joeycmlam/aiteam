# Claude Sonnet 4 Integration Guide

## Quick Start (3 Steps)

**Get up and running with Claude in 3 minutes:**

1. **Get API Key** - Visit https://console.anthropic.com/ and create an API key
2. **Configure** - Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ANTHROPIC_MODEL=claude-sonnet-4-20250514
   LLM_PROVIDER=anthropic
   ```
3. **Test** - Run: `python3 tests/test_claude.py`

**That's it!** All agents now support Claude. For detailed information, continue reading below.

---

## Overview

The aiteam project now supports **Claude Sonnet 4** (claude-sonnet-4-20250514) and other Claude models via the Anthropic API. This provides an alternative to GitHub Models API (GPT-4o) and Ollama for your AI agent workflows.

## Features

✅ **Claude Sonnet 4** - Latest and most capable Claude model
✅ **Multiple Claude Models** - Sonnet 4, Claude 3.5, Opus, Haiku
✅ **Seamless Switching** - Switch between Anthropic, GitHub, and Ollama providers
✅ **Fallback Support** - Automatically falls back to Ollama if Claude unavailable
✅ **Full Integration** - Works with all existing agents (BA, Tech Lead, Developer, etc.)

## Setup

### 1. Install Dependencies

```bash
cd /Users/joeylam/repo/aiteam
pip install -r requirements.txt
```

This installs the `anthropic` package (v0.39.0).

### 2. Get Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key

### 3. Configure Environment

Edit `.env` file in the project root:

```bash
# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxx  # Replace with your actual key
ANTHROPIC_MODEL=claude-sonnet-4-20250514      # Default model

# LLM Provider
LLM_PROVIDER=anthropic  # Use 'anthropic' to enable Claude
```

### 4. Update Agent Config (Optional)

Edit `config/agent_config.yaml`:

```yaml
llm:
  provider: "anthropic"  # Change from "ollama" to "anthropic"
  model: "claude-sonnet-4-20250514"
  temperature: 0.3
```

## Available Models

### Claude 4 Series (Latest)
- **claude-sonnet-4-20250514** - Claude Sonnet 4 (Recommended - Most capable)

### Claude 3.5 Series
- **claude-3-5-sonnet-20241022** - Claude 3.5 Sonnet (Fast and capable)

### Claude 3 Series
- **claude-3-opus-20240229** - Claude 3 Opus (Most capable of Claude 3)
- **claude-3-sonnet-20240229** - Claude 3 Sonnet (Balanced)
- **claude-3-haiku-20240307** - Claude 3 Haiku (Fastest and cheapest)

## Usage

### Basic Usage

```python
from shared.llm_manager import LLMManager

# Initialize with Anthropic provider
llm = LLMManager(provider="anthropic")

# Generate response
response = llm.generate(
    prompt="Explain Python decorators in 3 sentences.",
    system_message="You are a Python expert.",
    max_tokens=500
)
print(response)
```

### Override Model Per Request

```python
# Use default Claude Sonnet 4
llm = LLMManager(provider="anthropic")

# Override to use Claude 3.5 Sonnet for a specific request
response = llm.generate(
    prompt="Quick code review needed",
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000
)
```

### With Existing Agents

All existing agents automatically support Claude:

```python
from agents.ba_agent import BusinessAnalystAgent

# BA Agent will use Claude if LLM_PROVIDER=anthropic
ba = BusinessAnalystAgent(output_dir="output")
result = ba.process(requirements_text)
```

### Model Switching in Code

```python
from shared.llm_manager import LLMManager

# Quick prototyping with Ollama
llm_local = LLMManager(provider="ollama", model="llama3.2")

# Production with Claude Sonnet 4
llm_claude = LLMManager(provider="anthropic", model="claude-sonnet-4-20250514")

# Complex tasks with GPT-4o
llm_github = LLMManager(provider="github_copilot_cli", model="gpt-4o")
```

## Testing

### Test Claude Integration

```bash
python tests/test_claude.py
```

This will:
1. Verify Anthropic API key is configured
2. Test Claude Sonnet 4 response generation
3. Test Claude 3.5 Sonnet
4. Test model switching between providers

Expected output:
```
==================================================================
🧪 Testing Anthropic Claude Integration
==================================================================

1️⃣  Testing with Anthropic Claude...
🤖 LLM Manager initialized with provider: anthropic, model: claude-sonnet-4-20250514
✅ Anthropic API configured

📝 Prompt: Write a simple Python function that adds two numbers...

⏳ Generating response with Claude...
   🤖 Calling Anthropic API (claude-sonnet-4-20250514)...
   ✅ Anthropic API response received

✅ Response received (XXX characters):
----------------------------------------------------------------------
[Claude's response here]
----------------------------------------------------------------------

✅ All Claude tests completed successfully!
```

### Test with Specific Agent

```bash
# Test BA Agent with Claude
python agents/ba_agent.py --input doc/example_requirements.md
```

## Cost Considerations

Claude API pricing (as of 2024):

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Sonnet 4 | $3.00 | $15.00 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

💡 **Tip**: Use Claude 3 Haiku for simpler tasks to reduce costs.

## Provider Comparison

| Feature | Anthropic (Claude) | GitHub Models (GPT) | Ollama (Local) |
|---------|-------------------|---------------------|----------------|
| **Cost** | Pay-per-use | Included w/ Copilot | Free |
| **Privacy** | Cloud API | Cloud API | Local only |
| **Speed** | Fast | Fast | Depends on hardware |
| **Quality** | Excellent | Excellent | Good |
| **Best For** | Production, complex reasoning | Production, code generation | Development, testing |

## Fallback Behavior

If Claude API fails (no API key, rate limit, error), the system automatically falls back to Ollama:

```
⚠️  Anthropic API authentication failed
   Falling back to Ollama...
```

To disable fallback, ensure Ollama is not running or modify `llm_manager.py`.

## Troubleshooting

### Error: "Anthropic package not installed"

```bash
pip install anthropic==0.39.0
```

### Error: "ANTHROPIC_API_KEY not found"

1. Check `.env` file exists in project root
2. Verify `ANTHROPIC_API_KEY=sk-ant-api03-...` is set
3. Ensure no typos in the key
4. Restart your terminal/IDE to reload environment

### Error: "Anthropic API authentication failed"

1. Verify API key is correct
2. Check key hasn't expired
3. Generate new key at https://console.anthropic.com/

### Error: "Rate limit exceeded"

1. Wait a few minutes
2. Consider upgrading Anthropic plan
3. Temporarily switch to different provider:

```python
llm = LLMManager(provider="ollama")  # Use local model
```

## Best Practices

### 1. Use Appropriate Models

```python
# Complex reasoning, analysis → Claude Sonnet 4
llm = LLMManager(provider="anthropic", model="claude-sonnet-4-20250514")

# Fast responses, simple tasks → Claude 3 Haiku
llm = LLMManager(provider="anthropic", model="claude-3-haiku-20240307")
```

### 2. Set Reasonable Token Limits

```python
# For summaries
response = llm.generate(prompt, max_tokens=500)

# For detailed analysis
response = llm.generate(prompt, max_tokens=4000)
```

### 3. Use System Messages

```python
response = llm.generate(
    prompt="Review this code...",
    system_message="You are a senior Python architect with 15 years experience."
)
```

### 4. Environment-Specific Configs

```bash
# Development
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2

# Staging
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Production
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

## Integration with Workflows

### Example: BA Agent with Claude

```python
#!/usr/bin/env python3
from agents.ba_agent import BusinessAnalystAgent
import os

# Set provider via environment
os.environ['LLM_PROVIDER'] = 'anthropic'
os.environ['ANTHROPIC_MODEL'] = 'claude-sonnet-4-20250514'

# Initialize and run
ba = BusinessAnalystAgent(output_dir="output")
result = ba.analyze_requirements("requirements.md")
```

### Example: Complete Workflow

```bash
# Set Claude as provider
export LLM_PROVIDER=anthropic
export ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Run complete workflow
python workflows/initiative_pipeline.py \
  --jira-key PROJ-123 \
  --output-dir output/claude-analysis
```

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Model Guide](https://docs.anthropic.com/claude/docs/models-overview)
- [Anthropic Console](https://console.anthropic.com/)
- [Python SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)

## Support

For issues with:
- **Claude integration**: Check this guide and test with `tests/test_claude.py`
- **API errors**: See Troubleshooting section above
- **Agent behavior**: Review agent-specific documentation in `doc/`

---

**Last Updated**: 2024
**Version**: 1.0
**Status**: Production Ready ✅
