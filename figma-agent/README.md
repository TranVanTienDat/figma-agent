# Figma Agent

This directory contains data, configuration, and documentation for Figma Agent.

## 📂 Directory Structure

```
figma-agent/
├── data/                    # Contains extracted data from Figma
│   ├── footer-node.json     # Original file (large)
│   ├── footer-split-v2/     # ✅ Split data (Recommended)
│   └── ...
├── config.yaml              # Agent configuration
├── FINAL-SOLUTION.md        # 📘 Summary of split file solution
├── QUICK-REF.md             # ⚡ Quick reference guide
├── RECURSIVE-SPLIT-GUIDE.md # 📖 Recursive split guide
└── SPLIT-DATA-GUIDE.md      # 🇻🇳 Vietnamese specific guide
```

## 🚀 Main Tools

### Split Data Script

Automatically splits large Figma files into smaller files (200-300 lines) for more accurate AI processing.

```bash
python3 ../.agent/skills/figma-analysis/scripts/split_node_data.py \
  data/footer-node.json \
  --max-lines 250
```

See details: [QUICK-REF.md](QUICK-REF.md)

## 📚 Important Documentation

1. **[FINAL-SOLUTION.md](FINAL-SOLUTION.md)** (Recommended)
   - Most comprehensive summary of the solution
   - Usage, results, comparison
   - Best practices

2. **[QUICK-REF.md](QUICK-REF.md)**
   - Quick reference for commands and options
   - File reading order for AI

3. **[RECURSIVE-SPLIT-GUIDE.md](RECURSIVE-SPLIT-GUIDE.md)**
   - Explanation of recursive file splitting mechanism
   - How to configure deep split

4. **[SPLIT-DATA-GUIDE.md](SPLIT-DATA-GUIDE.md)**
   - Detailed documentation (Vietnamese)

## 🔄 Workflow

To build UI from Figma data most accurately:

1. **Check size**: Check if the original JSON file is large (>1000 lines).
2. **Split**: Run the split data script if the file is large.
3. **Read**: Read `00-summary.json` first, then `01-structure.json`.
4. **Build**: Read each file in the `sections/` directory to build each component part.

---

**Note**: Always prioritize using split data in the `data/*-split/` directories instead of the original JSON file to ensure highest accuracy (95% vs 10%).
