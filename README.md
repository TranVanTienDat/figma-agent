# 🚀 Figma Agent: Design-to-Code Powerhouse

Figma Agent là bộ công cụ mạnh mẽ dành cho Antigravity AI, giúp chuyển đổi thiết kế từ Figma thành mã nguồn React/Next.js chất lượng cao, chuẩn SEO và dễ bảo trì. Công cụ tập trung vào độ chính xác tuyệt đối (Pixel-Perfect) và tối ưu hóa hiệu suất với các tệp thiết kế lớn.

---

## 🛠 Cài đặt

### 1. Yêu cầu hệ thống

- **Node.js**: >= 18.0.0
- **Python**: 3.x (cùng thư viện `requests` và `python-dotenv`)

### 2. Cài đặt Global

Tại thư mục gốc của dự án công cụ này, chạy:

```bash
npm install -g .
```

### 3. Cấu hình môi trường

Bạn có thể cấu hình Token qua file `.env` hoặc trực tiếp qua Terminal:

**Cách 1: Sử dụng file `.env` (Khuyên dùng)**
Tạo file `.env` tại thư mục gốc dự án:

```env
FIGMA_ACCESS_TOKEN=your_personal_access_token
```

**Cách 2: Sử dụng lệnh Export (Terminal)**

- **Thiết lập**: `export FIGMA_ACCESS_TOKEN=your_token`
- **Kiểm tra**: `echo $FIGMA_ACCESS_TOKEN`
- **Xóa**: `unset FIGMA_ACCESS_TOKEN`

---

## 🔄 Quy trình chuẩn (Workflow)

Để đạt hiệu quả cao nhất, hãy tuân thủ quy trình 5 bước sau:

### Bước 1: Khởi tạo (Lần đầu)

Trong thư mục dự án của bạn (nơi chứa code Web), chạy:

```bash
figma-agent
```

Lệnh này tạo thư mục `figma-agent/` - trung tâm điều khiển của AI.

### Bước 2: Thiết lập Tech Stack

Trong khung chat Antigravity, gõ:
**`/figma-config`**
AI sẽ đọc cấu trúc dự án (Tailwind, TypeScript,...) để đảm bảo code sinh ra luôn tương thích hoàn toàn.

### Bước 3: Đồng bộ dữ liệu Figma

Tải dữ liệu thiết kế về máy:
**`/sync-figma-data [Figma-Link]`**
_Mẹo: Tool hỗ trợ Auto-Retry nếu gặp giới hạn API của Figma (Rate Limit)._

### Bước 4: Chuyển đổi Tokens (Tùy chọn)

Chuyển đổi các Styles từ Figma thành biến CSS/JSON:
**`/figma-map-tokens`**

### Bước 5: Build UI

Bắt đầu tạo code bằng ngôn ngữ tự nhiên:
**`/figma-build Build cho tôi Section Header chuẩn Responsive.`**

---

## 📂 Cấu trúc Thư mục `figma-agent/`

Hệ thống quản lý dữ liệu tập trung và minh bạch:

- `config.yaml`: Chứa bối cảnh dự án (Tech Stack, quy tắc code).
- `data/`: Dữ liệu thô đồng bộ từ Figma (styles, components, file structure).
- `common/`: Các Design Tokens và Assets dùng chung cho toàn dự án.
- `[section-name]/`: Dữ liệu chi tiết cho từng phần/trang cụ thể (specs, data.json).

---

## ⚡ Tối ưu cho Dự án Lớn

- **Đồng bộ từng phần**: Sử dụng Node ID (trong link Figma) để chỉ đồng bộ phần bạn cần làm việc, giúp tiết kiệm thời gian và tài nguyên.
  - Ví dụ: `/sync-figma-data [Link]?node-id=5965:18603`
- **Context Awareness**: Mỗi khi build, AI sẽ tự động đọc **toàn bộ** thư mục `figma-agent/` để đảm bảo code sinh ra khớp 100% với hệ thống thiết kế hiện có.

---

## 👨‍💻 Tác giả

Phát triển bởi **TranVanTienDat** 🚀
