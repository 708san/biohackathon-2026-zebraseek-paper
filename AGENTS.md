# ZebraSeek manuscript editing instructions

Before editing `paper/paper.md`, read these files in this order:

1. `MANUSCRIPT_LOGIC.md` — canonical scientific story, contribution boundaries, terminology and figure roles.
2. `EDITORIAL_CHECKLIST.md` — unresolved facts, author questions, reproducibility tasks and submission metadata.
3. `SCIENTIFIC_RATIONALE.md` and `DRAFT_NOTES.md` — historical background only; when they conflict with `MANUSCRIPT_LOGIC.md`, the latter takes precedence.

## Manuscript hygiene

- `paper/paper.md` must contain reader-facing manuscript prose only.
- Do not insert TODOs, drafting notes, questions to authors, uncertainty about missing metadata, or instructions to future editors into `paper/paper.md`.
- Put unresolved items in `EDITORIAL_CHECKLIST.md` instead.
- Do not invent missing experimental details. Ask the author or leave the item in the checklist.
- Preserve the current PDF section order, Figures 1–7 and Table 1 unless the author explicitly approves a structural change.
- Preserve the original 74-case ZebraSeek story and Figs. 1–6 when incorporating hackathon results.
- Treat Fig. 7 and Table 1 as analyses of how many candidates are taken from each tool, not end-to-end ZebraSeek performance.
- Keep `Recall@k`, candidate coverage, candidate availability, candidate retention, candidate-list depth and verification distinct as defined in `MANUSCRIPT_LOGIC.md`.
- Do not claim that top-30 coverage, the mathematical formulation, zero-shot LLM selection or the best-case reference that uses the known diagnosis is itself the main contribution or a completed case-specific selection method.
- Do not equate mean candidate count with measured compute cost unless tokens, latency, API calls or monetary cost were actually measured.
- Keep source traceability claims separate from claims about factual correctness or citation fidelity.

## Plain-language rule

- Prefer wording that states what the method actually does over machine-learning jargon or manuscript-specific shorthand.
- Avoid terms such as `oracle`, `headroom`, `candidate burden`, `gating`, or `policy` when a clearer phrase is available.
- For example, write `best-case retrospective reference using the known diagnosis` instead of `oracle`, `potential reduction in candidate count` instead of `headroom`, and `number of candidates passed to later stages` instead of `candidate burden`.
- When a technical term is necessary, define it at first use in reader-facing language.
- Do not introduce a new abbreviation unless it is used repeatedly and improves readability.

## Updating the scientific story

If a new result materially changes the interpretation:

1. Update `MANUSCRIPT_LOGIC.md` first.
2. Update the relevant evidence/task status in `EDITORIAL_CHECKLIST.md`.
3. Then revise `paper/paper.md`.

Do not silently change the manuscript's central claim to fit a newly added experiment.
