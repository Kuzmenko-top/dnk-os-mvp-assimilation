# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/ARCH_02_MVP_Master_Plan.md"
# purpose: "Canonical documentation and task tracking note"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-09"
# --- END DNK-MRH-HEADER ---

# 🏛️ Канонічна Архітектура Нової Версії DNK OS MVP 0.1.0 у директорії DNKOS_MVP

Цей документ зафіксовує **єдине джерело правди (Single Source of Truth)** для нової версії продукту **DNK OS MVP 0.1.0**. 

Уся інфраструктура, кодова база, REST API роутери, React/Next.js UI компоненти та еталонна тема **DNK Ecom (T Core / v0.1.0)** розгортаються **ВИКЛЮЧНО у директорії `DNKOS_MVP/`**.

---

## 🏛️ Канонічна Структура Директорії `DNKOS_MVP/`

```mermaid
graph TD
    Root["DNKOS_MVP/ (Єдине Джерело Правди)"] --> Core["1. core/ (OmniRouter, Swarm Orchestrator, Task Graph)"]
    Root --> Services["2. services/ (Мікросервіси & dnk_shopify)"]
    Root --> Docs["3. docs/ (Архітектурні Специфікації & RAG)"]
    Root --> Visual["4. visual_shell/ (React/Next.js UI Studio)"]

    Services --> ShopifyApp["services/dnk_shopify/"]
    ShopifyApp --> AppSrc["src/app/ (Super Admin & Merchant Routers, Service Bridge)"]
    ShopifyApp --> ThemeCore["DNK-e.com/ (Tinker 4.3.1 Core & blocks/)"]

    Execution["Герич (Hermes Execution Engine)"] -->|100% Фізичні Коміти| Root
```

---

## 📑 5 Фундаментальних Правил Чистоти Інфраструктури

### 1. Повна Локалізація у `DNKOS_MVP/`
- Жоден новий файл додатка не розгортається у застарілі зовнішні директорії.
- Сервіс створення магазинів розміщується строго за шляхом: `DNKOS_MVP/services/dnk_shopify/`.

---

### 2. Повторне Використання 6 Місяців Напрацювань та Блискучої Бази Знань
- Асимільовані знання (Tinker 4.3.1 Horizon architecture, Open Design Token Transpiler, Universal Commerce Protocol UCP, Nova Poshta 1-Click Checkout Proxy, Volume Discounts) переносяться у `DNKOS_MVP/services/dnk_shopify/` як випробувані, 100% пройдені атоми.

---

### 3. Єдина Еталонна Тема: `DNK Ecom v0.1.0 (T Core)`
- Тема розгортається у `DNKOS_MVP/services/dnk_shopify/DNK-e.com/`.
- Використовує **95 атомарних Horizon-блоків** у `blocks/` з підтримкою нових тегів Shopify `{% block %}` та `{% partial %}`.

---

### 4. Двохпанельний UI Studio у `DNKOS_MVP/visual_shell/`
- **Super Admin Studio**: Двохпанельний Diff-редактор для асиміляції донорів з GitHub/Figma та декомпозиції 2.0 тем у Horizon-блоки.
- **Merchant Launchpad**: 3-кроковий майстер Vibe Coding під нішу з 1-Click деплоєм у Shopify Admin.

---

### 5. Суворий Розподіл Ролей (Mentor vs Execution)
- **Antigravity (Ментор & Головний Архітектор)**: Формує архітектурні мапи, перевіряє цілісність системи, пише специфікації у `DNKOS_MVP/docs/tech/` та готує Промпти. **Нуль прямого редагування коду**.
- **Hermes (Герич)**: Фізично виконує 100% маніпуляцій з файлами у `DNKOS_MVP/`, реалізує Python/Liquid/JS код, запускає `pytest` та робить коміти в Git.