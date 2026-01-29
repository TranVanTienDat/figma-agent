---
description: Design-to-Code Audit - Compare existing components with Figma designs to ensure pixel-perfection
---

# Figma Audit Workflow

Automated workflow to verify the alignment between your existing code and the source of truth in Figma.

## Usage

Command: `/figma-audit [section-page] [link selection]`

## Step-by-Step Instructions

### 1. Data Refresh

- **Fetch Source of Truth**: Perform an exhaustive deep dive of the Figma `link selection` to get the most up-to-date metadata.
- **Identify Metadata**: Extract layout, typography, and color tokens from the fresh data.

### 2. Code Inspection

- **Locate Component**: Find the corresponding component file (e.g., `src/components/pages/[PageName]/[SectionPage].tsx`).
- **Analyze Code Structure**: Read the component implementation to understand its current layout logic (Flexbox, Grid, CSS variables).

### 3. Comparison Logic (The Audit)

Perform a line-by-line comparison across these dimensions:

- **Tokens**: Are the color variables and font presets used in code matching the Figma tokens?
- **Layout Precision**: Check if `gap`, `padding`, and `margin` values in code match the Figma Auto-layout specs.
- **Constraints**: Verify if "Fill Container" or "Hug Contents" behavior is correctly implemented with responsive CSS.
- **Content Overrides**: Ensure actual text and assets match the latest Figma overrides.

### 4. Audit Report Generation

Generate a report containing:

- **✅ Matches**: List of elements that are pixel-perfect.
- **❌ Discrepancies**: Specific differences found (e.g., "Expected 24px gap, found 16px").
- **⚠️ Technical Debt**: Identification of hard-coded values that should use Design Tokens.

### 5. Implementation Plan

Create a prioritized list of changes:

1. **Critical Fixes**: Layout or token mismatches that break the visual identity.
2. **Refinements**: Micro-interactions or subtle spacing adjustments.
3. **Optimizations**: Replacing custom values with standardized tokens.

## Expected Outcome

- A clear **Comparison Report**.
- A step-by-step **Remediation Plan** to synchronize the code with the design.
