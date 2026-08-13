# --- DNK-MRH-HEADER ---
# mrh_id: "core/utils/timeline_logger.py"
# purpose: "Timeline Logger Engine for agent actions with secret sanitization"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---
"""Timeline Logger for agent actions."""
import json
import re
from typing import Any, Dict, Optional
from uuid import UUID

from ..repositories.timeline_repository import ITimelineRepository


class TimelineLogger:
    """
    Logs agent actions to timeline with sanitization.
    
    Features:
    - log_action_start: Log when action begins
    - log_action_end: Log when action completes (success/failed)
    - Sanitization: Mask passwords, tokens, secrets before writing to payload_json
    """
    
    # Patterns for sanitization
    SECRET_PATTERNS = [
        (r'("password"\s*:\s*")[^"]+"', r'\1***REDACTED***"'),
        (r'("token"\s*:\s*")[^"]+"', r'\1***REDACTED***"'),
        (r'("secret"\s*:\s*")[^"]+"', r'\1***REDACTED***"'),
        (r'("api_key"\s*:\s*")[^"]+"', r'\1***REDACTED***"'),
        (r'(password["\']?\s*[:=]\s*["\']?)[^"\',\s]+', r'\1***REDACTED***'),
        (r'(token["\']?\s*[:=]\s*["\']?)[^"\',\s]+', r'\1***REDACTED***'),
        (r'(secret["\']?\s*[:=]\s*["\']?)[^"\',\s]+', r'\1***REDACTED***'),
        (r'(api_key["\']?\s*[:=]\s*["\']?)[^"\',\s]+', r'\1***REDACTED***'),
    ]
    
    SECRET_KEYS = {"password", "token", "secret", "api_key", "access_token", "auth_token", "private_key"}
    
    def __init__(self, repository: ITimelineRepository):
        self.repo = repository
    
    async def log_action_start(
        self,
        run_id: UUID,
        agent_id: str,
        action_name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """
        Log action start event.
        
        Args:
            run_id: Current agent run ID
            agent_id: Agent identifier
            action_name: Name of action (e.g., "delete_canvas")
            payload: Action payload (will be sanitized)
        
        Returns:
            event_id (UUID) for tracking
        """
        # Sanitize payload
        sanitized_payload = self._sanitize_payload(payload) if payload else None
        
        # Log to repository
        event_id = await self.repo.log_action_start(
            run_id=run_id,
            agent_id=agent_id,
            action_name=action_name,
            payload=sanitized_payload,
        )
        
        return event_id
    
    async def log_action_end(
        self,
        run_id: UUID,
        agent_id: str,
        action_name: str,
        status: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """
        Log action end event.
        
        Args:
            run_id: Current agent run ID
            agent_id: Agent identifier
            action_name: Name of action
            status: "success" or "failed"
            payload: Action result payload (will be sanitized)
        
        Returns:
            event_id (UUID) for tracking
        """
        # Sanitize payload
        sanitized_payload = self._sanitize_payload(payload) if payload else None
        
        # Log to repository
        event_id = await self.repo.log_action_end(
            run_id=run_id,
            agent_id=agent_id,
            action_name=action_name,
            status=status,
            payload=sanitized_payload,
        )
        
        return event_id
    
    def _sanitize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize payload: mask passwords, tokens, secrets.
        
        Args:
            payload: Original payload dictionary
        
        Returns:
            Sanitized payload with secrets masked
        """
        if not payload:
            return payload

        def _sanitize_val(val: Any) -> Any:
            if isinstance(val, dict):
                return {
                    k: ("***REDACTED***" if k.lower() in self.SECRET_KEYS else _sanitize_val(v))
                    for k, v in val.items()
                }
            elif isinstance(val, list):
                return [_sanitize_val(item) for item in val]
            elif isinstance(val, str):
                s = val
                for key in self.SECRET_KEYS:
                    s = re.sub(rf'({key}\s*[:=]\s*)[^\s,;&]+', r'\1***REDACTED***', s, flags=re.IGNORECASE)
                return s
            return val

        sanitized_dict = _sanitize_val(payload)
        
        try:
            payload_json = json.dumps(sanitized_dict)
            for pattern, replacement in self.SECRET_PATTERNS:
                payload_json = re.sub(pattern, replacement, payload_json, flags=re.IGNORECASE)
            return json.loads(payload_json)
        except Exception:
            return sanitized_dict
