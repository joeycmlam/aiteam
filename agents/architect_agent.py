import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime
from shared.llm_manager import LLMManager

class ArchitectAgent:
    """
    Solution Architect Agent - Designs system architecture and technical specifications
    
    Specializes in:
    - Designing scalable, secure system architectures for financial services
    - Creating API strategy and design patterns
    - Defining microservices boundaries and communication patterns
    - Ensuring compliance with financial industry standards
    - Documenting architectural decisions (ADRs)
    
    Technology stack preferences:
    - Cloud: Azure (AKS, API Management, Azure Data Explorer)
    - Languages: Python, TypeScript, C#
    - API: REST, OpenAPI specifications
    - DevSecOps: GitHub Actions, Docker
    
    Always considers:
    - Security best practices for financial services
    - Scalability and performance requirements
    - Cost optimization strategies
    - Disaster recovery and high availability
    """
    
    def __init__(self, llm_config: Dict, prompts_config_path: Optional[str] = None):
        self.llm_config = llm_config
        self.llm = LLMManager()
        
        # Load prompts configuration
        if prompts_config_path is None:
            prompts_config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config', 'prompts', 'architect_agent_prompts.yaml'
            )
        
        self.prompts = self._load_prompts(prompts_config_path)
        print("🏗️  Solution Architect Agent initialized")
    
    def _load_prompts(self, config_path: str) -> Dict:
        """Load prompts configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                prompts = yaml.safe_load(f)
            print(f"   ✅ Loaded prompts from: {config_path}")
            return prompts
        except FileNotFoundError:
            print(f"   ⚠️  Prompts config not found: {config_path}")
            print(f"   Using default inline prompts")
            return {}
        except Exception as e:
            print(f"   ⚠️  Error loading prompts: {e}")
            print(f"   Using default inline prompts")
            return {}
    
    def analyze_codebase(self, repo_path: str) -> Dict:
        """Analyzes legacy codebase structure"""
        print(f"\n📊 Analyzing codebase at: {repo_path}")
        
        structure = {
            "total_files": 0,
            "languages": {},
            "modules": [],
            "complexity": "medium"
        }
        
        # Walk through codebase
        for root, dirs, files in os.walk(repo_path):
            # Skip venv and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                ext = Path(file).suffix
                if ext in ['.py', '.java', '.js', '.ts', '.cs']:
                    structure["total_files"] += 1
                    structure["languages"][ext] = structure["languages"].get(ext, 0) + 1
        
        print(f"   Found {structure['total_files']} code files")
        print(f"   Languages: {structure['languages']}")
        
        return structure
    
    def recommend_patterns(self, analysis: Dict) -> List[str]:
        """Recommends design patterns using LLM"""
        print(f"\n💡 Analyzing patterns with LLM...")
        
        # Default prompt template
        default_template = '''Based on this codebase analysis:
- Total files: {total_files}
- Languages: {languages}
- Complexity: {complexity}

Recommend 4-5 design patterns for modernizing this legacy code.
Format as a simple list with brief rationale.'''
        
        # Default fallback patterns
        default_patterns = [
            'Repository Pattern - for data access layer',
            'Factory Pattern - for object creation',
            'Strategy Pattern - for business logic variants',
            'Dependency Injection - for loose coupling',
            'CQRS Pattern - if dealing with complex operations'
        ]
        
        # Get prompt template and system message from config with inline defaults
        prompt_config = self.prompts.get('recommend_patterns', {})
        prompt_template = prompt_config.get('template', default_template)
        system_message = prompt_config.get('system_message', 'You are a software architect specializing in design patterns.')
        
        # Format prompt with analysis data
        prompt = prompt_template.format(
            total_files=analysis.get('total_files', 0),
            languages=analysis.get('languages', {}),
            complexity=analysis.get('complexity', 'unknown')
        )

        try:
            llm_response = self.llm.generate(
                prompt,
                system_message=system_message
            )
            
            print(f"\n💡 LLM Recommendations:")
            print(llm_response)
            
        except Exception as e:
            print(f"⚠️  LLM unavailable: {e}")
        
        # Get fallback patterns from config or use defaults
        patterns = self.prompts.get('fallbacks', {}).get('default_patterns', default_patterns)
        
        print(f"\n📋 Recommended Design Patterns:")
        for pattern in patterns:
            print(f"   • {pattern}")
        
        return patterns
    
    def read_ba_analysis(self, analysis_source: Union[str, Dict]) -> Dict:
        """
        Read Business Analyst's requirements analysis.
        
        Args:
            analysis_source: Either a file path to requirements_structured.json 
                           or a dict containing the analysis data directly
        
        Returns:
            Dict containing BA analysis (raw_requirements, ai_analysis, scenarios, etc.)
        """
        print(f"\n📖 Reading BA Analysis...")
        
        if isinstance(analysis_source, dict):
            print(f"   ✅ Received analysis from context")
            return analysis_source
        
        # It's a file path
        analysis_path = Path(analysis_source)
        if not analysis_path.exists():
            raise FileNotFoundError(f"BA analysis file not found: {analysis_path}")
        
        with open(analysis_path, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        print(f"   ✅ Loaded analysis from: {analysis_path}")
        print(f"   Generated at: {analysis.get('generated_at', 'unknown')}")
        
        return analysis
    
    def design_system_architecture(
        self, 
        ba_analysis: Union[str, Dict],
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Design complete system architecture from BA analysis.
        
        Args:
            ba_analysis: Either path to requirements_structured.json or dict with analysis
            output_dir: Optional directory to save architecture outputs (markdown + JSON)
        
        Returns:
            Dict containing architecture design and metadata
        """
        print(f"\n🏗️  Designing System Architecture...")
        
        # Read BA analysis
        analysis = self.read_ba_analysis(ba_analysis)
        
        # Extract key components from BA analysis
        raw_requirements = analysis.get('raw_requirements', '')
        ai_analysis = analysis.get('ai_analysis', '')
        scenarios = analysis.get('scenarios', '')
        user_stories_data = analysis.get('user_stories', [])
        
        # Format user stories for prompt
        user_stories = '\n'.join([
            f"- {story.get('story', 'No story provided')}" 
            for story in user_stories_data
        ]) if user_stories_data else "No user stories provided"
        
        # Get design prompt from config
        design_config = self.prompts.get('design_architecture', {})
        prompt_template = design_config.get('template', self._get_default_design_template())
        system_message = design_config.get('system_message', 
            'You are a senior software architect with expertise in system design.')
        
        # Format prompt with BA analysis data
        prompt = prompt_template.format(
            raw_requirements=raw_requirements,
            ai_analysis=ai_analysis,
            user_stories=user_stories,
            scenarios=scenarios
        )
        
        # Generate architecture design with LLM
        try:
            print(f"   🤖 Generating architecture with LLM...")
            architecture_md = self.llm.generate(
                prompt,
                system_message=system_message
            )
            
            print(f"   ✅ Architecture design generated")
            
        except Exception as e:
            print(f"   ⚠️  LLM unavailable: {e}")
            print(f"   Using fallback architecture template")
            architecture_md = self._generate_fallback_architecture(analysis)
        
        # Prepare architecture result
        architecture_result = {
            'architecture_markdown': architecture_md,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_analysis': {
                'generated_at': analysis.get('generated_at', 'unknown'),
                'has_requirements': bool(raw_requirements),
                'has_analysis': bool(ai_analysis),
                'has_scenarios': bool(scenarios),
                'user_stories_count': len(user_stories_data)
            }
        }
        
        # Save outputs if output_dir provided
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Save markdown version
            md_file = output_path / 'system_architecture.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(architecture_md)
            print(f"   💾 Saved: {md_file}")
            
            # Save JSON version (for machine consumption by downstream agents)
            json_file = output_path / 'architecture_structured.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(architecture_result, f, indent=2, ensure_ascii=False)
            print(f"   💾 Saved: {json_file}")
        
        return architecture_result
    
    def _get_default_design_template(self) -> str:
        """Default template if config not loaded"""
        return '''Based on this comprehensive Business Analysis:

## Raw Requirements
{raw_requirements}

## Business Analysis
{ai_analysis}

## User Stories
{user_stories}

## BDD Scenarios
{scenarios}

Design a complete system architecture with:
1. System Overview
2. Architecture Style (layered, clean, microservices, etc.)
3. System Components and their responsibilities
4. Technology Stack recommendations
5. Data Model (entities and relationships)
6. API Design (if applicable)
7. Design Patterns to apply
8. Project Structure (directories/modules)
9. Implementation Phases
10. Risks and Mitigation

Format as comprehensive markdown suitable for development teams.'''
    
    def _generate_fallback_architecture(self, analysis: Dict) -> str:
        """Generate basic architecture when LLM unavailable"""
        fallback = self.prompts.get('design_architecture', {}).get('fallback_architecture', {})
        
        return f'''# System Architecture Design

## 1. System Overview
{fallback.get('overview', 'System designed based on requirements')}

## 2. Architecture Style
{fallback.get('architecture_style', 'Layered architecture')}

## 3. System Components
{chr(10).join([f"- {c}" for c in fallback.get('components', ['Component 1', 'Component 2'])])}

## 4. Technology Stack
- Language: {fallback.get('technology_stack', {}).get('language', 'Python 3.10+')}
- Framework: {fallback.get('technology_stack', {}).get('framework', 'FastAPI')}
- Database: {fallback.get('technology_stack', {}).get('database', 'PostgreSQL')}

## 5. Design Patterns
{chr(10).join([f"- {p}" for p in fallback.get('design_patterns', ['Repository', 'Service Layer'])])}

*Note: This is a fallback architecture. For detailed design, LLM service is required.*
'''

