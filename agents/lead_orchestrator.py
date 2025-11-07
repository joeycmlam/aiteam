from typing import Dict, List
from shared.memory_store import SharedMemory
from shared.llm_manager import LLMManager

class LeadOrchestrator:
    """Coordinates all agents and manages workflow"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.memory = SharedMemory()
        self.llm = LLMManager()
        print("🎯 Lead Orchestrator initialized")
    
    def create_workflow(self, jira_tickets: List[str]) -> Dict:
        """Creates migration workflow from JIRA tickets"""
        workflow = {
            "tickets": jira_tickets,
            "stages": [
                {"name": "Architecture Analysis", "agent": "ArchitectAgent", "status": "pending"},
                {"name": "Requirements Gathering", "agent": "BAAgent", "status": "pending"},
                {"name": "Test Design", "agent": "QAAgent", "status": "pending"},
                {"name": "Implementation", "agent": "DeveloperAgent", "status": "pending"},
                {"name": "Code Review", "agent": "SeniorDevAgent", "status": "pending"}
            ]
        }
        
        self.memory.store('workflow', workflow)
        print(f"📋 Workflow created with {len(workflow['stages'])} stages")
        return workflow
    
    def execute_workflow(self, workflow: Dict):
        """Execute the migration workflow"""
        print("\n🚀 Starting workflow execution...\n")
        
        for i, stage in enumerate(workflow['stages'], 1):
            print(f"{'='*60}")
            print(f"Stage {i}/{len(workflow['stages'])}: {stage['name']}")
            print(f"Agent: {stage['agent']}")
            print(f"{'='*60}\n")
            
            stage['status'] = 'completed'
            print(f"✅ {stage['name']} completed\n")
        
        print("🎉 Workflow execution completed!")
