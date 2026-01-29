# Antigravity Figma Workflow

This document outlines the standard operating procedures for the new "Graph-First" Figma Agent.

## 🌟 The Core Philosophy

Instead of guessing, we **extract**. This workflow separates data retrieval from code generation, ensuring higher accuracy and stability.

---

## 🚀 Phase 1: data Extraction (The Foundation)

_Goal: Get the raw materials (Styles, Components, Images) locally._

### 1. Sync Figma Data

**Command:** `/sync-figma-data`

- **Input**: `<FILE_KEY>` (from your Figma URL)
- **Action**:
  - Fetches File Structure (Pages/Frames overview).
  - Fetches Published Component Library.
  - Fetches Design Tokens (Styles & Variables).
- **Output**: Populates `figma-agent/data/` with JSON files.

### 2. Map Design Tokens

**Command:** `/figma-map-tokens`

- **Input**: None (Uses data from step 1)
- **Action**:
  - Analyzes `styles.json` and `variables.json`.
  - Creates a `tokens.json` map resolving IDs to semantic names (e.g., `style:123` -> `colors.primary`).
- **Output**: `figma-agent/data/tokens.json`.

---

## 🛠️ Phase 2: Design-to-Code (Deep Dive)

_Goal: Build a specific part of the UI._

### 3. Extract Section Data

**Command:** `python3 .agent/skills/figma-analysis/scripts/figma_cli.py nodes <FILE_KEY> <NODE_IDS>`

- **Input**: The Node IDs of the section you want to build (e.g., `1:2`).
- **Action**:
  - Fetches deep, recursive details of the node.
  - Enriches data with resolved tokens (automagically converts hex codes to variables).
- **Output**: Detailed JSON for that specific component.

### 4. Generate Code

**Action**: (Manual Agent Request)

- "Build the component in `data.json` using TailwindCSS."
- The Agent reads the enriched JSON and maps it to the tokens we established in Phase 1.

---

## �️ Directory Structure

```
figma-agent/
├── data/                       # 🟢 The Source of Truth
│   ├── file-structure.json
│   ├── components.json
│   ├── styles.json
│   └── tokens.json             # Processed token map
└── pages/                      # 🟡 Implementation Details
    └── [page-name]/
        └── [section]/
            └── data.json       # Deep extract of a specific UI part
```
