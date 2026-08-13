# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-COMP-012_agent-plugins-contracts"
# purpose: "Type and Data Contracts Specification for DNK OS Agent Plugins 1.0 integration."
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-ASSIM-012"]
# status: "Draft - Pending Mentor Audit"
# version: "1.0.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-COMP-012: Data Contracts & Type Specifications — Agent Plugins 1.0

## 1. Overview & Python Type Definitions

This document defines the strict Python type contracts (`TypedDict`, `Dataclasses`, and `Enums`) required for implementing `DNK-ARCH-012` within `core/plugins/`. All implementations MUST strictly adhere to these signatures.

---

## 2. Core Plugin Data Contracts

```python
from typing import TypedDict, Literal, Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Risk Levels
RiskLevel = Literal["L0", "L1", "L2", "L3", "L4"]

# Workspace Scopes
WorkspaceScope = Literal["required", "optional", "global"]

# Transport Variants for MCP
McpTransportType = Literal["stdio", "streamable-http", "sse"]

# Plugin States
PluginState = Literal[
    "discovered",
    "validated",
    "approval_pending",
    "approved",
    "installed",
    "enabled",
    "disabled",
    "revoked",
    "removed"
]

class SandboxPolicy(TypedDict):
    required: bool
    runtime: Literal["docker", "process_isolated", "none"]
    network: Literal["none", "host", "restricted"]
    read_only_root: bool

class TrustPolicy(TypedDict):
    source: str
    commit: Optional[str]
    publisher: Optional[str]
    verified: bool

class DnkPluginExtension(TypedDict):
    schema_version: str
    risk_level: RiskLevel
    permissions: List[str]
    workspace_scope: WorkspaceScope
    approval_required: bool
    sandbox: SandboxPolicy
    trust: TrustPolicy

class AuthorInfo(TypedDict, total=False):
    name: str
    email: str
    url: str

class DnkPluginManifest(TypedDict, total=False):
    schema: str  # maps to $schema
    name: str
    version: str
    description: str
    author: AuthorInfo
    homepage: str
    repository: str
    license: str
    keywords: List[str]
    extensions: Dict[str, Any]

class SkillDescriptor(TypedDict):
    name: str
    description: str
    path: str
    mrh_id: Optional[str]
    user_invocable: bool

class McpServerDescriptor(TypedDict):
    server_id: str
    transport: McpTransportType
    command: Optional[str]
    args: Optional[List[str]]
    env: Optional[Dict[str, str]]
    cwd: Optional[str]
    url: Optional[str]
    headers: Optional[Dict[str, str]]

@dataclass
class PluginValidationResult:
    valid: bool
    plugin_name: str
    errors: List[str]
    warnings: List[str]
    manifest: Optional[DnkPluginManifest]
    extension: Optional[DnkPluginExtension]

@dataclass
class PluginInstallRequest:
    plugin_id: str
    source_path: str
    workspace_id: str
    actor_id: str
    requested_at: datetime

@dataclass
class PluginApprovalRequest:
    plugin_id: str
    risk_level: RiskLevel
    requested_permissions: List[str]
    workspace_id: str
    approver_id: Optional[str]
    status: Literal["pending", "approved", "rejected"]

@dataclass
class PluginAuditEvent:
    event_id: str
    timestamp: datetime
    event_type: str
    plugin_id: str
    workspace_id: str
    actor_id: str
    details: Dict[str, Any]
```

---

## 3. State Machine & Transition Rules

### 3.1 Valid State Transitions
```text
discovered        -> [validated]
validated         -> [approval_pending, installed, rejected]
approval_pending  -> [approved, rejected]
approved          -> [installed]
installed         -> [enabled, disabled, revoked]
enabled           -> [disabled, revoked]
disabled          -> [enabled, revoked, removed]
revoked           -> [removed]
```

### 3.2 Error Handling for Invalid Transitions
Any attempted transition not explicitly listed in Section 3.1 MUST be rejected with error:
`409 INVALID_PLUGIN_STATE_TRANSITION`

---

## 4. Required Audit Events

Every plugin operation MUST emit one of the following audit event types:

1. `plugin.discovered`
2. `plugin.validation.started`
3. `plugin.validation.passed`
4. `plugin.validation.failed`
5. `plugin.approval.requested`
6. `plugin.approved`
7. `plugin.installed`
8. `plugin.enabled`
9. `plugin.disabled`
10. `plugin.revoked`
11. `plugin.tool.called`
12. `plugin.tool.blocked`
13. `plugin.uninstalled`
