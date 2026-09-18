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
- Treat Fig. 7 and Table 1 as analyses of candidate-list depth and downstream candidate count, not end-to-end ZebraSeek performance.
- Keep `Recall@k`, candidate coverage, candidate availability, candidate retention, candidate-list depth and verification distinct as defined in `MANUSCRIPT_LOGIC.md`.
- Do not equate mean candidate count with measured compute cost unless tokens, latency, API calls or monetary cost were actually measured.
- Keep source traceability claims separate from claims about factual correctness or citation fidelity.

## Citation placement

- Place each citation immediately after the specific factual statement or method description that it supports.
- Do not collect several references at the end of a sentence or paragraph when different clauses describe different studies.
- When multiple studies are listed, cite each study directly after its own description so the reader can see the claim-to-source correspondence.
- Repeating the same citation is preferable to leaving the supported claim ambiguous.

## Scientific positioning

- Begin the Introduction with the rare-disease diagnostic problem and diagnostic odyssey before introducing individual tools.
- Present prior multimodal work as evidence that combining modalities is valuable, not as evidence that ZebraSeek lacks novelty.
- Do not claim that multimodal rare-disease diagnosis or traceable reasoning is unique to ZebraSeek. DeepRare explicitly provides evidence-grounded, traceable reasoning.
- Position ZebraSeek around candidate-level modular integration: specialist tools produce disease candidates; their source identity is retained; LLM-based ranking and external-information verification operate on those candidates.
- The manuscript should communicate three design goals: **effectiveness**, **traceability**, and **efficiency**.
- Describe the current limitations clearly: heuristic top-five candidate input, inability to recover unseen candidates, non-comparable specialist scores, and downstream dependence on LLM reasoning/search cost.
- BioHackathon 2026 work is motivated by efficient candidate exploration and selection. Fixed-depth, zero-shot LLM and best-case retrospective conditions are baselines used to study that problem, not the objective by themselves.

## Plain-language rule

- Prefer wording that states what the method actually does over machine-learning jargon or manuscript-specific shorthand.
- Avoid terms such as `oracle`, `headroom`, `candidate burden`, `gating`, or `policy` when a clearer phrase is available.
- When a technical term is necessary, define it at first use in reader-facing language.
- Do not introduce a new abbreviation unless it is used repeatedly and improves readability.

## Required editing loop

Substantial manuscript revisions must use an iterative **plan → edit → whole-manuscript audit → revise** loop. Do not stop after a local paragraph edit.

### 1. Plan

Before writing, state internally:
- what scientific misunderstanding or narrative problem is being fixed;
- which sections need revision;
- which figures/results/claims must remain unchanged;
- which new factual claims require source verification.

If the scientific interpretation changes, update `MANUSCRIPT_LOGIC.md` before `paper/paper.md`.

### 2. Edit

Revise reader-facing prose. Move unresolved facts to `EDITORIAL_CHECKLIST.md` rather than inserting TODOs into the manuscript.

### 3. Whole-manuscript audit

Re-read at least Abstract, Introduction, Results headings/bridges, and Discussion as one argument. Check:

1. Does the rare-disease diagnostic problem naturally motivate ZebraSeek?
2. Is ZebraSeek's value clear as effectiveness + traceability + efficiency?
3. Is prior work represented fairly, without false `first` or `no previous work` claims?
4. Is the current architecture and its limitation understandable before the BioHackathon extension is introduced?
5. Does the BioHackathon section read as an investigation of efficient candidate exploration, rather than a contest among baselines?
6. Are original 74-case end-to-end results clearly separated from expanded candidate-coverage analyses?
7. Do Discussion claims match what Results actually show?
8. Is any editor-facing prose or unexplained jargon left in the manuscript?
9. Is every literature-derived factual claim followed immediately by the citation that supports it, without ambiguous citation bundles?

### 4. Revise and audit again

Fix the problems found in step 3 and repeat the whole-manuscript audit at least once. Preserve the current PDF structure unless the author approves a structural change.
