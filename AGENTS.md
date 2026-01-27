# Project Context & AI Guardrails

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Framer Motion (for animations)
- **Icons**: Lucide React
- **Components**: Radix UI (Headless components)

## Design System Preferences

- **Color Mode**: Dark Mode by default
- **Aesthetics**: Glassmorphism, Neon borders, Futuristic SaaS feel
- **Units**: Use `px` for spacing logic as per Figma, then convert to Tailwind classes.

## Coding Standards

- Use Arrow Functions for components.
- Modularize components: `components/sections/`, `components/ui/`, `components/layout/`.
- Strict Type safety for all props.
- Implement responsive design (Mobile-first).

## AI Instructions

1.  **Always read AGENTS.md** before generating code.
2.  Prioritize **Framer Motion** for all transitions and hover effects detected in Figma.
3.  Use **HSL** values for dynamic transparency if needed.
