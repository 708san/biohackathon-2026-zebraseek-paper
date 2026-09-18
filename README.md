# ZebraSeek manuscript

**Working title:** ZebraSeek integrates complementary facial and clinical evidence for rare disease prioritization

An English working manuscript being developed toward a **Nature Genetics Article**, with the **BioHackrXiv** metadata and PDF-generation workflow retained. This is a working draft, not a submitted or peer-reviewed article.

## Before editing the manuscript

AI-assisted and human editors should use the repository management files in this order:

1. [AGENTS.md](AGENTS.md): editing rules and entry point for GPT/Codex-style editors.
2. [MANUSCRIPT_LOGIC.md](MANUSCRIPT_LOGIC.md): canonical scientific story, contribution boundaries, terminology and figure/table roles.
3. [EDITORIAL_CHECKLIST.md](EDITORIAL_CHECKLIST.md): unresolved experimental details, author questions, reproducibility tasks and submission metadata.

[SCIENTIFIC_RATIONALE.md](SCIENTIFIC_RATIONALE.md) and [DRAFT_NOTES.md](DRAFT_NOTES.md) retain earlier scientific and drafting history. When those older notes conflict with `MANUSCRIPT_LOGIC.md`, the latter takes precedence.

`paper/paper.md` is reserved for reader-facing manuscript prose. TODOs and editor instructions should not be added to it.

## Edit the draft

- [paper/paper.md](paper/paper.md): title, author metadata, abstract, manuscript text, tables and figure captions.
- [paper/paper.bib](paper/paper.bib): reference records.
- [paper/paper.pdf](paper/paper.pdf): generated BioHackrXiv preview; edit the Markdown source rather than this file.
- [paper/figures/](paper/figures/): manuscript figures and interface image.
- [paper/data/aggregate_results.json](paper/data/aggregate_results.json): aggregate values for the original 74-case evaluation.
- [paper/data/adaptive_candidate_depth_summary.csv](paper/data/adaptive_candidate_depth_summary.csv): aggregate candidate-acquisition results from the expanded BioHackathon analysis.

Naoya Yoshikuwa is the first author and Toyofumi Fujiwara is the last author. Other names and affiliation assignments follow the supplied English author list. Unresolved author and submission metadata are tracked in `EDITORIAL_CHECKLIST.md` rather than in the manuscript body.

## Manuscript format

The draft follows the [Nature Genetics Article structure](https://www.nature.com/ng/content): an unreferenced abstract of no more than 150 words, an introduction without a heading, Results, Discussion and Online Methods. Results and Methods have topical subheadings; Discussion has none. Data availability, Code availability, Acknowledgements, Author contributions, Competing interests and Additional information remain structurally present.

The current Results preserve the original ZebraSeek 74-case analysis and Figs. 1-6, then extend the study with the DBCLS BioHackathon 2026 candidate-acquisition analysis in Fig. 7 and Table 1. The generated PDF intentionally retains **BioHackrXiv typesetting and its bibliography style**. It is not a Nature Genetics production template.

Event metadata are set to DBCLS BioHackathon 2026 (`BH26JP`), Matsuyama, Japan, 2026. The automated PDF's standard publication/submission labels do not mean that a submission has occurred.

## Reproduce the figures

Using Python 3.12 in a virtual environment:

```sh
python -m pip install -r scripts/requirements-figures.txt
python scripts/make_figures.py
python scripts/make_concept_figure.py
```

The original scripts reproduce aggregate study summaries and do **not** run ZebraSeek, provide case-level data, or implement its diagnostic workflow. Fig. 7 and the expanded candidate-acquisition summary are maintained separately from the original 74-case aggregate figures.

## Generate a PDF

The [Generate PDF workflow](.github/workflows/gen_pdf.yaml) runs on pushes and pull requests targeting `main`, or manually from Actions. It uses the official `ghcr.io/biohackrxiv/bhxiv-gen-pdf:master` image and `gen-pdf paper`.

Download the `paper` artifact from the workflow run. On a push to `main`, the workflow also commits the generated `paper/paper.pdf`. The built-in `GITHUB_TOKEN` is sufficient; no custom secret is required. PDF generation does not submit the manuscript to BioHackrXiv.

## License and submission

The manuscript and new repository contributions are licensed under [CC BY 4.0](LICENSE), following the [BioHackrXiv recommendation](https://guide.biohackrxiv.org/about.html). The reused workflow/template structure was available under CC0; that existing dedication is unaffected. Licenses and access conditions for external datasets, software and literature remain with their respective providers.

Before submission, resolve the author- and data-supplied items in [EDITORIAL_CHECKLIST.md](EDITORIAL_CHECKLIST.md) and obtain all co-authors' approval, following the [BioHackrXiv submission guidelines](https://guide.biohackrxiv.org/submission_guidelines.html).
