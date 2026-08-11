# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/specs/DNK_CANVAS_DATA_MODEL.md"
# purpose: "Database Schema and Data Model Specification for Embedded DNK Canvas"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-11"
# author: "DNK-e.com Maksym"
# license: "MIT"
# --- END DNK-MRH-HEADER ---

# 🗄️ DNK OS DATA MODEL SPECIFICATION: DNK CANVAS DATABASE SCHEMA

This document details the PostgreSQL relational database schema for the **DNK Canvas Engine**, managed under the `hub_memory` schema. This data model guarantees robust persistence, revision histories, asset deduplication, and task traceability.

---

## 1. Schema Diagram Overview (Logical Model)

```
 +------------------------+             +------------------------+
 |    canvas_documents    |             |    canvas_revisions    |
 +------------------------+             +------------------------+
 | PK id (UUID)           |<----+       | PK id (UUID)           |
 |    workspace_id (UUID) |     |       | FK document_id (UUID)  |-----> FK parent_revision_id
 |    title (VARCHAR)     |     +------o|    revision_number (INT|
 |    description (TEXT)  |             |    scene_json (JSONB)  |
 |    document_type (VAR) |             |    scene_checksum (TXT)|
 | FK curr_revision (UUID)|             |    created_by (VARCHAR)|
 |    created_by (VARCHAR)|             |    created_at (TZ)     |
 |    created_at (TZ)     |             |    change_summary (TXT)|
 |    updated_at (TZ)     |             +------------------------+
 |    status (VARCHAR)    |
 |    metadata (JSONB)    |             +------------------------+
 +------------------------+             |     canvas_assets      |
      |                                 +------------------------+
      |      +--------------------+     | PK id (UUID)           |
      +----->|    canvas_links    |     | FK document_id (UUID)  |
      |      +--------------------+     |    storage_key (VARCHAR|
      |      | PK id (UUID)       |     |    sha256 (VARCHAR)    |
      |      | FK document_id(UUID|     |    mime_type (VARCHAR) |
      |      |    entity_type(VAR)|     |    byte_size (INT)     |
      |      |    entity_id (VAR) |     |    width (INT, NULL)   |
      |      |    relation_type   |     |    height (INT, NULL)  |
      |      |    created_at (TZ) |     |    created_at (TZ)     |
      |      +--------------------+     +------------------------+
      |
      |      +--------------------+
      +----->| canvas_audit_events|
             +--------------------+
             | PK id (UUID)       |
             | FK document_id(UUID|
             |    actor_type (VAR)|
             |    actor_id (VAR)  |
             |    event_type (VAR)|
             | FK revision_id(UUID|
             |    payload (JSONB) |
             |    created_at (TZ) |
             +--------------------+
```

---

## 2. PostgreSQL DDL Specification

All tables are created under the `hub_memory` schema. If the schema does not exist, Alembic will initialize it before executing the table migration.

### 2.1. Documents Table: `canvas_documents`

Tracks top-level metadata, lifecycle state, and scope boundaries for each visual workspace.

```sql
CREATE TABLE hub_memory.canvas_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    document_type VARCHAR(64) NOT NULL DEFAULT 'excalidraw',
    current_revision_id UUID, -- circular constraint deferred to after revisions creation
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL
);

-- Indices
CREATE INDEX idx_canvas_docs_workspace ON hub_memory.canvas_documents(workspace_id);
CREATE INDEX idx_canvas_docs_status ON hub_memory.canvas_documents(status);
```

### 2.2. Revisions Table: `canvas_revisions`

Stores complete scene snapshots. The actual elements and state of the Excalidraw board are stored here as a raw `JSONB` document.

```sql
CREATE TABLE hub_memory.canvas_revisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES hub_memory.canvas_documents(id) ON DELETE CASCADE,
    revision_number INT NOT NULL,
    scene_json JSONB NOT NULL,
    scene_checksum VARCHAR(64) NOT NULL, -- SHA-256 hash of scene_json string for data integrity
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    change_summary TEXT,
    parent_revision_id UUID REFERENCES hub_memory.canvas_revisions(id) ON DELETE SET NULL,
    
    CONSTRAINT uq_document_revision UNIQUE (document_id, revision_number)
);

-- Add Foreign Key to canvas_documents now that revisions exists
ALTER TABLE hub_memory.canvas_documents 
ADD CONSTRAINT fk_current_revision FOREIGN KEY (current_revision_id) 
REFERENCES hub_memory.canvas_revisions(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;

-- Indices
CREATE INDEX idx_canvas_revisions_doc ON hub_memory.canvas_revisions(document_id);
CREATE INDEX idx_canvas_revisions_created ON hub_memory.canvas_revisions(created_at);
```

### 2.3. Assets Table: `canvas_assets`

Tracks external binary files (such as screenshots, annotations, and wireframes) uploaded directly to the S3-compatible cloud storage.

```sql
CREATE TABLE hub_memory.canvas_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES hub_memory.canvas_documents(id) ON DELETE CASCADE,
    storage_key VARCHAR(512) NOT NULL UNIQUE, -- S3 absolute path / key
    sha256 VARCHAR(64) NOT NULL, -- Asset SHA-256 hash for strict deduplication
    mime_type VARCHAR(128) NOT NULL,
    byte_size INT NOT NULL,
    width INT,
    height INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indices
CREATE INDEX idx_canvas_assets_doc ON hub_memory.canvas_assets(document_id);
CREATE INDEX idx_canvas_assets_hash ON hub_memory.canvas_assets(sha256);
```

### 2.4. Links Table: `canvas_links`

Connects coordinates and objects within the canvas space directly to domain entities inside the DNK OS Task Forest, competitor research databases, or active execution logs.

```sql
CREATE TABLE hub_memory.canvas_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES hub_memory.canvas_documents(id) ON DELETE CASCADE,
    entity_type VARCHAR(64) NOT NULL, -- competitor, screenshot, insight, flower, adr, agent_run
    entity_id VARCHAR(255) NOT NULL, -- Canonical string identifier or UUID
    relation_type VARCHAR(64) NOT NULL DEFAULT 'references',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT uq_canvas_entity_link UNIQUE (document_id, entity_type, entity_id)
);

-- Indices
CREATE INDEX idx_canvas_links_doc ON hub_memory.canvas_links(document_id);
CREATE INDEX idx_canvas_links_entity ON hub_memory.canvas_links(entity_type, entity_id);
```

### 2.5. Audit Events Table: `canvas_audit_events`

Maintains a tamper-proof audit trail tracking human-editor and agentic-swarm mutations alike. Useful for monitoring agentic actions and triggering recovery procedures.

```sql
CREATE TABLE hub_memory.canvas_audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES hub_memory.canvas_documents(id) ON DELETE CASCADE,
    actor_type VARCHAR(64) NOT NULL, -- human, agent
    actor_id VARCHAR(255) NOT NULL, -- User UUID or Agent Identifier (e.g., dnk_koder)
    event_type VARCHAR(128) NOT NULL, -- create, edit_scene, link_entity, unlink_entity, add_asset, delete
    revision_id UUID REFERENCES hub_memory.canvas_revisions(id) ON DELETE SET NULL,
    payload JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indices
CREATE INDEX idx_canvas_audit_doc ON hub_memory.canvas_audit_events(document_id);
CREATE INDEX idx_canvas_audit_actor ON hub_memory.canvas_audit_events(actor_type, actor_id);
CREATE INDEX idx_canvas_audit_type ON hub_memory.canvas_audit_events(event_type);
```

---

## 3. Storage Optimization & Separation Rules

To prevent database bloating and lag in the frontend:
1. **Raw Canvas Elements Separated**: Large assets are stored in object storage (MinIO/S3), while metadata are indexed in `canvas_assets`.
2. **Checksum Integrity Enforcement**: All revision inputs are hashed on the client-side (`scene_checksum`). The FastAPI backend recalculates the hash to guarantee no data was corrupted during transit.
3. **No Embedded Base64**: The client code strips raw base64 images from Excalidraw exports, uploads them separately, and maps them to standard asset nodes containing `asset_id`.

---

## 4. Alembic Migration Strategy

All migration operations must be script-driven via Python. The migration scripts will be placed inside `DNKOS_MVP/core/migrations/versions/`.

```python
# Sample Alembic Migration Script Template
# File: core/migrations/versions/xxxx_add_canvas_tables.py

"""add canvas tables

Revision ID: xxxx_add_canvas_tables
Revises: previous_revision
Create Date: 2026-08-11
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # 1. Create Schema if not exists
    op.execute("CREATE SCHEMA IF NOT EXISTS hub_memory")
    
    # 2. Create documents table
    op.create_table(
        'canvas_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('document_type', sa.String(length=64), server_default='excalidraw', nullable=False),
        sa.Column('current_revision_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_by', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('status', sa.String(length=32), server_default='active', nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        schema='hub_memory'
    )
    
    # [Table creation scripts continue for revisions, assets, links, and audit_events]
    # Detailed index and constraint setup is configured via Alembic operations.
```
