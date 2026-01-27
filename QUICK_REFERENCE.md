# 🚀 Quick Reference Guide

**Figma Agent Integration Tool** - Command and Structure Reference

---

## ⚡ Quick Commands

| Command           | Action                           | Usage                              |
| ----------------- | -------------------------------- | ---------------------------------- |
| `/figma-review`   | Initial analysis & global tokens | `/figma-review [link]`             |
| `/get-figma-info` | Targeted section deep dive       | `/get-figma-info [section] [link]` |
| `/figma-build`    | Generate code from data          | `/figma-build [section] [link]`    |
| `/figma-audit`    | Design-to-code audit             | `/figma-audit [section] [link]`    |

---

## 📁 Key Directories

| Directory                            | Content                                      |
| ------------------------------------ | -------------------------------------------- |
| `figma-agent/common/`                | Global tokens (Colors, Typography, Variants) |
| `figma-agent/[page]/section-[name]/` | Section-specific data (JSON, Specs, Images)  |
| `.agent/skills/`                     | AI logic for analysis and coding             |
| `.agent/workflows/`                  | Automated step-by-step processes             |

---

## 📄 Core Data Files (per section)

- **`data.json`**: The heart of the extraction. Contains layout, DOM structure, and component overrides.
- **`specs.md`**: Technical documentation including interaction states and accessibility.
- **`local-component.tsx`**: Boilerplate component code matching the design structure.
- **`images/`**: Standardized directory for SVG/PNG assets.

---

## 🎨 Token Reference

- **Colors**: `figma-agent/common/colors/system-colors.json`
- **Typography**: `figma-agent/common/typography/text-presets.json`
- **Global Variants**: `figma-agent/common/variants/global-variants.json`

---

## 🔧 Workflow Cheat Sheet

1. **Setup**: `/figma-review [link]` → Establishes the `figma-agent/` structure.
2. **Deep Dive**: `/get-figma-info hero [selection_link]` → Populates `hero/data.json`.
3. **Build**: `/figma-build hero [selection_link]` → Outputs `Hero.tsx` in your project.
4. **Audit**: `/figma-audit hero [link]` → Refines `Hero.tsx` for perfect matching.

---

## 🐛 Troubleshooting

- **Missing Overrides**: Check if you're selecting the component instance or the master.
- **Path Issues**: Ensure `figma-agent` is in your project root.
- **Empty Assets**: Verify the node ID in the selection link has valid fills/vectors.

---

**Made for professional developer workflows.**
