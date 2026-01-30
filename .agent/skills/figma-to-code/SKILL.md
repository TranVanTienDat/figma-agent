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

1.  **MANDATORY: Extensive Context Reading**: Before starting ANY code generation, the agent MUST read `figma-agent/config.yaml` and the content of the split data directories in `figma-agent/*` (starting with `00-summary.json`). Valid data is now split into multiple focused files (summary, structure, texts, etc.) for better accuracy.
2.  **Core Architecture Compliance**: All design data and configurations are centralized in the `figma-agent/` directory.
3.  **Token System**: Build the variable system by reading `05-colors.json` (for color palette) and `02-texts.json` (for typography styles) located in the split data directory. Do NOT look for a single `tokens.json`.
4.  **Component Reuse**: Check `03-instances.json` in the split directory to identify component instances. If a node matches a known design system component, use the shared component instead of rebuilding it.
5.  **Compliance**: Strictly adhere to the Framework, Language, and Styling system specified in `figma-agent/config.yaml`.
6.  **No Assumptions**: Never hard-code technologies. If a configuration is missing in `config.yaml`, ask the user for clarification.

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

- **CSS Design System**: Setup `globals.css` or equivalent with CSS Variables based on tokens.
- **App Shell Implementation**: Build the high-level layout structure (Sidebar, Navigation, Information Zones) with pixel-perfect precision.

### Phase 3: Atomic Component Build

- **Atoms**: Construct basic elements (Buttons, Inputs, Icons, Badges).
- **Molecules**: Build complex components like Chat Items, List items, or Search bars.
- **Note**: Every component must support required states (Hover, Active) as defined in `specs.md`.

### Phase 4: View Assembly & Integration

- **Page Composition**: Assemble the full views by placing components into the App Shell.
- **Heading & SEO Audit**: Apply the semantic structure and H1-H4 hierarchy across the assembled pages.

### Phase 5: Interaction & Refinement

- **Micro-interactions**: Implement animations for sidebar toggles, dropdowns, and notifications.
- **Visual Audit**: Perform a screenshot comparison between the code and Figma to ensure 100% fidelity.

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
