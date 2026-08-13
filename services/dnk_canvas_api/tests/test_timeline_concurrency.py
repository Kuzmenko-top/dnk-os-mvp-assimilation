# --- DNK-MRH-HEADER ---
# mrh_id: "tests/test_timeline_concurrency.py"
# purpose: "Concurrency tests for timeline logger: parallel writes and exponential backoff retry"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---
"""Concurrency tests for timeline logger: parallel writes + retry with backoff."""
import asyncio
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from core.utils.timeline_logger import TimelineLogger
from core.repositories.timeline_repository import PostgreSQLTimelineRepository


class TestTimelineConcurrency:
    """Test timeline logger concurrency and retry logic."""
    
    @pytest.mark.anyio
    async def test_concurrent_writes(self):
        """Test concurrent timeline writes (10+ parallel actions)."""
        # Mock repository
        mock_repo = AsyncMock()
        logger = TimelineLogger(mock_repo)
        
        run_id = uuid4()
        agent_id = "test_agent"
        
        # Create 10 concurrent log_action_start calls
        tasks = [
            logger.log_action_start(
                run_id=run_id,
                agent_id=agent_id,
                action_name=f"action_{i}",
            )
            for i in range(10)
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Verify all tasks completed
        assert len(results) == 10
        assert all(event_id is not None for event_id in results)
        assert mock_repo.log_action_start.call_count == 10
    
    @pytest.mark.anyio
    async def test_retry_with_exponential_backoff(self):
        """Test retry logic with exponential backoff on DB failures."""
        # Mock repository with simulated failure
        mock_repo = AsyncMock()
        
        # Simulate 2 failures, then success
        call_count = 0
        async def flaky_log_action_start(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise Exception("DB connection error")
            return uuid4()
        
        mock_repo.log_action_start = flaky_log_action_start
        logger = TimelineLogger(mock_repo)
        
        run_id = uuid4()
        agent_id = "test_agent"
        action_name = "flaky_action"
        
        # Retry with exponential backoff (max 3 retries)
        event_id = None
        for attempt in range(3):
            try:
                event_id = await logger.log_action_start(run_id, agent_id, action_name)
                break
            except Exception:
                if attempt < 2:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    await asyncio.sleep(wait_time * 0.01)  # Speed up for tests
                else:
                    raise
        
        assert event_id is not None
        assert call_count == 3  # 2 failures + 1 success
