# Figma Agent Integration Tool

> 🎨 A comprehensive Figma-to-code extraction system for Antigravity, specifically designed for professional developer workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org)

## 🌟 Overview

**@cam/figma-agent-int** automatically transforms Figma designs into structured data and production-ready code. It covers the entire lifecycle of UI implementation:

- ✅ **Design Tokens** - Global colors, typography, and effects extraction.
- ✅ **Deep Data Extraction** - Exhaustive analysis of UI sections (Auto-layout, DOM, Overrides).
- ✅ **Code Generation** - Automated React/Next.js component building.
- ✅ **Metadata Tracking** - Selection links saved directly into your project for traceability.
- ✅ **Design-to-Code Audit** - Comparing code with Figma to reach pixel-perfection.

## 🚀 Antigravity Workflow (The 4-Step Pipeline)

This tool is optimized for **Antigravity**. Use these slash commands in your chat to move from design to code seamlessly.

### Step 1: Initialize Project Anatomy

**Command:** `/figma-review [figma_url]`

- **Action**: Establishes the `figma-agent/` directory.
- **Result**: Extracts global colors, typography, and basic section skeletons (`specs.md`).

### Step 2: Exhaustive Deep Dive

**Command:** `/get-figma-info [section_name] [selection_link]`

- **Action**: Bypasses default component data to capture actual overrides and pixel-precise layout.
- **Result**: Populates `figma-agent/[page]/section-[name]/data.json`.

### Step 3: Architect the Code

**Command:** `/figma-build [section_name] [link selection]`

- **Action**: Triggers the `figma-to-code` AI architect.
- **Result**: Generates a professional React/Next.js component in your project files.

### Step 4: Pixel-Perfect Audit

**Command:** `/figma-audit [section_name] [link selection]`

- **Action**: Compares your code against the latest Figma selection.
- **Result**: Refinement plan to fix spacing, tokens, or content mismatches.

## 💻 Developer Integration Guide

Once tokens and metadata are extracted into `figma-agent/`, you can integrate them into your code manually or via automation.

### Using Global Tokens (Tailwind Example)

In your `tailwind.config.js`:

```javascript
const colors = require("./figma-agent/common/colors/system-colors.json");

module.exports = {
  theme: {
    extend: {
      colors: colors.brand, // Automatically use Figma colors
    },
  },
};
```

### Manual Component Implementation

The `data.json` provides everything you need to build custom components:

```tsx
import headerData from "./figma-agent/landing-page/section-header/data.json";

const Header = () => {
  const { padding, gap } = headerData.layout;
  return (
    <header style={{ padding: `${padding.top}px`, gap: `${gap}px` }}>
      {/* Build UI based on Figma DOM tree */}
    </header>
  );
};
```

---

## 📁 Standardized Directory Structure (`figma-agent/`)

The tool organizes data following a clean, scalable architecture:

```
figma-agent/
├── common/                         # Shared Design System
│   ├── colors/
│   │   └── system-colors.json      # Global color tokens
│   ├── typography/
│   │   └── text-presets.json      # Global font presets
│   └── variants/                   # Global component variants
│
└── [page-name]/                    # Page-specific assets
    └── section-[name]/
        ├── data.json               # Exhaustive layout & children metadata
        ├── specs.md                # Technical implementation documentation
        ├── components/             # Generated .tsx components
        └── images/                 # Downloaded SVG/PNG assets
```

## 📚 Documentation & Reference

- **[Installation Guide](INSTALL.md)** - Connectivity and setup.
- **[Quick Reference](QUICK_REFERENCE.md)** - Command cheat sheet.
- **[Project Hub](DOCS_INDEX.md)** - Documentation index.

---

**Built with ❤️ for Antigravity Developers**  
_Inspired by professional design-to-code specifications._
