# --- DNK-MRH-HEADER ---
# mrh_id: "tests/test_timeline_logger.py"
# purpose: "Unit tests for TimelineLogger engine and secret sanitization"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---
"""Tests for timeline logger: sanitization, log_action_start/end."""
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from core.utils.timeline_logger import TimelineLogger
from core.repositories.timeline_repository import PostgreSQLTimelineRepository


class TestTimelineLogger:
    """Test timeline logger functionality."""
    
    @pytest.mark.anyio
    async def test_log_action_start(self):
        """Test log_action_start creates event."""
        # Mock repository
        mock_repo = AsyncMock()
        logger = TimelineLogger(mock_repo)
        
        run_id = uuid4()
        agent_id = "test_agent"
        action_name = "delete_canvas"
        
        event_id = await logger.log_action_start(run_id, agent_id, action_name)
        
        assert event_id is not None
        assert mock_repo.log_action_start.called
    
    @pytest.mark.anyio
    async def test_log_action_end(self):
        """Test log_action_end creates event."""
        # Mock repository
        mock_repo = AsyncMock()
        logger = TimelineLogger(mock_repo)
        
        run_id = uuid4()
        agent_id = "test_agent"
        action_name = "delete_canvas"
        status = "success"
        
        event_id = await logger.log_action_end(run_id, agent_id, action_name, status)
        
        assert event_id is not None
        assert mock_repo.log_action_end.called
    
    @pytest.mark.anyio
    async def test_sanitization_masks_secrets(self):
        """Test sanitization masks passwords, tokens, secrets."""
        mock_repo = AsyncMock()
        logger = TimelineLogger(mock_repo)
        
        payload = {
            "username": "admin",
            "password": "supersecret123",
            "api_key": "sk-1234567890",
            "token": "ghp_xxxxxxxxxxxx",
        }
        
        sanitized = logger._sanitize_payload(payload)
        
        assert "supersecret123" not in str(sanitized)
        assert "sk-1234567890" not in str(sanitized)
        assert "ghp_xxxxxxxxxxxx" not in str(sanitized)
        assert "***REDACTED***" in str(sanitized)
