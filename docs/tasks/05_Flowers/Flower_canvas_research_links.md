---
id: flower_canvas_research_links
title: "🌸 Квітка: DNK Canvas Research Integration (Phase 2)"
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
# version: "1.0.0"
# updated_at: "2026-08-11"
# author: "DNK-e.com Maksym"
# license: "MIT"
# --- END DNK-MRH-HEADER ---

## 📌 Опис завдання

Реалізувати другу фазу (Phase 2) вбудованого DNK Canvas — бізнес-інтеграцію з конкурентним аналізом та Task Forest.

Забезпечити можливість пов'язувати окремі вузли (nodes) або цілі полотна з профілями конкурентів, завантажувати скріншоти доказів у хмару S3/MinIO та інтегрувати посилання на інсайти, ADR та квітки завдань.

---

## ⚡ Чекліст імплементації (Checklist)

- [ ] **1. Модель зв'язків та Сховище Активів (Database & S3)**
  - [ ] Створити Alembic міграцію для таблиць `canvas_links` та `canvas_assets`.
  - [ ] Налаштувати інтеграцію з S3-сумісним сховищем (або локальним MinIO в Docker).
  - [ ] Створити FastAPI роути для генерації препідписаних посилань: `POST /api/v1/canvases/{canvas_id}/assets/presign`.
  - [ ] Реалізувати роут `POST /api/v1/canvases/{canvas_id}/assets/commit` для фіксації метаданих завантаженого активу та перевірки хешу SHA-256 (дедуплікація).
- [ ] **2. Роути зв'язування сутностей (Entity Linking API)**
  - [ ] Додати роути `POST /api/v1/canvases/{canvas_id}/links` та `DELETE /api/v1/canvases/{canvas_id}/links/{link_id}`.
  - [ ] Реалізувати валідацію `entity_type` (competitor, screenshot, insight, flower, adr, agent_run).
- [ ] **3. Інтерфейс інтеграції (Frontend Link Panel & Sidebar)**
  - [ ] Додати бічну панель (Sidebar) у Next.js для відображення існуючих зв'язків Canvas.
  - [ ] Створити модальне вікно або меню швидкого додавання зв'язків для виділеного елементу на Excalidraw.
  - [ ] Реалізувати візуальне завантаження файлів зображень (Drag-and-Drop скріншотів):
    - [ ] Отримати pre-signed URL з бекенду.
    - [ ] Завантажити файл безпосередньо в S3/MinIO.
    - [ ] Додати зображення на Excalidraw-сцену, використовуючи посилання на серверну копію (без вбудовування base64).
  - [ ] Створити панель шаблонів (Canvas Templates) для швидкого старту аналізу (наприклад, SWOT, Competitive Feature Matrix).
- [ ] **4. Тестування та Верифікація**
  - [ ] Написати тести на дедуплікацію скріншотів (спроба завантажити однаковий хеш).
  - [ ] Перевірити безпеку завантаження файлів (блокування небезпечних MIME-типів на бекенді).

---

## 🔗 Залежності та Зв'язки
- **Батьківський кущ**: `bush_5_atom_canvas_Molecules`
- **Попередні завдання**: `flower_canvas_persistence` (Phase 1)
- **Виконавці**:
  - `dnk-dev-01` (glm-5.2) — Frontend Drag-and-Drop, завантаження на S3, Sidebar сутностей.
  - `dnk_koder` (codestral-22b) — FastAPI S3 integration, Link API, deduplication checks.

---

## 🏁 Definition of Done (Критерії завершення)
- [ ] Будь-який скріншот завантажується безпосередньо в S3/MinIO за препідписаним URL і рендериться на Canvas.
- [ ] Розмір JSON-документа сцени при завантаженні зображень не зростає на розмір файлу (base64 відсутній).
- [ ] Елементи успішно лінкуються з сутностями, зв'язки відображаються у бічній панелі.
- [ ] Спроба завантажити однаковий файл повторно використовує існуючий `storage_key` завдяки SHA-256 перевірці.
- [ ] Всі файли відповідають стандартам MRH.
