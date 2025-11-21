"""
Complete Agent Workflow Orchestrator with Framework
Orchestrates BA → Tech Lead → Developer workflow using agent framework
"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.agent_framework import AgentChain
from agents.enhanced_ba_agent import EnhancedBAAgent
from agents.enhanced_tech_lead_agent import EnhancedTechLeadAgent
from agents.enhanced_developer_agent import EnhancedDeveloperAgent
from agents.jira_agent import JiraAgent


class CompleteWorkflowOrchestrator:
    """
    Orchestrates complete workflow from requirements to implementation
    Uses agent framework for proper agent chaining
    """
    
    def __init__(self, 
                 base_dir: str = "output",
                 jira_enabled: bool = False):
        self.base_dir = base_dir
        self.jira_enabled = jira_enabled
        
        # Create directories
        self.requirements_dir = f"{base_dir}/requirements"
        self.technical_dir = f"{base_dir}/technical"
        self.implementation_dir = f"{base_dir}/implementation"
        
        for directory in [self.requirements_dir, self.technical_dir, self.implementation_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize JIRA if enabled
        self.jira_agent = None
        if jira_enabled:
            self.jira_agent = JiraAgent()
        
        print("🚀 Complete Workflow Orchestrator initialized")
        print(f"📁 Base directory: {base_dir}")
    
    def run_full_workflow(self, 
                         requirements_source: str,
                         jira_key: str = None) -> dict:
        """
        Run complete BA → Tech Lead → Developer workflow
        
        Args:
            requirements_source: Path to requirements file or JIRA key
            jira_key: Optional JIRA issue key
            
        Returns:
            Dictionary with results from all agents
        """
        print("\n" + "="*70)
        print("🎯 STARTING COMPLETE WORKFLOW")
        print("="*70)
        print(f"📌 Requirements source: {requirements_source}")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # STEP 0: JIRA Integration (if enabled)
        requirements_file = requirements_source
        if self.jira_enabled and jira_key:
            print("📌 STEP 0: Fetching from JIRA")
            print("-"*70)
            
            try:
                # Fetch and save requirements
                requirements_file = f"{self.requirements_dir}/{jira_key.replace('-', '_')}_requirement.md"
                self.jira_agent.prepare_requirements_document(jira_key, requirements_file)
                
                # Check completeness
                issue_data = self.jira_agent.fetch_issue(jira_key)
                completeness = self.jira_agent.analyze_completeness(issue_data)
                
                if not completeness['is_complete']:
                    print(f"❌ JIRA issue incomplete: {completeness['missing_fields']}")
                    return {'status': 'failed', 'reason': 'incomplete_jira_issue'}
                
                print("✅ JIRA requirements fetched and validated\n")
                
            except Exception as e:
                print(f"❌ JIRA fetch failed: {e}")
                return {'status': 'failed', 'reason': str(e)}
        
        # Create agent chain
        chain = AgentChain(name="BA→TechLead→Developer Workflow")
        
        # Initialize agents
        ba_agent = EnhancedBAAgent(output_dir=f"{self.requirements_dir}/analysis")
        tech_lead_agent = EnhancedTechLeadAgent(output_dir=self.technical_dir)
        developer_agent = EnhancedDeveloperAgent(output_dir=self.implementation_dir)
        
        # Add agents to chain
        chain.add_agent(ba_agent)
        chain.add_agent(tech_lead_agent)
        chain.add_agent(developer_agent)
        
        # Set shared context
        chain.set_shared_context('project_name', 'Portfolio System')
        chain.set_shared_context('requirements_file', requirements_file)
        
        # Execute chain
        try:
            results = chain.execute(requirements_file)
            
            # Save execution log
            log_file = f"{self.base_dir}/execution_log.json"
            chain.save_execution_log(log_file)
            
            # Print final summary
            self._print_final_summary(results, chain)
            
            return {
                'status': 'success',
                'results': results,
                'execution_log': chain.get_execution_log()
            }
            
        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            return {
                'status': 'failed',
                'reason': str(e),
                'execution_log': chain.get_execution_log()
            }
    
    def _print_final_summary(self, results: dict, chain: AgentChain):
        """Print comprehensive workflow summary"""
        print("\n" + "="*70)
        print("📊 COMPLETE WORKFLOW SUMMARY")
        print("="*70)
        
        # BA Agent results
        if 'BA' in results:
            ba_results = results['BA']
            print(f"\n✅ BA Agent:")
            print(f"   📄 Analysis: {ba_results['files']['analysis']}")
            print(f"   📄 User Stories: {ba_results['files']['stories']}")
            print(f"   📄 Structured Data: {ba_results['files']['json']}")
        
        # Tech Lead results
        if 'TechLead' in results:
            tech_results = results['TechLead']
            print(f"\n✅ Tech Lead Agent:")
            print(f"   📄 Technical Structure: {tech_results['files']['structure']}")
            print(f"   📄 Development Tasks: {tech_results['files']['tasks']}")
            print(f"   📄 Guidelines: {tech_results['files']['guidelines']}")
            print(f"   📄 Structured Data: {tech_results['files']['json']}")
        
        # Developer results
        if 'Developer' in results:
            dev_results = results['Developer']
            print(f"\n✅ Developer Agent:")
            print(f"   📦 Modules created: {len(dev_results['code_modules'])}")
            print(f"   🧪 Tests created: {len(dev_results['tests'])}")
            print(f"   📄 Total files: {len(dev_results['files'])}")
        
        # Execution stats
        execution_log = chain.get_execution_log()
        total_duration = sum(
            entry.get('duration_seconds', 0) 
            for entry in execution_log
        )
        
        print(f"\n⏱️  Total execution time: {total_duration:.2f} seconds")
        print(f"📁 All outputs saved to: {self.base_dir}")
        
        print("\n💡 Next Steps:")
        print("   1. Review BA analysis and user stories")
        print("   2. Review technical structure and tasks")
        print("   3. Review generated code and tests")
        print("   4. Run tests: cd implementation && pytest tests/")
        print("   5. Start development following the tasks")
        
        print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description="Complete Agent Workflow Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From requirements file
  python complete_workflow.py --requirements requirements/user_requirement.md
  
  # From JIRA issue
  python complete_workflow.py --jira PROJ-123 --jira-url https://company.atlassian.net
  
  # Full workflow with custom output directory
  python complete_workflow.py --requirements requirements.md --output workflow_output
        """
    )
    
    # Input options
    parser.add_argument('--requirements', '-r', type=str,
                       help='Path to requirements file')
    parser.add_argument('--jira', type=str,
                       help='JIRA issue key (e.g., PROJ-123)')
    
    # JIRA configuration
    parser.add_argument('--jira-url', type=str,
                       help='JIRA URL (or set JIRA_URL env var)')
    parser.add_argument('--jira-email', type=str,
                       help='JIRA email (or set JIRA_EMAIL env var)')
    parser.add_argument('--jira-token', type=str,
                       help='JIRA API token (or set JIRA_API_TOKEN env var)')
    
    # Output configuration
    parser.add_argument('--output', '-o', type=str, default='workflow_output',
                       help='Base output directory (default: workflow_output)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.requirements and not args.jira:
        parser.error("Either --requirements or --jira must be provided")
    
    # Determine requirements source
    requirements_source = args.requirements or args.jira
    jira_enabled = bool(args.jira)
    
    # Initialize JIRA agent if needed
    if jira_enabled:
        os.environ['JIRA_URL'] = args.jira_url or os.getenv('JIRA_URL', '')
        os.environ['JIRA_EMAIL'] = args.jira_email or os.getenv('JIRA_EMAIL', '')
        os.environ['JIRA_API_TOKEN'] = args.jira_token or os.getenv('JIRA_API_TOKEN', '')
    
    # Initialize orchestrator
    orchestrator = CompleteWorkflowOrchestrator(
        base_dir=args.output,
        jira_enabled=jira_enabled
    )
    
    # Run workflow
    result = orchestrator.run_full_workflow(
        requirements_source=requirements_source,
        jira_key=args.jira
    )
    
    # Exit with appropriate code
    if result['status'] == 'success':
        print("\n✅ Workflow completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Workflow failed: {result.get('reason', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
