"""Validate a translation file: python3 check.py <slug> [<slug> ...]"""
import re, sys
sys.path.insert(0, '.')
from build import read_segs, seg_kinds
ok = True
for slug in sys.argv[1:]:
    orig = read_segs(f'seg/{slug}.txt'); kinds = seg_kinds(f'seg/{slug}.txt')
    try:
        tr = read_segs(f'tr/{slug}.txt')
    except FileNotFoundError:
        print(slug, 'MISSING tr file'); ok = False; continue
    errs = []
    for i, t in tr.items():
        if i not in orig:
            errs.append(f'@{i}: id not in source'); continue
        if t.count('⟦') != t.count('⟧'):
            errs.append(f'@{i}: unbalanced ⟦ ⟧')
        for m in re.finditer(r'⟦([^⟧]*)⟧', t):
            if m.group(1).count('|') != 1:
                errs.append(f'@{i}: bad marker {m.group(0)!r} (need exactly one |)')
        if kinds[i] == 'pre':
            if '⟦' in t:
                errs.append(f'@{i}: markers not allowed inside pre blocks')
        else:
            if t.count('**') % 2:
                errs.append(f'@{i}: odd number of ** (bold)')
            a = sorted(re.findall(r'`[^`]+`', orig[i])); b = sorted(re.findall(r'`[^`]+`', t))
            if a != b:
                errs.append(f'@{i}: inline `code` spans changed: {a} -> {b}')
        if not t.strip():
            errs.append(f'@{i}: empty translation')
    n_marks = sum(len(re.findall('⟦', t)) for t in tr.values())
    print(f'{slug}: {len(tr)}/{len(orig)} segments translated, {n_marks} term markers, {len(errs)} errors')
    for e in errs[:30]:
        print('   ', e)
    ok = ok and not errs
sys.exit(0 if ok else 1)
