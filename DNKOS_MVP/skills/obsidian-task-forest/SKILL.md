---
name: obsidian-task-forest
description: Навичка Герича для авто-генерації та управління метафорою Саду/Лісу Задач (Project Field -> Sector -> Epic Tree -> Feature Bush -> Task Flower) у форматі Obsidian Markdown.
---

# 🌾 Навичка Герича: Obsidian Task Forest Management

Ця навичка дозволяє Геричу автономно створювати та вести структуровані плани проєктів у форматі Obsidian Markdown.

---

## 🌻 Правила Створення Нотаток Задач-Рослин

Кожного разу, коли Герич створює або оновлює задачу у проекті, він дотримується наступного порядку:

1. **🌾 Поле Проєкту (`project_field`)**:
   - Файл: `docs/tasks/Field_{project_id}.md`
   - YAML: `type: project_field`, `plant_scale: field`, `tags: [dnk-task-forest, dnk-project-field]`

2. **🏞️ Сектор / Напрямок (`sector_zone`)**:
   - Файл: `docs/tasks/Sector_{sector_id}.md`
   - YAML: `type: sector_zone`, `plant_scale: sector`, `project_id: {project_id}`, `tags: [dnk-task-forest, dnk-sector-zone]`

3. **🌳 Епічне Дерево (`epic_tree`)**:
   - Файл: `docs/tasks/Tree_{tree_id}.md`
   - YAML: `type: epic_tree`, `plant_scale: tree`, `parent_id: {sector_id}`, `tags: [dnk-task-forest, dnk-epic-tree]`

4. **🌿 Кущ Фічі (`feature_bush`)**:
   - Файл: `docs/tasks/Bush_{bush_id}.md`
   - YAML: `type: feature_bush`, `plant_scale: bush`, `parent_id: {tree_id}`, `tags: [dnk-task-forest, dnk-feature-bush]`

5. **🌱 Квіточка / Мікро-крок (`task_flower`)**:
   - Файл: `docs/tasks/Flower_{flower_id}.md`
   - YAML: `type: task_flower`, `plant_scale: flower`, `parent_id: {bush_id}`, `status: completed|in_progress|pending`, `tags: [dnk-task-forest, dnk-task-flower]`

---

## ⚡ Оновлення Статусів та Перерахунок %

Після виконання будь-якого коду або завдання Герич:
1. Змінює статус відповідної `Task Flower` на `status: completed`.
2. Запускає парсер: `uv run python -m DNKOS_MVP.services.dnk_obsidian_task_forest.cli --sync`
3. Перевіряє, що відсоток готовності батьківського Куща та Дерева оновився знизу вгору.
