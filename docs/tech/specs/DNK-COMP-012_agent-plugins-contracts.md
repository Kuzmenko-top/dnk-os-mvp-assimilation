# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-COMP-012_agent-plugins-contracts"
# purpose: "Type and Data Contracts Specification for DNK OS Agent Plugins 1.0 integration."
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-ASSIM-012"]
# status: "Approved with Conditions"
# version: "1.1.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-COMP-012: Data Contracts & Type Specifications — Agent Plugins 1.0

## 1. Overview & Python Type Definitions

This document defines the strict Python type contracts (`TypedDict`, `Dataclasses`, and `Enums`) required for implementing `DNK-ARCH-012` within `core/plugins/`.

```python
from typing import TypedDict, Literal, Optional, Dict, Any, List
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
    "validation_failed",
    "approval_pending",
    "approved",
    "installed",
    "install_failed",
    "enabled",
    "enable_failed",
    "disabled",
    "quarantined",
    "revoked",
    "removed"
]

VerificationStatus = Literal[
    "unverified",
    "hash_verified",
    "signature_verified",
    "trusted",
    "revoked"
]

class SandboxPolicy(TypedDict):
    required: bool
    runtime: Literal["docker", "process_isolated", "none"]
    network: Literal["none", "host", "restricted"]
    read_only_root: bool

class ProvenanceInfo(TypedDict, total=False):
    source_url: str
    repository: str
    commit: str
    publisher: str

class VerificationInfo(TypedDict, total=False):
    content_hash: str
    signature: str
    signer: str
    verified_at: str
    verification_status: VerificationStatus

class DnkPluginExtension(TypedDict):
    schema_version: str
    risk_level: RiskLevel
    permissions: List[str]
    workspace_scope: WorkspaceScope
    approval_required: bool
    sandbox: SandboxPolicy
    provenance: ProvenanceInfo
    verification: VerificationInfo

class AuthorInfo(TypedDict, total=False):
    name: str
    email: str
    url: str

class DnkPluginManifest(TypedDict, total=False):
    schema: str
    name: str
    version: str
    description: str
    author: AuthorInfo
    homepage: str
    repository: str
    license: str
    keywords: List[str]
    extensions: Dict[str, Any]

@dataclass
class PluginValidationResult:
    valid: bool
    plugin_name: str
    errors: List[str]
    warnings: List[str]
    manifest: Optional[DnkPluginManifest] = None
    extension: Optional[DnkPluginExtension] = None

@dataclass
class PluginAuditEvent:
    event_id: str
    timestamp: str
    event_type: str
    plugin_id: str
    workspace_id: str
    actor_id: str
    details: Dict[str, Any]
```

## 2. Invalid Transition Exception
Any invalid state transition MUST raise `PluginStateTransitionError` with message starting with `409 INVALID_PLUGIN_STATE_TRANSITION`.
