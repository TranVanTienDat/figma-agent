#!/usr/bin/env node

/**
 * Figma Agents Directory Initializer
 *
 * Creates the standard directory structure for storing extracted Figma data.
 * Usage: node init-figma-agents.js [page-name] [section-name]
 */

const fs = require("fs");
const path = require("path");

// Parse command line arguments
const args = process.argv.slice(2);
const pageName = args[0];
const sectionName = args[1];

// Base directory
const baseDir = path.join(process.cwd(), "figma-agent");

/**
 * Create directory if it doesn't exist
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`✅ Created: ${dirPath}`);
  } else {
    console.log(`⏭️  Exists: ${dirPath}`);
  }
}

/**
 * Create a template JSON file
 */
function createTemplateFile(filePath, content) {
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, JSON.stringify(content, null, 2));
    console.log(`✅ Created: ${filePath}`);
  } else {
    console.log(`⏭️  Exists: ${filePath}`);
  }
}

/**
 * Initialize common directory structure
 */
function initCommonStructure() {
  console.log("\n📁 Initializing common structure...\n");

  // Common directories
  ensureDir(path.join(baseDir, "common"));
  ensureDir(path.join(baseDir, "common", "colors"));
  ensureDir(path.join(baseDir, "common", "typography"));
  ensureDir(path.join(baseDir, "common", "styles")); // Updated: unified styles folder
  ensureDir(path.join(baseDir, "common", "components"));
  ensureDir(path.join(baseDir, "common", "variants"));

  // Default page directories
  ensureDir(path.join(baseDir, "pages"));

  // Create template files
  const colorsTemplate = {
    colors: {
      brand: {},
      neutral: {},
      semantic: {},
    },
    usage: {},
    extracted_from: "Figma file",
    last_updated: new Date().toISOString(),
  };

  const typographyTemplate = {
    typography: {},
    fontFamilies: {},
    extracted_from: "Figma file",
    last_updated: new Date().toISOString(),
  };

  const effectsTemplate = {
    effects: {
      glassmorphism: {},
      glows: {},
      gradients: {},
    },
    last_updated: new Date().toISOString(),
  };

  const variantsTemplate = {
    variants: {},
    last_updated: new Date().toISOString(),
  };

  createTemplateFile(
    path.join(baseDir, "common", "colors", "system-colors.json"),
    colorsTemplate,
  );

  createTemplateFile(
    path.join(baseDir, "common", "typography", "text-presets.json"),
    typographyTemplate,
  );

  createTemplateFile(
    path.join(baseDir, "common", "styles", "effects.json"),
    effectsTemplate,
  );

  createTemplateFile(
    path.join(baseDir, "common", "variants", "global-variants.json"),
    variantsTemplate,
  );
}

/**
 * Initialize page-specific section structure
 */
function initSectionStructure(page, section) {
  console.log(`\n📁 Initializing section: ${page}/${section}...\n`);

  // Removed "section-" prefix for cleaner naming
  const sectionDir = path.join(baseDir, page, section);

  // Section directories
  ensureDir(sectionDir);
  ensureDir(path.join(sectionDir, "components"));
  ensureDir(path.join(sectionDir, "images"));
  ensureDir(path.join(sectionDir, "colors"));

  // Create data.json template
  const dataTemplate = {
    sectionName: section,
    nodeId: "",
    figmaUrl: "",
    layout: {
      width: 0,
      height: 0,
      padding: { top: 0, right: 0, bottom: 0, left: 0 },
      gap: 0,
      direction: "horizontal",
      alignment: "center",
      justifyContent: "space-between",
    },
    children: [],
    vectors: [],
    interactions: [],
    audit_status: "Pending",
    last_updated: new Date().toISOString(),
    extracted_by: "figma-analysis-skill",
  };

  createTemplateFile(path.join(sectionDir, "data.json"), dataTemplate);

  // Create specs.md template
  const specsTemplate = `# ${section} Section

**Node ID**: [To be filled]  
**Figma URL**: [To be filled]  
**Status**: ⏳ Pending  
**Last Updated**: ${new Date().toISOString()}

---

## 📐 Layout Specifications

[To be filled]

---

## 🧩 Components

[To be filled]

---

## 🎨 Assets

[To be filled]

---

## 🎭 Interactions

[To be filled]

---

## ♿ Accessibility

- [ ] Add accessibility considerations

---

## 📱 Responsive Behavior

[To be filled]

---

## 💻 Implementation Code

[To be filled]
`;

  const specsPath = path.join(sectionDir, "specs.md");
  if (!fs.existsSync(specsPath)) {
    fs.writeFileSync(specsPath, specsTemplate);
    console.log(`✅ Created: ${specsPath}`);
  } else {
    console.log(`⏭️  Exists: ${specsPath}`);
  }

  // Create section-specific color tokens file
  const sectionColorsTemplate = {
    section: section,
    colors: {},
    last_updated: new Date().toISOString(),
  };

  createTemplateFile(
    path.join(sectionDir, "colors", "section-tokens.json"),
    sectionColorsTemplate,
  );
}

/**
 * Main execution
 */
function main() {
  console.log("🚀 Figma Agents Directory Initializer\n");

  // Always initialize common structure
  initCommonStructure();

  // Initialize section structure if provided
  if (pageName && sectionName) {
    initSectionStructure(pageName, sectionName);
  } else if (pageName || sectionName) {
    console.log(
      "\n⚠️  Warning: Both page-name and section-name are required for section initialization",
    );
    console.log("Usage: node init-figma-agents.js [page-name] [section-name]");
  }

  console.log("\n✨ Initialization complete!\n");
  console.log("Next steps:");
  console.log("1. Run /get-figma-info to preview your Figma file");
  console.log("2. Run /figma-review to extract design data");
  console.log("3. Check figma-agent/ for extracted data\n");
}

// Run
main();
