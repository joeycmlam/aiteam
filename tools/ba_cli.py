#!/usr/bin/env python3
"""
BA CLI Tool - Fetch JIRA epic and generate analysis + Cucumber scenarios

Usage:
    python3 tools/ba_cli.py SCRUM-6
    python3 tools/ba_cli.py SCRUM-6 --output ./output
    python3 tools/ba_cli.py SCRUM-6 --format json
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from jira import JIRA
from shared.llm_manager import LLMManager

class BAAssistant:
    """Business Analyst Assistant for JIRA analysis and Cucumber generation"""
    
    def __init__(self):
        load_dotenv(override=True)
        
        # Initialize JIRA connection
        self.jira_server = os.getenv('JIRA_SERVER')
        self.jira_user = os.getenv('JIRA_USER')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.jira_server, self.jira_user, self.jira_token]):
            raise ValueError(
                "Missing JIRA credentials. Set in .env:\n"
                "  JIRA_SERVER=https://your-domain.atlassian.net\n"
                "  JIRA_USER=your-email@example.com\n"
                "  JIRA_API_TOKEN=your-token"
            )
        
        self.jira = JIRA(
            server=self.jira_server,
            basic_auth=(self.jira_user, self.jira_token)
        )
        
        # Initialize LLM
        self.llm = LLMManager()
    
    def fetch_jira_epic(self, issue_key: str) -> dict:
        """Fetch JIRA epic with all linked issues"""
        print(f"📥 Fetching JIRA epic: {issue_key}")
        print(f"   Server: {self.jira_server}")
        
        try:
            # Fetch main issue
            issue = self.jira.issue(issue_key)
            
            # Extract data
            epic_data = {
                'key': issue.key,
                'summary': issue.fields.summary,
                'description': issue.fields.description or '',
                'issue_type': issue.fields.issuetype.name,
                'status': issue.fields.status.name,
                'priority': issue.fields.priority.name if issue.fields.priority else 'None',
                'reporter': issue.fields.reporter.displayName,
                'assignee': issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
                'created': str(issue.fields.created),
                'updated': str(issue.fields.updated),
                'labels': issue.fields.labels,
                'components': [c.name for c in issue.fields.components],
                'linked_issues': []
            }
            
            # Fetch linked issues
            if hasattr(issue.fields, 'issuelinks'):
                for link in issue.fields.issuelinks:
                    if hasattr(link, 'outwardIssue'):
                        linked = link.outwardIssue
                        epic_data['linked_issues'].append({
                            'key': linked.key,
                            'summary': linked.fields.summary,
                            'type': linked.fields.issuetype.name,
                            'status': linked.fields.status.name
                        })
                    elif hasattr(link, 'inwardIssue'):
                        linked = link.inwardIssue
                        epic_data['linked_issues'].append({
                            'key': linked.key,
                            'summary': linked.fields.summary,
                            'type': linked.fields.issuetype.name,
                            'status': linked.fields.status.name
                        })
            
            print(f"   ✅ Fetched: {epic_data['key']} - {epic_data['summary']}")
            print(f"   📊 Status: {epic_data['status']}")
            print(f"   🔗 Linked Issues: {len(epic_data['linked_issues'])}")
            
            return epic_data
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def analyze_requirements(self, epic_data: dict) -> str:
        """Analyze epic and generate requirements analysis"""
        print(f"\n🔍 Analyzing Requirements...")
        
        prompt = f"""
As a Business Analyst, analyze this JIRA epic and provide a comprehensive requirements analysis.

JIRA Epic: {epic_data['key']}
Title: {epic_data['summary']}
Description:
{epic_data['description']}

Status: {epic_data['status']}
Priority: {epic_data['priority']}
Components: {', '.join(epic_data['components'])}
Labels: {', '.join(epic_data['labels'])}

Linked Issues ({len(epic_data['linked_issues'])}):
{chr(10).join([f"- {i['key']}: {i['summary']} ({i['type']}, {i['status']})" for i in epic_data['linked_issues']])}

Generate a structured requirements analysis with:

1. EXECUTIVE SUMMARY
   - Project overview
   - Business objective
   - Key stakeholders

2. FUNCTIONAL REQUIREMENTS
   - List each functional requirement with ID (FR-1, FR-2, etc.)
   - Description
   - Priority (Must Have, Should Have, Nice to Have)
   - Acceptance criteria

3. NON-FUNCTIONAL REQUIREMENTS
   - Performance requirements
   - Security requirements
   - Scalability requirements
   - Usability requirements

4. USER PERSONAS
   - Identify user types
   - Their goals and needs

5. BUSINESS VALUE
   - Expected benefits
   - Success metrics

6. RISKS & DEPENDENCIES
   - Technical risks
   - External dependencies
   - Assumptions

7. PROJECT TYPE ASSESSMENT
   - Is this Greenfield (new), Enhancement (existing), or Migration?
   - Rationale for classification

Format in markdown with clear sections and bullet points.
"""
        
        analysis = self.llm.generate(prompt, max_tokens=3000)
        print(f"   ✅ Requirements analysis complete")
        return analysis
    
    def generate_business_solution(self, epic_data: dict, analysis: str) -> str:
        """Generate business solution recommendations"""
        print(f"\n💡 Generating Business Solution...")
        
        prompt = f"""
Based on this requirements analysis, provide business solution recommendations.

Epic: {epic_data['key']} - {epic_data['summary']}

Requirements Analysis:
{analysis}

Generate a business solution document with:

1. RECOMMENDED SOLUTION APPROACH
   - High-level solution description
   - Why this approach is recommended
   - Alternative approaches considered

2. IMPLEMENTATION PHASES
   - Phase 1: MVP (Minimum Viable Product)
   - Phase 2: Enhanced Features
   - Phase 3: Advanced Capabilities

3. RESOURCE REQUIREMENTS
   - Team composition needed
   - Estimated timeline
   - Key technologies

4. BUSINESS BENEFITS
   - Quantifiable benefits
   - ROI considerations
   - Time to value

5. RISK MITIGATION STRATEGIES
   - Identified risks
   - Mitigation approaches
   - Contingency plans

6. SUCCESS CRITERIA
   - How to measure success
   - KPIs to track
   - Definition of done

Format in markdown with actionable recommendations.
"""
        
        solution = self.llm.generate(prompt, max_tokens=2500)
        print(f"   ✅ Business solution generated")
        return solution
    
    def generate_cucumber_scenarios(self, epic_data: dict, analysis: str) -> str:
        """Generate Cucumber feature files"""
        print(f"\n🥒 Generating Cucumber Scenarios...")
        
        prompt = f"""
As a Business Analyst specializing in BDD, create comprehensive Cucumber feature files.

Epic: {epic_data['key']} - {epic_data['summary']}

Requirements:
{analysis[:2000]}  # Limit context

Generate Cucumber feature files in Gherkin syntax with:

1. FEATURE DESCRIPTION
   - Feature name
   - Business value (As a... I want... So that...)
   - Background setup

2. HAPPY PATH SCENARIOS
   - Main success scenarios
   - Cover primary user flows

3. NEGATIVE SCENARIOS
   - Error handling
   - Invalid inputs
   - Edge cases

4. SECURITY SCENARIOS
   - Authentication/Authorization
   - Data protection

5. SCENARIO OUTLINES
   - Data-driven test cases
   - Use Examples tables

Requirements:
- Use proper Gherkin syntax (Given-When-Then)
- Add @tags for test organization
- Include data tables where appropriate
- Make scenarios independent and reusable
- Add clear assertions in Then steps

Generate 2-3 feature files covering main functionality.
Format as valid Gherkin with file names and full scenarios.
"""
        
        scenarios = self.llm.generate(prompt, max_tokens=3000)
        print(f"   ✅ Cucumber scenarios generated")
        return scenarios
    
    def generate_user_stories(self, epic_data: dict, analysis: str) -> str:
        """Generate user stories with acceptance criteria"""
        print(f"\n📝 Generating User Stories...")
        
        prompt = f"""
Create detailed user stories from this epic.

Epic: {epic_data['key']} - {epic_data['summary']}

Analysis:
{analysis[:1500]}

Generate 5-8 user stories in this format:

---
Story ID: US-1
Title: [Concise title]

As a [role]
I want [capability]
So that [benefit]

Acceptance Criteria:
✓ Criterion 1
✓ Criterion 2
✓ Criterion 3

Technical Notes:
- Implementation detail 1
- Implementation detail 2

Story Points: [1-13]
Priority: High | Medium | Low
Dependencies: [Other stories if any]
---

Make stories:
- Independent (can be developed separately)
- Valuable (delivers business value)
- Estimable (team can size it)
- Small (fits in one sprint)
- Testable (clear acceptance criteria)
"""
        
        stories = self.llm.generate(prompt, max_tokens=2500)
        print(f"   ✅ User stories generated")
        return stories
    
    def save_outputs(self, output_dir: Path, epic_data: dict, analysis: str, 
                    solution: str, scenarios: str, stories: str):
        """Save all outputs to files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save requirements analysis
        analysis_file = output_dir / f"{epic_data['key']}_requirements_analysis.md"
        with open(analysis_file, 'w') as f:
            f.write(f"# Requirements Analysis: {epic_data['key']}\n\n")
            f.write(f"**Epic**: {epic_data['summary']}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(analysis)
        print(f"\n💾 Saved: {analysis_file}")
        
        # Save business solution
        solution_file = output_dir / f"{epic_data['key']}_business_solution.md"
        with open(solution_file, 'w') as f:
            f.write(f"# Business Solution: {epic_data['key']}\n\n")
            f.write(f"**Epic**: {epic_data['summary']}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(solution)
        print(f"💾 Saved: {solution_file}")
        
        # Save Cucumber scenarios
        cucumber_file = output_dir / f"{epic_data['key']}_cucumber_scenarios.feature"
        with open(cucumber_file, 'w') as f:
            f.write(f"# Generated from JIRA Epic: {epic_data['key']}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(scenarios)
        print(f"💾 Saved: {cucumber_file}")
        
        # Save user stories
        stories_file = output_dir / f"{epic_data['key']}_user_stories.md"
        with open(stories_file, 'w') as f:
            f.write(f"# User Stories: {epic_data['key']}\n\n")
            f.write(f"**Epic**: {epic_data['summary']}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(stories)
        print(f"💾 Saved: {stories_file}")
        
        # Save raw JIRA data
        jira_file = output_dir / f"{epic_data['key']}_jira_data.json"
        with open(jira_file, 'w') as f:
            json.dump(epic_data, f, indent=2)
        print(f"💾 Saved: {jira_file}")
        
        # Create summary
        summary_file = output_dir / f"{epic_data['key']}_SUMMARY.md"
        with open(summary_file, 'w') as f:
            f.write(f"# BA Analysis Summary: {epic_data['key']}\n\n")
            f.write(f"## Epic Details\n")
            f.write(f"- **Key**: {epic_data['key']}\n")
            f.write(f"- **Title**: {epic_data['summary']}\n")
            f.write(f"- **Status**: {epic_data['status']}\n")
            f.write(f"- **Priority**: {epic_data['priority']}\n")
            f.write(f"- **Reporter**: {epic_data['reporter']}\n")
            f.write(f"- **Assignee**: {epic_data['assignee']}\n")
            f.write(f"- **Linked Issues**: {len(epic_data['linked_issues'])}\n\n")
            f.write(f"## Generated Artifacts\n")
            f.write(f"1. **Requirements Analysis**: `{analysis_file.name}`\n")
            f.write(f"2. **Business Solution**: `{solution_file.name}`\n")
            f.write(f"3. **User Stories**: `{stories_file.name}`\n")
            f.write(f"4. **Cucumber Scenarios**: `{cucumber_file.name}`\n")
            f.write(f"5. **JIRA Raw Data**: `{jira_file.name}`\n\n")
            f.write(f"## Next Steps\n")
            f.write(f"1. Review requirements analysis with stakeholders\n")
            f.write(f"2. Get approval on business solution approach\n")
            f.write(f"3. Review Cucumber scenarios with QA team\n")
            f.write(f"4. Break down user stories into development tasks\n")
            f.write(f"5. Update JIRA with refined acceptance criteria\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"💾 Saved: {summary_file}")
        
        print(f"\n✅ All artifacts saved to: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='BA CLI Tool - Analyze JIRA epic and generate business artifacts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze JIRA epic SCRUM-6
  python3 tools/ba_cli.py SCRUM-6
  
  # Save to custom directory
  python3 tools/ba_cli.py SCRUM-6 --output ./ba_analysis
  
  # Generate specific artifacts only
  python3 tools/ba_cli.py SCRUM-6 --artifacts requirements solution

Required Environment Variables (.env):
  JIRA_SERVER=https://your-domain.atlassian.net
  JIRA_USER=your-email@example.com
  JIRA_API_TOKEN=your-api-token
  GITHUB_TOKEN=your-github-token (for LLM)
        """
    )
    
    parser.add_argument(
        'issue_key',
        help='JIRA issue key (e.g., SCRUM-6, EPIC-123)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./ba_output',
        help='Output directory for generated artifacts (default: ./ba_output)'
    )
    
    parser.add_argument(
        '--artifacts', '-a',
        nargs='+',
        choices=['requirements', 'solution', 'scenarios', 'stories', 'all'],
        default=['all'],
        help='Artifacts to generate (default: all)'
    )
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*70)
        print("🎯 BA ASSISTANT - JIRA Epic Analysis")
        print("="*70)
        
        # Initialize BA Assistant
        ba = BAAssistant()
        
        # Fetch JIRA epic
        epic_data = ba.fetch_jira_epic(args.issue_key)
        
        # Generate artifacts based on selection
        generate_all = 'all' in args.artifacts
        
        analysis = None
        if generate_all or 'requirements' in args.artifacts:
            analysis = ba.analyze_requirements(epic_data)
        
        solution = None
        if generate_all or 'solution' in args.artifacts:
            if not analysis:
                analysis = ba.analyze_requirements(epic_data)
            solution = ba.generate_business_solution(epic_data, analysis)
        
        stories = None
        if generate_all or 'stories' in args.artifacts:
            if not analysis:
                analysis = ba.analyze_requirements(epic_data)
            stories = ba.generate_user_stories(epic_data, analysis)
        
        scenarios = None
        if generate_all or 'scenarios' in args.artifacts:
            if not analysis:
                analysis = ba.analyze_requirements(epic_data)
            scenarios = ba.generate_cucumber_scenarios(epic_data, analysis)
        
        # Save outputs
        output_dir = Path(args.output)
        ba.save_outputs(
            output_dir, 
            epic_data,
            analysis or "Not generated",
            solution or "Not generated",
            scenarios or "Not generated",
            stories or "Not generated"
        )
        
        print("\n" + "="*70)
        print("🎉 BA ANALYSIS COMPLETED")
        print("="*70)
        print(f"\n📂 All artifacts available in: {output_dir}")
        print(f"\n💡 Next Steps:")
        print(f"   1. Review {args.issue_key}_SUMMARY.md")
        print(f"   2. Share requirements_analysis.md with stakeholders")
        print(f"   3. Review cucumber_scenarios.feature with QA")
        print(f"   4. Update JIRA with user stories")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
