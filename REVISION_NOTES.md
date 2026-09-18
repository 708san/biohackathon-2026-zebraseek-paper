# Revision notes

## 2026-09-18 — manuscript logic / editorial separation

The manuscript editing workflow was separated into three layers without changing the paper's section or figure order:

- `MANUSCRIPT_LOGIC.md`: canonical scientific story, claim boundaries, terminology and figure/table roles.
- `EDITORIAL_CHECKLIST.md`: unresolved experimental details, author questions, reproducibility work and submission metadata.
- `paper/paper.md`: reader-facing manuscript prose only.

`AGENTS.md` directs AI editors to read the logic and checklist before modifying the manuscript.

Visible TODO/editorial language was removed from `paper/paper.md`. The existing section order, Figures 1–7 and Table 1 were retained. Empty submission-metadata sections remain structurally present until author-approved statements are available.
