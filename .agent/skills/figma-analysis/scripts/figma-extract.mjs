/**
 * Figma REST API - Deep Extract v3.0
 *
 * Features:
 * - Full Node Tree extraction (no truncation)
 * - Variables API (Design Tokens) - Enterprise only
 * - Styles API (Typography & Effects)
 * - Components API (Component metadata)
 * - Images API (Icon export)
 * - Enriched tree with token names mapped from boundVariables
 *
 * Usage:
 * 1. Add your Figma token to .env.figma file
 * 2. Set FIGMA_FILE_KEY and TARGET_NODE_ID below
 * 3. Run: node scripts/figma-extract.mjs
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ============================================
// CONFIGURATION - Edit these values
// ============================================
const FIGMA_FILE_KEY = "i2JD5CfMgttyQqmDY5v72Z";
const TARGET_NODE_ID = "52:184";
// Optional: Node IDs to export as SVG icons (comma-separated or empty array)
const ICON_NODE_IDS = [];
// ============================================

// Load token from .env.figma
function loadEnv() {
  try {
    const envPath = resolve(__dirname, "../.env.figma");
    const envContent = readFileSync(envPath, "utf-8");
    const lines = envContent.split("\n");
    for (const line of lines) {
      if (line.startsWith("#") || !line.includes("=")) continue;
      const [key, ...valueParts] = line.split("=");
      const value = valueParts.join("=").trim();
      if (
        key.trim() === "FIGMA_TOKEN" &&
        value &&
        value !== "your_token_here"
      ) {
        return value;
      }
    }
  } catch (e) {
    // File not found
  }
  return process.env.FIGMA_TOKEN;
}

const FIGMA_TOKEN = loadEnv();

if (!FIGMA_TOKEN || FIGMA_TOKEN === "your_token_here") {
  console.error("❌ Please set FIGMA_TOKEN in .env.figma file");
  console.log("   1. Open .env.figma");
  console.log('   2. Replace "your_token_here" with your actual token');
  console.log(
    "   Get token from: https://www.figma.com/developers/api#access-tokens",
  );
  process.exit(1);
}

const API_BASE = "https://api.figma.com/v1";

// ============================================
// API FETCH FUNCTIONS
// ============================================

async function fetchFigma(endpoint) {
  const url = `${API_BASE}${endpoint}`;
  console.log(`📡 Fetching: ${endpoint}`);

  const response = await fetch(url, {
    headers: {
      "X-Figma-Token": FIGMA_TOKEN,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Figma API error: ${response.status} ${response.statusText}\n${errorText}`,
    );
  }

  return response.json();
}

// 1. Fetch Node Tree
async function fetchNodeTree(fileKey, nodeId) {
  const encodedNodeId = encodeURIComponent(nodeId);
  return fetchFigma(
    `/files/${fileKey}/nodes?ids=${encodedNodeId}&geometry=paths&plugin_data=shared`,
  );
}

// 2. Fetch Local Variables (Enterprise Only)
async function fetchLocalVariables(fileKey) {
  try {
    return await fetchFigma(`/files/${fileKey}/variables/local`);
  } catch (error) {
    if (error.message.includes("403") || error.message.includes("Limited")) {
      console.log("⚠️  Variables API not available (requires Enterprise plan)");
      return null;
    }
    throw error;
  }
}

// 3. Fetch File Styles
async function fetchFileStyles(fileKey) {
  try {
    return await fetchFigma(`/files/${fileKey}/styles`);
  } catch (error) {
    console.log("⚠️  Styles API error:", error.message);
    return null;
  }
}

// 4. Fetch File Components
async function fetchFileComponents(fileKey) {
  try {
    return await fetchFigma(`/files/${fileKey}/components`);
  } catch (error) {
    console.log("⚠️  Components API error:", error.message);
    return null;
  }
}

// 5. Export Images (Icons)
async function exportImages(fileKey, nodeIds, format = "svg", scale = 1) {
  if (!nodeIds || nodeIds.length === 0) return null;
  const ids = nodeIds.join(",");
  return fetchFigma(
    `/images/${fileKey}?ids=${encodeURIComponent(ids)}&format=${format}&scale=${scale}`,
  );
}

// ============================================
// TREE EXTRACTION & ENRICHMENT
// ============================================

function rgbaToHex(color) {
  if (!color) return null;
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  const a = color.a !== undefined ? color.a : 1;
  if (a === 1) {
    return `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
  }
  return `rgba(${r}, ${g}, ${b}, ${a.toFixed(2)})`;
}

function extractNodeTree(
  node,
  variablesMap = {},
  componentsMap = {},
  depth = 0,
) {
  const result = {
    id: node.id,
    name: node.name,
    type: node.type,
    // Layout properties
    layout: {
      width: node.absoluteBoundingBox?.width,
      height: node.absoluteBoundingBox?.height,
      x: node.absoluteBoundingBox?.x,
      y: node.absoluteBoundingBox?.y,
    },
    // Style properties
    styles: {},
    // Bound variables (token references)
    boundVariables: {},
    // Children
    children: [],
  };

  // Extract boundVariables and enrich with token names
  if (node.boundVariables) {
    for (const [prop, binding] of Object.entries(node.boundVariables)) {
      if (Array.isArray(binding)) {
        result.boundVariables[prop] = binding.map((b) => ({
          id: b.id,
          type: b.type,
          tokenName: variablesMap[b.id]?.name || null,
          tokenValue: variablesMap[b.id]?.value || null,
        }));
      } else if (binding.id) {
        result.boundVariables[prop] = {
          id: binding.id,
          type: binding.type,
          tokenName: variablesMap[binding.id]?.name || null,
          tokenValue: variablesMap[binding.id]?.value || null,
        };
      }
    }
  }

  // Extract fills (background)
  if (node.fills && node.fills.length > 0) {
    result.styles.fills = node.fills.map((fill) => ({
      type: fill.type,
      color: fill.color ? rgbaToHex(fill.color) : null,
      opacity: fill.opacity,
      gradientStops: fill.gradientStops?.map((stop) => ({
        color: rgbaToHex(stop.color),
        position: stop.position,
      })),
      visible: fill.visible,
    }));
  }

  // Extract strokes (border)
  if (node.strokes && node.strokes.length > 0) {
    result.styles.strokes = node.strokes.map((stroke) => ({
      type: stroke.type,
      color: stroke.color ? rgbaToHex(stroke.color) : null,
    }));
    result.styles.strokeWeight = node.strokeWeight;
    result.styles.strokeAlign = node.strokeAlign;
  }

  // Extract corner radius
  if (node.cornerRadius !== undefined) {
    result.styles.cornerRadius = node.cornerRadius;
  }
  if (node.rectangleCornerRadii) {
    result.styles.rectangleCornerRadii = node.rectangleCornerRadii;
  }

  // Extract effects (shadows, blur)
  if (node.effects && node.effects.length > 0) {
    result.styles.effects = node.effects.map((effect) => ({
      type: effect.type,
      color: effect.color ? rgbaToHex(effect.color) : null,
      offset: effect.offset,
      radius: effect.radius,
      spread: effect.spread,
      visible: effect.visible,
    }));
  }

  // Extract padding/layout
  if (node.paddingLeft !== undefined) {
    result.styles.padding = {
      top: node.paddingTop,
      right: node.paddingRight,
      bottom: node.paddingBottom,
      left: node.paddingLeft,
    };
  }

  // Extract gap
  if (node.itemSpacing !== undefined) {
    result.styles.gap = node.itemSpacing;
  }

  // Extract layout mode
  if (node.layoutMode) {
    result.styles.layoutMode = node.layoutMode;
    result.styles.primaryAxisAlignItems = node.primaryAxisAlignItems;
    result.styles.counterAxisAlignItems = node.counterAxisAlignItems;
    result.styles.layoutSizingHorizontal = node.layoutSizingHorizontal;
    result.styles.layoutSizingVertical = node.layoutSizingVertical;
    result.styles.layoutWrap = node.layoutWrap;
  }

  // Extract opacity
  if (node.opacity !== undefined && node.opacity !== 1) {
    result.styles.opacity = node.opacity;
  }

  // Extract text styles
  if (node.type === "TEXT") {
    result.styles.text = {
      characters: node.characters,
      fontSize: node.style?.fontSize,
      fontFamily: node.style?.fontFamily,
      fontWeight: node.style?.fontWeight,
      lineHeightPx: node.style?.lineHeightPx,
      letterSpacing: node.style?.letterSpacing,
      textAlignHorizontal: node.style?.textAlignHorizontal,
      textAlignVertical: node.style?.textAlignVertical,
    };
  }

  // Extract component reference for INSTANCE nodes
  if (node.type === "INSTANCE" && node.componentId) {
    result.componentId = node.componentId;
    result.componentName = componentsMap[node.componentId]?.name || null;
    result.componentDescription =
      componentsMap[node.componentId]?.description || null;
  }

  // Extract style references
  if (node.styles) {
    result.styleRefs = node.styles;
  }

  // Recursively extract children
  if (node.children && node.children.length > 0) {
    result.children = node.children.map((child) =>
      extractNodeTree(child, variablesMap, componentsMap, depth + 1),
    );
  }

  return result;
}

// Build variables lookup map
function buildVariablesMap(variablesData) {
  if (!variablesData?.meta?.variables) return {};

  const map = {};
  const collections = variablesData.meta.variableCollections || {};

  for (const [id, variable] of Object.entries(variablesData.meta.variables)) {
    const collection = collections[variable.variableCollectionId];
    const defaultModeId = collection?.defaultModeId;
    const value = variable.valuesByMode?.[defaultModeId];

    map[id] = {
      name: variable.name,
      resolvedType: variable.resolvedType,
      value:
        variable.resolvedType === "COLOR" && value ? rgbaToHex(value) : value,
      codeSyntax: variable.codeSyntax?.WEB || null,
      collectionName: collection?.name || null,
    };
  }

  return map;
}

// Build components lookup map
function buildComponentsMap(componentsData) {
  if (!componentsData?.meta?.components) return {};

  const map = {};
  for (const component of componentsData.meta.components) {
    map[component.node_id] = {
      key: component.key,
      name: component.name,
      description: component.description,
      containingFrame: component.containing_frame?.name,
    };
  }

  return map;
}

function printTree(node, depth = 0) {
  const indent = "  ".repeat(depth);
  const size =
    node.layout.width && node.layout.height
      ? `${Math.round(node.layout.width)}x${Math.round(node.layout.height)}`
      : "";

  let extras = [];

  // Print bound variables
  if (Object.keys(node.boundVariables).length > 0) {
    const tokens = Object.entries(node.boundVariables)
      .map(([prop, binding]) => {
        if (Array.isArray(binding)) {
          return binding
            .filter((b) => b.tokenName)
            .map((b) => `${prop}:${b.tokenName}`)
            .join(", ");
        }
        return binding.tokenName ? `${prop}:${binding.tokenName}` : null;
      })
      .filter(Boolean);
    if (tokens.length > 0) extras.push(`🎨 ${tokens.join(", ")}`);
  }

  // Print component name for instances
  if (node.componentName) {
    extras.push(`📦 ${node.componentName}`);
  }

  console.log(`${indent}├─ [${node.id}] ${node.name} (${node.type}) ${size}`);
  if (extras.length > 0) {
    console.log(`${indent}   ${extras.join(" | ")}`);
  }

  // Print key styles
  if (node.styles.fills?.length > 0) {
    const bg = node.styles.fills
      .filter((f) => f.visible !== false)
      .map((f) => f.color || f.type)
      .join(", ");
    if (bg) console.log(`${indent}   bg: ${bg}`);
  }
  if (node.styles.cornerRadius) {
    console.log(`${indent}   radius: ${node.styles.cornerRadius}px`);
  }
  if (node.styles.effects?.length > 0) {
    const effects = node.styles.effects
      .filter((e) => e.visible !== false)
      .map((e) => e.type)
      .join(", ");
    if (effects) console.log(`${indent}   effects: ${effects}`);
  }
  if (node.styles.text) {
    const preview =
      node.styles.text.characters?.substring(0, 30) +
      (node.styles.text.characters?.length > 30 ? "..." : "");
    console.log(
      `${indent}   text: "${preview}" (${node.styles.text.fontSize}px)`,
    );
  }

  // Recurse
  if (node.children) {
    node.children.forEach((child) => printTree(child, depth + 1));
  }
}

function countNodes(node) {
  let count = 1;
  if (node.children) {
    node.children.forEach((child) => (count += countNodes(child)));
  }
  return count;
}

// ============================================
// MAIN EXECUTION
// ============================================

async function main() {
  console.log("\n🚀 Figma Deep Extract v3.0\n");
  console.log("=".repeat(50));

  try {
    // Create debug folder
    const debugDir = resolve(__dirname, "../.figma-debug");
    if (!existsSync(debugDir)) {
      mkdirSync(debugDir, { recursive: true });
    }

    // 1. Fetch Node Tree
    console.log("\n📦 Step 1/5: Fetching Node Tree...");
    const nodeData = await fetchNodeTree(FIGMA_FILE_KEY, TARGET_NODE_ID);
    const node = nodeData.nodes[TARGET_NODE_ID];
    if (!node || !node.document) {
      throw new Error("Node not found in response");
    }

    // Save raw node data
    const rawPath = resolve(debugDir, "node-tree-raw.json");
    writeFileSync(rawPath, JSON.stringify(nodeData, null, 2));
    console.log(`   ✅ Raw node data saved`);

    // 2. Fetch Variables (Enterprise)
    console.log("\n🎨 Step 2/5: Fetching Variables (Design Tokens)...");
    const variablesData = await fetchLocalVariables(FIGMA_FILE_KEY);
    let variablesMap = {};
    if (variablesData) {
      const variablesPath = resolve(debugDir, "variables.json");
      writeFileSync(variablesPath, JSON.stringify(variablesData, null, 2));
      variablesMap = buildVariablesMap(variablesData);
      console.log(`   ✅ Found ${Object.keys(variablesMap).length} variables`);
    } else {
      console.log(`   ⚠️  Skipped (use MCP get_variable_defs as fallback)`);
    }

    // 3. Fetch Styles
    console.log("\n📝 Step 3/5: Fetching Styles (Typography & Effects)...");
    const stylesData = await fetchFileStyles(FIGMA_FILE_KEY);
    if (stylesData) {
      const stylesPath = resolve(debugDir, "styles.json");
      writeFileSync(stylesPath, JSON.stringify(stylesData, null, 2));
      const styleCount = stylesData.meta?.styles?.length || 0;
      console.log(`   ✅ Found ${styleCount} styles`);
    }

    // 4. Fetch Components
    console.log("\n🧩 Step 4/5: Fetching Components...");
    const componentsData = await fetchFileComponents(FIGMA_FILE_KEY);
    let componentsMap = {};
    if (componentsData) {
      const componentsPath = resolve(debugDir, "components.json");
      writeFileSync(componentsPath, JSON.stringify(componentsData, null, 2));
      componentsMap = buildComponentsMap(componentsData);
      console.log(
        `   ✅ Found ${Object.keys(componentsMap).length} components`,
      );
    }

    // 5. Export Icons (if configured)
    if (ICON_NODE_IDS.length > 0) {
      console.log("\n🖼️  Step 5/5: Exporting Icons...");
      const imagesData = await exportImages(
        FIGMA_FILE_KEY,
        ICON_NODE_IDS,
        "svg",
      );
      if (imagesData?.images) {
        const assetsDir = resolve(debugDir, "assets");
        if (!existsSync(assetsDir)) {
          mkdirSync(assetsDir, { recursive: true });
        }
        // Note: This returns URLs, you'd need to download them
        const iconsPath = resolve(debugDir, "icons-urls.json");
        writeFileSync(iconsPath, JSON.stringify(imagesData, null, 2));
        console.log(
          `   ✅ Icon URLs saved (${Object.keys(imagesData.images).length} icons)`,
        );
      }
    } else {
      console.log(
        "\n🖼️  Step 5/5: Skipping icon export (no ICON_NODE_IDS configured)",
      );
    }

    // Extract enriched tree
    console.log(
      "\n🔄 Processing: Creating enriched tree with token mappings...",
    );
    const enrichedTree = extractNodeTree(
      node.document,
      variablesMap,
      componentsMap,
    );

    // Save enriched tree
    const enrichedPath = resolve(debugDir, "enriched-tree.json");
    writeFileSync(enrichedPath, JSON.stringify(enrichedTree, null, 2));
    console.log(`   ✅ Enriched tree saved`);

    // Also save to legacy path for compatibility
    const legacyPath = resolve(__dirname, "../figma-node-tree.json");
    writeFileSync(legacyPath, JSON.stringify(enrichedTree, null, 2));

    // Print tree summary
    console.log("\n" + "=".repeat(50));
    console.log("📦 Node Tree Structure:");
    console.log("=".repeat(50) + "\n");
    printTree(enrichedTree);

    // Summary
    console.log("\n" + "=".repeat(50));
    console.log("📊 SUMMARY");
    console.log("=".repeat(50));
    console.log(`   Total nodes: ${countNodes(enrichedTree)}`);
    console.log(`   Variables: ${Object.keys(variablesMap).length}`);
    console.log(`   Components: ${Object.keys(componentsMap).length}`);
    console.log(`\n📁 Output files in: .figma-debug/`);
    console.log("   - enriched-tree.json (USE THIS!)");
    console.log("   - node-tree-raw.json");
    console.log("   - variables.json");
    console.log("   - styles.json");
    console.log("   - components.json");
    console.log(
      "\n✨ Done! Now use MCP to get CSS snippets and screenshots.\n",
    );
  } catch (error) {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  }
}

main();
