---
description: Sync Core Figma Data
---

This workflow synchronizes the fundamental data from a Figma file into the `figma-agent/data` directory. It uses the improved Python `figma_core` to safely fetch data without overloading the API.

# Prerequisites

- Ensure `FIGMA_ACCESS_TOKEN` is set in your environment (or `.env`).
- You need the FILE_KEY of your Figma Design.

## 🚀 Quick Start

Call this **ONE command** to sync all data sequentially:

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py sync-all <FILE_KEY> <NODE_IDS> --output-dir figma-agent/data
```

**Example:**

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py sync-all abcd1234 "1:2,3:4,5:6" --output-dir figma-agent/data
```

This will automatically:

1. ✏️ Fetch Node Tree
2. ✏️ Fetch Variables (Design Tokens)
3. ✏️ Fetch Styles (Typography & Colors)
4. ✏️ Fetch Components
5. ✏️ Export Images

All data saves to separate JSON files in `figma-agent/data/`.

---

## ⚙️ Optional Parameters

```bash
# Change image format (default: png)
--format png

# Change image scale (default: 1)
--scale 2

# Custom output directory (default: figma-agent/data)

```

**Example with options:**

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py sync-all <FILE_KEY> <NODE_IDS> \
  --format png \
  --scale 2 \
  --output-dir figma-agent/data
```

---

## 📌 Finding NODE_IDS

In Figma URL, look for `node-id=`:

```
https://figma.com/design/FILE_KEY/...?node-id=1:2
                                             ^^^
```

For multiple nodes, use comma-separated:

```bash
sync-all <FILE_KEY> "1:2,5:10,20:30"
```

## 📁 Output Structure

After running `sync-all`, you'll have these files in `figma-agent/data/`:

```
figma-agent/data/
├── node-tree.json          # Node structure & layout
├── variables.json          # Design tokens (colors, typography)
├── styles.json             # Published styles
├── components.json         # Published components      # Image URLs
└── sync-summary.json       # Summary of sync status
└── images
```

---

## 🔄 Next: Split Large Node Files

If `node-tree.json` is large (>1000 lines), split it for easier processing:

```bash
python3 .agent/skills/figma-analysis/scripts/split_node_data.py figma-agent/data/node-tree.json --max-lines 250
```

This creates `node-tree-split/` with organized sections.

---

## ✅ Post-Sync Validation

After sync completes, verify the following:

### Files Created

- [ ] `figma-agent/data/` directory populated with JSON files
- [ ] At least one `*node.json` file exists
- [ ] Optional files created (components.json, styles.json, tokens.json)
- [ ] Split directories created (`*-split/` folders with sections/)

### Validation Checklist

- [ ] All JSON files are valid (no parse errors)
- [ ] No duplicate files
- [ ] Split data organized in sections/
- [ ] Summary files (00-\*.json) exist
- [ ] Total line count > 1000
- [ ] Token/color files present

---

## 🎯 Next Steps: Build the UI

**After completing sync and validation:**

1. ✅ Data synced and split
2. ✅ Directory structure verified
3. ➡️ **Proceed to [figma-build.md](figma-build.md) workflow**
