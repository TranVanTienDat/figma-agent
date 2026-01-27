# Figma Analysis Tool for Antigravity

> A comprehensive Figma-to-code extraction system inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec), tailored for Antigravity development workflows.

## 🎯 Overview

This tool automatically extracts design specifications from Figma files and organizes them into a structured, developer-ready format. It captures colors, typography, components, layouts, and interactions—everything needed for pixel-perfect implementation.

## 📦 Installation

When you install `@cam/figma-agent-int`, this tool is automatically configured with:

- **Skills**: Figma analysis capabilities in `.agent/skills/figma-analysis/`
- **Workflows**: Automated extraction workflows in `.agent/workflows/`
- **Storage**: Organized data structure in `figma-agent/`

## 🚀 Quick Start

### 1. Get Figma File Info

```bash
/get-figma-info
```

Provide your Figma URL, and this will show you:

- Available pages and frames
- Component list
- Node IDs for targeted extraction

### 2. Run Full Analysis

```bash
/figma-review
```

This performs comprehensive extraction:

- Design tokens (colors, typography, effects)
- Component specifications
- Layout measurements
- Interactive states
- Visual assets

### 3. Access Extracted Data

All data is saved to `figma-agent/` in a structured format:

```
figma-agent/
├── common/                    # Shared design system
│   ├── colors/
│   ├── typography/
│   ├── effects/
│   └── components/
└── [page-name]/              # Page-specific sections
    └── section-[name]/
        ├── data.json         # Complete section data
        ├── specs.md          # Implementation guide
        ├── images/           # Downloaded assets
        └── components/       # Local components
```

## 📚 Documentation

### Skills

- **[figma-analysis](./SKILL.md)**: Core analysis skill with extraction guidelines

### Workflows

- **[/figma-review](../../workflows/figma-review.md)**: Full design analysis workflow
- **[/get-figma-info](../../workflows/get-figma-info.md)**: Quick file preview

### Templates

- **[system-colors.template.json](./templates/system-colors.template.json)**: Color palette structure
- **[text-presets.template.json](./templates/text-presets.template.json)**: Typography presets

### Examples

- **[section-data-example.json](./examples/section-data-example.json)**: Sample extracted data
- **[specs-example.md](./examples/specs-example.md)**: Sample implementation specs

### Schemas

- **[section-data.schema.json](./schemas/section-data.schema.json)**: JSON schema for validation

## 🎨 What Gets Extracted

### Design Tokens

✅ **Colors**

- All fill colors (Hex, HSL, RGB)
- Grouped by usage (brand, neutral, semantic)
- Color token names

✅ **Typography**

- Font families, sizes, weights
- Line heights and letter spacing
- Text presets (H1, H2, Body, etc.)

✅ **Effects**

- Box shadows (multi-layer support)
- Backdrop blur (glassmorphism)
- Opacity values

### Components

✅ **Global Components**

- Component definitions
- Variants and properties
- All states (default, hover, active, disabled)

✅ **Component Instances**

- Instance overrides (text, colors, visibility)
- Actual displayed content
- Layout constraints

### Layout

✅ **Auto-Layout**

- Direction (horizontal/vertical)
- Padding and gap
- Alignment and justify-content
- Mapped to Flexbox/Grid CSS

✅ **Constraints**

- Fill vs. Fixed sizing
- Min/max widths
- Responsive behavior

### Assets

✅ **Vectors**

- SVG extraction
- Icon dimensions
- Fill colors

✅ **Images**

- PNG/JPG export
- Retina (@2x) support
- Optimized file sizes

### Interactions

✅ **States**

- Hover effects
- Active states
- Focus styles

✅ **Behaviors**

- Click actions
- Navigation targets
- Animations

## 📖 Usage Examples

### Example 1: Extract Header Section

```typescript
// 1. Run workflow
/figma-review

// 2. Provide Figma URL
https://figma.com/file/ABC123?node-id=123:456

// 3. Specify page name
landing-page

// 4. Data is saved to:
.figma-agents/landing-page/section-header/
├── data.json
├── specs.md
└── images/
    └── logo.svg
```

### Example 2: Use Extracted Data

```typescript
import headerData from './.figma-agents/landing-page/section-header/data.json';

// Access layout info
const { width, height, padding, gap } = headerData.layout;

// Get component overrides
const logoText = headerData.children.find(c => c.name === 'Logo')?.overrides.text;

// Build component
<Header
  width={width}
  padding={padding}
  logoText={logoText}
/>
```

### Example 3: Generate CSS from Tokens

```typescript
import colors from './.figma-agents/common/colors/system-colors.json';
import typography from './.figma-agents/common/typography/text-presets.json';

// Generate CSS variables
:root {
  --primary-500: ${colors.brand['primary-500']};
  --h1-size: ${typography.h1.fontSize};
  --h1-weight: ${typography.h1.fontWeight};
}
```

## 🔧 Advanced Features

### Custom Extraction Depth

```typescript
// Shallow extraction (1 level)
mcp_FigmaAIBridge_get_figma_data({
  fileKey: "ABC123",
  nodeId: "123:456",
  depth: 1,
});

// Deep extraction (all levels)
mcp_FigmaAIBridge_get_figma_data({
  fileKey: "ABC123",
  nodeId: "123:456",
  depth: 10,
});
```

### Selective Asset Download

```typescript
// Download only specific icons
mcp_FigmaAIBridge_download_figma_images({
  fileKey: "ABC123",
  nodes: [
    { nodeId: "123:456", fileName: "logo.svg" },
    { nodeId: "789:012", fileName: "icon-search.svg" },
  ],
  localPath: ".figma-agents/common/icons/",
});
```

### Component Variant Extraction

The tool automatically detects and extracts all component variants:

```json
{
  "componentName": "Button",
  "variants": [
    { "name": "Primary", "properties": { "bg": "#3B82F6" } },
    { "name": "Secondary", "properties": { "bg": "#6B7280" } },
    { "name": "Outline", "properties": { "border": "#3B82F6" } }
  ]
}
```

## 🎯 Best Practices

### 1. Naming Conventions in Figma

- Use descriptive layer names: `Button/Primary`, `Icon/Search`
- Group related elements in frames
- Name components clearly for auto-detection

### 2. Organize by Sections

- Break designs into logical sections (Header, Hero, Footer)
- Use consistent naming: `section-header`, `section-hero`
- Keep sections self-contained

### 3. Component Strategy

- Create master components for reusable elements
- Use variants for different states
- Override text/colors at instance level

### 4. Verification

- Always review `audit_status` in data.json
- Cross-check extracted colors with visual design
- Verify text content is actual (not defaults)

## 🐛 Troubleshooting

### Issue: Missing Text Content

**Problem**: Text shows default component content instead of overrides

**Solution**: Check `overrides` property in component instances

```json
{
  "type": "INSTANCE",
  "overrides": {
    "text": "Actual displayed text" // ✅ This is what you need
  }
}
```

### Issue: Colors Don't Match

**Problem**: Extracted colors differ from visual design

**Solution**: Verify you're using the correct fill type

```json
{
  "fills": [
    { "type": "SOLID", "color": "#3B82F6" },  // ✅ Use this
    { "type": "GRADIENT", "stops": [...] }     // Not this
  ]
}
```

### Issue: Missing Assets

**Problem**: Images/icons not downloaded

**Solution**: Ensure node IDs are correct and images have proper fills

```typescript
// Check if node has imageRef
if (node.fills[0].type === 'IMAGE') {
  // Include imageRef in download request
  { nodeId: '123:456', fileName: 'image.png', imageRef: 'abc123' }
}
```

## 📊 Data Schema Reference

### Section Data (`data.json`)

```typescript
interface SectionData {
  sectionName: string;
  nodeId: string;
  figmaUrl?: string;
  layout: LayoutData;
  children: ChildNode[];
  vectors?: VectorNode[];
  interactions?: Interaction[];
  audit_status: "Pending" | "Verified" | "Needs Review";
  last_updated: string;
  extracted_by: string;
}
```

See [section-data.schema.json](./schemas/section-data.schema.json) for complete schema.

## 🤝 Contributing

This tool is designed to evolve with your needs. To add new features:

1. Update the skill in `.agent/skills/figma-analysis/SKILL.md`
2. Add new workflows to `.agent/workflows/`
3. Create templates in `./templates/`
4. Add examples to `./examples/`

## 📄 License

Part of the Antigravity development toolkit.

## 🔗 Related Resources

- [OpenSpec](https://github.com/Fission-AI/OpenSpec) - Original inspiration
- [Figma API Docs](https://www.figma.com/developers/api)
- [MCP Figma Bridge](https://github.com/your-org/mcp-figma-bridge)

---

**Made with ❤️ for Antigravity developers**
