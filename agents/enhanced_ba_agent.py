"""
BA Agent - Enhanced with Agent Framework
Business Analyst agent for requirements gathering and analysis
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.agent_framework import Agent
from shared.llm_manager import LLMManager


class EnhancedBAAgent(Agent):
    """
    Enhanced BA Agent using the agent framework
    Analyzes requirements, creates documentation, generates user stories
    """
    
    def __init__(self, 
                 output_dir: str = "requirements/analysis",
                 config_path: Optional[str] = None):
        super().__init__(
            name="BA",
            role="Business Analyst - Requirements gathering and analysis",
            output_dir=output_dir,
            config_path=config_path or "config/agents/ba.yaml"
        )
        
        self.llm_manager = LLMManager()
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process requirements input
        
        Args:
            input_data: Requirements text or file path
            
        Returns:
            Dictionary with analysis results
        """
        self.log_action("start_processing", {"input_type": type(input_data).__name__})
        
        # Load requirements
        if isinstance(input_data, str) and os.path.exists(input_data):
            requirements_text = self.load_input(input_data)
            self.set_context('requirements_file', input_data)
        else:
            requirements_text = str(input_data)
        
        self.set_context('requirements_text', requirements_text)
        
        # Analyze requirements
        analysis = self.analyze_requirements(requirements_text)
        
        # Generate user stories
        user_stories = self.generate_user_stories(requirements_text)
        
        # Create structured output
        structured_data = self.create_structured_output(analysis, user_stories)
        
        # Save outputs
        analysis_file = self.save_output("requirements_analysis.md", analysis)
        stories_file = self.save_output("user_stories.feature", user_stories)
        json_file = self.save_output("requirements_structured.json", 
                                    self._to_json(structured_data))
        
        result = {
            'analysis': analysis,
            'user_stories': user_stories,
            'structured_data': structured_data,
            'files': {
                'analysis': analysis_file,
                'stories': stories_file,
                'json': json_file
            }
        }
        
        self.log_action("completed", {"files_created": 3})
        
        return result
    
    def analyze_requirements(self, requirements_text: str) -> str:
        """Analyze requirements and generate markdown report"""
        self.log_action("analyze_requirements")
        
        prompt = f"""As a Business Analyst, analyze these requirements:

{requirements_text}

Provide a comprehensive analysis with:
1. Overview and objectives
2. Stakeholders
3. Functional requirements
4. Non-functional requirements
5. Constraints
6. Dependencies
7. Success criteria

Format as detailed Markdown."""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=4000
        )
        
        return response
    
    def generate_user_stories(self, requirements_text: str) -> str:
        """Generate user stories in Gherkin format"""
        self.log_action("generate_user_stories")
        
        prompt = f"""As a Business Analyst, create user stories from these requirements:

{requirements_text}

Generate Gherkin format user stories with:
- Feature description
- User stories (As a... I want... So that...)
- Scenarios (Given/When/Then)

Format as proper Gherkin/BDD syntax."""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=4000
        )
        
        return response
    
    def create_structured_output(self, analysis: str, user_stories: str) -> Dict[str, Any]:
        """Create structured JSON output"""
        return {
            "agent": self.name,
            "timestamp": self.history[-1]['timestamp'] if self.history else None,
            "analysis": analysis,
            "user_stories": user_stories,
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
    
    parser = argparse.ArgumentParser(description="Enhanced BA Agent")
    parser.add_argument('--input', '-i', required=True, help='Requirements file or text')
    parser.add_argument('--output-dir', '-o', default='requirements/analysis', 
                       help='Output directory')
    parser.add_argument('--config', '-c', help='Config file path')
    
    args = parser.parse_args()
    
    # Initialize agent
    ba_agent = EnhancedBAAgent(
        output_dir=args.output_dir,
        config_path=args.config
    )
    
    # Process requirements
    results = ba_agent.process(args.input)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 BA AGENT SUMMARY")
    print("="*70)
    print(f"✅ Analysis saved: {results['files']['analysis']}")
    print(f"✅ User stories saved: {results['files']['stories']}")
    print(f"✅ Structured data saved: {results['files']['json']}")
    
    # Save history
    ba_agent.save_history()
