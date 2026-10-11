"""Render dictionary entries.
  python3 scripts/dict_render.py check B001   -> validate work/dict/out/B001.json, write work/dict/out/B001.md (for quote_check_doc.py)
  python3 scripts/dict_render.py all          -> work/dict/dictionary.json (+ uncleaned render work/dict/22_raw.md)
Since the 2026-10-11 cleanup src/22 is written by dict_clean.py, not here."""
import json, sys, re, glob, unicodedata
R = 'work/dict/'
E = json.load(open(R + 'entries.json', encoding='utf-8')); byid = {e['id']: e for e in E}
KIND = {'term': 'term', 'person': 'person', 'treatise': 'treatise', 'collective': 'collective voice'}
def letter(h):
    c = re.sub(r'^(the|a|an)\s+', '', unicodedata.normalize('NFKD', h).encode('ascii', 'ignore').decode().lstrip('"\'“‘( '), flags=re.I).upper()[:1]
    return c if c.isalpha() else '#'
def anchor(e): return e['id'].lower()
def md(e, w):
    L = [f'<a id="{anchor(e)}"></a>', f"### {e['headword']}"]
    forms = [f for f in (w.get('forms') if w else e['forms']) if f != e['headword']]
    L.append(f"*{KIND[e['kind']]}*" + (' · ' + ', '.join(forms) if forms else ''))
    if w: L += ['', f"**{w['summary']}**", '', w['body'].strip()]
    else: L += ['', 'Cited for reference only.']
    sa = [f"[{byid[q['entry']]['headword']}](#{q['entry'].lower()}) [{q['ref']}]" if q.get('entry') else f"{q['with']} [{q['ref']}]" for q in e['equivalences']]
    if sa: L += ['', '**Identified with:** ' + '; '.join(sa)]
    if e['refs']: L += ['', '**References:** ' + ', '.join(e['refs'])]
    return '\n'.join(L)
if sys.argv[1] == 'check':
    b = sys.argv[2]; w = json.load(open(R + f'out/{b}.json', encoding='utf-8'))
    ids = [e['id'] for e in E if e.get('batch') == b]
    miss = [i for i in ids if i not in w]; extra = [i for i in w if i not in ids]
    bad = [i for i in ids if i in w and not all(isinstance(w[i].get(k), t) for k, t in (('forms', list), ('summary', str), ('body', str)))]
    open(R + f'out/{b}.md', 'w', encoding='utf-8', newline='\n').write('\n\n'.join(md(byid[i], w[i]) for i in ids if i in w and i not in bad))
    print(b, len(ids), 'missing', miss, 'extra', extra, 'malformed', bad); sys.exit(1 if miss or bad else 0)
W = {}
for f in sorted(glob.glob(R + 'out/B*.json')): W.update(json.load(open(f, encoding='utf-8')))
miss = [e['id'] for e in E if e.get('batch') and e['id'] not in W]
if miss: sys.exit(f'missing entries: {miss[:20]} ({len(miss)})')
out = ['# Master Lexicon and Concordance', '',
       'Terms, persons, works and voices of *A Suggestive Inquiry into the Hermetic Mystery* (1850), drawn only from the book. '
       'Quotes are verbatim; references point to chapter paragraphs (¶) and footnotes (n). Refs beginning `APP` are the Appendix '
       '(Table Talk, begun 1860), a later layer. "Identified with" lists only identities the text itself asserts; the many other names '
       'for one thing are kept as separate entries.', '']
cur = None
for e in E:
    l = letter(e['headword'])
    if l != cur: out += [f'## {l}', '']; cur = l
    out += [md(e, W.get(e['id'])), '']
open(R + '22_raw.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
dic = [dict({k: e[k] for k in ('id', 'kind', 'headword', 'forms', 'equivalences', 'refs')}, **({'forms': W[e['id']]['forms'], 'summary': W[e['id']]['summary'], 'body': W[e['id']]['body']} if e['id'] in W else {'summary': 'Cited for reference only.', 'body': ''})) for e in E]
json.dump(dic, open(R + 'dictionary.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('rendered', len(E), 'entries')
