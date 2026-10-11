"""Clean the dictionary and render the Master Lexicon (step 2 of 3, see RUNBOOK "Lexicon and worldbook cleanup").
  python3 scripts/dict_clean.py
Reads work/dict/dictionary.json (from dict_render.py all) + scripts/lexicon_rules.json + input/*.txt
Writes src/22_Master_Lexicon_and_Concordance.md, work/dict/dictionary_v2.json (worldbook input), work/review/headword_mapping.md"""
import json, re, glob, collections, unicodedata
R = json.load(open('scripts/lexicon_rules.json', encoding='utf-8'))
D = json.load(open('work/dict/dictionary.json', encoding='utf-8'))
by = {e['id']: e for e in D}
OUT = 'work/review/'
import os; os.makedirs(OUT, exist_ok=True)

# ---- book text: casing statistics (mid-sentence occurrences only) ----
TXT = '\n'.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob('input/0*.txt')) if 'front' not in f)
SPELL = R['spelling']
def respell(s):
    for a, b in SPELL.items(): s = re.sub(r'\b' + a, b, s)
    return s
TXTS = respell(TXT)
wc = collections.defaultdict(lambda: [0, 0])  # word.lower() -> [capitalised, lowercase]
for m in re.finditer(r"[A-Za-z][a-z’'\-]*", TXTS):
    w = m.group(0); pre = TXTS[max(0, m.start() - 3):m.start()]
    if re.search(r'([.!?:;“"(\[—]\s*|\n\s*)$', pre) or m.start() == 0: continue
    wc[w.lower()][0 if w[0].isupper() else 1] += 1
SMALL = {'of', 'the', 'and', 'in', 'to', 'a', 'an', 'on', 'by', 'with', 'for', 'from', 'or', 'at', 'as', 'his', 'her', 'their', 'our', 'its', 'de', 'la', 'le', 'du', 'von', 'van'}
def phrase_case(h):
    """Most common mid-sentence casing of the phrase in the book, or None."""
    if ' ' not in h: return None
    pat = re.compile(r'(?<![.!?:;“"(]\s)\b' + r'\s+'.join(map(re.escape, h.split())) + r'\b', re.I)
    c = collections.Counter(m.group(0) for m in pat.finditer(TXTS))
    return re.sub(r'\s+', ' ', c.most_common(1)[0][0]) if c else None
def case_headword(h, kind):
    if kind in ('person', 'treatise'): return h[:1].upper() + h[1:]
    ws = h.split(' ')
    if True:  # word-level book majority, so a word is cased the same in every headword
        for i, w in enumerate(ws):
            if i == 0 or not re.fullmatch(r"[A-Za-z][a-z’'\-]*", w): continue
            lw = w.lower()
            if lw in SMALL: ws[i] = lw; continue
            cap, low = wc.get(lw, (0, 0))
            if cap + low: ws[i] = (lw[:1].upper() + lw[1:]) if cap > low else lw
    for i, w in enumerate(ws):
        if i and w.lower() in SMALL and re.fullmatch(r'[A-Za-z]+', w): ws[i] = w.lower()
    out = ' '.join(ws)
    return out[:1].upper() + out[1:]

ART = re.compile(r'^(the|a|an)\s+', re.I)
DET = re.compile(r'^(some|these|those|this|that|certain)\s+(?=\S)', re.I)
def base_headword(e):
    """-> (headword, label) before casing."""
    if e['id'] in R['rename']: return tuple(R['rename'][e['id']])
    h, label = e['headword'], ''
    m = re.search(r'\s*\(([^)]*)\)\s*$', h)
    if m: label, h = m.group(1), h[:m.start()]
    if e['id'] not in R['keep_article']: h = DET.sub('', ART.sub('', h))
    if e['kind'] != 'term': h = re.sub(r'^(our|my|his|her)\s+(?=\S)', '', h, flags=re.I)
    return h.strip(), label

# ---- merges ----
member = {}
for tgt, others in R['merge'].items():
    for o in others: member[o] = tgt
groups = [[e['id']] + R['merge'].get(e['id'], []) for e in D if e['id'] not in member]

REFKEY = lambda r: (['I', 'II', 'III', 'IV', 'APP'].index(r.split('.')[0].split(' ')[0]) if r.split('.')[0].split(' ')[0] in ('I', 'II', 'III', 'IV', 'APP') else 9, r)
def nform(f): return ART.sub('', respell(f)).lower().replace('’', "'")
new, mapping = [], []
for g in groups:
    t = by[g[0]]
    if g[0] in R.get('merge_headword', {}): h, label = R['merge_headword'][g[0]]
    else: h, label = base_headword(t)
    h = respell(h)
    if t['kind'] == 'term' and g[0] not in R['rename'] and g[0] not in R.get('merge_headword', {}) and g[0] not in R['keep_article']: h = case_headword(h, t['kind'])
    elif t['id'] in R['keep_article'] or True: h = h[:1].upper() + h[1:]
    parts = [by[i] for i in g]
    forms, seen = [], {nform(h)}
    for p in parts:
        for f in [x for f0 in [p['headword']] + p['forms'] for x in re.split(r'\s+/\s+|;\s+', f0)]:
            if g[0] in R.get('merge_summary', {}): break
            f = respell(f.strip())
            if re.search(r'[()]', f) or not f: continue
            n = nform(f)
            if n in seen: continue
            seen.add(n); forms.append(f)
    summary = R.get('merge_summary', {}).get(g[0], t['summary'])
    body = t['body'].strip()
    if g[0] in R.get('merge_summary', {}): body = ''
    for p in parts[1 if g[0] not in R.get('merge_summary', {}) else 0:]:
        ph, pl = base_headword(p)
        lead = (ph + (f' ({pl})' if pl else '')) if ph else (pl or p['headword'])
        lead = lead.replace(' / ', ' and '); lead = lead[:1].upper() + lead[1:]
        if p['body']:
            body += f"\n\n*{lead}.* {p['body'].strip()}"
    refs = sorted({r for p in parts for r in p['refs']}, key=REFKEY)
    eqs = [q for p in parts for q in p['equivalences']]
    for q in eqs:
        if q.get('entry') in member: q['entry'] = member[q['entry']]
    ne = {'id': g[0], 'merged': g[1:], 'kind': t['kind'], 'headword': h, 'label': label, 'forms': forms,
          'equivalences': eqs, 'refs': refs, 'summary': respell(summary) if False else summary, 'body': body.strip(),
          'reference_only': not any(p['body'] for p in parts)}
    new.append(ne)
    for p in parts: mapping.append((p['id'], p['headword'], h + (f' ({label})' if label else ''), 'merged into ' + g[0] if p['id'] != g[0] else ''))

# ---- See also (mechanical, conservative) ----
nb = {e['id']: e for e in new}
def key_n(s): return re.sub(r'[^a-z0-9 ]', '', ART.sub('', s.lower()).replace('’', "'"))
def sing(w): return w[:-1] if len(w) > 3 and w.endswith('s') and not w.endswith('ss') else w
def hnorm(s): return ' '.join(sing(w) for w in key_n(s).split())
byh = collections.defaultdict(set); byform = collections.defaultdict(set)
for e in new:
    byh[hnorm(e['headword'])].add(e['id'])
    for f in [e['headword']] + e['forms']:
        n = hnorm(f)
        if len(n) >= 3: byform[n].add(e['id'])
seealso = collections.defaultdict(set)
for ids in list(byh.values()) + list(byform.values()):
    if 1 < len(ids) <= 6:
        for a in ids: seealso[a] |= ids - {a}
single = {hnorm(e['headword']): e['id'] for e in new if len(hnorm(e['headword']).split()) == 1}
for e in new:  # compound -> its head noun entry (e.g. Red Sulphur -> Sulphur)
    ws = hnorm(e['headword']).split()
    if len(ws) > 1 and ws[-1] in single and single[ws[-1]] != e['id']: seealso[e['id']].add(single[ws[-1]])
idmap = {o: e['id'] for e in new for o in [e['id']] + e['merged']}
for t, v in R.get('worldbook_fold', {}).items():  # entries combined in the worldbook link to each other here
    if t.startswith('_'): continue
    t2 = idmap[t]
    for m in v['members']:
        m2 = idmap[m]
        if m2 != t2: seealso[m2].add(t2); seealso[t2].add(m2)
asserted = {e['id']: {q['entry'] for q in e['equivalences'] if q.get('entry')} for e in new}
for e in new:
    e['see_also'] = sorted(seealso[e['id']] - asserted[e['id']] - {e['id']}, key=lambda i: (nb[i]['headword'].lower(), i))

# ---- render ----
KIND = {'term': 'term', 'person': 'person', 'treatise': 'treatise', 'collective': 'collective voice'}
def sortkey(e): return unicodedata.normalize('NFKD', ART.sub('', e['headword'])).encode('ascii', 'ignore').decode().lstrip('"\'“‘( ').lower()
new.sort(key=sortkey)
def letter(e):
    c = sortkey(e)[:1].upper(); return c if c.isalpha() else '#'
def link(i): return f"[{nb[i]['headword']}{' (' + nb[i]['label'] + ')' if nb[i]['label'] else ''}](#{i.lower()})"
L = ['# Master Lexicon and Concordance', '',
     'Terms, persons, works and voices of *A Suggestive Inquiry into the Hermetic Mystery* (1850), drawn only from the book. '
     'Quotes are verbatim; references point to chapter paragraphs (¶) and footnotes (n). Refs beginning `APP` are the Appendix '
     '(Table Talk, begun 1860), a later layer.', '',
     '**Conventions.** Headwords start with a capital letter; inside a headword, a word is capitalised only where the book itself '
     'mostly capitalises it. A leading “the” is dropped unless it belongs to a title or the term needs it. Spelling follows the book’s '
     'majority use (*Sulphur*, *center*); other spellings and word forms found in the text are listed after the kind. A note in italics '
     'after the kind tells homonyms apart. “Identified with” lists only identities the text itself asserts; “See also” links related '
     'entries editorially (shared names or forms, or a compound and its head word) and asserts no identity.', '']
cur = None
for e in new:
    l = letter(e)
    if l != cur: L += [f'## {l}', '']; cur = l
    L += [f'<a id="{e["id"].lower()}"></a>' + ''.join(f'<a id="{m.lower()}"></a>' for m in e['merged']), f"### {e['headword']}"]
    L.append(f"*{KIND[e['kind']]}*" + (f" — *{e['label']}*" if e['label'] else '') + (' · ' + ', '.join(e['forms']) if e['forms'] else ''))
    if e['reference_only']: L += ['', 'Cited for reference only.']
    else: L += ['', f"**{e['summary']}**", '', e['body']]
    sa = [f"{link(q['entry'])} [{q['ref']}]" if q.get('entry') else f"{q['with']} [{q['ref']}]" for q in e['equivalences']]
    if sa: L += ['', '**Identified with:** ' + '; '.join(sa)]
    if e['see_also']: L += ['', '**See also:** ' + ', '.join(link(i) for i in e['see_also'])]
    if e['refs']: L += ['', '**References:** ' + ', '.join(e['refs'])]
    L.append('')
open('src/22_Master_Lexicon_and_Concordance.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
json.dump(new, open('work/dict/dictionary_v2.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# Headword mapping (old → new)', '', '| id | old headword | new headword | note |', '|---|---|---|---|']
M += [f'| {i} | {o} | {n} | {note} |' for i, o, n, note in sorted(mapping) if o != n.split(' (')[0] or note or '(' in o]
open(OUT + 'headword_mapping.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('entries', len(D), '->', len(new), '| changed headwords', len(M) - 4)
