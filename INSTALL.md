# Setup Guide - Figma Agent Integration Hub

Complete setup manual for the **@cam/figma-agent-int** toolset.

## 📋 Requirements

- **Antigravity AI**: Professional agentic coding assistant.
- **MCP Server**: `FigmaAIBridge` must be configured.
- **Node.js**: v18.0.0 or higher

## 🚀 Step-by-Step Installation

### 1. Configure MCP (Essential)

Ensure your `FigmaAIBridge` is linked to a valid Figma Personal Access Token.

**Location**: `~/.config/mcp/config.json`

```json
{
  "mcpServers": {
    "FigmaAIBridge": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your-figma-token"
      }
    }
  }
}
```

### 2. Verify AI Skills

Once the project is loaded, Antigravity identifies the following skills automatically:

- `figma-analysis`: Extracts design logic.
- `figma-to-code`: Generates React components.

### 3. Initialize Metadata Folders

Run the local script to establish the `figma-agent/` structure:

```bash
npm run init
```

## 🎯 Usage Flow

### Phase 1: Global Setup

Run `/figma-review [link]` to set the common design tokens (Colors, Typography).

### Phase 2: Metadata Extraction

Run `/get-figma-info [section-name] [link selection]` to populate the `data.json` for a specific UI section.

### Phase 3: Automated Build

Run `/figma-build [section-name] [link selection]` to output the final `.tsx` code.

## 📁 Project Directory Reference

```
.
├── figma-agent/               # Extracted Design System & Data
├── .agent/
│   ├── skills/                # AI logic definitions
│   └── workflows/             # Automated slash commands
└── README.md
```

## 🐛 Common Fixes

- **"File not found"**: Ensure your Figma Selection Link contains both the `file key` and the `node-id`.
- **"Server Error"**: Check your internet connection and verify the `FIGMA_ACCESS_TOKEN`.
- **"Empty JSON"**: Make sure you have "Can View" or higher permissions on the Figma file.

---

**Build faster, build better. 🚀**
