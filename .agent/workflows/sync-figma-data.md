---
description: Sync Core Figma Data
---

This workflow synchronizes the fundamental data from a Figma file. It uses the Node.js Figma extraction script to safely fetch data without overloading the API.

# Prerequisites

- Ensure `FIGMA_ACCESS_TOKEN` is set in your environment (or `.env`).
- You need the FILE_KEY of your Figma Design.

## 🚀 Quick Start

Use the Node.js Figma extraction script to sync all data:

```bash
node .agent/skills/figma-analysis/scripts/figma-extract.mjs
```

Edit the configuration in `figma-extract.mjs` before running:

- Set `FIGMA_FILE_KEY` (your design file ID)
- Set `TARGET_NODE_ID` (the node to extract)
- Add your token to `.env.figma` file

1. ✏️ Fetch Node Tree (full hierarchy, no truncation)
2. ✏️ Fetch Variables (Design Tokens - Enterprise only)
3. ✏️ Fetch Styles (Typography & Effects)
4. ✏️ Fetch Components (metadata)
5. ✏️ Export Images (icon URLs)

All data saves to `.figma-debug/enriched-tree.json` and supporting files.

---

## ⚙️ Configuration

Edit these values in `figma-extract.mjs`:

```javascript
const FIGMA_FILE_KEY = "your_file_key_here"; // Change this
const TARGET_NODE_ID = "52:184"; // Change this
const ICON_NODE_IDS = []; // Optional: IDs to export as SVG
```

Set your token in `.env.figma`:

```
FIGMA_TOKEN=your_token_here
```

---

## 📌 Finding NODE_IDS and FILE_KEY

In Figma URL, look for:

```
https://figma.com/design/FILE_KEY/...?node-id=NODE_ID
                       ^^^^^^^^           ^^^^^^^
```

Example:

- **FILE_KEY**: `i2JD5CfMgttyQqmDY5v72Z`
- **NODE_ID**: `52:184` (colon format)

For multiple nodes, export them separately.

## 📁 Output Structure

After running the script, you'll have these files in `.figma-debug/`:

```
.figma-debug/
├── enriched-tree.json           # Main output: node tree with token mappings
├── node-tree-raw.json           # Raw Figma API response
├── variables.json               # Design tokens (if Enterprise)
├── styles.json                  # Published styles metadata
├── components.json              # Published components metadata
├── icons-urls.json              # Icon export URLs (if configured)
└── assets/                       # Downloaded icons (if configured)
```

The `enriched-tree.json` is the main file containing all node data with bound variables enriched with token names and values.

---

## ✅ Post-Extraction Validation

After extraction completes, verify the following:

### Files Created

- [ ] `.figma-debug/enriched-tree.json` exists (main output)
- [ ] `.figma-debug/node-tree-raw.json` exists (raw data)
- [ ] `.figma-debug/variables.json` exists (if Enterprise)
- [ ] `.figma-debug/styles.json` exists
- [ ] `.figma-debug/components.json` exists

### Validation Checklist

- [ ] All JSON files are valid (no parse errors)
- [ ] `enriched-tree.json` contains bound variables with token mappings
- [ ] Variable IDs are mapped to token names and values
- [ ] Component instances have component references
- [ ] Node tree has no truncation (full hierarchy)

---

## 🎯 Next Steps: Use the Data

**After completing extraction:**

1. ✅ Data extracted and available in `.figma-debug/`
2. ✅ Use `enriched-tree.json` for further processing
3. ➡️ **Copy data to `figma-agent/data/` for build workflows**
