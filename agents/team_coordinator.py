"""
Team Coordinator - Facilitates professional team collaboration
Acts as Scrum Master + Tech Lead to coordinate the AI agent team
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from shared.team_messaging import TeamMessageBus, MessageType, get_message_bus
from shared.memory_store import SharedMemory


class TeamCoordinator:
    """
    Coordinates the AI agent team with professional software development practices
    
    Responsibilities:
    - Facilitate daily standups
    - Lead sprint planning
    - Coordinate collaborative reviews
    - Manage escalations and blockers
    - Track team metrics
    - Facilitate retrospectives
    """
    
    def __init__(self, team_name: str = "AI Development Team"):
        self.team_name = team_name
        self.message_bus = get_message_bus()
        self.memory = SharedMemory()
        
        # Team members
        self.team_members = {
            'BA': {'role': 'Business Analyst', 'skills': ['requirements', 'jira', 'user_stories']},
            'Architect': {'role': 'Solution Architect', 'skills': ['architecture', 'design', 'patterns']},
            'Tech Lead': {'role': 'Technical Lead', 'skills': ['review', 'mentoring', 'architecture']},
            'QA': {'role': 'QA Engineer', 'skills': ['testing', 'bdd', 'quality_assurance']},
            'DBA': {'role': 'Database Administrator', 'skills': ['database', 'schema', 'optimization', 'sql']},
            'DevOps': {'role': 'DevOps Engineer', 'skills': ['ci_cd', 'infrastructure', 'deployment', 'kubernetes']},
            'Dev-Frontend-1': {'role': 'Frontend Developer', 'skills': ['react', 'typescript', 'ui', 'css']},
            'Dev-Frontend-2': {'role': 'Frontend Developer', 'skills': ['react', 'typescript', 'ui', 'css']},
            'Dev-Backend-1': {'role': 'Backend Developer', 'skills': ['python', 'api', 'fastapi', 'rest']},
            'Dev-Backend-2': {'role': 'Backend Developer', 'skills': ['python', 'api', 'fastapi', 'rest']},
            'Dev-FullStack': {'role': 'Full-Stack Developer', 'skills': ['frontend', 'backend', 'general']}
        }
        
        # Team state
        self.current_sprint = None
        self.blockers = []
        self.decisions = []
        self.learnings = []
        
        print(f"🎯 Team Coordinator initialized for '{team_name}'")
        print(f"   Team Size: {len(self.team_members)} agents")
    
    def daily_standup(self) -> Dict[str, Any]:
        """
        Facilitate daily standup meeting
        Each agent reports: completed, in-progress, blockers, help-needed
        """
        print("\n" + "="*70)
        print("🌅 DAILY STANDUP - " + datetime.now().strftime("%Y-%m-%d %H:%M"))
        print("="*70)
        
        self.message_bus.broadcast("Team Coordinator", "🌅 Daily Standup Starting!")
        
        standup_notes = {
            'date': datetime.now().isoformat(),
            'attendees': list(self.team_members.keys()),
            'updates': {},
            'blockers': [],
            'help_requests': []
        }
        
        # Simulate each agent giving update
        for agent_name, agent_info in self.team_members.items():
            print(f"\n👤 {agent_name} ({agent_info['role']}):")
            
            # Get status from memory if available
            agent_status = self.memory.retrieve(f'{agent_name.lower()}_status')
            
            if agent_status:
                status_msg = f"""
                ✅ Completed: {agent_status.get('completed', 'Initial setup')}
                🔄 In Progress: {agent_status.get('in_progress', 'Ready for tasks')}
                🚫 Blockers: {agent_status.get('blockers', 'None')}
                """
            else:
                status_msg = "✅ Ready for work | 🔄 Awaiting tasks | 🚫 No blockers"
            
            print(f"   {status_msg}")
            
            self.message_bus.post_message(
                agent_name,
                MessageType.STATUS,
                status_msg.strip()
            )
            
            standup_notes['updates'][agent_name] = status_msg.strip()
        
        print("\n" + "="*70)
        print("✅ Standup Complete - Team is aligned!")
        print("="*70 + "\n")
        
        # Store standup notes
        self.memory.store('latest_standup', standup_notes)
        
        return standup_notes
    
    def sprint_planning(self, jira_tickets: List[Dict], sprint_goal: str = None) -> Dict[str, Any]:
        """
        Facilitate sprint planning
        - Review tickets
        - Estimate effort
        - Assign tasks
        - Set sprint goal
        """
        print("\n" + "="*70)
        print("📋 SPRINT PLANNING SESSION")
        print("="*70)
        
        if sprint_goal:
            print(f"🎯 Sprint Goal: {sprint_goal}")
        
        print(f"📊 Tickets to Plan: {len(jira_tickets)}")
        
        self.message_bus.broadcast("Team Coordinator", f"📋 Sprint Planning: {len(jira_tickets)} tickets")
        
        sprint_plan = {
            'sprint_goal': sprint_goal or "Complete planned tickets",
            'start_date': datetime.now().isoformat(),
            'tickets': [],
            'total_story_points': 0,
            'assignments': {}
        }
        
        # Review and estimate each ticket
        for i, ticket in enumerate(jira_tickets, 1):
            print(f"\n📝 Ticket {i}: {ticket.get('key', 'UNKNOWN')}")
            print(f"   Summary: {ticket.get('summary', 'No summary')}")
            
            # Simulate team estimation (in real implementation, use LLM)
            story_points = self._estimate_story_points(ticket)
            print(f"   Story Points: {story_points}")
            
            # Assign to appropriate agent
            assigned_to = self._assign_ticket(ticket)
            print(f"   Assigned to: {assigned_to}")
            
            ticket_plan = {
                'ticket': ticket,
                'story_points': story_points,
                'assigned_to': assigned_to
            }
            
            sprint_plan['tickets'].append(ticket_plan)
            sprint_plan['total_story_points'] += story_points
            
            if assigned_to not in sprint_plan['assignments']:
                sprint_plan['assignments'][assigned_to] = []
            sprint_plan['assignments'][assigned_to].append(ticket.get('key', 'UNKNOWN'))
        
        print("\n" + "="*70)
        print(f"✅ Sprint Planned!")
        print(f"   Total Story Points: {sprint_plan['total_story_points']}")
        print(f"   Assignments: {sprint_plan['assignments']}")
        print("="*70 + "\n")
        
        self.current_sprint = sprint_plan
        self.memory.store('current_sprint', sprint_plan)
        
        # Announce to team
        self.message_bus.announce_decision(
            "Team Coordinator",
            f"Sprint planned: {sprint_plan['total_story_points']} points, {len(jira_tickets)} tickets"
        )
        
        return sprint_plan
    
    def _estimate_story_points(self, ticket: Dict) -> int:
        """Estimate story points for a ticket (simplified)"""
        # In real implementation, this would use LLM to analyze complexity
        ticket_type = ticket.get('type', 'Story').lower()
        
        if 'epic' in ticket_type:
            return 13  # Large effort
        elif 'bug' in ticket_type:
            return 3   # Small-medium
        else:
            return 5   # Medium (typical story)
    
    def _assign_ticket(self, ticket: Dict) -> str:
        """Assign ticket to appropriate agent based on type"""
        ticket_type = ticket.get('type', 'Story').lower()
        summary = ticket.get('summary', '').lower()
        
        # Check for specialized assignments
        if 'database' in summary or 'schema' in summary or 'migration' in summary:
            return 'DBA'
        elif 'cicd' in summary or 'deploy' in summary or 'infrastructure' in summary or 'pipeline' in summary:
            return 'DevOps'
        elif 'test' in summary or 'qa' in summary:
            return 'QA'
        elif 'architecture' in summary or 'design' in summary:
            return 'Architect'
        elif 'requirements' in summary or 'story' in summary:
            return 'BA'
        elif 'review' in summary:
            return 'Tech Lead'
        elif 'ui' in summary or 'frontend' in summary or 'react' in summary:
            return 'Dev-Frontend-1'
        elif 'api' in summary or 'backend' in summary or 'service' in summary:
            return 'Dev-Backend-1'
        else:
            return 'Dev-FullStack'
    
    def facilitate_discussion(self, 
                            topic: str, 
                            participants: List[str],
                            context: Dict = None) -> Dict[str, Any]:
        """
        Facilitate a team discussion on a specific topic
        
        Args:
            topic: Discussion topic
            participants: List of agents to participate
            context: Additional context for discussion
        
        Returns:
            Discussion summary with outcomes
        """
        print("\n" + "="*70)
        print(f"💬 TEAM DISCUSSION: {topic}")
        print("="*70)
        print(f"Participants: {', '.join(participants)}")
        
        discussion = {
            'topic': topic,
            'participants': participants,
            'context': context or {},
            'start_time': datetime.now().isoformat(),
            'contributions': [],
            'decisions': [],
            'action_items': []
        }
        
        # Announce discussion
        self.message_bus.post_message(
            "Team Coordinator",
            MessageType.ANNOUNCEMENT,
            f"💬 Starting discussion: {topic}",
            mentions=participants
        )
        
        print(f"\n📢 Discussion in progress...")
        print(f"   (In real implementation, agents would contribute via LLM)")
        print(f"   Context: {context}")
        
        # Simulate discussion (in real implementation, each agent would contribute)
        for participant in participants:
            contribution = f"{participant}'s perspective on {topic}"
            discussion['contributions'].append({
                'agent': participant,
                'contribution': contribution
            })
            print(f"   • {participant}: Contributing...")
        
        # Synthesize decision
        decision = f"Team consensus on {topic}"
        discussion['decisions'].append(decision)
        
        print(f"\n✅ Discussion Complete")
        print(f"   Decision: {decision}")
        print("="*70 + "\n")
        
        # Announce decision
        self.message_bus.announce_decision("Team Coordinator", decision)
        
        discussion['end_time'] = datetime.now().isoformat()
        self.decisions.append(discussion)
        
        return discussion
    
    def escalate_blocker(self, 
                        blocker: str, 
                        reported_by: str,
                        suggested_solutions: List[str] = None) -> Dict[str, Any]:
        """
        Handle blocker escalation
        
        Args:
            blocker: Description of the blocker
            reported_by: Agent reporting the blocker
            suggested_solutions: Possible solutions
        
        Returns:
            Escalation record with resolution plan
        """
        print("\n" + "="*70)
        print(f"🚨 BLOCKER ESCALATION")
        print("="*70)
        print(f"Reported by: {reported_by}")
        print(f"Blocker: {blocker}")
        
        escalation = {
            'blocker': blocker,
            'reported_by': reported_by,
            'reported_at': datetime.now().isoformat(),
            'suggested_solutions': suggested_solutions or [],
            'status': 'escalated',
            'resolution': None
        }
        
        # Broadcast blocker to team
        self.message_bus.report_blocker(
            reported_by,
            blocker,
            f"Escalated to team for resolution"
        )
        
        # Identify helpers
        print(f"\n📢 Requesting help from team...")
        
        if suggested_solutions:
            print(f"💡 Suggested Solutions:")
            for sol in suggested_solutions:
                print(f"   • {sol}")
        
        # In real implementation, would facilitate discussion to resolve
        resolution = "Team to discuss and resolve in next meeting"
        escalation['resolution'] = resolution
        escalation['status'] = 'pending_resolution'
        
        print(f"\n✅ Escalation Recorded")
        print(f"   Next Steps: {resolution}")
        print("="*70 + "\n")
        
        self.blockers.append(escalation)
        self.memory.store('active_blockers', self.blockers)
        
        return escalation
    
    def retrospective(self, sprint_data: Dict = None) -> Dict[str, Any]:
        """
        Facilitate sprint retrospective
        - What went well
        - What could improve
        - Action items for next sprint
        """
        print("\n" + "="*70)
        print("🔄 SPRINT RETROSPECTIVE")
        print("="*70)
        
        retro = {
            'date': datetime.now().isoformat(),
            'sprint_data': sprint_data or self.current_sprint,
            'went_well': [],
            'improvements': [],
            'action_items': [],
            'learnings': []
        }
        
        # Gather feedback (in real implementation, each agent would contribute)
        print("\n✅ What Went Well:")
        retro['went_well'] = [
            "Good collaboration between BA and Architect",
            "Clear requirements led to faster development",
            "TDD approach caught bugs early"
        ]
        for item in retro['went_well']:
            print(f"   • {item}")
        
        print("\n🔧 What Could Improve:")
        retro['improvements'] = [
            "Need better test coverage documentation",
            "Code review feedback could be more detailed",
            "Faster JIRA response time needed"
        ]
        for item in retro['improvements']:
            print(f"   • {item}")
        
        print("\n📋 Action Items:")
        retro['action_items'] = [
            "BA to create test coverage template",
            "Tech Lead to create code review checklist",
            "Set up JIRA webhook notifications"
        ]
        for item in retro['action_items']:
            print(f"   • {item}")
        
        print("\n💡 Key Learnings:")
        retro['learnings'] = self.learnings[-3:] if self.learnings else [
            "Early collaboration prevents rework",
            "Automated tests save review time",
            "Clear communication reduces blockers"
        ]
        for item in retro['learnings']:
            print(f"   • {item}")
        
        print("\n" + "="*70)
        print("✅ Retrospective Complete - Team will improve!")
        print("="*70 + "\n")
        
        # Store retrospective
        self.memory.store('latest_retrospective', retro)
        
        # Announce to team
        self.message_bus.broadcast(
            "Team Coordinator",
            f"🔄 Retrospective complete. {len(retro['action_items'])} action items for next sprint."
        )
        
        return retro
    
    def get_team_metrics(self) -> Dict[str, Any]:
        """Get current team performance metrics"""
        message_summary = self.message_bus.get_team_summary()
        
        metrics = {
            'team_size': len(self.team_members),
            'active_sprint': self.current_sprint is not None,
            'sprint_points': self.current_sprint.get('total_story_points', 0) if self.current_sprint else 0,
            'active_blockers': len([b for b in self.blockers if b['status'] == 'escalated']),
            'total_decisions': len(self.decisions),
            'total_learnings': len(self.learnings),
            'communication_stats': message_summary
        }
        
        return metrics
    
    def print_team_dashboard(self):
        """Print a dashboard of team status"""
        metrics = self.get_team_metrics()
        
        print("\n" + "="*70)
        print(f"📊 TEAM DASHBOARD - {self.team_name}")
        print("="*70)
        print(f"\n👥 Team:")
        for name, info in self.team_members.items():
            print(f"   {name:15} - {info['role']}")
        
        print(f"\n📈 Current Sprint:")
        if self.current_sprint:
            print(f"   Goal: {self.current_sprint.get('sprint_goal', 'N/A')}")
            print(f"   Story Points: {metrics['sprint_points']}")
            print(f"   Tickets: {len(self.current_sprint.get('tickets', []))}")
        else:
            print(f"   No active sprint")
        
        print(f"\n🚫 Blockers: {metrics['active_blockers']}")
        print(f"✅ Decisions Made: {metrics['total_decisions']}")
        print(f"💡 Learnings Shared: {metrics['total_learnings']}")
        
        print(f"\n💬 Communication:")
        comm = metrics['communication_stats']
        print(f"   Total Messages: {comm['total_messages']}")
        print(f"   Active Threads: {comm['active_threads']}")
        
        print("="*70 + "\n")


if __name__ == "__main__":
    # Demo usage
    print("Team Coordinator Demo\n")
    
    coordinator = TeamCoordinator("AI Development Team Alpha")
    
    # Daily standup
    coordinator.daily_standup()
    
    # Sprint planning
    sample_tickets = [
        {'key': 'EPIC-1', 'summary': 'Implement user authentication', 'type': 'Story'},
        {'key': 'EPIC-2', 'summary': 'Design database schema', 'type': 'Story'},
        {'key': 'EPIC-3', 'summary': 'Create integration tests', 'type': 'Story'}
    ]
    coordinator.sprint_planning(sample_tickets, "Deliver authentication module")
    
    # Team discussion
    coordinator.facilitate_discussion(
        "Architecture approach for auth module",
        ["Architect", "Developer", "QA"],
        {'complexity': 'medium', 'security_critical': True}
    )
    
    # Handle blocker
    coordinator.escalate_blocker(
        "JIRA API rate limit reached",
        "BA",
        ["Use caching", "Implement backoff strategy", "Request rate limit increase"]
    )
    
    # Sprint retrospective
    coordinator.retrospective()
    
    # Show dashboard
    coordinator.print_team_dashboard()
