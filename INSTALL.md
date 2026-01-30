# 📖 Hướng dẫn Cài đặt Chi tiết (Detailed Installation)

Tài liệu này hướng dẫn bạn cách thiết lập Figma Agent từ con số 0.

## 1. Chuẩn bị

- Đảm bảo bạn đã cài đặt **Node.js 18+**.
- Cài đặt các gói Python cần thiết:
  ```bash
  pip3 install requests python-dotenv
  ```

## 2. Cài đặt Công cụ

Di chuyển vào thư mục nguồn `build-tool` và chạy:

```bash
npm install -g .
```

Sau bước này, lệnh `figma-agent` sẽ khả dụng ở bất cứ đâu trong terminal của bạn.

## 3. Sử dụng trong Dự án Mới

Để tích hợp sức mạnh Figma vào một dự án web bất kỳ:

1. **Initialize**: Chạy `figma-agent` tại thư mục gốc dự án đó.
2. **Setup Token**: Tạo file `.env` và thêm `FIGMA_ACCESS_TOKEN`.
3. **Config**: Chạy `/figma-config` trong chat để AI tự nhận diện dự án đang dùng công nghệ gì (Vite, Next.js, Tailwind, etc.).

## 4. Troubleshooting (Xử lý sự cố)

- **Lỗi 403**: Kiểm tra lại Token của bạn hoặc quyền truy cập file Figma.
- **Lỗi 429 (Rate Limit)**: Đừng lo, tool sẽ tự động đợi và thử lại. Hãy kiên nhẫn.
- **Lỗi không tìm thấy file .env**: Trên Mac, nếu file ẩn bị chặn, hãy đảm bảo bạn run lệnh từ trong VS Code hoặc cấp quyền "Full Disk Access" cho Terminal.

---

© 2026 Figma Agent Integration Hub.
