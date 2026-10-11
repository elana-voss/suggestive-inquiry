# Review report: lexicon and worldbook cleanup

Before = git commit `285de1b`; after = current `src/22_Master_Lexicon_and_Concordance.md` and `lorebook/Atwood_Hermetic_Mystery.json`. Regenerate with:

```bash
python3 scripts/dict_render.py all     # -> work/dict/dictionary.json
python3 scripts/dict_clean.py          # -> src/22_Master_Lexicon_and_Concordance.md, work/dict/dictionary_v2.json, work/review/headword_mapping.md
python3 scripts/dict_worldbook_v2.py   # -> lorebook/Atwood_Hermetic_Mystery.json, work/review/worldbook_keys.md
python3 scripts/dict_review_report.py  # -> work/review/REVIEW_REPORT.md
```

Editorial decisions live in `scripts/lexicon_rules.json` (renames, merges, folds, article exceptions, tier-2 words, context keys, per-entry key overrides). Change it and re-run.

## Files

| file | what it is |
|---|---|
| `src/22_Master_Lexicon_and_Concordance.md` | the cleaned lexicon |
| `lorebook/Atwood_Hermetic_Mystery.json` | the cleaned worldbook |
| `work/review/headword_mapping.md` | every changed headword, old → new |
| `work/review/worldbook_keys.md` | every worldbook entry with its keys |
| `scripts/lexicon_rules.json` | the editable rules |

## Numbers

| | before | after |
|---|---|---|
| lexicon entries | 1964 | 1921 |
| headwords starting with the/a/an | 152 | 13 |
| headwords with brackets, slashes or semicolons | 102 | 0 |
| headwords starting lower-case | 863 | 0 |
| lexicon entries with “See also” links | 0 | 776 |
| worldbook entries | 1920 | 1843 (+1 disabled READ ME) |
| worldbook keys | 3032 | 2630 |
| keys with brackets, commas, slashes, colons | 177 | 0 |
| keys starting with the/a/an | 220 | 14 (titles and terms that need the article) |
| keys shared by more than one entry | 80 | 55 |
| entries with secondary keys | 0 | 47 |

The text of every entry is unchanged: each original summary and body appears verbatim in the draft lexicon, and every old anchor (`#e0001` …) still resolves.

## Your examples

| before | after |
|---|---|
| some modern Kabalists | Modern Kabalists |
| the son of Dirach | Son of Dirach |
| the material | Material |
| material Rites | Material rites |
| Isis (the old mythology) | Isis (merged) |
| Isis / Osiris | Fable of Isis and Osiris (merged) |
| Oracle of Apollo, from Eusebius | Oracle of Apollo (from Eusebius) |
| the oracle (to Amelius) | Oracle to Amelius |
| Spirit | Spirit |
| Sulphur | Sulphur |
| fixed sulfur | Fixed sulphur |
| worldbook Isis: keys | `Isis` |
| worldbook Oracle of Apollo: keys | `Oracle of Apollo` |
| worldbook Oracle to Amelius: keys | `oracle, oracles` + secondary (1: Amelius) |
| worldbook Oracles: keys | `Oracles, oracle, Oracula Chaldaica, Zoroastri Oracula` + NOT secondary (2: Amelius, Apollo) |
| worldbook Spirit: keys | `Spirit, spirits` |
| worldbook Agent: keys | `Agent, agents` + secondary (59: god, divine, holy, sacred …) |
| worldbook Book of Revelation: keys | `Revelation, Apocalypse, St John, St. John` |

## Rules applied

**Headwords.** Leading “the/a/an” (and “some/these/those”; for persons, voices and works also “our/my/his/her”) removed, except for 13 entries where the article belongs to a title or the term (The All, The Thing, The Fourth, The Name, The Power, The Critic, The Hermetic Wedding, A True and Faithful Relation of what passed for many years between Dr John Dee and some Spirits, A priori, A priori ground, The desirable, The experienced, The Wise). Bracketed notes moved out of the headword into an italic label after the kind. Slash pairs became “X and Y”, or the first name with the others as forms; 123 list-like or awkward headwords were renamed by hand (see `rename` in the rules file). First letter always capital; inside a headword, a word is capitalised only if the book capitalises it in most mid-sentence uses, so the same word is cased the same in every headword (e.g. *spirit* is lower-case in all compounds, *Wisdom* capitalised). This applies to terms; persons, works, group voices and hand-renamed headwords keep their own casing.

**Spelling.** Headwords follow the book’s majority: *sulphur* (47 chapter uses vs 28 *sulfur*), *center* (64 vs 5 *centre*). Worldbook keys include both spellings.

**Synonyms.** Merges only where entries are clearly one subject (below). Otherwise “See also” links, made mechanically: entries sharing a name or form, homonyms, and a compound pointing to its head word (*Red sulphur* → *Sulphur*). “Identified with” (identities the text asserts) is kept as before.

**Worldbook.** One entry per subject; lexicon homonyms with the same headword are combined into one worldbook entry (e.g. *Adept* + *Adepts*). Keys = headword and text forms, without notes, articles or commas; at most six words; both spellings; a simple plural for one-word terms; a key is dropped when a shorter key of the same entry already matches inside it (e.g. “the Spirit”, “our Mercury”).

**Everyday words.** 47 entries whose own headword is an everyday word (`tier2_words`) need one context word as well (secondary keys, AND ANY). Where an everyday word is only a side form of an entry, that key is dropped instead, so the entry stays ungated. All other entries trigger on their keys alone.

Context words (`context_keys`): `god`, `divine`, `holy`, `sacred`, `heaven`, `angel`, `prayer`, `soul`, `spirit`, `spiritual`, `faith`, `grace`, `church`, `temple`, `ritual`, `myth`, `mystery`, `mysteries`, `wisdom`, `enlightenment`, `meditation`, `magic`, `symbol`, `occult`, `/mystic\w*/i`, `esoteric`, `/theurg\w*/i`, `/[kcq]ab+al\w*/i`, `/(neo)?platon\w*/i`, `gnostic`, `rosicrucian`, `/initiat\w*/i`, `/regenerat\w*/i`, `arcanum`, `arcana`, `/alchem\w*/i`, `/hermetic\w*/i`, `hermes`, `/adepts?/i`, `/philosoph\w*/i`, `stone`, `mercury`, `/sul(ph|f)ur\w*/i`, `salt`, `fire`, `water`, `gold`, `elixir`, `/tinct\w*/i`, `/transmut\w*/i`, `quintessence`, `/a?ether\w*/i`, `vessel`, `furnace`, `conjunction`, `/sublimat\w*/i`, `/putref\w*/i`, `/distil\w*/i`, `atwood`

**Per-entry overrides** (`worldbook_overrides`): Book of Revelation keys = revelation, apocalypse, St John; the Bible no longer triggers on “revelation”; Oracle to Amelius = oracle + Amelius; the general Oracles entry does not fire when Amelius or Apollo is present (NOT ANY); “Author of X” entries without a work entry trigger on the title; a few keys inherited from folded entries that nobody would type, or that belong to another entry (e.g. “Master”, “Philosophers” on Norton), are removed.

**Recursion.** Cannot be set in the file. A disabled READ ME entry recommends Recursive Scan on and Max Recursion Steps 2–3.

## Merged lexicon entries

- **Adepts (cited voice)** ← the adept; the wise / adepts; the wise Adept; the wise Adepts
- **Arkite Mysteries** ← Arkite Mysteries; Arkite Mysteries
- **Chaldaic Oracles** ← Chaldaic Oracles; the Chaldaic oracle
- **Divine Oracle** ← the Divine Oracle; divine oracles
- **Ethnics** ← the Ethnics; Ethnic
- **Fable of Isis and Osiris** ← Egyptian Fable of Isis and Osiris; Egyptian Mythology of Isis and Osiris; Isis / Osiris; the fable (Typhon, Osiris, Isis; the Egyptian monarch)
- **Faith** ← faith; Faith
- **Isis** ← Isis; Isis (the old mythology); fable of Isis
- **Mesmerism** ← Mesmerism; Mesmerism
- **Moist nature** ← moist nature; moist natures
- **Mysteries** ← Mysteries; the Mysteries; the mysteries / the wise hierophants
- **Philosophers** ← philosophers; the philosophers
- **Sphinx** ← Sphinx; the Sphinx
- **St Paul** ← St Paul; the great Apostle (St Paul)
- **Theurgists** ← Theurgists; Theurgists
- **Unattributed sayings (quotations, verses and maxims Atwood gives without a named source)** ← (unattributed); another (unnamed); 'it is said' (unattributed); Latin maxim (unattributed); one (unnamed, 'says one'); Others (unnamed philosophers); the same author; unattributed ("as is declared"); unattributed ('as we are abundantly instructed'); unattributed couplet; unattributed Latin tag; unattributed Latin verse; unattributed maxim; unattributed quotation; unattributed saying; unattributed scriptural phrase; unattributed verse; unattributed verse (Helius); unattributed verse on Proteus; unattributed words: 'the fear of the Lord is the beginning of Wisdom'; unnamed ('Alchemy has been declared'); unnamed ('as it is narrated'); unnamed ("he ... who said")

## Combined only in the worldbook (same headword in the lexicon)

- Arabian + Arabians (collective; E0100, E0104)
- Brethren + Brethren (collective, term; E0211, E0212)
- Center and circumference + Centers and circumferences (term; E0254, E0255)
- Enigma + Enigma (term, treatise; E0486, E0487)
- First principle + First principles (term; E0598, E0599)
- Gold + Gold (term; E0675, E1754)
- Initiated + Initiated (collective, term; E0857, E0859)
- Principle + Principles (term; E1395, E1399)
- Three principles + Three principles (term; E1759, E1760)
- Universal + Universals (term; E1841, E1866)
- Van Helmont + Van Helmonts (collective, person; E1874, E1875)
- White and Red + Whites and Reds (term; E1929, E1938)

## Folded in the worldbook (school or group name as the trigger)

Fine-grained lexicon entries that a roleplayer would only reach by the school, group or work name are combined into that name’s worldbook entry. The lexicon keeps them separate and links them with “See also”. Rules: `worldbook_fold` in the rules file.

| worldbook entry ← folded lexicon entries | keys | ctx |
|---|---|---|
| Adepts ← Adepts; Experimental adeptist; French adept; Modern adept; More modern class of adepts; Mysterious adeptest; No less experienced adept; No less subtle than experienced adept | adeptist, adeptists, Adept, adepts, adeptest |  |
| Agrippa ← Disciple of Cornelius Agrippa | Agrippa |  |
| Alchemists ← Alchemists and Greek physicians; Ancient physiologists and alchemists; Modern Alchemists; Old Alchemists | Alchemist, Alchemists, older masters |  |
| Animal Magnetism ← Writers on Animal Magnetism | Animal Magnetism |  |
| Aquarium Sapientum ← Author of the Aquarium Sapientum | Water Stone, Aquarium Sapientum, Aquarium Sepientum, pious author of the Aquarium |  |
| Author of the Rosarium ← Monk in his Rosary | Rosarium, Rosary, Rosar |  |
| Book of Enoch ← Sage in Enoch | Enoch |  |
| Dr Dee ← Spirit to Dr Dee | Dee |  |
| Egyptians ← Egyptian relics | Egyptian, Egyptians |  |
| Ethnics ← Early Christians and the wisest Ethnics | Ethnics, Ethnic, early Christians |  |
| Greek fables ← Grecian fables; Heroes of the ordeal; Heroic fables; Labouring heroes | Greek fables, Grecian fables, Greek myth, Greek myths, Greek mythology, Greek fable, Midas, Cadmus, Deucalion, Bacchus, Hercules, Orpheus, Heroic fables, Labouring heroes, Perseus, Theseus, Ulysses, Jason |  |
| Greeks ← Greeks; Greeks and eastern sages | Greeks, Greek philosophy, Stoics, Pythagoreans, Platonists, Peripatetics |  |
| Hermeticists ← Hermetic luminaries; Hermetic philosophers | Hermeticist, Hermeticists, Hermetic luminaries, Hermetic philosophers |  |
| Kabalah ← Cabalistic; Cabalistic scriptures and schools of antique experience | Kabalah, Kabbalah, Kabala, Kabbala, Cabala, Cabbala, Cabbalah, Qabalah, Qabbalah, Kabbale, Kabalistic, Kabbalistic, Cabalistic, Cabbalistic, Qabalistic, schools of antique experience |  |
| Kabalists ← Hebrew Kabalists; Kabalistic commentators; Kabalistic Interpreter; Modern Kabalists | Kabalist, Kabalists, Kabbalist, Kabbalists, Cabalist, Cabalists, Cabbalist, Cabbalists, Qabalist, Qabalists, Rabbis |  |
| Lucerna Salis ← Author of the Lucerna Salis | Lucerna Salis, Lucerna Solis |  |
| Lumen de Lumine ← Author of the Lumen de Lumine | Lumen de Lumine |  |
| Masons ← Free masonry; Master mason | Mason, Masons, Freemason, Freemasons, Freemasonry, Masonry, Grand Architects |  |
| Mesmerism ← Pioneers of Mesmerism | mesmerist, mesmerists, mesmeric, Mesmerism, mesmerizing |  |
| Metaphysicians ← Metaphysicians; Modern metaphysicians | metaphysician, metaphysicians |  |
| Norton ← Authorities in Norton; Norton’s Master | Norton |  |
| Oracles ← Divine Oracle; Truth-telling Oracle | Oracles, oracle, Oracula Chaldaica, Zoroastri Oracula | NOT Amelius, Apollo |
| Orphic oracles, fragment and poet ← Orphic Fragment; Orphic poet | Orphic |  |
| Philosophers ← Famous Christian philosophers; Philosopher; Philosophers of tyme old; Renowned philosophers of various ages and nations | Philosophers, philosopher, olde Fathers |  |
| Platonists ← Greek and Alexandrian Platonists; Platonic Successor | Platonist, Platonists, Platonic |  |
| Plutarch ← Eudoxus in Plutarch | Plutarch |  |
| Poets ← Initiated poet; Poet; Poets and traditionalists; Wise poet | poet, poets |  |
| Pythagoras ← Biographer of Pythagoras | Pythagoras, Pythagorus |  |
| Pythagoreans ← Pythagoric precept | Pythagorean, Pythagoreans, Pythagoric |  |
| Rabbi Ben Jochai ← Ben Jochai | Ben Jochai, Rabbi |  |
| Rosicrucians ← Brethren of the Rosy Cross | Rosicrucian, Rosicrucians, Rosy Cross |  |
| Sphinx ← Sphinx’s fables | Sphinx |  |
| Tractatus Aureus ← Author of the Tractatus Aureus; Master | Tractatus Aureus, Golden Treatise, Tract. Aureus |  |
| Zohar ← Rabbi in Zohar | Zohar |  |

## Gated entries (need a context word)

Agent, The All, Ancients, Authorities, Being, Body, Center, The desirable, Earth, The experienced, Experiment, Expounders, Form, The Fourth, Identity, Image, Law, Life, Light, Material, Mathematician, Matter, Medium, Mind, Moderns, The Name, One, Oracle to Amelius, Ours, Patient, The Power, Principle + Principles, Reason, Red, Sense, Solution, Subject, The Thing, Union, Unit, Universal + Universals, Virtue, Will, The Wise, Word, Works

## Left out of the worldbook

Full list with reasons at the end of `worldbook_keys.md`. Counts:


None: the thin filter is off (`thin.enabled` = false), so every lexicon entry is in the worldbook (folded entries inside their target).

## Worth a look

- Casing is by the book’s majority per word, so some phrases look different from how they appear in one passage (*material Rites* → *Material rites*).
- Six entries with only long descriptive headwords got short keys by hand (`worldbook_overrides`), e.g. *Dry water of the sea of the wise* → “dry water”; *Unattributed sayings* → maxim, proverb, Latin verse, unattributed.
- “Revelation” fires both the Book of Revelation and the short term *Revelation* (Kirchringius); left as is, since more triggering was preferred.
- Entries that the book only cites for reference carry no text beyond “Cited for reference only.”; they are in the worldbook as asked, but add nothing when they fire.
