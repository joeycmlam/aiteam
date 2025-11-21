# BA Chat Participant - Quick Reference

## 🎯 Common Commands

### Requirements Analysis
```
@ba analyze requirements from [file]
@ba validate requirements for [feature]
@ba review this for completeness: [paste text]
```

### User Stories
```
@ba create user stories for [feature]
@ba convert to user stories: [paste requirements]
@ba generate user story with acceptance criteria for [feature]
```

### BDD Scenarios
```
@ba create BDD scenarios for [feature]
@ba generate Gherkin feature file for [feature]
@ba write test scenarios including error cases for [feature]
```

### JIRA Integration
```
@ba analyze JIRA ticket [TICKET-ID]
@ba fetch JIRA initiative [EPIC-ID]
@ba query JIRA: [JQL query]
```

## 🔄 Handoff Commands

### To Architect
```
@ba [task] then send to architect
```
Or click **"Send to Architect"** button

### To Developer
```
@ba [task] then hand off to developer
```
Or click **"Send to Developer"** button

### To Tech Lead
```
@ba [task] and consult tech lead
```
Or click **"Consult Tech Lead"** button

## 📝 Output Formats

### User Story Format
```markdown
As a [role]
I want [feature]
So that [benefit]

Acceptance Criteria:
- Given [context]
  When [action]
  Then [outcome]
```

### BDD Scenario Format
```gherkin
Feature: [name]

Scenario: [description]
  Given [precondition]
  When [action]
  Then [outcome]
```

## 🎓 Best Practices

### ✅ Do
- Provide specific file paths or ticket IDs
- Include relevant context in prompts
- Use descriptive feature names
- Ask for specific output formats

### ❌ Avoid
- Vague requests without context
- Missing file paths or ticket numbers
- Asking for "help" without specifics
- Mixing multiple unrelated requests

## 🔧 Available Tools

- **search** - Search codebase and docs
- **githubRepo** - Access GitHub issues/PRs

## 📚 File Locations

- **Chat Agent**: `.vscode/agents/ba.agent.md`
- **Config**: `config/agents/ba.yaml`
- **Prompts**: `config/prompts/ba_agent_prompts.yaml`
- **Python Agent**: `agents/ba_agent.py`

## 💡 Example Workflow

```
1. @ba analyze requirements from requirements/spec.md
2. Review analysis results
3. @ba create user stories based on this analysis
4. Review user stories
5. @ba generate BDD scenarios for these stories
6. Click "Send to Architect" for design phase
```

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not responding | Check Copilot is active |
| JIRA errors | Verify credentials and ticket ID |
| File not found | Use absolute or workspace-relative path |
| Missing output | Check VS Code Chat output panel |

## 🚀 Quick Start

Type in VS Code Chat:
```
@ba help
```

Or start with:
```
@ba analyze requirements from [your-file]
```

---

For detailed documentation, see [BA_CHAT_PARTICIPANT_GUIDE.md](./BA_CHAT_PARTICIPANT_GUIDE.md)
