# BA Agent Prompts - Quick Reference Card

## 📂 File Location
```
config/prompts/ba_agent_prompts.yaml
```

## 🚀 Quick Start

### Default Usage
```python
from agents.ba_agent import BAAgent

ba = BAAgent(llm_config, jira_config)
# Automatically loads: config/prompts/ba_agent_prompts.yaml
```

### Custom Prompts
```python
ba = BAAgent(llm_config, jira_config, 
             prompts_config_path='path/to/custom_prompts.yaml')
```

## 📝 Available Prompts

| Prompt Name | Purpose | Variables |
|-------------|---------|-----------|
| `extract_requirements` | Extract from JIRA tickets | `{ticket_id}`, `{summary}`, `{description}` |
| `analyze_initiative` | Analyze epics/initiatives | `{summary}`, `{description}`, `{issue_type}`, `{linked_count}` |
| `analyze_requirements` | Full requirements analysis | `{raw_content}` |
| `generate_scenarios` | Create BDD scenarios | `{analysis}` |

## 🎨 Customization Template

```yaml
prompt_name:
  template: |
    Your prompt here with {variables}
  
  system_message: "AI role/instructions"
  
  # Optional settings
  max_content_length: 3000
```

## 💡 Common Customizations

### Change Analysis Style
```yaml
analyze_requirements:
  template: |
    Use AGILE format:
    {raw_content}
    
    Output: Epics, Stories, Tasks
  system_message: "You are an Agile coach."
```

### Add Industry Context
```yaml
extract_requirements:
  system_message: "You are a healthcare BA with HIPAA expertise."
```

### Adjust Defaults
```yaml
defaults:
  acceptance_criteria:
    - "Feature complete"
    - "Tests pass"
    - "Security approved"
```

## ✅ Testing

```bash
# Validate prompts
python3 tests/test_prompts.py

# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config/prompts/ba_agent_prompts.yaml'))"
```

## 📚 Documentation

- Full Guide: `config/prompts/README.md`
- Examples: `config/prompts/examples/`
- Summary: `doc/PROMPTS_EXTERNALIZATION_SUMMARY.md`

## 🔗 Variables Reference

| Variable | Example Value |
|----------|---------------|
| `{ticket_id}` | "SCRUM-123" |
| `{summary}` | "Implement user login" |
| `{description}` | "As a user, I want..." |
| `{issue_type}` | "Story", "Epic" |
| `{linked_count}` | 5 |
| `{raw_content}` | Full requirements text |
| `{analysis}` | AI analysis output |

## ⚡ Tips

1. **Version prompts** - Keep backups before changes
2. **Test first** - Use test data before production
3. **Start small** - Change one prompt at a time
4. **Document why** - Note reasons for changes
5. **Share wins** - Tell team about successful prompts

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Prompts not loading | Check file path and YAML syntax |
| Variables not replaced | Use `{var}` not `$var` or `${var}` |
| Falls back to defaults | Verify prompts file exists and is valid |

## 📞 Support

Questions? Check:
1. This card
2. `config/prompts/README.md`
3. Test suite: `tests/test_prompts.py`
