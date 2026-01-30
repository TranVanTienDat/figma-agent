---
description: Generate React/Next.js code from Figma data with automatic large file optimization
---

# Figma Build Workflow

This workflow converts your synced Figma design data into production-ready React/Next.js code, with built-in optimization for large files.

## Prerequisites

- The `figma-agent/config.yaml` must contain the correct project context (Tech Stack, Styling, etc.).
- The `figma-agent/data/` directory must contain the synced design data.
- The `split_node_data.py` script must be available in `.agent/skills/figma-analysis/scripts/`.

## 🛠️ Technical Requirements

### 1. Data Processing Standards (New ⭐)

- **Large File Detection**: Automatically check if JSON files exceed 1000 lines.
- **Recursive Splitting**: Use `split_node_data.py` to break large files into manageable chunks (200-300 lines).
- **Context Prioritization**: Always prioritize reading split files (`summary.json`, `sections/*.json`) over raw monolithic files.

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

### Phase 2: Analysis & Building (Strict Order)

- [ ] **Step 1: Read Summary** (`00-summary.json`)
  - Understand total size, sections, and complexity.
- [ ] **Step 2: Read Structure** (`01-structure.json`)
  - Create the skeleton component (index.tsx) and plan sub-components (Header, FooterList, etc.).
- [ ] **Step 3: Build Sections** (Iterate `sections/*.json`)
  - **CRITICAL**: Read one section file at a time.
  - Build the corresponding sub-component with pixel-perfect precision.
- [ ] **Step 4: Inject Content** (`02-texts.json`)
  - Populate text content from the extracted list.
- [ ] **Step 5: Apply Styles** (`05-colors.json`)
  - Configure Tailwind/CSS variables based on collected colors.

### Phase 3: Implementation

- [ ] **Code Generation**: Write JSX/TSX incrementally section by section.
- [ ] **Review**: Audit generated code against design specs.

## 📚 Implementation Guide

### Handling Large Data (The "Split Strategy")

**⛔ DO NOT** read `99-full-tree.json` (unless absolutely necessary for debugging).

**✅ Recommended Reading Order:**

1.  **Overview**: `cat 00-summary.json` → "I am building a Footer with 5 columns."
2.  **Skeleton**: `cat 01-structure.json` → "I need a grid layout with these wrapper divs."
3.  **Detailing**:
    - `cat sections/frame_1.json` → "Building Column 1..."
    - `cat sections/frame_2.json` → "Building Column 2..."
4.  **Content**: `cat 02-texts.json` → "Filling text..."
5.  **Polishing**: `cat 05-colors.json` → "Fixing colors..."

### Example: Mapping Tokens

```tsx
// Using CSS Variables from tokens.json
const styles = {
  header: "bg-[var(--color-primary)] text-[var(--font-size-large)]",
};
```

## ✅ Completion

When finished, the agent **MUST**:

1.  **Mark the checklist** completed.
2.  **Provide a summary** of components created.
3.  **Confirm** that split data was used for better accuracy.

## 🚀 Usage

**Example commands:**

- "Build giúp tao cái Footer này. Nhớ check size và split trước."
- "Dựng UI Landing Page. Đọc file summary -> structure -> sections để code chi tiết."
- "Code component Button. Lấy text từ file texts.json."
