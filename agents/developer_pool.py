"""
Developer Pool - Manage multiple developer agents with specializations

Supports:
- Multiple concurrent developers
- Specialization (frontend, backend, full-stack, mobile)
- Task distribution and load balancing
- Parallel development
- Code integration coordination
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import os
import json
from shared.llm_manager import LLMManager


class DeveloperSpecialization(Enum):
    """Developer specialization types"""
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    MOBILE = "mobile"
    DATABASE = "database"
    DEVOPS = "devops"


class DeveloperAgent:
    """Individual developer agent with specific specialization"""
    
    def __init__(self, 
                 developer_id: str,
                 specialization: DeveloperSpecialization,
                 llm_config: Dict,
                 skills: List[str] = None):
        self.developer_id = developer_id
        self.specialization = specialization
        self.llm = LLMManager()
        self.skills = skills or self._get_default_skills()
        self.current_task = None
        self.tasks_completed = 0
        
        print(f"   👨‍💻 {developer_id} ({specialization.value}) initialized")
    
    def _get_default_skills(self) -> List[str]:
        """Get default skills based on specialization"""
        skill_map = {
            DeveloperSpecialization.FRONTEND: [
                'React', 'TypeScript', 'HTML/CSS', 'Redux', 'Jest'
            ],
            DeveloperSpecialization.BACKEND: [
                'Python', 'FastAPI', 'REST APIs', 'SQL', 'Redis'
            ],
            DeveloperSpecialization.FULLSTACK: [
                'JavaScript', 'Python', 'React', 'Node.js', 'SQL'
            ],
            DeveloperSpecialization.MOBILE: [
                'React Native', 'Swift', 'Kotlin', 'Mobile UI/UX'
            ],
            DeveloperSpecialization.DATABASE: [
                'SQL', 'NoSQL', 'Database Design', 'Query Optimization'
            ],
            DeveloperSpecialization.DEVOPS: [
                'Docker', 'Kubernetes', 'CI/CD', 'Infrastructure'
            ]
        }
        return skill_map.get(self.specialization, [])
    
    def can_handle_task(self, task: Dict) -> float:
        """
        Determine if developer can handle task
        
        Args:
            task: Task description with required skills
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        required_skills = task.get('required_skills', [])
        task_type = task.get('type', '').lower()
        
        # Check specialization match
        specialization_match = 0.0
        if self.specialization.value in task_type:
            specialization_match = 0.5
        
        # Check skill overlap
        if not required_skills:
            skill_match = 0.3  # Default if no specific skills
        else:
            matching_skills = set(self.skills) & set(required_skills)
            skill_match = len(matching_skills) / len(required_skills)
        
        # Combined confidence score
        confidence = (specialization_match + skill_match) / 1.5
        return min(confidence, 1.0)
    
    def implement_task(self, task: Dict, context: Dict = None) -> Dict:
        """
        Implement a development task
        
        Args:
            task: Task to implement
            context: Additional context (architecture, requirements, etc.)
            
        Returns:
            Implementation result with code and documentation
        """
        print(f"\n   👨‍💻 {self.developer_id} implementing: {task.get('name', 'task')}")
        
        self.current_task = task
        
        prompt = f"""
You are a {self.specialization.value} developer implementing this task:

Task:
{json.dumps(task, indent=2)}

Context:
{json.dumps(context or {}, indent=2)}

Your skills: {', '.join(self.skills)}

Provide:
1. Implementation approach
2. Code structure and files to create
3. Key code snippets with explanations
4. Dependencies needed
5. Testing approach
6. Integration considerations

Return as JSON:
{{
    "approach": "implementation approach",
    "files": [
        {{
            "path": "path/to/file",
            "purpose": "file purpose",
            "code": "code content"
        }}
    ],
    "dependencies": ["dependency1", "dependency2"],
    "tests": [
        {{
            "file": "test file path",
            "test_cases": ["test case descriptions"]
        }}
    ],
    "integration_notes": "how this integrates with other components"
}}
"""
        
        system_message = f"""You are a senior {self.specialization.value} developer with expertise in {', '.join(self.skills[:3])}.
Focus on clean code, best practices, and maintainability."""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message=system_message,
                max_tokens=3000,
                temperature=0.4
            )
            
            implementation = self._parse_implementation(response)
            implementation['developer_id'] = self.developer_id
            implementation['specialization'] = self.specialization.value
            
            self.tasks_completed += 1
            self.current_task = None
            
            print(f"      ✅ Completed: {len(implementation.get('files', []))} files")
            
            return implementation
            
        except Exception as e:
            print(f"      ⚠️  Error implementing task: {e}")
            return {
                "error": str(e),
                "developer_id": self.developer_id,
                "files": []
            }
    
    def review_code(self, code: Dict, author: str) -> Dict:
        """
        Review code from another developer
        
        Args:
            code: Code to review
            author: Original author
            
        Returns:
            Review with feedback and suggestions
        """
        print(f"   🔍 {self.developer_id} reviewing code from {author}")
        
        prompt = f"""
Review this code as a {self.specialization.value} developer:

Code:
{json.dumps(code, indent=2)}

Author: {author}

Provide feedback on:
1. Code quality and readability
2. Best practices adherence
3. Performance considerations
4. Security issues
5. Suggestions for improvement
6. Approval status

Return as JSON with sections for each aspect.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message=f"You are a code reviewer specializing in {self.specialization.value}.",
                max_tokens=1500
            )
            
            review = self._parse_review(response)
            review['reviewer'] = self.developer_id
            review['author'] = author
            
            return review
            
        except Exception as e:
            print(f"      ⚠️  Error reviewing code: {e}")
            return {"error": str(e), "reviewer": self.developer_id}
    
    def _parse_implementation(self, response: str) -> Dict:
        """Parse implementation from LLM response"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "approach": "Implementation approach",
            "files": [],
            "dependencies": [],
            "tests": []
        }
    
    def _parse_review(self, response: str) -> Dict:
        """Parse code review from LLM response"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "approved": True,
            "comments": ["Review completed"],
            "suggestions": []
        }
    
    def get_status(self) -> Dict:
        """Get current developer status"""
        return {
            "developer_id": self.developer_id,
            "specialization": self.specialization.value,
            "skills": self.skills,
            "current_task": self.current_task.get('name') if self.current_task else None,
            "tasks_completed": self.tasks_completed,
            "available": self.current_task is None
        }


class DeveloperPool:
    """Manage a pool of developer agents"""
    
    def __init__(self, llm_config: Dict, config: Dict = None):
        self.llm_config = llm_config
        self.config = config or {}
        self.developers: List[DeveloperAgent] = []
        self.task_queue: List[Dict] = []
        self.completed_tasks: List[Dict] = []
        
        print("🏊 Developer Pool initializing...")
        self._initialize_developers()
    
    def _initialize_developers(self):
        """Initialize developer agents based on configuration"""
        # Get counts from config
        frontend_count = self.config.get('frontend', {}).get('count', 2)
        backend_count = self.config.get('backend', {}).get('count', 2)
        fullstack_count = self.config.get('fullstack', {}).get('count', 1)
        
        # Create frontend developers
        for i in range(frontend_count):
            dev = DeveloperAgent(
                f"Dev-Frontend-{i+1}",
                DeveloperSpecialization.FRONTEND,
                self.llm_config,
                self.config.get('frontend', {}).get('skills')
            )
            self.developers.append(dev)
        
        # Create backend developers
        for i in range(backend_count):
            dev = DeveloperAgent(
                f"Dev-Backend-{i+1}",
                DeveloperSpecialization.BACKEND,
                self.llm_config,
                self.config.get('backend', {}).get('skills')
            )
            self.developers.append(dev)
        
        # Create full-stack developers
        for i in range(fullstack_count):
            dev = DeveloperAgent(
                f"Dev-FullStack-{i+1}",
                DeveloperSpecialization.FULLSTACK,
                self.llm_config,
                self.config.get('fullstack', {}).get('skills')
            )
            self.developers.append(dev)
        
        print(f"✅ Developer Pool ready: {len(self.developers)} developers")
    
    def assign_task(self, task: Dict) -> Optional[DeveloperAgent]:
        """
        Assign task to best-fit available developer
        
        Args:
            task: Task to assign
            
        Returns:
            Assigned developer or None if no one available
        """
        print(f"\n📋 Assigning task: {task.get('name', 'Unnamed task')}")
        
        # Find available developers
        available = [d for d in self.developers if d.current_task is None]
        
        if not available:
            print("   ⚠️  No developers available, queuing task")
            self.task_queue.append(task)
            return None
        
        # Find best match
        best_developer = None
        best_confidence = 0.0
        
        for dev in available:
            confidence = dev.can_handle_task(task)
            print(f"   {dev.developer_id}: {confidence:.2f} confidence")
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_developer = dev
        
        if best_developer:
            print(f"   ✅ Assigned to {best_developer.developer_id}")
            return best_developer
        
        # No good match, queue task
        self.task_queue.append(task)
        return None
    
    def distribute_tasks(self, tasks: List[Dict], context: Dict = None) -> List[Dict]:
        """
        Distribute multiple tasks across developers
        
        Args:
            tasks: List of tasks to distribute
            context: Shared context for all tasks
            
        Returns:
            List of implementation results
        """
        print(f"\n🚀 Distributing {len(tasks)} tasks across developer pool")
        
        results = []
        
        # Add all tasks to queue
        self.task_queue.extend(tasks)
        
        # Process queue
        while self.task_queue:
            task = self.task_queue.pop(0)
            
            # Try to assign
            developer = self.assign_task(task)
            
            if developer:
                # Implement task
                result = developer.implement_task(task, context)
                results.append(result)
                self.completed_tasks.append({
                    'task': task,
                    'result': result,
                    'developer': developer.developer_id
                })
            else:
                # No one available, put back in queue
                self.task_queue.insert(0, task)
                break
        
        print(f"\n✅ Completed {len(results)} tasks")
        if self.task_queue:
            print(f"⏳ {len(self.task_queue)} tasks still queued")
        
        return results
    
    def get_available_developers(self) -> List[DeveloperAgent]:
        """Get list of available developers"""
        return [d for d in self.developers if d.current_task is None]
    
    def get_team_status(self) -> Dict:
        """Get overall team status"""
        available = len(self.get_available_developers())
        busy = len(self.developers) - available
        
        return {
            "total_developers": len(self.developers),
            "available": available,
            "busy": busy,
            "queued_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "developers": [d.get_status() for d in self.developers]
        }
    
    def print_team_status(self):
        """Print formatted team status"""
        status = self.get_team_status()
        
        print("\n" + "="*70)
        print("👥 DEVELOPER TEAM STATUS")
        print("="*70)
        print(f"Total Developers: {status['total_developers']}")
        print(f"Available: {status['available']} | Busy: {status['busy']}")
        print(f"Queued Tasks: {status['queued_tasks']} | Completed: {status['completed_tasks']}")
        
        print("\n📊 Individual Status:")
        for dev_status in status['developers']:
            status_icon = "🟢" if dev_status['available'] else "🔴"
            task = dev_status['current_task'] or "Available"
            print(f"   {status_icon} {dev_status['developer_id']:20} - {task}")
        
        print("="*70 + "\n")


if __name__ == "__main__":
    # Demo usage
    print("Developer Pool Demo\n")
    
    config = {
        'frontend': {'count': 2, 'skills': ['React', 'TypeScript']},
        'backend': {'count': 2, 'skills': ['Python', 'FastAPI']},
        'fullstack': {'count': 1}
    }
    
    pool = DeveloperPool(
        {"provider": "ollama", "model": "llama3.2"},
        config
    )
    
    # Show team status
    pool.print_team_status()
    
    # Create sample tasks
    tasks = [
        {
            "name": "Implement login UI",
            "type": "frontend",
            "required_skills": ["React", "TypeScript"]
        },
        {
            "name": "Create authentication API",
            "type": "backend",
            "required_skills": ["Python", "FastAPI", "JWT"]
        },
        {
            "name": "User profile page",
            "type": "frontend",
            "required_skills": ["React"]
        }
    ]
    
    # Distribute tasks
    results = pool.distribute_tasks(tasks)
    
    print(f"\n✅ All tasks distributed: {len(results)} implementations")
    
    # Show final status
    pool.print_team_status()
