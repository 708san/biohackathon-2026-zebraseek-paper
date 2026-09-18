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
# Date of this working draft; confirm the submission date later.
date: "18 September 2026"
bibliography: paper.bib
event: "TODO: Event identifier"
biohackathon_name: "TODO: Event name"
biohackathon_url: "https://example.org/TODO-event"
biohackathon_location: "TODO: City, country, year"
group: "ZebraSeek"
git_url: "https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper"
authors_short: 'Naoya Yoshikuwa \emph{et al.}'
abstract: |
  Rare disease differentials must reconcile evidence unevenly represented across clinical descriptions, facial phenotypes and disease resources. ZebraSeek integrates specialist phenotype and facial matching, semantic retrieval and large language model predictions into a traceable ranked differential with external-information checks. In 74 literature-derived cases spanning 19 diseases, ZebraSeek retrieved the recorded diagnosis at rank one in 50 cases (67.6%) and within five ranks in 59 (79.7%). Eleven cases were recovered beyond PubCaseFinder's top-five coverage, while five were lost during integration. During the 2026 hackathon, an expanded analysis of 368 patients, 462 images and 54 disorders showed that PubCaseFinder-GestaltMatcher union coverage rose from 77.5% at top five to 89.0% at top 30. We therefore formulate adaptive candidate-depth selection: preserve candidate coverage while reducing downstream verification burden. Preliminary zero-shot policies support this direction; clinical utility remains unestablished.
---

<!-- Working draft, not a submitted or peer-reviewed article. See ../DRAFT_NOTES.md. -->
<!-- Introduction intentionally has no heading, following Nature Genetics Article guidance. -->

A differential diagnosis is a bridge between a patient's clinical presentation and the genetic investigations needed to explain it. For rare disorders, this bridge depends on recognizing a disease despite incomplete or unevenly documented phenotypes. Structured clinical findings, facial morphology and published disease descriptions represent different aspects of the same presentation. A diagnosis may therefore be suggested by one source while receiving little support from another. Bringing these sources together is useful only if the resulting shortlist preserves informative hypotheses and remains small enough to examine.

The Human Phenotype Ontology (HPO) standardizes clinical abnormalities [@HPO2024]. PubCaseFinder links such findings to disease-associated phenotypes in case reports [@PubCaseFinder2018], whereas GestaltMatcher retrieves similar facial phenotypes [@GestaltMatcher2022]. Combining these forms of information is already an established direction. PhenoScore combines facial analysis and HPO-based similarity to quantify phenotypic variation, and GestaltMML combines facial images with clinical text and demographic information [@PhenoScore2023; @GestaltMML2026]. PEDIA integrates facial and clinical evidence with exome analysis for gene prioritization, while SHEPHERD uses a knowledge graph for several phenotype-driven diagnostic tasks [@PEDIA2019; @SHEPHERD2025]. Thus, neither multimodality nor the use of external phenotype knowledge alone defines the contribution of a new system.

Large language models (LLMs) add a way to coordinate retrieval and compare candidate explanations. DeepRare, RareAgents and MEDDxAgent demonstrate different forms of tool-supported or iterative diagnostic reasoning [@DeepRare2026; @RareAgents2026; @MEDDxAgent2025]. Yet a stronger final ranking cannot be assumed from access to more tools. A recent systematic review found substantial variation across LLM evaluations and highlighted benchmark composition and potential information leakage as barriers to interpreting reported accuracy [@LLMReview2026]. These concerns make comparisons within a common evaluation setting, with explicit diagnostic targets and input information, particularly valuable.

We focus first on a specific question: can integration recover diagnoses available through complementary phenotype evidence while retaining useful candidates that receive support from only one component? ZebraSeek approaches this question at the candidate level. Specialized tools convert clinical and facial information into disease proposals, which an LLM ranks and checks against external medical information. This allows facial evidence to enter the differential through a specialist matcher rather than requiring the LLM to interpret the photograph directly. The evaluated task uses phenotypic information without genomic variants as inputs; it does not assess variant pathogenicity or discover new disease genes.

The initial design also exposes a second problem. If only the first few candidates from each specialist tool enter the integration stage, a correct diagnosis ranked more deeply cannot be recovered by later reasoning. Expanding every ranking can increase candidate coverage, but detailed evidence retrieval and LLM-based verification scale with the number of downstream candidates and can increase token use and latency. During the 2026 hackathon we therefore studied candidate depth as a separate decision variable: for each input, how deeply should each candidate generator be explored to preserve coverage while limiting the downstream verification burden? We additionally strengthened structured outputs so that candidate decisions remain tied to provenance, including source URLs where available.

Here we retain the original 74-case benchmark and its component analyses, then add an expanded candidate-coverage analysis using Phenopacket Store v0.1.27 linked to facial images. The first analysis asks whether complementary candidates are recovered and retained; the second asks how much candidate depth is needed before expensive integration and verification. Together they frame ZebraSeek as a traceable multimodal integration workflow whose effectiveness depends on both candidate coverage and efficient candidate selection.

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

## Expanded retrieval depth reveals additional candidate coverage

The original workflow supplied only shallow component lists to downstream integration. To examine how much correct-diagnosis coverage remained at deeper ranks, we performed a hackathon analysis using Phenopacket Store v0.1.27 linked to facial images, comprising 368 patients, 462 images and 54 recorded disorders. This is an image-level candidate-coverage analysis rather than an end-to-end ZebraSeek benchmark; multiple images can correspond to the same patient, and patient-level generalization therefore requires a separate analysis.

PubCaseFinder covered 73.4% of the 462 image-level instances at rank five, 78.1% at rank ten and 83.5% at rank 30. GestaltMatcher covered 30.3%, 34.6% and 45.0%, respectively. The deduplicated union of PubCaseFinder and GestaltMatcher increased from 77.5% at rank five to 82.7% at rank ten and 89.0% at rank 30 (Fig. 7). These results show that a substantial fraction of correct candidates lies beyond the shallow lists used by the initial ZebraSeek integration design.

![**Candidate coverage increases with retrieval depth in the expanded analysis.** Exact-OMIM inclusion was evaluated for 462 facial-image instances linked to 368 patients across 54 disorders. Bars show candidate coverage for PubCaseFinder (PCF), GestaltMatcher (GM) and their deduplicated union at increasing retrieval depths. The PCF-GM union increased from 77.5% at top five to 89.0% at top 30. This figure evaluates candidate-generation coverage and should not be interpreted as end-to-end ZebraSeek diagnostic performance.](figures/expanded_candidate_depth_recall.svg){width=100%}

## Adaptive candidate-depth selection exposes a coverage--cost trade-off

Expanding both component rankings to rank 30 substantially increases the number of candidates that must be normalized, checked against external information and reranked. We therefore formulated candidate depth as an input-specific selection problem: for each instance, choose how deeply to accept candidates from each generator while preserving a target level of correct-diagnosis coverage and reducing the deduplicated candidate set sent to downstream processing.

Fixed-depth conditions illustrate the trade-off (Table 1). PCF@30 reached 83.55% coverage with 30 candidates on average. The union PCF@30 ∪ GM@30 reached the maximum observed coverage of 88.96% but required 57.57 unique candidates on average. In contrast, an oracle-style ideal combination, which uses the known reference diagnosis to choose the minimum sufficient depth for each instance, reached the same 88.96% coverage with 2.66 candidates on average. This oracle is not an executable diagnostic method; it estimates the headroom available if input-specific depth selection could identify where each correct candidate is likely to occur.

Two preliminary zero-shot LLM depth-selection conditions reduced the candidate burden relative to exhaustive PCF@30 ∪ GM@30. An input-only policy achieved 84.38% coverage with 19.28 candidates on average, whereas a policy that also received tool results achieved 84.60% with 18.18 candidates on average. These values were available for 461 image-level instances; the missing-instance handling remains to be documented. The small difference between the two zero-shot conditions should not be interpreted as a demonstrated advantage without repeated runs and paired uncertainty estimates. Instead, the comparison provides a baseline for subsequent policies that explicitly optimize the coverage--candidate-count frontier.

**Table 1 | Candidate coverage and average deduplicated candidate count in the expanded analysis.**

| Selection condition | Correct-diagnosis coverage | Mean unique candidates | n |
| --- | ---: | ---: | ---: |
| PCF@5 | 0.7338 | 5.00 | 462 |
| PCF@10 | 0.7814 | 10.00 | 462 |
| PCF@30 | 0.8355 | 30.00 | 462 |
| PCF@5 ∪ GM@5 | 0.7749 | 9.66 | 462 |
| PCF@10 ∪ GM@5 | 0.8160 | 14.58 | 462 |
| PCF@30 ∪ GM@30 | 0.8896 | 57.57 | 462 |
| zero-shot LLM, input only | 0.8438 | 19.28 | 461 |
| zero-shot LLM, input + tool results | 0.8460 | 18.18 | 461 |
| Ideal combination (oracle reference) | 0.8896 | 2.66 | 462 |

The relevant efficiency gain concerns downstream verification rather than necessarily the cost of running PubCaseFinder or GestaltMatcher themselves. If a component returns its top 30 in a single request, selecting a shallower accepted depth does not make that component execution cheaper. It reduces the number of candidate diseases passed to evidence retrieval, LLM reasoning, verification and final ranking, which are the stages expected to dominate the variable downstream cost in the current workflow.

## Structured outputs strengthen provenance through the integration pipeline

The hackathon implementation also strengthened the structured-output contract used between candidate-generation, ranking and verification stages. Candidate decisions are tied to stable candidate identifiers rather than unconstrained disease-name generation, and provenance fields are carried with the candidate record. The revised schema additionally requires source references, including URLs where available, so that evidence used during verification can be traced back to its retrieval source.

This change is an implementation contribution rather than an independent demonstration of explanation correctness. A URL field can preserve provenance only if the retrieved source exists, supports the associated claim and is not detached from the candidate during later transformations. Those properties require separate citation-fidelity and expert-review evaluation. The immediate goal is narrower: make loss of candidate identity and evidence provenance detectable rather than implicit in free-text LLM output.

# Discussion

ZebraSeek connects facial and clinical phenotype tools to an LLM workflow for producing a compact, reviewable disease differential. In the original 74-case evaluation, its final list had higher observed recall than each individual component. The scientific interpretation rests on the paired outcomes: 11 diagnoses were recovered beyond PubCaseFinder's top-five coverage, while five diagnoses retrieved by PubCaseFinder were lost. The improvement is therefore a balance between complementary candidate availability and imperfect retention, not an unconditional benefit from adding tools.

The hackathon analyses extend this interpretation upstream. Candidate retention matters only after a useful hypothesis has entered the pool. In the expanded v0.1.27 analysis, the PCF-GM union rose from 77.5% coverage at top five to 89.0% at top 30, showing that a shallow candidate budget can itself impose a substantial ceiling. The obvious response--passing every deep candidate into verification--creates a different problem: exhaustive PCF@30 ∪ GM@30 produced 57.57 unique candidates per image-level instance on average. ZebraSeek therefore faces two linked selection problems: how far to explore each specialist ranking, and how to retain the useful hypotheses after they are retrieved.

Adaptive candidate-depth selection makes that trade-off explicit. The oracle analysis shows that the same observed 88.96% candidate coverage is compatible, in principle, with a much smaller mean candidate set when the necessary depth is chosen per input. Because the oracle uses the reference diagnosis, its 2.66-candidate mean is not an achievable benchmark and should not be compared with executable methods as if it were one. Its role is to quantify headroom. The preliminary zero-shot LLM policies recover part of the coverage available from deep retrieval while processing substantially fewer candidates than exhaustive depth, but the present results do not establish an optimal policy or a statistically reliable LLM advantage.

This efficiency question is especially relevant to the current architecture because later stages perform LLM ranking and evidence verification. Candidate count is not identical to compute cost, but it is a practical proxy when external retrieval and reasoning are performed per candidate. The next evaluation should therefore report actual input and output tokens, latency, API calls and monetary cost alongside candidate count. It should also compare the LLM policy with the best fixed-depth combination, simple rules based on within-tool rank or score shape, and learned or sequential policies on patient-wise development and test splits.

Traceability is the third part of the design. The interface already exposes component proposals and final candidates, while the revised structured-output contract preserves candidate identifiers and provenance fields, including source URLs where available. This architecture can make it possible to inspect which specialist tool introduced a disease and which external sources were used during verification. It does not, by itself, prove that explanations are faithful. Citation existence, claim support, patient-finding alignment and handling of negative findings remain separate evaluation targets.

These contributions should be distinguished from existing multimodal models. PhenoScore and GestaltMML already establish important precedents for integrating facial and clinical representations [@PhenoScore2023; @GestaltMML2026]. ZebraSeek instead combines proposals from specialist tools with LLM-based integration and external-information checks. Its proposed value is not a new facial representation or the first multimodal approach, but a modular workflow in which candidate coverage, candidate retention, downstream efficiency and provenance can be measured separately.

Several limitations constrain the present interpretation. The original benchmark is retrospective, small and selected for availability of both phenopackets and facial images. The expanded analysis contains 462 images from 368 patients, so image-level observations are not independent patient-level tests. The reported 54 disorders remain unevenly represented, and the zero-shot depth-selection analysis currently has one fewer usable instance than the fixed-depth analyses. No controlled end-to-end comparison has yet shown that adaptive depth improves final ZebraSeek Recall@5, latency or token cost. Repeated-run variability, disease-stratified performance and patient-wise held-out evaluation are also required.

Literature-derived cases additionally require a careful audit of information overlap. Source publications, related patients or query images may be represented in phenotype resources, facial reference galleries, model training corpora or verification-time retrieval. Removing explicit diagnoses from the query is necessary but insufficient to rule out these routes. Independent cases and transparent provenance are needed to test generalization; expert evaluation is additionally required to assess explanations and any effect on diagnostic decisions. The present findings do not establish molecular diagnostic yield, clinical benefit or equitable performance.

The resulting research question is broader than whether adding modalities improves accuracy: how can complementary specialist evidence be explored deeply enough to capture useful disease hypotheses, integrated efficiently enough to remain practical, and presented with enough provenance to be independently reviewed? The current ZebraSeek implementation, original 74-case benchmark and hackathon candidate-depth analysis provide an initial framework for answering these questions rather than a completed clinical validation.

# Online Methods

## Study design and original case selection

The original study retrospectively evaluated 74 literature-derived cases covering 19 diseases. Phenotypic descriptions, sex and recorded diagnoses were obtained from Phenopacket Store v0.1.25, a corpus built using the GA4GH Phenopacket representation [@PhenopacketStore2025]. Cases were linked to facial images in GestaltMatcher Database, a resource for facial phenotyping [@GMDB2024]. The presentation describes matching records corresponding to the same individual across the two resources.

**TODO:** Document the case-matching procedure, source publication and case identifiers, inclusion and exclusion criteria, number of images per individual, handling of duplicate or related individuals, selection dates and the GestaltMatcher Database release. Confirm all 19 disease labels and counts. The database-wide counts shown in the presentation are not treated as the study's screening denominator.

## Expanded candidate-depth analysis

The hackathon analysis used Phenopacket Store v0.1.27 and matched facial-image data, yielding 368 patients, 462 facial-image instances and 54 recorded disorders. Candidate coverage was evaluated at the image-instance level because multiple images can correspond to one patient. PubCaseFinder and GestaltMatcher rankings were examined to a maximum depth of 30. Exact-OMIM coverage was defined as the fraction of evaluated instances for which the recorded OMIM diagnosis was present in the accepted deduplicated candidate set.

For a patient or image instance $x_i$, let $R_j(x_i)=(c_{ij1},\ldots,c_{ijK_j})$ be the ranking returned by candidate generator $T_j$. An input-specific policy chooses an accepted depth $k_{ij}$ for each generator. The downstream candidate set is

$$
C_{\pi}(x_i)=\bigcup_j\{c_{ij1},\ldots,c_{ij k_{ij}}\},
$$

with duplicate diseases removed. Coverage is

$$
\mathrm{Coverage}(\pi)=\frac{1}{N}\sum_i \mathbf{1}[y_i\in C_{\pi}(x_i)].
$$

The principal optimization target is to reduce the mean deduplicated candidate count, or measured downstream computational cost, subject to a target coverage threshold. Candidate count and actual compute cost are reported separately because the two are not equivalent. In the present implementation PubCaseFinder and GestaltMatcher can return deep rankings in a single execution, so accepted depth primarily changes the number of candidates entering later search, LLM verification and ranking stages rather than the cost of the upstream tools themselves.

## Candidate-depth comparison conditions

Fixed-depth baselines applied the same accepted depth to all instances. The reported conditions include PCF@5, PCF@10, PCF@30, PCF@5 ∪ GM@5, PCF@10 ∪ GM@5 and PCF@30 ∪ GM@30. Mean candidate count was calculated after deduplication across the two component rankings.

The zero-shot LLM conditions asked an LLM to choose candidate depths per input. One condition used input information only; a second also received component-tool results. The present manuscript reports only the aggregate coverage and mean candidate counts supplied from these runs. **TODO:** Archive the exact prompts, model identifier and snapshot, candidate-depth action space, sampling parameters, retry policy, failure handling and the reason one image-level instance lacks a reported zero-shot result.

The ideal-combination condition is an oracle reference. It uses the known reference diagnosis and its position in each ranking to select, for each instance, the smallest candidate set that still contains the correct diagnosis whenever that diagnosis is available within the maximum evaluated depths. It is used only to estimate the theoretical reduction in downstream candidate burden and is not an executable diagnostic method.

## Input preparation and reference diagnoses

ZebraSeek used facial images, HPO findings and recorded sex. The reference diagnosis was used for evaluation rather than intentionally supplied as a model input. HPO provides standardized identifiers for phenotypic abnormalities [@HPO2024]. The workflow can consider explicitly recorded negative findings; the extent to which these were present in the original 74-case benchmark is not documented.

**TODO:** Specify HPO version, query serialization, present/absent finding handling, image preprocessing, sex encoding and any missing-value rules. Document removal of diagnosis-bearing fields, causal gene or variant annotations, file names, captions and other identifying labels from inputs, including information present in source phenopackets but outside the intended query fields. Report the reference-diagnosis ascertainment procedure, disease-identifier mapping, synonym handling and criteria for accepting a predicted diagnosis as correct, including disease families and subtypes.

## Interface documentation

Interface features were described from three screenshots supplied on 12 September 2026. The unpopulated input form is reproduced in Fig. 3. The results screenshot was used to identify visible workflow stages and table fields; its example disease ranking was not used as a benchmark observation. The landing page shows a login requirement. Interface text alone does not verify service access conditions, software licensing, backend data retention or conformity between the displayed application and the evaluated version.

**TODO:** Record the application URL and version, link it to the evaluated software commit, and confirm which interface fields entered each benchmark run. Document service access, storage and external processing arrangements from the implementation and applicable policies.

## Candidate generation

PubCaseFinder generated candidates from HPO findings using phenotype-based disease matching [@PubCaseFinder2018]. GestaltMatcher generated candidates from facial images [@GestaltMatcher2022]. SemanticSearch compared phenotype information with embeddings of disease descriptions obtained from Mondo, which integrates disease terminology across resources [@Mondo2026]. The direct LLM component, labelled GPT-5.2 in the source materials, generated candidates from HPO findings and sex in a zero-shot setting. Each component supplied up to five candidates in the original ZebraSeek benchmark. The expanded candidate-depth analysis separately examined PubCaseFinder and GestaltMatcher to rank 30.

**TODO:** Record component versions and endpoints, disease reference databases, the Mondo release and fields indexed, embedding model and version, query construction, similarity function and ranking rules. Specify the GestaltMatcher model and gallery, and exclusion of query individuals or duplicate images from its reference set. Provide the exact LLM identifier, evaluation dates, prompts, sampling parameters, reasoning settings where applicable and retry policy.

## Candidate integration, verification and provenance

The original integration stage received up to 20 candidate entries with source ranks and scores and used an LLM to rank candidate diseases. A verification stage related candidates to the available phenotype information and consulted external medical information, including PubMed. The reported workflow then generated a final top-five ranking and explanatory text. GPT-5.2 is shown for the ranking, verification and final-output stages in the supplied workflow diagram.

During the hackathon the structured-output contract was strengthened to preserve candidate identity and provenance through these stages. Candidate decisions are represented with candidate identifiers rather than relying only on unconstrained disease-name text, and source-reference fields include URLs where available. This structure is intended to make evidence provenance and candidate transformations auditable. It does not validate the factual correctness or citation fidelity of the retrieved evidence.

**TODO:** Archive the exact schemas, prompts and orchestration code. Define candidate deduplication and normalization, whether verification may introduce new diseases, the number of candidates verified, stopping rules, search queries, retrieval sources and dates, text truncation, error handling and the format of intermediate decisions. Confirm whether all stages used the same model snapshot and settings.

## Evaluation metrics and descriptive analysis

For the original benchmark, top-k recall was the fraction of 74 cases for which the recorded diagnosis occurred among the first k predictions, with k ranging from one to five. The expanded depth analysis instead uses candidate coverage: whether the exact reference OMIM diagnosis appears anywhere in the deduplicated accepted candidate set. These quantities answer different questions and are not directly interchangeable.

For plotting the original benchmark, each one-decimal percentage was converted to the integer count consistent with the denominator of 74. The overlap summaries distinguish successful ZebraSeek cases from its failures and use the component top-five lists. Candidate availability denotes presence of the recorded diagnosis in at least one component top-five list; retention denotes its continued presence in the final top-five list when initially available.

The expanded analysis reports candidate coverage and mean unique downstream candidate count as separate axes. Actual API calls, input and output tokens, wall-clock time and monetary cost have not yet been added to the reported comparison. These quantities should be measured before concluding that one candidate-depth policy is computationally superior in deployment.

**TODO:** Validate all transcribed aggregates against case-level predictions; specify tie handling, failures to return results, repeated-run design and any prompt or model selection performed on each cohort; add patient-wise evaluation for the expanded data; and prespecify paired comparisons and uncertainty estimates.

## Ethics and data governance

The benchmarks are described as secondary analyses of literature-derived cases and associated facial images. **TODO:** Provide the applicable ethics review or exemption determination, institution and reference number; the consent and access conditions for image reuse; and the data-processing arrangements for external services. Public availability of a case description does not establish unrestricted permission to redistribute identifiable facial images. This manuscript includes aggregate figures, schematics and an unpopulated interface screenshot, without patient photographs or populated patient records.

# Data availability

The aggregate values used for the original figures are provided in `paper/data/aggregate_results.json`. The hackathon candidate-depth summary is provided in `paper/data/adaptive_candidate_depth_summary.csv`. These files contain aggregate evaluation values rather than patient-level source data. Phenopacket Store is described in the cited resource paper [@PhenopacketStore2025]. Facial image access is governed by GestaltMatcher Database. **TODO:** Add exact dataset release links, a permitted case-matching manifest, patient-wise split information, case-level prediction and scoring records, and the relevant access conditions. The manuscript repository does not redistribute the underlying patient images.

# Code availability

The manuscript source and scripts used to reproduce its aggregate figures are available at [the manuscript repository](https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper). **TODO:** Add the ZebraSeek software repository, version or commit, license, environment specification, prompts, structured-output schemas and evaluation scripts. The existing figure-generation script reproduces the original presentation summaries; it is not the ZebraSeek diagnostic implementation.

# Acknowledgements

**TODO:** Add funding sources, grant identifiers and acknowledgements approved by the authors. The English draft, subsequent editorial revision and figure code were prepared with assistance from OpenAI Codex using the supplied research materials and verified literature. The authors' scientific verification and final approval remain pending.

# Author contributions

**TODO:** Confirm the contributions of Naoya Yoshikuwa, Hirokazu Chiba, Teppei Okazaki, Jae-Moon Shin, Eisuke Dohi, Hiroyuki Mishima, Atsuko Yamaguchi, Tzung-Chien Hsieh, Orion Buske, Susumu Goto and Toyofumi Fujiwara using an agreed contribution statement. Author order in this working draft places Naoya Yoshikuwa first and Toyofumi Fujiwara last; contribution roles and corresponding authorship have not been inferred from order.

# Competing interests

**TODO:** Obtain declarations from every author and replace this placeholder with the agreed statement. No absence-of-conflict declaration is assumed.

# Additional information

**TODO:** Designate the corresponding author or authors and confirm contact details, final institutional addresses and ORCID identifiers. BioHackrXiv event metadata also remain to be completed before submission.

# References
