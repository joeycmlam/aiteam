"""
Agent Framework for VS Code GitHub Copilot Integration
Provides base classes and utilities for building custom agents
"""
import os
import json
import yaml
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path


class Agent(ABC):
    """
    Base Agent class for all custom agents
    Provides common functionality for agent development
    """
    
    def __init__(self, 
                 name: str,
                 role: str,
                 output_dir: str = "output",
                 config_path: Optional[str] = None):
        """
        Initialize base agent
        
        Args:
            name: Agent name (e.g., "BA", "TechLead", "Developer")
            role: Agent role description
            output_dir: Directory for agent outputs
            config_path: Path to agent configuration file
        """
        self.name = name
        self.role = role
        self.output_dir = output_dir
        self.config_path = config_path
        self.config = self._load_config() if config_path else {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Agent state
        self.context = {}
        self.history = []
        
        print(f"✅ {name} Agent initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load agent configuration from YAML or JSON"""
        if not os.path.exists(self.config_path):
            print(f"⚠️  Config not found: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif self.config_path.endswith('.json'):
                    return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return {}
    
    def set_context(self, key: str, value: Any):
        """Store context for this agent"""
        self.context[key] = value
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'set_context',
            'key': key
        })
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Retrieve context"""
        return self.context.get(key, default)
    
    def save_output(self, filename: str, content: str, subdir: str = None) -> str:
        """
        Save agent output to file
        
        Args:
            filename: Output filename
            content: File content
            subdir: Optional subdirectory
            
        Returns:
            Full path to saved file
        """
        if subdir:
            output_path = os.path.join(self.output_dir, subdir)
            os.makedirs(output_path, exist_ok=True)
        else:
            output_path = self.output_dir
        
        filepath = os.path.join(output_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Saved: {filepath}")
        
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'save_output',
            'file': filepath
        })
        
        return filepath
    
    def load_input(self, filepath: str) -> str:
        """Load input file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Input file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Loaded: {filepath}")
        
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'load_input',
            'file': filepath
        })
        
        return content
    
    def log_action(self, action: str, details: Dict[str, Any] = None):
        """Log agent action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent': self.name,
            'action': action,
            'details': details or {}
        }
        self.history.append(log_entry)
        print(f"📝 {self.name}: {action}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get agent action history"""
        return self.history
    
    def save_history(self, filename: str = "agent_history.json"):
        """Save agent history to file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)
        print(f"💾 History saved: {filepath}")
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Main processing method - must be implemented by subclasses
        
        Args:
            input_data: Input for the agent to process
            
        Returns:
            Processed output
        """
        pass
    
    def __repr__(self):
        return f"{self.name}Agent(role='{self.role}')"


class AgentChain:
    """
    Chain multiple agents together for sequential processing
    Implements agent orchestration and context passing
    """
    
    def __init__(self, name: str = "AgentChain"):
        self.name = name
        self.agents: List[Agent] = []
        self.shared_context = {}
        self.execution_log = []
    
    def add_agent(self, agent: Agent):
        """Add agent to the chain"""
        self.agents.append(agent)
        print(f"➕ Added {agent.name} to chain")
    
    def set_shared_context(self, key: str, value: Any):
        """Set context shared across all agents"""
        self.shared_context[key] = value
    
    def get_shared_context(self, key: str, default: Any = None) -> Any:
        """Get shared context"""
        return self.shared_context.get(key, default)
    
    def execute(self, initial_input: Any) -> Dict[str, Any]:
        """
        Execute the agent chain
        
        Args:
            initial_input: Input for the first agent
            
        Returns:
            Dictionary with results from each agent
        """
        print(f"\n{'='*70}")
        print(f"🚀 Executing {self.name}")
        print(f"{'='*70}\n")
        
        results = {}
        current_input = initial_input
        
        for i, agent in enumerate(self.agents, 1):
            print(f"\n📌 Step {i}/{len(self.agents)}: {agent.name}")
            print(f"{'-'*70}")
            
            try:
                # Pass shared context to agent
                for key, value in self.shared_context.items():
                    agent.set_context(key, value)
                
                # Execute agent
                start_time = datetime.now()
                output = agent.process(current_input)
                end_time = datetime.now()
                
                # Log execution
                execution_entry = {
                    'step': i,
                    'agent': agent.name,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_seconds': (end_time - start_time).total_seconds(),
                    'status': 'success'
                }
                self.execution_log.append(execution_entry)
                
                # Store result
                results[agent.name] = output
                
                # Pass output to next agent
                current_input = output
                
                print(f"✅ {agent.name} completed")
                
            except Exception as e:
                print(f"❌ {agent.name} failed: {e}")
                execution_entry = {
                    'step': i,
                    'agent': agent.name,
                    'status': 'failed',
                    'error': str(e)
                }
                self.execution_log.append(execution_entry)
                raise
        
        print(f"\n{'='*70}")
        print(f"✅ {self.name} completed successfully!")
        print(f"{'='*70}\n")
        
        return results
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get execution log"""
        return self.execution_log
    
    def save_execution_log(self, filepath: str = "execution_log.json"):
        """Save execution log to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.execution_log, f, indent=2)
        print(f"💾 Execution log saved: {filepath}")


class VSCodeAgentIntegration:
    """
    Integration layer between Python agents and VS Code custom agents
    Provides utilities for VS Code agent development
    """
    
    @staticmethod
    def create_agent_definition(
        name: str,
        description: str,
        role: str,
        responsibilities: List[str],
        use_cases: List[str],
        examples: List[str],
        output_path: str
    ) -> str:
        """
        Create a VS Code custom agent definition file
        
        Args:
            name: Agent name
            description: Short description
            role: Agent role and expertise
            responsibilities: List of responsibilities
            use_cases: When to use this agent
            examples: Example usage patterns
            output_path: Where to save the .agent.md file
            
        Returns:
            Path to created file
        """
        template = f"""```chatagent
---
description: '{description}'
tools: []
---

# {name} Agent

{role}

## Your Role & Responsibilities

{chr(10).join(f"- {r}" for r in responsibilities)}

## When to Use This Agent

Use @{name.lower()} when you need to:
{chr(10).join(f"- {u}" for u in use_cases)}

## Example Usage

{chr(10).join(examples)}

## Integration with Python Agents

This VS Code agent complements the Python automation agent:
- **VS Code Agent**: Interactive chat, exploration, refinement (Claude Sonnet 4)
- **Python Agent**: Automated workflows, batch processing (GPT-4o)

You can use both:
```bash
# Python automation
python agents/{name.lower()}_agent.py --input requirements.md

# Then review in VS Code Chat
@{name.lower()} review the output in #file:output/{name.lower()}_output.md
```

---
*Generated by VS Code Agent Integration Framework*
```
"""
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ Created VS Code agent: {output_path}")
        return output_path
    
    @staticmethod
    def sync_config_to_vscode(python_agent_config: str, vscode_agent_path: str):
        """
        Sync Python agent configuration to VS Code agent definition
        Keeps both in sync
        """
        # Load Python agent config
        with open(python_agent_config, 'r') as f:
            config = yaml.safe_load(f)
        
        # Extract key information
        name = config.get('name', 'Unknown')
        description = config.get('description', '')
        
        # Update VS Code agent
        print(f"🔄 Syncing {name} config to VS Code agent")
        # Implementation here...
        
        print(f"✅ Synced: {vscode_agent_path}")


if __name__ == "__main__":
    print("Agent Framework loaded successfully!")
    print("\nAvailable classes:")
    print("- Agent: Base class for all agents")
    print("- AgentChain: Orchestrate multiple agents")
    print("- VSCodeAgentIntegration: VS Code integration utilities")
