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

  // The 'styles' endpoint returns metadata: [{ "key": "...", "name": "Primary/Blue", "style_type": "FILL" }]
  // It is effectively a "Dictionary" or "Map".

  const tokens = {
    colors: {},
    texts: {},
    raw_map: {},
  };

  const styles = rawData.meta?.styles || [];

  styles.forEach((s) => {
    // Create a raw map for lookup by NodeID later
    tokens.raw_map[s.node_id] = s;

    // Organize by type for human readability
    if (s.style_type === "FILL") {
      tokens.colors[s.name] = s.node_id;
    } else if (s.style_type === "TEXT") {
      tokens.texts[s.name] = s.node_id;
    }
  });

  fs.writeFileSync(outputPath, JSON.stringify(tokens, null, 2));
  console.log(`✅ Token Map created at figma-agent/data/tokens.json`);
  console.log(`   - Colors found: ${Object.keys(tokens.colors).length}`);
  console.log(`   - Text Styles found: ${Object.keys(tokens.texts).length}`);
} catch (e) {
  console.error("Error processing tokens:", e);
}
