---
id: flower_canvas_research_links
title: "🌸 Квітка: DNK Canvas Research Integration (Phase 2) [WAITING ON PHASE 1]"
type: task_flower
plant_scale: flower
parent_id: bush_5_atom_canvas_Molecules
status: pending
verification_status: pending
tags:
  - dnk-task-forest
  - dnk-task-flower
  - canvas-research-links
---

# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tasks/05_Flowers/Flower_canvas_research_links.md"
# purpose: "Task Flower for implementing competitor, flower, and evidence linking inside DNK Canvas"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.2.0"
# updated_at: "2026-08-11"
# author: "DNK-e.com Maksym"
# license: "DNK-INTERNAL"
# --- END DNK-MRH-HEADER ---

## 📌 Опис завдання

Реалізувати другу фазу (Phase 2) вбудованого DNK Canvas — бізнес-інтеграцію з конкурентним аналізом та Task Forest.

Забезпечити можливість пов'язувати окремі вузли (nodes через `element_id` з partial index унікальністю) або цілі полотна з профілями конкурентів, завантажувати скріншоти доказів у глобальну бібліотеку активів `canvas_assets` + `canvas_asset_links` з життєвим циклом статусів, та інтегрувати посилання на інсайти, ADR та квітки завдань.

*Увага*: Ця задача перебуває в статусі **WAIT** і фактично розпочнеться після повного успішного завершення та інтеграційного пробігу Phase 1 (Persistence MVP).

---

## ⚡ Чекліст імплементації (Checklist)

- [ ] **1. Модель зв'язків та Сховище Активів (Database & S3)**
  - [ ] Створити Alembic міграцію для таблиць `canvas_links`, `canvas_assets` та `canvas_asset_links`.
  - [ ] Налаштувати глобальну таблицю `canvas_assets` з унікальним `sha256` (глобальна дедуплікація) та життєвим циклом `status` (`pending_upload ➔ uploaded ➔ verifying ➔ verified`).
  - [ ] Реалізувати транзитний мапінг через `canvas_asset_links` для прив'язки глобального активу до конкретного документа та `element_id`.
  - [ ] Створити FastAPI роути для генерації препідписаних посилань `POST /api/v1/canvases/{canvas_id}/assets/presign`:
    - [ ] Якщо `sha256` вже присутній у базі зі статусом `verified`, одразу створювати запис у `canvas_asset_links` та повертати існуючий `asset_id` (без повторного завантаження).
  - [ ] Реалізувати роут `POST /api/v1/canvases/{canvas_id}/assets/{asset_id}/commit` для фіксації завантаженого активу, переходу через стан `verifying` та валідації розмірів і SHA-256 на сервері перед виставленням `verified`.
- [ ] **2. Роути зв'язування сутностей (Entity Linking API)**
  - [ ] Додати роути `POST /api/v1/canvases/{canvas_id}/links` та `DELETE /api/v1/canvases/{canvas_id}/links/{link_id}`.
  - [ ] Реалізувати валідацію `entity_type` (competitor, screenshot, insight, flower, adr, agent_run) та підтримку `element_id`.
  - [ ] Створити два часткових унікальних індекси (partial unique indexes) на базі `element_id` (`IS NOT NULL` та `IS NULL`) для правильної обробки унікальності лінків у PostgreSQL.
  - [ ] Захистити видалення лінків від імені агентів: інтегрувати **Supervisor Approval Gate** для `DELETE /links/{link_id}`, повертати `202 Accepted` у разі очікування підтвердження.
- [ ] **3. Інтерфейс інтеграції (Frontend Link Panel & Sidebar)**
  - [ ] Додати бічну панель (Sidebar) у Next.js для відображення існуючих зв'язків Canvas.
  - [ ] Створити модальне вікно або меню швидкого додавання зв'язків для виділеного елементу (`element_id`) на Excalidraw.
  - [ ] Реалізувати візуальне завантаження файлів зображень (Drag-and-Drop скріншотів):
    - [ ] Отримати pre-signed URL з бекенду або дублікат-інформацію.
    - [ ] Завантажити файл безпосередньо в S3/MinIO, якщо це унікальний файл.
    - [ ] Додати зображення на Excalidraw-сцену, використовуючи посилання на серверну копію (без вбудовування base64).
- [ ] **4. Тестування та Верифікація**
  - [ ] Написати тести на дедуплікацію скріншотів (спроба завантажити однаковий хеш у різні документи).
  - [ ] Перевірити безпеку завантаження файлів (блокування небезпечних MIME-типів на бекенді).

---

## 🔗 Залежності та Зв'язки
- **Батьківський кущ**: `bush_5_atom_canvas_Molecules`
- **Попередні завдання**: `flower_canvas_persistence` (Phase 1)
- **Виконавці**:
  - `dnk-dev-01` (glm-5.2) — Frontend Drag-and-Drop, Sidebar сутностей, Element ID linking UI.
  - `dnk_koder` (codestral-22b) — FastAPI S3 integration with statuses, Link API with element_id, Supervisor Approval Gate.

---

## 🏁 Definition of Done (Критерії завершення)
- [ ] Будь-який скріншот завантажується безпосередньо в S3/MinIO за препідписаним URL і рендериться на Canvas.
- [ ] Розмір JSON-документа сцени при завантаженні зображень не зростає на розмір файлу (base64 відсутній).
- [ ] Елементи з конкретними `element_id` успішно лінкуються з сутностями, зв'язки відображаються у бічній панелі.
- [ ] Спроба завантажити однаковий файл повторно використовує існуючий `storage_key` завдяки SHA-256 перевірці.
- [ ] Всі файли відповідають стандартам MRH та мають ліцензію "DNK-INTERNAL".
