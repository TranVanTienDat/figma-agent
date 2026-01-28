---
description: Initialize project context - Create AGENTS.md with tech stack and standards
---

# Project Initialization Workflow

This workflow sets up the mandatory `AGENTS.md` file which serves as the Single Source of Truth for all AI interactions in this project.

## Steps

### 1. Gather Project Information

Ask the user for the following details:

- **Project Name & Description**: What is this project about?
- **Tech Stack**:
  - Framework (e.g., Next.js, Vite, React)
  - Language (TypeScript/JavaScript)
  - Styling (Vanilla CSS, Tailwind, SCSS, etc.)
  - Component Library (Radix UI, Shadcn, etc.)
  - Icons (Lucide, Phosphor, etc.)
- **Folder Structure**: Preferred organization for components, assets, etc.
- **Coding Standards**: Linting rules, naming conventions (PascalCase for components, etc.)

### 2. Create AGENTS.md

Generate the `AGENTS.md` file in the project root with the following template:

```markdown
# Project Context: [Project Name]

## 📋 Overview

[Short description of the project]

## 🛠 Tech Stack

- **Framework**: [Framework]
- **Language**: [Language]
- **Styling**: [Styling Approach]
- **Icons**: [Icon Library]
- **State Management**: [Library]

## 📁 Repository Structure

- `src/components/`: Reusable UI components
- `src/hooks/`: Custom React hooks
- `src/styles/`: Global styles and tokens
- `figma-agent/`: Extracted design data and section specs
- ...

## 🎨 Coding Standards

- **Naming**: PascalCase for components, camelCase for variables/functions.
- **Styles**: Use [Styling Approach] (e.g., HSL tokens for colors).
- **Types**: Mandatory TypeScript for all components and utilities.
- **Documentation**: Use JSDoc for complex logic.

## 🤖 AI Instructions

- All design-to-code tasks MUST read `figma-agent/` data.
- Follow the structure defined in `.agent/skills/figma-analysis/SKILL.md`.
- Prioritize pixel-perfection based on `specs.md`.
```

### 3. Verify and Confirm

- Show the generated `AGENTS.md` to the user.
- Confirm if any adjustments are needed.
- Remind the user that all future workflows (`/figma-review`, `/figma-build`, etc.) will reference this file.

## Output

A complete `AGENTS.md` file in the project root.
