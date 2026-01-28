---
description: Get figma information - Quick extraction of basic Figma file data
---

# Get Figma Info Workflow

Quick workflow to fetch basic information from a Figma file or perform a targeted deep-dive for a specific section.

## Usage Modes

1. **General Preview**: Run `/get-figma-info [link]` to see the file structure.
2. **Targeted Extraction**: Run `/get-figma-info [section-name] [link selection]` to extract data for a specific section.

## Steps

### 1. Identify Target

- If a **section-name** and **link selection** (URL with `node-id`) are provided:
  - Proceed to **Targeted Extraction**.
- Otherwise, proceed to **General Preview**.

### 2. Targeted Extraction (Write to Data.json)

If targeted, perform the following:

1. **Extract Identifiers**:
   - `fileKey`: From URL
   - `nodeId`: From `node-id` parameter in URL
   - `page-name`: Identify the Figma page name from the data

2. **Fetch Deep Data**:
   - Use `mcp_FigmaAIBridge_get_figma_data` with `nodeId` and `depth: 20` (Exhaustive Deep Dive).

3. **Save to File Structure**:
   - Directory: `figma-agent/[page-name]/section-[section-name]/`
   - File: `data.json`
   - Content: Full JSON structure including layout, children, and properties.

4. **Verify Metadata**:
   - Ensure `audit_status` is set to "Extracted" in the JSON.

### 3. General Preview (Default)

If no section is specified:

1. **Fetch Basic File Data**:
   - Use `mcp_FigmaAIBridge_get_figma_data` (fileKey only).

2. **Display Structure**:
   - List Pages, Top-Level Frames, and Node IDs.
   - Show available components.

## Output Structure

When Targeted Extraction is used, it creates/updates:

```
figma-agent/
└── [page-name]/
    └── section-[section-name]/
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
