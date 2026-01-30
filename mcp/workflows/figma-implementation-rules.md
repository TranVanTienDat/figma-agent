---
description: Rules for implementing Figma designs to Code with pixel-perfect accuracy
---

# Figma to Code Implementation Rules

These rules must be followed strictly to avoid common implementation errors (spacing, colors, structure).

## 1. Structural Analysis (Layout & Spacing)

- **Do NOT guess Spacing**: Always identify the `Wrap` or `Container` Frame in Figma JSON.
  - Read `itemSpacing` (gap) directly from the parent container.
  - Read `padding` (top, right, bottom, left) directly from the parent container.
  - **Formula**: `Total Distance` = `Parent Padding` + `Parent Gap`.
- **Flex vs Padding**:
  - Prefer using `flex-col` + `gap` on the parent for distributing children.
  - Use `padding` on containers for internal breathing room.
  - Do not mix random margins if a parent gap exists.

## 2. Component Properties (Colors & Typography)

- **Explicit Color Verification**:
  - **Never assume Black**: Always check the `fills` property of Text and Vector nodes. Placeholder text is often `Secondary` or `Gray`, not `Primary`.
  - **Check all States**: Button backgrounds might be in a separate `Rectangle` node (with opacity/blur) behind the Icon/Text. Do not just export the inner Icon.
- **Glassmorphism & Shadows**:
  - If a Close Button or Modal has a blur, look for `effects: [{ type: "BACKGROUND_BLUR"... }]`.
  - Copy `shadow` values exactly (x, y, blur, spread, color/opacity).

## 3. Icons & Assets

- **Verify Icon Names**: Read the `name` of the `INSTANCE` node (e.g., `money-01`), not just the `VECTOR` child. This prevents semantic errors (e.g., using Calculator vs Banknote).

## 4. Alignment

- **Text Alignment**: Do not trust `textAlignHorizontal` alone. Check the Parent's `primaryAxisAlignItems` and `counterAxisAlignItems`.
- **Absolute vs Flex**: If an element is floating (like a Close button in a header), verify if it breaks the Flex flow. Use `absolute` positioning if the Title must remain centered relative to the container, not the siblings.

## Pre-Implementation Checklist

1. [ ] Have I checked the Parent Gap?
2. [ ] Have I checked the Parent Padding?
3. [ ] Did I verify the exact Hex/RGBA of purely decorative text (placeholders)?
4. [ ] Did I check if the Icon container has a background fill?
