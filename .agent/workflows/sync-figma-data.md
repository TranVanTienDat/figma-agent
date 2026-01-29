---
description: Sync Core Figma Data
---

This workflow synchronizes the fundamental data from a Figma file into the `figma-agent/data` directory. It uses the improved Python `figma_core` to safely fetch data without overloading the API.

# Prerequisites

- Ensure `FIGMA_ACCESS_TOKEN` is set in your environment (or `.env`).
- You need the FILE_KEY of your Figma Design.

# Steps

1. Create the data directory if it doesn't exist.
   // turbo

```bash
mkdir -p figma-agent/data
```

2. Fetch the File Structure (Summary).
   _This gets the document tree (Pages, Frames) to understand the layout._
   _Replace <FILE_KEY> with your actual file key._

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py file <FILE_KEY> --depth 2 --output figma-agent/data/file-structure.json --summary
```

3. Fetch Published Components.
   _This gets the library of reusable components._

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py components <FILE_KEY> --output figma-agent/data/components.json
```

4. Fetch Published Styles (Design Tokens).
   _This gets the colors, typography, and effects._

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py styles <FILE_KEY> --output figma-agent/data/styles.json
```

5. (Optional) Fetch Image Fills.
   _Useful if you need to download assets later._

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py images <FILE_KEY> --output figma-agent/data/images.json
```
