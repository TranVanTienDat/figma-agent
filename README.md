# 🚀 Figma Agent: Design-to-Code Powerhouse

Figma Agent is a powerful toolkit for Antigravity AI, enabling the conversion of specific Figma designs into high-quality, SEO-friendly, and maintainable React/Next.js source code. The tool focuses on pixel-perfect accuracy and performance optimization for large design files.

---

## 🛠 Installation

### 1. System Requirements

- **Node.js**: >= 18.0.0
- **Python**: 3.x (with `requests` and `python-dotenv` libraries)

### 2. Global Installation

Run the following command:

```bash
npm install -g @ckim03/figma-agent
```

### 3. Environment Configuration

You can configure the Token via a `.env` file or directly via the Terminal:

**Method 1: Using `.env` file (Recommended)**
Create a `.env` file in the project root:

```env
FIGMA_ACCESS_TOKEN=your_personal_access_token
```

**Method 2: Using Export command (Terminal)**

- **Set**: `export FIGMA_ACCESS_TOKEN=your_token`
- **Check**: `echo $FIGMA_ACCESS_TOKEN`
- **Remove**: `unset FIGMA_ACCESS_TOKEN`

### 4. Antigravity MCP Setup

Add the following configuration to your Antigravity settings to enable the Figma AI Bridge:

```json
{
  "mcpServers": {
    "FigmaAIBridge": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--stdio"],
      "env": {
        "FIGMA_API_KEY": "888"
      }
    }
  }
}
```

---

## 🔄 Standard Workflow

To achieve maximum efficiency, follow this 5-step process:

### Step 1: Initialization (First time)

In your project directory (where the Web code is located), run:

```bash
figma-agent
```

This command creates the `figma-agent/` directory - the AI's control center.

### Step 2: Tech Stack Setup

In the Antigravity chat, type:
**`/figma-config`**
The AI will analyze the project structure (Tailwind, TypeScript, etc.) to ensure the generated code is fully compatible.

### Step 3: Sync Figma Data

Download design data to your machine:
**`/sync-figma-data [Figma-Link]`**
_Tip: The tool supports Auto-Retry if it encounters Figma API limits (Rate Limit)._

### Step 4: Map Tokens (Optional)

Convert Styles from Figma into CSS/JSON variables:
**`/figma-map-tokens`**

### Step 5: Build UI

Start generating code using natural language:
**`/figma-build Build a responsive Header Section for me.`**

---

## 📂 `figma-agent/` Directory Structure

Centralized and transparent data management system:

- `project.md`: Contains project context (Tech Stack, coding rules, implementation status).
- `data/`: Raw data synced from Figma (styles, components, file structure).

---

## ⚡ Optimization for Large Projects

- **Partial Sync**: Use Node ID (in the Figma link) to sync only the part you need to work on, saving time and resources.
  - Example: `/sync-figma-data [Link]?node-id=5965:18603`
- **Context Awareness**: Whenever building, the AI will automatically read the **entire** `figma-agent/` directory to ensure the generated code matches the existing design system 100%.

---

## 👨‍💻 Author

Developed by **TranVanTienDat** 🚀
