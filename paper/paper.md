---
title: "ZebraSeek integrates facial and phenotypic evidence for rare disease prioritization"
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
  - name: Teppei Okazaki
    affiliation: 2
  - name: Jae-Moon Shin
    affiliation: 3
  - name: Orion Buske
    affiliation: 4
  - name: Eisuke Dohi
    affiliation: 5
  - name: Hiroyuki Mishima
    affiliation: 6
  - name: Atsuko Yamaguchi
    affiliation: 2
  - name: Tzung-Chien Hsieh
    affiliation: 7
  - name: Hirokazu Chiba
    affiliation: 3
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
# Date of this working draft; confirm the submission date later.
date: "11 September 2026"
bibliography: paper.bib
event: "TODO: Event identifier"
biohackathon_name: "TODO: Event name"
biohackathon_url: "https://example.org/TODO-event"
biohackathon_location: "TODO: City, country, year"
group: "ZebraSeek"
git_url: "https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper"
authors_short: 'Naoya Yoshikuwa \emph{et al.}'
abstract: |
  Rare disease prioritization requires evidence distributed across clinical phenotypes, facial features and medical literature. We developed ZebraSeek, a workflow that combines phenotype matching, semantic retrieval, facial analysis and large language model predictions, followed by candidate ranking and literature-based verification. In a retrospective benchmark of 74 literature-derived cases spanning 19 diseases, ZebraSeek ranked the recorded diagnosis first in 50 cases (67.6%) and within its top five in 59 (79.7%). The strongest individual comparator, PubCaseFinder, achieved 63.5% and 71.6%, respectively. ZebraSeek recovered 11 cases missed by PubCaseFinder at rank five but missed five cases recovered by PubCaseFinder. Among 15 ZebraSeek failures, eight lacked the diagnosis in every component's top-five list, whereas seven lost an available candidate during integration. These results support further evaluation of multimodal candidate integration while identifying candidate coverage and retention as distinct limitations. Independent validation and modality ablation remain necessary.
---

<!-- Working draft, not a submitted or peer-reviewed article. See ../DRAFT_NOTES.md. -->
<!-- Introduction intentionally has no heading, following Nature Genetics Article guidance. -->

Rare disease diagnosis often requires clinicians to reconcile overlapping phenotypes with evidence scattered across disease resources and individual case reports. Computational prioritization can make this information easier to examine, but the relevant evidence is expressed in different forms. Structured clinical findings support explicit phenotype comparisons, whereas facial morphology can provide a pattern that is difficult to capture fully in a list of terms. A useful diagnostic assistant must bring these forms of evidence into a manageable differential diagnosis while retaining enough context for clinical review.

The Human Phenotype Ontology (HPO) provides a common vocabulary for describing clinical abnormalities [@HPO2024]. PubCaseFinder uses phenotype information and disease associations derived from case reports to support differential diagnosis [@PubCaseFinder2018]. Facial analysis offers a complementary approach: GestaltMatcher represents facial phenotypes in a space that enables similarity-based matching between individuals with rare disorders [@GestaltMatcher2022]. These approaches provide different routes to candidate retrieval. Their usefulness in a combined workflow depends both on whether they retrieve the recorded diagnosis and on whether subsequent integration preserves it.

Large language models (LLMs) provide an interface for comparing heterogeneous candidate lists and relating them to clinical descriptions. Recent work on DeepRare illustrates how tool use and external knowledge retrieval can support rare disease prioritization [@DeepRare2026]. Nevertheless, access to multiple tools does not itself establish that a final ranking is better than its inputs. A system can recover a diagnosis absent from one component, but it can also discard a diagnosis that another component has already retrieved. Evaluating these outcomes separately is necessary to understand what integration contributes.

Here we present ZebraSeek, which combines HPO-based phenotype matching, semantic search over disease descriptions, facial phenotype analysis and direct LLM predictions. A subsequent LLM workflow ranks candidates and checks them against external medical information. We evaluated ZebraSeek using 74 literature-derived cases with matched phenopackets and facial images. In addition to comparing top-ranked diagnostic recall, we examined the overlap of correct candidates across component tools and separated failures of candidate coverage from failures to retain available diagnoses. This initial study assesses retrospective disease prioritization; it does not assess variant interpretation or establish clinical diagnostic utility.

# Results

## An integrated workflow for facial and phenotypic evidence

ZebraSeek accepts a facial image, HPO-encoded clinical findings and recorded sex (Fig. 1). The facial image is processed by GestaltMatcher, while HPO information is supplied to PubCaseFinder and SemanticSearch. The latter retrieves disease candidates by embedding-based similarity to disease descriptions derived from Mondo. A direct LLM component receives HPO information and sex and independently proposes a differential diagnosis. The implementation described in the source materials uses GPT-5.2 for direct predictions and the subsequent integration stages.

Each component returns up to five candidate diseases, yielding at most 20 candidate entries before accounting for overlap. The integration stage compares candidates while retaining information about their source ranks and scores. A verification stage consults external information, including PubMed, and relates candidate diseases to the patient's findings. Explicitly recorded negative findings can be considered during this step. ZebraSeek then returns five ranked candidates with explanatory text. The exact prompts, model snapshots and retrieval settings remain to be documented in the reproducible implementation.

![**ZebraSeek workflow.** Facial images are analysed by GestaltMatcher; HPO terms are supplied to PubCaseFinder and SemanticSearch; and HPO terms together with recorded sex are supplied to the direct LLM component. Each component provides up to five candidates. LLM-based ranking and literature-based verification produce a final top-five list with explanatory text. The diagram summarizes the workflow reported in the thesis abstract and presentation; it does not imply that the contribution of each stage has been isolated experimentally.](figures/figure1_workflow.png){width=100%}

## Higher observed recall in a benchmark of 74 cases

The evaluation set comprised 74 cases spanning 19 diseases, obtained by matching Phenopacket Store v0.1.25 records to facial images in GestaltMatcher Database. The recorded diagnosis served as the reference label; the stated system inputs were facial images, HPO findings and sex. The available results summarize whether this diagnosis appeared among the first one to five predictions from each method (Recall\@1 to Recall\@5).

ZebraSeek had the highest observed recall at every reported cutoff (Fig. 2). Recall\@1 was 67.6% (50/74), compared with 63.5% (47/74) for PubCaseFinder, 31.1% (23/74) for GestaltMatcher and 18.9% (14/74) for both SemanticSearch and the direct LLM. At rank five, ZebraSeek reached 79.7% (59/74), compared with 71.6% (53/74), 50.0% (37/74), 35.1% (26/74) and 33.8% (25/74) for PubCaseFinder, GestaltMatcher, the direct LLM and SemanticSearch, respectively. Relative to PubCaseFinder, the observed differences were 4.1 percentage points at rank one and 8.1 percentage points at rank five, corresponding to net increases of three and six correctly prioritized cases.

These are descriptive comparisons within the reported benchmark. Intermediate-cutoff counts were reconstructed from the plotted one-decimal percentages and the common denominator of 74, and remain to be checked against case-level outputs. No confidence intervals, repeat-run variability or significance claims are inferred from these summaries. The comparison also reflects different input modalities across methods; it is not a controlled estimate of the effect of LLM integration alone.

![**Top-k diagnostic recall across five methods.** Top-k recall is the percentage of 74 cases whose recorded diagnosis appears within the first k predictions. Values are transcribed from the supplied performance chart. The same denominator is used at all cutoffs; this figure reports aggregate results without uncertainty estimates. Displayed results have not been regenerated by running the diagnostic tools.](figures/figure2_recall.png){width=100%}

## Component tools retrieve complementary correct candidates

Among the 59 cases correctly prioritized by ZebraSeek at rank five, the recorded diagnosis was also present in PubCaseFinder's top five for 48 cases, in SemanticSearch's for 25, in the direct LLM's for 26 and in GestaltMatcher's for 35 (Fig. 3). Only 13 of these cases were recovered by all four component tools. The largest exclusive patterns after this four-tool overlap were PubCaseFinder alone (10 cases) and GestaltMatcher alone (seven cases). A further three cases had the recorded diagnosis only in the SemanticSearch candidate list.

ZebraSeek therefore recovered 11 cases in which PubCaseFinder did not retrieve the diagnosis within its top five. Conversely, five cases recovered by PubCaseFinder were missed by ZebraSeek. The difference between these two discordant groups accounts for the net gain of six cases over PubCaseFinder at rank five. This distinction matters: the final list extended coverage beyond the strongest individual component while also losing some of that component's correct candidates.

The observed overlaps support complementary candidate availability, but do not identify the causal contribution of any individual modality. For example, the seven successful cases with GestaltMatcher-only correct candidates motivate a matched evaluation without facial analysis; they do not substitute for that ablation. The integration process may also change its ranking when any component is removed.

![**Component overlap among the 59 ZebraSeek successes at rank five.** Each column represents an exclusive combination of component tools whose top-five lists contained the recorded diagnosis. Connected filled circles identify the tools in each combination; grey circles indicate absence. Bar heights show case counts. The totals at left are conditional on ZebraSeek success and are not the full-cohort recalls of the component tools.](figures/figure3_overlap.png){width=100%}

## Candidate coverage and retention account for different failures

ZebraSeek did not include the recorded diagnosis in its top five for 15 cases (Fig. 4). In eight, none of the four component top-five lists contained the diagnosis. These cases expose a coverage limitation in the candidate lists supplied to integration. In the remaining seven, the diagnosis was available from a component but absent from the final list: five had a correct PubCaseFinder-only candidate and two had a correct GestaltMatcher-only candidate. The aggregate results cannot locate the loss within initial ranking, verification or final selection, but they show that improving candidate retrieval alone would not address every failure.

Across the reported overlap patterns, at least one component contained the correct diagnosis in 66 of 74 cases (89.2%). This union is a descriptive measure of candidate coverage with up to 20 entries per case, not a top-five method or a validated performance target. Its difference from ZebraSeek's 59 successful cases identifies seven potentially recoverable diagnoses already present in the inputs.

The presentation further reports that the 15 failures were confined to two of the 19 disease labels: cardiac, facial, and digital anomalies (OMIM:618164; 10 cases) and a label abbreviated as neurodevelopmental disorder with coarse facies (OMIM:618505; five cases). Disease-specific denominators and label normalization require confirmation. This concentration makes case-level averages insufficient for assessing performance across diseases and motivates disease-stratified evaluation.

![**Correct-candidate availability among the 15 ZebraSeek failures at rank five.** Eight cases had no correct candidate in any component's top-five list. Five had a correct candidate only in PubCaseFinder and two only in GestaltMatcher. The latter seven cases distinguish failure to retain an available diagnosis from absence of that diagnosis in all initial lists.](figures/figure4_failures.png){width=85%}

# Discussion

ZebraSeek provides an initial example of integrating facial and structured phenotypic evidence with LLM-based disease prioritization. In the reported 74-case evaluation, the final rankings had higher observed recall than each of four individual components. The comparison with PubCaseFinder captures both the benefit and the cost of integration: 11 cases were recovered beyond that component's top-five coverage, while five of its correct candidates were lost. The resulting improvement is therefore a balance between complementary retrieval and imperfect retention.

Facial phenotype matching is a plausible source of additional candidates when structured phenotype retrieval is incomplete. However, this study does not establish the independent effect of facial information. The tools differed in their inputs, knowledge resources and ranking procedures, and no matched modality ablation was supplied. Evaluations that remove GestaltMatcher while holding all other settings fixed, as well as comparisons against simple score or rank aggregation, are needed to determine which parts of the workflow account for the observed differences. DeepRare provides relevant context for tool-supported reasoning, but its published benchmark conditions differ from those used here [@DeepRare2026]. The present results do not support a numerical ranking of ZebraSeek against DeepRare.

The failure analysis suggests two concrete development priorities. Cases without a correct initial candidate may benefit from broader retrieval, improved disease descriptions or better phenotype representations. Cases with an available but discarded diagnosis instead require an audit of candidate normalization, integration prompts and verification decisions. External retrieval should be evaluated for whether it supports accurate, case-specific discrimination rather than merely producing plausible text. The current evaluation measures the presence of a recorded diagnosis in a ranked list; it does not measure factual accuracy, citation fidelity or clinical usefulness of the explanations.

Several properties of the benchmark limit interpretation. It is a small, retrospective collection selected for the availability of both phenopackets and facial images. Nineteen diseases cannot represent the breadth of rare disease practice, and multiple cases from the same disease may make aggregate recall sensitive to disease composition. The concentration of failures in two labels further emphasizes this issue. Age, ancestry, sex distribution, severity and phenotype completeness were not available in the supplied summaries, so performance across these strata remains unresolved.

The use of literature-derived cases also requires explicit assessment of information overlap. Cases or their source publications may be represented in phenotype resources, facial reference galleries, LLM training data or material retrieved during verification. Supplying the recorded diagnosis only to the evaluator is necessary but does not by itself exclude these routes of leakage. An audit of case matching, gallery exclusions and retrieval provenance, followed by an independent evaluation, is needed before interpreting the results as generalization to unseen patients. The present study does not establish gains in diagnostic yield, time to diagnosis or patient outcomes.

Together, the results motivate a multimodal prioritization workflow in which specialized tools supply candidates and an integration stage makes their evidence easier to review. They also show why coverage and retention should be reported separately. A larger, independently validated study with prespecified evaluation rules, modality ablations and expert review of explanations will be needed to establish the conditions under which ZebraSeek is useful in clinical genetics.

# Online Methods

## Study design and case selection

The reported study retrospectively evaluated 74 literature-derived cases covering 19 diseases. Phenotypic descriptions, sex and recorded diagnoses were obtained from Phenopacket Store v0.1.25, a corpus built using the GA4GH Phenopacket representation [@PhenopacketStore2025]. Cases were linked to facial images in GestaltMatcher Database, a resource for facial phenotyping [@GMDB2024]. The presentation describes matching records corresponding to the same individual across the two resources.

**TODO:** Document the case-matching procedure, source publication and case identifiers, inclusion and exclusion criteria, number of images per individual, handling of duplicate or related individuals, selection dates and the GestaltMatcher Database release. Confirm all 19 disease labels and counts. The database-wide counts shown in the presentation are not treated as the study's screening denominator.

## Input preparation and reference diagnoses

ZebraSeek used facial images, HPO findings and recorded sex. The reference diagnosis was used for evaluation rather than intentionally supplied as a model input. HPO provides standardized identifiers for phenotypic abnormalities [@HPO2024]. The workflow can consider explicitly recorded negative findings; the extent to which these were present in the benchmark is not documented.

**TODO:** Specify HPO version, query serialization, present/absent finding handling, image preprocessing, sex encoding and any missing-value rules. Document removal of diagnosis-bearing fields, file names, captions and other identifying labels from inputs. Report the reference-diagnosis ascertainment procedure, disease-identifier mapping, synonym handling and criteria for accepting a predicted diagnosis as correct, including disease families and subtypes.

## Candidate generation

PubCaseFinder generated candidates from HPO findings using phenotype-based disease matching [@PubCaseFinder2018]. GestaltMatcher generated candidates from facial images [@GestaltMatcher2022]. SemanticSearch compared phenotype information with embeddings of disease descriptions obtained from Mondo, which integrates disease terminology across resources [@Mondo2026]. The direct LLM component, labelled GPT-5.2 in the source materials, generated candidates from HPO findings and sex in a zero-shot setting. Each component supplied up to five candidates.

**TODO:** Record component versions and endpoints, disease reference databases, the Mondo release and fields indexed, embedding model and version, query construction, similarity function and ranking rules. Specify the GestaltMatcher model and gallery, and exclusion of query individuals or duplicate images from its reference set. Provide the exact LLM identifier, evaluation dates, prompts, sampling parameters, reasoning settings where applicable and retry policy.

## Candidate integration and external verification

The integration stage received up to 20 candidate entries with source ranks and scores and used an LLM to rank candidate diseases. A verification stage related candidates to the available phenotype information and consulted external medical information, including PubMed. The reported workflow then generated a final top-five ranking and explanatory text. GPT-5.2 is shown for the ranking, verification and final-output stages in the supplied workflow diagram.

**TODO:** Archive the actual prompts and orchestration code. Define candidate deduplication and normalization, whether verification may introduce new diseases, the number of candidates verified, stopping rules, search queries, retrieval sources and dates, text truncation, error handling and the format of intermediate decisions. Confirm whether all stages used the same model snapshot and settings. Do not replace these missing details with an assumed implementation.

## Evaluation metrics and descriptive analysis

For each method, top-k recall was the fraction of evaluated cases for which the recorded diagnosis occurred among the first k predictions, with k ranging from one to five. All reported percentages used a denominator of 74. A case contributed at most one success at each cutoff. The initial draft transcribes the aggregate performance values and exclusive component-overlap counts supplied with the study; it does not report a new execution of ZebraSeek or its comparators.

For plotting, each one-decimal percentage was converted to the integer count consistent with the denominator of 74. These reconstructed counts are explicitly labelled in the accompanying aggregate-data file. The overlap summaries distinguish successful ZebraSeek cases from its failures and use the component top-five lists. Candidate-union coverage was computed by summing the reported successful-case patterns and the seven failures with an available correct component candidate. This quantity allows more than five candidate entries per case and is not directly comparable as a ranked top-five predictor.

**TODO:** Validate the transcribed aggregates against case-level predictions and specify tie handling, failures to return results, repeated-run design and any prompt or model selection performed on this cohort. Prespecify paired comparisons and uncertainty estimates that account for repeated cases within diseases. No formal significance tests or uncertainty estimates are asserted in this draft. Add controlled modality and integration ablations, disease-stratified performance, and an evaluation of evidence quality when these analyses have been completed.

## Ethics and data governance

The benchmark is described as a secondary analysis of literature-derived cases and associated facial images. **TODO:** Provide the applicable ethics review or exemption determination, institution and reference number; the consent and access conditions for image reuse; and the data-processing arrangements for external services. Public availability of a case description does not establish unrestricted permission to redistribute identifiable facial images. This manuscript includes aggregate figures and a schematic, without patient photographs.

# Data availability

The aggregate values used for this draft's figures are provided in `paper/data/aggregate_results.json` in the manuscript repository. They were transcribed from the supplied study summaries and are not case-level source data. Phenopacket Store is described in the cited resource paper [@PhenopacketStore2025]. Facial image access is governed by GestaltMatcher Database. **TODO:** Add the exact dataset release links, a permitted case-matching manifest, case-level prediction and scoring records, and the relevant access conditions. The manuscript repository does not redistribute the underlying patient images.

# Code availability

The manuscript source and scripts used to reproduce its aggregate figures are available at [the manuscript repository](https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper). **TODO:** Add the ZebraSeek software repository, version or commit, license, environment specification, prompts and evaluation scripts. The figure-generation script reproduces the presentation summaries; it is not the ZebraSeek diagnostic implementation.

# Acknowledgements

**TODO:** Add funding sources, grant identifiers and acknowledgements approved by the authors. An initial English draft and plotting code were prepared with assistance from OpenAI Codex using the supplied research materials. The authors' scientific verification and final approval remain pending.

# Author contributions

**TODO:** Confirm the contributions of Naoya Yoshikuwa, Teppei Okazaki, Jae-Moon Shin, Orion Buske, Eisuke Dohi, Hiroyuki Mishima, Atsuko Yamaguchi, Tzung-Chien Hsieh, Hirokazu Chiba, Susumu Goto and Toyofumi Fujiwara using an agreed contribution statement. Author order in this working draft places Naoya Yoshikuwa first and Toyofumi Fujiwara last; contribution roles and corresponding authorship have not been inferred from order.

# Competing interests

**TODO:** Obtain declarations from every author and replace this placeholder with the agreed statement. No absence-of-conflict declaration is assumed.

# Additional information

**TODO:** Designate the corresponding author or authors and confirm contact details, final institutional addresses and ORCID identifiers. BioHackrXiv event metadata also remain to be completed before submission.

# References
