---
name: code-conversion-principles
description: Mandatory principles for processing fragmented Figma data and converting it to code.
version: 1.0.0
---

# Code Conversion Processing Principles

This skill defines the strict rules for handling fragmented Figma data (JSON split files) to ensure accurate code generation.

## ⚠️ Mandatory Reading

Before generating any code from `figma-agent/data`, you **MUST** read and apply the principles defined below.

## 1. Fragmented Data Processing Principles

In the `/figma-agent` structure, data is often split into hundreds of JSON files with random ID filenames. The mandatory rule is to perform **Content-based Scanning** instead of relying on filenames.

### 1.1. Dynamic File Classification (Zero-Reliance on Filenames)

The system **MUST NOT** rely on filenames (e.g., `01-structure.json`, `texts.json`) as they vary by sync version. Instead, perform an initial scan to classify files based on content:

- **Structure Files**: Files containing `"children"`, `"type": "FRAME"`, and `"absoluteBoundingBox"`.
- **Content Files**: Files containing a large array of strings or mapping IDs to text (Source of Truth for copy).
- **Style/Token Files**: Files containing `"styles"`, `"fills"`, or hex codes mapping to IDs.
- **Component Files**: Files containing `componentPropertyDefinitions`.

### 1.2. Dynamic ID Linking Principles

Absolutely do not process a file in isolation. Every node in Figma has cross-links:

- **Style Lookup:** When encountering a node with property `styles: { fill: "S:123..." }`, the system must search the entire directory for which file defines ID `S:123` to retrieve the correct color code.
- **Master Component Lookup:** When encountering `instanceId`, must scan other JSON files to find the correct `mainComponentId`. Otherwise, generated code will be garbage `div` tags instead of calling the reused Component.

### 1.5. Visual Dominance vs. Usage Frequency

When defining the primary background vs. foreground colors:

- **DO NOT** use the color with the highest usage count as the background.
- **MANDATORY**: The color of the Root Frame or the largest bounding box (e.g., Rectangle filling the screen) is the **Background Color**.
- Colors with high frequency but small total area (e.g., White text on Black background) must be classified as **Foreground/Contrast colors**.

---

### 1.4. The "Path-to-Node" Indexing Rule

Before deep analysis, the agent **MUST** create a memory map of `NodeID -> FilePath`.

1. Run a recursive scan of the directory.
2. For each JSON, identify the root `id` or the `ids` of its children.
3. Store this map. When a structure file references a child ID that isn't present in its own `children` array, use the map to find the correct fragment file immediately.

---

## 2. Real-world Data Risk Control

| File Characteristic                       | Mandatory Action                                                                      | Consequence of Failure                              |
| :---------------------------------------- | :------------------------------------------------------------------------------------ | :-------------------------------------------------- |
| **Strange File IDs (e.g., `12:34.json`)** | Check `type`. If `INSTANCE`, must find the master file.                               | Generated code lacks logic, no reusability.         |
| **Complex Vector Data**                   | Extract the entire `fillGeometry` array to convert to SVG.                            | Icons/Drawings disappear or display incorrectly.    |
| **Duplicate Style Files**                 | Only take values from the file with the latest timestamp or most complete definition. | Inconsistent interface colors (Branding deviation). |

3. **Keyword Safety Net (The "Grep" Rule)**: In complex designs, structure JSONs might omit deeply nested text or components. The system **MUST** use keyword-based searching (e.g., `grep`) to locate specific strings or patterns (prices, labels, ratings) visible in reference images across **ALL** files in the `figma-agent/data/` directory.

---

## 3. Technical Logic Flow

1.  **Crawler:** Browse the entire `/figma-agent` directory, missing no `.json` file.
2.  **Keyword Searcher (New ⭐):** Run `grep` for core UI labels detected in the screenshot to find their file locations.
3.  **Indexer:** Create a Lookup Table containing all IDs appearing in the directory.
4.  **Linker:** Connect Style IDs and Component IDs to corresponding Nodes.
5.  **Generator:** Convert the complete data tree into source code following Atomic Design standards.

**Adherence to these principles is critical to avoid "garbage code" generation (deviation > 4% is failure).**

---

## 4. Styling Compliance Rule (CRITICAL)

Before generating ANY code, the agent **MUST** detect and use the styling system from `project.yaml`:

### Detection Steps

1. Read `figma-agent/project.yaml` → [techStack] → "styling" field
2. Identify system: CSS, Tailwind, MUI, Joy UI, Styled Components, Emotion, Sass
3. Verify markers: Check `package.json` and config files
4. Use ONLY the detected styling system

### Compliance Rules

- ✅ **Tailwind** → Use ONLY `className` with utilities
- ✅ **MUI/Joy** → Use ONLY `sx` prop
- ✅ **CSS Modules** → Use ONLY module imports
- ✅ **Styled Components** → Use ONLY styled() functions
- ✅ **Plain CSS** → Use ONLY CSS Variables

### Never Mix

❌ NO `className` + `sx` together  
❌ NO inline `style` + `className`  
❌ NO hardcoded CSS values  
❌ NO mixing frameworks

### Token Source

ALL values from `figma-agent/data/`:

- Colors from `05-colors.json`
- Typography from `02-texts.json`
- Spacing from layout data

**Failure Consequence**: Branding deviation > 4% = BUILD FAILURE ❌
