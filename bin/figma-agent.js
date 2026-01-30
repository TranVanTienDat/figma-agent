#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const targetDir = process.cwd();
const packageDir = path.join(__dirname, "..");

/**
 * Copy directory recursively
 */
function copyDir(src, dest) {
  try {
    // fs.cpSync is available in Node 16.7.0+
    if (fs.cpSync) {
      fs.cpSync(src, dest, { recursive: true });
    } else {
      // Fallback for older Node versions (basic implementation)
      if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
      }
      const entries = fs.readdirSync(src, { withFileTypes: true });
      for (let entry of entries) {
        let srcPath = path.join(src, entry.name);
        let destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
          copyDir(srcPath, destPath);
        } else {
          fs.copyFileSync(srcPath, destPath);
        }
      }
    }
    return true;
  } catch (err) {
    const red = "\x1b[31m";
    const reset = "\x1b[0m";
    console.error(
      `${red}❌ Error copying ${src} to ${reset}${dest}:`,
      err.message,
    );
    return false;
  }
}

/**
 * Initialize Figma Agent structure
 */
function initFigmaAgentStructure(destDir) {
  const figmaAgentDir = path.join(destDir, "figma-agent");

  // 1. Create base directory
  if (!fs.existsSync(figmaAgentDir)) {
    fs.mkdirSync(figmaAgentDir, { recursive: true });
    console.log("✅ Created: figma-agent/");
  }

  // 2. Create subdirectories
  const folders = ["data", "common"];
  folders.forEach((folder) => {
    const folderPath = path.join(figmaAgentDir, folder);
    if (!fs.existsSync(folderPath)) {
      fs.mkdirSync(folderPath, { recursive: true });
      console.log(`✅ Created: figma-agent/${folder}/`);
    }
  });

  // 3. Create config.yaml
  const srcConfigPath = path.join(packageDir, "figma-agent", "config.yaml");
  const destConfigPath = path.join(figmaAgentDir, "config.yaml");

  if (fs.existsSync(srcConfigPath)) {
    if (!fs.existsSync(destConfigPath)) {
      fs.copyFileSync(srcConfigPath, destConfigPath);
      console.log("✅ Created: figma-agent/config.yaml");
    } else {
      console.log("⏭️  Exists: figma-agent/config.yaml");
    }
  } else {
    // Fallback if source file is missing (should not happen in correct build)
    console.warn("⚠️  Warning: Template config.yaml not found in package.");
  }
}

async function main() {
  const reset = "\x1b[0m";
  const bold = "\x1b[1m";
  const cyan = "\x1b[36m";
  const green = "\x1b[32m";
  const yellow = "\x1b[33m";

  console.log(
    `\n🚀 ${bold}Starting @ckim03/figma-agent installation...${reset}\n`,
  );

  // 1. Check if we are in a valid directory
  if (fs.existsSync(path.join(targetDir, ".agent"))) {
    console.warn(
      `${yellow}⚠️  Warning: .agent folder already exists. Some files might be overwritten.${reset}`,
    );
  }

  // 2. Identify source folders
  const agentSrc = path.join(packageDir, ".agent");
  const agentDest = path.join(targetDir, ".agent");

  // 3. Copy .agent folder
  if (fs.existsSync(agentSrc)) {
    console.log("📁 Copying AI skills and workflows...");
    if (copyDir(agentSrc, agentDest)) {
      console.log("✅ AI configuration installed.");
    }
  } else {
    console.error("❌ Could not find .agent source directory in the package.");
    process.exit(1);
  }

  // 4. Initialize structure and config
  console.log("📦 Initializing project data structure...");
  initFigmaAgentStructure(targetDir);

  console.log(`\n${bold}${green}✨ INSTALLATION COMPLETE! ✨${reset}\n`);
  console.log(
    `${bold}Your project is now equipped with Figma-to-Code powers.${reset}`,
  );
  console.log("\nTry using these commands in the Antigravity chat:");
  console.log(
    `  ${cyan}/figma-config${reset}     - Auto-configure project context & rules`,
  );
  console.log(
    `  ${cyan}/sync-figma-data${reset}  - Sync latest data from your Figma Design`,
  );
  console.log(
    `  ${cyan}/figma-map-tokens${reset} - Transform Figma styles into Design Tokens`,
  );
  console.log(
    `  ${cyan}/figma-build${reset}      - Generate React/Next.js code from Figma\n`,
  );
}

main();
