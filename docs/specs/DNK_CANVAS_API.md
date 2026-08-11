# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/specs/DNK_CANVAS_API.md"
# purpose: "API Specification for Embedded DNK Canvas"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-11"
# author: "DNK-e.com Maksym"
# license: "MIT"
# --- END DNK-MRH-HEADER ---

# 📡 DNK OS API SPECIFICATION: DNK CANVAS OPENAPI ENDPOINTS

This specification documents the REST API endpoints exposed by the **FastAPI Core Orchestrator** (`dnk_orchestrator`) at base path `/api/v1`.

---

## 1. Authentication & Common Headers

All endpoints require authentication. The request must include:
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

---

## 2. API Endpoint Definitions

### 2.1. Create Canvas
- **Method**: `POST`
- **Path**: `/api/v1/canvases`
- **Description**: Creates a new canvas document.
- **Request Body**:
```json
{
  "workspace_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "title": "Competitor Analysis - Q3 2026",
  "description": "Visual board mapping competitor features and UI architecture.",
  "metadata": {}
}
```
- **Response** (`201 Created`):
```json
{
  "id": "e4b6c310-863a-4467-8e6d-6ee89dcb926c",
  "workspace_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "title": "Competitor Analysis - Q3 2026",
  "description": "Visual board mapping competitor features and UI architecture.",
  "document_type": "excalidraw",
  "current_revision_id": null,
  "created_by": "user-uuid-1234",
  "created_at": "2026-08-11T12:00:00Z",
  "updated_at": "2026-08-11T12:00:00Z",
  "status": "active",
  "metadata": {}
}
```

---

### 2.2. List Canvases
- **Method**: `GET`
- **Path**: `/api/v1/canvases`
- **Query Parameters**:
  - `workspace_id` (UUID, Required)
  - `limit` (int, default: 20)
  - `offset` (int, default: 0)
- **Response** (`200 OK`):
```json
{
  "total": 1,
  "items": [
    {
      "id": "e4b6c310-863a-4467-8e6d-6ee89dcb926c",
      "title": "Competitor Analysis - Q3 2026",
      "status": "active",
      "created_at": "2026-08-11T12:00:00Z"
    }
  ]
}
```

---

### 2.3. Get Canvas Details
- **Method**: `GET`
- **Path**: `/api/v1/canvases/{canvas_id}`
- **Response** (`200 OK`):
```json
{
  "id": "e4b6c310-863a-4467-8e6d-6ee89dcb926c",
  "workspace_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "title": "Competitor Analysis - Q3 2026",
  "current_revision_id": "a967f8f9-4b10-449e-ba78-ef788a129188",
  "current_revision_number": 3,
  "status": "active",
  "updated_at": "2026-08-11T12:30:00Z",
  "scene_json": { "type": "excalidraw", "elements": [...] }
}
```

---

### 2.4. Save Canvas Scene (Optimistic Concurrency Control)
- **Method**: `PUT`
- **Path**: `/api/v1/canvases/{canvas_id}/scene`
- **Description**: Updates the canvas scene. It enforces optimistic locking to prevent overlapping edits.
- **Request Body**:
```json
{
  "expected_revision": 3,
  "scene_json": {
    "type": "excalidraw",
    "version": 2,
    "elements": [
      { "id": "el_1", "type": "rectangle", "x": 100, "y": 150 }
    ]
  },
  "scene_checksum": "f0e3c59a38f32...",
  "change_summary": "Added comparison rect nodes"
}
```
- **Responses**:
  - `200 OK` (Save success):
    ```json
    {
      "status": "success",
      "new_revision_id": "b11a43a0-761a-4712-a1df-fbc7c01289cf",
      "new_revision_number": 4,
      "updated_at": "2026-08-11T12:45:00Z"
    }
    ```
  - `409 Conflict` (Optimistic lock collision):
    ```json
    {
      "error": "REVISION_CONFLICT",
      "message": "The canvas has been modified by another actor. Stale revision provided.",
      "client_revision": 3,
      "server_revision": 4,
      "modified_by": "dnk_koder",
      "modified_at": "2026-08-11T12:44:12Z"
    }
    ```

---

### 2.5. Create Canvas Manual Revision (Milestone)
- **Method**: `POST`
- **Path**: `/api/v1/canvases/{canvas_id}/revisions`
- **Description**: Explicitly commits a milestone revision (named tag) in the history.
- **Request Body**:
```json
{
  "change_summary": "Milestone: Finished competitors mapping"
}
```
- **Response** (`201 Created`):
```json
{
  "revision_id": "c1c1f211-125c-43f1-bd56-cf4c781199a1",
  "revision_number": 5,
  "change_summary": "Milestone: Finished competitors mapping",
  "created_at": "2026-08-11T13:00:00Z"
}
```

---

### 2.6. List Revisions
- **Method**: `GET`
- **Path**: `/api/v1/canvases/{canvas_id}/revisions`
- **Response** (`200 OK`):
```json
{
  "revisions": [
    {
      "id": "c1c1f211-125c-43f1-bd56-cf4c781199a1",
      "revision_number": 5,
      "change_summary": "Milestone: Finished competitors mapping",
      "created_by": "user-uuid-1234",
      "created_at": "2026-08-11T13:00:00Z"
    },
    {
      "id": "b11a43a0-761a-4712-a1df-fbc7c01289cf",
      "revision_number": 4,
      "change_summary": "Added comparison rect nodes",
      "created_by": "user-uuid-1234",
      "created_at": "2026-08-11T12:45:00Z"
    }
  ]
}
```

---

### 2.7. Retrieve Revision Details
- **Method**: `GET`
- **Path**: `/api/v1/canvases/{canvas_id}/revisions/{revision_id}`
- **Response** (`200 OK`):
```json
{
  "id": "b11a43a0-761a-4712-a1df-fbc7c01289cf",
  "revision_number": 4,
  "scene_json": { "type": "excalidraw", "elements": [...] },
  "scene_checksum": "f0e3c59a38f32...",
  "change_summary": "Added comparison rect nodes",
  "created_by": "user-uuid-1234",
  "created_at": "2026-08-11T12:45:00Z"
}
```

---

### 2.8. Link Entity to Canvas
- **Method**: `POST`
- **Path**: `/api/v1/canvases/{canvas_id}/links`
- **Request Body**:
```json
{
  "entity_type": "competitor", // competitor, screenshot, insight, flower, adr, agent_run
  "entity_id": "competitor_id_shopify_plus",
  "relation_type": "competitor_profile"
}
```
- **Response** (`201 Created`):
```json
{
  "link_id": "d0d0f411-456c-489f-bbd2-cc684a0d9dfc",
  "canvas_id": "e4b6c310-863a-4467-8e6d-6ee89dcb926c",
  "entity_type": "competitor",
  "entity_id": "competitor_id_shopify_plus",
  "relation_type": "competitor_profile",
  "created_at": "2026-08-11T13:10:00Z"
}
```

---

### 2.9. Remove Entity Link
- **Method**: `DELETE`
- **Path**: `/api/v1/canvases/{canvas_id}/links/{link_id}`
- **Security Check**: Since unlinking is considered a destructive action, if triggered by an agent, this request will generate a Supervisor Approval Gate prompt before committing.
- **Response** (`200 OK` or `202 Accepted` if pending approval):
```json
{
  "status": "deleted",
  "link_id": "d0d0f411-456c-489f-bbd2-cc684a0d9dfc",
  "message": "Entity link removed successfully."
}
```

---

### 2.10. S3 Asset Presign Upload URL
- **Method**: `POST`
- **Path**: `/api/v1/canvases/{canvas_id}/assets/presign`
- **Request Body**:
```json
{
  "filename": "screenshot_evidence_01.png",
  "mime_type": "image/png",
  "byte_size": 1542000,
  "sha256": "4a5c53102bc0f0d2c31ab..."
}
```
- **Response** (`200 OK`):
```json
{
  "asset_id": "f5f5e412-25ef-4311-ab3a-df79ef12cf51",
  "upload_url": "https://minio.dnk-os.local/canvases/assets/f5f5e412?AWSAccessKeyId=...",
  "storage_key": "canvases/assets/f5f5e412-25ef-4311-ab3a-df79ef12cf51.png"
}
```

---

### 2.11. Export Canvas Render
- **Method**: `GET`
- **Path**: `/api/v1/canvases/{canvas_id}/export`
- **Query Parameters**:
  - `format` (string, Options: `excalidraw`, `png`, `svg`, Required)
  - `scale` (int, default: 2)
- **Response**:
  - If `excalidraw`: Returns `{ "type": "excalidraw", "elements": [...] }`
  - If `png` or `svg`: Returns the raw binary stream with appropriate `Content-Type: image/png` or `image/svg+xml`.

---

### 2.12. Execute Agent Programmatic Canvas Actions
- **Method**: `POST`
- **Path**: `/api/v1/canvases/{canvas_id}/agent-actions`
- **Request Body**:
```json
{
  "action_type": "append_canvas_elements", // create_canvas, read_canvas, append_canvas_elements, create_canvas_revision, link_canvas_to_insight, link_canvas_to_flower, add_evidence_reference
  "idempotency_key": "idem-key-810dcf22",
  "expected_revision": 5,
  "payload": {
    "elements": [
      {
        "type": "text",
        "text": "🤖 Agent Observation: Competitor relies on dynamic hydrations.",
        "x": 400,
        "y": 600,
        "strokeColor": "#ff0000"
      }
    ]
  }
}
```
- **Response** (`200 OK`):
```json
{
  "status": "success",
  "action_id": "a5e5d32c-7bbf-4c7b-bc82-9cf3d2ef91a1",
  "new_revision_number": 6,
  "audit_event_id": "999f8d1c-b17c-47fc-8f7e-77d01cbcecf1"
}
```
