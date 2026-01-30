---
workflow_id: mcp-figma-exhaustive-deep-dive
description: Perform an exhaustive Figma data extraction combining REST API + MCP to ensure complete, untruncated design data.
---

# Figma Deep Extract Workflow v3.0

**HYBRID APPROACH: REST API + MCP**

To ensure **ABSOLUTELY NO DATA IS MISSED** and **NO GUESSING** occurs, the agent MUST strictly follow ALL steps below.

---

## Prerequisites

1. **Figma Token**: Ensure `.env.figma` has valid `FIGMA_TOKEN`
2. **Script**: `scripts/figma-extract.mjs` must exist
3. **Figma Desktop App**: Must be open with target file active (for MCP)

---

## Phase 1: Data Collection (Before Coding)

### Step 1.1: REST API - Full Data Extraction

**WHY**: MCP `get_design_context` bị truncate với components lớn. REST API lấy TOÀN BỘ data không giới hạn.

1. **Update Script Target**:
   - Edit `scripts/figma-extract.mjs`:
     - Set `FIGMA_FILE_KEY` = file key từ URL
     - Set `TARGET_NODE_ID` = node ID từ URL (format: `33:3750`)

2. **Run Script**:

   ```bash
   node scripts/figma-extract.mjs
   ```

3. **Script sẽ fetch các API sau**:

   | API Endpoint                           | Output File       | Mục đích                   |
   | -------------------------------------- | ----------------- | -------------------------- |
   | `GET /v1/files/:key/nodes?ids=X`       | `node-tree.json`  | Full node structure        |
   | `GET /v1/files/:key/variables/local`   | `variables.json`  | Design tokens (Enterprise) |
   | `GET /v1/files/:key/styles`            | `styles.json`     | Typography & Effects       |
   | `GET /v1/files/:key/components`        | `components.json` | Component metadata         |
   | `GET /v1/images/:key?ids=X&format=svg` | `assets/*.svg`    | Icon exports               |

4. **Output chính**: `.figma-debug/` folder chứa:
   - `node-tree.json` - Full recursive children (không bị cắt)
   - `variables.json` - All design tokens với `valuesByMode`
   - `styles.json` - Typography/Effect style names
   - `components.json` - Component names & descriptions
   - `enriched-tree.json` - 🔥 Tree với token names đã map sẵn từ `boundVariables`
   - `assets/` - Exported SVG icons

5. **Keep Files Open**: Reference JSON throughout coding

---

### Step 1.2: MCP - Variable Definitions (Cross-Validation)

**WHY**: MCP cho TOKEN NAMES nhanh chóng, dùng để cross-check với REST API.

1. **Invoke `get_variable_defs`** for target node:

   ```
   mcp_figma-dev-mode-mcp-server_get_variable_defs(nodeId: "33:3750")
   ```

2. **Extract ALL tokens** (nếu Variables API không available do không có Enterprise):
   - Colors: `Surface/primary_med_em`, `Text/high_em`, etc.
   - Spacing: `Space/xs`, `Space/md`, `Space/xl`, etc.
   - Typography: `Para/semibold`, `Caption 1/medium`, etc.
   - Radius: `Radius/component/radius_sm`, `Radius/big_component/radius_md`
   - Effects: `Elevation/e3`, `Component_effect/primary_default`

3. **Compare với `variables.json`**: MCP và REST API phải match

---

### Step 1.3: MCP - Key Element CSS (For Complex Styles)

**WHY**: REST API thiếu CSS output. MCP cho CSS snippets.

1. **Identify Key Elements** từ JSON tree:
   - Root container
   - Interactive states (selected, hover)
   - Buttons (primary, secondary)
   - Input fields
   - Any element with complex effects

2. **For Each Key Element**:
   - Designer select element đó trong Figma Desktop
   - Invoke `get_design_context` với nodeId trống (lấy selected)
   - HOẶC invoke với specific nodeId nếu biết

3. **Save CSS Snippets**: Giữ lại các CSS quan trọng từ MCP response

---

### Step 1.4: MCP - Screenshot for Visual Reference

**Invoke `get_screenshot`** để có hình ảnh tham chiếu:

```
mcp_figma-dev-mode-mcp-server_get_screenshot(nodeId: "33:3750")
```

---

## Phase 2: Token Synchronization (TRƯỚC KHI CODE)

### Step 2.1: Audit Existing Configuration

1. **Read config files**:
   - `src/index.css` - CSS variables
   - `tailwind.config.js` - Tailwind color/spacing mappings

2. **Compare with** `variables.json` và `enriched-tree.json`

---

### Step 2.2: FORCE ADD Missing Variables

**STRICTLY PROHIBITED**: DO NOT use raw hex values in components!

**Dùng `variables.json` để extract tokens:**

- Mỗi variable có `name` (token name) và `valuesByMode` (actual values)
- Nếu có `codeSyntax.WEB`, dùng trực tiếp

For EACH missing token:

1. **Add CSS Variable** to `src/index.css`:

   ```css
   :root {
     --surface-primary-med-em: #796bff;
     --text-base-em: #c3c6cc;
     /* ... */
   }
   ```

2. **Add Tailwind Mapping** to `tailwind.config.js`:

   ```js
   colors: {
     surfacePrimaryMedEm: "var(--surface-primary-med-em)",
     textBaseEm: "var(--text-base-em)",
   }
   ```

3. **Add Shadow Utilities** if needed:
   ```js
   boxShadow: {
     'e3': '0 20px 20px -12px rgba(0,0,0,0.03), 0 3px 3px -1.5px rgba(0,0,0,0.03), 0 1px 1px -0.5px rgba(0,0,0,0.03)',
   }
   ```

---

## Phase 3: Implementation (NOW You Can Code)

### Step 3.1: Container First

1. **Check Root Node** trong `enriched-tree.json`:
   - `cornerRadius` → `rounded-[Xpx]`
   - `fills` → Check `boundVariables.fills` for token name, else `bg-*`
   - `effects` → `shadow-*`
   - `strokes` → `border-*`
   - `padding` → Check `boundVariables` for spacing token

2. **NEVER ASSUME DEFAULTS**:
   - Figma có shadow → Code PHẢI có shadow
   - Figma có bg-white → Code PHẢI có bg-white

---

### Step 3.2: Traverse Tree Top-Down

For EACH node in JSON tree:

1. **Check Type**:
   - `FRAME` / `GROUP` → Layout wrapper, check fills/effects
   - `INSTANCE` → Check `componentId` → lookup in `components.json` for name
   - `TEXT` → Typography styling
   - `VECTOR` → Icon, check if exported in `assets/`

2. **Map Styles**:
   | JSON Property | CSS/Tailwind |
   |---------------|--------------|
   | `cornerRadius` | `rounded-[Xpx]` |
   | `fills[].color` | Use token from `boundVariables` if exists |
   | `strokes` + `strokeWeight` | `border border-[color]` |
   | `effects[].type: "DROP_SHADOW"` | `shadow-*` |
   | `effects[].type: "INNER_SHADOW"` | Custom box-shadow inset |
   | `effects[].type: "BACKGROUND_BLUR"` | `backdrop-blur-[Xpx]` |
   | `padding` | Use token from `boundVariables` if exists |
   | `gap` | Use token from `boundVariables` if exists |
   | `layoutMode: "HORIZONTAL"` | `flex flex-row` |
   | `layoutMode: "VERTICAL"` | `flex flex-col` |
   | `primaryAxisAlignItems` | `justify-*` |
   | `counterAxisAlignItems` | `items-*` |

---

### Step 3.3: Text Elements

For each `type: "TEXT"` node:

- Check `styles.text` → lookup in `styles.json` for style name
- `fontSize` → `text-[Xpx]`
- `fontWeight` → `font-*` (400=normal, 500=medium, 600=semibold)
- `lineHeightPx` → `leading-[Xpx]`
- `fills[].color` → Use token from `boundVariables`
- `characters` → Actual text content

---

### Step 3.4: Component Instances

For each `type: "INSTANCE"` node:

1. **Lookup `componentId`** trong `components.json`
2. **Get component name**: e.g., `Button/Primary`, `Input/Default`
3. **Check if existing component** in codebase matches
4. **Apply any overrides** từ `componentProperties`

---

### Step 3.5: Interactive States

**REST API chỉ có 1 state**. Cho interactive states (hover, selected):

1. **Check MCP `get_design_context`** từ Step 1.3
2. **Hoặc yêu cầu Designer copy CSS** từ Figma Dev Mode panel
3. **Không được đoán** - phải có data rõ ràng

---

## Phase 4: Cross-Validation

### Step 4.1: Compare Sources

| Data Point | REST API                            | MCP                  | Use Which?          |
| ---------- | ----------------------------------- | -------------------- | ------------------- |
| Colors     | `variables.json` + `boundVariables` | `get_variable_defs`  | REST API (complete) |
| Spacing    | `variables.json` + `boundVariables` | `get_variable_defs`  | REST API (complete) |
| Typography | `styles.json`                       | Font style ref       | REST API + MCP      |
| Effects    | `node-tree.json` effects            | `get_design_context` | Combine both        |
| Components | `components.json`                   | N/A                  | REST API            |

### Step 4.2: Resolve Conflicts

- **boundVariables exists** → Always use the token name
- **Only raw value** → Check if a close token exists in `variables.json`, if not, add new token
- **Different values** → Trust REST API Variables (design system source of truth)

---

## Failure Handling Rules

### ❌ NEVER DO:

1. Hardcode hex values when token exists in `boundVariables`
2. Guess dimensions not in data
3. Assume transparency for containers
4. Skip shadows/borders visible in Figma
5. Use truncated MCP data without verification against REST API
6. Ignore `componentId` for INSTANCE nodes

### ✅ ALWAYS DO:

1. Reference `enriched-tree.json` for token-mapped values
2. Use token classes from tailwind config
3. Cross-check MCP variables with REST API `variables.json`
4. Lookup component names from `components.json`
5. Ask for clarification if data is missing
6. Test visual output against Figma screenshot

---

## Quick Reference: Data Sources

| What                      | Primary Source                           | Fallback                    |
| ------------------------- | ---------------------------------------- | --------------------------- |
| Full tree structure       | REST `node-tree.json`                    | -                           |
| Variable/Token names      | REST `variables.json` + `boundVariables` | MCP `get_variable_defs`     |
| Style names               | REST `styles.json`                       | -                           |
| Component names           | REST `components.json`                   | -                           |
| Enriched tree with tokens | `enriched-tree.json`                     | Manual mapping              |
| Complex element CSS       | MCP `get_design_context`                 | Designer copy from Dev Mode |
| Interactive states        | Designer copy from Dev Mode              | MCP `get_design_context`    |
| Visual reference          | MCP `get_screenshot`                     | -                           |
| Icon assets               | REST `GET /images` (SVG)                 | Manual export               |

---

## TL;DR Checklist

- [ ] Run REST API script → `.figma-debug/` folder với all JSONs
- [ ] Verify `variables.json` exists (Enterprise) hoặc use MCP fallback
- [ ] Get MCP `get_variable_defs` → Cross-validate
- [ ] Get MCP `get_design_context` for key elements
- [ ] Sync all tokens to `index.css` + `tailwind.config.js`
- [ ] Use `enriched-tree.json` for token-mapped values
- [ ] Check `components.json` for INSTANCE nodes
- [ ] Code container first (root node styles)
- [ ] Traverse tree, map each node's styles with tokens
- [ ] Verify against screenshot
- [ ] NO hardcoded values, NO guessing

---

## 5. Next Step: Implementation Rules

Once data extraction is complete, you MUST proceed to the Implementation Rules to ensure code quality:
-> View `.agent/workflows/figma-implementation-rules.md`
