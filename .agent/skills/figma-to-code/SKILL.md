---
name: figma-to-code
description: Expert in converting figma-agent data into professional React/Next.js code according to industry standards. Use when you have analysis data in the figma-agent directory.
version: "1.1.0"
license: MIT
compatibility: Designed for modern React/Next.js environments. Requires prior execution of figma-analysis.
metadata:
  author: "Antigravity Team"
  category: "Code-Generation"
---

# Figma to Code - Development Architect

> Senior Frontend Engineer translating design data into pixel-perfect code. See [Technical Reference](references/REFERENCE.md) for style guides and accessibility rules.

## 🏗️ Core (Core System)

1.  **MANDATORY: Extensive Context Reading**: Before starting ANY code generation, the agent MUST read `figma-agent/project.yaml` and the content of the split data directories.
2.  **Zero-Guessing Policy**: If a property like `layoutPositioning: "ABSOLUTE"` is found, the agent **MUST** calculate its position relative to the main container and apply `fixed` or `absolute` positioning.
3.  **Global Search Integration**: If a UI element is visible in the design (e.g., Star Ratings, floating "Prev/Next" buttons) but missing in the primary section JSON, the agent **MUST** grep the entire `figma-agent/data/` directory for that element's label to find its actual data.
4.  **Token System**: Build the variable system by reading `05-colors.json` and `02-texts.json`. Any hex code found in `data.json` should be matched against `05-colors.json` to see if a variable exists.
5.  **Compliance**: Strictly adhere to the tech stack in `project.yaml`. Handle special cases like `text-decoration: line-through` for prices.

## 📋 Requirements (Technical Standards)

1.  **Pixel-Perfect Implementation**: Achieve 0px deviation in spacing and sizing. Use `figma-analysis` data for exact measurements.
2.  **Rational Structure & Modularity**: Follow **Atomic Design** principles (Atoms -> Molecules -> Organisms). Ensure components are reusable and logically separated.
3.  **SEO & Accessibility (A11y)**:
    - Use semantic HTML5 elements (`<aside>`, `<main>`, `<nav>`, `<header>`, etc.).
    - Proper Heading Hierarchy (H1-H4) reflecting content importance (e.g., H1 for page titles, H2 for section headers).
    - Implement ARIA labels, alt text, and proper focus states for keyboard navigation.
4.  **Handling Overrides**: Prioritize actual user content from the `overrides` section in `data.json`.

## 🎯 Goals (Project Objectives)

1.  **Figma Mirroring**: The resulting code must be a perfect "mirror" of the design in terms of Layout (Flex/Grid), Color (Hex/HSL), and Typography.
2.  **Dashboard/SaaS Excellence**: For dashboard projects, focus on high-density information layout, complex navigation (sidemaps/topbars), and data-driven components (tables, chat streams).
3.  **Interaction Fidelity**: Implement all variants (Hover, Active, Selected, Disabled) with smooth transitions.

## 📝 Planning (Implementation Roadmap)

### Phase 1: Deep Design Analysis

- **Token Sync**: Extract color codes, font presets, and shadow/border-radius tokens using `figma-analysis`.
- **Layout Mapping**: Identify the primary App Shell (Sidebar + Main Content + Topbar) and sub-layouts (Flex/Grid).
- **Pattern Identification**: Identify repeating patterns (Avatars, Status Badges, Table Rows, Chat Bubbles).

### Phase 2: Foundation & Shell

- **Step 1: Read Project Context (MANDATORY)**:
  - Read `figma-agent/project.yaml` → Section **"techStack"** → Field **"styling"**.
  - Identify the styling system: `CSS`, `Tailwind`, `MUI`, `Joy UI`, `Styled Components`, `Emotion`, etc.
- **Step 2: Setup Design Tokens (Based on Detected System)**:
  - **If Styling = "CSS" or "CSS Modules"**:
    - Create `src/styles/globals.css` or `src/styles/tokens.css`.
    - Map colors from `05-colors.json` to CSS Variables (e.g., `--color-primary: #d82255;`).
    - Map typography from `02-texts.json` to CSS Variables (e.g., `--font-heading: 'Manrope', sans-serif;`).
  - **If Styling = "Tailwind"**:
    - Extend `tailwind.config.js` → `theme.extend.colors` with tokens from `05-colors.json`.
    - Add custom fonts to `theme.extend.fontFamily` from `02-texts.json`.
    - Add spacing/shadows if needed.
  - **If Styling = "MUI" or "Joy UI"**:
    - Create `src/theme.ts` or `src/styles/theme.ts`.
    - Map Figma tokens to MUI/Joy theme structure: `palette.primary.main`, `typography.h1.fontFamily`, etc.
  - **If Styling = "Styled Components" or "Emotion"**:
    - Create `src/styles/theme.ts` with a theme object.
    - Wrap the app with `<ThemeProvider theme={theme}>`.

- **Step 3: App Shell Implementation**:
  - Build the high-level layout structure (Sidebar, Navigation, Information Zones) with pixel-perfect precision using the detected styling system.

### Phase 3: Atomic Component Build

- **Atoms**: Construct basic elements (Buttons, Inputs, Icons, Badges).
- **Molecules**: Build complex components like Chat Items, List items, or Search bars.
- **Note**: Every component must support required states (Hover, Active) as defined in `specs.md`.

### Phase 4: View Assembly & Integration

- **Page Composition**: Assemble the full views by placing components into the App Shell.
- **Heading & SEO Audit**: Apply the semantic structure and H1-H4 hierarchy across the assembled pages.

### Phase 5: Interaction & Refinement

- **Absolute Element Alignment**: Audit all elements that were marked as "ABSOLUTE" in Figma. Ensure they are correctly placed using `left`, `right`, `top`, or `bottom` with proper z-index.
- **Fidelity Audit**: Check for missing "Micro-details" (e.g., star ratings, small links like "Watch videos", pink link colors, price strike-throughs).
- **Visual Audit**: Perform a screenshot comparison. If deviation is > 4% (missing buttons, wrong prices, wrong positioning), the build is considered a FAILURE and must be refined.

## 📚 Implementation Examples

### 1. Mapping Tokens to CSS (from `data/`)

```css
/* src/styles/tokens.css */
:root {
  /* Values sourced from figma-agent/data/tokens.json */
  --color-primary: #ff3b30;
  --color-bg-dashboard: #f8f9fa;

  /* Typography presets from tokens.json */
  --font-h1: 700 32px/40px "Inter", sans-serif;
}
```

### 2. Building a UI Component (from `figma-agent/[section-name]`)

```tsx
// src/components/Sidebar.tsx
// Uses layout from figma-agent/sidebar/data.json
import { Button } from "../../common/Button"; // Reusing common atoms

export const Sidebar = () => {
  return (
    <aside className="w-[280px] h-full flex flex-col gap-3 p-4 bg-white border-r">
      <h2 className="text-lg font-bold">Menu</h2>
      <nav className="flex flex-col gap-2">
        {/* Mapping instances found in parsed data.json */}
        <Button variant="ghost" label="Dashboard" active />
        <Button variant="ghost" label="Settings" />
      </nav>
    </aside>
  );
};
```

## 📤 Output Standards

- **Clean Code**: No hard-coded values; use the established token system.
- **Responsiveness**: Ensure the layout adapts correctly (e.g., Sidebar collapsing on smaller screens).
- **Type Safety**: Use TypeScript interfaces for all component props where applicable.
