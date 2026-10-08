import re, json, html, glob
import lxml.html
from lxml import etree

BLOCK = {'p','ul','ol','li','pre','table','blockquote','h1','h2','h3','h4','h5','h6','hr','div'}
def inline_md(nodes_text, nodes):
    """Convert leading text + inline nodes to markdown-ish."""
    out = [nodes_text or '']
    for n in nodes:
        out.append(node_md(n)); out.append(n.tail or '')
    return ''.join(out)
def node_md(n):
    t = n.tag
    inner = inline_md(n.text, list(n))
    if t in ('strong','b'): return '**'+inner+'**'
    if t in ('em','i'): return '*'+inner+'*'
    if t == 'code': return '`'+inner+'`'
    if t == 'br': return '\\n'
    if t == 'input': return ''
    if t == 'a': return inner
    return inner

def lessons():
    idx = json.load(open('index.json'))
    for o in idx:
        p=o['path']
        if p in ('/','/roadmap','/about'): continue
        yield o

for o in lessons():
    path = o['path']; slug = path.strip('/').replace('/','__')
    s = open('raw/'+slug+'.html').read(); s = s[s.find('id="S:0"'):]
    s = re.sub(r'<script.*?</script>', '', s, flags=re.S)
    doc = lxml.html.fromstring('<div>'+s[s.find('>')+1:]+'</div>')
    arts = [a for a in doc.iter('article') if not list(a.iter('article'))[1:]]
    root = arts[0]
    segs = []
    def add(kind, text):
        segs.append((kind, text)); return len(segs)-1
    def process(el):
        tag = el.tag
        if tag == 'pre':
            code = el.find('code')
            lang = ''
            if code is not None:
                m = re.search(r'language-(\w+)', code.get('class') or '')
                lang = m.group(1) if m else ''
            txt = el.text_content()
            if lang in ('', 'markdown', 'text'):
                i = add('pre', txt)
                for c in list(el): el.remove(c)
                el.text = None
                c = etree.SubElement(el, 'code'); c.text = f'§§SEG{i}§§'
                if lang: c.set('class', 'language-'+lang)
            return
        if tag in ('p','h1','h2','h3','h4','h5','h6','td','th','li'):
            # leading inline part
            kids = list(el); lead = []
            for k in kids:
                if k.tag in BLOCK: break
                lead.append(k)
            has_check = any(k.tag=='input' for k in lead)
            txt = inline_md(el.text, lead)
            if txt.strip():
                i = add(tag, txt.strip())
                tail_last = None
                for k in lead: el.remove(k)
                el.text = ('§§CHECK§§' if has_check else '') + f'§§SEG{i}§§'
            for k in list(el):
                process(k)
            return
        for k in list(el): process(k)
    for k in list(root): process(k)
    tpl = etree.tostring(root, encoding='unicode', method='html')
    open(f'tpl/{slug}.html','w').write(tpl)
    with open(f'seg/{slug}.txt','w') as f:
        for i,(k,t) in enumerate(segs):
            f.write(f'@{i} {k}\n{t}\n')
    print(slug, len(segs))
