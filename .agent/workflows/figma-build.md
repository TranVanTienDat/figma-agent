---
description: Build code from figma-agent data - Convert analyzed sections into real components
---

# Figma Build Workflow

Automated workflow to convert data from `figma-agent/` into application code.

## Usage

Command: `/figma-build [section-name] [link selection]`

## Step-by-Step Instructions

### 1. Data Gathering

- **Identify Path**: Locate the directory `figma-agent/[page-name]/section-[section-name]/`.
- **Verify Data**:
  - Read `data.json` (Core structure).
  - Read `section-tokens.json` (Local colors/fonts).
  - Read `common/` (Global token system).

### 2. Activate Coding Skill & Metadata

- **Save Link**: Record the `link selection` into `data.json` and update `specs.md` for traceability.
- Read `figma-to-code/SKILL.md` to apply professional coding standards.

### 3. DOM Structure Analysis

- Traverse the `children` tree in `data.json`.
- Identify sub-components that need to be extracted.
- Map icons/images from the `images/` directory.

### 4. Code Generation

- Create the main component file (e.g., `src/components/sections/[SectionName].tsx`).
- Integrate Layout properties (Flex, Gap, Padding) from JSON.
- Apply interaction states from `specs.md`.

### 5. Verification & Finalization

- Check if the code correctly uses Design Token variables.
- Ensure image paths (`src`) point to the correct project asset directories.
- Report results and the location of the generated files.

## Expected Outcome

- A complete, ready-to-run React/Next.js component.
- Strictly adheres to the analyzed design and logic.
