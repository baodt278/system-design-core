"""Offline variant of build.py for sandboxes where the CDNs are blocked.

Serves mermaid, highlight.js and the fonts from local npm packages instead of the CDNs:
  (cd npmdeps && npm install mermaid@11.4.1 @highlightjs/cdn-assets@11.9.0 \
       @fontsource/be-vietnam-pro@5.1.0 @fontsource/literata@5.1.0)
  pip install --target=pwlib playwright
  python3 build_local.py [out]     # writes out.html and out.pdf
Uses the pre-installed Chromium at /opt/pw-browsers.
"""
import sys, os
sys.path.insert(0, os.environ.get('PWLIB', 'pwlib'))
sys.path.insert(0, '.')
import build
from playwright.sync_api import sync_playwright
NM = os.environ.get('NPM_MODULES', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'npmdeps', 'node_modules'))
import mimetypes
def _local(route, path):
    ct = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    if path.endswith('.mjs') or path.endswith('.js'): ct = 'application/javascript'
    route.fulfill(path=path, content_type=ct, headers={'Access-Control-Allow-Origin': '*'})
def _fonts_css():
    css = []
    for pkg, files in [('be-vietnam-pro', ['400', '600', '700', '800']), ('literata', ['400', '600', '700', '400-italic'])]:
        for w in files:
            c = open(f'{NM}/@fontsource/{pkg}/{w}.css').read()
            css.append(c.replace('url(./files/', f'url(https://local.fonts/{pkg}/files/').replace('font-display: swap', 'font-display: block'))
    return '\n'.join(css)
def install_routes(pg):
    pg.route('https://cdn.jsdelivr.net/npm/mermaid@11/dist/**', lambda r: _local(r, NM + '/mermaid/dist/' + r.request.url.split('/dist/', 1)[1]))
    pg.route('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/**', lambda r: _local(r, NM + '/@highlightjs/cdn-assets/' + r.request.url.split('/11.9.0/', 1)[1]))
    pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(body=_fonts_css(), content_type='text/css', headers={'Access-Control-Allow-Origin': '*'}))
    pg.route('https://fonts.gstatic.com/**', lambda r: r.abort())
    pg.route('https://local.fonts/**', lambda r: _local(r, NM + '/@fontsource/' + r.request.url.split('local.fonts/', 1)[1]))
def to_pdf(html_path, pdf_path):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg = b.new_page()
        install_routes(pg)
        pg.goto('file://' + os.path.abspath(html_path), wait_until='networkidle', timeout=300000)
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
build.to_pdf = to_pdf
out = sys.argv[1] if len(sys.argv) > 1 else 'book'
anchors = build.build(out + '.html', None, None)
to_pdf(out + '.html', out + '.pdf')
pm = build.page_numbers(out + '.pdf', anchors)
print('found', len(pm), 'of', len(anchors))
build.build(out + '.html', pm, None)
to_pdf(out + '.html', out + '.pdf')
from pypdf import PdfReader
print('pages', len(PdfReader(out + '.pdf').pages))
