# ZebraSeek manuscript

**Working title:** ZebraSeek integrates complementary facial and clinical evidence for rare disease prioritization

An English working manuscript being developed toward a **Nature Genetics Article**, with the **BioHackrXiv** metadata and PDF-generation workflow retained. This is a working draft, not a submitted or peer-reviewed article.

## Edit the draft

- [paper/paper.md](paper/paper.md): title, author metadata, the 146-word abstract in YAML, manuscript text and figure captions.
- [paper/paper.bib](paper/paper.bib): 14 reference records checked against primary sources.
- [paper/paper.pdf](paper/paper.pdf): generated BioHackrXiv preview; edit the Markdown source rather than this file.
- [SCIENTIFIC_RATIONALE.md](SCIENTIFIC_RATIONALE.md): scientific positioning, related-work comparison and prioritized validation questions (Japanese).
- [DRAFT_NOTES.md](DRAFT_NOTES.md): evidence provenance, assumptions and prioritized author TODOs (Japanese).
- [paper/figures/](paper/figures/): five scientific figures in PNG/editable SVG formats and one unaltered application screenshot.
- [paper/data/aggregate_results.json](paper/data/aggregate_results.json): aggregate values transcribed from the supplied research materials, with provenance and reconstructed counts explicitly identified.

Naoya Yoshikuwa is the first author and Toyofumi Fujiwara is the last author. Other names and affiliation assignments follow the supplied English author list; corresponding authorship and contribution roles remain to be confirmed.

## Manuscript format

The draft follows the [Nature Genetics Article structure](https://www.nature.com/ng/content): an unreferenced abstract of no more than 150 words, an introduction without a heading, Results, Discussion and Online Methods. The main text is below the 4,000-word limit and includes six figures. Results and Methods have topical subheadings; Discussion has none. Data availability, Code availability, acknowledgements, author contributions and competing interests are included.

The generated PDF intentionally retains **BioHackrXiv typesetting and its bibliography style**. It is not a Nature Genetics production template. Figure captions are kept with the figures for BioHackrXiv readability; final journal submission formatting can be adjusted later. Event metadata are still TODOs. The automated PDF's standard publication/submission labels do not mean that a submission has occurred.

## Reproduce the figures

Using Python 3.12 in a virtual environment:

```sh
python -m pip install -r scripts/requirements-figures.txt
python scripts/make_figures.py
python scripts/make_concept_figure.py
```

The original script checks aggregate totals, component overlaps and consistency of percentages before regenerating the original four PNG/SVG figure pairs (now manuscript Figs. 2 and 4–6). It reproduces the supplied study summaries; it does **not** run ZebraSeek, provide case-level data, or implement its diagnostic workflow.

The separate concept script regenerates Fig. 1 without changing the empirical figures. Fig. 3 is an unaltered input-form screenshot; its provenance is recorded in `paper/data/source_provenance.json`. The 12 September revision preserves all 74-case results and the original figure files.

## Generate a PDF

The [Generate PDF workflow](.github/workflows/gen_pdf.yaml) runs on pushes and pull requests targeting `main`, or manually from Actions. It uses the official `ghcr.io/biohackrxiv/bhxiv-gen-pdf:master` image and `gen-pdf paper`.

Download the `paper` artifact from the workflow run. On a push to `main`, the workflow also commits the generated `paper/paper.pdf`. The built-in `GITHUB_TOKEN` is sufficient; no custom secret is required. PDF generation does not submit the manuscript to BioHackrXiv.

## License and submission

The manuscript and new repository contributions are licensed under [CC BY 4.0](LICENSE), following the [BioHackrXiv recommendation](https://guide.biohackrxiv.org/about.html). The reused workflow/template structure was available under CC0; that existing dedication is unaffected. Licenses and access conditions for external datasets, software and literature remain with their respective providers.

Replace the remaining TODOs and obtain all co-authors' approval before submission, following the [BioHackrXiv submission guidelines](https://guide.biohackrxiv.org/submission_guidelines.html).
