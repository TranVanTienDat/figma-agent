# Figma Agent Integration Tool

> 🎨 A comprehensive Figma-to-code extraction system for Antigravity, specifically designed for professional developer workflows.

## 🌟 Overview

**@cam/figma-agent** automatically transforms Figma designs into structured data and production-ready code. It covers the entire lifecycle of UI implementation:

- ✅ **Graph-First Architecture** - Extracts deep node trees with full layout precision.
- ✅ **Design Tokens Support** - Resolves Figma Variables (Enterprise) & Styles to proper CSS/Tailwind variables.
- ✅ **Surgical Data Extraction** - Fetches only the section you need, ensuring speed and reliability.
- ✅ **Data Enrichment** - Automatically maps complex Figma IDs to human-readable names and semantic tokens.

## ⚙️ Quick Start

### 1. Installation

```bash
npm install -g @ckim03/figma-agent
```

### 2. Initialize Project

To add Figma-to-Code capabilities to your current project, simply run:

```bash
figma-agent
```

_This command will copy the necessary AI Skills and **Core Scripts** into your project folder `.agent/`._

### 3. Setup Project Context

**Action**: Read `AGENTS.md` in the project root.

- **Why**: To ensure analysis respects your project-specific tech stack and coding conventions.

---

## 🚀 Antigravity Workflow (The New Standard)

This tool is optimized for **Antigravity**. Use these slash commands in your chat to move from design to code seamlessly.

### Phase 1: Foundation (Sync)

**Command:** `/sync-figma-data`

- **Action**: Fetches the File Structure, Component Library, and Raw Styles.
- **Output**: Populates `figma-agent/data/` with the design system DNA.

**Command:** `/figma-map-tokens`

- **Action**: Converts raw styles into a usable `tokens.json` map.
- **Output**: `figma-agent/data/tokens.json`.

### Phase 2: Implementation (Deep Dive)

**Command:** `python3 .agent/skills/figma-analysis/scripts/figma_cli.py nodes <KEY> <ID>`

- **Action**: Extracts pixel-perfect layout data for a specific UI section.
- **Result**: A clean, enriched JSON file ready for AI code generation.

---

## 💻 Developer Integration

### Integrating Tokens (Tailwind)

In your `tailwind.config.js`:

```javascript
const tokens = require("./figma-agent/data/tokens.json");

module.exports = {
  theme: {
    extend: {
      colors: tokens.colors, // Automagically mapped from Figma
      fontFamily: tokens.typography,
    },
  },
};
```

### Generating Code

Once you have extracted the data for a Node (Phase 2), simply ask the Agent:

> "Build the 'Header' component using `figma-agent/pages/header/data.json`. Use the tokens from `figma-agent/data/tokens.json`."

---

## 📁 Directory Structure

```
figma-agent/
├── data/                       # 🟢 The Source of Truth
│   ├── file-structure.json     # Overview of Pages/Frames
│   ├── components.json         # Component Library
│   ├── styles.json             # Raw Styles
│   └── tokens.json             # Processed Token Map (Ready for Dev)
│
└── pages/                      # 🟡 Implementation Details
    └── [page-name]/
        └── [section-name]/
            └── data.json       # Deep extract of a specific UI part
```

---

**Built with ❤️ for Antigravity Developers**  
_Powered by the new Graph-First Core Architecture._
