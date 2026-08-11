---
id: flower_canvas_persistence
title: "🌸 Квітка: DNK Canvas Persistence (Phase 1)"
type: task_flower
plant_scale: flower
parent_id: bush_5_atom_canvas_Molecules
status: pending
verification_status: pending
tags:
  - dnk-task-forest
  - dnk-task-flower
  - canvas-persistence
---

# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tasks/05_Flowers/Flower_canvas_persistence.md"
# purpose: "Task Flower for implementing PostgreSQL and S3 persistence for DNK Canvas"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-11"
# author: "DNK-e.com Maksym"
# license: "MIT"
# --- END DNK-MRH-HEADER ---

## 📌 Опис завдання

Реалізувати першу фазу (Phase 1) вбудованого DNK Canvas — ядро системи персистентності на бекенді (FastAPI + PostgreSQL) та інтеграцію редактора на фронтенді (Next.js 14 + Excalidraw).

Забезпечити надійне збереження сцени, версіонування змін, запобігання перетиранию даних (Optimistic Concurrency Control) та автоматичне збереження.

---

## ⚡ Чекліст імплементації (Checklist)

- [ ] **1. База даних та Міграції (PostgreSQL & Alembic)**
  - [ ] Створити Alembic міграцію для схеми `hub_memory` та таблиць `canvas_documents` і `canvas_revisions`.
  - [ ] Налаштувати унікальний індекс на `(document_id, revision_number)`.
  - [ ] Додати серверну валідацію SHA-256 чексуми для вхідних JSON-сцен.
- [ ] **2. Core API (FastAPI)**
  - [ ] Створити Pydantic схеми для вхідних та вихідних payload-ів.
  - [ ] Створити роут `POST /api/v1/canvases` для ініціалізації документа.
  - [ ] Створити роут `GET /api/v1/canvases/{canvas_id}` для отримання поточної сцени.
  - [ ] Реалізувати роут `PUT /api/v1/canvases/{canvas_id}/scene` з логікою Optimistic Concurrency Control:
    - [ ] Отримати заголовок або поле `expected_revision`.
    - [ ] Перевірити, чи поточна `revision_number` в базі відповідає очікуваній.
    - [ ] Якщо ні ➔ повернути `409 Conflict`.
    - [ ] Якщо так ➔ записати новий рядок у `canvas_revisions` та оновити `canvas_documents`.
- [ ] **3. Frontend MVP (Next.js + Excalidraw)**
  - [ ] Налаштувати динамічний імпорт (`ssr: false`) для `@excalidraw/excalidraw` у роуті `/workspace/[workspace_id]/canvas/[canvas_id]`.
  - [ ] Додати індикатор збереження (Save / Last Saved).
  - [ ] Налаштувати дебаунс автозбереження (3 секунди) з відстеженням брудного стану (dirty state).
  - [ ] Реалізувати гарячу клавішу `cmd+s` / `ctrl+s` для негайного примусового збереження.
  - [ ] Додати обробку конфлікту злиття (`409 Conflict`): показати вікно діалогу з можливістю завантажити серверний стан або перезаписати його.
- [ ] **4. Експорт та Імпорт**
  - [ ] Інтегрувати серіалізаційне API Excalidraw на клієнті для експорту в `.excalidraw`, PNG та SVG.
- [ ] **5. Тестування (Unit & Integration)**
  - [ ] Написати юніт-тести для `PUT /scene` на перевірку 409 Conflict.
  - [ ] Написати інтеграційний тест для Alembic міграції.

---

## 🔗 Залежності та Зв'язки
- **Батьківський кущ**: `bush_5_atom_canvas_Molecules`
- **Виконавці**:
  - `dnk-dev-01` (glm-5.2) — Frontend UI, React інтеграція, Autosave.
  - `dnk_koder` (codestral-22b) — FastAPI роути, Alembic міграція, тестування.
  - `dnk_governance_companion` (gemma-4-31b) — Перевірка відповідності MRH, ліцензійний аудит.

---

## 🏁 Definition of Done (Критерії завершення)
- [ ] Таблиці документів та ревізій успішно мігровані через Alembic в PostgreSQL.
- [ ] Сцена відновлюється з бази після повного перезавантаження сторінки або очищення кешу браузера.
- [ ] Спроба одночасного збереження двома клієнтами з однаковим `expected_revision` призводить до помилки `409 Conflict` для другого клієнта.
- [ ] Кожна зміна сцени створює новий запис у `canvas_revisions` зі збільшеним `revision_number` та валідною чексумою.
- [ ] Всі файли мають заголовок MRH з авторством та ліцензією.
- [ ] Написані тести проходять успішно.
