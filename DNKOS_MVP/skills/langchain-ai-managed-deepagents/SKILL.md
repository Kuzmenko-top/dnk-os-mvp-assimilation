---
name: "langchain-ai-managed-deepagents"
description: "Асимільована SOTA навичка для побудови та деплою глибоких агентів (Deep Agents) на керованій інфраструктурі LangSmith за допомогою mda CLI."
repo_url: "https://github.com/langchain-ai/managed-deepagents"
assimilated_at: "2026-08-08"
status: "Active"
version: "1.0.0"
---

# 🌐 Managed Deep Agents (MDA) — SOTA Інтелектуальний Конспект

Managed Deep Agents — це сучасний фреймворк від LangChain, який дозволяє пакувати логіку агентів у структуровану папку проекту та запускати її на повністю керованій інфраструктурі LangSmith (LangSmith Agent Server + Sandboxes).

## 📁 Канонічна Структура Проекту (Project Structure)

Кожен проект Managed Deep Agent має чітку файлову структуру, яка автоматично розпізнається CLI-інструментом `mda`:

```
my-agent/
├── agent.py                        # Головний файл визначення агента (Required)
├── instructions.md                 # Глобальні інструкції та системний промпт
├── skills/                         # Папка з вузькоспеціалізованими навичками
│   └── <name>/
│       └── SKILL.md                # Специфікація навички (ідентична системі DNK OS!)
├── tools/                          # Кастомні інструменти (Python функції з @tool)
├── middleware/                     # Мідлварі для перехоплення викликів та життєвого циклу
├── channels/                       # Інтеграційні канали (Slack, Telegram, Web тощо)
├── sandbox/
│   └── __init__.py                 # Налаштування ізольованої пісочниці для виконання коду
├── memory.py                       # Налаштування довготривалої та сесійної пам'яті
├── pyproject.toml                  # Опис залежностей (uv-сумісний)
└── .env                            # Локальні секрети та API ключі
```

## ⚙️ Визначення Агента (`agent.py`)

Агент визначається за допомогою функції `define_deep_agent`:

```python
from managed_deepagents import define_deep_agent
from tools.search import internet_search

agent = define_deep_agent(
    name="research-assistant",
    model="google_genai:gemini-3.6-flash",  # Формат provider:model-name
    tools=[internet_search, {"type": "web_search"}],
    interrupt_on=["confirm_payout"],        # Human-in-the-loop апрув перед дією
    permissions=[{"path": "/sandbox/workspace", "access": "rw"}], # Безпека ФС
)
```

## 🧠 Навички (`skills/<name>/SKILL.md`) — Пряме Перекриття з DNK OS

Навички в Managed Deep Agents є декларативними Markdown-файлами з YAML-заголовком. Це повністю співпадає з архітектурою Skills у нашому DNK OS!

Приклад структури:
```yaml
---
name: research
description: Збір та синтез контексту перед відповіддю на складні запитання.
---
# Research Skill
1. Визначити відсутні дані.
2. Викликати інструмент пошуку.
3. Сформувати резюме.
```

## 🛡️ Пісочниця (`sandbox/__init__.py`)

Дозволяє агенту безпечно створювати файли та виконувати bash-команди:

```python
from managed_deepagents import define_sandbox

sandbox = define_sandbox(
    scope="thread",                 # На рівні треду (thread) або агента (agent)
    idle_ttl_seconds=600,
    default_timeout=600,
)
```

## 🚀 CLI-Команди `mda`

* `mda init <name>` — Ініціалізація нового проекту.
* `mda dev .` — Локальний запуск Agent Server та тестування в LangSmith Studio.
* `mda deploy .` — Деплой на керований сервер LangSmith.
* `mda delete` — Видалення деплою та пов'язаних пісочниць.
