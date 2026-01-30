---
description: Sync Core Figma Data
---

This workflow synchronizes the fundamental data from a Figma file into the `figma-agent/data` directory. It uses the improved Python `figma_core` to safely fetch data without overloading the API.

# Prerequisites

- Ensure `FIGMA_ACCESS_TOKEN` is set in your environment (or `.env`).
- You need the FILE_KEY of your Figma Design.

## 🚀 Optimization Strategies

For large Figma files (e.g., complex mockups with thousands of nodes), a full sync can be slow. Use these methods to optimize:

### 1. Light Sync (Top-level only)

Simply use the file summary command without depth restrictions if you want full tree (careful with large files), or use specific node extraction.

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py file <FILE_KEY> --output figma-agent/data/file-structure.json --summary
```

### 2. Partial Sync (Specific Nodes)

If you already know the Node IDs (found in Figma URL as `node-id=...`), fetch only what you need. This is much faster and uses less memory.

```bash
# Replace <NODE_IDS> with comma-separated IDs like 1:2,5:10
python3 .agent/skills/figma-analysis/scripts/figma_cli.py nodes <FILE_KEY> <NODE_IDS> --output figma-agent/data/target-node.json
```

### 3. Handle Rate Limits

The tool automatically handles 429 errors. If you see wait messages, let the script finish. It is retrying with a backoff strategy as recommended by Figma.

---

### 4. Fetch Local Variables (Enterprise Feature - Optional)

If your organization uses Figma Local Variables for tokens (colors, numbers, etc.), use this command:

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py local-variables <FILE_KEY> --output figma-agent/data/local-variables.json
```

### 5. Fetch Published Libraries (Optional)

If your file uses a Team Library, fetch the published components and styles:

```bash
python3 .agent/skills/figma-analysis/scripts/figma_cli.py components <FILE_KEY> --output figma-agent/data/components.json
python3 .agent/skills/figma-analysis/scripts/figma_cli.py styles <FILE_KEY> --output figma-agent/data/styles.json
```

### 6. Extract Local Tokens (Fallback)

If `styles.json` is empty (common for draft files), extract tokens directly from your downloaded node data:

```bash
# Analyze the specific node you just downloaded
python3 .agent/skills/figma-analysis/scripts/figma_cli.py extract-tokens figma-agent/data/target-node.json --output figma-agent/data/tokens.json
```

---

# Usage Flow

Simply gõ lệnh `/sync-figma-data [Link-Figma]` để chạy luồng mặc định. AI sẽ tự động:

1. Tải cấu trúc file.
2. Tải Components & Styles (nếu có).
3. Nếu tải Styles thất bại, nó sẽ tự động Extract Tokens từ dữ liệu thô.
4. **Tự động chia nhỏ (Auto-Split)** các file node lớn để tối ưu cho việc Build UI.

```bash
# Auto-run split after sync
for file in figma-agent/data/*node.json; do
    if [ -f "$file" ]; then
        python3 .agent/skills/figma-analysis/scripts/split_node_data.py "$file" --max-lines 250
    fi
done
```
