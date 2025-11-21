# Building GenAI Agents with VS Code & GitHub Copilot

## Available Options for Your Workflow

Your goal: **JIRA → BA Agent → Tech Lead Agent → Developer Agent**

---

## Option 1: VS Code Custom Agents (Interactive Chat)

### ✅ What You Get
- Interactive chat experience with `@BA`, `@TechLead`, `@Developer`
- Uses Claude Sonnet 4 via GitHub Copilot license
- Easy to create (just markdown files)
- No coding required

### ❌ Limitations
- **Cannot connect to JIRA API** - Custom agents can't make external API calls
- **No automation** - Manual handoff between agents
- **No file operations** - Can't read/write files programmatically
- **No tool access** - Limited to chat interactions only

### 📁 Structure
```bash
.github/agents/
├── BA.agent.md           # ✅ Already created
├── TechLead.agent.md     # Create this
├── Developer.agent.md    # Create this
```

### 💡 Use Case
Best for: **Interactive exploration, requirements clarification, getting suggestions**

**Example workflow:**
```
Developer: @BA analyze #file:requirements/user_requirement.md
BA Agent: [provides analysis]

Developer: @TechLead design system based on the above
TechLead Agent: [provides design]

Developer: @Developer implement the authentication module
Developer Agent: [provides code]
```

---

## Option 2: Python Automation Agents (Programmatic Workflow)

### ✅ What You Get
- **Full JIRA integration** via API
- **Automated workflow** - One command runs entire pipeline
- **File operations** - Reads/writes files automatically
- **Context passing** - Agents share data seamlessly
- **Customizable** - Full control over behavior

### ❌ Limitations
- Requires Python coding
- Uses GPT-4o (via GitHub Models API, not Claude)
- More setup required

### 📁 Structure (Just Created for You!)
```bash
aiteam/
├── agents/
│   ├── jira_agent.py          # ✅ NEW - JIRA integration
│   ├── ba_agent.py             # ✅ Exists
│   ├── tech_lead_agent.py      # ✅ Exists
│   ├── developer_agent.py      # Needs enhancement
│   └── lead_orchestrator.py    # ✅ Exists
├── workflows/
│   ├── enhanced_workflow.py    # ✅ NEW - JIRA→BA→TechLead→Dev
│   └── ai_workflow_orchestrated.py  # ✅ Exists (PPS project)
```

### 💡 Use Case
Best for: **Automated end-to-end workflows, production systems, batch processing**

**Example workflow:**
```bash
# One command runs entire pipeline
python workflows/enhanced_workflow.py \
  --jira PROJ-123 \
  --jira-url https://yourcompany.atlassian.net \
  --jira-email your@email.com \
  --jira-token YOUR_API_TOKEN

# Automatically:
# 1. Fetches JIRA issue
# 2. Checks completeness
# 3. Runs BA analysis
# 4. Runs Tech Lead design
# 5. Runs Developer implementation
```

---

## Option 3: Hybrid Approach (RECOMMENDED for Your Use Case)

### ✅ What You Get
- **JIRA Integration** via Python (automated fetch)
- **Interactive Design** via VS Code agents (Claude Sonnet 4)
- **Automated Workflows** when needed (batch processing)
- **Flexible** - Choose automation or interactive per step
- **Best of both models** - GPT-4o for automation, Claude for interaction

### 💡 Use Case
Best for: **Production workflows with human oversight, iterative design, flexible automation**

### 🔄 Three Hybrid Workflow Patterns

---

#### **Pattern A: Python Fetch → VS Code Interactive**

**When to use:** JIRA has the ticket, but you want interactive refinement

```bash
# Step 1: Fetch from JIRA (Python automation)
cd /Users/joeylam/repo/aiteam
python agents/jira_agent.py PROJ-123
# ✅ Output: requirements/PROJ_123_requirement.md

# Step 2: Open VS Code Chat (Cmd+Shift+I)
# Step 3: Interactive analysis with Claude
@BA analyze #file:requirements/PROJ_123_requirement.md
# → Copy/paste BA output to file if you want to save it

# Step 4: Interactive design
@TechLead design technical architecture based on the BA analysis above
# → Review, ask questions, iterate on design

# Step 5: Interactive implementation
@Developer implement the authentication module following tech lead design
# → Get code, review, ask for changes
```

**Pros:**
- ✅ Automated JIRA fetch (no manual copy-paste)
- ✅ Interactive refinement with Claude
- ✅ Human oversight at each step
- ✅ Can iterate and ask questions

**Cons:**
- 🟡 Manual copy-paste of chat outputs to files
- 🟡 Context doesn't auto-pass between agents

---

#### **Pattern B: Full Automation → VS Code Review**

**When to use:** Batch process multiple tickets, then review results

```bash
# Step 1: Run full automated pipeline (Python)
cd /Users/joeylam/repo/aiteam
python workflows/enhanced_workflow.py --jira PROJ-123

# ✅ Automatically generates:
# - requirements/PROJ_123_requirement.md
# - requirements/analysis/requirements_analysis.md
# - technical_structure/technical_structure.md
# - technical_structure/development_tasks.md

# Step 2: Review outputs in VS Code Chat
# Open Chat (Cmd+Shift+I)

# Review BA analysis
@BA review this requirements analysis and suggest improvements:
#file:requirements/analysis/requirements_analysis.md

# Review technical design
@TechLead review this technical structure and identify issues:
#file:technical_structure/technical_structure.md

# Get implementation guidance
@Developer what's the best way to implement this:
#file:technical_structure/development_tasks.md
```

**Pros:**
- ✅ Fast batch processing
- ✅ Automated file generation
- ✅ Context preserved in files
- ✅ Interactive review and refinement

**Cons:**
- 🟡 Less human oversight during generation
- 🟡 May need corrections after automation

---

#### **Pattern C: Step-by-Step Hybrid** (Most Control)

**When to use:** Complex projects needing oversight at each phase

```bash
# PHASE 1: JIRA Fetch (Automated)
cd /Users/joeylam/repo/aiteam
python agents/jira_agent.py PROJ-123
# ✅ requirements/PROJ_123_requirement.md created

# Check completeness
python -c "
from agents.jira_agent import JiraAgent
agent = JiraAgent()
issue = agent.fetch_issue('PROJ-123')
completeness = agent.analyze_completeness(issue)
print('Complete:', completeness['is_complete'])
print('Missing:', completeness['missing_fields'])
"

# PHASE 2: BA Analysis (Choose automation OR interactive)

# Option 2A: Automated BA
cd /Users/joeylam/repo/pps
python ai_workflow_orchestrated.py \
  --steps ba \
  --requirements requirements/PROJ_123_requirement.md

# Option 2B: Interactive BA
# Open VS Code Chat (Cmd+Shift+I)
@BA analyze #file:requirements/PROJ_123_requirement.md and create detailed analysis

# PHASE 3: Tech Lead Design (Choose automation OR interactive)

# Option 3A: Automated Tech Lead
python ai_workflow_orchestrated.py --steps tech_lead

# Option 3B: Interactive Tech Lead
@TechLead design system architecture based on #file:requirements/analysis/requirements_analysis.md

# PHASE 4: Developer Implementation (Interactive recommended)
@Developer implement authentication module following #file:technical_structure/technical_structure.md
```

**Pros:**
- ✅ Maximum flexibility
- ✅ Human oversight at decision points
- ✅ Choose automation vs interactive per step
- ✅ Can switch models (GPT-4o vs Claude) per task

**Cons:**
- 🟡 More manual coordination
- 🟡 Requires understanding of both systems

---

### 🛠️ Hybrid Setup Script

Create a helper script to make hybrid workflows easier:

```bash
# Create: ~/bin/ai-workflow.sh
#!/bin/bash

JIRA_KEY=$1
ACTION=${2:-"all"}

case $ACTION in
  fetch)
    echo "📥 Fetching JIRA issue $JIRA_KEY..."
    cd /Users/joeylam/repo/aiteam
    python agents/jira_agent.py $JIRA_KEY
    echo "✅ Done! File: requirements/${JIRA_KEY//-/_}_requirement.md"
    echo "💡 Next: Open VS Code Chat and run:"
    echo "   @BA analyze #file:requirements/${JIRA_KEY//-/_}_requirement.md"
    ;;
    
  auto-ba)
    echo "🤖 Running automated BA analysis..."
    cd /Users/joeylam/repo/pps
    python ai_workflow_orchestrated.py --steps ba \
      --requirements requirements/${JIRA_KEY//-/_}_requirement.md
    echo "✅ BA analysis complete!"
    echo "📄 Check: requirements/analysis/requirements_analysis.md"
    ;;
    
  auto-all)
    echo "🚀 Running full automated workflow..."
    cd /Users/joeylam/repo/aiteam
    python workflows/enhanced_workflow.py --jira $JIRA_KEY
    echo "✅ Full workflow complete!"
    ;;
    
  *)
    echo "Usage: ai-workflow.sh JIRA-KEY [fetch|auto-ba|auto-all]"
    echo ""
    echo "Examples:"
    echo "  ai-workflow.sh PROJ-123 fetch      # Fetch JIRA, then use @BA in chat"
    echo "  ai-workflow.sh PROJ-123 auto-ba    # Automated BA analysis"
    echo "  ai-workflow.sh PROJ-123 auto-all   # Full automation"
    ;;
esac
```

**Usage:**
```bash
# Make executable
chmod +x ~/bin/ai-workflow.sh

# Fetch JIRA, then use VS Code agents
ai-workflow.sh PROJ-123 fetch

# Run automated BA, then review in VS Code
ai-workflow.sh PROJ-123 auto-ba

# Full automation
ai-workflow.sh PROJ-123 auto-all
```

---

### 📊 When to Use Each Pattern

| Scenario | Recommended Pattern | Why |
|----------|-------------------|-----|
| **New feature from JIRA** | Pattern C (Step-by-Step) | Need oversight at each phase |
| **Urgent bug fix** | Pattern A (Fetch → Interactive) | Fast, interactive problem-solving |
| **Batch processing 10+ tickets** | Pattern B (Auto → Review) | Efficiency, bulk generation |
| **Complex system design** | Pattern C (Step-by-Step) | Maximum control and iteration |
| **Simple CRUD feature** | Pattern B (Auto → Review) | Standard pattern, less oversight needed |
| **Learning/exploring requirements** | Pattern A (Fetch → Interactive) | Interactive discovery with Claude |

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd /Users/joeylam/repo/aiteam
pip install jira python-dotenv
```

### 2. Configure JIRA Credentials

Create `.env` file:
```bash
# .env
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_jira_api_token
```

**How to get JIRA API token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy the token to `.env` file

### 3. Test JIRA Integration

```bash
# Set environment variables
export JIRA_URL="https://yourcompany.atlassian.net"
export JIRA_EMAIL="your@email.com"
export JIRA_API_TOKEN="your_token"

# Test fetching an issue
cd /Users/joeylam/repo/aiteam
python agents/jira_agent.py PROJ-123
```

### 4. Run Full Workflow

```bash
# From JIRA issue
python workflows/enhanced_workflow.py \
  --jira PROJ-123 \
  --jira-url $JIRA_URL \
  --jira-email $JIRA_EMAIL \
  --jira-token $JIRA_API_TOKEN

# Or from requirements file
python workflows/enhanced_workflow.py \
  --requirements requirements/user_requirement.md
```

---

## Comparison Table

| Feature | Custom Agents (@BA) | Python Automation | Hybrid |
|---------|-------------------|------------------|--------|
| **JIRA Integration** | ❌ No | ✅ Yes | ✅ Yes |
| **Automation** | ❌ Manual | ✅ Full | ⚡ Flexible |
| **LLM Model** | Claude Sonnet 4 | GPT-4o | Both |
| **Interactive** | ✅ Yes | ❌ No | ✅ Yes |
| **File Operations** | ❌ No | ✅ Yes | ✅ Yes |
| **Coding Required** | ❌ No | ✅ Yes | 🟡 Minimal |
| **Context Passing** | 🟡 Manual | ✅ Automatic | ⚡ Both |
| **Setup Time** | ⚡ 5 min | 🟡 30 min | 🟡 20 min |

---

## Recommended Workflow for Your Use Case

Based on your requirements:
1. ✅ Get JIRA number → **Python JIRA Agent**
2. ✅ Connect to JIRA → **Python JIRA Agent**
3. ✅ Analyze requirements → **Python BA Agent or @BA in chat**
4. ✅ Check if sufficient → **Python automated check**
5. ✅ Pass to Tech Lead → **Python Tech Lead Agent or @TechLead**
6. ✅ Design system/flows → **Python Tech Lead Agent or @TechLead**
7. ✅ Pass to Developer → **Python Developer Agent or @Developer**
8. ✅ Build implementation → **Python Developer Agent or @Developer**

**Recommendation:** Use **Python Automation** for the full workflow with JIRA integration.

---

## Quick Start Commands

```bash
# 1. Install dependencies
cd /Users/joeylam/repo/aiteam
pip install jira python-dotenv

# 2. Set up credentials (add to ~/.bashrc or ~/.zshrc)
export JIRA_URL="https://yourcompany.atlassian.net"
export JIRA_EMAIL="your@email.com"  
export JIRA_API_TOKEN="your_api_token"

# 3. Test JIRA connection
python agents/jira_agent.py YOUR-JIRA-KEY

# 4. Run full workflow
python workflows/enhanced_workflow.py --jira YOUR-JIRA-KEY

# 5. Or use in PPS project
cd /Users/joeylam/repo/pps
python ai_workflow_orchestrated.py --steps ba architect tech_lead
```

---

## Next Steps

1. **Test JIRA Agent**: `python agents/jira_agent.py PROJ-123`
2. **Create .env file** with your JIRA credentials
3. **Run enhanced workflow**: `python workflows/enhanced_workflow.py --jira PROJ-123`
4. **Create more VS Code agents** (TechLead.agent.md, Developer.agent.md) for interactive use
5. **Enhance Developer Agent** to generate actual code

---

## Files Created for You

✅ `/Users/joeylam/repo/aiteam/agents/jira_agent.py` - JIRA integration
✅ `/Users/joeylam/repo/aiteam/workflows/enhanced_workflow.py` - Full orchestration
✅ `/Users/joeylam/repo/aiteam/doc/GENAI_AGENT_OPTIONS.md` - This guide

Ready to test? Start with:
```bash
cd /Users/joeylam/repo/aiteam
python agents/jira_agent.py --help
```
