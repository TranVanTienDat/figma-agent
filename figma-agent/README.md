# Figma Agent

Thư mục này chứa dữ liệu, cấu hình và tài liệu cho Figma Agent.

## 📂 Cấu trúc thư mục

```
figma-agent/
├── data/                    # Chứa dữ liệu extracted từ Figma
│   ├── footer-node.json     # File gốc (lớn)
│   ├── footer-split-v2/     # ✅ Dữ liệu đã split (Recommended)
│   └── ...
├── config.yaml              # Cấu hình agent
├── FINAL-SOLUTION.md        # 📘 Tổng kết giải pháp split file
├── QUICK-REF.md             # ⚡ Quick reference guide
├── RECURSIVE-SPLIT-GUIDE.md # 📖 Hướng dẫn recursive split
└── SPLIT-DATA-GUIDE.md      # 🇻🇳 Hướng dẫn tiếng Việt
```

## 🚀 Công cụ chính

### Script Split Data

Tự động chia nhỏ file Figma lớn thành các file nhỏ (200-300 dòng) để AI xử lý chính xác hơn.

```bash
python3 ../.agent/skills/figma-analysis/scripts/split_node_data.py \
  data/footer-node.json \
  --max-lines 250
```

Xem chi tiết: [QUICK-REF.md](QUICK-REF.md)

## 📚 Tài liệu quan trọng

1. **[FINAL-SOLUTION.md](FINAL-SOLUTION.md)** (Recommended)
   - Tổng hợp đầy đủ nhất về giải pháp
   - Cách sử dụng, kết quả, so sánh
   - Best practices

2. **[QUICK-REF.md](QUICK-REF.md)**
   - Tra cứu nhanh lệnh và options
   - Thứ tự đọc file cho AI

3. **[RECURSIVE-SPLIT-GUIDE.md](RECURSIVE-SPLIT-GUIDE.md)**
   - Giải thích cơ chế chia file đệ quy
   - Cách cấu hình deep split

4. **[SPLIT-DATA-GUIDE.md](SPLIT-DATA-GUIDE.md)**
   - Tài liệu hướng dẫn chi tiết bằng tiếng Việt

## 🔄 Workflow

Để build UI từ Figma data chính xác nhất:

1. **Check size**: Kiểm tra file JSON gốc có lớn không (>1000 dòng).
2. **Split**: Chạy script split data nếu file lớn.
3. **Read**: Đọc `00-summary.json` trước, sau đó là `01-structure.json`.
4. **Build**: Đọc từng file trong thư mục `sections/` để build từng phần component.

---

**Lưu ý**: Luôn ưu tiên sử dụng dữ liệu đã split trong thư mục `data/*-split/` thay vì file JSON gốc để đảm bảo độ chính xác cao nhất (95% vs 10%).
