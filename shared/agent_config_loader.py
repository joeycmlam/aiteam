"""
Unified Agent Configuration Loader

Loads agent configurations from config/agents/*.yaml files.
These configurations are shared between VS Code Chat Agents and Python Agents.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional, List

class AgentConfigLoader:
    """
    Loads unified agent configurations from config/agents/*.yaml
    
    Provides consistent persona, prompts, and settings for both:
    - VS Code Chat Agents (.vscode/agents/*.agent.md)
    - Python Automation Agents (agents/*_agent.py)
    
    Example:
        loader = AgentConfigLoader()
        config = loader.load_agent_config('architect')
        persona = config['persona']
        prompts = config['prompts']
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize config loader
        
        Args:
            config_dir: Path to agents config directory
                       Default: {project_root}/config/agents/
        """
        if config_dir is None:
            base_dir = Path(__file__).parent.parent
            config_dir = base_dir / 'config' / 'agents'
        self.config_dir = Path(config_dir)
        
        # Fallback to old prompts directory if unified config not found
        self.prompts_dir = self.config_dir.parent / 'prompts'
    
    def load_agent_config(self, agent_role: str) -> Dict:
        """
        Load unified configuration for an agent
        
        Args:
            agent_role: Agent role identifier
                       Options: 'architect', 'ba', 'developer', 'lead', 'qa'
        
        Returns:
            Dict containing:
            - metadata: Agent name, description
            - persona: Role definition, expertise, focus areas
            - prompts: LLM prompts for Python agent methods
            - vscode_agent: VS Code Chat agent settings
        
        Raises:
            FileNotFoundError: If config file doesn't exist
        """
        config_file = self.config_dir / f"{agent_role}.yaml"
        
        if not config_file.exists():
            # Try fallback to old prompts directory
            return self._load_legacy_prompts(agent_role)
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _load_legacy_prompts(self, agent_role: str) -> Dict:
        """
        Fallback to legacy config/prompts/*.yaml format
        
        Provides backward compatibility with existing prompt files
        """
        legacy_file = self.prompts_dir / f"{agent_role}_agent_prompts.yaml"
        
        if not legacy_file.exists():
            raise FileNotFoundError(
                f"No config found for '{agent_role}' in {self.config_dir} or {self.prompts_dir}"
            )
        
        with open(legacy_file, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        
        # Wrap in unified structure
        return {
            'metadata': {
                'name': agent_role.title(),
                'role': agent_role,
                'source': 'legacy'
            },
            'prompts': prompts,
            'persona': {},
            'vscode_agent': {}
        }
    
    def get_metadata(self, agent_role: str) -> Dict:
        """
        Get agent metadata (name, description, role)
        
        Returns:
            Dict with name, description, role keys
        """
        config = self.load_agent_config(agent_role)
        return config.get('metadata', {})
    
    def get_persona(self, agent_role: str) -> Dict:
        """
        Get persona definition for an agent
        
        Returns:
            Dict with title, expertise, focus_areas, technology_stack, considerations
        """
        config = self.load_agent_config(agent_role)
        return config.get('persona', {})
    
    def get_prompts(self, agent_role: str) -> Dict:
        """
        Get prompts configuration for Python agent
        
        Returns:
            Dict with prompt templates and system messages for agent methods
        """
        config = self.load_agent_config(agent_role)
        return config.get('prompts', {})
    
    def get_vscode_config(self, agent_role: str) -> Dict:
        """
        Get VS Code Chat agent configuration
        
        Returns:
            Dict with tools, model, handoffs configuration
        """
        config = self.load_agent_config(agent_role)
        return config.get('vscode_agent', {})
    
    def get_system_message(self, agent_role: str) -> str:
        """
        Generate system message from persona
        
        Combines persona elements into a system message for LLM
        """
        persona = self.get_persona(agent_role)
        
        if not persona:
            return f"You are a {agent_role} agent."
        
        title = persona.get('title', agent_role.title())
        focus_areas = persona.get('focus_areas', [])
        
        message = f"You are a {title}.\n\n"
        
        if focus_areas:
            message += "Your responsibilities:\n"
            for area in focus_areas:
                message += f"- {area}\n"
        
        tech_stack = persona.get('technology_stack', {})
        if tech_stack:
            message += "\nTechnology preferences:\n"
            for key, value in tech_stack.items():
                if isinstance(value, list):
                    message += f"- {key.title()}: {', '.join(value)}\n"
                else:
                    message += f"- {key.title()}: {value}\n"
        
        return message.strip()
    
    def list_available_agents(self) -> List[str]:
        """
        List all available agent configurations
        
        Returns:
            List of agent role identifiers
        """
        agents = []
        
        # Check unified configs
        if self.config_dir.exists():
            for file in self.config_dir.glob("*.yaml"):
                if file.stem != 'README':
                    agents.append(file.stem)
        
        # Check legacy configs
        if self.prompts_dir.exists():
            for file in self.prompts_dir.glob("*_agent_prompts.yaml"):
                role = file.stem.replace('_agent_prompts', '')
                if role not in agents:
                    agents.append(role)
        
        return sorted(agents)
    
    def validate_config(self, agent_role: str) -> Dict:
        """
        Validate agent configuration structure
        
        Returns:
            Dict with validation results:
            - valid: bool
            - errors: List[str]
            - warnings: List[str]
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            config = self.load_agent_config(agent_role)
            
            # Check required sections
            if 'metadata' not in config:
                result['warnings'].append("Missing 'metadata' section")
            
            if 'persona' not in config:
                result['warnings'].append("Missing 'persona' section")
            
            if 'prompts' not in config:
                result['errors'].append("Missing 'prompts' section")
                result['valid'] = False
            
            # Validate persona structure
            persona = config.get('persona', {})
            if persona:
                if 'focus_areas' not in persona:
                    result['warnings'].append("Persona missing 'focus_areas'")
                if 'technology_stack' not in persona:
                    result['warnings'].append("Persona missing 'technology_stack'")
        
        except FileNotFoundError as e:
            result['valid'] = False
            result['errors'].append(str(e))
        except yaml.YAMLError as e:
            result['valid'] = False
            result['errors'].append(f"YAML parsing error: {e}")
        
        return result


# Convenience functions for quick access
def load_agent_persona(agent_role: str) -> Dict:
    """Quick access to agent persona"""
    loader = AgentConfigLoader()
    return loader.get_persona(agent_role)


def load_agent_prompts(agent_role: str) -> Dict:
    """Quick access to agent prompts"""
    loader = AgentConfigLoader()
    return loader.get_prompts(agent_role)


def get_agent_system_message(agent_role: str) -> str:
    """Quick access to generated system message"""
    loader = AgentConfigLoader()
    return loader.get_system_message(agent_role)
