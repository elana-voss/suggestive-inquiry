# Suggestive Inquiry: Summaries and Hermetic Lorebook

A structured digest of Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850), published as an mdBook, with a SillyTavern worldbook built from its lexicon. The book is the only source: quotations are verbatim with paragraph/footnote references, and nothing is added from outside knowledge.

Read the book online: <https://elana-voss.github.io/suggestive-inquiry/>

## Lorebook

[`lorebook/Atwood_Hermetic_Mystery.json`](https://raw.githubusercontent.com/elana-voss/suggestive-inquiry/main/lorebook/Atwood_Hermetic_Mystery.json) — built from the Master Lexicon: one entry per subject, with closely related lexicon entries combined (e.g. all the Kabalist voices under *Kabalists*). Download it and import it in SillyTavern under World Info, Import.

Keys are words and short phrases a roleplayer would actually type, in the common spellings (Kabbalah, Cabala, Qabalah …; sulphur/sulfur). Entries whose main word is an everyday word (will, mind, matter, light, life …) only trigger when a hermetic, religious or esoteric context word is also present; all others trigger on their keys alone. Recommended World Info settings: **Recursive Scan on, Max Recursion Steps 2–3**. If the terms rarely come up naturally in your chats, switching entries to Vectorized may give better results (requires embeddings under Data Bank / Vector Storage).

## How it was made

- `input/` — the book's text, split into chapters and footnotes; `chunks/` — the same, cut into referenced chunks.
- `prompts/` — instructions for the reading, synthesis, dictionary and checking agents; `prompts/rules_core.md` holds the binding rules.
- `scripts/` — chunking, bundling, verbatim quote checks, dictionary extraction/rendering, and worldbook generation.
- `work/` — the pipeline state, tracked because it is agent output that cannot be recomputed by script: chunk readings (`final/`, `readings/`), method syntheses (`method/`, `part_method/`), and the dictionary (`dict/`: merge decisions, entry packets, the 64 written and checked batches in `out/`), plus the files the scripts read (`context/`, `dict/*.json`) and the review reports (`review/`). Ignored: agent input bundles, archives, and script renders (`.gitignore` lists them).
- `PLAN.md` — the method; `RUNBOOK.md` — run notes.

Every chunk was read by one or two independent agents and reconciled; every synthesized page and dictionary batch was checked against its inputs by a separate checker agent and by a script that verifies each quotation verbatim against the source.

The repository alone regenerates the lexicon page and worldbook, byte for byte, from the checked dictionary batches in `work/dict/out/`; no agent run is needed. The other book pages in `src/` are the checked agent output itself. Editorial rules for headwords, merges and keys are in `scripts/lexicon_rules.json`:

```bash
python3 scripts/dict_render.py all      # work/dict/dictionary.json
python3 scripts/dict_clean.py           # src/22_Master_Lexicon_and_Concordance.md + work/dict/dictionary_v2.json
python3 scripts/dict_worldbook_v2.py    # lorebook/Atwood_Hermetic_Mystery.json
python3 scripts/dict_review_report.py   # work/review/REVIEW_REPORT.md (what changed since 285de1b)
```

The lexicon and worldbook as they were before the headword and key cleanup are in commit `285de1b`: `git checkout 285de1b -- src/22_Master_Lexicon_and_Concordance.md lorebook/Atwood_Hermetic_Mystery.json` (or `git show 285de1b:<path>` to look at one file).
