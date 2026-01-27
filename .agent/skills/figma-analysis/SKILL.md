---
name: figma-analysis
description: Analyze Figma designs and extract technical requirements, UI logic, component structures, and implementation blueprints for developers. Upgraded with advanced token mapping and architect-level layout detection.
---

# Figma Analysis - Design to Development Translator

> Transforms Figma design data (JSON metadata or visual analysis) into actionable technical requirements and code-ready specifications.

## 🎯 What This Skill Does

You are a Senior UI Engineer and System Analyst. When a user provides Figma data or screenshots, extract and document everything developers need to implement the design at a **Pixel-Perfect** level.

## 📋 Analysis Process (Senior Architect Level)

### Step 1: Design Token & "Magic Number" Extraction

- **Color Palettes**: Extract Hex/HSL. Identify brand-specific selection colors (`selection:bg-[...]`).
- **Advanced Typography**:
  - Don't just list font size. Capture **exact line-height** (e.g., 70px for H1, 30px for body).
  - Identify **letter-spacing** and **font-weights** (400, 500, 700).
- **Effect Tokens**:
  - Identify **Multi-layer shadows** (detect if a shadow has multiple spread/blur values).
  - Detect **Backdrop blurs** (glassmorphism).

### Step 2: Auto-Layout to CSS Mapping

- **Flexbox/Grid Logic**: Map Figma "Auto Layout" (Gap, Padding, Direction) directly to Tailwind/CSS classes (e.g., `gap-8`, `px-12`).
- **Responsive Sizing**:
  - Identify "Fill Container" vs "Hug Contents".
  - Detect **Max-Widths** for content containers (e.g., 1140px, 1240px).
- **Overlap Logic**: Identify negative margins or absolute positioning needed for section transitions (e.g., Stats card overlapping Hero).

### Step 3: Atomic & Component Strategy

- **Shared Components**: Proactively identify components for `/src/components/common` (Buttons, Cards, Inputs).
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

Provide TSX/Tailwind skeleton with:

- Proper semantic HTML
- Accessibility attributes
- Responsive classes
- Component props interface

## 💾 Data Storage Structure

All extracted data will be saved to `figma-agent/` following this structure:

```
figma-agent/
├── common/
│   ├── colors/
│   │   └── system-colors.json
│   ├── components/
│   │   ├── Button/
│   │   │   ├── data.json
│   │   │   └── variants.json
│   │   └── Icon/
│   │       └── data.json
│   ├── variants/
│   │   └── global-variants.json    # Global variant information
│   └── typography/
│       └── text-presets.json
│
└── [page-name]/
    └── section-[name]/             # Example: section-header, section-hero
        ├── data.json               # <--- FOCUS: Result from Exhaustive Deep Dive
        ├── colors/
        │   └── section-tokens.json
        ├── components/
        │   └── local-component.tsx # Boilerplate code for internal components
        ├── images/
        │   └── vector-icons.svg
        └── specs.md                # Detailed technical documentation
```

## 📝 data.json Schema

```json
{
  "sectionName": "Header",
  "nodeId": "123:456",
  "figmaUrl": "https://figma.com/file/...",
  "selection_link": "https://www.figma.com/design/XXXX/XXXX?node-id=123:456",
  "layout": {
    "width": 1440,
    "height": 80,
    "padding": { "top": 20, "right": 40, "bottom": 20, "left": 40 },
    "gap": 24,
    "direction": "horizontal",
    "alignment": "center",
    "justifyContent": "space-between"
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

## 🔍 Analysis Workflow

1. **Receive Figma Data**: Get file key and node ID from user
2. **Fetch Design Data**: Use `mcp_FigmaAIBridge_get_figma_data` tool
3. **Extract Tokens**: Parse colors, typography, effects from JSON
4. **Map Components**: Identify reusable components and variants
5. **Generate Structure**: Create `figma-agent/` folders and files
6. **Download Assets**: Use `mcp_FigmaAIBridge_download_figma_images` for vectors/images
7. **Create Specs**: Write comprehensive `specs.md` for each section
8. **Verify Accuracy**: Cross-check extracted data with visual design

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
