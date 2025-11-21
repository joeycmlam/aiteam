"""
Agent Collaboration - Patterns for agents working together

Supports:
- Pair programming (2 agents on same task)
- Code review cycles (Developer -> Tech Lead -> Developer)
- Cross-functional reviews (Developer -> QA -> DBA -> DevOps)
- Architecture review boards (Architect + Tech Lead + Senior Devs)
- Knowledge sharing and handoffs
"""

from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from datetime import datetime
from shared.team_messaging import get_message_bus, MessageType


class CollaborationPattern(Enum):
    """Types of collaboration patterns"""
    PAIR_PROGRAMMING = "pair_programming"
    CODE_REVIEW = "code_review"
    CROSS_FUNCTIONAL_REVIEW = "cross_functional_review"
    ARCHITECTURE_REVIEW = "architecture_review"
    KNOWLEDGE_TRANSFER = "knowledge_transfer"
    BRAINSTORMING = "brainstorming"


class CollaborationSession:
    """A collaboration session between agents"""
    
    def __init__(self,
                 session_id: str,
                 pattern: CollaborationPattern,
                 participants: List[str],
                 context: Dict = None):
        self.session_id = session_id
        self.pattern = pattern
        self.participants = participants
        self.context = context or {}
        
        self.started_at = datetime.now()
        self.ended_at = None
        self.contributions = []
        self.decisions = []
        self.artifacts = []
        
        print(f"🤝 Collaboration session started: {session_id}")
        print(f"   Pattern: {pattern.value}")
        print(f"   Participants: {', '.join(participants)}")
    
    def add_contribution(self, agent: str, contribution: Dict):
        """Add a contribution from an agent"""
        self.contributions.append({
            'agent': agent,
            'timestamp': datetime.now().isoformat(),
            'contribution': contribution
        })
    
    def add_decision(self, decision: str, decided_by: List[str] = None):
        """Record a decision made during collaboration"""
        self.decisions.append({
            'decision': decision,
            'decided_by': decided_by or self.participants,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_artifact(self, artifact_type: str, content: Any):
        """Add an artifact produced during collaboration"""
        self.artifacts.append({
            'type': artifact_type,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def end_session(self, summary: str = None):
        """End the collaboration session"""
        self.ended_at = datetime.now()
        duration = (self.ended_at - self.started_at).total_seconds()
        
        print(f"✅ Collaboration session ended: {self.session_id}")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Contributions: {len(self.contributions)}")
        print(f"   Decisions: {len(self.decisions)}")
        print(f"   Artifacts: {len(self.artifacts)}")
        
        if summary:
            print(f"   Summary: {summary}")
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'pattern': self.pattern.value,
            'participants': self.participants,
            'context': self.context,
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'contributions': self.contributions,
            'decisions': self.decisions,
            'artifacts': self.artifacts
        }


class AgentCollaboration:
    """Manages agent collaboration patterns"""
    
    def __init__(self):
        self.message_bus = get_message_bus()
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.completed_sessions: List[CollaborationSession] = []
        self.session_counter = 0
        
        print("🤝 Agent Collaboration system initialized")
    
    def start_pair_programming(self,
                              developer1: str,
                              developer2: str,
                              task: Dict) -> CollaborationSession:
        """
        Start a pair programming session
        
        Args:
            developer1: Driver developer
            developer2: Navigator developer
            task: Task to work on together
            
        Returns:
            Collaboration session
        """
        self.session_counter += 1
        session_id = f"PAIR-{self.session_counter:04d}"
        
        session = CollaborationSession(
            session_id=session_id,
            pattern=CollaborationPattern.PAIR_PROGRAMMING,
            participants=[developer1, developer2],
            context={
                'task': task,
                'roles': {
                    developer1: 'driver',
                    developer2: 'navigator'
                }
            }
        )
        
        self.active_sessions[session_id] = session
        
        # Notify participants
        self.message_bus.post_message(
            "Collaboration Manager",
            MessageType.ANNOUNCEMENT,
            f"🤝 Pair programming: {developer1} (driver) + {developer2} (navigator)",
            mentions=[developer1, developer2]
        )
        
        return session
    
    def start_code_review(self,
                         author: str,
                         reviewer: str,
                         code: Dict) -> CollaborationSession:
        """
        Start a code review cycle
        
        Args:
            author: Code author
            reviewer: Code reviewer
            code: Code to review
            
        Returns:
            Collaboration session
        """
        self.session_counter += 1
        session_id = f"REVIEW-{self.session_counter:04d}"
        
        session = CollaborationSession(
            session_id=session_id,
            pattern=CollaborationPattern.CODE_REVIEW,
            participants=[author, reviewer],
            context={
                'code': code,
                'author': author,
                'reviewer': reviewer,
                'review_status': 'pending'
            }
        )
        
        self.active_sessions[session_id] = session
        
        # Notify participants
        self.message_bus.post_message(
            author,
            MessageType.REQUEST,
            f"🔍 Code review requested from {reviewer}",
            mentions=[reviewer]
        )
        
        return session
    
    def start_cross_functional_review(self,
                                     deliverable: Dict,
                                     reviewers: List[str]) -> CollaborationSession:
        """
        Start a cross-functional review
        
        Args:
            deliverable: Work product to review
            reviewers: List of reviewers from different disciplines
            
        Returns:
            Collaboration session
        """
        self.session_counter += 1
        session_id = f"XREVIEW-{self.session_counter:04d}"
        
        session = CollaborationSession(
            session_id=session_id,
            pattern=CollaborationPattern.CROSS_FUNCTIONAL_REVIEW,
            participants=reviewers,
            context={
                'deliverable': deliverable,
                'reviews_required': len(reviewers),
                'reviews_completed': 0
            }
        )
        
        self.active_sessions[session_id] = session
        
        # Notify all reviewers
        self.message_bus.broadcast(
            "Collaboration Manager",
            f"🔍 Cross-functional review requested: {len(reviewers)} reviewers"
        )
        
        return session
    
    def start_architecture_review_board(self,
                                       architecture: Dict,
                                       board_members: List[str]) -> CollaborationSession:
        """
        Start an architecture review board
        
        Args:
            architecture: Architecture design to review
            board_members: Review board members
            
        Returns:
            Collaboration session
        """
        self.session_counter += 1
        session_id = f"ARB-{self.session_counter:04d}"
        
        session = CollaborationSession(
            session_id=session_id,
            pattern=CollaborationPattern.ARCHITECTURE_REVIEW,
            participants=board_members,
            context={
                'architecture': architecture,
                'approval_required': True,
                'votes': {}
            }
        )
        
        self.active_sessions[session_id] = session
        
        # Notify board members
        self.message_bus.broadcast(
            "Collaboration Manager",
            f"🏛️ Architecture Review Board convened: {len(board_members)} members"
        )
        
        return session
    
    def conduct_brainstorming(self,
                            topic: str,
                            participants: List[str],
                            duration_minutes: int = 30) -> CollaborationSession:
        """
        Conduct a brainstorming session
        
        Args:
            topic: Topic to brainstorm
            participants: Participating agents
            duration_minutes: Session duration
            
        Returns:
            Collaboration session
        """
        self.session_counter += 1
        session_id = f"BRAIN-{self.session_counter:04d}"
        
        session = CollaborationSession(
            session_id=session_id,
            pattern=CollaborationPattern.BRAINSTORMING,
            participants=participants,
            context={
                'topic': topic,
                'duration_minutes': duration_minutes,
                'ideas': []
            }
        )
        
        self.active_sessions[session_id] = session
        
        # Notify participants
        self.message_bus.broadcast(
            "Collaboration Manager",
            f"💡 Brainstorming session: {topic}"
        )
        
        return session
    
    def transfer_knowledge(self,
                          from_agent: str,
                          to_agent: str,
                          knowledge_area: str,
                          content: Dict) -> CollaborationSession:
        """
        Facilitate knowledge transfer between agents
        
        Args:
            from_agent: Knowledge source agent
            to_agent: Knowledge recipient agent
            knowledge_area: Area of knowledge
            content: Knowledge content
            
        Returns:
            Collaboration session
        """
        self.session_counter += 1
        session_id = f"KT-{self.session_counter:04d}"
        
        session = CollaborationSession(
            session_id=session_id,
            pattern=CollaborationPattern.KNOWLEDGE_TRANSFER,
            participants=[from_agent, to_agent],
            context={
                'knowledge_area': knowledge_area,
                'content': content,
                'source': from_agent,
                'recipient': to_agent
            }
        )
        
        self.active_sessions[session_id] = session
        
        # Notify participants
        self.message_bus.post_message(
            from_agent,
            MessageType.ANNOUNCEMENT,
            f"📚 Knowledge transfer to {to_agent}: {knowledge_area}",
            mentions=[to_agent]
        )
        
        return session
    
    def add_contribution_to_session(self,
                                   session_id: str,
                                   agent: str,
                                   contribution: Dict):
        """Add agent contribution to session"""
        session = self.active_sessions.get(session_id)
        if session:
            session.add_contribution(agent, contribution)
            print(f"   ✅ Contribution added by {agent}")
    
    def record_decision(self,
                       session_id: str,
                       decision: str,
                       decided_by: List[str] = None):
        """Record decision from session"""
        session = self.active_sessions.get(session_id)
        if session:
            session.add_decision(decision, decided_by)
            print(f"   ✅ Decision recorded: {decision}")
    
    def end_collaboration(self, session_id: str, summary: str = None):
        """End a collaboration session"""
        session = self.active_sessions.pop(session_id, None)
        if session:
            session.end_session(summary)
            self.completed_sessions.append(session)
            
            # Broadcast completion
            self.message_bus.broadcast(
                "Collaboration Manager",
                f"✅ Collaboration complete: {session_id}"
            )
    
    def get_active_sessions(self) -> List[CollaborationSession]:
        """Get all active collaboration sessions"""
        return list(self.active_sessions.values())
    
    def get_session(self, session_id: str) -> Optional[CollaborationSession]:
        """Get specific session by ID"""
        return self.active_sessions.get(session_id)
    
    def get_agent_collaborations(self, agent: str) -> List[CollaborationSession]:
        """Get all collaborations involving an agent"""
        sessions = []
        for session in self.active_sessions.values():
            if agent in session.participants:
                sessions.append(session)
        return sessions
    
    def print_active_sessions(self):
        """Print all active collaboration sessions"""
        sessions = self.get_active_sessions()
        
        print("\n" + "="*70)
        print("🤝 ACTIVE COLLABORATION SESSIONS")
        print("="*70)
        
        if not sessions:
            print("No active sessions")
        else:
            for session in sessions:
                duration = (datetime.now() - session.started_at).total_seconds() / 60
                print(f"\n{session.session_id} - {session.pattern.value}")
                print(f"   Participants: {', '.join(session.participants)}")
                print(f"   Duration: {duration:.1f} minutes")
                print(f"   Contributions: {len(session.contributions)}")
        
        print("="*70 + "\n")


# Singleton instance
_collaboration_instance = None


def get_collaboration_manager() -> AgentCollaboration:
    """Get singleton collaboration manager instance"""
    global _collaboration_instance
    if _collaboration_instance is None:
        _collaboration_instance = AgentCollaboration()
    return _collaboration_instance


if __name__ == "__main__":
    # Demo usage
    print("Agent Collaboration Demo\n")
    
    collab = get_collaboration_manager()
    
    # Pair programming
    session1 = collab.start_pair_programming(
        "Dev-Frontend-1",
        "Dev-Frontend-2",
        {"name": "Implement user dashboard", "type": "frontend"}
    )
    
    # Code review
    session2 = collab.start_code_review(
        "Dev-Backend-1",
        "Tech Lead",
        {"files": ["auth.py", "users.py"]}
    )
    
    # Cross-functional review
    session3 = collab.start_cross_functional_review(
        {"type": "API Implementation", "components": ["auth", "users"]},
        ["Tech Lead", "QA", "DBA", "DevOps"]
    )
    
    # Show active sessions
    collab.print_active_sessions()
    
    # Add contributions
    collab.add_contribution_to_session(
        session1.session_id,
        "Dev-Frontend-1",
        {"code": "Dashboard component implemented"}
    )
    
    # Record decisions
    collab.record_decision(
        session3.session_id,
        "API design approved with minor changes",
        ["Tech Lead", "Architect"]
    )
    
    # End sessions
    collab.end_collaboration(session1.session_id, "Dashboard completed successfully")
    
    print("\n✅ Demo complete")
