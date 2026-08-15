# --- DNK-MRH-HEADER ---
# mrh_id: "core_plugins_audit_events"
# purpose: "Structured audit logging for plugin provenance and signature verification"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

import time
from uuid import uuid4
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

@dataclass
class PluginAuditEvent:
    event_id: str
    event_type: str
    plugin_id: str
    plugin_version: str
    workspace_id: str
    key_id: Optional[str]
    content_hash: str
    signature_fingerprint: Optional[str]
    actor: str
    timestamp: float
    reason: str
    result: str

class PluginAuditLogger:
    def __init__(self):
        self.events: List[PluginAuditEvent] = []

    def log_event(
        self,
        event_type: str,
        plugin_id: str,
        plugin_version: str,
        workspace_id: str = "ws_default",
        key_id: Optional[str] = None,
        content_hash: str = "",
        signature_fingerprint: Optional[str] = None,
        actor: str = "DNK_SECURITY_GATE",
        reason: str = "",
        result: str = "SUCCESS"
    ) -> PluginAuditEvent:
        ev = PluginAuditEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            plugin_id=plugin_id,
            plugin_version=plugin_version,
            workspace_id=workspace_id,
            key_id=key_id,
            content_hash=content_hash,
            signature_fingerprint=signature_fingerprint,
            actor=actor,
            timestamp=time.time(),
            reason=reason,
            result=result
        )
        self.events.append(ev)
        return ev

    def get_events_for_plugin(self, plugin_id: str) -> List[PluginAuditEvent]:
        return [e for e in self.events if e.plugin_id == plugin_id]
