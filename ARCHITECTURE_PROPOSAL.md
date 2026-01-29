# 🏗️ Proposal: Redesigned Figma Agent Core Architecture

## 1. Problem Definition

The current system operates on a "Metadata-First" approach, which is insufficient for "Design-to-Code" capabilities.

- **Current Limitation**: usage of `?depth=1` and `/meta` avoids fetching the actual design layers (Frames, Text, Rectangles).
- **Consequence**: The agent knows _about_ the file (who made it, when) but doesn't know _what is in_ the file (the layout, colors, text).

## 2. The Solution: "Graph-First" Core Architecture

We propose a new Core System responsible for mirroring the Figma Document Graph locally.

### Core Modules

#### A. The `FigmaClient` (Low-Level API Layer)

A direct, robust wrapper around the Figma REST API.
API Reference: `https://developers.figma.com/docs/rest-api/`

**Key Endpoints to Support:**

1.  **`GET /v1/files/:key` (The Full Dump)**
    - _Usage_: Initial load of small files or specific pages only.
    - _Strategy_: Use `depth` parameter wisely. Support pagination if Figma creates it eventually (currently not for nodes).
2.  **`GET /v1/files/:key/nodes?ids=...` (Targeted Surgical Extraction)**
    - _Usage_: The PRIMARY method. Don't fetch the whole world. Fetch only the `Selection` the user is interested in (e.g., "Hero Section").
    - _Optimization_: This drastically reduces payload size and latency.
3.  **`GET /v1/images/:key`**
    - _Usage_: Resolving image fills to actual URLs for downloading.

#### B. The `DocumentWalker` (Processing Layer)

Raw JSON from Figma is deeply nested and hard for AI to read linearly.
**Responsibility**:

- Flatten the nested tree into a list of "Nodes".
- Resolve "Style IDs" to actual values (e.g., replace `styleId: "123"` with `color: #FF0000`).
- Calculate absolute bounding boxes (Figma gives relative coordinates).

#### C. The `LocalCache` (Persistence Layer)

- **Problem**: Figma API is slow and has rate limits.
- **Solution**: Save the `nodes` response to `.figma_cache/` grouped by `node_id` or `version`. Use `X-Figma-Version` header to detect changes.

## 3. Implementation Plan (Python)

We will replace `fetch_figma_metadata.py` with a modular `figma_core` package.

```python
class FigmaCore:
    def __init__(self, token):
        self.api = FigmaAPI(token)

    def get_node_data(self, file_key, node_id):
        # 1. Check Cache
        # 2. Fetch specific Node only
        data = self.api.get_nodes(file_key, ids=[node_id])
        # 3. Resolve images if needed
        return self.process_node(data)
```

## 4. Proposed Workflow

1.  User: `/figma-build [url]`
2.  Agent parses URL to get `file_key` and `node_id`.
3.  **Core System**:
    - Calls `GET /v1/files/{key}/nodes?ids={node_id}`
    - Returns a distinct JSON structure for just that component.
4.  Agent receives: Cleaned, simplified JSON (removed unnecessary internal Figma props).
5.  Agent generates Code.

## 5. Next Steps

1.  Create `figma_core/client.py` - The HTTP wrapper.
2.  Create `figma_core/parser.py` - The tree traverser.
3.  Update `fetch_figma_metadata.py` to use this new core.
