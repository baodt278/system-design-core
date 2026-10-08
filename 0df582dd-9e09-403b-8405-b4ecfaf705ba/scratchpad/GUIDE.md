# Translation guide — System Design book (Vietnamese)

## Goal
The source site (systemdesigncore.site) is written in Vietnamese but is full of English technical
jargon ("Cache invalidation là nightmare", "Team burnout vì complexity"). The reader finds this
distracting. We are producing a PDF book where the prose reads as **natural, fluent Vietnamese**.

You rewrite each text segment into fluent Vietnamese, translating English words/phrases.
Technical terms get a special marker so the book can show the English original once per chapter
and build a glossary.

## Files
- Source: `seg/<slug>.txt` — segments, each starts with a header line `@<id> <kind>` then the text
  (may be multi-line). kind ∈ h1..h4, p, li, td, th, pre.
- Output: `tr/<slug>.txt` — same `@<id>` header (kind optional, just `@<id>` is fine) followed by the
  translated text. **Only include segments you changed**; omitted segments keep the original.
  Never invent ids. Keep segments in id order.
- Reference translations already done (READ at least two of them first to match the style):
  `tr/phase__phase-0__lesson__lesson-1-code-first-to-problem-first.txt`,
  `tr/phase__phase-0__lesson__lesson-3-foundation-exercises.txt`,
  `tr/phase__phase-0__lesson__lesson-4-thinking-in-constraints.txt`
  (compare with the matching `seg/` files).
- Validate: `python3 check.py <slug>` (run from the scratchpad dir). Fix every error it reports.

## Term markers (prose segments only: h*, p, li, td, th)
- Write technical terms as `⟦tiếng Việt|English original⟧`, e.g. `⟦bộ nhớ đệm|cache⟧`,
  `⟦độ trễ|latency⟧`, `⟦cân bằng tải|load balancing⟧`.
- The English part is the term as it appeared in the source (keep its spelling; plural ok).
- Vietnamese part must fit the sentence grammatically and with correct capitalisation
  (`⟦Bộ nhớ đệm|Cache⟧ giúp...` at sentence start).
- Mark a term **every time** it appears (the renderer shows the English only on first occurrence per
  chapter). Mark only real technical/domain terms, not ordinary words: "Done" → "Xong",
  "nightmare" → "cơn ác mộng", "fit" → "phù hợp" without markers.
- Do not put markers inside `**` boundaries awkwardly: `**⟦bộ nhớ đệm|cache⟧ là gì?**` is fine.
- Never put markers inside inline code (backticks) or inside `pre` segments.

## What to keep in English (no translation, no marker)
- Product/company/tool names: Redis, Kafka, PostgreSQL, MySQL, Cassandra, MongoDB, Kubernetes,
  Docker, Nginx, AWS, S3, DynamoDB, Netflix, Facebook, Twitter, Instagram, Uber, Shopee...
- Well-known acronyms: API, CDN, DNS, HTTP(S), TCP, UDP, TLS, SQL, NoSQL, ACID, BASE, CAP, QPS,
  RPS, TPS, CPU, RAM, SSD, I/O, ID, UUID, URL, JSON, REST, gRPC, SLA, SLO, SLI, MVP, TTL, LRU,
  CRUD, JWT, OAuth, P99/p99, ms, GB, etc. (You may add a marker for an acronym only when expanding
  it in Vietnamese the first time if useful — usually don't.)
- Inline code in backticks, numbers, units, math, formulas, URLs.
- Named algorithms/patterns with no common Vietnamese name may stay English but add a short
  Vietnamese gloss when first introduced, e.g. "Round Robin (xoay vòng)", "Snowflake ID",
  "Two-Phase Commit (cam kết hai pha)", "Saga". Use judgement.
- Quotes from famous people: translate them into Vietnamese (keep the attribution name).

## pre segments (plain-text blocks: diagrams, notes, pseudo-flows, checklists)
- Translate English prose inside them into Vietnamese, **keeping the exact line structure**:
  same number of lines, same indentation, same bullets/arrows/symbols (→ ✅ ❌ ☐ ├ │ etc.).
- No ⟦ ⟧ markers inside pre. You may add an English term in parentheses once if it really helps,
  e.g. "Phân mảnh dữ liệu (sharding)".
- If a pre block is actually source code / config / SQL / a shell command / an HTTP message /
  JSON: leave it untouched (omit it from the output). You may translate a `# comment` only if it
  is plain English prose — usually just leave code alone.
- ASCII box diagrams (┌─┐│└┘ etc.) — translate labels only if the alignment survives; if alignment
  would break, leave the block unchanged.
- **Mermaid diagrams** (pre that starts with `graph`, `flowchart`, `sequenceDiagram`,
  `stateDiagram`, `classDiagram`, `erDiagram`, `gantt`, `pie`...): keep every keyword, node id,
  arrow, `style`/`classDef` line and syntax character exactly. Translate only the human-readable
  label text: inside `[...]`, `(...)`, `{...}`, `((...))`, `"..."`, `|edge label|`, and the text
  after `:` in sequence-diagram messages/notes. Do not introduce characters that break Mermaid
  syntax inside labels: no `"`, `[`, `]`, `{`, `}`, `(`, `)`, `|`, `;` added inside a label that
  didn't have them. Participant names in sequenceDiagram may stay as they are.

## Style
- Natural, fluent, technical Vietnamese, like a well-edited Vietnamese tech book. Keep the author's
  voice (first person "tôi", addressing "bạn", short punchy sentences).
- Keep markdown: `**bold**`, `*italic*`, `` `code` ``, literal `\n` sequences. Keep `→`, emoji, ✅ ❌.
- Do not summarise, skip or add content. Every sentence must be preserved.
- Headings: Title Case like the source ("Tại Sao Phải Thay Đổi Tư Duy?").
- "Key Takeaways" → "Những Điểm Cốt Lõi". "Checklist" → "Danh Sách Kiểm Tra" (or "Danh Sách Tự Kiểm
  Tra"). "Exercise N" → "Bài tập N". "Lesson N" → "Bài N". "Phase N" → "Phần N".
  "Trade-off" (noun) → "sự đánh đổi"/"đánh đổi". "Option A" → "Phương án A". "Case" → "Trường hợp".
  "Scenario" → "Kịch bản". "Example" → "Ví dụ". "Pros/Cons" → "Ưu điểm/Nhược điểm".
  "Gains/Costs" → "Được/Mất". "Step N" → "Bước N".
- Numbers: Vietnamese style is fine ("1.000", "2,5 giây") in prose; in pre blocks you may keep the
  original numerals.
- "1K/1M/1B users" → "1 nghìn / 1 triệu / 1 tỷ người dùng" in prose.

## Glossary (use these consistently)
architect → kiến trúc sư · senior architect → kiến trúc sư lâu năm · architecture → kiến trúc
system design → thiết kế hệ thống · developer/dev → lập trình viên · engineer → kỹ sư
junior/senior (engineer) → kỹ sư mới vào nghề / kỹ sư lâu năm · team → nhóm
startup → công ty khởi nghiệp · user(s) → người dùng · client → máy khách · server → máy chủ
request → yêu cầu · response → phản hồi · production → môi trường thực tế (vận hành thực tế)
deploy/deployment → triển khai · debug → gỡ lỗi · bug → lỗi · refactor → tái cấu trúc
scale (verb) → mở rộng · scale (noun) → quy mô · scalability → khả năng mở rộng
horizontal / vertical scaling → mở rộng theo chiều ngang / theo chiều dọc
cache → bộ nhớ đệm · caching → lưu đệm · cache hit/miss → trúng/trượt bộ nhớ đệm
cache invalidation → vô hiệu hoá bộ nhớ đệm · eviction → loại bỏ (khỏi bộ nhớ đệm)
stale data → dữ liệu cũ · hot data/key → dữ liệu/khoá "nóng"
database → cơ sở dữ liệu (CSDL in diagrams) · query → truy vấn · index → chỉ mục · schema → lược đồ
transaction → giao dịch · replication → nhân bản · replica → bản sao · read replica → bản sao chỉ đọc
primary/leader → máy chủ chính / nút chủ (leader) · follower → nút theo (follower)
sharding → phân mảnh dữ liệu · shard → mảnh · partition → phân vùng · partitioning → phân vùng
load balancer → bộ cân bằng tải · load balancing → cân bằng tải · load → tải · traffic → lưu lượng
latency → độ trễ · throughput → thông lượng · bandwidth → băng thông · performance → hiệu năng
availability → tính sẵn sàng · high availability → tính sẵn sàng cao · reliability → độ tin cậy
consistency → tính nhất quán · strong / eventual consistency → nhất quán mạnh / nhất quán cuối cùng
durability → độ bền dữ liệu · fault tolerance → khả năng chịu lỗi · failure → sự cố / lỗi
failover → chuyển đổi dự phòng · redundancy → dự phòng · single point of failure (SPOF) → điểm lỗi duy nhất
bottleneck → điểm nghẽn · trade-off → sự đánh đổi · constraint → ràng buộc · requirement → yêu cầu
functional / non-functional requirement → yêu cầu chức năng / phi chức năng
message queue → hàng đợi thông điệp · queue → hàng đợi · producer / consumer → bên phát / bên tiêu thụ
pub/sub → mô hình xuất bản – đăng ký · event → sự kiện · event-driven → hướng sự kiện
worker → tiến trình xử lý (worker) · background job → tác vụ nền · batch → lô / theo lô
sync / async → đồng bộ / bất đồng bộ · blocking → chặn · coupling → liên kết (tight/loose → chặt/lỏng)
decoupling → tách rời · retry → thử lại · timeout → hết thời gian chờ · idempotent → lũy đẳng
backpressure → áp lực ngược · rate limiting → giới hạn tần suất · throttling → điều tiết
circuit breaker → bộ ngắt mạch · graceful degradation → suy giảm có kiểm soát
monitoring → giám sát · observability → khả năng quan sát · logging/logs → ghi log / log
metrics → số liệu đo / chỉ số · tracing → truy vết · alert → cảnh báo · dashboard → bảng điều khiển
microservices → vi dịch vụ · monolith → hệ thống nguyên khối · service → dịch vụ
stateless / stateful → phi trạng thái / có trạng thái · session → phiên
consensus → đồng thuận · leader election → bầu chọn nút chủ · quorum → túc số (quorum)
clock → đồng hồ · timestamp → dấu thời gian · ordering → thứ tự · clock skew → lệch đồng hồ
distributed system → hệ thống phân tán · node → nút · cluster → cụm · network partition → phân vùng mạng
feed → bảng tin · fan-out → phân phát (fan-out) · timeline → dòng thời gian · read-heavy → thiên về đọc
write-heavy → thiên về ghi · edge → điểm biên · origin → máy chủ gốc · storage → lưu trữ
framework (thinking) → khung tư duy · mindset → tư duy · mental model → mô hình tư duy
pattern → mẫu (thiết kế) · best practice → thực hành tốt nhất · use case → tình huống sử dụng
interview → phỏng vấn · interviewer → người phỏng vấn · estimate/estimation → ước lượng
back-of-the-envelope → ước tính nhanh · capacity planning → hoạch định năng lực
over-engineering → thiết kế thừa · cost → chi phí · complexity → độ phức tạp · overhead → chi phí phụ
optimize → tối ưu · benchmark → đo hiệu năng · profiling → phân tích hiệu năng
peak → cao điểm/đỉnh · spike → tăng đột biến · downtime → thời gian ngừng hoạt động
rollback → hoàn tác (rollback) · migration → chuyển đổi/di chuyển dữ liệu · infrastructure → hạ tầng
CDN, API... keep. · endpoint → điểm cuối (endpoint) · payload → dữ liệu gửi kèm · header → tiêu đề (header)
