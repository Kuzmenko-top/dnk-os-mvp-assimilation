# 🌸 Flower_01_implement_timeline_db.md: Реалізація таблиці та логера Timeline-моделі

## 📋 Метадані
---
mrh_id: "docs/tasks/Sector_03_UI/Tree_01_Timeline/Bush_01_Logger/Flower_01_implement_timeline_db.md"
author: "Maxim"
license: "DNK-INTERNAL"
source_type: "competitor_observation"
source_reference: "crewai/001-crewai-dashboard.png"
derivative_status: "adapted"
status: "Pending"
version: "1.0.0"
created_at: "2026-08-11"
---

## 🎯 Мета (Purpose)
Створити централізовану структуру даних та логер для побудови єдиного таймлайну подій роботи всіх субагентів у системі DNK OS.

## 📝 Критерії Приймання (Acceptance Criteria)
- [ ] Створено SQLite таблицю `agent_timeline` з полями: `id`, `timestamp`, `agent_name`, `action_type`, `payload_json`, `status`.
- [ ] Реалізовано клас `TimelineLogger` у файлі `core/utils/timeline_logger.py`.
- [ ] Написано unit-тести для перевірки запису та читання подій з бази даних.
- [ ] Логер підтримує асинхронні виклики та коректно працює при паралельному доступі.

## 💡 Джерело Ідеї (Idea Source)
Адаптовано з CrewAI Enterprise Dashboard (детальні лог-трейси виконання кроків).
* Докладний аналіз: `docs/research/competitors/crewai_analysis.md` (screen_001)
* Продуктовий інсайт: `docs/research/competitors/insights/INSIGHT_001_timeline.md`

## ⚡ Ризики та Запобігання (Risks & Mitigations)
- **Ризик:** Блокування доступу до бази даних при одночасній транзакції від декількох субагентів.
  - *Запобігання:* Використовувати SQLite в режимі `WAL` (Write-Ahead Logging) з автоматичним ретраєм транзакцій (`timeout=30s`).

## 🔍 Метод Перевірки (Verification Method)
1. Запустити симуляційний скрипт паралельної роботи трьох агентів.
2. Виконати SQL-запит до таблиці `agent_timeline` та переконатися, що всі події збережено хронологічно.
3. Запустити тест `pytest tests/test_timeline_logger.py`.
