"""Verify every quote in a chunk reading is verbatim in the chunk and sits in the referenced paragraph/footnote.
Usage: python quote_check.py CHUNK.md READING.json   -> prints report, exit 1 if any quote not found."""
import json, re, sys

def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('—', '-').replace('–', '-').replace('---', '-').replace('--', '-')
    return re.sub(r'\s+', ' ', s).strip()

def segments(chunk_text):
    segs = {}
    for m in re.finditer(r'^\[([^\]]+)\] (.*?)(?=^\[|^## |\Z)', chunk_text, re.S | re.M):
        segs[m.group(1).replace('¶', '¶')] = norm(m.group(2))
    return segs

def quotes(r):
    for x in r.get('method', []):
        yield 'method', x.get('veiled'), [x.get('ref')]
        for a in x.get('also') or []: yield 'method/also', a.get('text'), [a.get('ref')]
    for t in r.get('terms', []):
        for e in t.get('equivalences', []): yield f"term:{t.get('term')}/equiv", e.get('quote'), [e.get('ref')]
        for q in t.get('quotes', []): yield f"term:{t.get('term')}", q.get('text'), [q.get('ref')]
    for s in r.get('sources', []): yield f"source:{s.get('name')}", s.get('quote'), s.get('refs', [])
    for a in r.get('ambiguities', []): yield 'ambiguity', a.get('quote'), [a.get('ref')]
    for t in r.get('translations', []): yield 'translation', t.get('original'), [t.get('ref')]

def check(chunk_path, reading_path):
    segs = segments(open(chunk_path, encoding='utf-8').read())
    allt = ' '.join(segs.values())
    r = json.load(open(reading_path, encoding='utf-8'))
    total, bad, misref = 0, [], []
    for where, q, refs in quotes(r):
        if not q: continue
        total += 1
        nq = norm(q)
        if any(nq in segs.get(ref or '', '') for ref in refs): continue
        if nq in allt:
            hit = [k for k, v in segs.items() if nq in v]
            misref.append(f"  wrong ref ({where}): {refs} -> found in {hit}: \"{q[:70]}\"")
        else:
            bad.append(f"  NOT FOUND ({where}) {refs}: \"{q[:90]}\"")
    print(f"{reading_path}: {total} quotes, {len(bad)} not found, {len(misref)} wrong ref")
    print('\n'.join(bad + misref))
    return not bad

if __name__ == '__main__':
    sys.exit(0 if check(sys.argv[1], sys.argv[2]) else 1)
