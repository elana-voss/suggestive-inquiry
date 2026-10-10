# Run procedure (orchestrator notes — for resuming after context compaction)

Container root: /mnt/user-data/outputs/atwood (mirror of project folder; commit back with device_commit_files to C:\Users\theco\ai\software\atwood\...).
Inputs staged: /mnt/user-data/uploads/atwood/chunks/<id>.md and /mnt/user-data/uploads/atwood/work/context/<id>.md (all 81).

## Stage 1 — chunks (state = files)
- Single reader (Parts I, II): readings/<id>.A.json -> scripts/qc_batch.py -> checker -> final/<id>.json
- Double (III.*, IV.*, APP_*): readings/<id>.A.json + <id>.B.json -> reconciler -> readings/<id>.R.json -> qc_batch -> checker -> final/<id>.json
- NOTE: final/III.1_02.json and final/IV.3_01.json are OLD pilot outputs (old rules) — must be redone like the others.
- Reader: opus/high. Reconciler: opus/high. Checker: opus/medium. Prompts in prompts/.
- After checker: python3 scripts/render_chunk.py final/<id>.json final/<id>.md; commit final/*.json+md to device.
- Done when every id in chunks/index.json has a final made under current rules.

## Stage 2+ — see PLAN.md (chapters, method per chapter -> book method (fable/max), parts, book, dictionary (fable/max merge), worldbook by script).
File map: I.1->01, I.2->02, I.3->03, PartI->04, II.1->05, II.2->06, II.3->07, II.4->08, PartII->09, III.1->10, III.2->11, III.3->12, III.4->13, PartIII->14, IV.1->15, IV.2->16, IV.3->17, IV.4->18, PartIV->19, Book->20, APP->21, Lexicon->22, Method->23 (new: 23_The_Method_in_Plain_Terms.md).

## Session 2026-10-10 — state and how to resume
Agent-input method: scripts/bundle.py builds ONE bundle per agent (work/bundles/, regenerable, not committed) = prompts/rules_core.md (binding rules extracted from chunk_reader.md) + task prompt + all inputs. Agent prompt: short; "Read the bundle (allow_large; continue with offset if cut off), read nothing else, one Write". Inlining file contents in agent prompts would cost more (orchestrator output tokens) than one read.
Staging: tar needed dirs on device -> device_stage_files -> extract to /mnt/user-data/outputs/atwood AND chunks to /mnt/user-data/uploads/atwood/chunks (quote_check_doc.py path).

DONE (written; checker NOT yet run). Quote check: APP 3 not found, 14 1 not found, rest 0 — checker must fix these:
- work/part_method/{I,II,III,IV,APP}.md — Fable high. 8–10k words each (over 7k target; agents kept all distinct points/keys).
- src/04, 09, 14, 19 Part synthesis pages — Opus medium, ~1.4k words each.
NEXT:
1. Checker (prompts/doc_checker.md, Opus medium) on each of the 9 files above. Bundle: RULES + TASK (part_method.md / part_writer.md) + INPUTS (same as writer) + DOCUMENT + QUOTE_REPORT (python3 scripts/quote_check_doc.py FILE).
2. src/23_The_Method_in_Plain_Terms.md — Fable max, from the 5 part_method files (prompt to write: prompts/method_statement.md). Then quote check + checker.
3. src/20 book synthesis — Opus medium, from 04/09/14/19 + 21 (Appendix labelled later layer); prompt prompts/book_writer.md. Quote check + checker.
4. Dictionary: script extracts terms (2,234) + sources (1,606) from work/final/*.json -> exact-match grouping -> Fable max merge (clusters; equivalences only where text asserts) -> per-entry packets -> Opus writer agents in batches of 20–30 entries, JSON out -> quote check + checker per batch -> script renders src/22.
5. Worldbook by script from dictionary JSON (one concept/entry, 5–10 keys, separate person/treatise entries; keep existing SillyTavern format: entries{uid,key,keysecondary,comment,content,...}).
6. Update src/SUMMARY.md (add 23), commit everything to device.

## Token rules (from 2026-10-10; models, efforts, checks and step order unchanged)
- Every agent prompt must say: read the bundle once, write the result once; no rewrite/compression passes, no self-verification of quotes (quote_check_doc.py + checker do that).
- Length targets are guides, not reasons to rewrite: method syntheses may run to ~10k words.
- Dictionary: filter "reference only" sources by script before any agent; merge agent gets headwords/variants/asserted equivalences only; each writer gets only its batch's packets.

## Session 2026-10-10 (2) — state
DONE + checked + committed: work/part_method/{I,II,III,IV,APP}.md; src/04,09,14,19; src/20 (book synthesis, new prompt prompts/book_writer.md); src/23 (method statement, Fable max, ~16k words; prompt prompts/method_statement.md). All quote checks 0 not found.
Dictionary (step 4) IN PROGRESS: scripts/dict_extract.py (groups by exact headword; variant-chaining over-merged, so not used) -> work/dict/groups.json + merge_input.md (1,449 term groups, 843 source groups, 172 reference-only sources filtered). prompts/dict_merge.md = merge agent outputs exceptions only (merge sets, kind overrides, splits); first full-list attempt hit the 64k output cap and failed — do not ask for a full entry list.
NEXT: run merge (Fable max) on bundle RULES+dict_merge.md+merge_input.md -> work/dict/merge.json; then packets -> writer batches -> quote check + checker -> render src/22; worldbook; SUMMARY.md.
If the merge agent fails again (output cap), do not retry Fable: use the PLAN.md fallback (Opus, high), same prompt.

## Session 2026-10-10 (3) — state
Merge DONE (Fable max, exceptions-only worked): work/dict/merge.json (185 merge sets, 323 kind overrides, 24 splits).
scripts/dict_packets.py -> work/dict/entries.json (1,964 entries; 44 reference-only, script-rendered) + work/dict/packets/B001..B064.md (<=30 entries each).
Writer: prompts/dict_writer.md, Opus high, bundle = RULES + TASK + PACKETS (work/bundles/dw_Bnnn.md) -> work/dict/out/Bnnn.json {id:{forms,summary,body}}.
Check: python3 scripts/dict_render.py check Bnnn (validates, writes out/Bnnn.md) -> quote_check_doc.py out/Bnnn.md -> doc_checker (Opus medium) on the JSON, bundle RULES+TASK(dict_writer)+INPUTS(packet)+DOCUMENT(json)+QUOTE_REPORT.
Render: python3 scripts/dict_render.py all -> src/22 + work/dict/dictionary.json (worldbook input).
Progress is tracked by files: out/Bnnn.json exists = written; out/Bnnn.checked marker = checker done.
Status 2026-10-11: writers B001–B032 done + validated (on device, work/dict/out). B033–B064 not written. No checkers run yet.
Resume: stage work/bundles/_dict_stage.tgz (chunks, scripts, prompts, groups.json) + work/dict/{merge.json,entries.json,packets/,out/}; extract to /mnt/user-data/outputs/atwood (chunks also to /mnt/user-data/uploads/atwood/chunks); rebuild bundles for B033–B064: python3 scripts/bundle.py work/bundles/dw_$b.md RULES=prompts/rules_core.md TASK=prompts/dict_writer.md PACKETS=work/dict/packets/$b.md.
Writer agents ~85k tokens each. Max 8 in parallel (a 24-wide wave hit the session limit). Sync out/*.json to device after every wave (commit to a NEW tgz name; same-name commit did not overwrite).

## Session 2026-10-11 — state
Writers B001–B064 ALL done + validated (device work/dict/out). Checkers: running now in waves of 8 (bundle work/bundles/dc_Bnnn.md; checker fixes JSON via targeted Edits, not full rewrite). Marker out/Bnnn.checked = done.
Sync after each wave: new tgz name (_cN.tgz) -> commit -> tar xzf --overwrite on device (plain tar fails: deletion not permitted).

DONE 2026-10-11: all 64 batches written + checked (quote check 0 not found). src/22 rendered (1,964 entries; dict_render.py all — keep *.pre.json OUT of work/dict/out, its glob picks them up). work/dict/dictionary.json.
Worldbook: scripts/dict_worldbook.py -> lorebook/Atwood_Hermetic_Mystery.json (1,920 entries; 44 reference-only skipped; keys = headword + forms as found in the text, refs stripped). Most entries have 1–3 keys: the text gives few forms; not padded with other concepts' names.
SUMMARY.md: 23 added. Pipeline complete.
