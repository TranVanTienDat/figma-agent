# Figma Agent Integration - Workflow Diagram

## 🔄 Complete Extraction Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIGMA DESIGN FILE                            │
│  https://figma.com/file/ABC123?node-id=123:456                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: Preview File Structure                     │
│                   /get-figma-info                               │
│                                                                 │
│  Output:                                                        │
│  • Available pages                                              │
│  • Frame list with node IDs                                     │
│  • Component inventory                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 2: Full Design Analysis                       │
│                   /figma-review                                 │
│                                                                 │
│  Process:                                                       │
│  1. Activate figma-analysis skill                               │
│  2. Fetch Figma data via MCP                                    │
│  3. Extract design tokens                                       │
│  4. Identify components                                         │
│  5. Parse layout structure                                      │
│  6. Download assets                                             │
│  7. Generate specifications                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 3: Data Organization                          │
│                                                                 │
│  figma-agent/                                                   │
│  ├── common/                  ← Shared design system (General)  │
│  │   ├── colors/                                                │
│  │   ├── typography/                                            │
│  │   └── components/                                            │
│  └── pages/                   ← All project pages               │
│      └── [page-name]/         ← Specific page info              │
│          └── [section-page]/  ← UI section data                 │
│              ├── data.json    ← Complete section metadata       │
│              ├── specs.md     ← Implementation guide            │
│              ├── images/      ← Downloaded assets               │
│              └── components/  ← Local components                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 4: Implementation                             │
│                                                                 │
│  Developer uses extracted data:                                 │
│  • Import data.json for structure                               │
│  • Read specs.md for guidance                                   │
│  • Use assets from images/                                      │
│  • Apply design tokens from common/                             │
│                                                                 │
│  Result: Pixel-perfect implementation! ✨                       │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow

```
Figma File
    │
    ├─► Design Tokens
    │   ├─► Colors         → figma-agent/common/colors/
    │   ├─► Typography     → figma-agent/common/typography/
    │   └─► Effects        → figma-agent/common/styles/
    │
    ├─► Components
    │   ├─► Global         → figma-agent/common/components/
    │   └─► Local          → figma-agent/pages/[page]/[section]/components/
    │
    ├─► Layout
    │   ├─► Structure      → data.json (layout property)
    │   ├─► Children       → data.json (children array)
    │   └─► Constraints    → data.json (constraints)
    │
    ├─► Assets
    │   ├─► Vectors (SVG)  → figma-agent/pages/[page]/[section]/images/
    │   └─► Images (PNG)   → figma-agent/pages/[page]/[section]/images/
    │
    └─► Specifications
        ├─► data.json      → Complete section metadata
        └─► specs.md       → Implementation guide
```

## 🎨 Component Extraction Flow

```
Component in Figma
    │
    ├─► Is it a Master Component?
    │   ├─► YES → Extract to common/components/
    │   │         ├─► Component definition
    │   │         ├─► All variants
    │   │         └─► Default properties
    │   │
    │   └─► NO → Is it a Component Instance?
    │       ├─► YES → Extract instance data
    │       │         ├─► Component ID reference
    │       │         ├─► Overrides (text, colors, etc.)
    │       │         └─► Actual displayed content
    │       │
    │       └─► NO → Extract as regular node
    │                 └─► Node properties and styles
```

## 🔍 Token Extraction Process

```
Figma Node
    │
    ├─► Analyze Fills
    │   ├─► Solid Color    → Extract Hex/HSL/RGB
    │   ├─► Gradient       → Extract stops and colors
    │   └─► Image          → Download image
    │
    ├─► Analyze Text Styles
    │   ├─► Font Family    → Extract font name
    │   ├─► Font Size      → Extract size in px
    │   ├─► Line Height    → Extract line-height
    │   ├─► Font Weight    → Extract weight (400, 700, etc.)
    │   └─► Letter Spacing → Extract spacing value
    │
    ├─► Analyze Effects
    │   ├─► Drop Shadow    → Extract shadow values
    │   ├─► Inner Shadow   → Extract shadow values
    │   ├─► Blur           → Extract blur radius
    │   └─► Opacity        → Extract opacity value
    │
    └─► Analyze Layout
        ├─► Auto-layout    → Extract flex properties
        ├─► Padding        → Extract padding values
        ├─► Gap            → Extract gap value
        └─► Constraints    → Extract sizing behavior
```

## 🚀 Usage Patterns

### Pattern 1: Design System Creation

```
1. Extract all pages with /figma-review
2. Consolidate tokens in common/
3. Generate CSS variables from tokens
4. Build component library
```

### Pattern 2: Landing Page Implementation

```
1. Preview file with /get-figma-info
2. Extract each section separately
3. Build sections using extracted data
4. Assemble complete page
```

### Pattern 3: Component Library

```
1. Extract component master definitions
2. Document all variants
3. Generate component code
4. Create Storybook stories
```

## 📈 Extraction Quality Levels

```
Level 1: Basic Extraction
├─► Layout dimensions
├─► Basic colors
└─► Text content

Level 2: Standard Extraction (Default)
├─► Complete layout with auto-layout
├─► All design tokens
├─► Component instances with overrides
├─► Basic assets
└─► Implementation specs

Level 3: Deep Extraction
├─► Multi-level component nesting
├─► All component variants
├─► Complex interactions
├─► All assets (optimized)
├─► Comprehensive specs
└─► Accessibility notes
```

## 🎯 Best Practices Flow

```
Before Extraction:
├─► Organize Figma file
├─► Name layers clearly
├─► Create components
└─► Use auto-layout

During Extraction:
├─► Start with /get-figma-info
├─► Extract incrementally
├─► Verify each section
└─► Check audit_status

After Extraction:
├─► Review data.json
├─► Read specs.md
├─► Test implementation
└─► Update as needed
```

## 🔄 Iteration Workflow

```
Design Changes in Figma
    │
    ▼
Re-run /figma-review
    │
    ▼
Compare with previous data.json
    │
    ├─► Colors changed?     → Update CSS variables
    ├─► Layout changed?     → Update component structure
    ├─► Content changed?    → Update text/images
    └─► Components changed? → Update component library
    │
    ▼
Update implementation
    │
    ▼
Verify changes
```

## 📊 File Size Optimization

```
Assets
    │
    ├─► Vectors (SVG)
    │   ├─► Optimize with SVGO
    │   ├─► Remove unnecessary attributes
    │   └─► Minify paths
    │
    └─► Images (PNG/JPG)
        ├─► Export at @2x for retina
        ├─► Compress with imagemin
        └─► Convert to WebP if possible
```

---

## 🎓 Learning Path

### Beginner

1. Run `/get-figma-info` on a simple file
2. Extract a single section with `/figma-review`
3. Review the generated data.json
4. Read the specs.md
5. Implement a simple component

### Intermediate

1. Extract complete landing page
2. Build design system from tokens
3. Create component library
4. Use variants and overrides
5. Implement responsive layouts

### Advanced

1. Extract complex multi-page applications
2. Automate extraction with scripts
3. Integrate with CI/CD pipeline
4. Custom template creation
5. Advanced component mapping

---

**Visual workflow complete! 🎨**

This diagram shows the complete flow from Figma design to implementation.
