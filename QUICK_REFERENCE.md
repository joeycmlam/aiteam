# 🚀 Claude 3.5 Sonnet - Quick Reference

## ⚡ 30-Second Setup

```bash
# 1. Get token: https://github.com/settings/tokens (scope: read:user)
# 2. Add to .env:
echo "GITHUB_TOKEN=ghp_your_token_here" >> .env

# 3. Test:
python3 test_github_models.py
```

## 💻 Basic Usage

```python
from shared.llm_manager import LLMManager

# Use Claude 3.5 Sonnet
llm = LLMManager("github_copilot_cli")
response = llm.generate("Write a Python function to validate emails")
print(response)
```

## 🎯 When to Use

**Claude 3.5 Sonnet** (15 req/min, 150K tokens/day):
- ✅ Architecture decisions
- ✅ Code reviews
- ✅ Bug analysis
- ✅ Requirements

**Ollama** (Unlimited):
- ✅ Bulk generation
- ✅ Testing
- ✅ Documentation
- ✅ Experimentation

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Token not found" | Add `GITHUB_TOKEN=...` to `.env` |
| "Access denied" | Check Copilot subscription active |
| "Rate limit" | Wait 60 sec or use Ollama |
| Falls back to Ollama | Token missing/invalid (but still works!) |

## 📚 Documentation

- **Full Setup**: `GITHUB_MODELS_SETUP.md`
- **Examples**: `example_claude_usage.py`
- **Test**: `python3 test_github_models.py`

## 🎁 Available Models

Change in `llm_manager.py` line ~106:

```python
"model": "claude-3.5-sonnet",  # Current
# "model": "gpt-4o",           # Alternative
# "model": "mistral-large",     # Alternative
```

## ✅ Verification

```bash
# Quick test:
python3 -c "from shared.llm_manager import LLMManager; \
llm = LLMManager('github_copilot_cli'); \
print(llm.generate('Say hello'))"
```

Expected: Claude response OR automatic Ollama fallback

---

**🎉 That's it! You're ready to use Claude 3.5 Sonnet!**
