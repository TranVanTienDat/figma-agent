---
description: Figma architect analysis - Extract complete design specifications from Figma
---

# Figma Review Workflow

This workflow performs a comprehensive analysis of a Figma design and extracts all necessary data for implementation.

## Prerequisites

- Figma file URL with node-id parameter (e.g., `https://figma.com/file/ABC123?node-id=123:456`)
- OR Figma file key and node ID separately

## Steps

### 1. Sync Project Context

**Action**: Read `AGENTS.md` in the project root.

- **Why**: To ensure analysis respects project-specific tech stack and coding conventions.

### 2. Activate Figma Analysis Skill

Read the figma-analysis skill to understand the extraction requirements:

```
View file: .agent/skills/figma-analysis/SKILL.md
```

### 2. Get Figma File Information

Ask the user for:

- Figma file URL or file key
- Specific node ID (if analyzing a specific frame/section)
- Page name for organizing extracted data

### 3. Fetch Figma Data

Use the MCP Figma tool to fetch design data:

```
Tool: mcp_FigmaAIBridge_get_figma_data
Parameters:
  - fileKey: [extracted from URL or provided]
  - nodeId: [specific node or omit for full file]
```

### 4. Analyze and Save Design Tokens (MANDATORY EXECUTION)

You **MUST** extract the following design tokens and physically save them as JSON files in the `common/` directory.

**1. System Colors:**

- **Action**: Use `write_to_file` to create/update `figma-agent/common/colors/system-colors.json`.
- Include brand colors, background (#0B0121, etc.), and text colors.

**2. Typography Presets:**

- **Action**: Use `write_to_file` to create/update `figma-agent/common/typography/text-presets.json`.
- Include H1-H6, Body, and UI Label presets.

**3. Effects & Premium Details:**

- **Action**: Use `write_to_file` to create/update `figma-agent/common/styles/effects.json`.
- Include Glassmorphism and Radial Glow rules.

**4. Global Variants:**

- **Action**: Use `write_to_file` to create/update `figma-agent/common/variants/global-variants.json`.

// turbo

> **Note**: As an agent, you must execute these tool calls immediately. Do not just show the code block to the user.

### 5. Identify Components

**Global Components:**

- Find all component definitions
- Extract variants and properties
- Document states (hover, active, disabled)
- Save to `figma-agent/common/components/[ComponentName]/data.json`

**Local Components:**

- Identify section-specific components
- Generate boilerplate code in `figma-agent/[page-name]/section-[name]/components/local-component.tsx`

### 6. identify and Create Section Folders (MANDATORY)

You **MUST** physically create the directory structure on the disk. Do not just describe it.

1. **Identify Sections**: Look for top-level frames (e.g., `header-nav`, `hero-section`, `features-grid`).
2. **Execute Initialization**: For each identified section, run the initialization script via the `run_command` tool.

   // turbo

   ```bash
   # Syntax: node .agent/skills/figma-analysis/scripts/init-figma-agents.js [page-name] [section-name]
   # Example:
   node .agent/skills/figma-analysis/scripts/init-figma-agents.js landing-page header-nav
   node .agent/skills/figma-analysis/scripts/init-figma-agents.js landing-page hero-section
   ```

3. **Verify Creation**: Using `list_dir`, verify that `figma-agent/[page-name]/[section-name]` exists.

### 7. Download Visual Assets

Extract vectors and images for each section and save them into the newly created folders:

```
Tool: mcp_FigmaAIBridge_download_figma_images
Parameters:
  - fileKey: [file key]
  - nodes: [array of image/icon node IDs]
  - localPath: figma-agent/[page-name]/[section-name]/images/
  - pngScale: 2
```

### 8. Generate Specifications

Create `specs.md` for each section with:

- Layout overview (dimensions, spacing)
- Component breakdown
- Interaction states
- Responsive behavior notes
- Implementation hints

### 9. Create Implementation Blueprint

Generate a comprehensive report and **Verify** that all folders were created on the filesystem.

### 10. Verify Extraction

Cross-check:

- All text content is actual displayed text (not defaults)
- Component overrides are captured
- Colors match visual design
- Measurements are accurate
- Assets are downloaded correctly

Set `audit_status: "Verified"` in data.json files

## Output Structure

After completion, you should have:

```
figma-agent/
├── common/                         # Shared Design System
│   ├── colors/
│   │   └── system-colors.json      # Global color tokens
│   ├── typography/
│   │   └── text-presets.json      # Global font presets
│   ├── styles/
│   │   └── effects.json           # Glassmorphism, Glows, Radiad Gradients
│   └── variants/                   # Global component variants
│
└── [page-name]/                    # Page-specific assets (e.g., landing-page)
    └── [section-name]/             # Examples: header-nav, hero-section, features-grid, footer
        ├── data.json               # Exhaustive layout & children metadata
        ├── specs.md                # Technical implementation documentation
        ├── components/             # Generated .tsx components (local to section)
        └── images/                 # Downloaded SVG/PNG assets
```

## Tips

- Always extract actual content, not placeholder text
- Pay attention to component instances vs. master components
- Document all interactive states (hover, focus, active)
- **Check for High-End Details**: Look for `-1%` letter-spacing on titles, 1px borders, and backdrop blurs.
- Note any animations or transitions
- Include accessibility considerations
- Be precise with measurements (don't round unnecessarily)

## Common Issues

**Issue**: Text shows default component content instead of overrides
**Solution**: Check `overrides` property in component instances

**Issue**: Colors don't match visual design
**Solution**: Verify you're using the correct fill (not stroke or effect)

**Issue**: Missing assets
**Solution**: Ensure node IDs are correct and images have proper fills

**Issue**: Layout doesn't match
**Solution**: Check for absolute positioning or negative margins
