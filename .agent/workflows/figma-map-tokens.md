---
description: Create Design System Tokens
---

This workflow takes the raw style data from Step 1 (`figma-agent/data/styles.json`) and converts it into usable code (CSS/Tailwind).

# Prerequisites

- You must have run `/sync-figma-data` first to generate `figma-agent/data/styles.json`.

# Steps

1. Create a Token Transformer Script.
   _This script reads the raw Figma JSON and outputs a cleaner Tailwind-ready format._
   // turbo

```javascript
const fs = require("fs");
const path = require("path");

const stylesPath = path.join(process.cwd(), "figma-agent/data/styles.json");
const outputPath = path.join(process.cwd(), "figma-agent/data/tokens.json");

if (!fs.existsSync(stylesPath)) {
  console.error("❌ styles.json not found. Run /sync-figma-data first.");
  process.exit(1);
}

const rawData = JSON.parse(fs.readFileSync(stylesPath, "utf8"));
const styles = rawData.meta?.styles || [];

const tokens = {
  colors: {},
  typography: {},
};

// Simple mapping logic (In a real app, you'd parse properties deeper if available,
// here we map metadata to placeholders for manual fill or advanced parsing)
styles.forEach((style) => {
  const name = style.name.toLowerCase().replace(/[^a-z0-9]/g, "-");
  if (style.style_type === "FILL") {
    tokens.colors[name] = "var(--color-" + name + ")"; // Placeholder or actual value if available
  } else if (style.style_type === "TEXT") {
    tokens.typography[name] = "var(--font-" + name + ")";
  }
});

fs.writeFileSync(outputPath, JSON.stringify(tokens, null, 2));
console.log(`✅ Generated tokens at ${outputPath}`);
```

2. Run the Transformer.
   // turbo

```bash
node -e "$(cat << 'EOF'
const fs = require('fs');
const path = require('path');
// ... [The script content from above effectively]
// Since we can't easily embed large scripts in one line, we recommend creating a dedicated script file in a real scenario.
// For now, we will assume the user creates 'scripts/transform-tokens.js' or we just run a simplified version.
EOF
)"
```

_Note: For stability, I will create a dedicated script file instead of inline execution._

3. Create the dedicated transformation script.
   // turbo

```bash
mkdir -p .agent/skills/figma-analysis/scripts
```

4. Write the transformer script.
   // turbo

```javascript
const fs = require("fs");
const path = require("path");

const stylesPath = path.join(process.cwd(), "figma-agent/data/styles.json");
const outputPath = path.join(process.cwd(), "figma-agent/data/tokens.json");

try {
  if (!fs.existsSync(stylesPath)) {
    console.error("❌ styles.json not found. Run /sync-figma-data first.");
    process.exit(1);
  }

  const rawData = JSON.parse(fs.readFileSync(stylesPath, "utf8"));
  // Figma API 'GET /styles' returns metadata only (key, name, description).
  // It does NOT return the actual hex codes. We actually need a separate "Node" lookup for that (a limitation of Figma API).
  // For this Step 1 workflow, we will prepare the dictionary mapping.

  const tokens = {
    map: {},
  };

  const styles = rawData.meta?.styles || [];
  styles.forEach((s) => {
    tokens.map[s.node_id] = {
      name: s.name,
      type: s.style_type,
    };
  });

  fs.writeFileSync(outputPath, JSON.stringify(tokens, null, 2));
  console.log(`✅ Token Map created with ${styles.length} entries.`);
  console.log(
    "ℹ️  Note: To get actual Hex codes, we will match these IDs during the 'Deep Dive' step.",
  );
} catch (e) {
  console.error("Error:", e);
}
```

5. Execute transformation.

```bash
node .agent/skills/figma-analysis/scripts/transform_tokens.js
```
