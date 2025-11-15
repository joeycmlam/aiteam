# AI Team - Project Architecture

This document explains the AI-powered legacy code migration system using Mermaid diagrams.

## System Overview

```mermaid
flowchart TB
    subgraph "User Interface"
        USER["👤 Developer"]
        CLI["🖥️ Command Line"]
    end
    
    subgraph "Entry Points"
        PIPELINE["workflows/migration_pipeline.py<br/>Main Orchestrator"]
        TEST_LLM["test_llm.py<br/>Test LLM Connection"]
        TEST_MODELS["test_model_switching.py<br/>Test Model Switching"]
    end
    
    subgraph "Configuration"
        ENV[".env<br/>🔐 API Keys & Tokens"]
        CONFIG["config/agent_config.yaml<br/>⚙️ Agent Settings"]
    end
    
    subgraph "LLM Providers"
        GITHUB["GitHub Models API<br/>☁️ gpt-4o, gpt-4o-mini<br/>mistral-large"]
        OLLAMA["Ollama (Local)<br/>💻 llama3.2, qwen2.5"]
    end
    
    subgraph "Core System"
        LLM_MGR["shared/llm_manager.py<br/>🧠 LLM Manager<br/>Dynamic Model Switching"]
        MEMORY["shared/memory_store.py<br/>💾 Shared Memory<br/>JSON Persistence"]
    end
    
    subgraph "AI Agents"
        LEAD["agents/lead_orchestrator.py<br/>🎯 Lead Orchestrator<br/>Workflow Coordinator"]
        ARCHITECT["agents/architect_agent.py<br/>🏗️ Architect Agent<br/>Architecture Analysis"]
        BA["agents/ba_agent.py<br/>📋 BA Agent<br/>Requirements Processing"]
        QA["agents/qa_agent.py<br/>🧪 QA Agent<br/>Test Generation"]
        SENIOR["agents/senior_dev_agent.py<br/>👨‍💼 Senior Dev Agent<br/>Code Review"]
        DEV["agents/developer_agent.py<br/>👨‍💻 Developer Agent<br/>Code Implementation"]
    end
    
    subgraph "Data Sources"
        JIRA["📊 JIRA API<br/>Tickets & Requirements"]
        LEGACY["tests/fixtures/<br/>📁 Legacy Code"]
    end
    
    subgraph "Outputs"
        TESTS["tests/features/<br/>✅ Generated Tests"]
        CODE["generated_code/<br/>💻 New Implementation"]
        REPORTS["📄 Analysis Reports"]
    end
    
    USER --> CLI
    CLI --> PIPELINE
    CLI --> TEST_LLM
    CLI --> TEST_MODELS
    
    PIPELINE --> CONFIG
    PIPELINE --> ENV
    PIPELINE --> LEAD
    
    LEAD --> LLM_MGR
    LEAD --> MEMORY
    LEAD --> ARCHITECT
    LEAD --> BA
    LEAD --> QA
    LEAD --> SENIOR
    LEAD --> DEV
    
    ARCHITECT --> LLM_MGR
    BA --> LLM_MGR
    QA --> LLM_MGR
    SENIOR --> LLM_MGR
    DEV --> LLM_MGR
    
    LLM_MGR --> GITHUB
    LLM_MGR --> OLLAMA
    
    BA --> JIRA
    ARCHITECT --> LEGACY
    DEV --> LEGACY
    
    QA --> TESTS
    DEV --> CODE
    ARCHITECT --> REPORTS
    SENIOR --> REPORTS
    
    CONFIG -.-> LLM_MGR
    ENV -.-> GITHUB
    
    style USER fill:#e1f5ff
    style GITHUB fill:#fff3cd
    style OLLAMA fill:#d4edda
    style LLM_MGR fill:#f8d7da
    style LEAD fill:#d1ecf1
    style PIPELINE fill:#d1ecf1
```

## Workflow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Pipeline as Migration Pipeline
    participant Lead as Lead Orchestrator
    participant BA as BA Agent
    participant Arch as Architect Agent
    participant QA as QA Agent
    participant Dev as Developer Agent
    participant Senior as Senior Dev Agent
    participant LLM as LLM Manager
    participant Memory as Shared Memory
    
    User->>Pipeline: Run migration_pipeline.py
    activate Pipeline
    
    Pipeline->>Lead: Initialize workflow
    activate Lead
    
    Lead->>Memory: Create workflow state
    Memory-->>Lead: Workflow created
    
    Lead->>BA: Get JIRA tickets
    activate BA
    BA->>LLM: Analyze requirements
    LLM-->>BA: Requirements breakdown
    BA->>Memory: Store requirements
    BA-->>Lead: Requirements ready
    deactivate BA
    
    Lead->>Arch: Analyze legacy code
    activate Arch
    Arch->>LLM: Analyze architecture
    LLM-->>Arch: Architecture insights
    Arch->>Memory: Store architecture analysis
    Arch-->>Lead: Architecture analyzed
    deactivate Arch
    
    Lead->>QA: Generate test cases
    activate QA
    QA->>Memory: Get requirements & architecture
    QA->>LLM: Generate tests
    LLM-->>QA: Test specifications
    QA->>Memory: Store test cases
    QA-->>Lead: Tests generated
    deactivate QA
    
    Lead->>Dev: Implement new code
    activate Dev
    Dev->>Memory: Get all context
    Dev->>LLM: Generate implementation
    LLM-->>Dev: Code implementation
    Dev->>Memory: Store implementation
    Dev-->>Lead: Code implemented
    deactivate Dev
    
    Lead->>Senior: Review code
    activate Senior
    Senior->>Memory: Get implementation
    Senior->>LLM: Review code
    LLM-->>Senior: Review feedback
    Senior->>Memory: Store review
    Senior-->>Lead: Review complete
    deactivate Senior
    
    Lead-->>Pipeline: Workflow complete
    deactivate Lead
    
    Pipeline-->>User: Migration complete ✅
    deactivate Pipeline
```

## LLM Manager - Model Switching

```mermaid
flowchart LR
    subgraph "Initialization"
        INIT["LLMManager()<br/>provider, model"]
    end
    
    subgraph "Model Selection"
        DEFAULT["Default Model<br/>from __init__"]
        OVERRIDE["Per-Request Override<br/>model parameter"]
        SELECTED["Selected Model"]
    end
    
    subgraph "API Calls"
        GITHUB_CALL["GitHub Models API<br/>gpt-4o<br/>gpt-4o-mini<br/>mistral-large"]
        OLLAMA_CALL["Ollama API<br/>llama3.2<br/>qwen2.5<br/>mistral"]
    end
    
    subgraph "Error Handling"
        ERROR["API Error?"]
        FALLBACK["Automatic Fallback<br/>to Ollama"]
    end
    
    subgraph "Response"
        RESULT["AI Response"]
    end
    
    INIT --> DEFAULT
    DEFAULT --> SELECTED
    OVERRIDE -.Override.-> SELECTED
    
    SELECTED --> GITHUB_CALL
    SELECTED --> OLLAMA_CALL
    
    GITHUB_CALL --> ERROR
    ERROR -->|Yes| FALLBACK
    ERROR -->|No| RESULT
    FALLBACK --> OLLAMA_CALL
    OLLAMA_CALL --> RESULT
    
    style INIT fill:#d1ecf1
    style OVERRIDE fill:#fff3cd
    style SELECTED fill:#d4edda
    style GITHUB_CALL fill:#e1f5ff
    style OLLAMA_CALL fill:#d4edda
    style FALLBACK fill:#f8d7da
    style RESULT fill:#d4edda
```

## Agent Workflow States

```mermaid
stateDiagram-v2
    [*] --> Initialized: Create workflow
    
    Initialized --> RequirementsGathering: Start pipeline
    
    RequirementsGathering --> ArchitectureAnalysis: BA Agent completes
    note right of RequirementsGathering
        BA Agent:
        - Fetch JIRA tickets
        - Parse requirements
        - Store in memory
    end note
    
    ArchitectureAnalysis --> TestDesign: Architect Agent completes
    note right of ArchitectureAnalysis
        Architect Agent:
        - Analyze legacy code
        - Identify patterns
        - Recommend architecture
    end note
    
    TestDesign --> Implementation: QA Agent completes
    note right of TestDesign
        QA Agent:
        - Generate test cases
        - Create test files
        - Define acceptance criteria
    end note
    
    Implementation --> CodeReview: Developer Agent completes
    note right of Implementation
        Developer Agent:
        - Generate new code
        - Follow architecture
        - Pass all tests
    end note
    
    CodeReview --> Completed: Senior Dev Agent completes
    note right of CodeReview
        Senior Dev Agent:
        - Review implementation
        - Check best practices
        - Suggest improvements
    end note
    
    CodeReview --> Implementation: Changes required
    
    Completed --> [*]
```

## File Structure

```mermaid
flowchart TB
    subgraph "Project Root"
        ROOT["📁 /Users/joeylam/repo/aiteam/"]
    end
    
    subgraph "Configuration Files"
        ENV_FILE[".env<br/>🔐 GITHUB_TOKEN<br/>JIRA_API_TOKEN"]
        CONFIG_FILE["config/agent_config.yaml<br/>⚙️ LLM settings<br/>Workflow config"]
        REQ_FILE["requirements.txt<br/>📦 Dependencies"]
    end
    
    subgraph "Core Modules"
        SHARED["📁 shared/"]
        LLM_PY["llm_manager.py<br/>🧠 Model switching"]
        MEMORY_PY["memory_store.py<br/>💾 JSON persistence"]
    end
    
    subgraph "Agent Modules"
        AGENTS["📁 agents/"]
        LEAD_PY["lead_orchestrator.py"]
        ARCH_PY["architect_agent.py"]
        BA_PY["ba_agent.py"]
        QA_PY["qa_agent.py"]
        SENIOR_PY["senior_dev_agent.py"]
        DEV_PY["developer_agent.py"]
    end
    
    subgraph "Workflows"
        WORKFLOWS["📁 workflows/"]
        PIPE_PY["migration_pipeline.py<br/>🚀 Main entry point"]
    end
    
    subgraph "Test Files"
        TESTS["📁 tests/"]
        FIXTURES["fixtures/<br/>📁 Legacy code"]
        FEATURES["features/<br/>📁 Generated tests"]
    end
    
    subgraph "Test Scripts"
        TEST_LLM_PY["test_llm.py<br/>✅ Test connection"]
        TEST_MODELS_PY["test_model_switching.py<br/>✅ Test switching"]
        TEST_CLAUDE["test_claude_models.py<br/>✅ Check Claude"]
    end
    
    ROOT --> ENV_FILE
    ROOT --> CONFIG_FILE
    ROOT --> REQ_FILE
    ROOT --> SHARED
    ROOT --> AGENTS
    ROOT --> WORKFLOWS
    ROOT --> TESTS
    ROOT --> TEST_LLM_PY
    ROOT --> TEST_MODELS_PY
    ROOT --> TEST_CLAUDE
    
    SHARED --> LLM_PY
    SHARED --> MEMORY_PY
    
    AGENTS --> LEAD_PY
    AGENTS --> ARCH_PY
    AGENTS --> BA_PY
    AGENTS --> QA_PY
    AGENTS --> SENIOR_PY
    AGENTS --> DEV_PY
    
    WORKFLOWS --> PIPE_PY
    
    TESTS --> FIXTURES
    TESTS --> FEATURES
    
    style ROOT fill:#e1f5ff
    style SHARED fill:#fff3cd
    style AGENTS fill:#d4edda
    style WORKFLOWS fill:#f8d7da
    style TESTS fill:#d1ecf1
```

## Data Flow

```mermaid
flowchart LR
    subgraph "Input Sources"
        JIRA_IN["📊 JIRA Tickets"]
        LEGACY_IN["📁 Legacy Code<br/>tests/fixtures/"]
    end
    
    subgraph "Processing Layer"
        BA_PROC["BA Agent<br/>Requirements"]
        ARCH_PROC["Architect Agent<br/>Analysis"]
        QA_PROC["QA Agent<br/>Test Design"]
        DEV_PROC["Developer Agent<br/>Implementation"]
        SENIOR_PROC["Senior Dev Agent<br/>Review"]
    end
    
    subgraph "Memory Store"
        MEM_REQ["Requirements"]
        MEM_ARCH["Architecture"]
        MEM_TESTS["Test Cases"]
        MEM_CODE["Implementation"]
        MEM_REVIEW["Review Feedback"]
    end
    
    subgraph "Output Artifacts"
        OUT_TESTS["✅ Test Files<br/>tests/features/"]
        OUT_CODE["💻 New Code<br/>generated_code/"]
        OUT_REPORTS["📄 Reports"]
    end
    
    JIRA_IN --> BA_PROC
    LEGACY_IN --> ARCH_PROC
    
    BA_PROC --> MEM_REQ
    ARCH_PROC --> MEM_ARCH
    
    MEM_REQ --> QA_PROC
    MEM_ARCH --> QA_PROC
    QA_PROC --> MEM_TESTS
    
    MEM_REQ --> DEV_PROC
    MEM_ARCH --> DEV_PROC
    MEM_TESTS --> DEV_PROC
    DEV_PROC --> MEM_CODE
    
    MEM_CODE --> SENIOR_PROC
    SENIOR_PROC --> MEM_REVIEW
    
    MEM_TESTS --> OUT_TESTS
    MEM_CODE --> OUT_CODE
    MEM_ARCH --> OUT_REPORTS
    MEM_REVIEW --> OUT_REPORTS
    
    style JIRA_IN fill:#e1f5ff
    style LEGACY_IN fill:#e1f5ff
    style MEM_REQ fill:#fff3cd
    style MEM_ARCH fill:#fff3cd
    style MEM_TESTS fill:#fff3cd
    style MEM_CODE fill:#fff3cd
    style MEM_REVIEW fill:#fff3cd
    style OUT_TESTS fill:#d4edda
    style OUT_CODE fill:#d4edda
    style OUT_REPORTS fill:#d4edda
```

## Key Features

### 🎯 Dynamic Model Switching
- **Initialize with default model**: `LLMManager("github_copilot_cli", model="gpt-4o")`
- **Override per request**: `llm.generate(prompt, model="gpt-4o-mini")`
- **Automatic fallback**: GitHub Models → Ollama (if API fails)

### 🤖 Six Specialized AI Agents
1. **Lead Orchestrator**: Coordinates entire workflow
2. **Architect Agent**: Analyzes legacy code architecture
3. **BA Agent**: Processes JIRA tickets and requirements
4. **QA Agent**: Generates comprehensive test cases
5. **Developer Agent**: Implements new code
6. **Senior Dev Agent**: Reviews and validates code

### 💾 Shared Memory System
- Persistent JSON storage
- Cross-agent data sharing
- Workflow state management
- Timestamped entries

### ☁️ Dual LLM Support
- **GitHub Models API**: GPT-4o, GPT-4o-mini, Mistral-large
- **Ollama (Local)**: llama3.2, qwen2.5, mistral (unlimited, free)

### ⚙️ Configurable Workflow
- YAML-based configuration
- Environment variable support
- Parallel processing options
- Retry mechanisms

## Quick Start Commands

```bash
# Run full migration pipeline
python3 workflows/migration_pipeline.py

# Test LLM connection
python3 test_llm.py

# Test model switching
python3 test_model_switching.py

# Check Claude models availability
python3 test_claude_models.py
```

## Environment Variables

```bash
# Required for GitHub Models API
GITHUB_TOKEN=ghp_your_token_here

# Optional for JIRA integration
JIRA_API_TOKEN=your_jira_token

# Optional model defaults
GITHUB_MODEL=gpt-4o
OLLAMA_MODEL=llama3.2
LLM_PROVIDER=github_copilot_cli
```

---

**📚 For more information, see:**
- `README_START_HERE.md` - Getting started guide
- `MODEL_SWITCHING_GUIDE.md` - Model switching documentation (if exists)
- `GITHUB_MODELS_SETUP.md` - GitHub Models API setup
