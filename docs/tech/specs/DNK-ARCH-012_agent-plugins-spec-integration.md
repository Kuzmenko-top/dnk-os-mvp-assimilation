# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-ARCH-012_agent-plugins-spec-integration"
# purpose: "Architecture Specification for integrating agentplugins/agent-plugins-spec v1.0.0 into DNK OS."
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-ASSIM-012"]
# status: "Draft - Pending Mentor Audit"
# version: "1.0.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-ARCH-012: Architecture Specification — Agent Plugins 1.0 Integration

## 1. Executive Summary & System Context

DNK OS integrates the open-source **Agent Plugins 1.0** specification (`agentplugins/agent-plugins-spec`) as its primary portable packaging layer for third-party skills and Model Context Protocol (MCP) servers.

While upstream Agent Plugins 1.0 standardizes the filesystem layout (`plugin.json`, `skills/`, `mcp.json`), it deliberately omits runtime sandboxing, permissions, provenance verification, and lifecycle state management. DNK OS provides an **enterprise governance overlay** around the upstream specification, enforcing zero-trust execution, L0-L4 permission policies, Docker-based process sandboxing, multi-tenant workspace isolation, and full audit logging.

```text
+-----------------------------------------------------------------------------------+
|                                  DNK OS RUNTIME                                  |
|                                                                                   |
|  +------------------------+      +---------------------+      +----------------+  |
|  | PluginLifecycleEngine  | ---> | PolicyGate (L0-L4)  | ---> | Supervisor     |  |
|  +------------------------+      +---------------------+      +----------------+  |
|               |                             |                          |          |
|               v                             v                          v          |
|  +-----------------------------------------------------------------------------+  |
|  |                         DNK Plugin Adapter Layer                           |  |
|  +-----------------------------------------------------------------------------+  |
|                                       |                                           |
|                                       v                                           |
|  +-----------------------------------------------------------------------------+  |
|  |                 Upstream Agent Plugins 1.0 Package Layout                   |  |
|  |  [plugin.json]        [skills/*/SKILL.md]        [mcp.json]                     |  |
|  |  - name / version     - Agent Skills Spec        - stdio / http / sse           |  |
|  |  - extensions         - scripts & references     - env expansion                |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Upstream Spec Boundary vs. DNK Extension Boundary

### 2.1 Upstream Portable Core (Strict Conformance)
DNK OS respects the upstream specification without modifying portable core schemas:
- **`plugin.json`**: Closed root manifest parsed using JSON Schema Draft 2020-12. Core fields (`$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`) are portable and unpolluted.
- **`skills/`**: Discovered at fixed location `skills/*/SKILL.md` compliant with `agentskills.io` standard.
- **`mcp.json`**: Discovered at root location `mcp.json`. Evaluates `stdio`, `streamable-http`, and `sse` transports with `${PLUGIN_ROOT}` and `${PLUGIN_DATA}` variable expansion.

### 2.2 Versioned DNK Extension Namespace
Enterprise governance, security, and runtime constraints are defined exclusively under `extensions["com.dnk-os.plugin"]` inside `plugin.json`:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "dnk-analytics-plugin",
  "version": "1.0.0",
  "description": "Analytics tool for DNK OS",
  "extensions": {
    "com.dnk-os.plugin": {
      "schema_version": "1.0",
      "risk_level": "L1",
      "permissions": [
        "canvas.read",
        "artifact.create",
        "mcp.stdio.execute"
      ],
      "workspace_scope": "required",
      "approval_required": false,
      "sandbox": {
        "required": true,
        "runtime": "docker",
        "network": "none",
        "read_only_root": true
      },
      "trust": {
        "source": "github",
        "commit": "bd383552095128f6effe895b9257cfd580a6d179",
        "publisher": "DNK-e.com Maksym"
      }
    }
  }
}
```

---

## 3. Plugin Discovery & Validation Architecture

### 3.1 Discovery Pipeline
1. **Directory Inspection**: Target directory must contain `plugin.json` at root.
2. **Path Safety Boundary**: All package file targets MUST resolve strictly within `PLUGIN_ROOT`. Symlink escapes or relative path traversal (`../`) trigger immediate rejection (`400 PATH_TRAVERSAL_DETECTED`).
3. **Manifest Schema Validation**: Validates `plugin.json` against `plugin.schema.json`. Unknown top-level fields trigger non-fatal warnings; schema invalidity triggers fatal rejection.
4. **Extension Extraction**: Parses `extensions["com.dnk-os.plugin"]`. If missing, default fallback values (Risk Level L1, Sandbox Required, Approval Pending) are automatically injected by DNK Plugin Manager.
5. **Component Discovery**:
   - `skills/`: Scans immediate child directories for `SKILL.md`.
   - `mcp.json`: Scans and validates against `mcp.schema.json`.

---

## 4. Execution, Security & Sandboxing Architecture

### 4.1 Subprocess & Docker Sandboxing
For stdio MCP servers, direct host execution is **strictly prohibited**. Execution takes place inside an isolated Docker runner or process sandbox:
- **`PLUGIN_ROOT`**: Mounted read-only (`ro`) inside the container/sandbox.
- **`PLUGIN_DATA`**: Mounted read-write (`rw`) inside persistent, tenant-isolated storage (`/var/dnk/plugins/data/<plugin_id>`).
- **Network Isolation**: Default network policy is `none` (no external internet egress). Egress to specific endpoints requires explicit `L2/L3` permission approval.
- **FileSystem Isolation**: Container root filesystem is mounted read-only (`read_only_root: true`). Temporary execution directories use ephemeral `tmpfs`.

### 4.2 L0-L4 Permission Resolution
DNK OS PolicyGate evaluates every plugin tool call before dispatching to the underlying MCP server or Skill runner:
- **L0 (Pure Deterministic)**: Internal string transforms, formatting. Auto-approved.
- **L1 (Read-Only Workspace)**: Reading canvas, reading files inside workspace. Auto-approved if workspace-scoped.
- **L2 (Controlled Write / API Egress)**: Writing workspace artifacts, sending webhooks. Requires workspace admin policy.
- **L3 (System Modification / Host Access)**: Invoking stdio sub-processes, external API integration. Requires explicit user approval (`approval_pending`).
- **L4 (Critical Administrative)**: Executing shell binaries, modifying system configs. Requires MFA / Owner approval.

---

## 5. Plugin Lifecycle & Governance State Machine

Plugins progress through a formal, deterministic state machine enforced by `PluginLifecycleEngine`:

```text
  [discovered] ---> [validated] ---> [approval_pending] ---> [approved]
       |                 |                   |                   |
       v                 v                   v                   v
   (rejected)        (rejected)          (rejected)         [installed]
                                                                 |
                                                                 v
                                                             [enabled]
                                                            /        \
                                                           v          v
                                                      [disabled]  [revoked]
                                                           |          |
                                                           +----+-----+
                                                                |
                                                                v
                                                            [removed]
```

---

## 6. Audit, Monitoring & System Integration

### 6.1 Supervisor & PolicyGate Integration
- **Supervisor**: Monitors plugin subprocess health, memory usage, CPU limits, and zombie process cleanup.
- **PolicyGate**: Intercepts every tool invocation (`plugin.tool.called`), validates active token permissions against `PermissionSet`, and emits `plugin.tool.blocked` on violation.
- **Structured Audit Logging**: Every state transition and tool invocation emits a structured JSON audit log entry with correlation IDs, timestamp, actor ID, workspace ID, and exact parameters.

### 6.2 Existing Plugin Migration Path (Slack & Notion)
Existing native DNK plugins (`plugins/slack_plugin`, `plugins/notion_plugin`) will be wrapped in the Agent Plugins 1.0 format:
1. Generate root `plugin.json` with `com.dnk-os.plugin` extensions.
2. Expose tools via `mcp.json` (stdio or FastMCP wrapper).
3. Move documentation and procedural prompts into `skills/` directory.
