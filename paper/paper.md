---
title: "ZebraSeek integrates complementary facial and clinical evidence for rare disease prioritization"
title_short: "ZebraSeek for rare disease prioritization"
article_type: "Article"
tags:
  - rare disease
  - differential diagnosis
  - facial phenotyping
  - Human Phenotype Ontology
  - large language models
authors:
  - name: Naoya Yoshikuwa
    affiliation: 1
  - name: Hirokazu Chiba
    affiliation: 3
  - name: Teppei Okazaki
    affiliation: 2
  - name: Jae-Moon Shin
    affiliation: 3
  - name: Eisuke Dohi
    affiliation: 5
  - name: Hiroyuki Mishima
    affiliation: 6
  - name: Atsuko Yamaguchi
    affiliation: 2
  - name: Tzung-Chien Hsieh
    affiliation: 7
  - name: Orion Buske
    affiliation: 4
  - name: Susumu Goto
    affiliation: "1,3"
  - name: Toyofumi Fujiwara
    affiliation: 3
affiliations:
  - name: "Department of Computational Biology and Medical Sciences, Graduate School of Frontier Sciences, The University of Tokyo"
    index: 1
  - name: "Information and Data Sciences, Graduate School of Information and Data Sciences, Tokyo City University"
    index: 2
  - name: "Database Division for Life Science (DBCLS), BioData Science Initiative (BSI), National Institute of Genetics (NIG), Research Organization of Information and Systems (ROIS)"
    index: 3
  - name: "PhenoTips, Toronto, Ontario, Canada"
    index: 4
  - name: "National Institute of Neuroscience, National Center of Neurology and Psychiatry (NCNP)"
    index: 5
  - name: "Atomic Bomb Disease Institute, Nagasaki University"
    index: 6
  - name: "Institute for Genomic Statistics and Bioinformatics, University Hospital Bonn"
    index: 7
date: "18 September 2026"
bibliography: paper.bib
event: "BH26JP"
biohackathon_name: "DBCLS BioHackathon 2026"
biohackathon_url: "https://2026.biohackathon.org/"
biohackathon_location: "Matsuyama, Japan, 2026"
group: "ZebraSeek"
git_url: "https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper"
authors_short: 'Naoya Yoshikuwa \emph{et al.}'
abstract: |
  Rare disease differentials must reconcile evidence that is unevenly represented across clinical descriptions, facial phenotypes and disease resources. Combining tools can broaden candidate retrieval but can also discard useful diagnoses. We developed ZebraSeek to integrate phenotype matching, semantic retrieval, facial analysis and large language model predictions into a ranked differential with explanatory text. In 74 literature-derived cases spanning 19 diseases, ZebraSeek retrieved the recorded diagnosis at rank one in 50 cases (67.6%) and within five ranks in 59 (79.7%), compared with 63.5% and 71.6% for PubCaseFinder. Eleven cases were recovered beyond PubCaseFinder's top-five coverage, while five of its correct candidates were lost. Of 15 ZebraSeek failures, eight lacked a correct component candidate and seven lost one during integration. These observations distinguish complementary candidate retrieval from candidate retention, providing a framework for testing when multimodal integration improves disease prioritization. Causal modality contributions and clinical utility remain unestablished.
---

<!-- Working draft, not a submitted or peer-reviewed article. See ../DRAFT_NOTES.md. -->
<!-- Introduction intentionally has no heading, following Nature Genetics Article guidance. -->

A differential diagnosis is a bridge between a patient's clinical presentation and the genetic investigations needed to explain it. For rare disorders, this bridge depends on recognizing a disease despite incomplete or unevenly documented phenotypes. Structured clinical findings, facial morphology and published disease descriptions represent different aspects of the same presentation. A diagnosis may therefore be suggested by one source while receiving little support from another. Bringing these sources together is useful only if the resulting shortlist preserves informative hypotheses and remains small enough to examine.

The Human Phenotype Ontology (HPO) standardizes clinical abnormalities [@HPO2024]. PubCaseFinder links such findings to disease-associated phenotypes in case reports [@PubCaseFinder2018], whereas GestaltMatcher retrieves similar facial phenotypes [@GestaltMatcher2022]. Combining these forms of information is already an established direction. PhenoScore combines facial analysis and HPO-based similarity to quantify phenotypic variation, and GestaltMML combines facial images with clinical text and demographic information [@PhenoScore2023; @GestaltMML2026]. PEDIA integrates facial and clinical evidence with exome analysis for gene prioritization, while SHEPHERD uses a knowledge graph for several phenotype-driven diagnostic tasks [@PEDIA2019; @SHEPHERD2025]. Thus, neither multimodality nor the use of external phenotype knowledge alone defines the contribution of a new system.

Large language models (LLMs) add a way to coordinate retrieval and compare candidate explanations. DeepRare, RareAgents and MEDDxAgent demonstrate different forms of tool-supported or iterative diagnostic reasoning [@DeepRare2026; @RareAgents2026; @MEDDxAgent2025]. Yet a stronger final ranking cannot be assumed from access to more tools. A recent systematic review found substantial variation across LLM evaluations and highlighted benchmark composition and potential information leakage as barriers to interpreting reported accuracy [@LLMReview2026]. These concerns make comparisons within a common evaluation setting, with explicit diagnostic targets and input information, particularly valuable.

We focus on a specific question: can integration recover diagnoses available through complementary phenotype evidence while retaining useful candidates that receive support from only one component? ZebraSeek approaches this question at the candidate level. Specialized tools convert clinical and facial information into disease proposals, which an LLM ranks and checks against external medical information. This allows facial evidence to enter the differential through a specialist matcher rather than requiring the LLM to interpret the photograph directly. The evaluated task uses phenotypic information without genomic variants as inputs; it does not assess variant pathogenicity or discover new disease genes.

Here we describe this workflow and its interface, and examine 74 literature-derived cases with matched phenopackets and facial images. We retain the component comparisons and evaluate two distinct properties: availability of the recorded diagnosis among retrieved candidates and its retention in the final top-five differential. This distinction makes gains and losses visible even when aggregate recall improves. The study provides an initial empirical basis for evaluating candidate integration, rather than establishing the superiority of multimodal or LLM-based reasoning in general.

# Results

## Complementary evidence creates both opportunities and a selection problem

The organizing principle of ZebraSeek is that a useful disease hypothesis need not be supported by every component (Fig. 1). Phenotype matching, facial similarity, semantic retrieval and direct LLM prediction provide different routes to the same disease vocabulary. Their outputs are candidate proposals, not independent measurements of diagnostic probability: tools can share phenotype annotations, literature and underlying knowledge. Agreement can support review, but the number of agreeing tools is not a calibrated measure of certainty.

Integration must address two questions in sequence. First, is the recorded diagnosis available in any component's candidate list? Second, if available, does it remain in the final differential? A correct candidate absent from one tool can expand that tool's coverage, whereas discarding a candidate supplied by another can offset this benefit. Figure 1 presents this conceptual distinction; the following analyses examine it using the existing component and final-output summaries. It does not introduce a new ranking algorithm or an additional experiment.

![**From complementary evidence to a reviewable differential.** Different representations can retrieve shared or source-specific disease hypotheses. The conceptual distinction is between candidate availability and retention during shortlist formation. A source-specific candidate may be useful even without cross-tool agreement. Candidate-level integration connects specialist retrieval with LLM ranking and external-information checks; correctness and the value of each stage require separate evaluation. This schematic illustrates the study question without assigning probabilities or claiming independent evidence across tools.](figures/concept_candidate_retention.png){width=100%}

## ZebraSeek integrates candidate proposals from facial and clinical evidence

In the evaluated workflow, ZebraSeek uses a facial image, HPO-encoded clinical findings and recorded sex (Fig. 2). The facial image is processed by GestaltMatcher, while HPO information is supplied to PubCaseFinder and SemanticSearch. The latter retrieves disease candidates by embedding-based similarity to disease descriptions derived from Mondo. A direct LLM component receives HPO information and sex and separately proposes a differential diagnosis. The implementation described in the source materials uses GPT-5.2 for direct predictions and the subsequent integration stages.

Each component returns up to five candidate diseases, yielding at most 20 candidate entries before accounting for overlap. The integration stage compares candidates while retaining information about their source ranks and scores. A verification stage consults external information, including PubMed, and relates candidate diseases to the patient's findings. Explicitly recorded negative findings can be considered during this step. ZebraSeek then returns five ranked candidates with explanatory text. The exact prompts, model snapshots and retrieval settings remain to be documented in the reproducible implementation.

![**ZebraSeek workflow.** Facial images are analysed by GestaltMatcher; HPO terms are supplied to PubCaseFinder and SemanticSearch; and HPO terms together with recorded sex are supplied to the direct LLM component. Each component provides up to five candidates. LLM-based ranking and literature-based verification produce a final top-five list with explanatory text. The diagram summarizes the workflow reported in the thesis abstract and presentation; it does not imply that the contribution of each stage has been isolated experimentally.](figures/figure1_workflow.png){width=100%}

## A web interface connects clinical input to staged candidate review

The ZebraSeek input interface supports observed and excluded findings, recorded sex, age of onset, facial-image upload and import from Phenopackets (Fig. 3). It brings structured clinical descriptions and facial evidence into one query workflow. These controls describe the interface available at the time of manuscript preparation; they should not be interpreted as evidence that every field was populated or used in the 74-case benchmark.

The supplied results view separates tool output, tentative candidates, a stage labelled validation, and final disease candidates. Component tables display disease identifiers, ranks and similarity scores alongside the final differential. This organization allows users to inspect component proposals as well as the integrated result. The validation label denotes the system's external-information checking stage, not independent clinical validation. The screenshots document interface functionality; they do not establish explanation accuracy, usability or an effect on clinical decisions.

![**ZebraSeek clinical input interface.** The unpopulated input form shows Phenopacket import, observed and excluded findings, sex, age of onset and facial-image upload. The screenshot was supplied on 12 September 2026 and is reproduced without alteration. Interface fields and notices describe the displayed application; they are not a record of benchmark inputs or an independent audit of data handling. No patient photograph or populated patient record is shown.](figures/zebraseek_input_interface.png){width=90%}

## Higher observed recall in a benchmark of 74 cases

The evaluation set comprised 74 cases spanning 19 diseases, obtained by matching Phenopacket Store v0.1.25 records to facial images in GestaltMatcher Database. The recorded diagnosis served as the reference label; the stated system inputs were facial images, HPO findings and sex. The available results summarize whether this diagnosis appeared among the first one to five predictions from each method (Recall\@1 to Recall\@5).

ZebraSeek had the highest observed recall at every reported cutoff (Fig. 4). Recall\@1 was 67.6% (50/74), compared with 63.5% (47/74) for PubCaseFinder, 31.1% (23/74) for GestaltMatcher and 18.9% (14/74) for both SemanticSearch and the direct LLM. At rank five, ZebraSeek reached 79.7% (59/74), compared with 71.6% (53/74), 50.0% (37/74), 35.1% (26/74) and 33.8% (25/74) for PubCaseFinder, GestaltMatcher, the direct LLM and SemanticSearch, respectively. Relative to PubCaseFinder, the observed differences were 4.1 percentage points at rank one and 8.1 percentage points at rank five, corresponding to net increases of three and six correctly prioritized cases.

These are descriptive comparisons within the reported benchmark. Intermediate-cutoff counts were reconstructed from the plotted one-decimal percentages and the common denominator of 74, and remain to be checked against case-level outputs. No confidence intervals, repeat-run variability or significance claims are inferred from these summaries. The comparison also reflects different input modalities across methods; it is not a controlled estimate of the effect of LLM integration alone.

![**Top-k diagnostic recall across five methods.** Top-k recall is the percentage of 74 cases whose recorded diagnosis appears within the first k predictions. Values are transcribed from the supplied performance chart. The same denominator is used at all cutoffs; this figure reports aggregate results without uncertainty estimates. Displayed results have not been regenerated by running the diagnostic tools.](figures/figure2_recall.png){width=100%}

## Component tools retrieve complementary correct candidates

Among the 59 cases correctly prioritized by ZebraSeek at rank five, the recorded diagnosis was also present in PubCaseFinder's top five for 48 cases, in SemanticSearch's for 25, in the direct LLM's for 26 and in GestaltMatcher's for 35 (Fig. 5). Only 13 of these cases were recovered by all four component tools. The largest exclusive patterns after this four-tool overlap were PubCaseFinder alone (10 cases) and GestaltMatcher alone (seven cases). A further three cases had the recorded diagnosis only in the SemanticSearch candidate list.

ZebraSeek therefore recovered 11 cases in which PubCaseFinder did not retrieve the diagnosis within its top five. Conversely, five cases recovered by PubCaseFinder were missed by ZebraSeek. The difference between these two discordant groups accounts for the net gain of six cases over PubCaseFinder at rank five. This distinction matters: the final list extended coverage beyond the strongest individual component while also losing some of that component's correct candidates.

The observed overlaps support complementary candidate availability, but do not identify the causal contribution of any individual modality. For example, the seven successful cases with GestaltMatcher-only correct candidates motivate a matched evaluation without facial analysis; they do not substitute for that ablation. The integration process may also change its ranking when any component is removed.

![**Component overlap among the 59 ZebraSeek successes at rank five.** Each column represents an exclusive combination of component tools whose top-five lists contained the recorded diagnosis. Connected filled circles identify the tools in each combination; grey circles indicate absence. Bar heights show case counts. The totals at left are conditional on ZebraSeek success and are not the full-cohort recalls of the component tools.](figures/figure3_overlap.png){width=100%}

## Candidate coverage and retention account for different failures

ZebraSeek did not include the recorded diagnosis in its top five for 15 cases (Fig. 6). In eight, none of the four component top-five lists contained the diagnosis. These cases expose a coverage limitation in the candidate lists supplied to integration. In the remaining seven, the diagnosis was available from a component but absent from the final list: five had a correct PubCaseFinder-only candidate and two had a correct GestaltMatcher-only candidate. All seven losses therefore involved a diagnosis retrieved by only one component. The aggregate results cannot locate the loss within normalization, initial ranking, verification or final selection. Together with the source-specific candidates retained among ZebraSeek successes, these observations motivate testing when integration preserves useful disagreements; they do not establish a systematic preference for consensus.

Across the reported overlap patterns, at least one component contained the correct diagnosis in 66 of 74 cases (89.2%). This union is a descriptive measure of candidate coverage with up to 20 entries per case, not a top-five method or a validated performance target. Its difference from ZebraSeek's 59 successful cases identifies seven potentially recoverable diagnoses already present in the inputs.

The presentation further reports that the 15 failures were confined to two of the 19 disease labels: cardiac, facial, and digital anomalies (OMIM:618164; 10 cases) and a label abbreviated as neurodevelopmental disorder with coarse facies (OMIM:618505; five cases). Disease-specific denominators and label normalization require confirmation. This concentration makes case-level averages insufficient for assessing performance across diseases and motivates disease-stratified evaluation.

![**Correct-candidate availability among the 15 ZebraSeek failures at rank five.** Eight cases had no correct candidate in any component's top-five list. Five had a correct candidate only in PubCaseFinder and two only in GestaltMatcher. The latter seven cases distinguish failure to retain an available diagnosis from absence of that diagnosis in all initial lists.](figures/figure4_failures.png){width=85%}

# Discussion

ZebraSeek connects facial and clinical phenotype tools to an LLM workflow for producing a compact disease differential. In the reported 74-case evaluation, its final list had higher observed recall than each individual component. The scientific interpretation rests on the paired outcomes: 11 diagnoses were recovered beyond PubCaseFinder's top-five coverage, while five diagnoses retrieved by PubCaseFinder were lost. The improvement is therefore a balance between complementary candidate availability and imperfect retention, not an unconditional benefit from adding tools.

This distinction matters for clinical genetics because phenotypic evidence is heterogeneous even within a disease. A facial pattern and a structured phenotype description need not point to the same hypotheses with the same strength. PhenoScore and GestaltMML already establish important precedents for integrating these representations [@PhenoScore2023; @GestaltMML2026]. ZebraSeek instead combines candidate proposals from existing specialist tools with LLM-based ranking and external-information checks. Its proposed value is a way to assemble and examine a differential across these tools, not a new facial representation or the first multimodal approach. The present results motivate, but do not yet demonstrate, that this candidate-level approach offers an advantage over established multimodal models or simpler integration rules.

The seven successful cases with GestaltMatcher-only correct candidates show that facial matching can supply a correct proposal absent from the other component lists. They do not establish that the photograph caused the final success: removing a tool may alter retrieval, ranking and verification in other ways. Similarly, all seven failures with an available correct candidate involved a single supporting component, but this pattern does not identify an LLM bias against uncommon or weakly documented diseases. Matched runs without facial analysis, without LLM integration and with simple rank aggregation are needed to separate the contributions of input information, candidate diversity and the integration procedure. Component and final lists must be scored under the same disease-normalization and candidate-budget rules.

The review by Nguyen and colleagues further cautions against treating results on different benchmarks as a common league table [@LLMReview2026]. Disease composition and information availability can shape observed performance; disease prevalence is only a proxy for the latter. Whether ZebraSeek helps when textual descriptions are sparse or facial presentations are atypical is a testable hypothesis, not a finding of this study. The reported concentration of failures in two disease labels makes this distinction especially relevant. Disease-specific denominators, phenotype completeness and source coverage must be established before attributing these failures to biological rarity, inadequate knowledge or the integration mechanism. Comparisons with DeepRare or other agent systems require matched cases, inputs, resources and scoring rather than their published headline accuracies.

The interface provides a practical setting for inspecting inputs, intermediate proposals and final candidates. This can support examination of discordant tool outputs, but visibility alone does not establish that explanations are faithful or clinically useful. In particular, the external-information checking stage must be evaluated for factual support, citation fidelity and whether it changes the differential appropriately. A plausible narrative cannot substitute for evidence that a candidate fits the patient. Accessibility and reusable software can enable independent testing; they are implementation strengths whose scientific value depends on documented releases, permissions and reproducible evaluations. Public access to a manuscript or an application should not be conflated with release of its complete implementation.

Several limitations constrain the present interpretation. The benchmark is retrospective, small and selected for availability of both phenopackets and facial images. Its 19 diseases and their unequal representation may influence case-level recall. The supplied summaries do not permit assessment by ancestry, age, sex, severity or phenotype completeness, nor do they quantify repeated-run variability. No controlled ablation or independent clinical evaluation is reported. The union of component candidates allows up to 20 entries per case and is a coverage measure, not a competing top-five predictor or a demonstrated performance ceiling for the full workflow.

Literature-derived cases also require a careful audit of information overlap. Source publications, related patients or query images may be represented in phenotype resources, facial reference galleries, model training corpora or verification-time retrieval. Removing explicit diagnoses from the query is necessary but insufficient to rule out these routes. Neither the current aggregate analysis nor the broader literature resolves this uncertainty for ZebraSeek. Independent cases and transparent provenance are needed to test generalization; expert evaluation is additionally required to assess explanations and any effect on diagnostic decisions. The present findings do not establish molecular diagnostic yield, clinical benefit or equitable performance.

The resulting research question is more precise than whether adding modalities improves accuracy: under what conditions can a system turn complementary phenotype evidence into a compact differential without discarding informative hypotheses? ZebraSeek provides an implementation and an initial benchmark in which both recovery and loss can be examined. Establishing when those gains are reproducible, and which evidence supports them, is the next step toward useful phenotype-driven diagnostic assistance.

# Online Methods

## Study design and case selection

The reported study retrospectively evaluated 74 literature-derived cases covering 19 diseases. Phenotypic descriptions, sex and recorded diagnoses were obtained from Phenopacket Store v0.1.25, a corpus built using the GA4GH Phenopacket representation [@PhenopacketStore2025]. Cases were linked to facial images in GestaltMatcher Database, a resource for facial phenotyping [@GMDB2024]. The presentation describes matching records corresponding to the same individual across the two resources.

**TODO:** Document the case-matching procedure, source publication and case identifiers, inclusion and exclusion criteria, number of images per individual, handling of duplicate or related individuals, selection dates and the GestaltMatcher Database release. Confirm all 19 disease labels and counts. The database-wide counts shown in the presentation are not treated as the study's screening denominator.

## Input preparation and reference diagnoses

ZebraSeek used facial images, HPO findings and recorded sex. The reference diagnosis was used for evaluation rather than intentionally supplied as a model input. HPO provides standardized identifiers for phenotypic abnormalities [@HPO2024]. The workflow can consider explicitly recorded negative findings; the extent to which these were present in the benchmark is not documented.

**TODO:** Specify HPO version, query serialization, present/absent finding handling, image preprocessing, sex encoding and any missing-value rules. Document removal of diagnosis-bearing fields, causal gene or variant annotations, file names, captions and other identifying labels from inputs, including information present in source phenopackets but outside the intended query fields. Report the reference-diagnosis ascertainment procedure, disease-identifier mapping, synonym handling and criteria for accepting a predicted diagnosis as correct, including disease families and subtypes.

## Interface documentation

Interface features were described from three screenshots supplied on 12 September 2026. The unpopulated input form is reproduced in Fig. 3. The results screenshot was used to identify visible workflow stages and table fields; its example disease ranking was not used as a benchmark observation. The landing page shows a login requirement. Interface text alone does not verify service access conditions, software licensing, backend data retention or conformity between the displayed application and the evaluated version.

**TODO:** Record the application URL and version, link it to the evaluated software commit, and confirm which interface fields entered each benchmark run. Document service access, storage and external processing arrangements from the implementation and applicable policies.

## Candidate generation

PubCaseFinder generated candidates from HPO findings using phenotype-based disease matching [@PubCaseFinder2018]. GestaltMatcher generated candidates from facial images [@GestaltMatcher2022]. SemanticSearch compared phenotype information with embeddings of disease descriptions obtained from Mondo, which integrates disease terminology across resources [@Mondo2026]. The direct LLM component, labelled GPT-5.2 in the source materials, generated candidates from HPO findings and sex in a zero-shot setting. Each component supplied up to five candidates.

**TODO:** Record component versions and endpoints, disease reference databases, the Mondo release and fields indexed, embedding model and version, query construction, similarity function and ranking rules. Specify the GestaltMatcher model and gallery, and exclusion of query individuals or duplicate images from its reference set. Provide the exact LLM identifier, evaluation dates, prompts, sampling parameters, reasoning settings where applicable and retry policy.

## Candidate integration and external verification

The integration stage received up to 20 candidate entries with source ranks and scores and used an LLM to rank candidate diseases. A verification stage related candidates to the available phenotype information and consulted external medical information, including PubMed. The reported workflow then generated a final top-five ranking and explanatory text. GPT-5.2 is shown for the ranking, verification and final-output stages in the supplied workflow diagram.

**TODO:** Archive the actual prompts and orchestration code. Define candidate deduplication and normalization, whether verification may introduce new diseases, the number of candidates verified, stopping rules, search queries, retrieval sources and dates, text truncation, error handling and the format of intermediate decisions. Confirm whether all stages used the same model snapshot and settings. Do not replace these missing details with an assumed implementation.

## Evaluation metrics and descriptive analysis

For each method, top-k recall was the fraction of evaluated cases for which the recorded diagnosis occurred among the first k predictions, with k ranging from one to five. All reported percentages used a denominator of 74. A case contributed at most one success at each cutoff. This draft transcribes the aggregate performance values and exclusive component-overlap counts supplied with the study; it does not report a new execution of ZebraSeek or its comparators.

For plotting, each one-decimal percentage was converted to the integer count consistent with the denominator of 74. These reconstructed counts are explicitly labelled in the accompanying aggregate-data file. The overlap summaries distinguish successful ZebraSeek cases from its failures and use the component top-five lists. Candidate availability denotes presence of the recorded diagnosis in at least one component top-five list; retention denotes its continued presence in the final top-five list when initially available. These terms describe evaluation outcomes and do not imply that the diagnosis was known to the ranking procedure. Candidate-union coverage was computed by summing the reported successful-case patterns and the seven failures with an available correct component candidate. This quantity allows more than five candidate entries per case and is not directly comparable as a ranked top-five predictor.

**TODO:** Validate the transcribed aggregates against case-level predictions and specify tie handling, failures to return results, repeated-run design and any prompt or model selection performed on this cohort. Prespecify paired comparisons and uncertainty estimates that account for repeated cases within diseases. No formal significance tests or uncertainty estimates are asserted in this draft. Add controlled modality and integration ablations, disease-stratified performance, and an evaluation of evidence quality when these analyses have been completed.

## Ethics and data governance

The benchmark is described as a secondary analysis of literature-derived cases and associated facial images. **TODO:** Provide the applicable ethics review or exemption determination, institution and reference number; the consent and access conditions for image reuse; and the data-processing arrangements for external services. Public availability of a case description does not establish unrestricted permission to redistribute identifiable facial images. This manuscript includes aggregate figures, schematics and an unpopulated interface screenshot, without patient photographs or populated patient records.

# Data availability

The aggregate values used for this draft's figures are provided in `paper/data/aggregate_results.json` in the manuscript repository. They were transcribed from the supplied study summaries and are not case-level source data. Phenopacket Store is described in the cited resource paper [@PhenopacketStore2025]. Facial image access is governed by GestaltMatcher Database. **TODO:** Add the exact dataset release links, a permitted case-matching manifest, case-level prediction and scoring records, and the relevant access conditions. The manuscript repository does not redistribute the underlying patient images.

# Code availability

The manuscript source and scripts used to reproduce its aggregate figures are available at [the manuscript repository](https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper). **TODO:** Add the ZebraSeek software repository, version or commit, license, environment specification, prompts and evaluation scripts. The figure-generation script reproduces the presentation summaries; it is not the ZebraSeek diagnostic implementation.

# Acknowledgements

**TODO:** Add funding sources, grant identifiers and acknowledgements approved by the authors. The English draft, subsequent editorial revision and figure code were prepared with assistance from OpenAI Codex using the supplied research materials and verified literature. The authors' scientific verification and final approval remain pending.

# Author contributions

**TODO:** Confirm the contributions of Naoya Yoshikuwa, Hirokazu Chiba, Teppei Okazaki, Jae-Moon Shin, Eisuke Dohi, Hiroyuki Mishima, Atsuko Yamaguchi, Tzung-Chien Hsieh, Orion Buske, Susumu Goto and Toyofumi Fujiwara using an agreed contribution statement. Author order in this working draft places Naoya Yoshikuwa first and Toyofumi Fujiwara last; contribution roles and corresponding authorship have not been inferred from order.

# Competing interests

**TODO:** Obtain declarations from every author and replace this placeholder with the agreed statement. No absence-of-conflict declaration is assumed.

# Additional information

**TODO:** Designate the corresponding author or authors and confirm contact details, final institutional addresses and ORCID identifiers. BioHackrXiv event metadata also remain to be completed before submission.

# References
