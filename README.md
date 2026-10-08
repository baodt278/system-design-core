# System Design Core — Bản Dịch Tiếng Việt

Dự án biên soạn lại nội dung của [systemdesigncore.site](https://systemdesigncore.site) (tác giả Steve Bang) thành một cuốn sách PDF **"Thiết Kế Hệ Thống — Từ con số 0 đến chuyên gia"**, trong đó phần văn bản trộn nhiều thuật ngữ tiếng Anh đã được viết lại thành tiếng Việt tự nhiên.

- Thuật ngữ chuyên ngành được Việt hoá, kèm thuật ngữ gốc trong ngoặc ở lần xuất hiện đầu tiên của mỗi bài, ví dụ: *bộ nhớ đệm (cache)*.
- Tên sản phẩm, công cụ, từ viết tắt phổ biến (Redis, Kafka, API, CDN, SQL…) và mã nguồn được giữ nguyên.
- Cuối sách có **Phụ lục B — Bảng thuật ngữ Anh – Việt** được tổng hợp tự động.

📖 **Sách đã build:** [`0df582dd-9e09-403b-8405-b4ecfaf705ba/scratchpad/book.pdf`](0df582dd-9e09-403b-8405-b4ecfaf705ba/scratchpad/book.pdf) (1011 trang)

## Nội dung sách

| Phần | Chủ đề |
|------|--------|
| Lời mở đầu | Giới thiệu lộ trình học |
| Phần 0 | Chuyển Đổi Mô Hình Tư Duy (8 bài) |
| Phần 1 | Nền Tảng: Tư Duy Theo Hệ Thống (5 bài) |
| Phần 2 | Các Khối Xây Dựng Cốt Lõi (5 bài) |
| Phần 3 | Nền Tảng Hệ Thống Phân Tán (6 bài) |
| Phần 4 | Khả Năng Mở Rộng & Hiệu Năng (7 bài) |
| Phần 5 | Các Mẫu Kiến Trúc Thực Tế (3 bài) |
| Phần 6 | Làm Chủ Thiết Kế Hệ Thống (6 bài) |
| Phụ lục A | Chuẩn Bị Cho Phỏng Vấn Thiết Kế Hệ Thống |
| Phụ lục B | Bảng thuật ngữ Anh – Việt |

## Cấu trúc thư mục

Toàn bộ mã và dữ liệu nằm trong `0df582dd-9e09-403b-8405-b4ecfaf705ba/scratchpad/`:

| Đường dẫn | Mô tả |
|-----------|-------|
| `urls.txt`, `sitemap.xml` | Danh sách trang cần lấy từ website gốc |
| `crawl.py` → `raw/` | Tải HTML gốc của từng trang |
| `extract.py` → `seg/`, `tpl/`, `index.json` | Tách mỗi trang thành các đoạn văn bản (`seg/<slug>.txt`) và khuôn HTML (`tpl/<slug>.html`) |
| `tr/<slug>.txt` | **Bản dịch** — chỉ chứa các đoạn đã dịch, đoạn nào thiếu sẽ dùng bản gốc |
| `GUIDE.md` | Quy tắc dịch, cách đánh dấu thuật ngữ và bảng thuật ngữ chuẩn |
| `check.py` | Kiểm tra bản dịch (id hợp lệ, dấu `⟦…⟧`, `**`, mã inline…) |
| `build.py` | Ghép bản dịch vào khuôn, dựng HTML và xuất PDF bằng Playwright |
| `build_local.py` | Biến thể của `build.py` chạy offline (dùng thư viện từ npm thay vì CDN) |
| `book.css` | Định dạng trang sách |
| `pylib/` | Thư viện `pypdf` đi kèm (dùng để đánh số trang mục lục) |

### Định dạng file đoạn văn

Mỗi đoạn bắt đầu bằng dòng `@<id> <loại>` (loại: `h1`–`h4`, `p`, `li`, `td`, `th`, `pre`), sau đó là nội dung. Trong bản dịch, thuật ngữ được viết dạng `⟦tiếng Việt|English⟧`:

```
@12 p
⟦Bộ nhớ đệm|Cache⟧ giúp giảm ⟦độ trễ|latency⟧ cho hệ thống.
```

## Cách sử dụng

Chạy các lệnh trong thư mục `0df582dd-9e09-403b-8405-b4ecfaf705ba/scratchpad/`.

**Kiểm tra bản dịch**

```bash
python3 check.py <slug> [<slug> ...]
# ví dụ: kiểm tra tất cả
python3 check.py $(ls seg | sed 's/\.txt$//')
```

**Build sách (có Internet, dùng Chrome)**

```bash
pip install playwright
python3 build.py            # tạo book.html và book.pdf
python3 build.py 0,1 out    # chỉ build Phần 0 và 1, ghi ra out.html / out.pdf
```

**Build sách khi các CDN bị chặn**

```bash
mkdir -p npmdeps && (cd npmdeps && npm install mermaid@11.4.1 @highlightjs/cdn-assets@11.9.0 \
    @fontsource/be-vietnam-pro@5.1.0 @fontsource/literata@5.1.0)
pip install --target=pwlib playwright
python3 build_local.py book
```

`build_local.py` dùng Chromium tại `/opt/pw-browsers`; đường dẫn tới `node_modules` và `pwlib` có thể đổi bằng biến môi trường `NPM_MODULES` và `PWLIB`.

Quá trình build chạy hai lượt: lượt đầu để xác định số trang của từng chương, lượt sau điền số trang vào mục lục.

## Bản quyền

Nội dung gốc thuộc về tác giả của [systemdesigncore.site](https://systemdesigncore.site). Repo này chỉ chứa bản biên soạn và dịch lại phục vụ mục đích học tập.
