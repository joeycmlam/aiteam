from typing import Dict, List, Optional, Callable
from shared.memory_store import SharedMemory
from shared.llm_manager import LLMManager

class LeadOrchestrator:
    """Coordinates all agents and manages workflow with flexible step execution"""
    
    # Available workflow steps
    AVAILABLE_STEPS = {
        'architect': {'name': 'Architecture Analysis', 'agent': 'ArchitectAgent'},
        'ba': {'name': 'Requirements Gathering', 'agent': 'BAAgent'},
        'qa': {'name': 'Test Design', 'agent': 'QAAgent'},
        'developer': {'name': 'Implementation', 'agent': 'DeveloperAgent'},
        'senior_dev': {'name': 'Code Review', 'agent': 'SeniorDevAgent'}
    }
    
    def __init__(self, llm_config: Dict, jira_config: Optional[Dict] = None):
        self.llm_config = llm_config
        self.jira_config = jira_config or {}
        self.memory = SharedMemory()
        self.llm = LLMManager()
        self.step_handlers = {}  # Registered step execution handlers
        print("🎯 Lead Orchestrator initialized")
    
    def register_step_handler(self, step_key: str, handler: Callable):
        """Register a handler function for a specific workflow step
        
        Args:
            step_key: Step identifier (e.g., 'ba', 'architect')
            handler: Function that executes the step logic
        """
        self.step_handlers[step_key] = handler
        print(f"   ✅ Registered handler for '{step_key}' step")
    
    def create_workflow(self, 
                       jira_tickets: Optional[List[str]] = None,
                       steps: Optional[List[str]] = None,
                       context: Optional[Dict] = None) -> Dict:
        """Creates a flexible workflow with specified steps
        
        Args:
            jira_tickets: Optional list of JIRA ticket IDs
            steps: List of step keys to include (e.g., ['ba', 'architect'])
                  If None, includes all available steps in default order
            context: Optional context data to pass through workflow
        
        Returns:
            Workflow dictionary with configured stages
            
        Examples:
            # Full pipeline
            create_workflow(steps=['ba', 'architect', 'qa', 'developer', 'senior_dev'])
            
            # Single step for review
            create_workflow(steps=['ba'])
            
            # Partial pipeline
            create_workflow(steps=['ba', 'architect'])
        """
        # Use provided steps or default to all steps
        if steps is None:
            steps = list(self.AVAILABLE_STEPS.keys())
        
        # Validate steps
        invalid_steps = [s for s in steps if s not in self.AVAILABLE_STEPS]
        if invalid_steps:
            raise ValueError(f"Invalid steps: {invalid_steps}. Available: {list(self.AVAILABLE_STEPS.keys())}")
        
        # Build workflow stages
        stages = []
        for step_key in steps:
            step_info = self.AVAILABLE_STEPS[step_key]
            stages.append({
                "key": step_key,
                "name": step_info['name'],
                "agent": step_info['agent'],
                "status": "pending",
                "result": None
            })
        
        workflow = {
            "tickets": jira_tickets or [],
            "stages": stages,
            "context": context or {},
            "status": "created"
        }
        
        self.memory.store('workflow', workflow)
        print(f"📋 Workflow created with {len(workflow['stages'])} step(s): {', '.join(steps)}")
        return workflow
    
    def execute_workflow(self, workflow: Dict, pause_between_steps: bool = False) -> Dict:
        """Execute the workflow with optional step-by-step control
        
        Args:
            workflow: Workflow dictionary from create_workflow()
            pause_between_steps: If True, waits for confirmation between steps
            
        Returns:
            Updated workflow with results
        """
        print("\n🚀 Starting workflow execution...\n")
        workflow['status'] = 'running'
        
        for i, stage in enumerate(workflow['stages'], 1):
            print(f"{'='*60}")
            print(f"Step {i}/{len(workflow['stages'])}: {stage['name']}")
            print(f"Agent: {stage['agent']} (key: {stage['key']})")
            print(f"{'='*60}\n")
            
            # Execute step handler if registered
            step_key = stage['key']
            if step_key in self.step_handlers:
                try:
                    stage['status'] = 'running'
                    result = self.step_handlers[step_key](workflow['context'])
                    stage['result'] = result
                    stage['status'] = 'completed'
                    
                    # Store result in context for next steps
                    workflow['context'][f'{step_key}_result'] = result
                    
                    print(f"✅ {stage['name']} completed\n")
                except Exception as e:
                    stage['status'] = 'failed'
                    stage['error'] = str(e)
                    print(f"❌ {stage['name']} failed: {e}\n")
                    
                    if not pause_between_steps:
                        # Stop on error unless in step-by-step mode
                        workflow['status'] = 'failed'
                        return workflow
            else:
                # No handler registered - mark as skipped
                stage['status'] = 'skipped'
                print(f"⚠️  No handler registered for '{step_key}' - skipped\n")
            
            # Update workflow in memory
            self.memory.store('workflow', workflow)
            
            # Pause for review if requested
            if pause_between_steps and i < len(workflow['stages']):
                input(f"\n⏸️  Press Enter to continue to next step...")
        
        workflow['status'] = 'completed'
        print("🎉 Workflow execution completed!")
        return workflow
    
    def execute_single_step(self, step_key: str, context: Optional[Dict] = None) -> Dict:
        """Execute a single workflow step independently
        
        Args:
            step_key: Step identifier (e.g., 'ba', 'architect')
            context: Optional context data
            
        Returns:
            Result from step execution
        """
        if step_key not in self.AVAILABLE_STEPS:
            raise ValueError(f"Invalid step: {step_key}. Available: {list(self.AVAILABLE_STEPS.keys())}")
        
        step_info = self.AVAILABLE_STEPS[step_key]
        print(f"\n🎯 Executing single step: {step_info['name']}")
        print(f"{'='*60}\n")
        
        context = context or {}
        
        if step_key in self.step_handlers:
            result = self.step_handlers[step_key](context)
            print(f"\n✅ {step_info['name']} completed")
            return result
        else:
            print(f"⚠️  No handler registered for '{step_key}'")
            return {"status": "no_handler"}
    
    def get_available_steps(self) -> List[str]:
        """Returns list of available workflow steps"""
        return list(self.AVAILABLE_STEPS.keys())
    
    def get_step_info(self, step_key: str) -> Dict:
        """Get information about a specific step"""
        return self.AVAILABLE_STEPS.get(step_key, {})
