import os
from pathlib import Path
from typing import Dict, List
from shared.llm_manager import LLMManager

class ArchitectAgent:
    """Analyzes code structure and recommends design patterns"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("🏗️  Architect Agent initialized")
    
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
        
        # Use LLM to recommend patterns
        prompt = f"""Based on this codebase analysis:
- Total files: {analysis['total_files']}
- Languages: {analysis['languages']}
- Complexity: {analysis['complexity']}

Recommend 4-5 design patterns for modernizing this legacy code.
Format as a simple list with brief rationale."""

        try:
            llm_response = self.llm.generate(
                prompt,
                system_message="You are a software architect specializing in design patterns."
            )
            
            print(f"\n💡 LLM Recommendations:")
            print(llm_response)
            
        except Exception as e:
            print(f"⚠️  LLM unavailable: {e}")
        
        # Fallback patterns
        patterns = [
            "Repository Pattern - for data access layer",
            "Factory Pattern - for object creation",
            "Strategy Pattern - for business logic variants",
            "Dependency Injection - for loose coupling",
            "CQRS Pattern - if dealing with complex operations"
        ]
        
        print(f"\n📋 Recommended Design Patterns:")
        for pattern in patterns:
            print(f"   • {pattern}")
        
        return patterns
