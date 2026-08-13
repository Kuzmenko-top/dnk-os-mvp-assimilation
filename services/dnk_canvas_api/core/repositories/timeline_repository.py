# --- DNK-MRH-HEADER ---
# mrh_id: "core/repositories/timeline_repository.py"
# purpose: "Timeline Repository Interface + PostgreSQL implementation"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---
"""Timeline Repository Interface + PostgreSQL implementation."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..security.models import TimelineEvent


class ITimelineRepository(ABC):
    """Interface for timeline storage."""
    
    @abstractmethod
    async def log_action_start(
        self,
        run_id: UUID,
        agent_id: str,
        action_name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """Log action start event."""
        pass
    
    @abstractmethod
    async def log_action_end(
        self,
        run_id: UUID,
        agent_id: str,
        action_name: str,
        status: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """Log action end event."""
        pass
    
    @abstractmethod
    async def get_timeline_by_run(
        self,
        run_id: UUID,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get timeline events for a specific run."""
        pass


class PostgreSQLTimelineRepository(ITimelineRepository):
    """PostgreSQL implementation of timeline repository."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def log_action_start(
        self,
        run_id: UUID,
        agent_id: str,
        action_name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """Log action start to PostgreSQL."""
        event_id = uuid4()
        event = TimelineEvent(
            id=event_id,
            run_id=run_id,
            agent_id=agent_id,
            event_type='action_start',
            status='pending',
            action_name=action_name,
            payload_json=payload,
        )
        
        self.db.add(event)
        await self.db.commit()
        
        return event_id
    
    async def log_action_end(
        self,
        run_id: UUID,
        agent_id: str,
        action_name: str,
        status: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """Log action end to PostgreSQL."""
        event_id = uuid4()
        event = TimelineEvent(
            id=event_id,
            run_id=run_id,
            agent_id=agent_id,
            event_type='action_end',
            status=status,
            action_name=action_name,
            payload_json=payload,
        )
        
        self.db.add(event)
        await self.db.commit()
        
        return event_id
    
    async def get_timeline_by_run(
        self,
        run_id: UUID,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query timeline by run_id."""
        stmt = (
            select(TimelineEvent)
            .where(TimelineEvent.run_id == run_id)
            .order_by(TimelineEvent.timestamp.desc())
            .limit(limit)
        )
        
        result = await self.db.execute(stmt)
        events = result.scalars().all()
        
        return [
            {
                'id': event.id,
                'run_id': event.run_id,
                'agent_id': event.agent_id,
                'event_type': event.event_type,
                'status': event.status,
                'action_name': event.action_name,
                'payload_json': event.payload_json,
                'timestamp': event.timestamp,
            }
            for event in events
        ]
