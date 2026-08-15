# author: "DNK-e.com Maksym"
# ADR-002: Open-SWE Task Dispatcher

## Status
Accepted

## Context
Autonomous subagents require sandboxed filesystem and process isolation.

## Decision
Implement Open-SWE dispatcher with containerized Docker sandboxing.

## Alternatives Considered
1. Bare-metal subprocess execution (security risk)
2. Chroot jail (insufficient isolation)

## Consequences
### Positive
- ✅ Strict process and filesystem containment
- ✅ Reproducible agent test suites

### Negative
- ❌ Overhead of container initialization (~200ms)

## Dependencies
- Docker Engine
- python-docker

## Date
2026-08-15

## Owner
DNK OS Governance Team
