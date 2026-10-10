"""Render a chunk reading JSON as readable Markdown. Usage: python render_chunk.py READING.json OUT.md"""
import json, sys

def r(path, out):
    d = json.load(open(path, encoding='utf-8'))
    L = [f"# {d['chunk']}", '', f"*{d.get('gist', '')}*", '', '## Argument', '']
    L += [f"- {n['point']} `{', '.join(n.get('refs', []))}` — {n.get('voice', '')}" for n in d.get('notes', [])]
    L += ['', '## Method', '']
    for m in d.get('method', []):
        L += [f"- **{m.get('aspect')}** — “{m.get('veiled')}” `{m.get('ref')}` ({m.get('voice')})",
              f"  - **Plain ({m.get('status')}):** {m.get('plain')}"]
        if m.get('basis'): L.append(f"  - Basis: {m['basis']}")
        for a in m.get('also') or []: L.append(f"  - Also: “{a['text']}” `{a['ref']}`")
    L += ['', '## Terms', '']
    for t in d.get('terms', []):
        v = f" (also: {', '.join(t['variants'])})" if t.get('variants') else ''
        L.append(f"- **{t['term']}**{v} — {t.get('meaning')} ({t.get('voice')})")
        for e in t.get('equivalences', []): L.append(f"  - = {e['with']}: “{e['quote']}” `{e['ref']}`")
        for q in t.get('quotes', []): L.append(f"  - “{q['text']}” `{q['ref']}`")
    L += ['', '## Sources cited', '']
    for s in d.get('sources', []):
        w = f", *{s['work']}*" if s.get('work') else ''
        q = f" — “{s['quote']}”" if s.get('quote') else ''
        L.append(f"- **{s['name']}**{w}{q} `{', '.join(s.get('refs', []))}` — {s.get('use')}")
    if d.get('ambiguities'):
        L += ['', '## Ambiguities', '']
        for a in d['ambiguities']:
            L.append(f"- “{a['quote']}” `{a['ref']}`")
            L += [f"  - Reading: {x}" for x in a.get('readings', [])]
            L.append(f"  - Basis: {a.get('basis')}")
    if d.get('translations'):
        L += ['', '## Translations', '']
        L += [f"- `{t['ref']}` “{t['original']}” → {t['translation']} *({t['by']})*" for t in d['translations']]
    if d.get('threads'):
        L += ['', '## Threads', '']
        L += [f"- `{t['ref']}` {t['note']}" for t in d['threads']]
    open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')

if __name__ == '__main__':
    r(sys.argv[1], sys.argv[2])
