# Skill: 1:1 Figma-to-Code Implementation

id: figma-to-code-1to1
version: 2.0.0
category: ui-implementation

## Objective

Convert Figma designs into React + TailwindCSS code with **absolute 1:1 precision (Pixel Perfect)** based on technical specifications from **REST API JSON files** (primary) and **MCP tools** (secondary/validation).

## Data Sources (Priority Order)

| Source       | File/Tool                | Purpose                                              |
| ------------ | ------------------------ | ---------------------------------------------------- |
| 1️⃣ Primary   | `enriched-tree.json`     | Node tree với token names đã map từ `boundVariables` |
| 2️⃣ Primary   | `variables.json`         | Design tokens (colors, spacing, radius)              |
| 3️⃣ Primary   | `components.json`        | Component metadata cho INSTANCE nodes                |
| 4️⃣ Primary   | `styles.json`            | Typography & Effect styles                           |
| 5️⃣ Secondary | MCP `get_variable_defs`  | Cross-validate tokens                                |
| 6️⃣ Secondary | MCP `get_design_context` | CSS snippets, complex styles                         |
| 7️⃣ Reference | MCP `get_screenshot`     | Visual verification                                  |

## MANDATORY Rules (Strict Compliance)

### 1. Source of Truth

- **NO GUESSING**: Never estimate colors, spacing, or dimensions by looking at images.
- **USE JSON FILES FIRST**: Check `.figma-debug/enriched-tree.json` trước khi dùng MCP.
- **CHECK `boundVariables`**: Nếu node có `boundVariables`, **PHẢI dùng token name** thay vì raw value.
- **Node ID Extraction**: Extract the exact `node-id` from the provided Figma link (e.g., `27-324` becomes `27:324`).
- **NO STYLE ASSOCIATION**: Never assume a node follows a named design token just because its size matches. Always verify via `boundVariables` or MCP.
- **FLEX DISTORTION PREVENTION**: For fixed-size elements in flex containers, apply `flex-shrink: 0` to prevent distortion.
- **ASPECT RATIO FIDELITY**: Maintain unequal `width`/`height` ratios as designed.

### 2. Token-First Color Management

- **Check `boundVariables.fills`** trong `enriched-tree.json`:

  ```json
  "boundVariables": {
    "fills": [{ "tokenName": "Surface/primary", "tokenValue": "#796bff" }]
  }
  ```

  → Dùng token class `bg-surfacePrimary` thay vì `bg-[#796bff]`

- **Config Synchronization**:
  1. Check `variables.json` để lấy tất cả tokens.
  2. So sánh với `tailwind.config.js`.
  3. **ADD MISSING** tokens vào config TRƯỚC khi code.
  4. **NEVER** use raw HEX in component code.

### 3. Component Instance Handling

- **For `type: "INSTANCE"` nodes**:
  1. Check `componentId` in node.
  2. Lookup in `components.json` để lấy component name.
  3. Kiểm tra xem component đã tồn tại trong codebase chưa.
  4. Reuse existing component nếu có, else create new.

### 4. Spacing & Layout

- **Check `boundVariables`** cho spacing tokens:

  ```json
  "boundVariables": {
    "itemSpacing": { "tokenName": "Space/md", "tokenValue": 16 }
  }
  ```

  → Dùng `gap-4` (nếu đã map) thay vì `gap-[16px]`

- **No Manual Balancing**: If Figma says X px, code X px.
- **AutoLayout Faithful**: Replicate exact flex structure from `layoutMode`, `primaryAxisAlignItems`, `counterAxisAlignItems`.

### 5. Typography

- **Check `styles.text`** reference trong node → lookup in `styles.json`.
- **Detailed Parameters**: Copy exact `font-size`, `line-height`, `font-weight`, `letter-spacing`.
- **Weight Mapping**: Regular=400, Medium=500, SemiBold=600, Bold=700.

### 6. No Subjective Optimization

- **NO "Modernization"**: Do not improve UI based on trends.
- **1:1 Accuracy**: Code must be a technical clone of Figma data.
- **CROSS-CHECK**: If REST API lacks info, use MCP tools to validate.

## Execution Workflow

1. **STEP 1**: Receive Figma link + extract `nodeId`.
2. **STEP 2**: Run `node scripts/figma-extract.mjs` (đã config đúng nodeId).
3. **STEP 3**: Open `.figma-debug/enriched-tree.json` - đây là source chính.
4. **STEP 4**: Check `variables.json` → sync missing tokens to `tailwind.config.js` + `index.css`.
5. **STEP 5**: Check `components.json` cho INSTANCE nodes.
6. **STEP 6**: Use MCP `get_design_context` cho CSS snippets nếu cần.
7. **STEP 7**: Write UI code using:
   - Token classes từ `boundVariables`
   - Component lookup từ `components.json`
   - Exact pixel values cho những gì không có token
8. **STEP 8**: Verify against MCP `get_screenshot`.

## Quick Reference: boundVariables → Tailwind

| boundVariables Property        | Check For   | Use                           |
| ------------------------------ | ----------- | ----------------------------- |
| `fills`                        | `tokenName` | `bg-{tokenName}` class        |
| `strokes`                      | `tokenName` | `border-{tokenName}` class    |
| `itemSpacing`                  | `tokenName` | `gap-{mapped}` or `gap-[Xpx]` |
| `paddingLeft/Right/Top/Bottom` | `tokenName` | `p-{mapped}` or `p-[Xpx]`     |
| `cornerRadius`                 | `tokenName` | `rounded-{mapped}`            |

---

**CRITICAL:**

- Dùng `enriched-tree.json` (REST API) làm source chính
- `boundVariables` có token → PHẢI dùng token, KHÔNG dùng raw value
- MCP dùng để cross-validate và lấy CSS snippets
