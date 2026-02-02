# Figma Analysis Scripts - Setup Guide

This directory contains Node.js scripts for deep Figma data extraction and analysis.

## 📋 Prerequisites

- **Node.js**: Version 14 or higher
- **Figma Personal Access Token**: Required for API access

### 🚀 How to Install Node.js

**macOS** (using Homebrew):

```bash
brew install node
```

**Windows**:
Download the installer from [nodejs.org](https://nodejs.org/). Choose the LTS version.

**Linux (Ubuntu/Debian)**:

```bash
sudo apt update
sudo apt install nodejs npm
```

## 🚀 Quick Setup

### Step 1: Configure Figma Access Token

Create a `.env.figma` file in the project root:

```bash
touch .env.figma
```

Add your token:

```env
FIGMA_TOKEN=your_personal_access_token_here
```

**Security**: Add to `.gitignore`:

```bash
echo ".env.figma" >> .gitignore
```

### Step 2: Get Your Figma Personal Access Token

1. Open Figma and go to **Settings** (click your profile picture)
2. Scroll to **Personal access tokens**
3. Click **Generate new token**
4. Give it a name (e.g., "Figma Agent Tool")
5. **Copy the token** (it only shows once!)
6. Paste it into your `.env.figma` file

## 📝 Available Scripts

### 1. `figma-extract.mjs` (⭐ Main Script)

Deep extraction of Figma nodes with token mapping.

**Features:**

- ✅ Full node tree extraction (no truncation)
- ✅ Variables API (Design Tokens - Enterprise)
- ✅ Styles API (Typography & Effects)
- ✅ Components API (metadata)
- ✅ Images export (SVG icons)
- ✅ Bound variables enriched with token names

**Configuration:**

Edit `figma-extract.mjs` and set these values:

```javascript
const FIGMA_FILE_KEY = "i2JD5CfMgttyQqmDY5v72Z"; // Your design file
const TARGET_NODE_ID = "52:184"; // Node to extract
const ICON_NODE_IDS = []; // Optional: IDs to export as SVG
```

**Usage:**

```bash
node figma-extract.mjs
```

**Output:** `.figma-debug/`

- `enriched-tree.json` - Main output with token mappings
- `node-tree-raw.json` - Raw API response
- `variables.json` - Design tokens
- `styles.json` - Styles metadata
- `components.json` - Components metadata
- `icons-urls.json` - Icon URLs (if configured)

### 2. `init-figma-agents.js`

Initializes directory structure for a new page/section.

**Usage:**

```bash
node init-figma-agents.js [page-name] [section-name]

# Example:
node init-figma-agents.js landing-page hero-section
```

## 🔍 Verify Installation

Test if everything is set up correctly:

```bash
# Check Node version
node --version  # Should be 14+

# Check if token file exists
cat .env.figma | grep FIGMA_TOKEN

# Test fetch
node -e "console.log('Node.js works!')"
```

## ⚠️ Troubleshooting

### "command not found: node"

- Reinstall Node.js from [nodejs.org](https://nodejs.org/)
- On macOS with Homebrew: `brew install node`
- Make sure Node is in your PATH

### "FIGMA_TOKEN not found" or "401 Unauthorized"

- Verify `.env.figma` exists in project root
- Check token is correct (copy from Figma Settings again)
- Ensure `.env.figma` format: `FIGMA_TOKEN=token_here` (no spaces)

### "Request failed" or "403 Forbidden"

- Token may have expired - generate a new one
- Verify the Figma file is accessible with your account
- Check your internet connection

### Script timeout or hangs

- File may be very large - be patient, extraction takes time
- Check console output for progress messages
- Ctrl+C to stop and check logs

## 📚 Additional Resources

- [Figma REST API Documentation](https://developers.figma.com/docs/rest-api/)
- [How to get a Figma Personal Access Token](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)
- [Workflow Guide](../../workflows/sync-figma-data.md)
- [Build Guide](../../workflows/figma-build.md)

---

**Need help?** Check the main [INSTALL.md](../../../INSTALL.md) in the project root.
