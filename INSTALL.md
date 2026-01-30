# 📖 Detailed Installation Guide

This document guides you through setting up Figma Agent from scratch.

## 1. Prerequisites

- Ensure you have **Node.js 18+** installed.
- Install the required Python packages:
  ```bash
  pip3 install requests python-dotenv
  ```

## 2. Tool Installation

Navigate to the `build-tool` source directory and run:

```bash
npm install -g .
```

After this step, the `figma-agent` command will be available anywhere in your terminal.

## 3. Usage in New Projects

To integrate Figma capabilities into any web project:

1. **Initialize**: Run `figma-agent` in the project's root directory.
2. **Setup Token**: Create a `.env` file and add `FIGMA_ACCESS_TOKEN`.
3. **Config**: Run `/figma-config` in the chat to let the AI automatically detect the technology stack (Vite, Next.js, Tailwind, etc.).

## 4. Troubleshooting

- **403 Error**: Check your Token or Figma file access permissions.
- **429 Error (Rate Limit)**: Don't worry, the tool will automatically wait and retry. Please be patient.
- **.env file not found**: On Mac, if hidden files are blocked, ensure you run the command from within VS Code or grant "Full Disk Access" to the Terminal.

---

© 2026 Figma Agent Integration Hub.
