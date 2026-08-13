# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-ARCH-012_agent-plugins-spec-integration"
# purpose: "Architecture Specification for integrating agentplugins/agent-plugins-spec v1.0.0 into DNK OS."
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-ASSIM-012"]
# status: "Approved with Conditions"
# version: "1.1.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-ARCH-012: Architecture Specification — Agent Plugins 1.0 Integration

## 1. Executive Summary & System Context

DNK OS integrates the open-source **Agent Plugins 1.0** specification (`agentplugins/agent-plugins-spec`) as its primary portable packaging layer for third-party skills and Model Context Protocol (MCP) servers.

While upstream Agent Plugins 1.0 standardizes the filesystem layout (`plugin.json`, `skills/`, `mcp.json`), it deliberately omits runtime sandboxing, permissions, provenance verification, and lifecycle state management. DNK OS provides an **enterprise governance overlay** around the upstream specification, enforcing zero-trust execution, L0-L4 permission policies, Docker-based process sandboxing, multi-tenant workspace isolation, and full audit logging.

---

## 2. Upstream Spec Boundary vs. DNK Extension Boundary

### 2.1 Upstream Portable Core (Strict Conformance)
DNK OS respects the upstream specification without modifying portable core schemas:
- **`plugin.json`**: Closed root manifest parsed using JSON Schema Draft 2020-12. Core fields (`$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`) are portable and unpolluted.
- **`skills/`**: Discovered at fixed location `skills/*/SKILL.md` compliant with `agentskills.io` standard.
- **`mcp.json`**: Discovered at root location `mcp.json`. Evaluates `stdio`, `streamable-http`, and `sse` transports with `${PLUGIN_ROOT}` and `${PLUGIN_DATA}` variable expansion.

### 2.2 Versioned DNK Extension Namespace
Enterprise governance, security, trust verification, and runtime constraints are defined exclusively under `extensions["com.dnk-os.plugin"]` inside `plugin.json`:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "dnk-analytics-plugin",
  "version": "1.0.0",
  "description": "Analytics tool for DNK OS",
  "extensions": {
    "com.dnk-os.plugin": {
      "schema_version": "1.0",
      "risk_level": "L2",
      "permissions": [
        "canvas.read",
        "artifact.create",
        "mcp.stdio.execute"
      ],
      "workspace_scope": "required",
      "approval_required": true,
      "sandbox": {
        "required": true,
        "runtime": "docker",
        "network": "none",
        "read_only_root": true
      },
      "provenance": {
        "source_url": "https://github.com/agentplugins/example-plugin",
        "repository": "agentplugins/example-plugin",
        "commit": "bd383552095128f6effe895b9257cfd580a6d179",
        "publisher": "DNK-e.com Maksym"
      },
      "verification": {
        "content_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "signature": "sig_ed25519_sample",
        "signer": "DNK Trust Authority",
        "verified_at": "2026-08-13T22:00:00Z",
        "verification_status": "trusted"
      }
    }
  }
}
```

---

## 3. Security, Sandboxing & Executable Allowlisting

1. **`mcp.stdio.execute` Default Risk**: Assigned **L2 risk level** by default. Any command allowing arbitrary executables or unvalidated parameters triggers mandatory L3/L4 approval.
2. **Sandbox Execution Guard**: Stdio MCP processes must execute inside a sandboxed container (Docker/process isolation). Execution attempts without an active sandbox are blocked automatically (`403 MCP_EXECUTION_UNSANDBOXED`).
3. **Execution Limits**: Bounded runtime (`max_runtime_seconds: 60`), max output bytes (`max_output_bytes: 1048576`), read-only `PLUGIN_ROOT`, writeable isolated `PLUGIN_DATA`, network `none` by default.

---

## 4. Lifecycle & Quarantine State Machine

Plugins progress through a formal, deterministic state machine:

```text
discovered -> validated -> approval_pending -> approved -> installed -> enabled -> disabled -> revoked -> removed
                                                                               |
                                                                               +-> [quarantined]
```

Additional failure and isolation states: `validation_failed`, `install_failed`, `enable_failed`, `quarantined`.
Invalid state transitions raise `409 INVALID_PLUGIN_STATE_TRANSITION`. Untrusted plugins or runtime policy violations automatically transition the plugin to `quarantined`.
