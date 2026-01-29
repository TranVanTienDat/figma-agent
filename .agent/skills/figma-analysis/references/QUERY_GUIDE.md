# Metadata Query Tool - Quick Reference

## Purpose

Efficiently extract specific information from large Figma metadata files without loading thousands of lines into AI context.

## Installation

No additional installation needed if you have `python3` and the metadata file already generated.

## Commands

### 1. Get File Summary

```bash
python3 .agent/skills/figma-analysis/scripts/query_metadata.py summary
```

**Output Example:**

```json
{
  "file_name": "SaaS Dashboard Design",
  "folder": "Marketing Projects",
  "last_modified": "2026-01-28T14:30:00Z",
  "version": "1.2.3",
  "total_components": 42,
  "total_styles": 18
}
```

### 2. Search Components

```bash
python3 .agent/skills/figma-analysis/scripts/query_metadata.py components --search "nav"
```

**Output Example:**

```json
[
  {
    "name": "Sidebar Navigation",
    "node_id": "123:456",
    "description": "Main navigation component",
    "thumbnail": "https://..."
  }
]
```

### 3. Filter Styles by Type

```bash
python3 .agent/skills/figma-analysis/scripts/query_metadata.py styles --type TEXT
```

**Available Types:** `FILL`, `TEXT`, `EFFECT`, `GRID`

### 4. Get Component Details

```bash
python3 .agent/skills/figma-analysis/scripts/query_metadata.py component "Primary Button"
```

Returns full metadata for the specified component.

## Use Cases for AI

| User Question                        | Query Command                  |
| ------------------------------------ | ------------------------------ |
| "What components are available?"     | `components`                   |
| "Find button-related components"     | `components --search "button"` |
| "What text styles exist?"            | `styles --type TEXT`           |
| "Show me the Primary Button details" | `component "Primary Button"`   |
| "Give me a project overview"         | `summary`                      |

## Performance Benefits

- **Before**: Load 5000+ lines → ~2000 tokens
- **After**: Load 10-50 lines → ~50-200 tokens
- **Speed**: 10-20x faster queries
- **Accuracy**: Focused results, less confusion
