# 🌸 Flower_01_security_decorator.md: Реалізація декоратора безпеки Supervisor Approval Gates

## 📋 Метадані
---
mrh_id: "docs/tasks/Sector_01_Core/Tree_03_Security/Bush_02_Gates/Flower_01_security_decorator.md"
author: "Maxim"
license: "DNK-INTERNAL"
source_type: "competitor_observation"
source_reference: "crewai/002-crewai-approval-gate.png"
derivative_status: "adapted"
status: "Pending"
version: "1.0.0"
created_at: "2026-08-11"
---

## 🎯 Мета (Purpose)
Впровадити гнучкий та надійний механізм верифікації критичних дій (Supervisor Approval Gates) за допомогою Python-декоратора для захисту системи від небезпечних операцій.

## 📝 Критерії Приймання (Acceptance Criteria)
- [ ] Створено декоратор `@security_gate(level="high")` в `core/security/gates.py`.
- [ ] При виклику декорованої функції процес призупиняється та створює запис у базі даних `approval_queue` зі статусом `pending`.
- [ ] Оркестратор `herich_librarian` отримує сповіщення про запит та ініціює виклик `clarify` для отримання рішення користувача.
- [ ] Після схвалення або відхилення функція продовжує виконання або повертає виняток `PermissionError`.

## 💡 Джерело Ідеї (Idea Source)
Адаптовано з механізму CrewAI Human-in-the-loop (HITL).
* Докладний аналіз: `docs/research/competitors/crewai_analysis.md` (screen_002)
* Продуктовий інсайт: `docs/research/competitors/insights/INSIGHT_002_approval_gate.md`

## ⚡ Ризики та Запобігання (Risks & Mitigations)
- **Ризик:** Нескінченне блокування процесу виконання, якщо користувач не відповідає довгий час.
  - *Запобігання:* Додати таймаут очікування (`timeout=600s`). Після закінчення таймауту автоматично маркувати запит як `rejected` та зупиняти виконання.

## 🔍 Метод Перевірки (Verification Method)
1. Декорувати тестову функцію `@security_gate(level="high")`.
2. Запустити її виконання у фоновому режимі та переконатися, що вона призупинилась і створила запит у черзі.
3. Просимулювати схвалення та перевірити успішне завершення функції.
4. Запустити тест `pytest tests/test_security_gates.py`.
