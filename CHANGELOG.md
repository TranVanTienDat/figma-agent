# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-28

### Added

- ✅ Initial release of Figma Agent Integration Tool
- ✅ Global CLI tool `figma-agent` for initializing projects
- ✅ Figma analysis skill for extracting design specifications
- ✅ Figma-to-code skill for automated component generation
- ✅ Slash commands: `/figma-review`, `/figma-build`, `/figma-audit`, `/get-figma-info`
- ✅ GitHub-based installation support
- ✅ Complete documentation (README, INSTALL, QUICK_REFERENCE)

### Features

- **Design Token Extraction**: Colors, typography, effects
- **Deep Data Extraction**: Layout, auto-layout, DOM tree analysis
- **Code Generation**: React/Next.js components
- **Design-to-Code Audit**: Pixel-perfect comparison
- **Metadata Tracking**: Selection links for traceability

---

## Installation

Install globally from GitHub:

```bash
npm install -g git+https://github.com/TranVanTienDat/figma-agent.git
```

## Usage

After installation, run in any project:

```bash
figma-agent
```

See [README.md](README.md) for full documentation.
