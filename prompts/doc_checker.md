# Document Checker — instructions

You independently check one synthesized document (a Part method synthesis, a Part page, the book page, the method statement, or a batch of dictionary entries) built from Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850). You did not write it. Your job is to make it trustworthy. The binding rules (the book is the only source; verbatim quotes with refs; voices; stated vs interpreted; translations) are at the top of your bundle.

## Inputs (all in your bundle)
- `RULES` — the binding rules.
- `TASK` — the instructions the writer followed.
- `INPUTS` — the material the writer was given. This is the authority: every claim must be traceable to it.
- `DOCUMENT` — the document to check.
- `QUOTE_REPORT` — automatic verbatim check of the document's quotes against the source (failed quotes listed, if any).

## Check for
1. **Outside knowledge** — any identification, date, title, gloss, historical or doctrinal claim not in the inputs. Most important. Remove it or rewrite to what the inputs say.
2. **Untraceable claims** — a statement the cited reference/inputs don't support; wrong refs. Fix or remove.
3. **Failed quotes** from `QUOTE_REPORT` — replace with the exact span as the inputs give it, or remove the quotation marks and paraphrase.
4. **Voice errors** — a cited authority's words presented as Atwood's position, or vice versa; Appendix (later layer) material not labelled as such.
5. **Overreach** — "stated" that is really interpreted; merged points stronger than their inputs; a reading chosen where the inputs record an open question.
6. **Material omissions** — distinct points, decoding keys (asserted identities) or tensions in the inputs that the document dropped although its task required them. Add them briefly.
7. **Task conformance** — required sections/structure/length roughly met.

Do not rewrite for style; don't remove supported content; keep within the task's length limit.

## Output
Overwrite the DOCUMENT path with the corrected version (or leave it unchanged if nothing needs fixing). Reply with only: the path and a compact list of changes grouped by the categories above (omit empty ones), or "no changes".
