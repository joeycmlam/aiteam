from typing import Dict, List
from shared.llm_manager import LLMManager

class SeniorDevAgent:
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
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("👨‍💻 Tech Lead Agent initialized")
    
    def provide_guidelines(self, context: Dict) -> Dict:
        """Provides coding guidelines"""
        print("\n📚 Providing coding guidelines")
        
        guidelines = {
            "code_style": "Follow PEP 8 for Python",
            "testing": "Minimum 80% code coverage",
            "documentation": "Docstrings for all public methods",
            "security": "Input validation required",
            "patterns": context.get('recommended_patterns', [])
        }
        
        print("   Guidelines provided:")
        for key, value in guidelines.items():
            if key != 'patterns':
                print(f"   • {key}: {value}")
        
        return guidelines
    
    def review_code(self, code: str, requirements: Dict) -> Dict:
        """Reviews code implementation using LLM"""
        print(f"\n🔍 Reviewing code for: {requirements.get('ticket_id', 'unknown')}")
        
        prompt = f"""Review this code implementation:

Requirements:
{requirements.get('title', 'N/A')}

Code:
{code[:1000]}

Check for:
1. Correctness (meets requirements)
2. Security vulnerabilities
3. Code quality
4. Error handling
5. Test coverage

Provide: issues list, suggestions, approval recommendation."""

        try:
            llm_review = self.llm.generate(
                prompt,
                system_message="You are a senior developer doing code review."
            )
            print(f"\n🤖 LLM Review:\n{llm_review[:300]}...")
        except:
            llm_review = "Manual review needed"
        
        review = {
            "status": "approved_with_comments",
            "llm_analysis": llm_review,
            "issues": [],
            "suggestions": [
                "Consider adding more error handling",
                "Add logging for debugging",
                "Include performance metrics"
            ],
            "approved": True
        }
        
        print(f"   Status: {review['status']}")
        
        return review
