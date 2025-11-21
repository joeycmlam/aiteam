# Business Analyst Chat Participant Guide

## 🎯 Overview

The **Business Analyst (BA) Chat Participant** is an AI-powered assistant integrated into VS Code through the Chat Participant API. It specializes in requirements analysis, user story creation, and BDD scenario generation.

## 🚀 Getting Started

### Activation

To use the BA agent in VS Code, simply type:
```
@ba [your question or command]
```

The agent is automatically available in the VS Code Chat panel once the workspace is opened.

### Prerequisites

- VS Code with GitHub Copilot enabled
- Access to the workspace with the BA agent configuration
- JIRA credentials (optional, for JIRA integration)

## 📋 Key Features

### 1. Requirements Analysis
The BA agent can analyze requirements from various sources:

**Analyze JIRA tickets:**
```
@ba analyze JIRA ticket PROJ-123
```

**Analyze requirement documents:**
```
@ba analyze requirements from /pps/requirements/user_01.md
```

**Review requirements for quality:**
```
@ba validate these requirements: [paste requirements]
```

### 2. User Story Creation
Generate detailed user stories following INVEST principles:

**Create user stories:**
```
@ba create user stories for user authentication feature
```

**Convert requirements to stories:**
```
@ba convert these requirements into user stories with acceptance criteria
```

### 3. BDD Scenario Generation
Generate Gherkin feature files for testing:

**Generate scenarios:**
```
@ba create BDD scenarios for login functionality
```

**Create comprehensive feature file:**
```
@ba generate complete .feature file for the shopping cart
```

### 4. JIRA Integration
Work directly with JIRA initiatives and epics:

**Fetch and analyze initiative:**
```
@ba fetch JIRA initiative EPIC-456 and structure requirements
```

**Query JIRA tickets:**
```
@ba fetch JIRA tickets with JQL: project = MYPROJ AND status = "To Do"
```

## 🔄 Collaboration & Handoffs

The BA agent can seamlessly hand off work to other agents:

### Hand Off to Architect
After completing requirements analysis:
```
@ba analyze requirements then hand off to architect
```

Or use the built-in handoff button in the Chat UI.

### Hand Off to Developer
Once user stories are ready:
```
@ba create user stories and hand off to developer for implementation
```

### Consult Tech Lead
For technical feasibility or resource planning:
```
@ba validate these requirements and consult tech lead
```

## 💡 Example Workflows

### Workflow 1: Complete Requirements Analysis

```
1. @ba analyze requirements from requirements/feature_spec.md
2. [BA analyzes and provides comprehensive breakdown]
3. @ba create user stories based on this analysis
4. [BA generates detailed user stories with acceptance criteria]
5. @ba generate BDD scenarios for these user stories
6. [BA creates Gherkin feature files]
7. Click "Send to Architect" button to hand off for design
```

### Workflow 2: JIRA Initiative Processing

```
1. @ba fetch JIRA initiative EPIC-789
2. [BA retrieves initiative and all linked issues]
3. @ba structure requirements from this initiative
4. [BA creates structured user stories]
5. Click "Send to Developer" to start implementation
```

### Workflow 3: Requirements Validation

```
1. @ba validate these requirements: [paste raw requirements]
2. [BA reviews for completeness, clarity, testability]
3. @ba suggest improvements based on the validation
4. [BA provides actionable recommendations]
5. @ba create final user stories incorporating feedback
```

## 📝 Best Practices

### Writing Effective Prompts

**✅ Good Prompts:**
```
@ba analyze the user authentication requirements in user_01.md and create user stories with acceptance criteria
@ba generate BDD scenarios for the payment processing flow including error cases
@ba validate these requirements for completeness and testability
```

**❌ Avoid Vague Prompts:**
```
@ba help me with requirements
@ba create some stories
@ba look at this
```

### Providing Context

Always provide sufficient context:
- Reference specific files or JIRA tickets
- Include relevant background information
- Specify what output format you need
- Mention any constraints or dependencies

### Using Tools

The BA agent has access to:
- **search**: Search codebase and documentation
- **githubRepo**: Access GitHub issues and PRs

Example:
```
@ba search for existing authentication requirements in the codebase
@ba check GitHub issues related to user management
```

## 🎓 Capabilities Reference

### Requirements Analysis Outputs

When analyzing requirements, the BA agent provides:

1. **Business Objectives** - Clear, measurable goals
2. **Functional Requirements** - What the system must do
3. **Non-Functional Requirements** - Performance, security, scalability
4. **User Stories** - INVEST-compliant stories
5. **Acceptance Criteria** - Given-When-Then format
6. **Risks & Dependencies** - Potential challenges
7. **Out of Scope** - Explicit boundaries
8. **Assumptions** - Items needing validation

### User Story Format

Each user story includes:
```markdown
## User Story: [Title]

**As a** [role]
**I want** [feature]
**So that** [benefit]

### Acceptance Criteria
1. **Given** [context]
   **When** [action]
   **Then** [outcome]

### Priority: High/Medium/Low
### Complexity: [Story Points or Size]
### Dependencies: [List of dependencies]
### Notes: [Technical considerations]
```

### BDD Scenario Format

Generated feature files follow Gherkin syntax:
```gherkin
Feature: [Feature Name]
  [Feature description]
  
  Background:
    Given [common setup]
  
  Scenario: [Happy path]
    Given [precondition]
    When [action]
    Then [expected outcome]
  
  Scenario: [Alternative path]
    Given [different context]
    When [different action]
    Then [different outcome]
  
  Scenario: [Error handling]
    Given [error condition]
    When [trigger]
    Then [error response]
```

## 🔧 Configuration

### Agent Configuration Location

The BA agent is configured through multiple files:

1. **Chat Participant Definition**: `.vscode/agents/ba.agent.md`
   - Defines persona, tools, handoffs
   - Contains instructions and best practices

2. **Agent Configuration**: `config/agents/ba.yaml`
   - Unified config for VS Code and Python agent
   - Prompts, fallbacks, defaults

3. **Prompts Configuration**: `config/prompts/ba_agent_prompts.yaml`
   - Detailed prompt templates
   - System messages for different tasks

### Customizing Prompts

You can customize how the BA agent analyzes requirements by editing:
```yaml
# config/agents/ba.yaml

prompts:
  analyze_requirements:
    template: |
      [Your custom prompt template]
    system_message: |
      [Your custom system message]
```

### Adjusting Handoffs

Modify handoff destinations in `.vscode/agents/ba.agent.md`:
```yaml
handoffs:
  - label: Send to Architect
    agent: architect
    prompt: Design technical architecture based on these requirements
    send: false
```

## 🐛 Troubleshooting

### Agent Not Responding

1. Check VS Code Chat panel is open
2. Ensure GitHub Copilot is active
3. Verify workspace contains agent configuration files
4. Try reloading VS Code window

### JIRA Integration Issues

1. Verify JIRA credentials in environment variables
2. Check JIRA server URL is accessible
3. Confirm ticket/initiative keys are correct
4. Review JIRA permissions

### LLM Analysis Failures

The BA agent includes fallback templates when LLM is unavailable:
- Basic requirement templates
- Standard user story formats
- Minimal BDD scenarios

## 📚 Additional Resources

### Related Documentation

- [BA Agent Python Implementation](../../agents/ba_agent.py)
- [BA Configuration](../../config/agents/ba.yaml)
- [BA Prompts](../../config/prompts/ba_agent_prompts.yaml)
- [Agent Framework](../../shared/agent_framework.py)

### External Resources

- [VS Code Chat Participant API](https://code.visualstudio.com/api/extension-guides/chat)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/)
- [INVEST User Stories](https://en.wikipedia.org/wiki/INVEST_(mnemonic))
- [BDD Best Practices](https://cucumber.io/docs/bdd/)

## 🤝 Contributing

To extend the BA agent capabilities:

1. Update `.vscode/agents/ba.agent.md` for Chat Participant features
2. Modify `config/agents/ba.yaml` for configuration
3. Enhance `agents/ba_agent.py` for Python functionality
4. Add tests in `tests/` directory
5. Update this guide with new features

---

**Last Updated**: November 22, 2025
**Version**: 1.1.0
**Maintainer**: AI Team
