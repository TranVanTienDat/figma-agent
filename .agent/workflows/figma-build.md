---
description: Generate React/Next.js code from Figma data with automatic large file optimization
---

# Figma Build Workflow

This workflow converts your synced Figma design data into production-ready React/Next.js code, with built-in optimization for large files.

## Prerequisites

- The `figma-agent/project.yaml` must contain the correct project context (Tech Stack, Styling, etc.).
- The `figma-agent/data/` directory must contain the synced design data (ALL JSON files).
- **CRITICAL**: All JSON files in `figma-agent/data/` and subdirectories MUST be read without exception.

## 🛠️ Technical Requirements

### 0. CRITICAL: No Files Will Be Skipped ⭐⭐⭐

- **RULE #1**: Every `.json` file in `figma-agent/data/` directory MUST be read
- **RULE #2**: Every `.json` file in subdirectories (e.g., `sections/`, `target-node-split/`) MUST be read
- **RULE #3**: No file naming convention determines if a file is skipped - ALL files are processed
- **RULE #4**: If a file exists in the data directory, it will be included in the analysis

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

> **Note**: File splitting is already handled in the `sync-figma-data` workflow. Proceed directly to Phase 2: Analysis & Building.

## 🤖 AI Processing Order for Split Data (CRITICAL FOR ACCURACY)

**READ FILES IN THIS EXACT ORDER TO AVOID BUILD ERRORS:**

### 0️⃣ **Design Images** ⭐⭐⭐⭐⭐ (START HERE - VISUAL REFERENCE)

- **Location**: `figma-agent/data/images/*`
- **Content**: PNG/SVG design screenshots
- **Purpose**: Visual reference for what needs to be built
- **Action**:
  - Open each design image to understand layout, colors, typography
  - Take mental notes of: spacing, colors, text content, components
  - This is your ground truth for validation later

### 1️⃣ **`00-summary.json`** ⭐⭐⭐ (START HERE)

- **Content**: Statistics, node counts, colors, sections overview
- **Purpose**: Get bird's eye view of the entire design
- **Action**: Extract `statistics` (total_nodes, text_nodes, component_instances), `top_colors`, `sections` list

### 2️⃣ **`01-structure.json`** ⭐⭐ (UNDERSTAND HIERARCHY)

- **Content**: Hierarchical tree (3 levels deep)
- **Purpose**: Understand component organization and nesting
- **Action**: Map the structure tree, identify root frames and child components

### 3️⃣ **`02-texts.json`** ⭐⭐ (GET ALL TEXT CONTENT)

- **Content**: All text nodes with styles and content
- **Purpose**: Know what text labels, prices, descriptions, etc. are needed
- **Action**: Extract all text content and associate with components

### 4️⃣ **`03-instances.json`** ⭐⭐ (FIND COMPONENTS)

- **Content**: All component instances and their references
- **Purpose**: Identify which components are used and where
- **Action**: Map component instances to master components

### 5️⃣ **`04-images.json`** ⭐ (REFERENCE IMAGES)

- **Content**: Image and icon nodes
- **Purpose**: Know which assets need to be handled
- **Action**: List all images/icons that need to be imported

### 6️⃣ **`05-colors.json`** ⭐⭐⭐ (MAP COLOR TOKENS)

- **Content**: Complete color palette with usage counts
- **Purpose**: Create design tokens and color system
- **Action**: Create color variables and map to theme

### 7️⃣ **`sections/*.json`** ⭐⭐⭐⭐ (DIVE INTO DETAILS - DO THIS FOR EACH SECTION)

- **Content**: Individual section data (200-300 lines each)
- **Purpose**: Get detailed properties for each component
- **Action**: Read all section files in order, extract fills, strokes, typography, layout

### 8️⃣ **`99-full-tree.json`** ⭐ (LAST RESORT ONLY)

- **Content**: Complete raw Figma node tree
- **Purpose**: Backup if you need all details
- **Action**: Only read if `sections/*.json` doesn't have needed info

---

**⚠️ IMPORTANT: Do NOT skip to step 7 (sections). Follow order 1-6 first!**

**✅ Build Path**: `00-summary → 01-structure → 02-texts → 03-instances → 04-images → 05-colors → sections/ → build`

---

## ⚠️ CRITICAL: UI Review & Visual Validation

**THIS STEP IS NOT OPTIONAL - YOU MUST DO THIS AFTER EVERY BUILD**

### Build → Compare → Fix Loop

After building UI, you **MUST**:

1. **Compare generated UI against original design image** (from `figma-agent/data/images/`)
2. **Identify any visual differences** (color, spacing, text, components)
3. **Fix all issues** until UI matches design image exactly
4. **Re-validate** against original image again

```
┌─────────────────────────────────────────────────────┐
│ 1. Build component from image + JSON data           │
├─────────────────────────────────────────────────────┤
│ 2. Open original design image from:                 │
│    figma-agent/data/images/[design-image].png       │
├─────────────────────────────────────────────────────┤
│ 3. Place side-by-side: Generated UI ↔ Design Image  │
├─────────────────────────────────────────────────────┤
│ 4. Compare visually:                                 │
│    ✅ Colors match?                                  │
│    ✅ Spacing/padding correct?                       │
│    ✅ Text content matches?                          │
│    ✅ All components present?                        │
│    ✅ Typography correct (size/weight)?              │
├─────────────────────────────────────────────────────┤
│ 5a. NO DIFFERENCES → ✅ DONE                         │
│ 5b. FOUND DIFFERENCES → Fix code → Go to step 2     │
└─────────────────────────────────────────────────────┘
```

### Post-Build Visual Validation (MANDATORY)

After code generation, perform these checks **using design images as reference**:

#### Step 1: Visual Comparison Scan (vs Design Image)

```bash
# Open the design image for reference
open figma-agent/data/images/[design-image-filename].png
```

Then check:

- [ ] **Layout & Spacing**: Does generated layout match image spacing exactly?
- [ ] **All Components Present**: Every button/input/card in image is in your code?
- [ ] **Text Content**: Text labels match image exactly (no missing text)?
- [ ] **Images/Icons**: All images from design are displayed?
- [ ] **Colors**: Background, text, borders match design image colors?

#### Step 2: Detailed Comparison

Compare these specific elements:

1. **Visual Layout** (compare to image)
   - [ ] Spacing/padding matches image
   - [ ] Alignment (left/center/right) same as image?
   - [ ] Element positions correct?

2. **Colors** (compare to image)
   - [ ] Background color matches image?
   - [ ] Text color matches image?
   - [ ] Button/accent colors match image?
   - [ ] Border colors accurate?

3. **Typography** (compare to image)
   - [ ] Text content matches image exactly?
   - [ ] Font size looks right (compare pixel sizes)?
   - [ ] Font weight correct (bold/regular)?
   - [ ] Line height/spacing correct?

4. **Components** (compare to image)
   - [ ] All buttons in image are present in code?
   - [ ] All input fields in image are present?
   - [ ] Cards/containers match image structure?
   - [ ] Icons/images displayed correctly?

#### Step 3: Error Detection (Find What's Wrong)

If UI doesn't match image, identify the issue:

- ❌ **Color mismatch**: Wrong RGB/hex value
- ❌ **Spacing mismatch**: Padding/margin too large/small
- ❌ **Missing element**: Component not in code
- ❌ **Wrong text**: Text content doesn't match image
- ❌ **Wrong layout**: Element positioned incorrectly
- ❌ **Wrong size**: Component too large/small

#### Step 4: Fix Issues

For each difference found:

```
1. Identify problem
   ↓
2. Find root cause (check data vs code)
   ↓
3. Update component code
   ↓
4. Re-compare with image
   ↓
5. Match? → Next component : Back to step 1
```

Example fix:

```tsx
// BEFORE (Wrong - doesn't match image)
<div className="bg-red-500 p-4">  {/* Wrong color! */}
  {text}
</div>

// AFTER (Fixed - matches image)
<div className="bg-blue-600 p-8">  {/* Now matches image! */}
  {text}
</div>
```

#### Step 5: Re-validate

```bash
# After fixing all issues:
# 1. Regenerate/rebuild component
# 2. Open design image again
# 3. Compare side-by-side with generated UI
# 4. Confirm: Does it match now?
```

### Quality Criteria (vs Design Image)

**Target**: UI matches design image exactly (≤ 4% deviation)

- **0-2%**: Minor spacing/sizing differences → ✅ ACCEPTABLE
- **2-4%**: Small color tone differences, minor layout shifts → ⚠️ ACCEPTABLE WITH NOTES
- **> 4%**: Missing components, wrong colors, incorrect text → ❌ FAILURE (MUST FIX)

### Common Issues to Watch For

| Issue                    | How to Fix                                        |
| ------------------------ | ------------------------------------------------- |
| Colors don't match image | Check hex value in styles.json, update CSS class  |
| Spacing wrong vs image   | Adjust padding/margin to match image measurements |
| Text missing or wrong    | Check images-manifest.json, verify text content   |
| Component missing        | Check component was added to JSX                  |
| Wrong layout vs image    | Verify flexbox/grid setup matches image structure |

## 🚀 Usage

**Example commands:**

- "Build the Footer component. Check file size first and split if needed."
- "Generate the Landing Page UI. Read summary → structure → sections for detailed implementation."
- "Create a Button component. Extract text from texts.json file."
- "Build the Header and verify it matches the Figma design pixel-perfectly."
