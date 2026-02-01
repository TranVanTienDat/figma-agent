#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { select } = require("@inquirer/prompts");

// Color functions for CommonJS compatibility
const colors = {
  bold: (str) => `\x1b[1m${str}\x1b[0m`,
  green: (str) => `\x1b[32m${str}\x1b[0m`,
  cyan: (str) => `\x1b[36m${str}\x1b[0m`,
  yellow: (str) => `\x1b[33m${str}\x1b[0m`,
};

const targetDir = process.cwd();
const packageDir = path.join(__dirname, "..");

/**
 * Create interactive menu to select tool
 */
async function showToolMenu() {
  const tool = await select({
    message: "Select a tool to configure",
    choices: [
      {
        name: "Antigravity",
        value: "antigravity",
        description: "Antigravity AI Agent",
      },
      { name: "Copilot", value: "copilot", description: "GitHub Copilot" },
    ],
    pageSize: 10,
  });

  return tool;
}

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
    console.error(
      `${red}❌ Error copying ${src} to ${reset}${dest}:`,
      err.message,
    );
    return false;
  }
}

/**
 * Rename workflow files to .prompt.md format for Copilot
 */
function renameWorkflowFilesToPrompt(destDir) {
  try {
    if (!fs.existsSync(destDir)) {
      return false;
    }

    const entries = fs.readdirSync(destDir, { withFileTypes: true });
    for (let entry of entries) {
      const fullPath = path.join(destDir, entry.name);

      if (entry.isDirectory()) {
        // Recursively process subdirectories
        renameWorkflowFilesToPrompt(fullPath);
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        // Rename .md files to .prompt.md
        const newName = entry.name.replace(/\.md$/, ".prompt.md");
        const newPath = path.join(destDir, newName);
        fs.renameSync(fullPath, newPath);
        console.log(`✅ Renamed: ${entry.name} → ${newName}`);
      }
    }
    return true;
  } catch (err) {
    console.error(
      `❌ Error renaming workflow files in ${destDir}:`,
      err.message,
    );
    return false;
  }
}

/**
 * Initialize Figma Agent structure for Antigravity
 */
function initFigmaAgentStructureAntigravity(destDir) {
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

  // 3. Create project.md
  const srcConfigPath = path.join(packageDir, "figma-agent", "project.md");
  const destConfigPath = path.join(figmaAgentDir, "project.md");

  if (fs.existsSync(srcConfigPath)) {
    if (!fs.existsSync(destConfigPath)) {
      fs.copyFileSync(srcConfigPath, destConfigPath);
      console.log("✅ Created: figma-agent/project.md");
    } else {
      console.log("⏭️  Exists: figma-agent/project.md");
    }
  } else {
    console.warn("⚠️  Warning: Template project.md not found in package.");
  }
}

/**
 * Initialize Figma Agent structure for Copilot
 */
function initFigmaAgentStructureCopilot(destDir) {
  // 1. Create .github directories
  const githubDir = path.join(destDir, ".github");
  const skillsDir = path.join(githubDir, "skills");
  const promptsDir = path.join(githubDir, "prompts");

  if (!fs.existsSync(skillsDir)) {
    fs.mkdirSync(skillsDir, { recursive: true });
    console.log("✅ Created: .github/skills/");
  }

  if (!fs.existsSync(promptsDir)) {
    fs.mkdirSync(promptsDir, { recursive: true });
    console.log("✅ Created: .github/prompts/");
  }

  // 2. Create figma-agent directory for data
  const figmaAgentDir = path.join(destDir, "figma-agent");
  const folders = ["data", "common"];
  folders.forEach((folder) => {
    const folderPath = path.join(figmaAgentDir, folder);
    if (!fs.existsSync(folderPath)) {
      fs.mkdirSync(folderPath, { recursive: true });
      console.log(`✅ Created: figma-agent/${folder}/`);
    }
  });

  // 3. Create project.md
  const srcConfigPath = path.join(packageDir, "figma-agent", "project.md");
  const destConfigPath = path.join(figmaAgentDir, "project.md");

  if (fs.existsSync(srcConfigPath)) {
    if (!fs.existsSync(destConfigPath)) {
      fs.copyFileSync(srcConfigPath, destConfigPath);
      console.log("✅ Created: figma-agent/project.md");
    } else {
      console.log("⏭️  Exists: figma-agent/project.md");
    }
  } else {
    console.warn("⚠️  Warning: Template project.md not found in package.");
  }
}

async function main() {
  console.log(
    `\n🚀 ${colors.bold("Starting @ckim03/figma-agent installation...")}\n`,
  );

  // 1. Show tool selection menu
  const selectedTool = await showToolMenu();

  console.log(
    `\n${colors.bold(colors.green(`✓ Selected: ${selectedTool.toUpperCase()}`))}}\n`,
  );

  // 2. Check if we are in a valid directory
  let agentFolderExists = false;
  if (selectedTool === "antigravity") {
    agentFolderExists = fs.existsSync(path.join(targetDir, ".agent"));
  } else {
    agentFolderExists = fs.existsSync(path.join(targetDir, ".github"));
  }

  if (agentFolderExists) {
    console.warn(
      `${colors.yellow("⚠️  Warning: Agent folder already exists. Some files might be overwritten.")}`,
    );
  }

  // 3. Identify source folders and copy based on tool
  const agentSrc = path.join(packageDir, ".agent");

  if (!fs.existsSync(agentSrc)) {
    console.error("❌ Could not find .agent source directory in the package.");
    process.exit(1);
  }

  if (selectedTool === "antigravity") {
    // Antigravity: Copy to .agent/
    const agentDest = path.join(targetDir, ".agent");

    // Skip if already in the package directory
    if (targetDir === packageDir) {
      console.log("✅ Already in package directory, skipping .agent copy");
    } else {
      console.log("📁 Copying AI skills and workflows for Antigravity...");
      if (copyDir(agentSrc, agentDest)) {
        console.log("✅ AI configuration installed for Antigravity.");
      }
    }
  } else {
    // Copilot: Copy skills to .github/skills and workflows to .github/prompts
    const skillsSrc = path.join(agentSrc, "skills");
    const promptsSrc = path.join(agentSrc, "workflows");

    console.log("📁 Copying AI skills and workflows for Copilot...");

    if (fs.existsSync(skillsSrc)) {
      const skillsDest = path.join(targetDir, ".github", "skills");
      if (copyDir(skillsSrc, skillsDest)) {
        console.log("✅ Skills installed to .github/skills/");
      }
    }

    if (fs.existsSync(promptsSrc)) {
      const promptsDest = path.join(targetDir, ".github", "prompts");
      if (copyDir(promptsSrc, promptsDest)) {
        console.log("✅ Workflows installed to .github/prompts/");
        // Rename workflow files to .prompt.md format
        console.log("🔄 Renaming workflow files to .prompt.md format...");
        if (renameWorkflowFilesToPrompt(promptsDest)) {
          console.log("✅ Workflow files renamed successfully!");
        }
      }
    }
  }

  // 4. Initialize structure and config
  console.log("📦 Initializing project data structure...");
  if (selectedTool === "antigravity") {
    initFigmaAgentStructureAntigravity(targetDir);
  } else {
    initFigmaAgentStructureCopilot(targetDir);
  }

  console.log(
    `\n${colors.bold(colors.green("✨ INSTALLATION COMPLETE! ✨"))}\n`,
  );
  console.log(
    `${colors.bold("Your project is now equipped with Figma-to-Code powers.")}`,
  );

  if (selectedTool === "antigravity") {
    console.log(`\n${colors.bold("Antigravity Commands:")}`);
    console.log(
      `  ${colors.cyan("/figma-config")}     - Auto-configure project context & rules`,
    );
    console.log(
      `  ${colors.cyan("/sync-figma-data")}  - Sync latest data from your Figma Design`,
    );
    console.log(
      `  ${colors.cyan("/figma-build")}      - Generate React/Next.js code from Figma\n`,
    );
  } else {
    console.log(`\n${colors.bold("Copilot Instructions:")}`);
    console.log(`  ${colors.cyan("Skills")} are available in: .github/skills/`);
    console.log(
      `  ${colors.cyan("Prompts")} are available in: .github/prompts/`,
    );
    console.log(
      `  Configure your Copilot workspace with the prompts and skills above.\n`,
    );
  }
}

main();
