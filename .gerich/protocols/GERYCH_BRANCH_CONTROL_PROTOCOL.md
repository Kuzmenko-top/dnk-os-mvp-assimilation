# --- DNK-MRH-HEADER ---
# mrh_id: "GERYCH_BRANCH_CONTROL_PROTOCOL.md"
# purpose: "Canonical Pre-Task Branch Control Protocol for Gerych in DNK OS repositories."
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# GERYCH BRANCH CONTROL PROTOCOL

## Purpose

Цей протокол є обов'язковою інструкцією для створення та виконання кожної задачі Герича в репозиторіях DNK OS.

Мета протоколу:

- не змішувати задачі різних сесій;
- прив'язувати кожну реалізацію до owner/domain/task ID;
- створювати окрему Git-гілку для повноцінного аудиту та рев'ю ментором;
- не допускати прямого push у `main`;
- забезпечити відтворюваний handoff після завершення задачі.

## Mandatory rule

Перед початком будь-якої задачі Герич ЗОБОВ'ЯЗАНИЙ зупинитися і поставити branch decision question.

Не можна:

- починати змінювати файли до branch decision;
- створювати branch з довільною назвою;
- працювати напряму в `main`;
- пушити зміни без підтвердження branch policy;
- змішувати кілька domain/session у межах одного task branch;
- вважати задачу завершеною без commit SHA, branch name і handoff report.

## Step 0 — Task intake

Після отримання нової задачі спочатку сформувати Task Intake Card:

```yaml
task_id: "DNK-<DOMAIN>-<NUMBER>"
title: "<short task title>"
session_owner: "<DNK_MENTOR_CANVAS|DNK_MENTOR_LLM_GATE|DNK_MENTOR_CORE|DNK_MENTOR_PRODUCT|DNK_MENTOR_RND|DNK_MENTOR_KNOWLEDGE>"
domain: "<canvas|llm|core|product|rnd|knowledge>"
repository: "Kuzmenko-top/dnk-os-mvp-assimilation"
base_branch: "main"
requested_by: "<user or mentor>"
implementation_required: true
mentor_audit_required: true
```

Якщо відсутній `task_id`, `session_owner`, `domain` або repository — не починати реалізацію. Поставити уточнювальне питання.

## Step 1 — Mandatory branch question

Показати користувачу саме це питання:

> Для задачі `<TASK_ID>: <TITLE>` визначено owner `<SESSION_OWNER>` і domain `<DOMAIN>`. Чи створюємо окрему гілку для реалізації, перевірки та аудиту ментором?
>
> Рекомендація: **так**. Гілка буде створена від `main` за схемою:
>
> `mentor/<domain>/<task-id>-<short-name>`
>
> Наприклад:
>
> `mentor/canvas/DNK-TEST-001-playwright-glibc-runner`
>
> Підтвердіть: `BRANCH: YES` або `BRANCH: NO`.

Не трактувати мовчання, нечітку відповідь або фразу “роби” як дозвіл на branch creation. Потрібно отримати явне `BRANCH: YES` або `BRANCH: NO`.

## Default decision policy

| Task type | Default | Rule |
|---|---|---|
| Production code | YES | Branch mandatory |
| Database/schema/migration | YES | Branch mandatory |
| Security/auth/RBAC | YES | Branch mandatory |
| API/contract change | YES | Branch mandatory |
| LLM/provider/tool change | YES | Branch mandatory |
| Canvas/UI behavior | YES | Branch mandatory |
| Test infrastructure | YES | Branch mandatory |
| Bug fix | YES | Branch mandatory |
| Documentation-only | CONDITIONAL | Ask user |
| Read-only research | NO branch by default | Use research artifact/handoff |
| Emergency hotfix | YES | Use `hotfix/<domain>/<task-id>-<short-name>` and request immediate review |

For all `YES` cases, still ask the explicit branch question and record the response.

## Step 2 — Branch name

Canonical branch format:

```text
mentor/<domain>/<task-id>-<short-name>
```

Examples:

```text
mentor/canvas/DNK-TEST-001-playwright-glibc-runner
mentor/llm/DNK-LLM-002-shadow-ui-e2e
mentor/llm/DNK-LLM-003-materialization-compiler
mentor/core/DNK-CORE-001-integration-audit
mentor/product/DNK-PRODUCT-001-workspace-mvp
mentor/rnd/DNK-RND-001-open-design-audit
mentor/knowledge/DNK-KNOWLEDGE-006-rag-foundation
```

Rules:

- lowercase domain and short name;
- task ID remains uppercase exactly as registered;
- words separated by hyphens;
- no spaces or Cyrillic characters;
- no `feature/test`, `fix/latest`, `gerich-work`, `temp`, `experiment`;
- one branch equals one task and one owner;
- never reuse a completed branch for a new task.

## Step 3 — Mentor approval record

Before branch creation, print:

```yaml
branch_decision:
  task_id: "<TASK_ID>"
  session_owner: "<SESSION_OWNER>"
  domain: "<DOMAIN>"
  repository: "Kuzmenko-top/dnk-os-mvp-assimilation"
  base_branch: "main"
  proposed_branch: "mentor/<domain>/<task-id>-<short-name>"
  mentor_audit_required: true
  user_decision: "PENDING"
```

After explicit approval:

```yaml
user_decision: "BRANCH: YES"
```

Only then create/switch to the branch.

If `BRANCH: NO`:

- do not create a branch;
- do not push code;
- work only if the task is explicitly approved as read-only/local-only;
- mark final status `LOCAL_ONLY_NOT_PUSHED`;
- request a new branch before any production implementation.

## Step 4 — Repository preparation

For `BRANCH: YES` execute:

```bash
git fetch origin main
git switch main
git pull --ff-only origin main
git switch -c mentor/<domain>/<task-id>-<short-name>
git branch --show-current
git status --short
git log -1 --oneline
```

Expected:

```text
- current branch equals proposed branch;
- working tree is clean before implementation;
- branch starts from current origin/main.
```

If branch already exists:

```bash
git fetch origin
git switch mentor/<domain>/<task-id>-<short-name>
git pull --ff-only origin mentor/<domain>/<task-id>-<short-name>
```

Do not silently create a second branch name.

## Step 5 — Scope control

Before implementation define allowed and forbidden paths:

```yaml
scope:
  allowed_paths: []
  forbidden_paths: []
  no_mixed_domain_changes: true
```

Examples:

```yaml
canvas:
  allowed_paths:
    - visual_shell/
    - services/dnk_canvas_api/canvas/
    - e2e/canvas/
    - docs/specs/DNK_CANVAS_*.md
  forbidden_paths:
    - core/providers/
    - services/llm_gateway/
    - RAG/
```

```yaml
llm:
  allowed_paths:
    - core/providers/
    - core/llm/
    - services/llm_gateway/
    - tests/verification/test_llm_*.py
    - docs/gates/GATE_5*.md
  forbidden_paths:
    - canvas persistence schema
    - core/swarm_engine.py
    - product workspace UI
```

If implementation requires a forbidden path:

1. stop;
2. report a cross-domain dependency;
3. do not modify the file;
4. request a separate task or mentor decision.

## Step 6 — Commit and push

Before commit:

```bash
git status --short
git diff --stat
git diff --name-only
git diff --check
```

Commit format:

```text
<type>(<domain>): <short task description>
```

Examples:

```text
test(canvas): add glibc Playwright E2E runner
feat(llm): add Gemini shadow provider gateway
fix(core): stabilize supervisor retry transition
docs(rnd): audit Open Design skill architecture
```

One task should normally produce one scoped commit. If multiple commits are required, all must remain in the same task branch.

Push only after tests:

```bash
git push -u origin mentor/<domain>/<task-id>-<short-name>
```

Never:

```bash
git push origin main
git push --force
git reset --hard origin/main
```

## Step 7 — Final report

The final report MUST begin with:

```text
REPOSITORY: Kuzmenko-top/dnk-os-mvp-assimilation
BASE BRANCH: main
WORKING BRANCH: <actual branch>
SESSION OWNER: <owner>
DOMAIN: <domain>
TASK ID: <task id>
BRANCH DECISION: BRANCH: YES/NO
COMMIT SHA: <sha>
PUSHED TO: origin/<branch>
```

Then include:

```text
1. Changed files
2. Intentionally unchanged files
3. Tests executed
4. Test results
5. Docker/runtime verification
6. Security checks
7. Known limitations
8. Remaining work
9. Handoff path
10. PR URL, if created
```

Statuses must be separated:

```text
IMPLEMENTED_LOCAL
TESTED_LOCAL
PUSHED_GITHUB
RUNTIME_VERIFIED
PR_READY
MERGED
```

Never report only `DONE`.

## Step 8 — Handoff

Create:

```text
docs/handoffs/HANDOFF_<TASK_ID>_<YYYY-MM-DD>.md
```

Minimum YAML:

```yaml
source_session: "<owner>"
target_session: "<next owner>"
task_id: "<TASK_ID>"
repository: "Kuzmenko-top/dnk-os-mvp-assimilation"
base_branch: "main"
branch: "<actual branch>"
commit_sha: "<sha>"
pr_url: "<url or null>"
status: "<status>"
completed: []
pending: []
known_risks: []
required_verification: []
```

## Mandatory response template for every new task

Before doing any work, respond:

```text
TASK INTAKE
Task ID: <...>
Title: <...>
Owner/session: <...>
Domain: <...>
Repository: Kuzmenko-top/dnk-os-mvp-assimilation
Base branch: main

BRANCH DECISION REQUIRED
For this implementation task I recommend a dedicated branch:
mentor/<domain>/<task-id>-<short-name>

Create the branch for implementation and mentor audit?
Reply exactly:
BRANCH: YES
or
BRANCH: NO

No files will be modified before the decision is recorded.
```

## Final enforcement rule

If the user has not explicitly answered `BRANCH: YES` or `BRANCH: NO`, Герич must not:

- create or switch to a task branch;
- modify production files;
- commit;
- push;
- claim implementation started.

For production implementation, the default recommendation is always:

```text
BRANCH: YES
```

The branch name, commit SHA, changed files and handoff report are mandatory evidence for mentor review.
