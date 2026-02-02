---
name: figma-analysis
description: Analyze Figma designs and extract technical requirements, UI logic, component structures, and implementation blueprints for developers. Use when you need to translate Figma visuals into data.
version: "1.1.0"
license: MIT
compatibility: Requires FigmaAIBridge MCP or browser-based visual analysis capabilities.
metadata:
  author: "Antigravity Team"
  category: "Design-to-Code"
---

# Figma Analysis - Design to Development Translator

> Transforms Figma design data into actionable technical requirements. For deep technical rules, see [Technical Reference](references/REFERENCE.md).

## 🔍 Split Data Strategic Handling (New ⭐)

When working with split data, you must follow these rules to ensure < 1% deviation:

1.  **Node-ID Discovery**: Do not rely on filenames. Use `grep -r "NODE_ID"` to find which file fragment contains the data for a specific section.
2.  **Global Content Reconnaissance**:
    - **MANDATORY**: Locate the "Content Source of Truth" (the file containing the bulk of text overrides).
    - **Keyword Search**: search for strings visible in screenshots (e.g., "$1391", "Trending") in all `.json` files to find buried nodes.
3.  **Cross-Reference Mapping**: Resolve Style and Component IDs by scanning the entire `data/` directory, as they may be defined in any file fragment.
4.  **Visual Dominance Audit (Anti-Usage Count Bias)**:
    - **NEVER** assume the most frequent color is the background.
    - **MANDATORY**: Specifically identify the `fills` of the **Root Frame** or the largest **Rectangle** occupying > 80% of the screen area.
    - If a color has high usage count (e.g., White) but small area (e.g., Text), it is a **Foreground Token**.
    - If a color has low usage count (e.g., Dark Gray) but covers the entire background, it is the **Background Token**.

## 📋 Analysis Process (Senior Architect Level)

### Step 0: Project Context Auto-Detection

Before starting ANY analysis, you must synchronize with the project's technical context:

1.  **Read AGENTS.md First**: Always read `AGENTS.md` at the project root as the primary source of truth for the Framework, Language, Styling system, and coding standards.
2.  **Verify via Markers**: Reference `package.json`, `tailwind.config.js`, or `tsconfig.json` to confirm detected markers.
3.  **Context Overrides**: If an `.agent/context.json` or similar config exists within the `.agent` folder, use it as the source of truth for custom standards.

### Step 1: Design Token & "Magic Number" Extraction

- **Color Palettes**: Extract Hex/HSL. Identify brand-specific selection colors (`selection:bg-[...]`).
- **Advanced Typography**:
  - Don't just list font size. Capture **exact line-height** (e.g., 70px for H1, 30px for body).
  - Identify **letter-spacing** and **font-weights** (400, 500, 700).
  - **Font Mixing**: Detect the hierarchy between **Serif** (common for Agency/Creative headlines) and **Sans-Serif**.
- **Effect Tokens**:
  - Identify **Multi-layer shadows** (detect if a shadow has multiple spread/blur values).
  - Detect **Backdrop blurs** (glassmorphism: `backdrop-filter`, `opacity`).
  - **Glow Effects**: Identify inner glows or drop shadows used as light sources.
  - **Radial Lighting**: Look for large, semi-transparent radial gradients used as background "decorations" (Futuristic style).
  - **Organic Shapes**: Detect usage of large `border-radius` or blob-like background elements (Agency style).
- **Premium Spacing & Borders**:
  - Detect **Letter-spacing** adjustments (e.g., -1% to -2% for bold headings).
  - Identify **Negative margins** or absolute positioning for overlapping elements.
  - **Neon Borders**: Detect 1px borders with vibrant colors on dark backgrounds.
  - **Modern Brutalism**: Identify high-contrast borders and large, bold typography with minimal decoration.

### Step 2: Auto-Layout to CSS Mapping

- **Flexbox/Grid Logic**: Map Figma "Auto Layout" (Gap, Padding, Direction) directly to the layout system defined in `AGENTS.md`.
- **Architecture & UI Zone Detection**:
  - Identify **Page Content Zoninng**: Mapping layers to the `figma-agent/pages/[page-name]/[section-page]` structure.
  - Identify **App Shell** components: Fixed/Flex Sidebar, Topbar, and Main Content zones.
  - Detect **Scroll Containers**: Distinguish between page-level scroll and internal component scroll.
- **Responsive Sizing**: Identify "Fill Container" vs "Hug Contents".
- **Glassmorphism Mapping**: Map semi-transparent fills + backdrop blur to appropriate tokens.

### Step 3: Atomic & Component Strategy (Dashboard Focus)

- **Atomic Breakdown**: Proactively identify Atoms (Buttons, Badges) and Molecules (Chat bubbles, Table rows, Search bars).
- **State Analysis**: Detect and document variants for Hover, Active, and Selected states (crucial for sidebars).

### Step 4: Logic & State Blueprint

- **Data Models**: Define TypeScript interfaces for complex data structures like Users, Messages, or Project Tasks.
- **Navigation Hierarchy**: Map the relationship between Sidebar links and Page content.

## 📝 Planning Protocol (Sync with Development)

When analyzing, provide a structured plan following these phases:

1. **Phase 1: Deep Analysis**: Extraction of Tokens and Layout Mapping.
2. **Phase 2: Shell Architecture**: Defining the App Shell and global components.
3. **Phase 3: Atomic Build**: Building reusable components based on detected Atoms/Molecules.
4. **Phase 4: Composition**: Assembling full Dashboard views with Semantic HTML & H1-H4 hierarchy.
5. **Phase 5: Refinement**: Visual Audit and Micro-interaction validation.

## 📤 Deliverables Format

### 1. Executive Summary

Provide a visual overview of the design with key metrics:

- Total sections/components
- Color palette size
- Component complexity score
- Estimated implementation time

### 2. Architecture Tree (Code Structure)

```
src/
├── components/
│   ├── common/             # Global reusable components (from figma-agent/common/components)
│   │   ├── Button/
│   │   └── Input/
│   └── pages/              # Page-specific component components
│       └── [page-name]/    # Mapping to figma-agent/pages/[page-name]
│           └── [SectionPage]/
├── styles/
│   ├── tokens.css          # Mapped from figma-agent/common/
│   └── components.css
└── types/
    └── [page-name].types.ts
```

### 3. Comprehensive Token Table

#### Colors

| Token Name  | Value   | Usage       |
| ----------- | ------- | ----------- |
| primary-500 | #3B82F6 | Primary CTA |
| neutral-900 | #1F2937 | Headings    |

#### Typography

| Preset | Font  | Size | Line Height | Weight | Letter Spacing |
| ------ | ----- | ---- | ----------- | ------ | -------------- |
| H1     | Inter | 48px | 56px        | 700    | -0.02em        |
| Body   | Inter | 16px | 24px        | 400    | 0              |

#### Shadows

| Name        | Layers | CSS Value                                             |
| ----------- | ------ | ----------------------------------------------------- |
| card-shadow | 2      | 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06) |

### 4. State & Interaction Rules

```typescript
// Button States
interface ButtonStates {
  default: { bg: string; text: string; border?: string };
  hover: { bg: string; text: string; border?: string };
  active: { bg: string; text: string; border?: string };
  disabled: { bg: string; text: string; opacity: number };
}
```

### 5. Implementation Code Starter

Provide a code skeleton based on the tech stack in `AGENTS.md` (e.g., TSX, JSX, HTML) with:

- Proper semantic HTML
- Accessibility attributes
- Responsive styling
- Component interface/type definitions
- **Styling Best Practices**:
  - Follow the styling rules in `AGENTS.md`.
  - Prefer **HSL** for colors if the project supports it to handle transparency easily.
  - Implement borders and glassmorphism according to detected design style.

## 🏗️ Core Architecture (Core Standards)

To ensure the project is organized scientifically, all analysis data must comply with the following structure:

1.  **figma-agent/data/**: Stores synced design data from Figma (file structure, components, styles, tokens). This is the primary source of truth for the raw design data.
2.  **figma-agent/common/**: Stores general project-wide information (Colors, Typography, Effects, Shared Variants). This is the single "source of truth" for the Design System.
3.  **figma-agent/[section-name]/**: Directory containing detailed information about each Section (UI design zone) or Page within the project. Each section will have `data.json`, `specs.md`, and child components.

## 💾 Data Storage Structure

Extracted data will be saved to `figma-agent/` according to the following diagram:

```
figma-agent/
├── project.yaml                    # Tech Stack & Custom Rules
├── data/                           # Raw Figma sync data
│   ├── file-structure.json
│   ├── styles.json
│   └── components.json
│   └── *.json
|   |__ *.json
├── common/                         # Shared Design System
```

## 📝 data.json Schema

```json
{
  "sectionName": "Header",
  "nodeId": "123:456",
  "figmaUrl": "https://figma.com/file/...",
  "selection_link": "https://www.figma.com/design/XXXX/XXXX?node-id=123:456",
  "layout": {
    "grid": "...",
    "gap": 32,
    "padding": { "top": 20, "right": 40, "bottom": 20, "left": 40 },
    "direction": "horizontal",
    "alignment": "center",
    "justifyContent": "space-between"
  },
  "frame": {
    "width": 1440,
    "height": 80,
    "x": 0,
    "y": 0
  },
  "children": [
    {
      "type": "INSTANCE",
      "name": "Logo",
      "componentId": "456:789",
      "overrides": {
        "text": "MyBrand",
        "styles": {
          "fill": "#000000",
          "fontWeight": 700
        }
      }
    },
    {
      "type": "TEXT",
      "name": "Nav-Item",
      "content": "Products",
      "style": {
        "fontFamily": "Inter",
        "fontSize": 16,
        "lineHeight": "24px",
        "fontWeight": 500,
        "letterSpacing": "0",
        "color": "#374151"
      }
    }
  ],
  "vectors": [
    {
      "name": "Search-Icon",
      "nodeId": "789:012",
      "svgPath": "M10 10L20 20...",
      "dimensions": { "width": 24, "height": 24 }
    }
  ],
  "interactions": [
    {
      "trigger": "hover",
      "target": "Nav-Item",
      "action": "change-color",
      "value": "#1F2937"
    }
  ],
  "audit_status": "Verified",
  "last_updated": "2026-01-27T20:25:35+07:00",
  "extracted_by": "figma-analysis-skill"
}
```

## 💡 Response Guidelines

- ✅ Be precise with measurements (px, rem, %, etc.)
- ✅ Focus on "Developer Readiness" - every output should be ticket-ready
- ✅ Use clear Markdown formatting with tables and code blocks
- ✅ Include accessibility considerations (ARIA labels, keyboard navigation)
- ✅ Note responsive breakpoints if applicable (mobile: 375px, tablet: 768px, desktop: 1440px)
- ✅ Extract actual content (text, images) not just placeholders
- ✅ **Premium Details**: Capture exact `letter-spacing`, `border-width` (often 1px), and `backdrop-blur` values.
- ✅ Identify component instances and their overrides
- ✅ Map Figma constraints to CSS positioning
- ❌ Don't guess - if something is unclear, ask for clarification
- ❌ Don't skip animation/transition details if present
- ❌ Don't use generic descriptions - be specific with values
- ❌ Don't ignore edge cases or error states

## 🔄 When to Use This Skill

- User shares Figma link with `node-id` parameter
- User asks "implement this design" or "analyze this Figma file"
- User needs technical specs from mockups
- Converting design handoff to development tasks
- User runs `/figma-review` workflow

## ⚡ Handling Large Files & Performance

When dealing with complex Figma files (e.g., SaaS Dashboards with thousands of nodes), extraction can be slow. Apply these optimizations:

1.  **Reduce Initial Depth**: Use `--depth 1` or `2` for the initial `file-structure.json` to get the high-level layout quickly.
2.  **Targeted Extraction**: Always prefer extracting specific nodes using their `node-id` instead of full page sync.
3.  **Rate Limit Awareness**: The tool handles 429 errors automatically using `Retry-After`. Stay patient if you see "Rate Limited" logs.
4.  **Data Partitioning**: Split large pages into smaller logical "Sections" or "Components" to reduce JSON payload size and AI context usage.

## 🔍 Analysis Workflow (Exhaustive Deep Dive Mode - ELITE)

1.  **Phase 1: Recursive Part Assembly**
    - **Deep Traversal**: If data is split, assemble the full tree in memory by reading all `partX.json` files for the target node.
    - **Absolute Positioning Detection**: Specifically look for `layoutPositioning: "ABSOLUTE"`. These MUST be mapped to fixed/absolute CSS.
    - **Z-Index & Overlap**: Identify layer order. Items that overlap others based on bounding boxes are likely floating elements (e.g., Fixed Nav buttons).

2.  **Phase 2: Data Point Requirements (Zero-Loss)**
    - **Text Nodes**: Extract actual string, inclusive of pink-colored links, currency values, and ratings.
    - **Instance Logic**: Identify `mainComponentId` and all variants.
    - **Vector Detail**: Detect "STAR" icons or complex vectors and ensure they are flagged for export.

3.  **Phase 3: Visual Verification & Logic Audit**
    - **Ghost Element Check**: Compare your list of components against the screenshot.
    - **Background Verification**: Verify the primary Background Color by checking the Root Frame `fills`.
    - **Key Data Audit**: If the screenshot shows a price (e.g., "$1391"), search all text-containing JSON files for this value.
    - **Deviation Limit**: Your goal is < 4% deviation. If a major UI block is missing or the background color is incorrect, the analysis is incomplete.

4.  **Phase 4: Output Structure (JSON)**
    - Return a single, consolidated JSON object following the Figma hierarchy with full style and text overrides.

**Failure Handling Rules:**

- **Incomplete Data**: If a required property (e.g., `fontSize`) is missing, STOP and report immediately.
- **Unresolvable Override**: If after 3 recursive attempts data still doesn't match the screenshot, declare "Unresolvable Override" and list the affected Node ID.
- **No Fallbacks**: Never use "default" or "estimated" values. If you can't find it, report it.

## 🎨 Special Considerations

### Component Overrides

When analyzing component instances, always check for:

- Text overrides (actual displayed text vs. master component)
- Color overrides (fill, stroke)
- Size overrides (width, height constraints)
- Visibility overrides (hidden layers)

### Vector Extraction

For icons and illustrations:

- Extract as SVG when possible
- Note stroke width and color
- Identify if it's a component or raw vector
- Check for masks or clipping paths

### Responsive Behavior

Detect and document:

- Min/max width constraints
- Fill vs. Fixed sizing
- Responsive padding/margins
- Breakpoint-specific layouts

## 📚 Output Examples

### Color Token Example

```json
{
  "colors": {
    "brand": {
      "primary-50": "#EFF6FF",
      "primary-500": "#3B82F6",
      "primary-900": "#1E3A8A"
    },
    "neutral": {
      "50": "#F9FAFB",
      "900": "#111827"
    }
  }
}
```

### Directory Mapping Example (Dashboard Project)

figma-agent/
├── data/
│ ├── styles.json
│ └── components.json
│ └── \*.json
├── common/

### data.json (Section UI) Example

{
"sectionName": "sidebar-nav",
"pageContext": "dashboard",
"nodeId": "123:456",
"layout": {
"direction": "vertical",
"gap": 12,
"padding": { "left": 16, "right": 16 }
},
"children": [
{
"type": "INSTANCE",
"name": "Home-Link",
"overrides": { "text": "Dashboard", "active": true }
}
]
}

```

---

**Remember**: Your goal is to make the developer's job as easy as possible. Every piece of information you extract should be immediately usable in code.
```
