# --- DNK-MRH-HEADER ---
# mrh_id: "tests/test_skill_registry_timeline.py"
# purpose: "Integration tests for SkillRegistry with TimelineLogger"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---
"""Integration tests for SkillRegistry with TimelineLogger."""
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from skills.registry import SkillRegistry


class TestSkillRegistryTimelineIntegration:
    """Test SkillRegistry execution with TimelineLogger."""
    
    @pytest.mark.anyio
    async def test_execute_skill_logs_timeline(self):
        """Test that executing a skill triggers timeline log_action_start and log_action_end."""
        mock_logger = AsyncMock()
        registry = SkillRegistry()
        
        run_id = uuid4()
        params = {"prompt": "Build a landing page", "api_key": "sk-secret123"}
        
        # Execute skill dnk.ui.generate_workspace
        result = await registry.execute_skill(
            skill_id="dnk.ui.generate_workspace",
            params=params,
            run_id=run_id,
            timeline_logger=mock_logger,
        )
        
        assert result is not None
        assert mock_logger.log_action_start.called
        assert mock_logger.log_action_end.called
        
        # Verify log_action_start arguments
        start_call = mock_logger.log_action_start.call_args
        assert start_call.kwargs["run_id"] == run_id
        assert start_call.kwargs["agent_id"] == "skill_registry"
        assert start_call.kwargs["action_name"] == "execute_skill:dnk.ui.generate_workspace"
