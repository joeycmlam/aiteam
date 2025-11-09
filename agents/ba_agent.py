from typing import Dict, List, Optional
from jira import JIRA
from shared.llm_manager import LLMManager

class BAAgent:
    """Reads JIRA and structures business requirements"""
    
    def __init__(self, llm_config: Dict, jira_config: Dict):
        self.llm_config = llm_config
        self.jira_config = jira_config
        self.llm = LLMManager()
        self.jira_client = None
        print("📋 BA Agent initialized")
    
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
            prompt = f"""Extract structured requirements from this JIRA ticket:

ID: {ticket['id']}
Summary: {ticket['summary']}
Description: {ticket['description']}

Extract:
1. Core business requirement (1 sentence)
2. Acceptance criteria (3-4 items in Given-When-Then format)
3. Technical considerations

Format as JSON."""

            try:
                llm_response = self.llm.generate(prompt, system_message="You are a business analyst.")
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
                "acceptance_criteria": [
                    "Implementation meets requirements",
                    "All tests pass",
                    "Code review approved"
                ]
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
        
        initiative_prompt = f"""Analyze this JIRA initiative and extract:

Title: {initiative['summary']}
Description: {initiative['description']}
Type: {initiative['type']}
Number of linked issues: {len(initiative['linked_issues'])}

Extract:
1. Overall business objective (2-3 sentences)
2. Key success criteria (3-5 items)
3. High-level technical approach
4. Potential risks or challenges

Format as structured JSON."""

        try:
            llm_response = self.llm.generate(
                initiative_prompt, 
                system_message="You are a senior business analyst analyzing project initiatives."
            )
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
                    "All related tests pass",
                    "Code review approved"
                ]
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
