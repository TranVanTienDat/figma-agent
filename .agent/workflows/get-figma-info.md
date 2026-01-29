---
description: Get figma information - Quick extraction of basic Figma file data
---

# Get Figma Info Workflow

Quick workflow to fetch basic information from a Figma file or perform a targeted deep-dive for a specific section.

## 🛡️ Permanent Guardrails

This workflow operates under strict security and accuracy protocols defined in `.agent/skills/figma-analysis/SKILL.md`:

1.  **Figma-Only Access**: No external links are permitted.
2.  **Exhaustive Deep Dive Mode**: Continuous recursive scanning until leaf nodes are reached. Zero guessing.

## Steps

### 1. Identify Target

- If a **section-page** and **link selection** (URL with `node-id`) are provided:
  - Proceed to **Targeted Extraction (Exhaustive Deep Dive)**.
- Otherwise, proceed to **General Preview**.

### 2. Targeted Extraction (Exhaustive Deep Dive)

If targeted, perform the following strict protocol:

1.  **Phase 1: Recursive X-Ray Scan**:
    - Use `mcp_figma_desktop_get_metadata` (or equivalent) with `nodeId` and **Full Depth** traversal.
    - Reach all "leaves" (Text, Vector, Boolean).
    - Discard all `hidden == true` nodes.

2.  **Phase 2: Data Point extraction**:
    - Extract Text Overrides (actual strings), Typography styles, Component Variants/Properties, and Auto-Layout specs.

3.  **Phase 3: Visual Verification (Audit)**:
    - **MANDATORY**: Run `get_screenshot` for the target frame.
    - Compare text/icons in image vs. JSON data.
    - If mismatch found, re-scan subtree immediately.

4.  **Save to File Structure**:
    - Directory: `figma-agent/pages/[page-name]/[section-page]/`
    - File: `data.json`
    - Metadata: Set `audit_status: "Verified"` after successful comparison.

### 3. General Preview (Default)

If no section is specified:

1. **Fetch Basic File Data**:
   - Use `mcp_figma_desktop_get_metadata` (fileKey only).

2. **Display Structure**:
   - List Pages, Top-Level Frames, and Node IDs.
   - Show available components.

## Output Structure

When Targeted Extraction is used, it creates/updates:

```
figma-agent/
└── pages/
    └── [page-name]/
        └── [section-page]/
            ├── data.json               # Populated with deep-dive data
            └── ...                     # Other section assets
```

## Output

User should know:

- What's in the Figma file
- Which frames to analyze
- Node IDs for targeted extraction
- Whether the file is accessible

## Error Handling

**If file not found:**

- Check if file key is correct
- Verify Figma access token is configured
- Ensure file is not private/restricted

**If no frames found:**

- File might be empty
- Check different pages
- Verify you have view permissions
