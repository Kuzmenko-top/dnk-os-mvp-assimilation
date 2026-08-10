---
name: "open_canvas-assimilated"
description: "Assimilated patterns and components from langchain-ai/open-canvas"
version: "2.0.0"
category: "research"
assimilated_at: "2026-08-10"
---

# 🌐 Open-Canvas Assimilated Index Skill

This skill represents the structural and architectural patterns assimilated from LangChain's open-canvas repository. The codebase has been fully decomposed into 4 modular artifacts under DNK OS.

## 📂 Decomposed Artifact Index

1. 🔍 **Research & Evidence Trail**
   - **Path**: `DNKOS_MVP/docs/reports/rd_assimilation/open_canvas/RN-001_open-canvas-research.md`
   - **Scope**: Code evidence, mapping from React Flow to ProseMirror editors, and state handling validation.

2. 🏛️ **DNK OS Architecture Spec**
   - **Path**: `DNKOS_MVP/docs/tech/specs/DNK-ARCH-001_canvas-artifacts.md`
   - **Scope**: Artifact DB schema on PostgreSQL (`hub_memory.artifacts`), ownerId validation, and Event Bus synchronization protocol.

3. 🧬 **Component Inventory & Interfaces**
   - **Path**: `DNKOS_MVP/docs/tech/specs/DNK-COMP-001_editors.md`
   - **Scope**: Typed TS Interfaces for `ArtifactRendererProps`, `CodeRendererProps`, and `TextRendererProps` alongside events (`onContentChange`, `onSelectionChange`).

4. 🛡️ **Concrete Sandbox & Docker Rules**
   - **Path**: `DNKOS_MVP/docs/tech/standards/DNK-SEC-001_canvas-sandbox.md`
   - **Scope**: Network isolation policies, Docker anonymous volume masks, and zero-host pollution enforcement.

## 🚀 Usage Guide
Whenever configuring canvas workspace interfaces, react-flow layers, or editing states, reference the respective modular spec directly instead of using a monolithic file.
