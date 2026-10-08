import re, json, html, os, sys, collections
sys.path.insert(0, 'pylib')

MERMAID = re.compile(r'^(graph|flowchart|sequenceDiagram|stateDiagram|classDiagram|erDiagram|gantt|pie|journey|mindmap|timeline|quadrantChart)\b')
MARK = re.compile(r'⟦([^|⟧]+)\|([^⟧]+)⟧')

def read_segs(fn):
    segs = {}
    if not os.path.exists(fn):
        return segs
    cur = None; buf = []
    for line in open(fn).read().split('\n'):
        m = re.match(r'^@(\d+)(?: (\w+))?$', line)
        if m:
            if cur is not None:
                segs[cur] = '\n'.join(buf)
            cur = int(m.group(1)); buf = []
        else:
            buf.append(line)
    if cur is not None:
        segs[cur] = '\n'.join(buf)
    return segs

def seg_kinds(fn):
    return {int(m.group(1)): m.group(2) for m in re.finditer(r'^@(\d+) (\w+)$', open(fn).read(), re.M)}

class Chapter:
    def __init__(self):
        self.seen = set()

glossary = collections.defaultdict(collections.Counter)

def render_marks(text, ch, in_pre):
    def rep(m):
        vi, en = m.group(1).strip(), m.group(2).strip()
        glossary[en.lower()][vi.lower()] += 1
        if in_pre or ch is None or vi.lower() == en.lower():
            return vi
        key = en.lower()
        if key in ch.seen:
            return vi
        ch.seen.add(key)
        return f'{vi} <span class="en">({en})</span>'
    return MARK.sub(rep, text)

def md_inline(text, ch):
    t = html.escape(text.strip('\n'), quote=False)
    codes = []
    def keep(m):
        codes.append(m.group(1)); return f'\x00{len(codes)-1}\x00'
    t = re.sub(r'`([^`]+)`', keep, t)
    t = render_marks(t, ch, False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t, flags=re.S)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t, flags=re.S)
    t = t.replace('\\n', '<br>').replace('\n', '<br>')
    t = re.sub('\x00(\\d+)\x00', lambda m: '<code>' + render_marks(codes[int(m.group(1))], None, True) + '</code>', t)
    return t

def render_page(slug, ch):
    tpl = re.sub(r' id="[^"]*"', '', open(f'tpl/{slug}.html').read())
    kinds = seg_kinds(f'seg/{slug}.txt')
    orig = read_segs(f'seg/{slug}.txt')
    tr = read_segs(f'tr/{slug}.txt')
    unknown = set(tr) - set(orig)
    if unknown:
        print('WARN unknown seg ids', slug, sorted(unknown)[:10])
    out = []
    pos = 0
    for m in re.finditer(r'(§§CHECK§§)?§§SEG(\d+)§§', tpl):
        out.append(tpl[pos:m.start()]); pos = m.end()
        i = int(m.group(2))
        text = tr.get(i, orig[i])
        if kinds[i] == 'pre':
            body_txt = render_marks(html.escape(text, quote=False), ch, True)
            if MERMAID.match(text.lstrip()):
                body_txt = '@@MERMAID@@' + body_txt + '@@/MERMAID@@'
            out.append(body_txt)
        else:
            box = '<span class="check">☐</span> ' if m.group(1) else ''
            out.append(box + md_inline(text, ch))
    out.append(tpl[pos:])
    body = ''.join(out)
    body = re.sub(r'(<pre[^>]*>\s*<code[^>]*>)\n+', r'\1', body)
    body = re.sub(r'\n+(</code>\s*</pre>)', r'\1', body)
    body = re.sub(r'<pre[^>]*>\s*<code[^>]*>@@MERMAID@@(.*?)@@/MERMAID@@</code>\s*</pre>',
                  r'<div class="mermaid">\1</div>', body, flags=re.S)
    # strip outer <article ...> / <div> wrapper
    body = re.sub(r'^<(article|div)[^>]*>|</(article|div)>$', '', body.strip())
    return body, (tr.get(0) or orig.get(0))

def strip_marks(t):
    return re.sub(r'\*\*|`', '', MARK.sub(lambda m: m.group(1), t)).strip()

PHASE_VI = {
 'phase-0': ('Chuyển Đổi Mô Hình Tư Duy', 'Giai đoạn khởi đầu giúp bạn chuyển từ tư duy ⟦lấy mã nguồn làm trung tâm|code-first⟧ sang ⟦tư duy hệ thống|system thinking⟧ trước khi học sâu về thiết kế hệ thống.'),
 'phase-1': ('Nền Tảng: Tư Duy Theo Hệ Thống', 'Nền tảng tư duy hệ thống để chuyển từ hiểu khái niệm sang phân tích hệ thống thực tế.'),
 'phase-2': ('Các Khối Xây Dựng Cốt Lõi', 'Nền tảng kỹ thuật cốt lõi để xây dựng hệ thống vận hành thực tế có khả năng mở rộng, tối ưu hiệu năng và tích hợp dịch vụ.'),
 'phase-3': ('Nền Tảng Hệ Thống Phân Tán', 'Đi sâu vào thực tế của hệ phân tán: sự cố, tính nhất quán, phối hợp, toàn vẹn dữ liệu và thứ tự sự kiện.'),
 'phase-4': ('Khả Năng Mở Rộng & Hiệu Năng', 'Tư duy và kỹ thuật tối ưu hiệu năng ở quy mô vận hành thực tế: điểm nghẽn, bộ nhớ đệm, kiểm soát tải, khả năng quan sát.'),
 'phase-5': ('Các Mẫu Kiến Trúc Thực Tế', 'Áp dụng kiến thức hệ phân tán và hiệu năng vào kiến trúc vận hành thực tế theo từng bối cảnh.'),
 'phase-6': ('Làm Chủ Thiết Kế Hệ Thống', 'Giai đoạn làm chủ: tư duy kiến trúc sư, ra quyết định kiến trúc, chiến lược phỏng vấn và làm chủ hệ thống vận hành thực tế.'),
}

MERMAID_JS = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('pre code[class*="language-"]').forEach(el => { try { hljs.highlightElement(el); } catch (e) {} });
});</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:false, theme:'neutral', securityLevel:'loose',
  fontFamily:'Be Vietnam Pro, sans-serif', themeVariables:{fontSize:'13px'},
  flowchart:{htmlLabels:true, useMaxWidth:true, wrappingWidth:180}, sequence:{useMaxWidth:true}});
window.__mermaidFail = [];
window.__mermaidDone = (async () => {
  await document.fonts.ready;
  const els = [...document.querySelectorAll('div.mermaid')];
  for (const [i, el] of els.entries()) {
    const txt = el.textContent;
    try { await mermaid.parse(txt); el.textContent = txt; }
    catch (e) {
      window.__mermaidFail.push(i + ': ' + String(e.message || e).slice(0, 160));
      const pre = document.createElement('pre'); pre.textContent = txt; el.replaceWith(pre);
    }
  }
  await mermaid.run({querySelector: 'div.mermaid', suppressErrors: true});
  return els.length;
})();
</script>'''

def build(out_html, page_map=None, only=None):
    idx = json.load(open('index.json'))
    paths = [o['path'] for o in idx]
    glossary.clear()
    parts = []   # html chunks
    toc = []     # (level, label, anchor)
    n = 0
    def anchor():
        nonlocal n; n += 1; return f'c{n}'
    def chapter(slug, kicker, level=1, cls='chapter'):
        ch = Chapter()
        body, title = render_page(slug, ch)
        a = anchor()
        toc.append((level, kicker, strip_marks(title), a))
        parts.append(f'<section class="{cls}" id="{a}"><span class="pm">§{a}§</span>'
                     f'<div class="kicker">{kicker}</div>{body}</section>')
    # intro
    chapter('docs__getting-started', 'Lời mở đầu')
    for p in range(7):
        pslug = f'phase-{p}'
        if only is not None and p not in only: continue
        vi_title, vi_desc = PHASE_VI[pslug]
        a = anchor()
        toc.append((0, f'Phần {p}', vi_title, a))
        lessons = [x for x in paths if x.startswith(f'/phase/{pslug}/lesson/')]
        ch = Chapter()
        intro, _ = render_page(f'phase__{pslug}', ch)
        parts.append(f'<section class="part" id="{a}"><span class="pm">§{a}§</span>'
                     f'<div class="part-num">Phần {p}</div><h1 class="part-title">{vi_title}</h1>'
                     f'<p class="part-desc">{md_inline(vi_desc, Chapter())}</p></section>'
                     f'<section class="chapter part-intro">{intro}</section>')
        for i, lp in enumerate(lessons, 1):
            chapter(lp.strip('/').replace('/', '__'), f'Phần {p} · Bài {i}')
    chapter('docs__interview__preparation', 'Phụ lục A')
    # glossary
    a = anchor()
    toc.append((1, 'Phụ lục B', 'Bảng thuật ngữ Anh – Việt', a))
    rows = []
    for en in sorted(glossary, key=lambda s: s.lower()):
        vis = [v for v, _ in glossary[en].most_common()]
        rows.append(f'<tr><td class="g-en">{html.escape(en)}</td><td>{html.escape(", ".join(vis[:3]))}</td></tr>')
    parts.append(f'<section class="chapter glossary" id="{a}"><span class="pm">§{a}§</span><div class="kicker">Phụ lục B</div>'
                 f'<h1>Bảng thuật ngữ Anh – Việt</h1><p>Các thuật ngữ chuyên ngành đã được Việt hoá trong sách. '
                 f'Lần đầu xuất hiện trong mỗi bài, thuật ngữ gốc được ghi kèm trong ngoặc.</p>'
                 f'<table><thead><tr><th>Tiếng Anh</th><th>Tiếng Việt</th></tr></thead><tbody>{"".join(rows)}</tbody></table></section>')
    # toc
    t = []
    for level, kicker, label, a in toc:
        pg = page_map.get(a, '') if page_map else ''
        t.append(f'<li class="l{level}"><a href="#{a}"><span class="k">{html.escape(kicker)}</span>'
                 f'<span class="t">{html.escape(label)}</span><span class="pg">{pg}</span></a></li>')
    toc_html = f'<section class="toc"><h1>Mục lục</h1><ul>{"".join(t)}</ul></section>'
    cover = ('<section class="cover"><div class="cover-top">SYSTEM DESIGN CORE</div>'
             '<h1>Thiết Kế Hệ Thống</h1><div class="cover-sub">Từ con số 0 đến chuyên gia</div>'
             '<p class="cover-note">Biên soạn lại từ systemdesigncore.site — nội dung gốc của Steve Bang.<br>'
             'Thuật ngữ chuyên ngành được Việt hoá, kèm thuật ngữ gốc ở lần xuất hiện đầu tiên mỗi bài.</p></section>')
    css = open('book.css').read()
    doc = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Thiết Kế Hệ Thống</title>'
           '<link rel="preconnect" href="https://fonts.googleapis.com">'
           '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&display=block" rel="stylesheet">'
           f'<style>{css}</style>{MERMAID_JS}</head><body>{cover}{toc_html}{"".join(parts)}</body></html>')
    if page_map:
        doc = re.sub(r'<span class="pm">§c\d+§</span>', '', doc)
    open(out_html, 'w').write(doc)
    return [a for _, _, _, a in toc]

def to_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')
        pg = b.new_page()
        pg.goto('file://' + os.path.abspath(html_path), wait_until='networkidle', timeout=180000)
        pg.evaluate('document.fonts.ready')
        n = pg.evaluate('window.__mermaidDone')
        fails = pg.evaluate('window.__mermaidFail')
        print('mermaid diagrams:', n, 'failed:', len(fails))
        for f in fails: print('  mermaid fail', f)
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True, outline=True, tagged=True,
               display_header_footer=True, header_template='<span></span>',
               footer_template='<div style="width:100%;font-size:8px;color:#888;text-align:center;font-family:sans-serif"><span class="pageNumber"></span></div>',
               margin={'top': '18mm', 'bottom': '18mm', 'left': '17mm', 'right': '17mm'})
        b.close()

def page_numbers(pdf_path, anchors):
    from pypdf import PdfReader
    r = PdfReader(pdf_path); found = {}
    for i, page in enumerate(r.pages, 1):
        txt = page.extract_text() or ''
        for m in re.finditer(r'§(c\d+)§', txt):
            found.setdefault(m.group(1), i)
    return found

if __name__ == '__main__':
    only = None
    if len(sys.argv) > 1:
        only = [int(x) for x in sys.argv[1].split(',')]
    out = sys.argv[2] if len(sys.argv) > 2 else 'book'
    anchors = build(out + '.html', None, only)
    to_pdf(out + '.html', out + '.pdf')
    pm = page_numbers(out + '.pdf', anchors)
    print('found', len(pm), 'of', len(anchors))
    build(out + '.html', pm, only)
    to_pdf(out + '.html', out + '.pdf')
    from pypdf import PdfReader
    print('pages', len(PdfReader(out + '.pdf').pages))
