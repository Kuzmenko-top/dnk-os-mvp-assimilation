# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-SEC-015-runtime-hardening-report"
# purpose: "Security report for DNK-SEC-015 Sandbox Runtime Hardening Verification"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-15"
# --- END DNK-MRH-HEADER ---

# Security Report: DNK-SEC-015 Sandbox Runtime Hardening Verification

## 1. LINUX_CGROUPS_V2 & Runtime Inspection
- **NanoCpus Limit:** `500000000` (0.50 CPU quota)
- **Memory Limit:** `134217728` bytes (128 MB RAM ceiling)
- **PID Limit:** `32` maximum tasks
- **cgroups Driver:** `cgroups v2` unified hierarchy

## 2. DOCKER_DESKTOP_MACOS Behavior
- Memory and CPU limits mapped cleanly via Docker Desktop Hypervisor.
- macOS ARM64 translation validated for `python:3.12-slim` container base.

## 3. SECCOMP Profile
- Explicit custom seccomp profile deployed: `docker/seccomp_profile.json`
- Default action: `SCMP_ACT_ERRNO`
- Blocked dangerous syscalls: `ptrace`, `sys_module`, `kexec_load`, `process_vm_writev`

## 4. NON_ROOT Execution
- Effective Container User: `user: "10001:10001"` (`sandboxuser`)
- Root privileges completely revoked within container namespace.

## 5. NO_NEW_PRIVILEGES
- `security_opt: ["no-new-privileges:true"]` enforced.
- Setuid / setgid privilege escalation attempts blocked at kernel level.

## 6. OOM & RESTART Policy
- OOM kill behavior: Kernel OOM-killer terminates process when exceeding 128M RAM.
- Container restart policy: `restart: "no"` (prevents infinite restart loops).

## 7. QUARANTINE & AUDIT Trail
- Repeated violations trigger `PluginManager.quarantine_plugin()`.
- Audit events logged to `SecurityGateTimelineAdapter` and `PluginManager.quarantined_plugins`.

## 8. RESIDUAL_RISKS
- Production cgroups v2 kernel tuning on bare-metal Linux nodes pending final staging deployment.
