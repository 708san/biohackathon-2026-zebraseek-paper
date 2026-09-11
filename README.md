# TODO: Manuscript title

An independent manuscript repository for publication in [BioHackrXiv](https://biohackrxiv.org/).

## Write the manuscript

- Manuscript source: [paper/paper.md](paper/paper.md).
- References: [paper/paper.bib](paper/paper.bib). Add BibTeX entries and cite them with `[@citation-key]`.
- Replace all TODO metadata and text before submission. Author names and affiliations are placeholders, not confirmed authorship. Add real ORCID/ROR identifiers only when known.
- Confirm the event metadata against the [BioHackrXiv meeting list](https://index.biohackrxiv.org/meetings).
- Add new figures under `paper/` and link them relative to `paper/paper.md`.

## Generate a PDF

The [Generate PDF workflow](.github/workflows/gen_pdf.yaml) runs on pushes and pull requests targeting `main`, and can also be run manually from Actions.
It uses the official `ghcr.io/biohackrxiv/bhxiv-gen-pdf:master` image and `gen-pdf paper`.
Download the `paper` artifact from the workflow run. On a push to `main`, the workflow also commits the newly generated `paper/paper.pdf`.
The workflow uses the built-in `GITHUB_TOKEN`; no custom secret is required. Organization Actions policies must allow the referenced actions, container image, and workflow write permissions.
PDF generation is a preview step; it does not submit the manuscript to BioHackrXiv.

## License

The new manuscript and repository contributions are licensed under [CC BY 4.0](LICENSE), following the [BioHackrXiv recommendation](https://guide.biohackrxiv.org/about.html).
The reused workflow/template structure was available under CC0; that existing dedication is unaffected.
Before submission, replace every placeholder and obtain all co-authors' approval as required by the [submission guidelines](https://guide.biohackrxiv.org/submission_guidelines.html).
