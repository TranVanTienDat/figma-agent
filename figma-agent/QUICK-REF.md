# 🚀 Quick Reference: Extract Figma Data

## One-liner

```bash
node .agent/skills/figma-analysis/scripts/figma-extract.mjs
```

## Configuration

Edit `figma-extract.mjs`:

```javascript
const FIGMA_FILE_KEY = "your_file_key"; // Your design file
const TARGET_NODE_ID = "52:184"; // The node to extract
const ICON_NODE_IDS = []; // Optional icons
```

Set token in `.env.figma`:

```
FIGMA_TOKEN=your_token_here
```

## Output

```
.figma-debug/
├── enriched-tree.json      # Main output ⭐
├── node-tree-raw.json      # Raw data
├── variables.json          # Tokens
├── styles.json             # Styles
└── components.json         # Components
```

## Features

- ✅ Full node tree (no truncation)
- ✅ Variables API (Design Tokens)
- ✅ Styles API (Typography)
- ✅ Components API (metadata)
- ✅ Images export (icons)
- ✅ Bound variables enriched with token names

## Results

- Full hierarchy extraction
- Token mapping included
- Enterprise Variables support
- No data loss or truncation

## Docs

- Full guide: `figma-agent/FINAL-SOLUTION.md`
- Workflow: `.agent/workflows/sync-figma-data.md`
- Build Guide: `.agent/workflows/figma-build.md`
- Script: `.agent/skills/figma-analysis/scripts/figma-extract.mjs`
