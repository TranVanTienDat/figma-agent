# Setup Guide - Figma Agent Integration Hub

Complete setup manual for the **@cam/figma-agent-int** toolset.

## 📋 Requirements

- **Antigravity AI**: Professional agentic coding assistant.
- **MCP Server**: `FigmaAIBridge` must be configured.
- **Node.js**: v18.0.0 or higher.
- **Python**: v3.9 or higher (for metadata analysis scripts).

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

### 2. Install Tool Globally (Recommended)

Run the following command to make the tool available everywhere:

```bash
npm install -g @ckim03/figma-agent
```

**Alternative Method** - Install from GitHub or clone locally:

```bash
# From GitHub
npm install -g git+https://github.com/TranVanTienDat/figma-agent.git

# Or clone and link
git clone https://github.com/TranVanTienDat/figma-agent.git
cd figma-agent
npm link
```

### 3. Initialize in Your New Project

Open your terminal in your new project directory and run:

```bash
figma-agent
```

This command will automatically:

1. Copy AI Skills (figma-analysis, figma-to-code) into the project.
2. Copy Slash Commands (`/figma-review`, `/figma-build`, etc.).
3. Initialize the `figma-agent/` directory structure for data storage.

### 4. Local Environment Configuration (.env)

For advanced metadata extraction and Python scripts, it is recommended to set up a local `.env` file in your project root.

1. **Install Python dependencies**:

   ```bash
   pip install python-dotenv requests
   ```

2. **Create a `.env` file**:

   ```bash
   touch .env
   ```

3. **Add your Figma Token**:
   ```env
   FIGMA_ACCESS_TOKEN=your_personal_access_token_here
   ```

**⚠️ Security Note**: Always add `.env` to your `.gitignore` to prevent leaking your Figma Token.

```bash
echo ".env" >> .gitignore
```

_Note: The metadata script will prioritize the `.env` file over system environment variables._

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
├── figma-agent/               # Data Assets
│   ├── common/                # Common Tokens (Colors, Typography)
│   └── pages/                 # Structured data organized by pages/[page-name]/[section-page]
├── .agent/
│   ├── skills/                # AI logic (AgentSkills.io spec)
│   │   ├── figma-analysis/
│   │   │   └── references/    # Technical guides
│   │   └── figma-to-code/
│   └── workflows/             # Automated slash commands
└── README.md
```

## 🐛 Common Fixes

- **"File not found"**: Ensure your Figma Selection Link contains both the `file key` and the `node-id`.
- **"Server Error"**: Check your internet connection and verify the `FIGMA_ACCESS_TOKEN`.
- **"Empty JSON"**: Make sure you have "Can View" or higher permissions on the Figma file.

---

**Build faster, build better. 🚀**
