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
- Treat Fig. 7 and Table 1 as candidate-acquisition analyses, not end-to-end ZebraSeek performance.
- Keep `Recall@k`, candidate coverage, candidate availability, candidate retention, candidate acquisition and verification distinct as defined in `MANUSCRIPT_LOGIC.md`.
- Do not claim that top-30 coverage, the mathematical formulation, zero-shot LLM selection or the oracle reference is itself the main contribution or a completed adaptive solution.
- Do not equate mean candidate count with measured compute cost unless tokens, latency, API calls or monetary cost were actually measured.
- Preserve provenance/traceability claims separately from claims about factual correctness or citation fidelity.

## Updating the scientific story

If a new result materially changes the interpretation:

1. Update `MANUSCRIPT_LOGIC.md` first.
2. Update the relevant evidence/task status in `EDITORIAL_CHECKLIST.md`.
3. Then revise `paper/paper.md`.

Do not silently change the manuscript's central claim to fit a newly added experiment.
