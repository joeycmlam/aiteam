# GitHub Copilot CLI Setup Guide

## 📋 Prerequisites

You need to install and configure GitHub CLI with Copilot extension.

## 🔧 Installation Steps

### 1. Install GitHub CLI (if not already installed)

```bash
brew install gh
```

### 2. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate.

### 3. Install GitHub Copilot Extension

```bash
gh extension install github/gh-copilot
```

### 4. Verify Installation

```bash
# Check gh CLI version
gh --version

# List installed extensions
gh extension list

# Test Copilot
gh copilot suggest "write a python function to calculate fibonacci"
```

## 🎯 Usage with Your AI Agents

Your agents will now use GitHub Copilot CLI automatically when configured with:

```yaml
# config/agent_config.yaml
llm:
  provider: "github_copilot_cli"
  model: "claude-3.5-sonnet"  # or "gpt-4"
```

And in `.env`:
```bash
LLM_PROVIDER=github_copilot_cli
```

## 💡 Available Commands

The system will use these GitHub Copilot CLI features:

- **`gh copilot suggest`** - For code generation
- **`gh copilot explain`** - For code analysis
- **`gh api`** - For direct API access to Copilot models

## ⚙️ Configuration

Edit `.env` to switch between providers:

```bash
# Use GitHub Copilot CLI (recommended if you have Copilot subscription)
LLM_PROVIDER=github_copilot_cli

# Or use Ollama (free, runs locally)
LLM_PROVIDER=ollama
```

## 🚀 Run Your Agents

```bash
# Activate virtual environment
source venv/bin/activate

# Run the migration pipeline
python workflows/migration_pipeline.py
```

## 🔍 Troubleshooting

### "gh: command not found"
Install GitHub CLI: `brew install gh`

### "Copilot extension not found"
Install extension: `gh extension install github/gh-copilot`

### "Authentication required"
Login to GitHub: `gh auth login`

### Fallback to Ollama
If GitHub Copilot CLI fails, the system automatically falls back to Ollama.
Make sure Ollama is running: `ollama serve`

## 📊 Which Provider Should You Use?

| Provider | Pros | Cons | Cost |
|----------|------|------|------|
| **github_copilot_cli** | • Uses Claude 3.5 Sonnet or GPT-4<br>• Part of your Copilot subscription<br>• High quality responses | • Requires internet<br>• API rate limits | Included with Copilot |
| **ollama** | • Runs locally<br>• No API limits<br>• Privacy | • Slower on older Macs<br>• Lower quality than Claude/GPT-4 | Free |

## 🎉 Benefits

✅ No need for separate API keys (uses your GitHub Copilot subscription)
✅ Access to Claude 3.5 Sonnet and GPT-4 models  
✅ Automatic fallback to Ollama if Copilot is unavailable
✅ Works with your existing setup

Happy coding! 🚀
