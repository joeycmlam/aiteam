"""
Test suite for multi-agent system
Tests DBA Agent, DevOps Agent, Developer Pool, Task Queue, and Collaboration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agents.dba_agent import DBAAgent
from agents.devops_agent import DevOpsAgent
from agents.developer_pool import DeveloperPool, DeveloperSpecialization
from shared.task_queue import TaskQueue, TaskPriority, TaskStatus
from shared.agent_collaboration import AgentCollaboration, CollaborationPattern


# Test configuration
LLM_CONFIG = {
    'provider': 'ollama',
    'model': 'llama3.2',
    'temperature': 0.3
}


class TestDBAAgent:
    """Test DBA Agent functionality"""
    
    def test_dba_initialization(self):
        """Test DBA agent initializes correctly"""
        dba = DBAAgent(LLM_CONFIG)
        assert dba is not None
        print("✅ DBA Agent initialized")
    
    def test_schema_design(self):
        """Test database schema design"""
        dba = DBAAgent(LLM_CONFIG)
        
        requirements = {
            'features': ['User management', 'Product catalog'],
            'entities': ['User', 'Product', 'Order']
        }
        
        schema = dba.design_schema(requirements)
        
        assert schema is not None
        assert 'tables' in schema
        assert len(schema['tables']) > 0
        print(f"✅ Schema designed with {len(schema['tables'])} tables")
    
    def test_migration_generation(self):
        """Test migration script generation"""
        dba = DBAAgent(LLM_CONFIG)
        
        current_schema = {'tables': []}
        new_requirements = {'features': ['Add authentication']}
        
        migrations = dba.generate_migrations(current_schema, new_requirements)
        
        assert migrations is not None
        assert 'migrations' in migrations
        print(f"✅ Generated {len(migrations['migrations'])} migrations")


class TestDevOpsAgent:
    """Test DevOps Agent functionality"""
    
    def test_devops_initialization(self):
        """Test DevOps agent initializes correctly"""
        devops = DevOpsAgent(LLM_CONFIG)
        assert devops is not None
        print("✅ DevOps Agent initialized")
    
    def test_pipeline_design(self):
        """Test CI/CD pipeline design"""
        devops = DevOpsAgent(LLM_CONFIG)
        
        project_info = {
            'technology_stack': {
                'language': 'python',
                'framework': 'fastapi'
            },
            'requirements': {
                'environments': ['dev', 'prod']
            }
        }
        
        pipeline = devops.design_cicd_pipeline(project_info)
        
        assert pipeline is not None
        assert 'stages' in pipeline
        assert len(pipeline['stages']) > 0
        print(f"✅ Pipeline designed with {len(pipeline['stages'])} stages")
    
    def test_dockerfile_generation(self):
        """Test Dockerfile generation"""
        devops = DevOpsAgent(LLM_CONFIG)
        
        tech_stack = {
            'language': 'python',
            'framework': 'fastapi'
        }
        
        dockerfile = devops.generate_dockerfile(tech_stack)
        
        assert dockerfile is not None
        assert 'FROM' in dockerfile
        print("✅ Dockerfile generated")


class TestDeveloperPool:
    """Test Developer Pool functionality"""
    
    def test_pool_initialization(self):
        """Test developer pool initializes correctly"""
        config = {
            'frontend': {'count': 2},
            'backend': {'count': 2},
            'fullstack': {'count': 1}
        }
        
        pool = DeveloperPool(LLM_CONFIG, config)
        
        assert pool is not None
        assert len(pool.developers) == 5
        print(f"✅ Developer pool initialized with {len(pool.developers)} developers")
    
    def test_task_assignment(self):
        """Test task assignment to developers"""
        config = {
            'frontend': {'count': 2},
            'backend': {'count': 1}
        }
        
        pool = DeveloperPool(LLM_CONFIG, config)
        
        task = {
            'name': 'Create login UI',
            'type': 'frontend',
            'required_skills': ['react', 'typescript']
        }
        
        developer = pool.assign_task(task)
        
        assert developer is not None
        assert 'Frontend' in developer.developer_id
        print(f"✅ Task assigned to {developer.developer_id}")
    
    def test_team_status(self):
        """Test team status retrieval"""
        config = {
            'frontend': {'count': 1},
            'backend': {'count': 1},
            'fullstack': {'count': 1}
        }
        
        pool = DeveloperPool(LLM_CONFIG, config)
        status = pool.get_team_status()
        
        assert status is not None
        assert status['total_developers'] == 3
        assert status['available'] == 3
        print("✅ Team status retrieved")


class TestTaskQueue:
    """Test Task Queue functionality"""
    
    def test_queue_initialization(self):
        """Test task queue initializes correctly"""
        queue = TaskQueue()
        assert queue is not None
        print("✅ Task queue initialized")
    
    def test_add_task(self):
        """Test adding tasks to queue"""
        queue = TaskQueue()
        
        task_id = queue.add_task(
            "Implement feature X",
            "Create feature X with tests",
            priority=TaskPriority.HIGH,
            required_skills=['python']
        )
        
        assert task_id is not None
        assert task_id.startswith('TASK-')
        print(f"✅ Task added: {task_id}")
    
    def test_task_dependencies(self):
        """Test task dependency handling"""
        queue = TaskQueue()
        
        task1 = queue.add_task("Task 1", "First task")
        task2 = queue.add_task(
            "Task 2", 
            "Second task",
            dependencies=[task1]
        )
        
        # Task 2 should not be available yet
        next_task = queue.get_next_task()
        assert next_task.task_id == task1
        
        # Complete task 1
        queue.start_task(task1)
        queue.complete_task(task1)
        
        # Now task 2 should be available
        next_task = queue.get_next_task()
        assert next_task.task_id == task2
        
        print("✅ Task dependencies working correctly")
    
    def test_task_priority(self):
        """Test priority-based task ordering"""
        queue = TaskQueue()
        
        task_low = queue.add_task("Low priority", "desc", TaskPriority.LOW)
        task_high = queue.add_task("High priority", "desc", TaskPriority.HIGH)
        task_critical = queue.add_task("Critical", "desc", TaskPriority.CRITICAL)
        
        # Should get critical task first
        next_task = queue.get_next_task()
        assert next_task.task_id == task_critical
        
        print("✅ Priority ordering working correctly")
    
    def test_queue_statistics(self):
        """Test queue statistics"""
        queue = TaskQueue()
        
        queue.add_task("Task 1", "Description")
        queue.add_task("Task 2", "Description")
        
        stats = queue.get_statistics()
        
        assert stats['total_tasks'] == 2
        assert stats['pending'] == 2
        print("✅ Queue statistics retrieved")


class TestAgentCollaboration:
    """Test Agent Collaboration functionality"""
    
    def test_collaboration_initialization(self):
        """Test collaboration system initializes correctly"""
        collab = AgentCollaboration()
        assert collab is not None
        print("✅ Collaboration system initialized")
    
    def test_pair_programming(self):
        """Test pair programming session"""
        collab = AgentCollaboration()
        
        session = collab.start_pair_programming(
            "Dev-1",
            "Dev-2",
            {'name': 'Build feature', 'type': 'implementation'}
        )
        
        assert session is not None
        assert session.pattern == CollaborationPattern.PAIR_PROGRAMMING
        assert len(session.participants) == 2
        print(f"✅ Pair programming session started: {session.session_id}")
    
    def test_code_review(self):
        """Test code review session"""
        collab = AgentCollaboration()
        
        session = collab.start_code_review(
            "Developer",
            "Tech Lead",
            {'files': ['main.py']}
        )
        
        assert session is not None
        assert session.pattern == CollaborationPattern.CODE_REVIEW
        print(f"✅ Code review session started: {session.session_id}")
    
    def test_cross_functional_review(self):
        """Test cross-functional review"""
        collab = AgentCollaboration()
        
        session = collab.start_cross_functional_review(
            {'type': 'API Implementation'},
            ['Tech Lead', 'QA', 'DBA', 'DevOps']
        )
        
        assert session is not None
        assert session.pattern == CollaborationPattern.CROSS_FUNCTIONAL_REVIEW
        assert len(session.participants) == 4
        print(f"✅ Cross-functional review started: {session.session_id}")
    
    def test_session_contributions(self):
        """Test adding contributions to session"""
        collab = AgentCollaboration()
        
        session = collab.start_pair_programming(
            "Dev-1", "Dev-2",
            {'name': 'Feature'}
        )
        
        collab.add_contribution_to_session(
            session.session_id,
            "Dev-1",
            {'code': 'implementation'}
        )
        
        assert len(session.contributions) == 1
        print("✅ Contribution added to session")
    
    def test_end_session(self):
        """Test ending collaboration session"""
        collab = AgentCollaboration()
        
        session = collab.start_pair_programming(
            "Dev-1", "Dev-2",
            {'name': 'Feature'}
        )
        
        session_id = session.session_id
        collab.end_collaboration(session_id, "Session completed successfully")
        
        assert session_id not in collab.active_sessions
        assert len(collab.completed_sessions) == 1
        print("✅ Session ended successfully")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 RUNNING MULTI-AGENT SYSTEM TESTS")
    print("="*70 + "\n")
    
    # DBA Tests
    print("Testing DBA Agent...")
    test_dba = TestDBAAgent()
    test_dba.test_dba_initialization()
    test_dba.test_schema_design()
    test_dba.test_migration_generation()
    
    # DevOps Tests
    print("\nTesting DevOps Agent...")
    test_devops = TestDevOpsAgent()
    test_devops.test_devops_initialization()
    test_devops.test_pipeline_design()
    test_devops.test_dockerfile_generation()
    
    # Developer Pool Tests
    print("\nTesting Developer Pool...")
    test_pool = TestDeveloperPool()
    test_pool.test_pool_initialization()
    test_pool.test_task_assignment()
    test_pool.test_team_status()
    
    # Task Queue Tests
    print("\nTesting Task Queue...")
    test_queue = TestTaskQueue()
    test_queue.test_queue_initialization()
    test_queue.test_add_task()
    test_queue.test_task_dependencies()
    test_queue.test_task_priority()
    test_queue.test_queue_statistics()
    
    # Collaboration Tests
    print("\nTesting Agent Collaboration...")
    test_collab = TestAgentCollaboration()
    test_collab.test_collaboration_initialization()
    test_collab.test_pair_programming()
    test_collab.test_code_review()
    test_collab.test_cross_functional_review()
    test_collab.test_session_contributions()
    test_collab.test_end_session()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
