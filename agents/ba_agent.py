from typing import Dict, List, Optional
import os
import json
import yaml
from jira import JIRA
from shared.llm_manager import LLMManager

class BAAgent:
    """
    Business Analyst Agent - Analyzes requirements and creates user stories from JIRA tickets
    
    Responsibilities:
    - Analyze JIRA tickets and extract functional requirements
    - Create detailed acceptance criteria
    - Map requirements to technical specifications
    - Collaborate with stakeholders to clarify ambiguities
    - Document business rules and workflows
    
    When working with JIRA tickets, always:
    - Break down complex requirements into manageable user stories
    - Define clear acceptance criteria using Given-When-Then format
    - Identify dependencies and edge cases
    - Suggest test scenarios for QA validation
    """
    
    def __init__(self, llm_config: Dict, jira_config: Dict, prompts_config_path: str = None):
        self.llm_config = llm_config
        self.jira_config = jira_config
        self.llm = LLMManager()
        self.jira_client = None
        
        # Load prompts configuration
        if prompts_config_path is None:
            prompts_config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config', 'prompts', 'ba_agent_prompts.yaml'
            )
        
        self.prompts = self._load_prompts(prompts_config_path)
        print("📋 Business Analyst Agent initialized")
    
    def _load_prompts(self, config_path: str) -> Dict:
        """Load prompts configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                prompts = yaml.safe_load(f)
            print(f"   ✅ Loaded prompts from: {config_path}")
            return prompts
        except FileNotFoundError:
            print(f"   ⚠️  Prompts config not found: {config_path}")
            print(f"   Using default inline prompts")
            return self._get_default_prompts()
        except Exception as e:
            print(f"   ⚠️  Error loading prompts: {e}")
            print(f"   Using default inline prompts")
            return self._get_default_prompts()
    
    def _get_default_prompts(self) -> Dict:
        """Fallback to default prompts if config file not found"""
        return {
            'extract_requirements': {
                'template': 'Extract structured requirements from this JIRA ticket:\n\nID: {ticket_id}\nSummary: {summary}\nDescription: {description}\n\nExtract:\n1. Core business requirement (1 sentence)\n2. Acceptance criteria (3-4 items in Given-When-Then format)\n3. Technical considerations\n\nFormat as JSON.',
                'system_message': 'You are a business analyst.'
            },
            'analyze_initiative': {
                'template': 'Analyze this JIRA initiative and extract:\n\nTitle: {summary}\nDescription: {description}\nType: {issue_type}\nNumber of linked issues: {linked_count}\n\nExtract:\n1. Overall business objective (2-3 sentences)\n2. Key success criteria (3-5 items)\n3. High-level technical approach\n4. Potential risks or challenges\n\nFormat as structured JSON.',
                'system_message': 'You are a senior business analyst analyzing project initiatives.'
            },
            'defaults': {
                'acceptance_criteria': [
                    'Implementation meets requirements',
                    'All tests pass',
                    'Code review approved'
                ]
            }
        }
    
    def _connect_jira(self) -> Optional[JIRA]:
        """Establish JIRA connection"""
        if self.jira_client:
            return self.jira_client
        
        try:
            self.jira_client = JIRA(
                server=self.jira_config['server'],
                basic_auth=(self.jira_config['user'], self.jira_config['token'])
            )
            print(f"   ✅ Connected to JIRA: {self.jira_config['server']}")
            return self.jira_client
        except Exception as e:
            print(f"   ❌ Failed to connect to JIRA: {type(e).__name__}: {e}")
            return None
    
    def fetch_initiative(self, issue_key: str) -> Dict:
        """Fetch a specific JIRA initiative/epic and all linked issues"""
        print(f"\n🎯 Fetching JIRA Initiative: {issue_key}")
        
        jira = self._connect_jira()
        if not jira:
            print("   ⚠️  Using mock data - JIRA unavailable")
            return self._get_mock_initiative()
        
        try:
            # Fetch the main initiative/epic
            initiative = jira.issue(issue_key)
            
            print(f"   📌 Title: {initiative.fields.summary}")
            print(f"   📝 Type: {initiative.fields.issuetype.name}")
            print(f"   🎨 Status: {initiative.fields.status.name}")
            
            # Extract initiative details
            initiative_data = {
                "key": initiative.key,
                "summary": initiative.fields.summary,
                "description": initiative.fields.description or "No description provided",
                "type": initiative.fields.issuetype.name,
                "status": initiative.fields.status.name,
                "priority": initiative.fields.priority.name if initiative.fields.priority else "Medium",
                "linked_issues": []
            }
            
            # Fetch linked issues (stories, tasks, bugs)
            print(f"\n   🔗 Fetching linked issues...")
            
            # Method 1: Check if it's an Epic and get issues in the epic
            if hasattr(initiative.fields, 'issuelinks'):
                for link in initiative.fields.issuelinks:
                    if hasattr(link, 'outwardIssue'):
                        linked_issue = link.outwardIssue
                        initiative_data['linked_issues'].append({
                            "key": linked_issue.key,
                            "summary": linked_issue.fields.summary,
                            "type": linked_issue.fields.issuetype.name,
                            "status": linked_issue.fields.status.name,
                            "link_type": link.type.outward
                        })
                    elif hasattr(link, 'inwardIssue'):
                        linked_issue = link.inwardIssue
                        initiative_data['linked_issues'].append({
                            "key": linked_issue.key,
                            "summary": linked_issue.fields.summary,
                            "type": linked_issue.fields.issuetype.name,
                            "status": linked_issue.fields.status.name,
                            "link_type": link.type.inward
                        })
            
            # Method 2: Search for issues that reference this epic
            try:
                jql = f'"Epic Link" = {issue_key} OR parent = {issue_key}'
                child_issues = jira.search_issues(jql, maxResults=100)
                
                for child in child_issues:
                    if not any(issue['key'] == child.key for issue in initiative_data['linked_issues']):
                        initiative_data['linked_issues'].append({
                            "key": child.key,
                            "summary": child.fields.summary,
                            "type": child.fields.issuetype.name,
                            "status": child.fields.status.name,
                            "link_type": "child of"
                        })
            except Exception as e:
                print(f"   ⚠️  Could not fetch child issues: {e}")
            
            print(f"   ✅ Found {len(initiative_data['linked_issues'])} linked issues")
            
            for issue in initiative_data['linked_issues']:
                print(f"      • {issue['key']}: {issue['summary']} [{issue['type']}]")
            
            return initiative_data
            
        except Exception as e:
            print(f"   ❌ Error fetching initiative: {type(e).__name__}: {e}")
            print("   Using mock data for demonstration")
            return self._get_mock_initiative()
    
    def _get_mock_initiative(self) -> Dict:
        """Return mock initiative data for testing"""
        return {
            "key": "SCRUM-5",
            "summary": "Mock Initiative - Legacy System Migration",
            "description": "This is mock data - actual JIRA connection failed",
            "type": "Epic",
            "status": "In Progress",
            "priority": "High",
            "linked_issues": [
                {
                    "key": "SCRUM-6",
                    "summary": "Analyze legacy authentication system",
                    "type": "Story",
                    "status": "To Do",
                    "link_type": "child of"
                },
                {
                    "key": "SCRUM-7",
                    "summary": "Design new OAuth2 architecture",
                    "type": "Story",
                    "status": "To Do",
                    "link_type": "child of"
                }
            ]
        }
    
    def fetch_tickets(self, jql: str) -> List[Dict]:
        """Fetches tickets from JIRA"""
        print(f"\n🔍 Fetching JIRA tickets with JQL: {jql}")
        
        try:
            jira_client = JIRA(
                server=self.jira_config['server'],
                basic_auth=(self.jira_config['user'], self.jira_config['token'])
            )
            
            issues = jira_client.search_issues(jql, maxResults=50)
            
            tickets = []
            for issue in issues:
                ticket = {
                    "id": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description or "No description",
                    "status": issue.fields.status.name,
                    "priority": issue.fields.priority.name if issue.fields.priority else "Medium"
                }
                tickets.append(ticket)
            
            print(f"   ✅ Found {len(tickets)} tickets")
            return tickets
            
        except ConnectionError as e:
            print(f"   ⚠️  JIRA connection error: {e}")
            print("   Check your JIRA_SERVER and network connection")
            return self._get_mock_tickets()
        except Exception as e:
            print(f"   ⚠️  JIRA error: {type(e).__name__}: {e}")
            print("   Using mock data for demonstration")
            return self._get_mock_tickets()
    
    def _get_mock_tickets(self) -> List[Dict]:
        """Return mock data for testing"""
        return [
            {
                "id": "DEMO-1",
                "summary": "Migrate user authentication module",
                "description": "Move legacy auth to OAuth2",
                "status": "To Do",
                "priority": "High"
            },
            {
                "id": "DEMO-2",
                "summary": "Refactor database access layer",
                "description": "Implement repository pattern for data access",
                "status": "To Do",
                "priority": "Medium"
            }
        ]
    
    def structure_requirements(self, tickets: List[Dict]) -> Dict:
        """Structures requirements from JIRA tickets using LLM"""
        print(f"\n📝 Structuring requirements from {len(tickets)} tickets")
        
        requirements = {
            "user_stories": [],
            "technical_tasks": []
        }
        
        for ticket in tickets:
            # Use LLM to extract structured requirements
            prompt_config = self.prompts.get('extract_requirements', {})
            prompt = prompt_config.get('template', '').format(
                ticket_id=ticket['id'],
                summary=ticket['summary'],
                description=ticket['description']
            )
            system_message = prompt_config.get('system_message', 'You are a business analyst.')

            try:
                llm_response = self.llm.generate(prompt, system_message=system_message)
                print(f"   🤖 LLM analyzed: {ticket['id']}")
            except ConnectionError:
                print(f"   ⚠️  LLM unavailable for {ticket['id']}, using default analysis")
                llm_response = "Manual review needed - LLM unavailable"
            except Exception as e:
                print(f"   ⚠️  Error analyzing {ticket['id']}: {type(e).__name__}")
                llm_response = "Manual review needed"
            
            structured = {
                "ticket_id": ticket['id'],
                "title": ticket['summary'],
                "description": ticket['description'],
                "llm_analysis": llm_response,
                "acceptance_criteria": self.prompts.get('defaults', {}).get('acceptance_criteria', [
                    "Implementation meets requirements",
                    "All tests pass",
                    "Code review approved"
                ])
            }
            
            requirements['user_stories'].append(structured)
            print(f"   • {ticket['id']}: {ticket['summary']}")
        
        return requirements
    
    def structure_requirements_from_initiative(self, initiative: Dict) -> Dict:
        """Structure requirements from a JIRA initiative and its linked issues"""
        print(f"\n📝 Structuring requirements from initiative: {initiative['key']}")
        
        requirements = {
            "initiative": {
                "key": initiative['key'],
                "title": initiative['summary'],
                "description": initiative['description'],
                "type": initiative['type'],
                "status": initiative['status'],
                "priority": initiative['priority']
            },
            "user_stories": [],
            "technical_tasks": [],
            "overall_objective": "",
            "success_criteria": []
        }
        
        # Analyze the main initiative with LLM
        print(f"\n   🤖 Analyzing initiative with AI...")
        
        prompt_config = self.prompts.get('analyze_initiative', {})
        initiative_prompt = prompt_config.get('template', '').format(
            summary=initiative['summary'],
            description=initiative['description'],
            issue_type=initiative['type'],
            linked_count=len(initiative['linked_issues'])
        )
        system_message = prompt_config.get('system_message', 'You are a senior business analyst analyzing project initiatives.')

        try:
            llm_response = self.llm.generate(initiative_prompt, system_message=system_message)
            print(f"   ✅ Initiative analyzed by AI")
            requirements['overall_objective'] = llm_response
        except Exception as e:
            print(f"   ⚠️  AI analysis unavailable: {type(e).__name__}")
            requirements['overall_objective'] = initiative['description']
        
        # Process each linked issue
        print(f"\n   📋 Processing {len(initiative['linked_issues'])} linked issues...")
        
        for issue in initiative['linked_issues']:
            print(f"      • {issue['key']}: {issue['summary']}")
            
            # Categorize by type
            if issue['type'].lower() in ['story', 'user story']:
                category = 'user_stories'
            else:
                category = 'technical_tasks'
            
            # Structure the issue
            structured_issue = {
                "key": issue['key'],
                "title": issue['summary'],
                "type": issue['type'],
                "status": issue['status'],
                "link_type": issue['link_type'],
                "acceptance_criteria": [
                    f"Implements requirements for {issue['key']}",
                ] + self.prompts.get('defaults', {}).get('acceptance_criteria', [
                    "All related tests pass",
                    "Code review approved"
                ])[1:]  # Use default criteria except first item which is customized
            }
            
            requirements[category].append(structured_issue)
        
        # Generate success criteria
        requirements['success_criteria'] = [
            f"All {len(initiative['linked_issues'])} linked issues completed",
            "System passes all acceptance tests",
            "Code quality meets standards",
            "Documentation is complete"
        ]
        
        print(f"\n   ✅ Requirements structured:")
        print(f"      User Stories: {len(requirements['user_stories'])}")
        print(f"      Technical Tasks: {len(requirements['technical_tasks'])}")
        
        return requirements
    
    def read_requirement_file(self, file_path: str) -> Dict:
        """Read user requirement from various file formats"""
        print(f"\n📄 Reading requirement file: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"   ❌ File not found: {file_path}")
            return {"error": "File not found"}
        
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        try:
            if ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"   ✅ Loaded JSON file")
                return data
                
            elif ext in ['.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                print(f"   ✅ Loaded YAML file")
                return data
                
            elif ext in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"   ✅ Loaded text file ({len(content)} characters)")
                return {"content": content, "format": "text"}
                
            else:
                # Try to read as plain text
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"   ✅ Loaded as plain text ({len(content)} characters)")
                return {"content": content, "format": "text"}
                
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON format: {e}")
            return {"error": f"JSON parse error: {e}"}
        except yaml.YAMLError as e:
            print(f"   ❌ Invalid YAML format: {e}")
            return {"error": f"YAML parse error: {e}"}
        except Exception as e:
            print(f"   ❌ Error reading file: {type(e).__name__}: {e}")
            return {"error": str(e)}
    
    def analyze_requirements(self, requirement_data: Dict, output_dir: str = 'requirements') -> Dict:
        """Analyze user requirements with AI and generate structured documentation"""
        print(f"\n🤖 Analyzing requirements with AI...")
        
        # Extract content based on format
        if 'content' in requirement_data:
            raw_content = requirement_data['content']
        elif 'error' in requirement_data:
            print(f"   ❌ Cannot analyze: {requirement_data['error']}")
            return requirement_data
        else:
            raw_content = json.dumps(requirement_data, indent=2)
        
        # AI Analysis Prompt
        prompt_config = self.prompts.get('analyze_requirements', {})
        max_length = prompt_config.get('max_content_length', 3000)
        analysis_prompt = prompt_config.get('template', '').format(
            raw_content=raw_content[:max_length]
        )
        system_message = prompt_config.get('system_message', 'You are an expert Business Analyst.')
        
        try:
            print(f"   🧠 Sending to LLM for analysis...")
            analysis = self.llm.generate(analysis_prompt, system_message=system_message)
            print(f"   ✅ AI analysis completed ({len(analysis)} characters)")
        except Exception as e:
            print(f"   ⚠️  AI analysis failed: {type(e).__name__}: {e}")
            fallback_template = self.prompts.get('fallbacks', {}).get('requirements_analysis', '')
            analysis = fallback_template.format(raw_content=raw_content[:1000]) if fallback_template else f"""# Requirements Analysis (AI Unavailable)

## Raw Requirements
{raw_content[:1000]}

## Manual Review Needed
AI analysis unavailable. Please review requirements manually.
"""
        
        # Generate scenarios/feature files
        print(f"\n📝 Generating BDD scenarios...")
        scenarios = self._generate_scenarios(analysis, raw_content)
        
        # Create structured requirement document
        requirement_doc = {
            "raw_requirements": raw_content,
            "ai_analysis": analysis,
            "scenarios": scenarios,
            "generated_at": self._get_timestamp(),
            "assumptions": self._extract_assumptions(analysis),
            "user_stories": self._extract_user_stories(analysis)
        }
        
        # Save to files
        os.makedirs(output_dir, exist_ok=True)
        
        # Save analysis document
        analysis_file = os.path.join(output_dir, 'requirements_analysis.md')
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(f"# Requirements Analysis\n\n")
            f.write(f"Generated: {requirement_doc['generated_at']}\n\n")
            f.write(f"## AI Analysis\n\n{analysis}\n\n")
            f.write(f"## Assumptions\n\n")
            for assumption in requirement_doc['assumptions']:
                f.write(f"- {assumption}\n")
        print(f"   ✅ Saved analysis: {analysis_file}")
        
        # Save scenarios as feature file
        feature_file = os.path.join(output_dir, 'requirements.feature')
        with open(feature_file, 'w', encoding='utf-8') as f:
            f.write(scenarios)
        print(f"   ✅ Saved scenarios: {feature_file}")
        
        # Save structured JSON
        json_file = os.path.join(output_dir, 'requirements_structured.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(requirement_doc, f, indent=2)
        print(f"   ✅ Saved structured data: {json_file}")
        
        return requirement_doc
    
    def _generate_scenarios(self, analysis: str, raw_content: str) -> str:
        """Generate Gherkin/BDD scenarios from requirements"""
        prompt_config = self.prompts.get('generate_scenarios', {})
        max_length = prompt_config.get('max_analysis_length', 2000)
        scenario_prompt = prompt_config.get('template', '').format(
            analysis=analysis[:max_length]
        )
        system_message = prompt_config.get('system_message', 'You are a QA expert specializing in BDD and Gherkin syntax.')
        
        try:
            scenarios = self.llm.generate(scenario_prompt, system_message=system_message)
            return scenarios
        except Exception as e:
            print(f"   ⚠️  Scenario generation failed: {type(e).__name__}")
            fallback_template = self.prompts.get('fallbacks', {}).get('scenarios', '')
            return fallback_template if fallback_template else f"""Feature: Requirements Implementation
  As a user
  I want the system to meet the specified requirements
  So that business objectives are achieved

  Scenario: Basic functionality
    Given the system is operational
    When I use the main feature
    Then I should see expected results
"""
    
    def _extract_assumptions(self, analysis: str) -> List[str]:
        """Extract assumptions from AI analysis"""
        assumptions = []
        lines = analysis.split('\n')
        in_assumptions = False
        
        for line in lines:
            if 'assumption' in line.lower() and ('#' in line or '**' in line):
                in_assumptions = True
                continue
            if in_assumptions:
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    assumptions.append(line.strip().lstrip('-*').strip())
                elif line.strip().startswith('#') or (line.strip() and not line.strip()[0].isdigit()):
                    if len(assumptions) > 0:  # Stop if we've collected some
                        break
        
        if not assumptions:
            assumptions = self.prompts.get('defaults', {}).get('assumptions', [
                "User requirements are complete and accurate",
                "Technical infrastructure is available",
                "Stakeholders are available for clarification"
            ])
        
        return assumptions
    
    def _extract_user_stories(self, analysis: str) -> List[Dict]:
        """Extract user stories from AI analysis"""
        stories = []
        lines = analysis.split('\n')
        
        for line in lines:
            if 'as a' in line.lower() and 'i want' in line.lower():
                stories.append({
                    "story": line.strip().lstrip('-*').strip(),
                    "status": "pending"
                })
        
        default_story = self.prompts.get('defaults', {}).get('user_story', {
            "story": "As a user, I want the system to work as specified",
            "status": "pending"
        })
        return stories if stories else [default_story]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def create_epic_in_jira(self, requirement_doc: Dict, project_key: str = 'SCRUM') -> Optional[str]:
        """Create an Epic in JIRA from the requirement document"""
        print(f"\n📊 Creating Epic in JIRA...")
        
        jira = self._connect_jira()
        if not jira:
            print(f"   ❌ Cannot create Epic: JIRA connection failed")
            print(f"   💡 Epic details saved to requirement document instead")
            return None
        
        try:
            # Extract epic details
            analysis = requirement_doc.get('ai_analysis', '')
            
            # Generate epic summary from first line or objective
            summary_lines = analysis.split('\n')
            epic_summary = "New Feature Implementation"
            for line in summary_lines:
                if 'objective' in line.lower() and len(line.strip()) > 10:
                    epic_summary = line.strip().lstrip('#*-').strip()[:255]
                    break
            
            # Create epic description
            epic_description = f"""h2. Business Objectives
{self._extract_section(analysis, 'objective')}

h2. Assumptions
{chr(10).join(f'* {a}' for a in requirement_doc.get('assumptions', []))}

h2. User Stories
{chr(10).join(f'* {s["story"]}' for s in requirement_doc.get('user_stories', []))}

h2. Generated
{requirement_doc.get('generated_at', 'Unknown')}

h2. Full Analysis
See attached requirements documentation.
"""
            
            # Create the epic
            print(f"   📝 Project: {project_key}")
            print(f"   📋 Summary: {epic_summary}")
            
            epic_dict = {
                'project': {'key': project_key},
                'summary': epic_summary,
                'description': epic_description,
                'issuetype': {'name': 'Epic'},
            }
            
            # Try to add Epic Name (some JIRA instances require it)
            try:
                epic_dict['customfield_10011'] = epic_summary  # Epic Name field
            except:
                pass
            
            new_epic = jira.create_issue(fields=epic_dict)
            epic_key = new_epic.key
            
            print(f"   ✅ Epic created: {epic_key}")
            print(f"   🔗 URL: {self.jira_config['server']}/browse/{epic_key}")
            
            # Create user stories as sub-tasks
            self._create_user_stories(jira, epic_key, requirement_doc.get('user_stories', []))
            
            return epic_key
            
        except Exception as e:
            print(f"   ❌ Failed to create Epic: {type(e).__name__}: {e}")
            print(f"   💡 Tip: Check project key '{project_key}' exists and you have permissions")
            return None
    
    def _extract_section(self, text: str, keyword: str) -> str:
        """Extract a section from markdown text"""
        lines = text.split('\n')
        section = []
        capturing = False
        
        for line in lines:
            if keyword.lower() in line.lower() and ('#' in line or '**' in line):
                capturing = True
                continue
            if capturing:
                if line.strip().startswith('#'):
                    break
                if line.strip():
                    section.append(line)
        
        return '\n'.join(section[:5]) if section else f"See full analysis for {keyword} details."
    
    def _create_user_stories(self, jira: JIRA, epic_key: str, user_stories: List[Dict]):
        """Create user stories as issues linked to the epic"""
        print(f"\n   📝 Creating user stories for {epic_key}...")
        
        for idx, story in enumerate(user_stories[:5], 1):  # Limit to first 5
            try:
                story_dict = {
                    'project': {'key': epic_key.split('-')[0]},
                    'summary': story['story'][:255],
                    'description': f"User Story: {story['story']}\n\nStatus: {story['status']}",
                    'issuetype': {'name': 'Story'},
                    'parent': {'key': epic_key}  # Link to epic
                }
                
                new_story = jira.create_issue(fields=story_dict)
                print(f"      ✅ Created story {idx}: {new_story.key}")
                
            except Exception as e:
                print(f"      ⚠️  Failed to create story {idx}: {type(e).__name__}")
                # Continue with other stories
                continue
