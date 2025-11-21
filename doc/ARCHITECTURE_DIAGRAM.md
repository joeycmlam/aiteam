# AITeam Architecture with Claude Integration

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AITeam Framework                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   BA Agent   │  │ Tech Lead    │  │ Architect    │         │
│  │              │  │   Agent      │  │   Agent      │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                  │
│         └─────────────────┴──────────────────┘                  │
│                           │                                     │
│                  ┌────────▼────────┐                           │
│                  │  LLM Manager    │                           │
│                  │  (Routing Layer)│                           │
│                  └────────┬────────┘                           │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                 │
│         │                 │                 │                  │
│    ┌────▼─────┐    ┌─────▼──────┐    ┌────▼──────┐          │
│    │ Anthropic│    │   GitHub   │    │  Ollama   │          │
│    │  Claude  │    │   Models   │    │  (Local)  │          │
│    │          │    │            │    │           │          │
│    │ Sonnet 4 │    │   GPT-4o   │    │ llama3.2  │          │
│    │ 3.5      │    │ 4o-mini    │    │ qwen2.5   │          │
│    │ Opus     │    │ mistral    │    │ mistral   │          │
│    │ Haiku    │    │            │    │           │          │
│    └──────────┘    └────────────┘    └───────────┘          │
│         │                 │                 │                  │
│         │                 │                 │                  │
│    [Cloud API]      [Cloud API]       [Local Host]           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## LLM Manager Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────────┐
│         LLM Manager                      │
│   (shared/llm_manager.py)               │
└─────────────────────────────────────────┘
     │
     ▼
Check LLM_PROVIDER
     │
     ├─── "anthropic" ───────┐
     │                        ▼
     │              ┌──────────────────────┐
     │              │ _generate_with_      │
     │              │   anthropic()        │
     │              │                      │
     │              │ • Check API key      │
     │              │ • Build messages     │
     │              │ • Call Claude API    │
     │              │ • Handle errors      │
     │              │ • Fallback if needed │
     │              └──────────────────────┘
     │                        │
     ├─── "github_copilot_cli" ─┤
     │                        ▼
     │              ┌──────────────────────┐
     │              │ _generate_with_      │
     │              │   github_copilot_    │
     │              │   cli()              │
     │              └──────────────────────┘
     │                        │
     └─── "ollama" ──────────┤
                             ▼
                    ┌──────────────────────┐
                    │ _generate_with_      │
                    │   ollama()           │
                    └──────────────────────┘
                             │
                             ▼
                      Return Response
```

## Configuration Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    Environment Setup                          │
└──────────────────────────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         .env file    agent_config.yaml   Code
              │              │              │
              ▼              ▼              ▼
    ANTHROPIC_API_KEY   llm.provider   LLMManager(
    ANTHROPIC_MODEL     llm.model       provider="anthropic",
    LLM_PROVIDER                        model="claude-..."
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                      LLM Manager
                             │
                             ▼
                   Selected Provider
```

## Model Selection Logic

```
Request with model parameter?
     │
     ├─ YES ────► Use specified model
     │
     └─ NO ─────► Use default model from:
                  1. Constructor parameter
                  2. Environment variable
                  3. Hardcoded default

Example:
llm = LLMManager(provider="anthropic")  # Uses ANTHROPIC_MODEL from .env

llm.generate(prompt, model="claude-3-haiku-20240307")  # Overrides
```

## Agent Integration

```
┌──────────────────────────────────────────────────────────┐
│                   Agent (BA, Tech Lead, etc.)             │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  def process(self, input_data):                          │
│      llm = LLMManager()  # Uses env config               │
│      response = llm.generate(                            │
│          prompt=self.build_prompt(input_data),           │
│          system_message=self.system_prompt               │
│      )                                                    │
│      return self.process_response(response)              │
│                                                           │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
                     LLM Manager
                            │
                ┌───────────┼───────────┐
                │           │           │
           Anthropic    GitHub     Ollama
```

## Workflow Example

```
User runs: python3 agents/ba_agent.py --input requirements.md

┌─────────────────────────────────────────────────────────┐
│ Step 1: Load Environment                                 │
│   • Read .env file                                       │
│   • LLM_PROVIDER = anthropic                            │
│   • ANTHROPIC_MODEL = claude-sonnet-4-20250514          │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Initialize BA Agent                              │
│   • Load agent config                                    │
│   • Initialize LLM Manager                               │
│   • LLM Manager detects "anthropic" provider            │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Process Requirements                             │
│   • Read requirements.md                                 │
│   • Build analysis prompt                                │
│   • Call llm.generate(prompt)                           │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: LLM Manager Routes to Claude                     │
│   • Check ANTHROPIC_API_KEY                             │
│   • Initialize Anthropic client                          │
│   • Call claude-sonnet-4-20250514                       │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Process Response                                 │
│   • Receive Claude response                              │
│   • Format output                                        │
│   • Save to output/ba_analysis.md                       │
└─────────────────────────────────────────────────────────┘
```

## Error Handling & Fallback

```
Claude API Call
     │
     ▼
  Success? ─── YES ──► Return response
     │
     NO
     │
     ▼
Check Error Type
     │
     ├─ AuthenticationError
     │  └─► Print: "API key invalid"
     │      └─► Fallback to Ollama
     │
     ├─ RateLimitError
     │  └─► Print: "Rate limit exceeded"
     │      └─► Fallback to Ollama
     │
     └─ APIError / Other
        └─► Print: Error message
            └─► Fallback to Ollama
                     │
                     ▼
              Ollama Available?
                     │
                ┌────┴────┐
               YES        NO
                │          │
                ▼          ▼
         Use Ollama   Return error message
```

## File Structure Impact

```
aiteam/
├── shared/
│   └── llm_manager.py ──────────► [MODIFIED] Added Claude support
│
├── config/
│   └── agent_config.yaml ───────► [MODIFIED] Added model docs
│
├── tests/
│   └── test_claude.py ──────────► [NEW] Claude test suite
│
├── doc/
│   └── CLAUDE_INTEGRATION.md ───► [NEW] Full documentation
│
├── .env ────────────────────────► [MODIFIED] Added Claude config
│
├── requirements.txt ────────────► [MODIFIED] Added anthropic
│
├── README.md ───────────────────► [NEW] Project overview
│
├── CLAUDE_QUICKSTART.md ────────► [NEW] Quick start
│
└── CLAUDE_IMPLEMENTATION_       ► [NEW] Technical details
    SUMMARY.md
```

## Provider Comparison Matrix

```
┌────────────────────┬─────────────┬──────────────┬──────────────┐
│                    │  Anthropic  │   GitHub     │   Ollama     │
│                    │   Claude    │   Models     │   (Local)    │
├────────────────────┼─────────────┼──────────────┼──────────────┤
│ Setup Complexity   │    Easy     │    Easy      │   Medium     │
│ Cost               │ Pay-per-use │   Included   │    Free      │
│ Privacy            │   Cloud     │    Cloud     │   Local      │
│ Speed              │    Fast     │    Fast      │   Variable   │
│ Quality            │  Excellent  │  Excellent   │    Good      │
│ Internet Required  │     Yes     │     Yes      │     No       │
│ Best For           │  Reasoning  │    Code      │    Dev       │
└────────────────────┴─────────────┴──────────────┴──────────────┘
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    Existing Agents                           │
│  • BusinessAnalystAgent                                      │
│  • TechLeadAgent                                            │
│  • ArchitectAgent                                           │
│  • EnhancedDeveloperAgent                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ No code changes needed!
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Manager                               │
│  • Automatically uses provider from .env                     │
│  • Supports all three providers                             │
│  • Transparent to agents                                    │
└─────────────────────────────────────────────────────────────┘
```

---

**Key Points:**

1. ✅ **Zero Changes Required** - Existing agents work unchanged
2. ✅ **Flexible Provider Selection** - Switch via environment variables
3. ✅ **Automatic Fallback** - Degrades gracefully to Ollama
4. ✅ **Model Override** - Can specify different model per request
5. ✅ **Error Handling** - Comprehensive error messages and recovery

**Configuration Priority:**
```
Method Parameter > Constructor Parameter > Environment Variable > Default
```

**Example:**
```python
# All use different models!
llm = LLMManager(provider="anthropic", model="claude-3-haiku-20240307")

response1 = llm.generate(prompt)  # Uses haiku

response2 = llm.generate(prompt, model="claude-sonnet-4-20250514")  # Uses sonnet 4
```
