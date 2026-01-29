# Figma to Code Technical Reference

## Code Style Best Practices

### Component Structure

1. **Container**: Handles layout, padding, and background.
2. **Inner Content**: Handles child alignment and gaps.
3. **Atoms**: Direct usage of system tokens.

### State Transitions

Always use CSS transitions for:

- `background-color`
- `color`
- `border-color`
- `opacity`
- `transform` (for hover scales/movements)

## Accessibility (A11y) Guide

| Element     | Requirement                                            |
| ----------- | ------------------------------------------------------ |
| Buttons     | `aria-label` if only icon. `type="button"` by default. |
| Navigation  | Use `<nav>` wrapper.                                   |
| Sidebar     | Use `<aside>` semantic tag.                            |
| Images      | `alt` text mandatory from `specs.md`.                  |
| Interaction | Support `:focus-visible` states.                       |

## Responsive Implementation

- Use `w-full` for "Fill Container" components.
- Use `flex-col md:flex-row` for responsive stack changes detected in analysis.
- Use CSS Variables from `common/` to ensure consistency.
