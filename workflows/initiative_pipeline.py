#!/usr/bin/env python3
"""
Initiative Pipeline - Fetch and process a JIRA Initiative/Epic

This pipeline:
1. Fetches a specific JIRA initiative (e.g., SCRUM-5)
2. Retrieves all linked issues (stories, tasks, bugs)
3. Structures requirements using AI
4. Analyzes legacy code
5. Generates implementation plan
6. Creates test cases
7. Generates code implementation
8. Performs code review

Usage:
    python3 workflows/initiative_pipeline.py SCRUM-5
    python3 workflows/initiative_pipeline.py --help
"""

import os
import sys
import yaml
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all agents
from agents.lead_orchestrator import LeadOrchestrator
from agents.architect_agent import ArchitectAgent
from agents.ba_agent import BAAgent
from agents.qa_agent import QAAgent
from agents.tech_lead_agent import TechLeadAgent
from agents.developer_agent import DeveloperAgent
from shared.memory_store import SharedMemory

class InitiativePipeline:
    """Pipeline for processing JIRA initiatives"""
    
    def __init__(self, config_path: str = 'config/agent_config.yaml'):
        # Load environment variables
        load_dotenv(override=True)
        
        # Load configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        llm_config = config['llm']
        jira_config = {
            'server': os.getenv('JIRA_SERVER') or config['jira']['server'],
            'user': os.getenv('JIRA_USER') or config['jira']['user'],
            'token': os.getenv('JIRA_API_TOKEN')
        }
        
        # Validate JIRA configuration
        if not jira_config['token']:
            print("⚠️  WARNING: JIRA_API_TOKEN not found in .env file")
            print("   The pipeline will use mock data instead of real JIRA data")
        
        # Initialize shared memory
        self.memory = SharedMemory('./memory_initiative.json')
        
        # Initialize all agents
        print("\n" + "="*70)
        print("🚀 Initializing AI Agents for Initiative Processing")
        print("="*70)
        print(f"   LLM Provider: {llm_config['provider']}")
        print(f"   Model: {llm_config.get('model', 'default')}")
        print(f"   JIRA Server: {jira_config['server']}")
        print("="*70 + "\n")
        
        self.lead = LeadOrchestrator(llm_config)
        self.architect = ArchitectAgent(llm_config)
        self.ba = BAAgent(llm_config, jira_config)
        self.qa = QAAgent(llm_config)
        self.senior_dev = TechLeadAgent(llm_config)
        self.developer = DeveloperAgent(llm_config)
        
        print("="*70)
        print("✅ All agents initialized successfully\n")
    
    def process_initiative(self, issue_key: str):
        """Process a JIRA initiative end-to-end"""
        
        print("\n" + "="*70)
        print(f"🎯 INITIATIVE PIPELINE - {issue_key}")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # Stage 1: Fetch Initiative from JIRA
        print("╔" + "="*68 + "╗")
        print("║" + " "*20 + "STAGE 1: FETCH INITIATIVE" + " "*23 + "║")
        print("╚" + "="*68 + "╝\n")
        
        initiative = self.ba.fetch_initiative(issue_key)
        self.memory.store('initiative', initiative)
        
        print(f"\n📊 Initiative Summary:")
        print(f"   Key: {initiative['key']}")
        print(f"   Title: {initiative['summary']}")
        print(f"   Type: {initiative['type']}")
        print(f"   Status: {initiative['status']}")
        print(f"   Priority: {initiative['priority']}")
        print(f"   Linked Issues: {len(initiative['linked_issues'])}")
        
        # Stage 2: Structure Requirements
        print("\n\n╔" + "="*68 + "╗")
        print("║" + " "*18 + "STAGE 2: STRUCTURE REQUIREMENTS" + " "*19 + "║")
        print("╚" + "="*68 + "╝\n")
        
        requirements = self.ba.structure_requirements_from_initiative(initiative)
        self.memory.store('requirements', requirements)
        
        print(f"\n📝 Requirements Structured:")
        print(f"   User Stories: {len(requirements.get('user_stories', []))}")
        print(f"   Technical Tasks: {len(requirements.get('technical_tasks', []))}")
        
        # Stage 3: Analyze Architecture
        print("\n\n╔" + "="*68 + "╗")
        print("║" + " "*18 + "STAGE 3: ANALYZE ARCHITECTURE" + " "*21 + "║")
        print("╚" + "="*68 + "╝\n")
        
        # Get legacy code path
        legacy_path = os.getenv('LEGACY_CODE_PATH', 'tests/fixtures/legacy_code.py')
        
        if os.path.exists(legacy_path):
            print(f"   📁 Analyzing legacy code: {legacy_path}")
            architecture = self.architect.analyze_codebase(legacy_path)
        else:
            print(f"   ⚠️  Legacy code not found: {legacy_path}")
            print(f"   💡 Using demo analysis instead")
            architecture = {
                "patterns": ["MVC", "Repository Pattern"],
                "technologies": ["Python", "Flask"],
                "complexity": "Medium",
                "recommendations": [
                    "Modernize authentication",
                    "Implement dependency injection",
                    "Add comprehensive logging"
                ]
            }
        
        self.memory.store('architecture', architecture)
        print(f"\n🏗️  Architecture Analysis Complete")
        
        # Stage 4: Generate Test Cases
        print("\n\n╔" + "="*68 + "╗")
        print("║" + " "*20 + "STAGE 4: GENERATE TESTS" + " "*25 + "║")
        print("╚" + "="*68 + "╝\n")
        
        # Create tests directory
        tests_dir = 'tests/features'
        os.makedirs(tests_dir, exist_ok=True)
        
        self.qa.create_feature_files(requirements, tests_dir)
        
        print(f"\n🧪 Test Cases Generated in: {tests_dir}")
        
        # Stage 5: Get Implementation Guidelines
        print("\n\n╔" + "="*68 + "╗")
        print("║" + " "*16 + "STAGE 5: IMPLEMENTATION GUIDELINES" + " "*18 + "║")
        print("╚" + "="*68 + "╝\n")
        
        guidelines = self.senior_dev.provide_guidelines({
            'requirements': requirements,
            'architecture': architecture
        })
        self.memory.store('guidelines', guidelines)
        
        print(f"\n📋 Guidelines Generated")
        
        # Stage 6: Generate Implementation
        print("\n\n╔" + "="*68 + "╗")
        print("║" + " "*18 + "STAGE 6: GENERATE IMPLEMENTATION" + " "*19 + "║")
        print("╚" + "="*68 + "╝\n")
        
        implementation = self.developer.implement_feature(requirements, guidelines)
        self.memory.store('implementation', implementation)
        
        print(f"\n💻 Implementation Generated")
        
        # Stage 7: Code Review
        print("\n\n╔" + "="*68 + "╗")
        print("║" + " "*22 + "STAGE 7: CODE REVIEW" + " "*27 + "║")
        print("╚" + "="*68 + "╝\n")
        
        # Extract code from implementation
        code_to_review = implementation.get('code', str(implementation))
        
        review = self.senior_dev.review_code(code_to_review, requirements)
        self.memory.store('review', review)
        
        print(f"\n👨‍💼 Code Review Complete")
        
        # Final Summary
        print("\n\n" + "="*70)
        print("🎉 INITIATIVE PIPELINE COMPLETED")
        print("="*70)
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        print(f"\n📂 Results saved to: ./memory_initiative.json")
        print(f"\n✅ Next Steps:")
        print(f"   1. Review requirements in memory_initiative.json")
        print(f"   2. Check test cases")
        print(f"   3. Review implementation code")
        print(f"   4. Apply code review feedback")
        
        return {
            'initiative': initiative,
            'requirements': requirements,
            'architecture': architecture,
            'guidelines': guidelines,
            'implementation': implementation,
            'review': review
        }

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Process a JIRA Initiative with AI agents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process initiative SCRUM-5
  python3 workflows/initiative_pipeline.py SCRUM-5
  
  # Process initiative with custom config
  python3 workflows/initiative_pipeline.py SCRUM-5 --config custom_config.yaml
  
  # Show help
  python3 workflows/initiative_pipeline.py --help

JIRA Setup:
  Make sure these environment variables are set in .env:
    JIRA_SERVER=https://your-domain.atlassian.net
    JIRA_USER=your-email@example.com
    JIRA_API_TOKEN=your-api-token
        """
    )
    
    parser.add_argument(
        'issue_key',
        nargs='?',
        default='SCRUM-5',
        help='JIRA issue key (e.g., SCRUM-5, EPIC-123)'
    )
    
    parser.add_argument(
        '--config',
        default='config/agent_config.yaml',
        help='Path to agent configuration file'
    )
    
    args = parser.parse_args()
    
    # Create and run pipeline
    try:
        pipeline = InitiativePipeline(args.config)
        results = pipeline.process_initiative(args.issue_key)
        
        print(f"\n✅ Pipeline completed successfully!")
        sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n❌ Pipeline failed with error:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
