---
description: Build code from figma-agent data - Convert analyzed sections into real components
---

# Figma Build Workflow

Automated workflow to convert data from `figma-agent/` into application code.

## Usage

Command: `/figma-build [section-name] [link selection]`

## Step-by-Step Instructions

### 1. Sync Project Context

- **Action**: Read `AGENTS.md` in the project root.
- **Goal**: Identify framework (Next.js/React), styling (Tailwind/CSS), and preferred directory structure.

### 2. Data Gathering

- **Identify Path**: Locate the directory `figma-agent/[page-name]/section-[section-name]/`.
- **Verify Data**:
  - Read `data.json` (Core structure).
  - Read `section-tokens.json` (Local colors/fonts).
  - Read `common/` (Global token system).

### 3. Activate Coding Skill & Metadata

- **Save Link**: Record the `link selection` into `data.json` and update `specs.md` for traceability.
- Read `figma-to-code/SKILL.md` to apply professional coding standards.

### 4. Download Visual Assets

**Action**: Use the `mcp_FigmaAIBridge_download_figma_images` tool to fetch images/icons identified in Step 2.

- **Source**: Get node IDs from the Asset Manifest in `specs.md` or from `data.json`.
- **Destination**: `figma-agent/[page-name]/section-[section-name]/images/`.
- **Note**: This directory should be created now if it doesn't exist.

### 5. DOM Structure Analysis

- Traverse the `children` tree in `data.json`.
- Identify sub-components that need to be extracted.
- Map icons/images from the `images/` directory.

### 6. Code Generation

- Create the main component file (e.g., `src/components/sections/[SectionName].tsx`).
- Integrate Layout properties (Flex, Gap, Padding) from JSON.
- Apply interaction states from `specs.md`.

### 7. Verification & Finalization

- Check if the code correctly uses Design Token variables.
- Ensure image paths (`src`) point to the correct project asset directories.
- Report results and the location of the generated files.

## Expected Outcome

- A complete, ready-to-run React/Next.js component.
- Strictly adheres to the analyzed design and logic.
