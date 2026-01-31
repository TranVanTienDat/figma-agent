const fs = require("fs");
const path = require("path");

// Configuration paths for the test environment
const dataDir = path.join(process.cwd(), "TEST/data/target-node-split");
const structurePath = path.join(dataDir, "01-structure.json");
const fullTreePath = path.join(dataDir, "99-full-tree.json");
const colorsPath = path.join(dataDir, "05-colors.json");
const outputPath = path.join(process.cwd(), "figma-agent/data/tokens.json");

function getBackgroundColor() {
  try {
    if (!fs.existsSync(structurePath)) return "#ffffff";

    // 1. Get Root ID from structure
    const structure = JSON.parse(fs.readFileSync(structurePath, "utf8"));
    const rootId = structure.id;

    if (!rootId) return "#ffffff";

    // 2. Find this Node in the full tree to get its fills
    // Note: In a real scenario we'd scan multiple fragments if needed
    if (!fs.existsSync(fullTreePath)) return "#ffffff";

    const treeData = JSON.parse(fs.readFileSync(fullTreePath, "utf8"));

    // Recursive search for the node with rootId
    function findNode(node, id) {
      if (node.id === id) return node;
      if (node.children) {
        for (const child of node.children) {
          const found = findNode(child, id);
          if (found) return found;
        }
      }
      return null;
    }

    const rootNode = findNode(treeData, rootId);
    if (rootNode && rootNode.fills && rootNode.fills.length > 0) {
      const fill = rootNode.fills[0];
      if (fill.type === "SOLID" && fill.color) {
        return fill.color;
      }
    }

    return "#ffffff"; // Fallback
  } catch (e) {
    console.error(
      "Warning: Could not auto-detect background color, using fallback.",
      e.message,
    );
    return "#ffffff";
  }
}

try {
  console.log("🚀 Starting Dynamic Token Mapping...");

  // 1. Auto-detect Background using Visual Dominant Logic
  const detectedBg = getBackgroundColor();
  console.log(`🔍 Auto-detected Background Color: ${detectedBg}`);

  // 2. Read all available colors
  let colors = [];
  if (fs.existsSync(colorsPath)) {
    const colorData = JSON.parse(fs.readFileSync(colorsPath, "utf8"));
    colors = colorData.colors || [];
  }

  const tokens = {
    colors: {},
    background: detectedBg,
  };

  // 3. Map colors and identify background token
  colors.forEach((c, index) => {
    const hex = c.color;
    let name = `color-${index + 1}`;

    // If this color matches our detected background, give it a semantic name
    if (hex.toLowerCase() === detectedBg.toLowerCase()) {
      name = "background";
    }

    tokens.colors[name] = hex;
  });

  // Ensure 'background' exists even if not in the usage list
  if (!Object.values(tokens.colors).includes(detectedBg)) {
    tokens.colors["background"] = detectedBg;
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(tokens, null, 2));

  console.log(`✅ Tokens generated at: ${outputPath}`);
  console.log(`📊 Summary: ${colors.length} colors processed.`);
} catch (e) {
  console.error("❌ Critical Error:", e);
}
