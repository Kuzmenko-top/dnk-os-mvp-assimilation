# TECHNICAL REPORT: MULTI-AGENT SWARM, SKILLS FRAMEWORK, & INFINITE CANVAS ARCHITECTURE
## Target Audience: Antigravity AI (Supervisor & Macro-Architect)
## Status: Active | Version: 3.0.0 | Updated: 2026-08-10
## Author: Gerych (Chief Orchestrator) | License: MIT

---

### 1. Architectural Vision & Unified Canvas Workspace
We have formulated the SOTA architectural model for creating the **DNK OS Team of Agents, Skills Framework, and visual DAG Workflows**. 

The fundamental thesis is a **Unified Infinite Canvas** (the Visual Shell) acting as the main cockpit, while specific sub-services (Memory, Chat, Logs, Database Viewer) are integrated as **pluggable slide-out panels (sliding sheets) or overlay tabs**, powered by Tailwind CSS v4 and Framer Motion, ensuring zero workspace fragmentation and preservation of the node editor state.

```
       +-------------------------------------------------------------+
       |                  Next.js Visual Shell (UI)                  |
       |  +-------------------------------------------------------+  |
       |  |                 Infinite Canvas                       |  |
       |  |  [Agent Node] ---> [Workflow Node] ---> [Tool Node]   |  |
       |  |       |                                               |  |
       |  +-------v-----------------------------------------------+  |
       |  | Pluggable Overlay Pane (Memory/Logs/Wiki Explorer)    |  |
       |  | * Slides in from right using Framer Motion            |  |
       |  | * Preserves canvas state underneath                    |  |
       |  +-------------------------------------------------------+  |
       +------------------------------+------------------------------+
                                      |
                      WebSocket / Server-Sent Events (SSE)
                                      |
                                      v
       +-------------------------------------------------------------+
       |                  Gerych Backend Orchestrator                 |
       |  (FastAPI + Python / Node.js Daemon + PostgreSQL Memory DB) |
       +------------------------------+------------------------------+
                                      |
                         Docker Container Sandboxes
                                      |
         +----------------------------+----------------------------+
         |                            |                            |
         v                            v                            v
     [ Rick ]                     [ Yuriy ]                    [ Cas ]
 (Scout - Web R/O)            (Slicer - Temp W/W)         (Synthesizer - R/W)
```

---

### 2. State-of-the-Art (SOTA) Donor Assimilation Mapping
We analyzed both the local repository knowledge catalog (`CATALOG_Repo_Knowledge.json`) and external standards to select our donor patterns:

1. **`langchain-ai/open-canvas` (UI Canvas)**:
   - **Role:** Primary donor for the infinite workspace canvas, artifacts rendering engine, and ProseMirror/CodeMirror-based side editors.
   - **Tech Stack:** React Flow (`@xyflow/react`), Zustand 5 (for lightweight canvas state management), and Next.js 14 dynamic imports (`ssr: false`).
2. **`langchain-ai/managed-deepagents` (Orchestration)**:
   - **Role:** Standardized runtime for our backend sandboxed agent container team (Rick, Yuriy, Cas, Tiffany, Morgan).
   - **Tech Stack:** Docker sandbox profiles, network isolation policies, and volume mounting guidelines.
3. **`langchain-ai/openwiki` (Memory UI)**:
   - **Role:** Markdown-based wiki-graph memory with visual node linking.
   - **Tech Stack:** Used to build the pluggable Memory tab/bot sliding panel.
4. **`pgvector/pgvector` & `chroma-core/chroma` (Memory DB)**:
   - **Role:** Memory embedding layer and cognitive episodic cache.

---

### 3. Structural Implementation of the Skills & Workflow Engine
Our skills framework is directory-driven to allow isolated, version-controlled execution inside Docker containers, preventing host system pollution.

#### A. Standardized Skill Directory Structure
Each skill complies with `SPEC_01_Agentic_Swarm_Patterns.md`:
```text
skills/<skill_name>/
├── SKILL.md                 # YAML frontmatter + Markdown directives (under 500 lines)
├── scripts/                 # Independent Python or Bash scripts running in Docker
├── references/              # Detailed API endpoints, specifications, and checklists
├── examples/                # Code examples and usage scenarios
└── resources/               # JSON-schemas, configurations, and templates
```

#### B. Workflow DAG Engine
Workflows are built as Directed Acyclic Graphs (DAG) on the canvas. 
- **Frontend Validation:** Handles are linked dynamically using `useUpdateNodeInternals()` to recalculate coordinates on variable additions.
- **Backend Validation:** Cycle detection is performed in Python using a lightweight Depth-First Search (DFS) algorithm to avoid heavy dependencies (like networkx) in production.
- **Database Persistence Guard:** PostgreSQL updates for canvas positions must explicitly invoke `conn.commit()` due to `autocommit=False` configurations in the DNK OS pool.

---

### 4. Taxonomy Alignment & Restructuring Performed
In accordance with strict structured taxonomy directives, we audited and cleaned the `docs/tasks/` workspace:
1. **Removed Redundant Draft:** Deleted the legacy/draft file `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/DNKOS_MVP/docs/tasks/Task_Flower_Managed_DeepAgents.md`.
2. **Taxonomy & MRH Realignment:** Re-routed and structured `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/DNKOS_MVP/docs/tasks/Task_Flower_open_canvas.md` to `docs/tasks/05_Flowers/Flower_open_canvas.md`, enriching it with correct YAML frontmatter and proper `mrh_id`.

---


## DNK-SOTA-001 Validation Status

- Status: VALIDATED SOTA BLUEPRINT v1.1 (Sandboxed Agent Runtimes)
- Scope: Filesystem + Egress + Sandbox contracts (see DNK-SOTA-001, Scope & Applicability)
- CI Gates:
  - tests/verification/test_path_hygiene.py (enforced via GitHub Actions)
