# --- DNK-MRH-HEADER ---
# mrh_id: "GERYCH.md"
# purpose: "Mandatory Pre-Task Execution Directive and Branch Control Mandate for Gerych."
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# GERYCH PRE-TASK MANDATE

Перед виконанням КОЖНОЇ нової задачі у репозиторіях DNK OS Герич (herich_librarian) ЗОБОВ'ЯЗАНИЙ прочитати протокол:

`.gerich/protocols/GERYCH_BRANCH_CONTROL_PROTOCOL.md`

і виконати його як обов'язковий pre-task protocol.

## Mandatory Pre-Task Checklist
1. Сформувати **Task Intake Card** (Task ID, Session Owner, Domain, Repository, Base Branch, Proposed Branch).
2. Запитати у користувача рішення щодо гілки (**BRANCH DECISION REQUIRED**): `BRANCH: YES` або `BRANCH: NO`.
3. Не проводити жодних змін файлів, комітів чи пушів до отримання явного підтвердження.
4. Створити та перейти у гілку вигляду `mentor/<domain>/<task-id>-<short-name>`.
5. Після завершення задачі надати фінальний звіт та згенерувати Handoff Report у `docs/handoffs/HANDOFF_<TASK_ID>_<YYYY-MM-DD>.md`.
