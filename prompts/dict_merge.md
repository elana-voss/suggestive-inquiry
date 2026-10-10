# Dictionary Merge — instructions

You plan the entries of the dictionary for Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850). A script has grouped the term and source records extracted from the book by exact headword. You decide which groups form one entry. You see headwords, variants and asserted equivalences only; writer agents later get the full records.

The binding rules (`RULES`) apply: the book is the only source. Don't use outside knowledge to decide identities — two names are one entry only if they are the same word (spelling, case, inflection, archaic form, Latin/English form of the same word, abbreviation) or the same person/work under a different spelling. Different names for one thing ("many names for one thing") stay **separate entries**, linked only where the input shows an asserted equivalence (`= … @ref`).

## Input (`MERGE_INPUT`)
- `TERM GROUPS`: `id | forms | records | asserted equivalences (with @ref)`. Forms are the headwords plus the readers' "variants"; some readers wrongly listed other names as variants — judge by the headword(s), not the variant list.
- `SOURCE GROUPS`: `id | name | live/total records | works`. Persons, works and anonymous voices cited. Reference-only records are already excluded from the live count.

## Task
1. Find groups that belong in one entry by the test above (e.g. `Philosopher's Stone` + `Philosophers' stone`; `Behmen` + `Boehme` only if both are the book's spellings for one author — a spelling question, not an identity claim). When unsure, keep separate. A term group and a source group can be merged when both name the same person or work.
2. Mark `kind` for every entry that is **not** the default. Defaults: a T group is a `term`; an S group is a `person`. Other kinds: `treatise` (a named work discussed in its own right, not merely cited), `collective` (anonymous or group voices: "the adept", "the Greeks", "the Rabbis", multi-name lists), `person` for a T group naming a person, `term` for an S group that is a concept.
3. A source group listing several persons at once: map it to the single-person groups it names (`split`).

Everything not mentioned stays a one-group entry of default kind. A script picks headwords and builds cross-references from the asserted equivalences, so don't output those.

## Output (compact — only the exceptions)
Write JSON to the OUTPUT path:
```
{"merge": [["T0001", "T0009"], ["S0031", "S0207", "T0412"]],
 "kind": {"S0009": "collective", "T0577": "person", "T0120": "treatise"},
 "split": {"S0400": ["S0012", "S0006"]}}
```
For a merged set, give `kind` under its first id.

Read the bundle once and write the result once. Reply with only the path and the counts (merge sets, kind overrides, splits).
