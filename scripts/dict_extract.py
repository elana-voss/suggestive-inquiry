"""Stage A of the dictionary: extract terms + sources from work/final/*.json, filter reference-only sources,
group by exact normalized headword (term; source name). Writes work/dict/groups.json and work/dict/merge_input.md."""
import json, glob, re, unicodedata, collections
R = 'work/dict/'
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"[\"'“”‘’`*_()\[\].,;:!?]", '', s).strip()
    s = re.sub(r'^(the|a|an)\s+', '', s)
    return re.sub(r'\s+', ' ', s)
T, S = [], []
for f in sorted(glob.glob('work/final/*.json')):
    d = json.load(open(f, encoding='utf-8')); c = d['chunk']
    for t in d['terms']: t['chunk'] = c; T.append(t)
    for s in d['sources']: s['chunk'] = c; S.append(s)
refonly = lambda s: not s.get('quote') and re.match(r'\s*reference\b', s.get('use') or '', re.I)
# union-find over term records
par = {}
def find(x):
    while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
    return x
def union(a, b): par[find(a)] = find(b)
# exact headword only: chaining through variants over-merges (readers listed other names as variants);
# the merge agent joins spelling/form variants.
tg = collections.defaultdict(list)
for i, t in enumerate(T): tg[find(norm(t['term']))].append(i)
sg = collections.defaultdict(list)
for i, s in enumerate(S): sg[norm(s['name'])].append(i)
groups = []
for k, idx in sorted(tg.items(), key=lambda kv: -len(kv[1])):
    groups.append({'id': f'T{len(groups)+1:04d}', 'kind': 'term', 'records': idx})
nt = len(groups)
for k, idx in sorted(sg.items(), key=lambda kv: -len(kv[1])):
    groups.append({'id': f'S{len(groups)-nt+1:04d}', 'kind': 'source', 'records': idx})
json.dump({'terms': T, 'sources': S, 'groups': groups}, open(R + 'groups.json', 'w', encoding='utf-8'), ensure_ascii=False)
# merge input: headwords / variants / asserted equivalences only
out = ['# TERM GROUPS (id | forms | records | asserted equivalences: with @ref)']
for g in groups[:nt]:
    rs = [T[i] for i in g['records']]
    forms = list(dict.fromkeys([r['term'] for r in rs] + [v for r in rs for v in r.get('variants') or []]))
    eq = list(dict.fromkeys(f"{e.get('with')} @{e.get('ref')}" for r in rs for e in r.get('equivalences') or []))
    out.append(f"{g['id']} | {' / '.join(forms)} | {len(rs)}" + (f" | = {'; '.join(eq)}" if eq else ''))
out.append('\n# SOURCE GROUPS (id | name forms | records | works) — persons/treatises; reference-only records excluded from counts')
for g in groups[nt:]:
    rs = [S[i] for i in g['records']]; live = [r for r in rs if not refonly(r)]
    works = list(dict.fromkeys(r['work'] for r in rs if r.get('work')))[:6]
    out.append(f"{g['id']} | {rs[0]['name']} | {len(live)}/{len(rs)}" + (f" | {'; '.join(works)}" if works else ''))
open(R + 'merge_input.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(T), len(S), 'term groups', nt, 'source groups', len(groups) - nt, 'refonly', sum(1 for s in S if refonly(s)))
