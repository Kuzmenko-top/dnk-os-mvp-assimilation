---
name: "open_canvas_assimilated"
description: "Assimilated patterns and components from langchain-ai/open-canvas"
version: "2.1.0"
category: "research"
author: "DNK-e.com Maksym"
triggers:
  - "open canvas"
  - "canvas editor"
  - "prosemirror code editor"
  - "canvas state persistence"
inputs_schema:
  type: "object"
  properties:
    action: {type: "string"}
    artifact_id: {type: "string"}
outputs_schema:
  type: "object"
  properties:
    status: {type: "string"}
---

# 🌐 Open-Canvas Assimilation Skill

## Overview
Meta-index and operational guide for integrating rich side-panel text and code editors (`ProseMirror` / `CodeMirror`) into the React Flow infinite canvas.

## Core Specifications
1. **[Research & Evidence Trail](../../docs/reports/rd_assimilation/open_canvas/RN-001_open-canvas-research.md)**
2. **[Architecture Specification](../../docs/tech/specs/DNK-ARCH-001_canvas-artifacts.md)**
3. **[Component Interfaces & Contracts](../../docs/tech/specs/DNK-COMP-001_editors.md)**
4. **[Security & Egress Standards](../../docs/tech/standards/DNK-SEC-001_canvas-sandbox.md)**

## Intent & Triggers
- Prompt triggers: `"open canvas"`, `"canvas editor"`, `"prosemirror code editor"`, `"canvas state persistence"`.
- Activates when building generative UI sidebars or syncing canvas node states with PostgreSQL.

## Quick Recipes & Execution Flow

### Recipe A: Using Editor Interfaces in Visual Shell (web_ui)
- Import state wrappers and properties defined in `DNK-COMP-001_editors.md`:
  ```typescript
  import { ArtifactRendererProps } from '@/types/canvas';
  ```
- Handle `onContentChange` and `onSelectionChange` events on the React Flow canvas.

### Recipe B: PostgreSQL Schema & State Synchronization
- Persist canvas editor states to PostgreSQL table `hub_memory.artifacts`:
  ```python
  with db_pool.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("UPDATE hub_memory.artifacts SET content = %s WHERE id = %s", (content, artifact_id))
      conn.commit()
  ```

## Pitfalls & Error Handling
- **Database Connection Pool Exhaustion**: Always ensure `conn.commit()` is called within `with` blocks to release pool connections.
- **State Synchronization Drift**: Unsaved editor changes must be flushed before triggering canvas node re-renders.
