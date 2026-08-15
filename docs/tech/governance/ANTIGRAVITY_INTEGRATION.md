# author: "DNK-e.com Maksym"
# Antigravity Governance Integration

## Overview
Architecture Governance System is now integrated with Antigravity (Supervisor).

## How It Works

### 1. Task Assignment
When Antigravity assigns a task:
```bash
python scripts/antigravity_governance_hook.py on_task_assigned <task-id> "<description>" "<files-json>"
```
- Automatically detects if task requires ADR
- Automatically detects if task requires compatibility matrix update
- Automatically detects if task requires regression tests
- Adds governance tasks to DoD

### 2. Pre-Merge Gate
Before merging:
```bash
python scripts/antigravity_governance_hook.py on_pre_merge <task-id>
```
- Checks health score >= 75
- Validates all ADRs
- Runs regression tests
- Blocks merge if any gate fails

### 3. Pre-Export Gate
Before exporting:
```bash
python scripts/antigravity_governance_hook.py on_pre_export <task-id>
```
- Checks health score >= 60
- Validates all ADRs
- Runs regression tests
- Blocks export if any gate fails

## Governance Gates

| Gate | Threshold | When |
|------|-----------|------|
| Health Score | >= 75 (merge), >= 60 (export) | Pre-merge, Pre-export |
| ADR Validation | 0 errors | Pre-merge, Pre-export |
| Regression Tests | 100% pass | Pre-merge, Pre-export |

## Example Workflow

```
1. Antigravity assigns DNK-ASSIM-018
   → on_task_assigned hook runs
   → Adds "Create ADR" to DoD

2. Gerych completes task
   → Creates ADR
   → Updates compatibility matrix
   → Adds regression tests

3. Antigravity prepares to merge
   → on_pre_merge hook runs
   → Health score = 100/100 ✅
   → ADR validation = 0 errors ✅
   → Regression tests = 4/4 PASS ✅
   → Merge allowed ✅

4. Antigravity prepares to export
   → on_pre_export hook runs
   → All gates pass ✅
   → Export allowed ✅
```
