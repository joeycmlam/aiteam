# Agent Prompts Configuration

This directory contains externalized prompt templates for AI agents, making them easy to customize without modifying code.

## Overview

All AI agent prompts are now stored in YAML configuration files, allowing you to:
- ✅ Customize prompts without changing code
- ✅ Version control prompt changes separately
- ✅ A/B test different prompt variations
- ✅ Share prompts across teams
- ✅ Maintain consistency across agents

## Files

### `ba_agent_prompts.yaml`
Prompts for the Business Analyst Agent, including:
- **extract_requirements** - Extract structured requirements from JIRA tickets
- **analyze_initiative** - Analyze JIRA initiatives/epics
- **analyze_requirements** - Comprehensive requirements analysis
- **generate_scenarios** - Generate BDD/Gherkin scenarios
- **fallbacks** - Templates when AI is unavailable
- **defaults** - Default values for extracted data

## Configuration Structure

```yaml
prompt_name:
  template: |
    Your prompt template here.
    Use {variable_name} for placeholders.
  
  system_message: "Instructions for the AI model"
  
  # Optional settings
  max_content_length: 3000
  max_analysis_length: 2000
```

## Usage

### Default Usage (Automatic)
The BA Agent automatically loads prompts from this directory:

```python
from agents.ba_agent import BAAgent

# Automatically loads config/prompts/ba_agent_prompts.yaml
ba = BAAgent(llm_config, jira_config)
```

### Custom Prompts File
Use a different prompts file:

```python
ba = BAAgent(
    llm_config, 
    jira_config,
    prompts_config_path='/path/to/custom_prompts.yaml'
)
```

## Customization Examples

### Example 1: Change Requirements Analysis Format

Edit `ba_agent_prompts.yaml`:

```yaml
analyze_requirements:
  template: |
    Analyze the following requirements in AGILE format:
    
    RAW REQUIREMENTS:
    {raw_content}
    
    Provide:
    1. **Epics** (High-level features)
    2. **User Stories** (Format: As a <role>, I want <feature>, so that <benefit>)
    3. **Tasks** (Detailed implementation steps)
    4. **Definition of Done** (Acceptance criteria)
    
    Use bullet points and keep it concise.
  
  system_message: "You are an Agile coach helping to structure requirements."
```

### Example 2: Add Domain-Specific Instructions

For a financial services project:

```yaml
extract_requirements:
  template: |
    Extract structured requirements from this JIRA ticket:
    
    ID: {ticket_id}
    Summary: {summary}
    Description: {description}
    
    Extract:
    1. Core business requirement
    2. Regulatory compliance considerations
    3. Security requirements
    4. Audit trail needs
    5. Acceptance criteria (Given-When-Then format)
    
    Format as JSON.
  
  system_message: "You are a business analyst specializing in financial services and regulatory compliance."
```

### Example 3: Change Scenario Generation Style

For mobile app testing:

```yaml
generate_scenarios:
  template: |
    Create mobile app test scenarios in Gherkin format.
    
    ANALYSIS:
    {analysis}
    
    Create scenarios covering:
    1. Happy path on iOS and Android
    2. Offline mode behavior
    3. Network interruption handling
    4. Device rotation scenarios
    5. Push notification handling
    
    Use tags: @ios, @android, @offline, @critical
  
  system_message: "You are a mobile QA expert specializing in cross-platform testing."
```

### Example 4: Customize Default Values

Change default acceptance criteria:

```yaml
defaults:
  acceptance_criteria:
    - "Feature works as specified"
    - "Unit tests pass with >90% coverage"
    - "Integration tests pass"
    - "Security scan shows no vulnerabilities"
    - "Performance benchmarks met"
    - "Code review approved by 2+ reviewers"
    - "Documentation updated"
```

## Variables Reference

### Common Variables in Templates

| Variable | Description | Example |
|----------|-------------|---------|
| `{ticket_id}` | JIRA ticket ID | "SCRUM-123" |
| `{summary}` | Ticket summary/title | "Implement user login" |
| `{description}` | Full description | "As a user, I want..." |
| `{issue_type}` | Type of issue | "Story", "Epic", "Task" |
| `{linked_count}` | Number of linked issues | 5 |
| `{raw_content}` | Raw requirement text | Full requirements doc |
| `{analysis}` | AI analysis output | Structured analysis |

## Best Practices

### 1. **Be Specific**
```yaml
# ❌ Bad - Too vague
system_message: "You are helpful."

# ✅ Good - Specific role
system_message: "You are a senior business analyst with 10 years experience in enterprise software requirements engineering."
```

### 2. **Use Structured Output**
```yaml
# ✅ Good - Request specific format
template: |
  Extract requirements and format as JSON:
  {
    "business_need": "...",
    "acceptance_criteria": ["...", "..."],
    "assumptions": ["...", "..."]
  }
```

### 3. **Limit Input Length**
```yaml
# ✅ Good - Prevent token overflow
analyze_requirements:
  max_content_length: 3000  # Truncate to 3000 chars
```

### 4. **Provide Examples**
```yaml
template: |
  Extract user stories in this format:
  
  Example:
  As a customer, I want to reset my password so that I can regain access.
  
  Now extract from:
  {description}
```

### 5. **Version Your Prompts**
```bash
# Create dated versions for A/B testing
config/prompts/
  ba_agent_prompts.yaml          # Current version
  ba_agent_prompts_v1.yaml       # Previous version
  ba_agent_prompts_experimental.yaml  # Testing new approach
```

## Testing Prompt Changes

### 1. Test with Sample Data
```python
# test_prompts.py
from agents.ba_agent import BAAgent

# Test with your custom prompts
ba = BAAgent(llm_config, jira_config, 
             prompts_config_path='config/prompts/ba_agent_prompts_experimental.yaml')

# Run on sample ticket
result = ba.structure_requirements(sample_tickets)
print(result)
```

### 2. Compare Results
```bash
# Compare old vs new prompts
python3 test_prompts.py --prompts=ba_agent_prompts.yaml > output_old.txt
python3 test_prompts.py --prompts=ba_agent_prompts_experimental.yaml > output_new.txt
diff output_old.txt output_new.txt
```

## Troubleshooting

### Prompt Not Loading
```python
# Check if prompts loaded successfully
ba = BAAgent(llm_config, jira_config)
print(ba.prompts)  # Should show loaded prompts

# If empty, check file path
import os
path = 'config/prompts/ba_agent_prompts.yaml'
print(f"File exists: {os.path.exists(path)}")
```

### Template Variables Not Replaced
```yaml
# ❌ Wrong - Using $ instead of {}
template: "Analyze $raw_content"

# ✅ Correct - Use curly braces
template: "Analyze {raw_content}"
```

### YAML Syntax Errors
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config/prompts/ba_agent_prompts.yaml'))"
```

## Future Enhancements

- [ ] Add prompts for other agents (Architect, QA, Developer, Senior Dev)
- [ ] Create prompt templates library
- [ ] Add multi-language support
- [ ] Implement prompt versioning system
- [ ] Add prompt performance metrics
- [ ] Create prompt testing framework

## Contributing

When modifying prompts:
1. Test thoroughly with sample data
2. Document changes in git commit messages
3. Consider creating a new version instead of overwriting
4. Share successful prompt improvements with the team

## Support

For questions or issues with prompts:
- Check this README first
- Review example prompts in this directory
- Test with simple examples before complex ones
- Document what worked and what didn't
