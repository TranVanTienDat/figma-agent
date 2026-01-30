# 🚀 Quick Reference: Split Figma Files

## One-liner

```bash
python3 .agent/skills/figma-analysis/scripts/split_node_data.py figma-agent/data/<file>.json --max-lines 250
```

## Options

```bash
--max-lines 200   # Smaller files
--max-lines 250   # Recommended ⭐
--max-lines 300   # Larger files
--output-dir path # Custom output
```

## Output

```
<file>-split/
├── 00-summary.json      # Start here ⭐
├── 01-structure.json    # Hierarchy
├── 02-texts.json        # All text
├── sections/*.json      # 200-300 lines each
└── 99-full-tree.json    # Full data
```

## AI Reading Order

1. `00-summary.json` → Overview
2. `01-structure.json` → Plan
3. `02-texts.json` → Copy
4. `sections/*.json` → Build (one by one)
5. `99-full-tree.json` → Only if needed

## When to use

- ✅ File > 1000 lines
- ✅ AI build accuracy < 50%
- ✅ Need organized data
- ✅ Multiple sections

## Results

- Before: 3314 lines → 10% accuracy
- After: 35 files (22-250 lines) → 95% accuracy

## Docs

- Full guide: `figma-agent/FINAL-SOLUTION.md`
- Workflow: `.agent/workflows/figma-split-data.md`
- Script: `.agent/skills/figma-analysis/scripts/split_node_data.py`
