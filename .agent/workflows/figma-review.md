---
description: Figma architect analysis - Extract complete design specifications from Figma
---

# Figma Review Workflow

This workflow performs a comprehensive analysis of a Figma design and extracts all necessary data for implementation.

## 🛡️ Permanent Guardrails

This workflow operates under strict security and accuracy protocols defined in `.agent/skills/figma-analysis/SKILL.md`:

1.  **Figma-Only Access**: No external links are permitted.
2.  **Exhaustive Deep Dive**: Recursive scanning with visual verification via screenshots.

## Steps

### 1. Sync Project Context

**Action**: Read `AGENTS.md` in the project root.

- **Why**: To ensure analysis respects project-specific tech stack and coding conventions.

### 2. Activate Figma Analysis Skill

Read the figma-analysis skill to understand the extraction requirements:

```
View file: .agent/skills/figma-analysis/SKILL.md
```

### 3. File Discovery & Metadata (Initial Phase)

Before deep-diving into nodes, extract the file-level context to understand the project's scale and ownership.

// turbo

```bash
# Get file key from URL and fetch metadata
python3 .agent/skills/figma-analysis/scripts/fetch_figma_metadata.py "[figma_url]"
```

- **Action**: Read the generated `figma_metadata.json` to identify the file name, creator, and total components/styles.
- **Goal**: Provide a summary of the project to the user before proceeding.

### 4. Fetch Figma Data (Exhaustive Mode)

**Security Reminder**: You are strictly prohibited from accessing any non-Figma URLs during this process.

Use the MCP Figma tool to fetch design data recursively:

```
Tool: mcp_FigmaAIBridge_get_figma_data
Parameters:
  - fileKey: [extracted]
  - nodeId: [specific node]
  - depth: [Full traversal to leaves]
```

### 4. Recursive Scan & Data Point Extraction

Follow the **Phase 1 & 2** of the Exhaustive Deep Dive protocol:

- Discard hidden nodes.
- Extract Text Overrides, Font Styles, Component Properties, and Auto-Layout specs.

### 6. Analyze and Save Design Tokens (MANDATORY EXECUTION)

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

### 7. Identify Components

**Global Components:**

- Find all component definitions
- Extract variants and properties
- Document states (hover, active, disabled)
- Save to `figma-agent/common/components/[ComponentName]/data.json`
- **Metadata Requirement**: `data.json` must include `frame` info (width, height, absolute position) and a deep `children` tree representing the full node hierarchy.

**Local Components:**

- Identify section-specific components
- Generate boilerplate code in `figma-agent/[page-name]/section-[name]/components/local-component.tsx`

### 8. Identify and Create Section Folders (MANDATORY Architecture)

You **MUST** physically create the directory structure on the disk following the hierarchical rule:
`figma-agent/pages/[page-name]/[section-page]`.

1. **Identify Sections**: Look for top-level frames (e.g., `sidebar-nav`, `project-list`, `chat-content`).
2. **Execute Initialization**: For each identified section, run the initialization script via the `run_command` tool.

   // turbo

   ```bash
   # Syntax: node .agent/skills/figma-analysis/scripts/init-figma-agents.js [page-name] [section-page]
   # Example for Information Page:
   node .agent/skills/figma-analysis/scripts/init-figma-agents.js information-page sidebar-nav

   # Example for User Detail Page:
   node .agent/skills/figma-analysis/scripts/init-figma-agents.js user-detail-page header-profile
   ```

3. **Verify Creation**: Using `list_dir`, verify that `figma-agent/[page-name]/[section-name]` exists.

### 9. Identify Visual Assets

Identify all image and icon nodes that will be needed for implementation.

- List their node IDs and intended filenames in `specs.md`.
- **DO NOT** download them now. They will be fetched during the `@figma-build` phase to keep the review process lean.

### 10. Generate Specifications

Create `specs.md` for each section with:

- Layout overview (dimensions, spacing)
- Component breakdown
- Interaction states
- Responsive behavior notes
- Implementation hints
- **Assets Manifest**: List all image/icon nodes with their IDs and proposed file names.

### 11. Create Implementation Blueprint

Generate a comprehensive report and **Verify** that all folders were created on the filesystem.

### 10. Finalize Review

Set `audit_status: "Review-Complete"` in data.json files (Visual Verification deferred to Build phase).

## 📂 Output Structure

After completion, the `figma-agent/` directory must follow this organization:

```
figma-agent/
├── common/                         # General project information (Design System)
│   ├── colors/
│   │   └── system-colors.json      # Global color tokens
│   ├── typography/
│   │   └── text-presets.json      # Global font presets
│   ├── styles/
│   │   └── effects.json           # Glassmorphism, Glows, Radial Gradients
│   └── variants/                   # Global component variants
│
└── pages/                          # All project pages
    └── [page-name]/                # Data for a specific page (e.g., information-page)
        └── [section-page]/         # UI Section information within that page
            ├── data.json           # Metadata layout & node tree structure
            ├── specs.md            # Technical documentation & display logic
            └── components/         # Child components for this section
```

## 📖 Usage Examples

When a user requests to review a specific page, follow the `[name]-page` naming convention.

**Example 1: Reviewing the Information Page**

- **Prompt**: `/figma-review [link]. review the information page`
- **Action**: Create the directory `figma-agent/pages/information-page/`. If `landing-page` was previously used, replace it with this new name.

**Example 2: Reviewing an additional User Detail Page**

- **Prompt**: `/figma-review [link]. review the user-detail page`
- **Action**: Create the directory `figma-agent/pages/user-detail-page/` alongside `information-page`. Do not delete existing pages.

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
