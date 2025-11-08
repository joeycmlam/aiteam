import os
import sys
import yaml
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all agents
from agents.lead_orchestrator import LeadOrchestrator
from agents.architect_agent import ArchitectAgent
from agents.ba_agent import BAAgent
from agents.qa_agent import QAAgent
from agents.senior_dev_agent import SeniorDevAgent
from agents.developer_agent import DeveloperAgent

class MigrationPipeline:
    """Main orchestration pipeline using Ollama + GitHub Copilot workflow"""
    
    def __init__(self, config_path: str):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        llm_config = config['llm']
        jira_config = {
            'server': config['jira']['server'],
            'user': config['jira']['user'],
            'token': os.getenv('JIRA_API_TOKEN')
        }
        
        # Initialize all agents
        print("🤖 Initializing AI Agents...")
        print("="*60)
        print(f"   LLM Provider: {llm_config['provider']}")
        print(f"   Model: {llm_config.get('model', 'default')}")
        print("="*60)
        
        self.lead = LeadOrchestrator(llm_config)
        self.architect = ArchitectAgent(llm_config)
        self.ba = BAAgent(llm_config, jira_config)
        self.qa = QAAgent(llm_config)
        self.senior_dev = SeniorDevAgent(llm_config)
        self.developer = DeveloperAgent(llm_config)
        
        print("="*60)
        print("✅ All agents initialized\n")
    
    def run(self, jira_jql: str, repo_path: str):
        """Execute the migration pipeline"""
        print("\n" + "="*60)
        print("🚀 LEGACY CODE MIGRATION PIPELINE")
        print("   Using: Ollama + GitHub Copilot Workflow")
        print("="*60 + "\n")
        
        # Stage 1: Fetch JIRA tickets
        print("📋 STAGE 1: Fetching Requirements")
        print("-"*60)
        tickets = self.ba.fetch_tickets(jira_jql)
        
        # Stage 2: Analyze architecture
        print("\n🏗️  STAGE 2: Architecture Analysis")
        print("-"*60)
        analysis = self.architect.analyze_codebase(repo_path)
        patterns = self.architect.recommend_patterns(analysis)
        
        # Stage 3: Structure requirements
        print("\n📝 STAGE 3: Requirements Structuring")
        print("-"*60)
        requirements = self.ba.structure_requirements(tickets)
        
        # Stage 4: Generate tests
        print("\n🧪 STAGE 4: Test Generation")
        print("-"*60)
        self.qa.create_feature_files(requirements, './tests/features')
        
        # Stage 5: Provide guidelines
        print("\n📚 STAGE 5: Development Guidelines")
        print("-"*60)
        guidelines = self.senior_dev.provide_guidelines({'recommended_patterns': patterns})
        
        # Stage 6: Implementation loop
        print("\n💻 STAGE 6: Implementation")
        print("-"*60)
        for story in requirements['user_stories']:
            # Developer implements using LLM
            implementation = self.developer.implement_feature(story, guidelines)
            
            # Senior reviews using LLM
            review = self.senior_dev.review_code(implementation['code'], story)
            
            if review['approved']:
                print(f"   ✅ {story['ticket_id']} - APPROVED")
            else:
                print(f"   🔄 {story['ticket_id']} - NEEDS REVISION")
        
        # Final summary
        print("\n" + "="*60)
        print("✨ MIGRATION PIPELINE COMPLETED")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Tickets processed: {len(tickets)}")
        print(f"   • Features implemented: {len(requirements['user_stories'])}")
        print(f"   • Tests created: {len(requirements['user_stories'])} feature files")
        print(f"   • Design patterns applied: {len(patterns)}")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Review generated code in ./generated_code/")
        print(f"   2. Open files in VS Code")
        print(f"   3. Use GitHub Copilot (Cmd+I) to refine")
        print(f"   4. Run tests: pytest tests/")
        print("\n✅ All stages completed!\n")

# Main execution
if __name__ == "__main__":
    # Ensure Ollama is running
    import subprocess
    try:
        subprocess.run(["ollama", "list"], check=True, capture_output=True)
        print("✅ Ollama is running\n")
    except:
        print("⚠️  Starting Ollama...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(3)
    
    # Run pipeline
    pipeline = MigrationPipeline('./config/agent_config.yaml')
    pipeline.run(
        jira_jql="project = LEGACY AND status = 'To Do'",
        repo_path="./tests/fixtures"
    )
