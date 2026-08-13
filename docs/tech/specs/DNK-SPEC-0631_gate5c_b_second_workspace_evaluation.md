# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-SPEC-0631_gate5c_b_second_workspace_evaluation.md"
# purpose: "Define specifications, multi-tenant safety contracts, and canonical budget policies for Gate 5C-B Second Workspace Evaluation."
# canonical_source: true
# status: "Active"
# version: "1.1.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# license: "MIT"
# --- END DNK-MRH-HEADER ---

# 🛡️ GATE 5C-B: SECOND WORKSPACE EVALUATION CONTRACT

This specification defines the multi-tenant operational contracts, configuration policies, and security isolation requirements for evaluating and enabling a second whitelisted workspace under **Gate 5C-B (DNK OS LLM Gates)**.

## ⚙️ 1. Multi-Tenant Configuration Contract

All workspace identifiers MUST be supplied via environment variables or secret managers. No hardcoded tenant UUIDs are permitted in source code.

```bash
# Activation mode
export LLM_PROVIDER_MODE=validated

# Dual Whitelisted Target UUIDs for Gate 5C-B (Primary & Secondary Pilot Workspaces)
export LLM_WHITELISTED_WORKSPACES="${PRIMARY_WORKSPACE_UUID},${SECONDARY_WORKSPACE_UUID}"

# Active workspace identifier supplied at request runtime
export LLM_CANARY_WORKSPACE_ID="${SECONDARY_WORKSPACE_UUID}"

# Strict budget and rate-limit enforcement switch
export LLM_BUDGET_ENFORCED=true
```

## 💰 2. Canonical Budget Policy

Per-workspace and system-wide budget limits MUST adhere strictly to the project-wide budget enforcement policy:

- **Per-request Limit**: `$0.05`
- **Daily Workspace Limit**: `$1.00`
- **Monthly Project Limit**: `$10.00`
- **Emergency Circuit-Breaker Threshold**: `$50.00`

Exceeding any of these thresholds immediately triggers a fail-closed circuit breaker, halting live provider calls and falling back to deterministic shadow mode.

## 🔒 3. Safety Guards & Run-Time Isolation Constraints

1. **Multi-Tenant Whitelisting Guard**: Execution requests from either `PRIMARY_WORKSPACE_UUID` or `SECONDARY_WORKSPACE_UUID` are granted live validated mode access. Requests from any non-whitelisted workspace ID instantly degrade to safe **shadow mode** with deterministic mock execution.
2. **Cross-Tenant Isolation Firewall**: Data, memory, state mutations, and canvas state trees must remain 100% isolated per tenant. Cross-workspace state leaks trigger an immediate `SecurityException` and terminate execution.
3. **Independent Per-Workspace Budget Isolation**: Each active workspace operates under its own isolated budget quota. Exhaustion of Workspace A's daily quota (`$1.00`) does not affect Workspace B.

## 🧪 4. Evaluation Benchmark Metrics

- **Tenant Routing Correctness**: 100% pass rate for dual whitelisted workspace validation.
- **Fail-Closed Fallback Rate**: 100% fallback to shadow mode for 3rd-party/unwhitelisted workspace requests.
- **Cross-Tenant Mutation Security**: 0 cross-workspace state leakage or unauthorized mutations.
- **Budget Policy Compliance**: All limits strictly aligned with project budget thresholds ($0.05 / $1.00 / $10.00 / $50.00).

---
**Approved by:** Maksym (Lead Developer / CTO)  
**Enforced by:** DNK OS Supervisor & LLM Gateway  
