"""
Team Messaging System - Communication hub for AI agent team
Enables professional team collaboration through structured messaging
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json


class MessageType(Enum):
    """Types of messages agents can send"""
    STATUS = "status"  # Progress updates
    QUESTION = "question"  # Questions to other agents
    HELP_REQUEST = "help_request"  # Request for assistance
    ANNOUNCEMENT = "announcement"  # Team-wide announcements
    DECISION = "decision"  # Decision notifications
    FEEDBACK = "feedback"  # Feedback on work
    BLOCKER = "blocker"  # Report blockers
    LEARNING = "learning"  # Share learnings


class Message:
    """Individual message in team communication"""
    
    def __init__(self, 
                 from_agent: str,
                 message_type: MessageType,
                 content: str,
                 to_agent: Optional[str] = None,
                 mentions: List[str] = None,
                 thread_id: Optional[str] = None):
        self.id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type
        self.content = content
        self.mentions = mentions or []
        self.thread_id = thread_id
        self.timestamp = datetime.now().isoformat()
        self.responses = []
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'from_agent': self.from_agent,
            'to_agent': self.to_agent,
            'message_type': self.message_type.value,
            'content': self.content,
            'mentions': self.mentions,
            'thread_id': self.thread_id,
            'timestamp': self.timestamp,
            'responses': self.responses
        }
    
    def __repr__(self):
        return f"[{self.message_type.value}] {self.from_agent} → {self.to_agent or 'Team'}: {self.content[:50]}..."


class TeamMessageBus:
    """
    Central communication hub for the AI agent team
    Manages all inter-agent communication and collaboration
    """
    
    def __init__(self):
        self.messages: List[Message] = []
        self.threads: Dict[str, List[Message]] = {}
        self.agent_inbox: Dict[str, List[Message]] = {}
        print("💬 Team Message Bus initialized")
    
    def post_message(self, 
                     from_agent: str,
                     message_type: MessageType,
                     content: str,
                     to_agent: Optional[str] = None,
                     mentions: List[str] = None,
                     thread_id: Optional[str] = None) -> Message:
        """
        Post a message to the team
        
        Args:
            from_agent: Agent sending the message
            message_type: Type of message (status, question, etc.)
            content: Message content
            to_agent: Specific agent to message (optional, None for broadcast)
            mentions: List of agents to mention/notify
            thread_id: Thread to reply to (for threading conversations)
        
        Returns:
            Created message object
        """
        message = Message(from_agent, message_type, content, to_agent, mentions, thread_id)
        self.messages.append(message)
        
        # Add to thread if specified
        if thread_id:
            if thread_id not in self.threads:
                self.threads[thread_id] = []
            self.threads[thread_id].append(message)
        
        # Add to recipient's inbox
        if to_agent:
            if to_agent not in self.agent_inbox:
                self.agent_inbox[to_agent] = []
            self.agent_inbox[to_agent].append(message)
        
        # Add to mentioned agents' inboxes
        if mentions:
            for agent in mentions:
                if agent not in self.agent_inbox:
                    self.agent_inbox[agent] = []
                self.agent_inbox[agent].append(message)
        
        # Print message to console for visibility
        self._print_message(message)
        
        return message
    
    def _print_message(self, message: Message):
        """Pretty print a message to console"""
        icon = {
            MessageType.STATUS: "📊",
            MessageType.QUESTION: "❓",
            MessageType.HELP_REQUEST: "🆘",
            MessageType.ANNOUNCEMENT: "📢",
            MessageType.DECISION: "✅",
            MessageType.FEEDBACK: "💭",
            MessageType.BLOCKER: "🚫",
            MessageType.LEARNING: "💡"
        }.get(message.message_type, "💬")
        
        recipient = f" → {message.to_agent}" if message.to_agent else " → Team"
        mentions_str = f" @{', @'.join(message.mentions)}" if message.mentions else ""
        
        print(f"\n{icon} [{message.from_agent}]{recipient}{mentions_str}")
        print(f"   {message.content}")
    
    def get_messages_for(self, agent: str, unread_only: bool = False) -> List[Message]:
        """Get all messages for a specific agent"""
        return self.agent_inbox.get(agent, [])
    
    def get_thread(self, thread_id: str) -> List[Message]:
        """Get all messages in a conversation thread"""
        return self.threads.get(thread_id, [])
    
    def broadcast(self, from_agent: str, content: str, message_type: MessageType = MessageType.ANNOUNCEMENT) -> Message:
        """Send a message to all agents"""
        return self.post_message(from_agent, message_type, content)
    
    def request_help(self, 
                     from_agent: str, 
                     issue: str, 
                     suggested_helpers: List[str] = None) -> Message:
        """Request help from other agents"""
        content = f"🆘 Help needed: {issue}"
        if suggested_helpers:
            content += f"\n   Requesting: {', '.join(suggested_helpers)}"
        
        return self.post_message(
            from_agent, 
            MessageType.HELP_REQUEST, 
            content,
            mentions=suggested_helpers
        )
    
    def report_blocker(self, from_agent: str, blocker: str, impact: str) -> Message:
        """Report a blocker to the team"""
        content = f"🚫 Blocker: {blocker}\n   Impact: {impact}"
        return self.post_message(from_agent, MessageType.BLOCKER, content)
    
    def share_learning(self, from_agent: str, learning: str) -> Message:
        """Share a learning or insight with the team"""
        content = f"💡 Learning: {learning}"
        return self.post_message(from_agent, MessageType.LEARNING, content)
    
    def ask_question(self, 
                     from_agent: str, 
                     question: str, 
                     to_agent: Optional[str] = None) -> Message:
        """Ask a question to another agent or the team"""
        return self.post_message(from_agent, MessageType.QUESTION, question, to_agent)
    
    def provide_feedback(self, 
                        from_agent: str, 
                        to_agent: str, 
                        feedback: str) -> Message:
        """Provide feedback to another agent"""
        return self.post_message(from_agent, MessageType.FEEDBACK, feedback, to_agent)
    
    def announce_decision(self, from_agent: str, decision: str) -> Message:
        """Announce a decision to the team"""
        return self.post_message(from_agent, MessageType.DECISION, decision)
    
    def get_recent_messages(self, count: int = 10) -> List[Message]:
        """Get most recent messages"""
        return self.messages[-count:] if len(self.messages) > count else self.messages
    
    def get_team_summary(self) -> Dict[str, Any]:
        """Get summary of team communication"""
        summary = {
            'total_messages': len(self.messages),
            'messages_by_type': {},
            'messages_by_agent': {},
            'active_threads': len(self.threads),
            'agents_with_messages': len(self.agent_inbox)
        }
        
        # Count by type
        for msg in self.messages:
            msg_type = msg.message_type.value
            summary['messages_by_type'][msg_type] = summary['messages_by_type'].get(msg_type, 0) + 1
        
        # Count by agent
        for msg in self.messages:
            agent = msg.from_agent
            summary['messages_by_agent'][agent] = summary['messages_by_agent'].get(agent, 0) + 1
        
        return summary
    
    def save_transcript(self, filepath: str = "team_chat_transcript.json"):
        """Save chat transcript to file"""
        transcript = {
            'messages': [msg.to_dict() for msg in self.messages],
            'summary': self.get_team_summary()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2)
        
        print(f"💾 Team transcript saved to: {filepath}")
    
    def print_recent_activity(self, count: int = 5):
        """Print recent team activity"""
        print(f"\n{'='*70}")
        print(f"📋 Recent Team Activity (last {count} messages)")
        print(f"{'='*70}")
        
        recent = self.get_recent_messages(count)
        if not recent:
            print("   No messages yet")
        else:
            for msg in recent:
                self._print_message(msg)
        
        print(f"{'='*70}\n")


# Singleton instance for easy access
_message_bus_instance = None

def get_message_bus() -> TeamMessageBus:
    """Get the global message bus instance"""
    global _message_bus_instance
    if _message_bus_instance is None:
        _message_bus_instance = TeamMessageBus()
    return _message_bus_instance


if __name__ == "__main__":
    # Demo usage
    print("Team Messaging System Demo\n")
    
    bus = TeamMessageBus()
    
    # BA posts status
    bus.post_message("BA", MessageType.STATUS, "Starting requirements analysis for EPIC-123")
    
    # BA asks question to Architect
    bus.ask_question("BA", "What's the recommended architecture pattern for this use case?", "Architect")
    
    # Architect responds
    bus.post_message("Architect", MessageType.FEEDBACK, "I recommend using microservices architecture", "BA")
    
    # Developer requests help
    bus.request_help("Developer", "Need help with authentication implementation", ["Tech Lead", "Architect"])
    
    # Tech Lead shares learning
    bus.share_learning("Tech Lead", "Using JWT tokens improves security and scalability")
    
    # QA reports blocker
    bus.report_blocker("QA", "Test environment is down", "Cannot run integration tests")
    
    # Lead makes decision
    bus.announce_decision("Lead", "We'll proceed with microservices architecture as recommended")
    
    # Print summary
    print("\n" + "="*70)
    summary = bus.get_team_summary()
    print(f"Team Communication Summary:")
    print(f"  Total Messages: {summary['total_messages']}")
    print(f"  Active Threads: {summary['active_threads']}")
    print(f"  Messages by Type: {summary['messages_by_type']}")
    print("="*70)
