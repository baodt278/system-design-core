import re, json, os, urllib.request, html, time
urls=[u.strip() for u in open('urls.txt') if u.strip()]
seen=[]; out=[]
for u in urls:
    path=u.replace('https://systemdesigncore.site','') or '/'
    if path in seen: continue
    seen.append(path)
    req=urllib.request.Request('https://www.systemdesigncore.site'+path, headers={'User-Agent':'Mozilla/5.0'})
    s=urllib.request.urlopen(req).read().decode('utf-8')
    fn='raw/'+(path.strip('/').replace('/','__') or 'home')+'.html'
    open(fn,'w').write(s)
    i=s.find('id="S:0"'); body=s[i:] if i>=0 else s
    m=re.search(r'<article class="prose-ui">(.*?)</article>\s*</article>', body, re.S)
    title=re.search(r'<title>(.*?)</title>', s)
    out.append({'path':path,'title':html.unescape(title.group(1)) if title else '', 'has_prose':bool(m), 'len':len(m.group(1)) if m else 0})
    time.sleep(0.3)
json.dump(out,open('index.json','w'),ensure_ascii=False,indent=1)
for o in out: print(o['has_prose'], o['len'], o['path'], '|', o['title'][:70])
