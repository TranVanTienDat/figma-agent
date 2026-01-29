# Figma Analysis Technical Reference

## UI Layout Mapping Rules

| Figma Property           | CSS Equivalent                                 | Logic                                           |
| ------------------------ | ---------------------------------------------- | ----------------------------------------------- |
| Auto Layout (Vertical)   | `display: flex; flex-direction: column;`       | Map `itemSpacing` to `gap`.                     |
| Auto Layout (Horizontal) | `display: flex; flex-direction: row;`          | Map `itemSpacing` to `gap`.                     |
| Hug Contents             | `width: fit-content;` / `height: fit-content;` | Component shrinks to fit children.              |
| Fill Container           | `flex-grow: 1;` / `width: 100%;`               | Component expands to fill parent space.         |
| Absolute Position        | `position: absolute;`                          | Used when nodes are placed outside manual flow. |

## Design Token Schemas

### `system-colors.json`

```json
{
  "colors": {
    "brand": { "primary": "#HEX" },
    "neutral": { "black": "#HEX" }
  }
}
```

### `text-presets.json`

```json
{
  "typography": {
    "h1": {
      "fontFamily": "string",
      "fontSize": "string (px)",
      "fontWeight": number,
      "lineHeight": "string (px)"
    }
  }
}
```
