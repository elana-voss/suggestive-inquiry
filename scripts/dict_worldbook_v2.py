"""Build the SillyTavern worldbook (step 3 of 3, see RUNBOOK "Lexicon and worldbook cleanup").
  python3 scripts/dict_worldbook_v2.py -> lorebook/Atwood_Hermetic_Mystery.json + work/review/worldbook_keys.md
Reads work/dict/dictionary_v2.json (from dict_clean.py) + scripts/lexicon_rules.json"""
import json, re, collections
R = json.load(open('scripts/lexicon_rules.json', encoding='utf-8'))
D = json.load(open('work/dict/dictionary_v2.json', encoding='utf-8'))
by = {e['id']: e for e in D}
KIND = {'term': 'Term', 'person': 'Person', 'treatise': 'Treatise', 'collective': 'Voice'}
REF = re.compile(r'\s*\[(?:cf\. )?(?:I|II|III|IV|APP)[.\s][^\]]*\]')
def clean(t): return re.sub(r'[ \t]+([,.;:])', r'\1', REF.sub('', t)).strip()
ART = re.compile(r'^(the|a|an|some|these|those|this|that)\s+', re.I)
T2 = {w.lower() for w in R['tier2_words']}
NOX = re.compile(R['thin']['no_explanation_pattern'])
def sing(w): return w[:-1] if len(w) > 3 and w.endswith('s') and not w.endswith('ss') else w
def hnorm(s): return ' '.join(sing(w) for w in re.sub(r'[^a-z0-9 ]', '', ART.sub('', s.lower()).replace('’', "'")).split())

def thin(e):
    if not R['thin'].get('enabled', True): return None
    n = len(e['summary']) + len(e['body'])
    if e['reference_only']: return 'reference only'
    if e['kind'] != 'term' and len(e['refs']) == 1 and n < R['thin']['minor_name_max_chars']: return 'minor name, one mention'
    if n < R['thin']['min_chars'] and NOX.search(e['summary'] + ' ' + e['body']): return 'short, not explained in the text'
    return None

dropped = []
keep = []
for e in D:
    why = 'excluded by rule (no usable trigger)' if e['id'] in R['worldbook_exclude'] else thin(e)
    if why: dropped.append((e, why))
    else: keep.append(e)
# group: same headword (homonyms) + editorial folds (worldbook_fold); fold members leave their homonym group
FOLD = {k: v for k, v in R.get('worldbook_fold', {}).items() if not k.startswith('_')}
fmember = {m: t for t, v in FOLD.items() for m in v['members']}
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b): parent[find(a)] = find(b)
hg = collections.defaultdict(list)
for e in keep:
    find(e['id'])
    if e['id'] not in fmember: hg[hnorm(e['headword'])].append(e['id'])
for ids in hg.values():
    for i in ids[1:]: union(i, ids[0])
for m, t in fmember.items():
    if m in parent: union(m, t)
groups = collections.OrderedDict()
for e in keep: groups.setdefault(find(e['id']), []).append(e)
def fold_of(root): return next((t for t in FOLD if t in parent and find(t) == root), None)
for root, parts in groups.items():
    t = fold_of(root)
    if t: parts.sort(key=lambda e: e['id'] != t)

VAR = [('sulphur', 'sulfur'), ('center', 'centre')]
def variants(k):
    out = [k]
    for a, b in VAR:
        for x, y in ((a, b), (b, a)):
            if re.search(x, k, re.I): out.append(re.sub(x, y, k, flags=re.I) if k.islower() else re.sub(x, y, k).replace(x.capitalize(), y.capitalize()))
    return out
MAXW = R['thin'].get('max_key_words', 6)
KEEPART = set(R['keep_article'])
def ok(k): return k and len(k) >= 3 and not re.search(r'[,:“”"‘…]|\.\.\.|^\d+$', k) and len(k.split()) <= MAXW
def cand_keys(e):
    n = 0
    for f in [e['headword']] + e['forms']:
        f = re.sub(r'\s*\([^)]*\)', '', f)
        for k in re.split(r'\s+/\s+|;\s*', f):
            k = k.strip().strip('.').strip()
            if e['id'] not in KEEPART: k = ART.sub('', k)
            if ok(k): n += 1; yield from variants(k)
    if not n:  # last resort: split a list headword into its parts
        for k in re.split(r',\s*|\s+and\s+', e['headword']):
            k = ART.sub('', k.strip())
            if ok(k) and k.lower() not in T2: yield from variants(k)
def canon(k):
    k = k.lower()
    for a, b in VAR: k = k.replace(b, a)
    return sing(k)

def build_keys(parts, extra=()):
    keys = []
    for k in extra:
        if k.lower() not in [x.lower() for x in keys]: keys.append(k)
    for e in parts:
        for k in cand_keys(e):
            if k.lower() not in [x.lower() for x in keys]: keys.append(k)
        k = e['headword']  # simple plural of a one-word term headword (whole-word matching misses plurals)
        if e['kind'] == 'term' and re.fullmatch(r'[A-Za-z]{4,}', k) and not re.search(r'(s|x|z|ch|sh|y|fe|f|al|ed|ic|ous|ive|ism|ry)$', k, re.I):
            for v in variants(k):
                if (v + 's').lower() not in [x.lower() for x in keys]: keys.append(v + 's')
    heads = {canon(hnorm(e['headword'])) for e in parts}
    gated = any(e['id'] in KEEPART and ART.sub('', e['headword']).lower() in T2 for e in parts)
    for k in list(keys):
        if ' ' not in k and k.lower() in T2:
            if canon(k) in heads: gated = True
            elif len(keys) > 1: keys.remove(k)
            else: gated = True
    return keys, gated

def unredundant(keys):
    """Drop a key when a shorter key of the same entry matches inside it as whole words (it would fire anyway)."""
    out = []
    for a in keys:
        if a.lower() in [x.lower() for x in out]: continue
        if any(b.lower() != a.lower() and len(b) < len(a) and re.search(r'(?<!\w)' + re.escape(b) + r'(?!\w)', a, re.I) for b in keys): continue
        out.append(a)
    return out
REDUNDANT = 0
def secondary(keys):
    out = []
    for c in R['context_keys']:
        if c.startswith('/'):
            m = re.fullmatch(r'/(.*)/(\w*)', c); rx = re.compile(m.group(1), re.I)
            if any(rx.fullmatch(k) for k in keys): continue
        elif c.lower() in [k.lower() for k in keys]: continue
        out.append(c)
    return out

OV = {k: v for k, v in R.get('worldbook_overrides', {}).items() if not k.startswith('_')}
entries, rows = {}, []
for g, parts in groups.items():
    ft = fold_of(g)
    keys, gated = build_keys(parts, FOLD[ft]['add_keys'] if ft else ())
    name = FOLD[ft]['name'] if ft else ' + '.join(e['headword'] for e in parts)
    logic, sec = 0, None
    for e in parts:
        o = OV.get(e['id'])
        if not o: continue
        if 'keys' in o: keys = list(o['keys'])
        keys += [k for k in o.get('add_keys', []) if k.lower() not in [x.lower() for x in keys]]
        keys = [k for k in keys if k.lower() not in [x.lower() for x in o.get('remove_keys', [])]]
        if 'secondary' in o: sec, logic = list(o['secondary']), o.get('logic', 0)
    if not keys:
        for e in parts: dropped.append((e, 'no usable trigger key'))
        continue
    blocks = []
    for e in parts:
        head = e['headword'] + (f" — {e['label']}" if e['label'] else '')
        c = f"[{KIND[e['kind']]}: {head}]\n{clean(e['summary'])}" + (f"\n\n{clean(e['body'])}" if e['body'] else '')
        eq = [by[q['entry']]['headword'] if q.get('entry') and q['entry'] in by else q.get('with', '') for q in e['equivalences']]
        eq = [x for x in dict.fromkeys(eq) if x]
        if eq: c += '\n\nIdentified in the text with: ' + '; '.join(eq) + '.'
        sa = [by[i]['headword'] for i in e['see_also'] if i in by]
        if sa: c += '\nRelated: ' + '; '.join(sa) + '.'
        blocks.append(c)
    n0 = len(keys); keys = unredundant(keys); REDUNDANT += n0 - len(keys)
    if sec is None: sec = secondary(keys) if gated else []
    uid = len(entries)
    ids = [i for e in parts for i in [e['id']] + e['merged']]
    entries[str(uid)] = {'uid': uid, 'key': keys, 'keysecondary': sec,
        'comment': name + f" ({', '.join(sorted({e['kind'] for e in parts}))}; {', '.join(ids)})",
        'content': '\n\n'.join(blocks), 'constant': False, 'selective': bool(sec), 'selectiveLogic': logic, 'addMemo': True,
        'order': 100, 'position': 1, 'disable': False, 'excludeRecursion': False, 'preventRecursion': False,
        'delayUntilRecursion': False, 'probability': 100, 'useProbability': False, 'depth': 4}
    rows.append((name + (' ← ' + '; '.join(e['headword'] for e in parts[1:]) if ft else ''), keys, ('ctx' if logic == 0 else 'NOT ' + ', '.join(sec)) if sec and (logic or len(sec) > 3) else (('needs ' + ', '.join(sec)) if sec else '')))
uid = len(entries)
entries[str(uid)] = {'uid': uid, 'key': [], 'keysecondary': [], 'comment': 'READ ME: recommended settings (disabled, never inserted)',
    'content': 'Recommended SillyTavern World Info settings for this lorebook: turn on Recursive Scan and set Max Recursion Steps to 2-3, '
               'so entries can pull in related entries without cascading. Entries whose main word is an everyday word (will, mind, matter, '
               'light, life, work ...) only trigger when a hermetic, religious or esoteric context word is also present (secondary keys, AND ANY). '
               'All other entries trigger on their keys alone.',
    'constant': False, 'selective': False, 'selectiveLogic': 0, 'addMemo': True, 'order': 0, 'position': 1, 'disable': True,
    'excludeRecursion': True, 'preventRecursion': True, 'delayUntilRecursion': False, 'probability': 100, 'useProbability': False, 'depth': 4}
out = {'entries': entries, 'name': 'Atwood Hermetic Mystery Lorebook',
       'description': "Dictionary of terms, persons, works and voices in Mary Anne Atwood's A Suggestive Inquiry into the Hermetic Mystery (1850), drawn only from the book. Appendix (Table Talk, begun 1860) material is labelled as a later layer."}
json.dump(out, open('lorebook/Atwood_Hermetic_Mystery.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
K = ['# Worldbook keys (draft)', '', f'{len(entries) - 1} entries (+1 disabled READ ME). “ctx” = needs a context word (secondary keys, AND ANY).', '',
     '| entry | keys | ctx |', '|---|---|---|'] + [f"| {h} | {', '.join(k)} | {s} |" for h, k, s in sorted(rows, key=lambda r: r[0].lower())]
K += ['', '## Not in the worldbook', '', '| entry | reason |', '|---|---|'] + [f"| {e['headword']} | {w} |" for e, w in sorted(dropped, key=lambda x: (x[1], x[0]['headword'].lower()))]
open('work/review/worldbook_keys.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(K) + '\n')
print('redundant keys removed', REDUNDANT, '| worldbook entries', len(entries) - 1, '| gated', sum(1 for r in rows if r[2]), '| dropped', collections.Counter(w for _, w in dropped))
