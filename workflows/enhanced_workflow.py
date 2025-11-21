"""
Enhanced AI Workflow Orchestrator with JIRA Integration
Handles: JIRA → BA → Tech Lead → Developer workflow
"""
import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.jira_agent import JiraAgent
from agents.ba_agent import BAAgent
from agents.tech_lead_agent import TechLeadAgent
from agents.developer_agent import DeveloperAgent
from shared.memory_store import MemoryStore


class EnhancedWorkflowOrchestrator:
    """
    Orchestrates the complete workflow from JIRA to implementation
    """
    
    def __init__(self, 
                 requirements_dir: str = "requirements",
                 architecture_dir: str = "architecture", 
                 technical_dir: str = "technical_structure",
                 implementation_dir: str = "implementation"):
        
        self.requirements_dir = requirements_dir
        self.architecture_dir = architecture_dir
        self.technical_dir = technical_dir
        self.implementation_dir = implementation_dir
        
        # Create directories
        for directory in [requirements_dir, architecture_dir, technical_dir, implementation_dir]:
            os.makedirs(directory, exist_ok=True)
            os.makedirs(f"{directory}/analysis", exist_ok=True)
        
        # Initialize agents
        self.jira_agent = None
        self.ba_agent = BAAgent(output_dir=f"{requirements_dir}/analysis")
        self.tech_lead_agent = TechLeadAgent(output_dir=technical_dir)
        self.developer_agent = DeveloperAgent(output_dir=implementation_dir)
        
        # Memory store for context passing
        self.memory = MemoryStore()
        
        print("🚀 Enhanced Workflow Orchestrator initialized")
    
    def initialize_jira(self, jira_url: str = None, jira_email: str = None, jira_token: str = None):
        """Initialize JIRA connection"""
        try:
            self.jira_agent = JiraAgent(jira_url, jira_email, jira_token)
            return True
        except Exception as e:
            print(f"⚠️  JIRA initialization failed: {e}")
            return False
    
    def run_workflow(self, jira_key: str = None, requirements_file: str = None):
        """
        Run the complete workflow
        
        Args:
            jira_key: JIRA issue key (e.g., 'PROJ-123')
            requirements_file: Path to existing requirements file (alternative to JIRA)
        """
        print("\n" + "="*70)
        print("🎯 STARTING AI WORKFLOW")
        print("="*70)
        
        context = {}
        
        # STEP 1: JIRA Integration (if JIRA key provided)
        if jira_key:
            print("\n📌 STEP 1: Fetching from JIRA")
            print("-"*70)
            
            if not self.jira_agent:
                print("❌ JIRA agent not initialized. Use --jira-url, --jira-email, --jira-token")
                return
            
            try:
                # Fetch issue
                issue_data = self.jira_agent.fetch_issue(jira_key)
                
                # Check completeness
                completeness = self.jira_agent.analyze_completeness(issue_data)
                print(f"\n📊 Completeness: {'✅ PASS' if completeness['is_complete'] else '❌ FAIL'}")
                
                if not completeness['is_complete']:
                    print(f"❌ Missing: {', '.join(completeness['missing_fields'])}")
                    print("⚠️  Cannot proceed without complete information")
                    return
                
                if completeness['warnings']:
                    print(f"⚠️  Warnings: {', '.join(completeness['warnings'])}")
                
                # Generate requirements document
                req_file = f"{self.requirements_dir}/{jira_key.replace('-', '_')}_requirement.md"
                self.jira_agent.prepare_requirements_document(jira_key, req_file)
                
                context['jira_key'] = jira_key
                context['requirements_file'] = req_file
                requirements_file = req_file
                
                print(f"✅ JIRA Step Complete")
                
            except Exception as e:
                print(f"❌ JIRA step failed: {e}")
                return
        
        # STEP 2: BA Agent (Requirements Analysis)
        if requirements_file:
            print("\n📌 STEP 2: BA Agent - Requirements Analysis")
            print("-"*70)
            
            try:
                # Read requirements
                with open(requirements_file, 'r') as f:
                    requirements = f.read()
                
                context['requirements'] = requirements
                
                # Analyze with BA Agent
                ba_outputs = self.ba_agent.gather_requirements(requirements_text=requirements)
                context['ba_analysis'] = ba_outputs
                
                print(f"✅ BA Analysis Complete")
                print(f"   📄 Analysis: {ba_outputs.get('analysis_file')}")
                print(f"   📄 Stories: {ba_outputs.get('feature_file')}")
                
            except Exception as e:
                print(f"❌ BA step failed: {e}")
                return
        else:
            print("❌ No requirements file provided")
            return
        
        # STEP 3: Tech Lead Agent (Technical Design)
        print("\n📌 STEP 3: Tech Lead Agent - Technical Design")
        print("-"*70)
        
        try:
            # First need architecture (you might want to add ArchitectAgent here)
            # For now, assuming architecture exists or Tech Lead creates it
            
            ba_analysis = context.get('ba_analysis', {})
            
            # Design technical structure
            tech_structure = self.tech_lead_agent.design_technical_structure(
                architecture_design=None,  # Add architecture if available
                ba_analysis=ba_analysis.get('structured_data')
            )
            
            # Break down into tasks
            tasks = self.tech_lead_agent.breakdown_tasks(
                architecture_design=None,
                ba_analysis=ba_analysis.get('structured_data')
            )
            
            context['technical_structure'] = tech_structure
            context['development_tasks'] = tasks
            
            print(f"✅ Technical Design Complete")
            print(f"   📄 Structure: {self.technical_dir}/technical_structure.md")
            print(f"   📄 Tasks: {self.technical_dir}/development_tasks.md")
            
        except Exception as e:
            print(f"❌ Tech Lead step failed: {e}")
            return
        
        # STEP 4: Developer Agent (Implementation)
        print("\n📌 STEP 4: Developer Agent - Implementation")
        print("-"*70)
        
        try:
            tech_structure = context.get('technical_structure')
            tasks = context.get('development_tasks')
            
            if not tech_structure:
                print("⚠️  No technical structure available, skipping implementation")
                return
            
            # Implement based on technical structure
            # (You'll need to implement this method in developer_agent.py)
            print("🔨 Developer Agent starting implementation...")
            print(f"   Based on: {self.technical_dir}/technical_structure.md")
            
            # TODO: Implement actual code generation
            print("⚠️  Developer implementation pending - agent needs enhancement")
            
        except Exception as e:
            print(f"❌ Developer step failed: {e}")
        
        # Save workflow context
        self.memory.store("workflow", context)
        
        print("\n" + "="*70)
        print("✅ WORKFLOW COMPLETED")
        print("="*70)
        self._print_summary(context)
    
    def _print_summary(self, context: dict):
        """Print workflow summary"""
        print("\n📊 WORKFLOW SUMMARY")
        print("-"*70)
        
        if context.get('jira_key'):
            print(f"📌 JIRA Issue: {context['jira_key']}")
        
        if context.get('requirements_file'):
            print(f"📄 Requirements: {context['requirements_file']}")
        
        if context.get('ba_analysis'):
            print(f"📄 BA Analysis: {context['ba_analysis'].get('analysis_file')}")
        
        if context.get('technical_structure'):
            print(f"📄 Technical Design: {self.technical_dir}/technical_structure.md")
        
        print("\n💡 Next Steps:")
        print("   1. Review technical structure")
        print("   2. Review development tasks")
        print("   3. Begin implementation following the tasks")


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced AI Workflow with JIRA Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From JIRA issue
  python enhanced_workflow.py --jira PROJ-123 --jira-url https://company.atlassian.net --jira-email user@company.com --jira-token YOUR_TOKEN
  
  # From requirements file
  python enhanced_workflow.py --requirements requirements/user_requirement.md
  
  # Full workflow with all outputs
  python enhanced_workflow.py --jira PROJ-123 --req-dir requirements --arch-dir architecture --tech-dir technical --impl-dir implementation
        """
    )
    
    # JIRA options
    parser.add_argument('--jira', type=str, help='JIRA issue key (e.g., PROJ-123)')
    parser.add_argument('--jira-url', type=str, help='JIRA URL (or set JIRA_URL env var)')
    parser.add_argument('--jira-email', type=str, help='JIRA email (or set JIRA_EMAIL env var)')
    parser.add_argument('--jira-token', type=str, help='JIRA API token (or set JIRA_API_TOKEN env var)')
    
    # Alternative: Requirements file
    parser.add_argument('--requirements', '-r', type=str, help='Path to requirements file')
    
    # Output directories
    parser.add_argument('--req-dir', type=str, default='requirements', help='Requirements directory')
    parser.add_argument('--arch-dir', type=str, default='architecture', help='Architecture directory')
    parser.add_argument('--tech-dir', type=str, default='technical_structure', help='Technical structure directory')
    parser.add_argument('--impl-dir', type=str, default='implementation', help='Implementation directory')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.jira and not args.requirements:
        parser.error("Either --jira or --requirements must be provided")
    
    # Initialize orchestrator
    orchestrator = EnhancedWorkflowOrchestrator(
        requirements_dir=args.req_dir,
        architecture_dir=args.arch_dir,
        technical_dir=args.tech_dir,
        implementation_dir=args.impl_dir
    )
    
    # Initialize JIRA if needed
    if args.jira:
        success = orchestrator.initialize_jira(
            jira_url=args.jira_url,
            jira_email=args.jira_email,
            jira_token=args.jira_token
        )
        if not success:
            print("❌ Failed to initialize JIRA. Check credentials.")
            sys.exit(1)
    
    # Run workflow
    orchestrator.run_workflow(
        jira_key=args.jira,
        requirements_file=args.requirements
    )


if __name__ == "__main__":
    main()
