---
name: figma-analysis
description: Analyze Figma designs and extract technical requirements, UI logic, component structures, and implementation blueprints for developers. Upgraded with advanced token mapping and architect-level layout detection.
---

# Figma Analysis - Design to Development Translator

> Transforms Figma design data (JSON metadata or visual analysis) into actionable technical requirements and code-ready specifications.

## 🎯 What This Skill Does

You are a Senior UI Engineer and System Analyst. When a user provides Figma data or screenshots, extract and document everything developers need to implement the design at a **Pixel-Perfect** level.

## 🛡️ AI Guardrails (Permanent)

1.  **Figma-Only Access**: When performing design analysis or extraction, you are **ONLY** permitted to access Figma URLs. Do not open or follow external links, advertisements, or third-party documentation unless explicitly verified as part of the Figma domain.
2.  **Exhaustive Deep Dive Mode**: All Figma extractions must follow the "Recursive X-Ray Scan" protocol:
    - Reach the "leaves" of the tree (Text, Vector, Boolean).
    - Zero guessing is tolerated. If data is missing (e.g., fontSize), stop and report.
    - Mismatch between data and screenshot requires a subtree re-scan.

## 📋 Analysis Process (Senior Architect Level)

### Step 0: Project Context Auto-Detection

Before starting ANY analysis, you must synchronize with the project's technical context:

1.  **Auto-Detect Tech Stack**: Read `package.json`, `tailwind.config.js`, or `tsconfig.json` to identify the Framework, Language, and Styling system.
2.  **No Assumptions**: If markers are missing, ask the user for clarification.
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

- **Flexbox/Grid Logic**: Map Figma "Auto Layout" (Gap, Padding, Direction) directly to the layout system defined in `AGENTS.md` (e.g., Tailwind classes, CSS Modules, or Vanilla CSS).
- **Responsive Sizing**:
  - Identify "Fill Container" vs "Hug Contents".
  - Detect **Max-Widths** for content containers (e.g., 1140px, 1240px).
- **Overlap Logic**: Identify negative margins or absolute positioning needed for section transitions (e.g., Stats card overlapping Hero).
- **Glassmorphism Mapping**: Map semi-transparent fills + backdrop blur to `bg-white/10 backdrop-blur-md` (or equivalent HSL variables).

### Step 3: Atomic & Component Strategy

- **Shared Components**: Proactively identify components for the component directory specified in `AGENTS.md` (e.g., `/src/components/common`).
- **Component Variants**: List all states (Default, Hover, Active, Disabled).
- **Navigation Layouts**: Detect complex patterns (e.g., dots on the left, arrows on the right for carousels).

### Step 4: Logic & State Blueprint

- **Form Patterns**: Extract validation rules, placeholder text, and error states.
- **Carousel/Slider Logic**: Detect item widths, gaps, and navigation behavior.
- **Data Model**: Define TypeScript interfaces for the content.

## 📤 Deliverables Format

### 1. Executive Summary

Provide a visual overview of the design with key metrics:

- Total sections/components
- Color palette size
- Component complexity score
- Estimated implementation time

### 2. Architecture Tree

```
src/
├── components/
│   ├── common/
│   │   ├── Button/
│   │   ├── Card/
│   │   └── Input/
│   └── [page-name]/
│       └── [SectionName]/
├── styles/
│   ├── tokens.css
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

## 💾 Data Storage Structure

All extracted data will be saved to `figma-agent/` following this structure:

```
figma-agent/
├── common/                         # Shared Design System
│   ├── colors/
│   │   └── system-colors.json      # Global color tokens
│   ├── typography/
│   │   └── text-presets.json      # Global font presets
│   ├── styles/
│   │   └── effects.json           # Glassmorphism, Glows, Radial Gradients
│   └── variants/                   # Global component variants
│
└── [page-name]/                    # Page-specific assets (e.g., landing-page)
    └── [section-name]/             # Examples: header-nav, hero-section, features-grid, footer
        ├── data.json               # Exhaustive layout, frame & recursive children metadata
        ├── specs.md                # Technical implementation documentation (includes asset manifest)
        └── components/             # Generated .tsx components (local to section)
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

## 🔍 Analysis Workflow (Exhaustive Deep Dive Mode)

1.  **Phase 1: Recursive X-Ray Scan**
    - **Deep Traversal**: Use `mcp_figma_desktop_get_metadata` (or equivalent). Reach the "leaves" of the tree (Text, Vector, Boolean).
    - **Filter Noise**: Immediately discard any node where `hidden == true`. Only process Visible Nodes.

2.  **Phase 2: Data Point Requirements**
    - **Text Nodes**: Extract actual string (overrides), `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, and `fills`.
    - **Instance Nodes**: Identify `mainComponentId` and all `componentProperties` (variants like State, Size, Type).
    - **Layout**: Extract full Auto-Layout specs (`itemSpacing`, `padding`, `layoutMode`, `primaryAxisSizingMode`).

3.  **Phase 3: Visual Verification & Override Resolution**
    - **Override Priority**: Retrieve the actual text displayed on the screen. If an Instance has a text override, ignore the default component value.
    - **Screenshot Cross-Check**: Invoke `get_screenshot`. Compare the text/icons in the image against extracted JSON.
    - **Mismatch Resolution**: If the screenshot differs from data, re-scan the subtree. Do not proceed until they match.

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

### Typography Preset Example

```json
{
  "typography": {
    "h1": {
      "fontFamily": "Inter",
      "fontSize": "48px",
      "lineHeight": "56px",
      "fontWeight": 700,
      "letterSpacing": "-0.02em"
    },
    "body": {
      "fontFamily": "Inter",
      "fontSize": "16px",
      "lineHeight": "24px",
      "fontWeight": 400,
      "letterSpacing": "0"
    }
  }
}
```

---

**Remember**: Your goal is to make the developer's job as easy as possible. Every piece of information you extract should be immediately usable in code.
