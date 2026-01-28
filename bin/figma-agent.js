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
    console.error(`❌ Error copying ${src} to ${dest}:`, err.message);
    return false;
  }
}

async function main() {
  console.log("\n🚀 Starting @ckim03/figma-agent installation...\n");

  // 1. Check if we are in a valid directory
  if (fs.existsSync(path.join(targetDir, ".agent"))) {
    console.log(
      "⚠️  Warning: .agent folder already exists. Some files might be overwritten.",
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

  // 4. Run the initialization script for figma-agent data folders
  const initScript = path.join(
    agentDest,
    "skills/figma-analysis/scripts/init-figma-agents.js",
  );
  if (fs.existsSync(initScript)) {
    console.log("📦 Initializing project data structure...");
    try {
      execSync(`node "${initScript}"`, { stdio: "inherit" });
    } catch (err) {
      console.error(
        "⚠️  Data initialization script failed, but skills were copied.",
      );
    }
  }

  console.log("\n✨ INSTALLATION COMPLETE! ✨\n");
  console.log("Your project is now equipped with Figma-to-Code powers.");
  console.log("Try using these commands in the Antigravity chat:");
  console.log("  /figma-review    - Extract design system tokens");
  console.log("  /get-figma-info  - Deep dive into a specific UI section");
  console.log("  /figma-build     - Generate React/HTML code from Figma");
  console.log(
    "  /figma-audit     - Audit existing code against Figma design\n",
  );
}

main();
