import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime
from shared.llm_manager import LLMManager

class TechLeadAgent:
    """
    Tech Lead Agent - Coordinates team activities and code reviews
    
    Focus areas:
    
    Code Review:
    - Review code for quality, security, and maintainability
    - Ensure adherence to coding standards
    - Check test coverage and documentation
    - Validate architectural alignment
    
    Team Coordination:
    - Break down JIRA epics into manageable tasks
    - Assign work based on team capacity and expertise
    - Track progress and remove blockers
    - Facilitate knowledge sharing
    
    Technical Standards:
    - Enforce DevSecOps practices and DORA metrics
    - Ensure proper Git workflow (feature branches, PRs)
    - Maintain CI/CD pipeline health
    - Monitor code quality metrics
    
    Review Checklist:
    - Code follows team standards
    - Tests are comprehensive and passing
    - API changes are documented
    - Security considerations addressed
    - Performance impact evaluated
    - Breaking changes identified
    """
    
    def __init__(self, llm_config: Dict, prompts_config_path: Optional[str] = None):
        self.llm_config = llm_config
        self.llm = LLMManager()
        
        # Load prompts configuration
        if prompts_config_path is None:
            prompts_config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config', 'prompts', 'tech_lead_agent_prompts.yaml'
            )
        
        self.prompts = self._load_prompts(prompts_config_path)
        print("👨‍💻 Tech Lead Agent initialized")
    
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
    
    def read_architecture_design(self, architecture_source: Union[str, Dict]) -> Dict:
        """
        Read Architect's system architecture design.
        
        Args:
            architecture_source: Either a file path to architecture_structured.json 
                               or a dict containing the architecture data directly
        
        Returns:
            Dict containing architecture design
        """
        print(f"\n📖 Reading Architecture Design...")
        
        if isinstance(architecture_source, dict):
            print(f"   ✅ Received architecture from context")
            return architecture_source
        
        # It's a file path
        architecture_path = Path(architecture_source)
        if not architecture_path.exists():
            raise FileNotFoundError(f"Architecture file not found: {architecture_path}")
        
        with open(architecture_path, 'r', encoding='utf-8') as f:
            architecture = json.load(f)
        
        print(f"   ✅ Loaded architecture from: {architecture_path}")
        print(f"   Generated at: {architecture.get('generated_at', 'unknown')}")
        
        return architecture
    
    def read_ba_analysis(self, ba_source: Union[str, Dict]) -> Dict:
        """
        Read Business Analyst's requirements analysis.
        
        Args:
            ba_source: Either a file path to requirements_structured.json 
                      or a dict containing the analysis data directly
        
        Returns:
            Dict containing BA analysis
        """
        print(f"\n📖 Reading BA Analysis...")
        
        if isinstance(ba_source, dict):
            print(f"   ✅ Received BA analysis from context")
            return ba_source
        
        # It's a file path
        ba_path = Path(ba_source)
        if not ba_path.exists():
            raise FileNotFoundError(f"BA analysis file not found: {ba_path}")
        
        with open(ba_path, 'r', encoding='utf-8') as f:
            ba_analysis = json.load(f)
        
        print(f"   ✅ Loaded BA analysis from: {ba_path}")
        print(f"   Generated at: {ba_analysis.get('generated_at', 'unknown')}")
        
        return ba_analysis
    
    def design_technical_structure(
        self,
        architecture_design: Union[str, Dict],
        ba_analysis: Union[str, Dict],
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Design detailed technical structure from architecture and BA analysis.
        
        Args:
            architecture_design: Path to architecture_structured.json or dict with architecture
            ba_analysis: Path to requirements_structured.json or dict with BA analysis
            output_dir: Optional directory to save technical structure outputs
        
        Returns:
            Dict containing technical structure design and metadata
        """
        print(f"\n🏗️  Designing Technical Structure...")
        
        # Read architecture and BA analysis
        architecture = self.read_architecture_design(architecture_design)
        ba_data = self.read_ba_analysis(ba_analysis)
        
        # Extract architecture markdown
        architecture_md = architecture.get('architecture_markdown', '')
        
        # Extract BA analysis summary
        ba_summary = ba_data.get('ai_analysis', '')
        if not ba_summary:
            # Fallback to raw requirements if no AI analysis
            ba_summary = ba_data.get('raw_requirements', 'No business analysis available')
        
        # Get design prompt from config
        design_config = self.prompts.get('design_technical_structure', {})
        prompt_template = design_config.get('template', self._get_default_technical_structure_template())
        system_message = design_config.get('system_message', 
            'You are a Tech Lead creating detailed technical specifications.')
        
        # Truncate inputs if needed
        max_arch_length = design_config.get('max_architecture_length', 5000)
        max_ba_length = design_config.get('max_analysis_length', 3000)
        
        architecture_md = architecture_md[:max_arch_length]
        ba_summary = ba_summary[:max_ba_length]
        
        # Format prompt
        prompt = prompt_template.format(
            architecture_design=architecture_md,
            ba_analysis_summary=ba_summary
        )
        
        # Generate technical structure with LLM
        try:
            print(f"   🤖 Generating technical structure with LLM...")
            technical_structure_md = self.llm.generate(
                prompt,
                system_message=system_message
            )
            
            print(f"   ✅ Technical structure generated")
            
        except Exception as e:
            print(f"   ⚠️  LLM unavailable: {e}")
            print(f"   Using fallback technical structure template")
            technical_structure_md = self._generate_fallback_technical_structure(architecture, ba_data)
        
        # Prepare result
        result = {
            'technical_structure_markdown': technical_structure_md,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_architecture': {
                'generated_at': architecture.get('generated_at', 'unknown'),
                'has_architecture': bool(architecture_md)
            },
            'source_ba_analysis': {
                'generated_at': ba_data.get('generated_at', 'unknown'),
                'has_analysis': bool(ba_summary)
            }
        }
        
        # Save outputs if output_dir provided
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Save markdown version
            md_file = output_path / 'technical_structure.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(technical_structure_md)
            print(f"   💾 Saved: {md_file}")
            
            # Save JSON version
            json_file = output_path / 'technical_structure.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"   💾 Saved: {json_file}")
        
        return result
    
    def _get_default_technical_structure_template(self) -> str:
        """Default template if config not loaded"""
        return '''Based on this Architecture Design and Business Analysis, create detailed technical structure:

## Architecture Design
{architecture_design}

## Business Analysis
{ba_analysis_summary}

Provide:
1. Complete project structure (directories and files)
2. Module design with responsibilities
3. Class diagrams
4. Database schema
5. API specifications
6. Configuration files needed
7. Implementation checklist
8. Code templates
9. Testing strategy
10. DevOps setup

Format as comprehensive markdown for developers.'''
    
    def _generate_fallback_technical_structure(self, architecture: Dict, ba_analysis: Dict) -> str:
        """Generate basic technical structure when LLM unavailable"""
        fallback = self.prompts.get('fallbacks', {}).get('technical_structure', '')
        
        if fallback:
            return fallback
        
        return f'''# Technical Structure Design

## Project Structure
```
project/
├── src/
│   ├── models/
│   ├── services/
│   ├── controllers/
│   └── utils/
├── tests/
├── config/
└── docs/
```

## Implementation Checklist
- [ ] Set up project structure
- [ ] Implement data models
- [ ] Create service layer
- [ ] Build API endpoints
- [ ] Write tests
- [ ] Configure CI/CD

*Note: This is a fallback structure. For detailed design, LLM service is required.*

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
    
    def provide_guidelines(self, context: Dict) -> Dict:
        """Provides coding guidelines based on architecture and patterns"""
        print("\n📚 Providing coding guidelines")
        
        # Get context data
        project_context = context.get('project', 'Unknown project')
        recommended_patterns = context.get('recommended_patterns', [])
        technology_stack = context.get('technology_stack', {})
        
        # Get prompt from config
        guidelines_config = self.prompts.get('provide_guidelines', {})
        prompt_template = guidelines_config.get('template', '')
        system_message = guidelines_config.get('system_message', 
            'You are a Tech Lead providing coding standards.')
        
        if prompt_template:
            # Use LLM to generate comprehensive guidelines
            prompt = prompt_template.format(
                project_context=project_context,
                recommended_patterns='\n'.join([f"- {p}" for p in recommended_patterns]) if recommended_patterns else 'No specific patterns',
                technology_stack=str(technology_stack) if technology_stack else 'Not specified'
            )
            
            try:
                print("   🤖 Generating comprehensive guidelines with LLM...")
                guidelines_md = self.llm.generate(prompt, system_message=system_message)
                print("   ✅ Guidelines generated")
                
                return {
                    'guidelines_markdown': guidelines_md,
                    'patterns': recommended_patterns,
                    'technology_stack': technology_stack
                }
            except Exception as e:
                print(f"   ⚠️  LLM unavailable: {e}")
        
        # Fallback to basic guidelines
        guidelines = {
            "code_style": "Follow PEP 8 for Python",
            "testing": "Minimum 80% code coverage",
            "documentation": "Docstrings for all public methods",
            "security": "Input validation required",
            "patterns": recommended_patterns
        }
        
        print("   Guidelines provided:")
        for key, value in guidelines.items():
            if key != 'patterns':
                print(f"   • {key}: {value}")
        
        return guidelines
    
    def review_code(self, code: str, requirements: Dict, technical_structure: Optional[Dict] = None) -> Dict:
        """Reviews code implementation using LLM with technical structure reference"""
        print(f"\n🔍 Reviewing code for: {requirements.get('ticket_id', 'unknown')}")
        
        # Get review prompt from config
        review_config = self.prompts.get('review_code', {})
        prompt_template = review_config.get('template', self._get_default_review_template())
        system_message = review_config.get('system_message',
            'You are a senior Tech Lead doing code review.')
        
        # Prepare technical structure summary
        tech_structure_summary = "No technical structure provided"
        if technical_structure:
            tech_structure_summary = technical_structure.get('technical_structure_markdown', '')[:500]
        
        # Truncate code if needed
        max_code_length = review_config.get('max_code_length', 2000)
        code_snippet = code[:max_code_length]
        if len(code) > max_code_length:
            code_snippet += f"\n\n... (truncated {len(code) - max_code_length} characters)"
        
        # Format prompt
        prompt = prompt_template.format(
            ticket_id=requirements.get('ticket_id', 'N/A'),
            title=requirements.get('title', 'N/A'),
            description=requirements.get('description', 'N/A'),
            code=code_snippet,
            technical_structure_summary=tech_structure_summary
        )

        try:
            print("   🤖 Performing LLM code review...")
            llm_review = self.llm.generate(prompt, system_message=system_message)
            print(f"   ✅ LLM review completed")
            print(f"\n🤖 LLM Review:\n{llm_review[:300]}...")
            
            review = {
                "status": "approved_with_comments",
                "llm_analysis": llm_review,
                "issues": [],
                "suggestions": ["See LLM analysis for detailed suggestions"],
                "approved": True
            }
        except Exception as e:
            print(f"   ⚠️  LLM unavailable: {e}")
            llm_review = self._get_fallback_review()
            
            review = {
                "status": "manual_review_required",
                "llm_analysis": llm_review,
                "issues": [],
                "suggestions": [
                    "Consider adding more error handling",
                    "Add logging for debugging",
                    "Include performance metrics"
                ],
                "approved": False
            }
        
        print(f"   Status: {review['status']}")
        
        return review
    
    def _get_default_review_template(self) -> str:
        """Default review template if config not loaded"""
        return '''Review this code implementation:

## Requirements
Ticket ID: {ticket_id}
Title: {title}
Description: {description}

## Code Implementation
{code}

## Technical Structure Reference
{technical_structure_summary}

Check for:
1. Correctness (meets requirements)
2. Security vulnerabilities
3. Code quality
4. Error handling
5. Test coverage
6. Architecture alignment

Provide: issues list, suggestions, approval recommendation.'''
    
    def _get_fallback_review(self) -> str:
        """Get fallback review when LLM unavailable"""
        fallback = self.prompts.get('fallbacks', {}).get('code_review', '')
        if fallback:
            return fallback
        
        return '''## Code Review (Manual Review Required)

**Status**: Manual review needed (AI unavailable)

### Review Checklist
- [ ] Code meets requirements
- [ ] Follows coding standards
- [ ] Includes error handling
- [ ] Has adequate tests
- [ ] Security considerations addressed
- [ ] Documentation complete

Please conduct manual review.'''
    
    def breakdown_tasks(
        self,
        architecture_design: Union[str, Dict],
        ba_analysis: Union[str, Dict],
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Break down architecture into actionable development tasks.
        
        Args:
            architecture_design: Path to architecture_structured.json or dict
            ba_analysis: Path to requirements_structured.json or dict
            output_dir: Optional directory to save task breakdown
        
        Returns:
            Dict containing task breakdown
        """
        print(f"\n📋 Breaking down architecture into tasks...")
        
        # Read architecture and BA analysis
        architecture = self.read_architecture_design(architecture_design)
        ba_data = self.read_ba_analysis(ba_analysis)
        
        # Extract data
        architecture_md = architecture.get('architecture_markdown', '')
        requirements_summary = ba_data.get('ai_analysis', ba_data.get('raw_requirements', ''))
        
        # Get prompt from config
        breakdown_config = self.prompts.get('breakdown_tasks', {})
        prompt_template = breakdown_config.get('template', self._get_default_breakdown_template())
        system_message = breakdown_config.get('system_message',
            'You are a Tech Lead breaking down architecture into tasks.')
        
        # Format prompt
        prompt = prompt_template.format(
            architecture_design=architecture_md[:3000],
            requirements_summary=requirements_summary[:2000]
        )
        
        # Generate task breakdown
        try:
            print("   🤖 Generating task breakdown with LLM...")
            tasks_md = self.llm.generate(prompt, system_message=system_message)
            print("   ✅ Task breakdown generated")
        except Exception as e:
            print(f"   ⚠️  LLM unavailable: {e}")
            tasks_md = self._generate_fallback_tasks()
        
        # Prepare result
        result = {
            'tasks_markdown': tasks_md,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save if output_dir provided
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            md_file = output_path / 'development_tasks.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(tasks_md)
            print(f"   💾 Saved: {md_file}")
            
            json_file = output_path / 'tasks_structured.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"   💾 Saved: {json_file}")
        
        return result
    
    def _get_default_breakdown_template(self) -> str:
        """Default task breakdown template"""
        return '''Break down this architecture into development tasks:

## System Architecture
{architecture_design}

## Requirements Summary
{requirements_summary}

Create phased task breakdown with:
- Phase 1: Foundation
- Phase 2: Data Layer
- Phase 3: Business Logic
- Phase 4: API/Interface
- Phase 5: Integration
- Phase 6: Testing
- Phase 7: DevOps

For each task: ID, title, description, acceptance criteria, effort, dependencies.'''
    
    def _generate_fallback_tasks(self) -> str:
        """Generate fallback task list"""
        fallback = self.prompts.get('fallbacks', {}).get('default_tasks', '')
        if fallback:
            return fallback
        
        return '''## Development Tasks

### Phase 1: Setup
- Task 1: Initialize project structure
- Task 2: Set up development environment
- Task 3: Configure CI/CD pipeline

### Phase 2: Core Development
- Task 4: Implement data models
- Task 5: Create business logic
- Task 6: Build API layer

### Phase 3: Testing & Deployment
- Task 7: Write comprehensive tests
- Task 8: Deploy to staging
- Task 9: Production release

*Note: Detailed task breakdown requires LLM service.*'''
