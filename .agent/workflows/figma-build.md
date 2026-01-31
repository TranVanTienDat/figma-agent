---
description: Generate React/Next.js code from Figma data with automatic large file optimization
---

# Figma Build Workflow

This workflow converts your synced Figma design data into production-ready React/Next.js code, with built-in optimization for large files.

## Prerequisites

- The `figma-agent/project.md` must contain the correct project context (Tech Stack, Styling, etc.).
- The `figma-agent/data/` directory must contain the synced design data.
- The `split_node_data.py` script must be available in `.agent/skills/figma-analysis/scripts/`.

## 🛠️ Technical Requirements

### 1. Data Processing Standards (New ⭐)

- **Large File Detection**: Automatically check if JSON files exceed 1000 lines.
- **Recursive Splitting**: Use `split_node_data.py` to break large files into manageable chunks (200-300 lines).
- **Context Prioritization**: Always prioritize reading split files (`summary.json`, `sections/*.json`) over raw monolithic files.
- **Code Conversion Principles**: Must follow strict rules for scanning, dynamic ID linking, and recursive priority as defined in the `code-conversion-principles` skill.

### 2. Design Analysis Standards

- **Layout Mapping**: Identify primary structures using Flexbox or Grid. Analyze Auto Layout properties (padding, gap, alignment).
- **Pattern Recognition**: Detect repeating UI patterns to determine sub-components.
- **State & Tokens**: Identify interactive states and map colors/typography to `tokens.json`.

### 3. Component Creation Standards

- **Modular Structure**: Follow Atomic Design. Create focused, reusable components.
- **Clean Code**: Use the project's tech stack (e.g., TypeScript). Avoid hard-coded values.
- **Responsive & Accessible**: Ensure adaptability and semantic HTML5.

## 📝 Build Execution Checklist

The agent will perform the following steps:

### Phase 1: Preprocessing (Critical for Accuracy)

- [ ] **Check File Size**: If target data file > 1000 lines, proceed to split.
- [ ] **Run Split Script**: Execute:
  ```bash
  python3 .agent/skills/figma-analysis/scripts/split_node_data.py figma-agent/data/<file>.json --max-lines 250
  ```
- [ ] **Verify Output**: Confirm generation of `summary.json`, `structure.json`, and `sections/`.

### Phase 2: Analysis & Building (Senior Fragmented Data Strategy)

- [ ] **Step 1: Read `00-summary.json` (The Map)**
  - Quickly understand node distribution (Text, Frames, Instances).
  - Identify root frame layout and top-level sections.
  - **MANDATORY**: Verify **Background Color** via root fills (Visual Dominance Rule).
- [ ] **Step 2: Read `01-structure.json` (The Skeleton)**
  - Map the 3-level hierarchy and plan the component tree.
  - Detect layout patterns (Flex/Grid) and spacing.
- [ ] **Step 3: Read `02-texts.json` (Source of Truth for Copy)**
  - Extract all 40+ text nodes and their styles (Manrope,Inter, etc.).
  - Identify critical labels (Prices, Ratings, Labels) for visual audit.
- [ ] **Step 4: Read `03-instances.json` (Component Discovery)**
  - Scan for component IDs and variants.
  - Link instances to their master logic (Buttons, Icons, Badges).
- [ ] **Step 5: Read `04-images.json` & `05-colors.json` (Design Tokens)**
  - Extract image metadata and resolve the full Color Palette.
  - Map hex codes to semantic design tokens (Primary, Neutral).
- [ ] **Step 6: Build Sections (Incremental Build)**
  - Read `sections/*.json` one by one (200-250 lines each).
  - Process fragments sequentially to maintain accuracy < 1% deviation.
- [ ] **Step 7: Reference `99-full-tree.json` (Debug Mode)**
  - Only use for cross-referencing buried data or complex recursive overrides.

### Phase 3: Implementation & Validation

- [ ] **Code Generation**: Write JSX/TSX incrementally section by section.
- [ ] **Pixel-Perfect Validation Audit**:
  - Compare generated layout against the "Real UI" image.
  - Verify presence of: Star ratings, precise prices, license list items, and floating nav buttons.
  - If deviation > 4%, perform a "Sub-node Re-scan" and fix the code.

## 📚 Implementation Guide

### Handling Large Data (The "Disovery-First Strategy")

**✅ Mandatory Workflow Order:**

1.  **Index**: Run `grep -r "type" figma-agent/data/` to classify files.
2.  **Locate Root**: Find the file containing the top-level Frame ID.
3.  **Keyword Safety Net**:
    - `grep -r "$1391" figma-agent/data/`
    - `grep -r "Rating" figma-agent/data/`
    - This bypasses random filenames and finds the exact data fragment needed.

### Example: Mapping Tokens

```tsx
// Using CSS Variables from tokens.json
const styles = {
  header: "bg-[var(--color-primary)] text-[var(--font-size-large)]",
};
```

## ✅ Completion & UI Validation

When finished, the agent **MUST**:

1.  **Mark the checklist** completed.
2.  **Provide a summary** of components created and file structure.
3.  **Confirm** that split data was used for better accuracy.

### 🎨 UI Verification Checklist (CRITICAL)

Before declaring completion, perform the following validation:

- [ ] **Visual Comparison**: Compare the generated UI against the original Figma design
  - Check layout structure (spacing, alignment, hierarchy)
  - Verify all components are present (buttons, inputs, cards, etc.)
  - Confirm text content matches exactly (no missing or incorrect labels)
- [ ] **Design Accuracy Audit**:
  - [ ] Colors match the design tokens (no color deviations)
  - [ ] Typography matches (font sizes, weights, line heights)
  - [ ] Spacing matches specifications (padding, margins, gaps)
  - [ ] Component states visible (hover, active, disabled states if applicable)
- [ ] **Content Completeness**:
  - [ ] All text nodes from `02-texts.json` are rendered
  - [ ] All images from `04-images.json` are displayed
  - [ ] All component instances are correctly linked
  - [ ] No placeholder content remains (e.g., "Lorem Ipsum", "[COMPONENT]")
- [ ] **Responsive Behavior** (if applicable):
  - [ ] Layout adapts correctly on different screen sizes
  - [ ] Mobile/tablet variations match design specifications
  - [ ] Navigation collapses/expands as designed
- [ ] **Accessibility & Code Quality**:
  - [ ] Semantic HTML structure is correct (h1-h4 hierarchy)
  - [ ] ARIA labels present where needed
  - [ ] No hard-coded values (all values from tokens)
  - [ ] TypeScript types properly defined

### Quality Criteria

**Acceptable Deviation**: ≤ 4% visual deviation

- **0-2%**: Minor spacing/sizing differences → Acceptable ✅
- **2-4%**: Small color tone differences, minor layout shifts → Acceptable with notes ⚠️
- **> 4%**: Missing components, wrong colors, incorrect text → FAILURE ❌ (Must be refactored)

If deviation > 4%, you **MUST**:

- Identify the problematic elements
- Re-scan the Figma data using grep for missing components
- Update the code to match the design precisely
- Re-validate until deviation ≤ 4%

### Final Validation Report

Provide a detailed report including:

```markdown
## Build Completion Report

**Status**: ✅ COMPLETE / ❌ NEEDS REVISION

### Components Built

- [x] Component Name (Lines: 50-100, File: components/ComponentName.tsx)
- [x] Component Name (Lines: 101-150, File: components/ComponentName.tsx)

### Design Accuracy

- Visual Deviation: 2.1% ✅
- Missing Elements: None
- Color Accuracy: 100% ✅
- Typography Match: 100% ✅

### Files Generated

- src/components/...
- src/styles/...
- src/types/...

### Notes

- All colors mapped from 05-colors.json
- Typography extracted from 02-texts.json
- Layout generated from split sections
- No hard-coded values used
```

## 🚀 Usage

**Example commands:**

- "Build the Footer component. Check file size first and split if needed."
- "Generate the Landing Page UI. Read summary → structure → sections for detailed implementation."
- "Create a Button component. Extract text from texts.json file."
- "Build the Header and verify it matches the Figma design pixel-perfectly."
