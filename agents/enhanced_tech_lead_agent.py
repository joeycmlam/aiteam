"""
Tech Lead Agent - Enhanced with Agent Framework
Technical leadership agent for system design and implementation planning
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.agent_framework import Agent
from shared.llm_manager import LLMManager


class EnhancedTechLeadAgent(Agent):
    """
    Enhanced Tech Lead Agent using the agent framework
    Designs technical architecture, creates specifications, breaks down tasks
    """
    
    def __init__(self, 
                 output_dir: str = "technical_structure",
                 config_path: Optional[str] = None):
        super().__init__(
            name="TechLead",
            role="Technical Lead - System design and implementation planning",
            output_dir=output_dir,
            config_path=config_path or "config/agents/tech_lead.yaml"
        )
        
        self.llm_manager = LLMManager()
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process architecture and requirements to create technical design
        
        Args:
            input_data: Dictionary with 'architecture' and 'ba_analysis' or file paths
            
        Returns:
            Dictionary with technical design results
        """
        self.log_action("start_processing", {"input_type": type(input_data).__name__})
        
        # Load inputs
        if isinstance(input_data, dict):
            architecture = input_data.get('architecture', '')
            ba_analysis = input_data.get('ba_analysis', '')
        else:
            # Assume it's a file path or text
            architecture = ""
            ba_analysis = str(input_data)
        
        self.set_context('architecture', architecture)
        self.set_context('ba_analysis', ba_analysis)
        
        # Create technical structure
        technical_structure = self.design_technical_structure(architecture, ba_analysis)
        
        # Break down into development tasks
        development_tasks = self.breakdown_tasks(architecture, ba_analysis)
        
        # Create implementation guidelines
        guidelines = self.create_guidelines()
        
        # Create structured output
        structured_data = self.create_structured_output(
            technical_structure, development_tasks, guidelines
        )
        
        # Save outputs
        structure_file = self.save_output("technical_structure.md", technical_structure)
        tasks_file = self.save_output("development_tasks.md", development_tasks)
        guidelines_file = self.save_output("implementation_guidelines.md", guidelines)
        json_file = self.save_output("technical_structure.json",
                                     self._to_json(structured_data))
        
        result = {
            'technical_structure': technical_structure,
            'development_tasks': development_tasks,
            'guidelines': guidelines,
            'structured_data': structured_data,
            'files': {
                'structure': structure_file,
                'tasks': tasks_file,
                'guidelines': guidelines_file,
                'json': json_file
            }
        }
        
        self.log_action("completed", {"files_created": 4})
        
        return result
    
    def design_technical_structure(self, architecture: str, ba_analysis: str) -> str:
        """Design detailed technical structure"""
        self.log_action("design_technical_structure")
        
        prompt = f"""As a Technical Lead, create a detailed technical structure document.

Architecture Context:
{architecture if architecture else "No architecture provided"}

BA Analysis:
{ba_analysis}

Create a comprehensive technical structure with:

1. **Project Structure**: Directory layout, file organization
2. **Technology Stack**: Languages, frameworks, libraries with justification
3. **Module Design**: Detailed component breakdown
4. **Class Diagrams**: Key classes, attributes, methods, relationships
5. **Database Schema**: Tables, columns, types, relationships, indexes
6. **API Specifications**: Endpoints, methods, request/response formats
7. **Configuration**: Environment variables, settings files, configs
8. **Security**: Authentication, authorization, data protection approach
9. **Testing Strategy**: Unit, integration, E2E testing approach
10. **DevOps Setup**: CI/CD, containerization, deployment strategy

Format as detailed Markdown with code examples."""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=4000
        )
        
        return response
    
    def breakdown_tasks(self, architecture: str, ba_analysis: str) -> str:
        """Break down architecture into development tasks"""
        self.log_action("breakdown_tasks")
        
        prompt = f"""As a Technical Lead, break down the system into phased development tasks.

Architecture:
{architecture if architecture else "Based on requirements"}

Requirements:
{ba_analysis}

Create a phased task breakdown:

## Phase 1: Foundation
- Task 1.1: [Specific task with acceptance criteria]
- Task 1.2: [Specific task with acceptance criteria]

## Phase 2: Core Features
...

## Phase 3: Advanced Features
...

## Phase 4: Testing & Deployment
...

For each task include:
- Clear description
- Acceptance criteria
- Dependencies
- Estimated effort (S/M/L)

Format as Markdown."""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=3000
        )
        
        return response
    
    def create_guidelines(self) -> str:
        """Create implementation guidelines"""
        self.log_action("create_guidelines")
        
        prompt = """As a Technical Lead, create comprehensive implementation guidelines for developers.

Include:

1. **Coding Standards**
   - Naming conventions
   - Code organization
   - Documentation requirements

2. **Architecture Patterns**
   - Patterns to follow
   - Anti-patterns to avoid
   - When to use each pattern

3. **Best Practices**
   - Error handling
   - Logging
   - Security practices
   - Performance considerations

4. **Testing Requirements**
   - Test coverage expectations
   - Testing patterns
   - Mock usage guidelines

5. **Code Review Checklist**
   - What reviewers should check
   - Common issues to catch

Format as detailed Markdown with code examples."""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=3000
        )
        
        return response
    
    def create_structured_output(self, structure: str, tasks: str, guidelines: str) -> Dict[str, Any]:
        """Create structured JSON output"""
        return {
            "agent": self.name,
            "timestamp": self.history[-1]['timestamp'] if self.history else None,
            "technical_structure": structure,
            "development_tasks": tasks,
            "implementation_guidelines": guidelines,
            "metadata": {
                "output_dir": self.output_dir,
                "config": self.config_path
            }
        }
    
    def _to_json(self, data: Dict[str, Any]) -> str:
        """Convert dict to formatted JSON"""
        import json
        return json.dumps(data, indent=2)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Tech Lead Agent")
    parser.add_argument('--architecture', '-a', help='Architecture file or text')
    parser.add_argument('--ba-analysis', '-b', required=True, help='BA analysis file')
    parser.add_argument('--output-dir', '-o', default='technical_structure',
                       help='Output directory')
    parser.add_argument('--config', '-c', help='Config file path')
    
    args = parser.parse_args()
    
    # Initialize agent
    tech_lead = EnhancedTechLeadAgent(
        output_dir=args.output_dir,
        config_path=args.config
    )
    
    # Prepare input
    input_data = {}
    if args.architecture:
        if os.path.exists(args.architecture):
            input_data['architecture'] = tech_lead.load_input(args.architecture)
        else:
            input_data['architecture'] = args.architecture
    
    if os.path.exists(args.ba_analysis):
        input_data['ba_analysis'] = tech_lead.load_input(args.ba_analysis)
    else:
        input_data['ba_analysis'] = args.ba_analysis
    
    # Process
    results = tech_lead.process(input_data)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TECH LEAD AGENT SUMMARY")
    print("="*70)
    print(f"✅ Technical structure: {results['files']['structure']}")
    print(f"✅ Development tasks: {results['files']['tasks']}")
    print(f"✅ Implementation guidelines: {results['files']['guidelines']}")
    print(f"✅ Structured data: {results['files']['json']}")
    
    # Save history
    tech_lead.save_history()
