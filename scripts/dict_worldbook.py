"""Build the SillyTavern worldbook from work/dict/dictionary.json (one entry per dictionary concept).
  python3 scripts/dict_worldbook.py -> lorebook/Atwood_Hermetic_Mystery.json"""
import json, re, sys
sys.exit('Superseded by scripts/dict_worldbook_v2.py (2026-10-11 cleanup, see RUNBOOK). Old version: git show 285de1b:scripts/dict_worldbook.py')
D = json.load(open('work/dict/dictionary.json', encoding='utf-8'))
by = {e['id']: e for e in D}
KIND = {'term': 'Term', 'person': 'Person', 'treatise': 'Treatise', 'collective': 'Voice'}
REF = re.compile(r'\s*\[(?:cf\. )?(?:I|II|III|IV|APP)[.\s][^\]]*\]')
def clean(t): return re.sub(r'[ \t]+([,.;:])', r'\1', REF.sub('', t)).strip()
entries = {}
for e in D:
    if not e.get('body'): continue  # reference-only citations carry no content
    keys = []
    for k in [e['headword']] + e['forms'] + [re.sub(r'^(the|a|an)\s+', '', f, flags=re.I) for f in [e['headword']] + e['forms']]:
        k = k.strip()
        if len(k) >= 3 and k.lower() not in [x.lower() for x in keys]: keys.append(k)
    keys = keys[:10]
    eq = [by[q['entry']]['headword'] if q.get('entry') else q['with'] for q in e['equivalences']]
    c = f"[{KIND[e['kind']]}: {e['headword']}]\n{clean(e['summary'])}\n\n{clean(e['body'])}"
    if eq: c += '\n\nIdentified in the text with: ' + '; '.join(dict.fromkeys(eq)) + '.'
    uid = len(entries)
    entries[str(uid)] = {'uid': uid, 'key': keys, 'keysecondary': [], 'comment': f"{e['headword']} ({e['kind']}, {e['id']})",
        'content': c, 'constant': False, 'selective': False, 'selectiveLogic': 0, 'addMemo': True, 'order': 100,
        'position': 1, 'disable': False, 'excludeRecursion': False, 'probability': 100, 'useProbability': False, 'depth': 4}
out = {'entries': entries, 'name': 'Atwood Hermetic Mystery Lorebook',
       'description': "Dictionary of terms, persons, works and voices in Mary Anne Atwood's A Suggestive Inquiry into the Hermetic Mystery (1850), drawn only from the book. Appendix (Table Talk, begun 1860) material is labelled as a later layer."}
json.dump(out, open('lorebook/Atwood_Hermetic_Mystery.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print(len(entries), 'entries')
