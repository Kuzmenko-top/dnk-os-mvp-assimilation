---
name: "managed_deepagents_assimilated"
description: "SOTA indices and maps for LangChain Managed Deep Agents assimilation."
version: "1.0.0"
category: "research"
assimilated_at: "2026-08-10"
---

# 🌐 Managed Deep Agents (MDA) Assimilation Index

Meta-index tracking the architecture, contracts, and security of sandboxed runtimes.

## 📁 Assimilated Core Specifications

1. **[Research & Evidence Trail](file:../../docs/reports/rd_assimilation/managed_deepagents/RN-002_managed-deepagents-research.md)**
   - Researched abstractions (Docker Runtime, Sandbox, CLI lifecycle) and verification matrix.
2. **[Sandbox Architecture Specification](file:../../docs/tech/specs/DNK-ARCH-002_agent-sandbox-runtime.md)**
   - Subagent sandbox topologies (Rick, Yuriy, Cas) and Supervisor-to-Sandbox async queue design.
3. **[Component Interfaces & Contracts](file:../../docs/tech/specs/DNK-COMP-002_isolated-fs-contracts.md)**
   - Type-safe Python Pydantic structures, TS-contracts, and error definitions (PathTraversalError).
4. **[Egress and Sandbox Security Standards](file:../../docs/tech/standards/DNK-SEC-002_sandbox-network-egress.md)**
   - `sandbox_runner` topology, Calico network policies, iptables rules, and anonymous Volume Masking.

## 🛠️ Verification Routine

To verify isolated sandbox operational hygiene, execute the compliance suite:
```bash
pytest tests/verification/test_sandbox_hygiene.py
```
