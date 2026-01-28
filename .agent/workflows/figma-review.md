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

### 4. Analyze Design Tokens

Extract and organize:

**Colors:**

- Parse all fill colors from nodes
- Group by usage (brand, neutral, semantic)
- Convert to HSL and Hex
- Save to `figma-agent/common/colors/system-colors.json`

**Typography:**

- Extract font families, sizes, weights
- Calculate line heights and letter spacing
- Create presets (H1, H2, Body, Caption, etc.)
- Save to `figma-agent/common/typography/text-presets.json`

**Global Variants:**

- Identify common component states and variations
- Save to `figma-agent/common/variants/global-variants.json`

### 5. Identify Components

**Global Components:**

- Find all component definitions
- Extract variants and properties
- Document states (hover, active, disabled)
- Save to `figma-agent/common/components/[ComponentName]/data.json`

**Local Components:**

- Identify section-specific components
- Generate boilerplate code in `figma-agent/[page-name]/section-[name]/components/local-component.tsx`

### 6. identify and Create Section Folders

For each logical section identified in the design (e.g., Header, Hero, Features, Pricing, Footer):

1. **Identify Sections**: Look for top-level frames or logical groups in the Figma tree.
2. **Create Directory**: `figma-agent/[page-name]/section-[name]/` (e.g., `figma-agent/landingpage/header-hero/`).
3. **Generate specs.md**: Create detailed technical documentation for the section.
4. **Initialize data.json**: Extract the node metadata for this section and save it.
5. **Setup sub-folders**: Create `components/` and `images/` folders within the section directory.

### 7. Download Visual Assets

Extract vectors and images for each section:

```
Tool: mcp_FigmaAIBridge_download_figma_images
Parameters:
  - fileKey: [file key]
  - nodes: [array of image/icon node IDs]
  - localPath: figma-agent/[page-name]/section-[name]/images/
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

Generate a comprehensive report including:

1. **Executive Summary**
   - Total sections analyzed
   - Components identified
   - Color palette size
   - Estimated implementation complexity

2. **Architecture Tree**
   - Recommended file structure
   - Component organization
   - Asset locations

3. **Token Tables**
   - Colors with usage
   - Typography presets
   - Spacing scale
   - Shadow definitions

4. **Component Specifications**
   - Props interface
   - State variations
   - Accessibility requirements

5. **Code Starters**
   - TSX component skeletons
   - Tailwind/CSS classes
   - Type definitions

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
│   └── variants/                   # Global component variants
│
└── [page-name]/                    # Page-specific assets (e.g., landingpage)
    └── section-[name]/             # Example: header-hero, features, footer
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
