"""Stage B of the dictionary: apply work/dict/merge.json to groups.json -> entries + writer packets.
Writes work/dict/entries.json (skeleton per entry) and work/dict/packets/B<nn>.md (<=30 entries, <=MAXC chars).
Reference-only source records never reach an agent; entries with nothing else are rendered by script only."""
import json, re, collections, os, unicodedata
R = 'work/dict/'; MAXN, MAXC = 30, 45000
g = json.load(open(R + 'groups.json', encoding='utf-8')); T, S, G = g['terms'], g['sources'], g['groups']
m = json.load(open(R + 'merge.json', encoding='utf-8'))
refonly = lambda s: not s.get('quote') and re.match(r'\s*reference\b', s.get('use') or '', re.I)
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"[\"'“”‘’`*_()\[\].,;:!?]", '', s).strip(); s = re.sub(r'^(the|a|an)\s+', '', s)
    return re.sub(r'\s+', ' ', s)
gid = {x['id']: x for x in G}
recs = {x['id']: [('T' if x['id'][0] == 'T' else 'S', i) for i in x['records']] for x in G}
for src, tgts in m['split'].items():
    for t in tgts: recs[t] += recs[src]
    recs[src] = []
sets, seen = [], set()
for s in m['merge']:
    s = [i for i in s if i not in m['split']]
    if s: sets.append(s); seen.update(s)
sets += [[x['id']] for x in G if x['id'] not in seen and x['id'] not in m['split']]
def rec(kind, i): return T[i] if kind == 'T' else S[i]
def ref_sort(r):
    mm = re.match(r'(APP|[IV]+\.\d)\s*([¶n])(\d+)', r or ''); return (mm.groups() if mm else (r, '', '0'))
entries = []
for s in sets:
    rs = [x for i in s for x in recs[i]]
    if not rs: continue
    kind = next((m['kind'][i] for i in s if i in m['kind']), 'term' if s[0][0] == 'T' else 'person')
    names = collections.Counter((rec(k, i)['term'] if k == 'T' else rec(k, i)['name']) or '' for k, i in rs)
    names.pop('', None)
    if not names: names = collections.Counter([(rec(*rs[0]).get('work') or '?')])
    head = names.most_common(1)[0][0].strip()
    forms = list(dict.fromkeys(n.strip() for n in names))
    variants = list(dict.fromkeys(v for k, i in rs if k == 'T' for v in rec(k, i).get('variants') or [] if v not in forms))
    eq = list(dict.fromkeys((e.get('with'), e.get('ref')) for k, i in rs if k == 'T' for e in rec(k, i).get('equivalences') or []))
    refs = set()
    for k, i in rs:
        r = rec(k, i)
        if k == 'T': refs.update(q['ref'] for q in r.get('quotes') or []); refs.update(e.get('ref') for e in r.get('equivalences') or [])
        else: refs.update(r.get('refs') or [])
    live = [(k, i) for k, i in rs if k == 'T' or not refonly(rec(k, i))]
    entries.append({'groups': s, 'kind': kind, 'headword': head, 'forms': forms, 'variants': variants,
                    'equivalences': [{'with': w, 'ref': r} for w, r in eq],
                    'refs': sorted((r for r in refs if r), key=ref_sort), 'live': live})
entries.sort(key=lambda e: (norm(e['headword']), e['headword']))
for n, e in enumerate(entries, 1): e['id'] = f'E{n:04d}'
# resolve equivalences to entries by normalized form
fmap = {}
for e in entries:
    for f in e['forms']: fmap.setdefault(norm(f), e['id'])
for e in entries:
    for q in e['equivalences']:
        t = fmap.get(norm(q['with']));
        if t and t != e['id']: q['entry'] = t
def packet(e):
    L = [f"## {e['id']} | {e['kind']} | {e['headword']}", 'forms: ' + ' / '.join(e['forms'])]
    if e['variants']: L.append('variants listed by readers (may include other names): ' + ' / '.join(e['variants']))
    for k, i in e['live']:
        r = rec(k, i)
        if k == 'T':
            q = '; '.join(f"“{x['text']}” @{x['ref']}" for x in r.get('quotes') or [])
            eqs = '; '.join(f"= {x.get('with')} (“{x.get('quote')}” @{x.get('ref')})" for x in r.get('equivalences') or [])
            L.append(f"- [{r.get('voice')}] {r.get('term')}: {r.get('meaning')} | {q}" + (f' | {eqs}' if eqs else ''))
        else:
            L.append(f"- [cited] {r.get('name')}" + (f" — work: {r['work']}" if r.get('work') else '') + f": {r.get('use')}"
                     + (f" | “{r['quote']}”" if r.get('quote') else '') + f" @{', '.join(r.get('refs') or [])}")
    return '\n'.join(L)
os.makedirs(R + 'packets', exist_ok=True)
for f in os.listdir(R + 'packets'): os.remove(R + 'packets/' + f)
batches, cur, size = [], [], 0
for e in entries:
    if not e['live']: e['batch'] = None; continue
    p = packet(e)
    if cur and (len(cur) >= MAXN or size + len(p) > MAXC): batches.append(cur); cur, size = [], 0
    cur.append((e, p)); size += len(p)
if cur: batches.append(cur)
for b, items in enumerate(batches, 1):
    name = f'B{b:03d}'
    for e, _ in items: e['batch'] = name
    open(R + f'packets/{name}.md', 'w', encoding='utf-8', newline='\n').write(f'# PACKETS {name} ({len(items)} entries)\n\n' + '\n\n'.join(p for _, p in items) + '\n')
for e in entries: e['live'] = len(e['live'])
json.dump(entries, open(R + 'entries.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=0)
print('entries', len(entries), 'script-only', sum(1 for e in entries if not e['batch']), 'batches', len(batches),
      'kinds', dict(collections.Counter(e['kind'] for e in entries)),
      'packet chars', sum(len(p) for b in batches for _, p in b))
