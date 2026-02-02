---
description: Auto-configure figma-agent/project.yaml by analyzing the project
---

# Figma Agent Configuration Workflow

This workflow analyzes your project structure and dependencies to automatically populate the `figma-agent/project.yaml` file with the correct context.

**When to use**: Run this workflow when starting a new project integration or updating an existing project's configuration in figma-agent.

## 1. Analyze Project Structure

- Read `package.json` to identify:
  - **Frameworks**: Next.js, React, Vue, Svelte, etc.
  - **Styling**: TailwindCSS, Styled Components, CSS Modules, Sass, etc.
  - **Language**: TypeScript (look for tsconfig.json) or JavaScript.
- Read `README.md` (if available) to understand the project's purpose and domain.
- Check for existing configuration files (e.g., `tailwind.config.js`, `tsconfig.json`) to confirm specific conventions.

## 2. Update Configuration

1. Read the existing `figma-agent/project.yaml`.
2. Based on the analysis, update the corresponding sections in `project.yaml`:
   - **Section 1. Project Overview**: Fill in Name, Description (from package.json/README) and infer Domain.
   - **Section 2. Tech Stack**: Fill in Framework, Language, Styling, etc.
   - **Section 3. Coding Conventions & Rules**: Suggest default best-practice rules based on the project type (e.g., "Use functional components", "Mobile-first").

**Example Update:**

```markdown
## 2. Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: TailwindCSS
```

## 3. Update .gitignore

- Check if `.gitignore` exists in the root directory.
- If it exists:
  - Check if `figma-agent/` is already ignored.
  - If not ignored, append `figma-agent/` as a new line to `.gitignore`.
- If `.gitignore` does not exist, create it with `figma-agent/` as the first entry.

**Result**: The `.gitignore` file should contain:

```
figma-agent/
```

## 4. Verify Configuration

Before finalizing:

- ✅ Is `project.yaml` valid YAML?
- ✅ Is the tech stack detected correctly?
- ✅ Are there any conflicts or inconsistencies?
- ✅ Does the configuration match the actual project?

## 5. User Verification

- Show the updated content of `figma-agent/project.yaml` to the user.
- Ask if they want to add any specific domain knowledge or custom rules to the file.
