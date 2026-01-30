---
description: Auto-configure figma-agent/config.yaml by analyzing the project
---

# Figma Agent Configuration Workflow

This workflow analyzes your project structure and dependencies to automatically populate the `figma-agent/config.yaml` file with the correct context.

## 1. Analyze Project Structure

- Read `package.json` to identify:
  - **Frameworks**: Next.js, React, Vue, Svelte, etc.
  - **Styling**: TailwindCSS, Styled Components, CSS Modules, Sass, etc.
  - **Language**: TypeScript (look for tsconfig.json) or JavaScript.
- Read `README.md` (if available) to understand the project's purpose and domain.
- Check for existing configuration files (e.g., `tailwind.config.js`, `tsconfig.json`) to confirm specific conventions.

## 2. Generate Context

Based on the analysis, construct a context string.

**Example Context Structure:**

```yaml
context: |
  Project: [Project Name from package.json]
  Summary: [Brief description]
  Tech Stack:
    - Framework: [Detected Framework]
    - Language: [TypeScript/JavaScript]
    - Styling: [Detected Styling Solution]
  Conventions:
    - [e.g. Use functional components]
    - [e.g. Mobile-first responsive design]
```

## 3. Update Configuration

1. Read the existing `figma-agent/config.yaml`.
2. Replace the commented-out `context` section with the generated context.
3. Suggest default best-practice rules for the `rules` section based on the project type (e.g., strict component structures for React).

## 4. Update .gitignore

- Check if `.gitignore` exists in the root directory.
- If it exists, check if `figma-agent` is already ignored.
- If not ignored, append `figma-agent` to `.gitignore`.
- If `.gitignore` does not exist, skip this step.

## 5. User Verification

- Show the proposed configuration to the user.
- Ask if they want to add any specific domain knowledge or custom rules.
