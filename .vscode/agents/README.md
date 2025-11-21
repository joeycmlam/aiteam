# VS Code Chat Agents

This directory contains Chat Participant configurations for the AI Team agents. Each agent is available through VS Code's Chat interface using the `@` mention syntax.

## 🤖 Available Agents

### Business Analyst (`@ba`)
**Role**: Requirements analysis, user story creation, BDD scenario generation

**Key Capabilities**:
- Analyze JIRA tickets and initiatives
- Parse requirement documents (MD, JSON, YAML, TXT)
- Generate detailed user stories with acceptance criteria
- Create BDD scenarios in Gherkin format
- Validate requirements for completeness and quality
- Export documentation and feature files

**Common Commands**:
```
@ba analyze requirements from [file]
@ba create user stories for [feature]
@ba generate BDD scenarios for [feature]
@ba fetch JIRA initiative [EPIC-ID]
```

**Documentation**:
- [Full Guide](./BA_CHAT_PARTICIPANT_GUIDE.md)
- [Quick Reference](./BA_QUICK_REFERENCE.md)
- [Agent Definition](./ba.agent.md)

**Handoffs**: Architect, Developer, Tech Lead

---

### Architect (`@architect`)
**Role**: System design and architecture planning

**Key Capabilities**:
- Design system architecture
- Create technical specifications
- Define integration patterns
- Select technology stack
- Plan scalability and performance

**Documentation**: [architect.agent.md](./archtiect.agent.md)

---

### Developer (`@developer`)
**Role**: Feature implementation following TDD and best practices

**Key Capabilities**:
- Implement features in Python and TypeScript/Node.js
- Write tests (unit, integration, E2E)
- Follow TDD methodology
- Code review and refactoring
- API development with Postman

**Documentation**: [developer.agent.md](./developer.agent.md)

**Handoffs**: QA

---

### Tech Lead (`@lead`)
**Role**: Technical leadership and coordination

**Key Capabilities**:
- Sprint planning and estimation
- Resource allocation
- Technical decision making
- Team coordination
- Risk management

**Documentation**: [lead.agent.md](./lead.agent.md)

---

## 🚀 Getting Started

### Basic Usage

1. Open VS Code Chat panel (Cmd/Ctrl + Shift + I)
2. Type `@` followed by agent name
3. Provide your request or question
4. Agent will analyze and respond with relevant output

### Example Workflow

```
User: @ba analyze requirements from pps/requirements/user_01.md

BA Agent: [Analyzes the file and provides comprehensive breakdown]
          [Click "Send to Architect" to continue]

User: [Clicks handoff button]

Architect: [Receives requirements and creates technical design]
           [Click "Send to Developer" to implement]

Developer: [Receives design and implements features]
           [Click "Send to QA" for testing]
```

## 🔄 Agent Collaboration

### Handoff System

Agents can seamlessly hand off work to each other:

```
BA → Architect → Developer → QA
     ↓
     Tech Lead (consulting)
```

**Methods**:
1. **Button-based**: Click handoff buttons in Chat UI
2. **Command-based**: Mention handoff in your prompt
   ```
   @ba analyze this then hand off to architect
   ```

### When to Use Each Agent

| Phase | Agent | Purpose |
|-------|-------|---------|
| Discovery | `@ba` | Analyze requirements, create user stories |
| Design | `@architect` | Design system architecture |
| Planning | `@lead` | Estimate effort, plan sprints |
| Implementation | `@developer` | Write code, run tests |
| Testing | `@qa` | Test features, validate quality |

## 🔧 Configuration

### Agent Definition Files

Each agent has a `.agent.md` file with:
- **Metadata**: name, description, tools, model
- **Handoffs**: available handoff targets
- **Instructions**: persona, responsibilities, best practices

### Configuration Structure

```
.vscode/
└── agents/
    ├── README.md                           # This file
    ├── ba.agent.md                         # BA Chat Participant
    ├── BA_CHAT_PARTICIPANT_GUIDE.md        # BA detailed guide
    ├── BA_QUICK_REFERENCE.md               # BA quick ref
    ├── architect.agent.md                  # Architect agent
    ├── developer.agent.md                  # Developer agent
    └── lead.agent.md                       # Tech Lead agent
```

### Related Configurations

- **Python Agents**: `/agents/*.py`
- **Agent Configs**: `/config/agents/*.yaml`
- **Prompts**: `/config/prompts/*_prompts.yaml`

## 🛠️ Customization

### Modifying Agent Behavior

1. **Edit Agent Definition**: Update `.agent.md` file
   - Change persona instructions
   - Add/remove tools
   - Modify handoff destinations

2. **Update Configuration**: Modify `config/agents/*.yaml`
   - Customize prompts
   - Adjust fallbacks
   - Change defaults

3. **Extend Python Agent**: Update `agents/*.py`
   - Add new methods
   - Integrate new tools
   - Enhance capabilities

### Adding New Agents

1. Create `[name].agent.md` in this directory
2. Define metadata, tools, and handoffs
3. Write detailed instructions
4. Create corresponding Python agent if needed
5. Update this README

## 📚 Tools Available to Agents

### Common Tools

- **search**: Search workspace files and documentation
- **githubRepo**: Access GitHub issues and pull requests
- **edit**: Edit files (Developer agent)
- **terminal**: Run commands (Developer agent)
- **run**: Execute code (Developer agent)
- **fetch**: Retrieve external data (Developer agent)

### Tool Usage

Agents automatically use appropriate tools based on context:
```
@ba search for existing authentication requirements
@developer run tests for the new feature
@architect check GitHub issues related to scalability
```

## 🎓 Best Practices

### Writing Effective Prompts

**✅ Good**:
```
@ba analyze requirements from pps/requirements/user_01.md and create user stories
@architect design REST API architecture for user management module
@developer implement login feature following TDD with pytest
```

**❌ Avoid**:
```
@ba help
@architect what should I do
@developer fix it
```

### Providing Context

- Reference specific files, tickets, or features
- Include relevant background information
- Specify desired output format
- Mention constraints or dependencies

### Leveraging Handoffs

- Use handoffs for natural workflow progression
- Include context when handing off
- Review handoff prompts for clarity
- Verify recipient agent capabilities

## 🐛 Troubleshooting

### Agent Not Responding

1. Verify GitHub Copilot is active
2. Check Chat panel is open
3. Ensure workspace contains agent configs
4. Try reloading VS Code window

### Tool Access Issues

1. Verify agent has required tools in `.agent.md`
2. Check workspace permissions
3. Review VS Code output panel for errors
4. Confirm file paths are correct

### Handoff Problems

1. Verify target agent exists
2. Check handoff configuration in `.agent.md`
3. Ensure handoff prompt is clear
4. Review Chat history for context

## 📖 Additional Resources

### Documentation

- [VS Code Chat Participant API](https://code.visualstudio.com/api/extension-guides/chat)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [AI Team Architecture](../../README.md)

### Related Files

- [Agent Framework](../../shared/agent_framework.py)
- [LLM Manager](../../shared/llm_manager.py)
- [Team Messaging](../../shared/team_messaging.py)

### Examples

- [BA Usage Examples](./BA_CHAT_PARTICIPANT_GUIDE.md#example-workflows)
- [Developer Workflows](./developer.agent.md)
- [Architecture Patterns](./archtiect.agent.md)

## 🤝 Contributing

### Adding Features

1. Update relevant `.agent.md` file
2. Modify Python agent if needed
3. Update configuration files
4. Add tests
5. Update documentation

### Reporting Issues

1. Check troubleshooting section
2. Review existing GitHub issues
3. Create new issue with:
   - Agent name
   - Expected behavior
   - Actual behavior
   - Steps to reproduce

---

**Last Updated**: November 22, 2025  
**Version**: 1.1.0  
**Maintainer**: AI Team

For questions or support, please create an issue in the repository.
