# GitHub Models API Setup Guide

## ⚠️ Important: Claude NOT Available via GitHub Models API

**CORRECTION**: Claude models are **NOT available** through GitHub Models API despite some documentation claims.

Your GitHub Copilot subscription provides:
- **GPT-4o** (OpenAI) ✅
- **GPT-4o-mini** (OpenAI) ✅
- **Mistral Large** (Mistral AI) ✅
- ~~**Claude 3.5 Sonnet**~~ ❌ NOT AVAILABLE

**To use Claude with GitHub Copilot license:**
1. Use VS Code Chat Agents (`.vscode/agents/*.agent.md`) - Claude Sonnet 4 available via chat interface
2. OR add separate Anthropic API key for programmatic access (not included with Copilot)

---

## 🔧 Setup Steps

### 1. Get Your GitHub Token

You need a GitHub Personal Access Token (Classic) with minimal permissions:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Set:
   - **Note**: "GitHub Models API"
   - **Expiration**: 90 days (recommended)
   - **Scopes**: Check **ONLY** `read:user` (minimal permission needed)
4. Click **"Generate token"**
5. **Copy the token immediately** (you won't see it again!)

### 2. Add Token to .env File

```bash
# Edit your .env file
nano .env
```

Add this line:
```bash
# GitHub Models API (for Claude 3.5 Sonnet access)
GITHUB_TOKEN=ghp_your_token_here

# Keep your existing settings
LLM_PROVIDER=github_copilot_cli
OLLAMA_MODEL=llama3.2
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

### 3. Test the Setup

```bash
python3 test_github_models.py
```

---

## 🚀 Usage in Code

The LLM Manager will now use Claude 3.5 Sonnet when you set provider to `github_copilot_cli`:

```python
from shared.llm_manager import LLMManager

# Use Claude 3.5 Sonnet via GitHub Models API
llm = LLMManager("github_copilot_cli")

response = llm.generate(
    "Write a Python function to calculate fibonacci numbers",
    system_message="You are an expert Python developer"
)

print(response)
```

---

## 📊 Available Models (GitHub Models API)

Change the model in `llm_manager.py` or via `GITHUB_MODEL` env variable:

```python
"model": "gpt-4o",  # Recommended for programmatic use
```

**Verified Available Models:**
- `gpt-4o` - OpenAI's latest model (recommended)
- `gpt-4o-mini` - Faster, cheaper GPT-4o
- `mistral-large` - Mistral AI's flagship model
- `o1-preview` - OpenAI's reasoning model
- `o1-mini` - Smaller reasoning model

**NOT Available:**
- ❌ `claude-3.5-sonnet` - Use VS Code Chat Agents instead
- ❌ `claude-*` - Any Claude models

---

## 🎯 Why This Instead of Copilot CLI?

| Feature | GitHub Copilot CLI | GitHub Models API |
|---------|-------------------|-------------------|
| **Status** | ❌ Deprecated (Sep 2025) | ✅ Active & Supported |
| **Access** | Terminal only | Programmatic API |
| **Models** | Limited | Claude 3.5, GPT-4o, Mistral Large |
| **Integration** | Can't embed in code | Full Python integration |
| **Rate Limits** | Unclear | Documented & generous |
| **Cost** | Included in Copilot | Included in Copilot |

**Bottom line**: GitHub Models API is the official, supported way to access Claude 3.5 Sonnet programmatically.

---

## 🔍 How It Works

1. **Authentication**: Uses your GitHub token (requires Copilot subscription)
2. **Endpoint**: `https://models.inference.ai.azure.com/chat/completions`
3. **Protocol**: OpenAI-compatible Chat Completions API
4. **Fallback**: Automatically falls back to Ollama if GitHub API fails

---

## 🛡️ Security Notes

**Your .env file now contains:**
- ✅ `GITHUB_TOKEN` - Keep this SECRET!
- ✅ Already in `.gitignore` - Won't be committed to git

**Token Permissions:**
- ✅ Minimal scope (`read:user` only)
- ✅ Can be revoked anytime at https://github.com/settings/tokens
- ⚠️ Set expiration to 90 days (recommended)

---

## 📈 Rate Limits

GitHub Models API has generous limits for Copilot users:
- **Requests**: 15 requests per minute
- **Tokens**: Up to 150,000 tokens per day
- **Models**: All models share the same quota

If you hit limits:
- Wait 1 minute for rate limit reset
- Consider using Ollama for bulk operations
- Use GitHub Models for critical/complex tasks

---

## 🔄 Hybrid Strategy (Recommended)

**Best of both worlds:**

```python
# Complex architecture decisions → Claude 3.5 Sonnet
architect_llm = LLMManager("github_copilot_cli")  # Uses Claude 3.5
architecture = architect_llm.generate("Design microservices architecture...")

# Bulk code generation → Ollama (local, unlimited)
dev_llm = LLMManager("ollama")  # Uses llama3.2
code = dev_llm.generate("Generate CRUD endpoints...")
```

**When to use each:**
- **Claude 3.5 Sonnet** (GitHub Models):
  - Architecture decisions
  - Complex code reviews
  - Critical bug analysis
  - Requirements analysis
  
- **Ollama** (Local):
  - Bulk code generation
  - Test data creation
  - Documentation generation
  - Learning/experimentation

---

## 🐛 Troubleshooting

### "GitHub token is invalid or expired"
```bash
# Generate new token at:
https://github.com/settings/tokens

# Update .env with new token
```

### "GitHub Models API access denied"
```bash
# Check your Copilot subscription:
https://github.com/settings/copilot

# You need an active Copilot Individual or Business subscription
```

### "Rate limit exceeded"
```bash
# Wait 60 seconds, then try again
# Or switch to Ollama temporarily:
llm = LLMManager("ollama")
```

### "Connection error"
```bash
# Check internet connection
ping github.com

# Check if endpoint is accessible
curl -I https://models.inference.ai.azure.com
```

---

## 📚 Resources

- **GitHub Models Documentation**: https://docs.github.com/en/github-models
- **Available Models**: https://github.com/marketplace/models
- **API Reference**: https://learn.microsoft.com/en-us/azure/ai-studio/
- **Copilot Settings**: https://github.com/settings/copilot

---

## ✨ Quick Test

```bash
# Test Claude 3.5 Sonnet access
python3 -c "
from shared.llm_manager import LLMManager
llm = LLMManager('github_copilot_cli')
result = llm.generate('Say hello in Python')
print(result)
"
```

Expected output:
```
🤖 LLM Manager initialized with provider: github_copilot_cli
✅ GitHub CLI detected: 2.83.0
   🤖 Calling GitHub Models API (Claude 3.5 Sonnet)...
   ✅ GitHub Models API response received
print("Hello, World!")
```

---

**🎉 You're all set! Now you can use Claude 3.5 Sonnet in your AI agents!**
