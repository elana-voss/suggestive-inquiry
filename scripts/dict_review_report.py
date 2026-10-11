"""Write work/review/REVIEW_REPORT.md comparing the pre-cleanup state (git commit BASE) with the current lexicon/worldbook.
  python3 scripts/dict_review_report.py [BASE]   (default BASE 285de1b; run after dict_clean.py and dict_worldbook_v2.py)
Needs work/dict/dictionary.json (the uncleaned dictionary, from dict_render.py all) for the before-side of headword counts."""
import json, re, collections, subprocess, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else '285de1b'
R = json.load(open('scripts/lexicon_rules.json', encoding='utf-8'))
D = json.load(open('work/dict/dictionary.json', encoding='utf-8')); by = {e['id']: e for e in D}
N = json.load(open('work/dict/dictionary_v2.json', encoding='utf-8')); nb = {e['id']: e for e in N}
O = json.loads(subprocess.run(['git', 'show', f'{BASE}:lorebook/Atwood_Hermetic_Mystery.json'], capture_output=True, check=True).stdout.decode('utf-8'))['entries']
W = json.load(open('lorebook/Atwood_Hermetic_Mystery.json', encoding='utf-8'))['entries']
def kstats(E):
    ks = [k for e in E.values() for k in e['key']]; kc = collections.Counter(k.lower() for k in ks)
    return [len(E), len(ks), sum(1 for k in ks if re.search(r'[(),/;:]', k)), sum(1 for k in ks if re.match(r'(?i)(the|a|an) ', k)),
            sum(1 for c in kc.values() if c > 1), sum(1 for e in E.values() if e['keysecondary'])]
o, w = kstats(O), kstats({k: v for k, v in W.items() if not v['disable']})
hw = lambda L: [sum(1 for e in L if re.match(r'(?i)(the|a|an) ', e['headword'])), sum(1 for e in L if re.search(r'[()/;]', e['headword'])),
                sum(1 for e in L if e['headword'][:1].islower())]
ho, hn = hw(D), hw(N)
def lab(e): return e['headword'] + (f" ({e['label']})" if e.get('label') else '')
L = ['# Review report: lexicon and worldbook cleanup', '',
     f'Before = git commit `{BASE}`; after = current `src/22_Master_Lexicon_and_Concordance.md` and `lorebook/Atwood_Hermetic_Mystery.json`. Regenerate with:', '',
     '```bash', 'python3 scripts/dict_render.py all     # -> work/dict/dictionary.json', 'python3 scripts/dict_clean.py          # -> src/22_Master_Lexicon_and_Concordance.md, work/dict/dictionary_v2.json, work/review/headword_mapping.md',
     'python3 scripts/dict_worldbook_v2.py   # -> lorebook/Atwood_Hermetic_Mystery.json, work/review/worldbook_keys.md',
     'python3 scripts/dict_review_report.py  # -> work/review/REVIEW_REPORT.md', '```', '',
     'Editorial decisions live in `scripts/lexicon_rules.json` (renames, merges, folds, article exceptions, tier-2 words, context keys, per-entry key overrides). Change it and re-run.', '',
     '## Files', '',
     '| file | what it is |', '|---|---|',
     '| `src/22_Master_Lexicon_and_Concordance.md` | the cleaned lexicon |',
     '| `lorebook/Atwood_Hermetic_Mystery.json` | the cleaned worldbook |',
     '| `work/review/headword_mapping.md` | every changed headword, old → new |',
     '| `work/review/worldbook_keys.md` | every worldbook entry with its keys |',
     '| `scripts/lexicon_rules.json` | the editable rules |', '',
     '## Numbers', '',
     '| | before | after |', '|---|---|---|',
     f'| lexicon entries | {len(D)} | {len(N)} |',
     f'| headwords starting with the/a/an | {ho[0]} | {hn[0]} |',
     f'| headwords with brackets, slashes or semicolons | {ho[1]} | {hn[1]} |',
     f'| headwords starting lower-case | {ho[2]} | {hn[2]} |',
     f'| lexicon entries with “See also” links | 0 | {sum(1 for e in N if e["see_also"])} |',
     f'| worldbook entries | {o[0]} | {w[0]} (+1 disabled READ ME) |',
     f'| worldbook keys | {o[1]} | {w[1]} |',
     f'| keys with brackets, commas, slashes, colons | {o[2]} | {w[2]} |',
     f'| keys starting with the/a/an | {o[3]} | {w[3]} (titles and terms that need the article) |',
     f'| keys shared by more than one entry | {o[4]} | {w[4]} |',
     f'| entries with secondary keys | {o[5]} | {w[5]} |', '',
     'The text of every entry is unchanged: each original summary and body appears verbatim in the draft lexicon, and every old anchor (`#e0001` …) still resolves.', '',
     '## Your examples', '', '| before | after |', '|---|---|']
for i in ('E1625', 'E1627', 'E1036', 'E1038', 'E0899', 'E0898', 'E1231', 'E1232', 'E1644', 'E1690', 'E0612'):
    t = nb.get(i) or next(e for e in N if i in e['merged'])
    L.append(f'| {by[i]["headword"]} | {lab(t)}{" (merged)" if t["id"] != i else ""} |')
def wkeys(sub):
    for v in W.values():
        if sub in v['comment']: return v
for name, sub in (('Isis', 'E0897'), ('Oracle of Apollo', 'E1231'), ('Oracle to Amelius', 'E1232'), ('Oracles', 'E1233'), ('Spirit', 'E1644'), ('Agent', 'E0031'), ('Book of Revelation', 'E1499')):
    v = wkeys(sub)
    L.append(f'| worldbook {name}: keys | `{", ".join(v["key"])}`' + (f' + {"NOT " if v["selectiveLogic"] == 2 else ""}secondary ({len(v["keysecondary"])}: {", ".join(v["keysecondary"][:4])}{" …" if len(v["keysecondary"]) > 4 else ""})' if v['keysecondary'] else '') + ' |')
L += ['', '## Rules applied', '',
      '**Headwords.** Leading “the/a/an” (and “some/these/those”; for persons, voices and works also “our/my/his/her”) removed, except for '
      f'{len(R["keep_article"])} entries where the article belongs to a title or the term (' + ', '.join(nb[i]['headword'] for i in R['keep_article'] if i in nb) + '). '
      'Bracketed notes moved out of the headword into an italic label after the kind. Slash pairs became “X and Y”, or the first name with the others as forms; '
      f'{len(R["rename"])} list-like or awkward headwords were renamed by hand (see `rename` in the rules file). '
      'First letter always capital; inside a headword, a word is capitalised only if the book capitalises it in most mid-sentence uses, so the same word is cased the same in every headword '
      '(e.g. *spirit* is lower-case in all compounds, *Wisdom* capitalised). This applies to terms; persons, works, group voices and hand-renamed headwords keep their own casing.', '',
      '**Spelling.** Headwords follow the book’s majority: *sulphur* (47 chapter uses vs 28 *sulfur*), *center* (64 vs 5 *centre*). Worldbook keys include both spellings.', '',
      '**Synonyms.** Merges only where entries are clearly one subject (below). Otherwise “See also” links, made mechanically: entries sharing a name or form, '
      'homonyms, and a compound pointing to its head word (*Red sulphur* → *Sulphur*). “Identified with” (identities the text asserts) is kept as before.', '',
      '**Worldbook.** One entry per subject; lexicon homonyms with the same headword are combined into one worldbook entry (e.g. *Adept* + *Adepts*). '
      'Keys = headword and text forms, without notes, articles or commas; at most six words; both spellings; a simple plural for one-word terms; '
      'a key is dropped when a shorter key of the same entry already matches inside it (e.g. “the Spirit”, “our Mercury”).', '',
      f'**Everyday words.** {w[5]} entries whose own headword is an everyday word (`tier2_words`) need one context word as well (secondary keys, AND ANY). '
      'Where an everyday word is only a side form of an entry, that key is dropped instead, so the entry stays ungated. All other entries trigger on their keys alone.', '',
      'Context words (`context_keys`): ' + ', '.join(f'`{c}`' for c in R['context_keys']), '',
      '**Per-entry overrides** (`worldbook_overrides`): Book of Revelation keys = revelation, apocalypse, St John; the Bible no longer triggers on “revelation”; '
      'Oracle to Amelius = oracle + Amelius; the general Oracles entry does not fire when Amelius or Apollo is present (NOT ANY); “Author of X” entries without a work entry trigger on the title; '
      'a few keys inherited from folded entries that nobody would type, or that belong to another entry (e.g. “Master”, “Philosophers” on Norton), are removed.', '',
      '**Recursion.** Cannot be set in the file. A disabled READ ME entry recommends Recursive Scan on and Max Recursion Steps 2–3.', '',
      '## Merged lexicon entries', '']
for e in N:
    if e['merged']: L.append(f'- **{lab(e)}** ← ' + '; '.join(by[i]['headword'] for i in [e['id']] + e['merged']))
wm = [v['comment'] for v in W.values() if ' + ' in v['comment'].split(' (')[0]]
L += ['', '## Combined only in the worldbook (same headword in the lexicon)', ''] + [f'- {c}' for c in wm]
fold = [l for l in open('work/review/worldbook_keys.md', encoding='utf-8').read().splitlines() if ' ← ' in l]
L += ['', '## Folded in the worldbook (school or group name as the trigger)', '',
      'Fine-grained lexicon entries that a roleplayer would only reach by the school, group or work name are combined into that name’s worldbook entry. '
      'The lexicon keeps them separate and links them with “See also”. Rules: `worldbook_fold` in the rules file.', '',
      '| worldbook entry ← folded lexicon entries | keys | ctx |', '|---|---|---|'] + fold
L += ['', '## Gated entries (need a context word)', '', ', '.join(v['comment'].split(' (')[0] for v in W.values() if v['keysecondary'] and v['selectiveLogic'] == 0)]
drop = open('work/review/worldbook_keys.md', encoding='utf-8').read().split('## Not in the worldbook')[1]
dc = collections.Counter(re.findall(r'\| ([^|]+) \|\n', drop))
L += ['', '## Left out of the worldbook', '', 'Full list with reasons at the end of `worldbook_keys.md`. Counts:', ''] + [f'- {k}: {v}' for k, v in dc.most_common() if k != 'reason' and not k.startswith('-')]
if not R['thin'].get('enabled', True): L += ['', 'None: the thin filter is off (`thin.enabled` = false), so every lexicon entry is in the worldbook (folded entries inside their target).']
else: L += []
L += ['', '## Worth a look', '',
      '- Casing is by the book’s majority per word, so some phrases look different from how they appear in one passage (*material Rites* → *Material rites*).',
      '- Six entries with only long descriptive headwords got short keys by hand (`worldbook_overrides`), e.g. *Dry water of the sea of the wise* → “dry water”; *Unattributed sayings* → maxim, proverb, Latin verse, unattributed.',
      '- “Revelation” fires both the Book of Revelation and the short term *Revelation* (Kirchringius); left as is, since more triggering was preferred.',
      '- Entries that the book only cites for reference carry no text beyond “Cited for reference only.”; they are in the worldbook as asked, but add nothing when they fire.']
open('work/review/REVIEW_REPORT.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('report written', len(L), 'lines')
