# Revision notes — 2026-09-19

Post-PDF audit revisions:

- clarified that the evaluation cases used for GestaltMatcher were excluded from its training data
- clarified that source case reports were not directly supplied as ZebraSeek query inputs, while prior exposure through public LLM training or indexed resources cannot be excluded
- changed the Abstract wording so five PubCaseFinder-positive cases are described as absent from the final ZebraSeek top five rather than assigning the loss to a specific integration substage
- changed Figure 7 x-axis labels from `Recall@k` to candidate depth (`Top k`)
- clarified that the GPT-5.2 image-based depth selector was an exploratory feasibility experiment distinct from the main ZebraSeek diagnostic path; future selector work is intended to use a local model
- replaced editorial/meta wording in the Introduction with manuscript-facing prose
- reframed PEDIA as addressing a different multimodal score-fusion problem rather than as a limited or inferior method
- removed empty Acknowledgements, Author contributions, Competing interests and Additional information headings; CC-BY licensing metadata remains in the document header

No benchmark values, table values, or reported coverage/recall values were changed.
