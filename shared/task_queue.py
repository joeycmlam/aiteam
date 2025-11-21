"""
Task Queue - Distributed task queue for parallel agent work

Features:
- Priority-based task scheduling
- Task dependencies management
- Agent assignment tracking
- Status monitoring
- Task completion tracking
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import json


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class Task:
    """Individual task"""
    
    def __init__(self,
                 task_id: str,
                 name: str,
                 description: str,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 required_skills: List[str] = None,
                 dependencies: List[str] = None,
                 metadata: Dict = None):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.priority = priority
        self.required_skills = required_skills or []
        self.dependencies = dependencies or []
        self.metadata = metadata or {}
        
        self.status = TaskStatus.PENDING
        self.assigned_to = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            'task_id': self.task_id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority.value,
            'required_skills': self.required_skills,
            'dependencies': self.dependencies,
            'metadata': self.metadata,
            'status': self.status.value,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def can_start(self, completed_tasks: List[str]) -> bool:
        """Check if task can start based on dependencies"""
        if not self.dependencies:
            return True
        return all(dep in completed_tasks for dep in self.dependencies)


class TaskQueue:
    """Manages task queue and distribution"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.completed_task_ids: List[str] = []
        self.task_counter = 0
        
        print("📋 Task Queue initialized")
    
    def add_task(self,
                 name: str,
                 description: str,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 required_skills: List[str] = None,
                 dependencies: List[str] = None,
                 metadata: Dict = None) -> str:
        """
        Add a new task to the queue
        
        Args:
            name: Task name
            description: Task description
            priority: Task priority
            required_skills: Required skills for the task
            dependencies: Task IDs that must complete first
            metadata: Additional task metadata
            
        Returns:
            task_id: Generated task ID
        """
        self.task_counter += 1
        task_id = f"TASK-{self.task_counter:04d}"
        
        task = Task(
            task_id=task_id,
            name=name,
            description=description,
            priority=priority,
            required_skills=required_skills,
            dependencies=dependencies,
            metadata=metadata
        )
        
        self.tasks[task_id] = task
        print(f"   ✅ Task added: {task_id} - {name} (Priority: {priority.name})")
        
        return task_id
    
    def get_next_task(self,
                     agent_skills: List[str] = None,
                     assigned_agent: str = None) -> Optional[Task]:
        """
        Get next available task for an agent
        
        Args:
            agent_skills: Skills available to the agent
            assigned_agent: Agent requesting task
            
        Returns:
            Next available task or None
        """
        available_tasks = []
        
        for task in self.tasks.values():
            # Skip if not pending
            if task.status != TaskStatus.PENDING:
                continue
            
            # Check if dependencies are met
            if not task.can_start(self.completed_task_ids):
                continue
            
            # Check skill match if provided
            if agent_skills and task.required_skills:
                if not any(skill in agent_skills for skill in task.required_skills):
                    continue
            
            available_tasks.append(task)
        
        if not available_tasks:
            return None
        
        # Sort by priority (lower number = higher priority)
        available_tasks.sort(key=lambda t: t.priority.value)
        
        # Assign task
        next_task = available_tasks[0]
        next_task.status = TaskStatus.ASSIGNED
        next_task.assigned_to = assigned_agent
        
        return next_task
    
    def start_task(self, task_id: str) -> bool:
        """Mark task as in progress"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        print(f"   ▶️  Task started: {task_id} by {task.assigned_to}")
        return True
    
    def complete_task(self, task_id: str, result: Any = None) -> bool:
        """Mark task as completed"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.result = result
        
        self.completed_task_ids.append(task_id)
        
        print(f"   ✅ Task completed: {task_id}")
        return True
    
    def fail_task(self, task_id: str, error: str) -> bool:
        """Mark task as failed"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.error = error
        
        print(f"   ❌ Task failed: {task_id} - {error}")
        return True
    
    def block_task(self, task_id: str, reason: str) -> bool:
        """Mark task as blocked"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = TaskStatus.BLOCKED
        task.metadata['blocked_reason'] = reason
        
        print(f"   🚫 Task blocked: {task_id} - {reason}")
        return True
    
    def unblock_task(self, task_id: str) -> bool:
        """Unblock a task"""
        task = self.tasks.get(task_id)
        if not task or task.status != TaskStatus.BLOCKED:
            return False
        
        task.status = TaskStatus.PENDING
        if 'blocked_reason' in task.metadata:
            del task.metadata['blocked_reason']
        
        print(f"   ✅ Task unblocked: {task_id}")
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with specific status"""
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_tasks_by_agent(self, agent_name: str) -> List[Task]:
        """Get all tasks assigned to an agent"""
        return [t for t in self.tasks.values() if t.assigned_to == agent_name]
    
    def get_statistics(self) -> Dict:
        """Get queue statistics"""
        total = len(self.tasks)
        by_status = {}
        
        for status in TaskStatus:
            count = len(self.get_tasks_by_status(status))
            by_status[status.value] = count
        
        return {
            'total_tasks': total,
            'by_status': by_status,
            'completed': len(self.completed_task_ids),
            'pending': by_status.get(TaskStatus.PENDING.value, 0),
            'in_progress': by_status.get(TaskStatus.IN_PROGRESS.value, 0),
            'blocked': by_status.get(TaskStatus.BLOCKED.value, 0),
            'failed': by_status.get(TaskStatus.FAILED.value, 0)
        }
    
    def print_status(self):
        """Print formatted queue status"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("📋 TASK QUEUE STATUS")
        print("="*70)
        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"")
        print(f"Status Breakdown:")
        print(f"  ⏳ Pending:     {stats['pending']}")
        print(f"  ▶️  In Progress: {stats['in_progress']}")
        print(f"  ✅ Completed:   {stats['completed']}")
        print(f"  🚫 Blocked:     {stats['blocked']}")
        print(f"  ❌ Failed:      {stats['failed']}")
        print("="*70 + "\n")
    
    def print_task_list(self, status: TaskStatus = None):
        """Print list of tasks"""
        if status:
            tasks = self.get_tasks_by_status(status)
            print(f"\n📋 Tasks with status: {status.value.upper()}")
        else:
            tasks = list(self.tasks.values())
            print(f"\n📋 All Tasks")
        
        print("-" * 70)
        
        for task in sorted(tasks, key=lambda t: t.priority.value):
            status_icon = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.ASSIGNED: "📌",
                TaskStatus.IN_PROGRESS: "▶️",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.BLOCKED: "🚫",
                TaskStatus.FAILED: "❌"
            }.get(task.status, "❓")
            
            assigned = task.assigned_to or "Unassigned"
            deps = f" (deps: {', '.join(task.dependencies)})" if task.dependencies else ""
            
            print(f"{status_icon} {task.task_id} [{task.priority.name:8}] {task.name}")
            print(f"   Assigned: {assigned}{deps}")
        
        print("-" * 70 + "\n")
    
    def export_to_json(self, filepath: str):
        """Export queue to JSON file"""
        data = {
            'tasks': [task.to_dict() for task in self.tasks.values()],
            'completed_task_ids': self.completed_task_ids,
            'statistics': self.get_statistics()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Task queue exported to: {filepath}")


if __name__ == "__main__":
    # Demo usage
    print("Task Queue Demo\n")
    
    queue = TaskQueue()
    
    # Add tasks with dependencies
    task1 = queue.add_task(
        "Design database schema",
        "Create database schema for user management",
        priority=TaskPriority.HIGH,
        required_skills=['database', 'sql']
    )
    
    task2 = queue.add_task(
        "Implement authentication API",
        "Create API endpoints for user authentication",
        priority=TaskPriority.HIGH,
        required_skills=['backend', 'api'],
        dependencies=[task1]
    )
    
    task3 = queue.add_task(
        "Create login UI",
        "Build login form and UI components",
        priority=TaskPriority.MEDIUM,
        required_skills=['frontend', 'react'],
        dependencies=[task2]
    )
    
    task4 = queue.add_task(
        "Write unit tests",
        "Create unit tests for authentication",
        priority=TaskPriority.MEDIUM,
        required_skills=['testing']
    )
    
    # Show initial status
    queue.print_status()
    queue.print_task_list()
    
    # Simulate task processing
    print("\n🔄 Processing tasks...\n")
    
    # Get next task for DBA
    task = queue.get_next_task(['database', 'sql'], 'DBA')
    if task:
        queue.start_task(task.task_id)
        queue.complete_task(task.task_id, {"schema": "users table created"})
    
    # Get next task for Backend Dev
    task = queue.get_next_task(['backend', 'api'], 'Backend-Dev')
    if task:
        queue.start_task(task.task_id)
        queue.complete_task(task.task_id, {"api": "authentication endpoints"})
    
    # Show updated status
    queue.print_status()
    queue.print_task_list()
