"""
JIRA Integration Agent
Fetches JIRA issues and prepares requirements for BA Agent
"""
import os
import json
from typing import Dict, Any, Optional
from jira import JIRA


class JiraAgent:
    """Agent that connects to JIRA, reads issues, and prepares requirements"""
    
    def __init__(self, jira_url: str = None, jira_email: str = None, jira_token: str = None):
        """
        Initialize JIRA connection
        
        Args:
            jira_url: JIRA instance URL (e.g., https://yourcompany.atlassian.net)
            jira_email: JIRA user email
            jira_token: JIRA API token
        """
        self.jira_url = jira_url or os.getenv('JIRA_URL')
        self.jira_email = jira_email or os.getenv('JIRA_EMAIL')
        self.jira_token = jira_token or os.getenv('JIRA_API_TOKEN')
        
        self.jira_client = None
        if self.jira_url and self.jira_email and self.jira_token:
            self._connect()
    
    def _connect(self):
        """Establish connection to JIRA"""
        try:
            self.jira_client = JIRA(
                server=self.jira_url,
                basic_auth=(self.jira_email, self.jira_token)
            )
            print(f"✅ Connected to JIRA: {self.jira_url}")
        except Exception as e:
            print(f"❌ Failed to connect to JIRA: {e}")
            raise
    
    def fetch_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Fetch a single JIRA issue by key
        
        Args:
            issue_key: JIRA issue key (e.g., 'PROJ-123')
            
        Returns:
            Dictionary containing issue details
        """
        if not self.jira_client:
            raise ValueError("JIRA client not connected. Check credentials.")
        
        print(f"📥 Fetching JIRA issue: {issue_key}")
        
        try:
            issue = self.jira_client.issue(issue_key)
            
            issue_data = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description or "",
                "status": issue.fields.status.name,
                "issue_type": issue.fields.issuetype.name,
                "priority": issue.fields.priority.name if issue.fields.priority else "None",
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else "Unknown",
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "created": str(issue.fields.created),
                "updated": str(issue.fields.updated),
                "labels": issue.fields.labels,
                "components": [c.name for c in issue.fields.components] if issue.fields.components else [],
                "acceptance_criteria": self._extract_acceptance_criteria(issue),
                "comments": self._extract_comments(issue),
                "attachments": [a.filename for a in issue.fields.attachment] if issue.fields.attachment else []
            }
            
            print(f"✅ Fetched: {issue_key} - {issue.fields.summary}")
            return issue_data
            
        except Exception as e:
            print(f"❌ Error fetching issue {issue_key}: {e}")
            raise
    
    def _extract_acceptance_criteria(self, issue) -> str:
        """Extract acceptance criteria from issue (if available)"""
        description = issue.fields.description or ""
        
        # Look for common acceptance criteria markers
        markers = [
            "Acceptance Criteria:",
            "AC:",
            "Acceptance:",
            "Given/When/Then"
        ]
        
        for marker in markers:
            if marker in description:
                # Extract text after the marker
                parts = description.split(marker, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        
        return ""
    
    def _extract_comments(self, issue) -> list:
        """Extract comments from issue"""
        comments = []
        if hasattr(issue.fields, 'comment') and issue.fields.comment:
            for comment in issue.fields.comment.comments:
                comments.append({
                    "author": comment.author.displayName,
                    "body": comment.body,
                    "created": str(comment.created)
                })
        return comments
    
    def prepare_requirements_document(self, issue_key: str, output_path: str = None) -> str:
        """
        Fetch JIRA issue and convert to requirements document for BA Agent
        
        Args:
            issue_key: JIRA issue key
            output_path: Path to save markdown file (optional)
            
        Returns:
            Markdown formatted requirements document
        """
        issue_data = self.fetch_issue(issue_key)
        
        # Generate markdown document
        markdown = f"""# Requirement from JIRA {issue_key}

## Overview
**Issue Type:** {issue_data['issue_type']}  
**Status:** {issue_data['status']}  
**Priority:** {issue_data['priority']}  
**Reporter:** {issue_data['reporter']}  
**Assignee:** {issue_data['assignee']}  

## Summary
{issue_data['summary']}

## Description
{issue_data['description']}

## Acceptance Criteria
{issue_data['acceptance_criteria'] or 'Not specified'}

## Labels
{', '.join(issue_data['labels']) if issue_data['labels'] else 'None'}

## Components
{', '.join(issue_data['components']) if issue_data['components'] else 'None'}

## Comments
"""
        
        if issue_data['comments']:
            for i, comment in enumerate(issue_data['comments'], 1):
                markdown += f"\n### Comment {i} by {comment['author']}\n{comment['body']}\n"
        else:
            markdown += "\nNo comments\n"
        
        markdown += f"""
## Attachments
{', '.join(issue_data['attachments']) if issue_data['attachments'] else 'None'}

---
*Generated from JIRA {issue_key} on {issue_data['updated']}*
"""
        
        # Save to file if path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"💾 Requirements saved: {output_path}")
        
        return markdown
    
    def analyze_completeness(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze if JIRA issue has sufficient information for BA analysis
        
        Returns:
            Dictionary with completeness analysis
        """
        completeness = {
            "is_complete": True,
            "missing_fields": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Check critical fields
        if not issue_data.get('description') or len(issue_data['description']) < 50:
            completeness['is_complete'] = False
            completeness['missing_fields'].append("Detailed description")
        
        if not issue_data.get('acceptance_criteria'):
            completeness['warnings'].append("No acceptance criteria defined")
            completeness['recommendations'].append("Add clear acceptance criteria")
        
        if issue_data.get('priority') == 'None':
            completeness['warnings'].append("Priority not set")
        
        if not issue_data.get('components'):
            completeness['warnings'].append("No components specified")
            completeness['recommendations'].append("Tag with relevant components")
        
        return completeness


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python jira_agent.py <JIRA-KEY>")
        print("Example: python jira_agent.py PROJ-123")
        sys.exit(1)
    
    issue_key = sys.argv[1]
    
    # Initialize agent (reads from environment variables)
    jira_agent = JiraAgent()
    
    # Fetch and prepare requirements
    requirements_md = jira_agent.prepare_requirements_document(
        issue_key,
        output_path=f"requirements/{issue_key.replace('-', '_')}_requirement.md"
    )
    
    # Check completeness
    issue_data = jira_agent.fetch_issue(issue_key)
    completeness = jira_agent.analyze_completeness(issue_data)
    
    print("\n" + "="*70)
    print("📊 COMPLETENESS ANALYSIS")
    print("="*70)
    print(f"✅ Complete: {completeness['is_complete']}")
    if completeness['missing_fields']:
        print(f"❌ Missing: {', '.join(completeness['missing_fields'])}")
    if completeness['warnings']:
        print(f"⚠️  Warnings: {', '.join(completeness['warnings'])}")
    if completeness['recommendations']:
        print(f"💡 Recommendations: {', '.join(completeness['recommendations'])}")
