# --- DNK-MRH-HEADER ---
# mrh_id: "tests/test_timeline_repository.py"
# purpose: "Unit tests for PostgreSQLTimelineRepository"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---
"""Tests for timeline repository."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from core.repositories.timeline_repository import PostgreSQLTimelineRepository


class TestPostgreSQLTimelineRepository:
    """Test timeline repository implementation."""
    
    @pytest.mark.anyio
    async def test_log_action_start(self):
        """Test log_action_start creates event."""
        # Mock DB session
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        repo = PostgreSQLTimelineRepository(mock_db)
        
        run_id = uuid4()
        agent_id = "test_agent"
        action_name = "delete_canvas"
        
        event_id = await repo.log_action_start(run_id, agent_id, action_name)
        
        assert event_id is not None
        assert mock_db.add.called
        assert mock_db.commit.called
    
    @pytest.mark.anyio
    async def test_log_action_end(self):
        """Test log_action_end creates event."""
        # Mock DB session
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        repo = PostgreSQLTimelineRepository(mock_db)
        
        run_id = uuid4()
        agent_id = "test_agent"
        action_name = "delete_canvas"
        status = "success"
        
        event_id = await repo.log_action_end(run_id, agent_id, action_name, status)
        
        assert event_id is not None
        assert mock_db.add.called
        assert mock_db.commit.called
    
    @pytest.mark.anyio
    async def test_get_timeline_by_run(self):
        """Test get_timeline_by_run returns events."""
        # Mock DB session
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result
        
        repo = PostgreSQLTimelineRepository(mock_db)
        
        run_id = uuid4()
        events = await repo.get_timeline_by_run(run_id)
        
        assert isinstance(events, list)
        assert mock_db.execute.called
