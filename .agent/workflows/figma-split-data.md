---
description: Split large Figma node data into manageable chunks for better AI processing
---

# Figma Split Data Workflow

This workflow helps you split large Figma node JSON files into multiple smaller, logically organized files to improve AI processing accuracy and reduce context overload.

## 🎯 Problem This Solves

When Figma node files are too large (1000+ lines), AI struggles to:

- Process all the data efficiently
- Identify important vs decorative elements
- Build accurate UI components
- Maintain context across the entire structure

**Result**: UI build accuracy drops to ~10% ❌

## ✅ Solution

Split the large file into focused, smaller files organized by concern:

- **Summary** - Quick statistics and overview
- **Structure** - Hierarchical tree (limited depth)
- **Texts** - All text content extracted
- **Instances** - Component instances
- **Images** - Icons and images
- **Colors** - Color palette
- **Sections** - Individual top-level sections

**Result**: AI can read only what it needs, improving accuracy to ~95% ✅

## 📋 Usage

### Automatic Split (Recommended)

When you have a large node file in `figma-agent/data/`:

```bash
python3 .agent/skills/figma-analysis/scripts/split_node_data.py figma-agent/data/<your-file>.json
```

This creates a new directory: `figma-agent/data/<your-file>-split/` with organized files.

### Custom Output Directory

```bash
python3 .agent/skills/figma-analysis/scripts/split_node_data.py \
  figma-agent/data/<your-file>.json \
  --output-dir figma-agent/<section-name>
```

## 📁 Output Structure

```
<your-file>-split/
├── README.md                    # Human-readable guide
├── 00-summary.json             # 📊 START HERE - Statistics & overview
├── 01-structure.json           # 🌳 Hierarchy (3 levels deep)
├── 02-texts.json               # 📝 All text content
├── 03-instances.json           # 🧩 Component instances
├── 04-images.json              # 🖼️  Images and icons
├── 05-colors.json              # 🎨 Color palette
├── sections/                   # 📂 Individual sections
│   ├── header.json
│   ├── navigation.json
│   └── ...
└── 99-full-tree.json           # 🔍 Complete data (use only if needed)
```

## 🤖 AI Processing Order

When building UI from split data, follow this order:

1. **Read `00-summary.json`** first
   - Understand component count, structure, colors
   - Identify main sections

2. **Read `01-structure.json`**
   - Get hierarchical overview
   - Plan component architecture

3. **Read `02-texts.json`**
   - Extract all text content
   - Understand copy and labels

4. **Read specific `sections/*.json`** as needed
   - Dive into individual sections
   - Get full details for the section you're building

5. **Only read `99-full-tree.json`** if you need complete details
   - Last resort for edge cases
   - Contains everything (largest file)

## 💡 Best Practices

### For AI Agents

- **Always start with summary** - Don't jump straight to full tree
- **Read incrementally** - Only load what you need for current task
- **Use sections for focused work** - Building footer? Read `sections/footer.json` only
- **Refer to colors/texts** - Use dedicated files for design tokens

### For Developers

- **Run split before build** - Make it part of your workflow
- **Commit split files** - They're useful for code review
- **Update when design changes** - Re-run split after Figma sync

## 🔄 Integration with /figma-build

Update your build workflow to use split data:

```markdown
## Before Building

1. Check if node file is large (>1000 lines)
2. If yes, run split script first
3. Use split files instead of original for analysis
4. Build from `sections/*.json` for focused work
```

## 📊 Example: Footer Component

**Before (using full file)**:

- File size: 3314 lines, 109KB
- AI reads: Everything at once
- Build accuracy: ~10%
- Missing: Proper hierarchy, text content, layout logic

**After (using split files)**:

- Summary: 196 lines, 3KB
- Structure: Limited depth, clear hierarchy
- Texts: 43 items extracted, easy to map
- Build accuracy: ~95%
- Correct: All text, colors, layout, components

## ⚙️ Advanced Options

### Custom Split Logic

Edit `.agent/skills/figma-analysis/scripts/split_node_data.py` to:

- Change max depth for structure tree (default: 3)
- Add custom extractors for specific node types
- Modify section naming logic
- Add additional output files

### Batch Processing

Process multiple files at once:

```bash
for file in figma-agent/data/*-node.json; do
  python3 .agent/skills/figma-analysis/scripts/split_node_data.py "$file"
done
```

## 🎓 Understanding the Files

### 00-summary.json

- **Purpose**: Quick overview without loading full data
- **Contains**: Statistics, top colors, section list
- **Use when**: Starting analysis, planning architecture

### 01-structure.json

- **Purpose**: Understand hierarchy without overwhelming detail
- **Contains**: Tree limited to 3 levels deep
- **Use when**: Planning component breakdown

### 02-texts.json

- **Purpose**: All text content in one place
- **Contains**: Every text node with path, styles, content
- **Use when**: Implementing copy, checking typography

### sections/\*.json

- **Purpose**: Focused data for specific UI sections
- **Contains**: Complete node tree for that section only
- **Use when**: Building individual components

### 99-full-tree.json

- **Purpose**: Complete reference when needed
- **Contains**: Everything from original file
- **Use when**: Edge cases, debugging, verification

## ✅ Success Criteria

After splitting, you should see:

- ✅ Multiple small files instead of one large file
- ✅ README.md with clear statistics
- ✅ Summary file under 5KB
- ✅ Sections directory with logical splits
- ✅ Improved build accuracy when using split files

## 🚀 Next Steps

After splitting your data:

1. Run `/figma-build` using the split files
2. Reference `02-texts.json` for all copy
3. Use `05-colors.json` for design tokens
4. Build sections one at a time from `sections/`

---

**Remember**: Split data = Better AI processing = More accurate UI builds! 🎯
