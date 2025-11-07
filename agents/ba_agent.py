from typing import Dict, List
from jira import JIRA
from shared.llm_manager import LLMManager

class BAAgent:
    """Reads JIRA and structures business requirements"""
    
    def __init__(self, llm_config: Dict, jira_config: Dict):
        self.llm_config = llm_config
        self.jira_config = jira_config
        self.llm = LLMManager()
        print("📋 BA Agent initialized")
    
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
