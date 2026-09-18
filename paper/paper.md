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
  Rare disease differentials must reconcile evidence unevenly represented across clinical descriptions, facial phenotypes and disease resources. ZebraSeek integrates specialist phenotype and facial matching, semantic retrieval and large language model predictions into a traceable ranked differential with external-information checks. In 74 literature-derived cases spanning 19 diseases, ZebraSeek retrieved the recorded diagnosis at rank one in 50 cases (67.6%) and within five ranks in 59 (79.7%); 11 diagnoses were recovered beyond PubCaseFinder's top-five coverage, while five were lost during integration. The fixed top-five input budget nevertheless prevents later reasoning from recovering diagnoses ranked more deeply by specialist tools. During DBCLS BioHackathon 2026, we expanded evaluation to 368 patients, 462 images and 54 disorders to characterize this retrieval bottleneck and test basic candidate-acquisition strategies that balance coverage against downstream candidate burden. Structured outputs were also strengthened to preserve candidate identity and source URLs. End-to-end gains from adaptive retrieval remain to be established.
---

A differential diagnosis is a bridge between a patient's clinical presentation and the genetic investigations needed to explain it. For rare disorders, this bridge depends on recognizing a disease despite incomplete or unevenly documented phenotypes. Structured clinical findings, facial morphology and published disease descriptions represent different aspects of the same presentation. A diagnosis may therefore be suggested by one source while receiving little support from another. Bringing these sources together is useful only if the resulting shortlist preserves informative hypotheses and remains small enough to examine.

The Human Phenotype Ontology (HPO) standardizes clinical abnormalities [@HPO2024]. PubCaseFinder links such findings to disease-associated phenotypes in case reports [@PubCaseFinder2018], whereas GestaltMatcher retrieves similar facial phenotypes [@GestaltMatcher2022]. Combining these forms of information is already an established direction. PhenoScore combines facial analysis and HPO-based similarity to quantify phenotypic variation, and GestaltMML combines facial images with clinical text and demographic information [@PhenoScore2023; @GestaltMML2026]. PEDIA integrates facial and clinical evidence with exome analysis for gene prioritization, while SHEPHERD uses a knowledge graph for several phenotype-driven diagnostic tasks [@PEDIA2019; @SHEPHERD2025]. Thus, neither multimodality nor the use of external phenotype knowledge alone defines the contribution of a new system.

Large language models (LLMs) add a way to coordinate retrieval and compare candidate explanations. DeepRare, RareAgents and MEDDxAgent demonstrate different forms of tool-supported or iterative diagnostic reasoning [@DeepRare2026; @RareAgents2026; @MEDDxAgent2025]. Yet a stronger final ranking cannot be assumed from access to more tools. A recent systematic review found substantial variation across LLM evaluations and highlighted benchmark composition and potential information leakage as barriers to interpreting reported accuracy [@LLMReview2026]. These concerns make comparisons within a common evaluation setting, with explicit diagnostic targets and input information, particularly valuable.

ZebraSeek addresses this setting at the candidate level. Specialized tools convert clinical and facial information into disease proposals, which an LLM ranks and checks against external medical information. This design allows facial evidence to enter the differential through a specialist matcher rather than requiring the LLM to interpret the photograph directly. In the original evaluation, the central question was whether integration could recover diagnoses available through complementary phenotype evidence while retaining useful candidates supported by only one component. The evaluated task uses phenotypic information without genomic variants as inputs; it does not assess variant pathogenicity or discover new disease genes.

This modular design also creates a practical limitation. The modalities are processed by heterogeneous specialist tools, and their internal scores are not assumed to form a calibrated common scale. Downstream integration therefore receives ranked disease candidates and tool-specific metadata rather than a directly comparable joint representation of facial and HPO evidence. In the current workflow each component contributes only its top five candidates. A correct diagnosis ranked more deeply is consequently invisible to later LLM reasoning and verification, regardless of the quality of those downstream stages.

During DBCLS BioHackathon 2026, we focused on this upstream retrieval bottleneck. We examined how much candidate coverage is lost by the fixed top-five input budget, how coverage changes as specialist rankings are explored more deeply, and whether practical input-specific strategies can acquire enough candidates without forwarding every deep-ranked disease to downstream verification. We also strengthened structured outputs so candidate identity and source provenance, including URLs where available, are preserved more explicitly through the integration pipeline.

Here we retain the original 74-case ZebraSeek results and component analyses, and add an expanded candidate-acquisition analysis using Phenopacket Store v0.1.27 linked to facial images. The original analysis evaluates complementary retrieval and candidate retention. The hackathon analysis characterizes the candidate-acquisition problem and provides fixed-depth, zero-shot LLM and oracle-reference baselines for subsequent adaptive retrieval. Together these analyses preserve ZebraSeek's original aim: effective multimodal integration with a compact, reviewable and traceable differential.

# Results

## Complementary evidence creates both opportunities and a selection problem

The organizing principle of ZebraSeek is that a useful disease hypothesis need not be supported by every component (Fig. 1). Phenotype matching, facial similarity, semantic retrieval and direct LLM prediction provide different routes to the same disease vocabulary. Their outputs are candidate proposals, not independent measurements of diagnostic probability: tools can share phenotype annotations, literature and underlying knowledge. Agreement can support review, but the number of agreeing tools is not a calibrated measure of certainty.

Integration must address two questions in sequence. First, is the recorded diagnosis available in any component's candidate list? Second, if available, does it remain in the final differential? A correct candidate absent from one tool can expand that tool's coverage, whereas discarding a candidate supplied by another can offset this benefit. Figure 1 presents this conceptual distinction; the following analyses examine it using the existing component and final-output summaries.

![**From complementary evidence to a reviewable differential.** Different representations can retrieve shared or source-specific disease hypotheses. The conceptual distinction is between candidate availability and retention during shortlist formation. A source-specific candidate may be useful even without cross-tool agreement. Candidate-level integration connects specialist retrieval with LLM ranking and external-information checks; correctness and the value of each stage require separate evaluation.](figures/concept_candidate_retention.png){width=100%}

## ZebraSeek integrates candidate proposals from facial and clinical evidence

In the evaluated workflow, ZebraSeek uses a facial image, HPO-encoded clinical findings and recorded sex (Fig. 2). The facial image is processed by GestaltMatcher, while HPO information is supplied to PubCaseFinder and SemanticSearch. The latter retrieves disease candidates by embedding-based similarity to disease descriptions derived from Mondo. A direct LLM component receives HPO information and sex and separately proposes a differential diagnosis. The evaluated implementation used GPT-5.2 for direct predictions and subsequent integration stages.

Each component returns up to five candidate diseases, yielding at most 20 candidate entries before accounting for overlap. The integration stage compares candidates while retaining information about their source ranks and scores. A verification stage consults external information, including PubMed, and relates candidate diseases to the patient's findings. Explicitly recorded negative findings can be considered during this step. ZebraSeek then returns five ranked candidates with explanatory text. This staged design separates specialist candidate generation from LLM-based integration and external-information checking, while retaining the origin of each candidate for review.

![**ZebraSeek workflow.** Facial images are analysed by GestaltMatcher; HPO terms are supplied to PubCaseFinder and SemanticSearch; and HPO terms together with recorded sex are supplied to the direct LLM component. Each component provides up to five candidates. LLM-based ranking and literature-based verification produce a final top-five list with explanatory text.](figures/figure1_workflow.png){width=100%}

## A web interface connects clinical input to staged candidate review

The ZebraSeek input interface supports observed and excluded findings, recorded sex, age of onset, facial-image upload and import from Phenopackets (Fig. 3). It brings structured clinical descriptions and facial evidence into one query workflow.

The results view separates tool output, tentative candidates, a stage labelled validation, and final disease candidates. Component tables display disease identifiers, ranks and similarity scores alongside the final differential. This organization allows users to inspect component proposals as well as the integrated result. The validation label denotes the system's external-information checking stage, not independent clinical validation.

![**ZebraSeek clinical input interface.** The input form supports Phenopacket import, observed and excluded findings, sex, age of onset and facial-image upload. No patient photograph or populated patient record is shown.](figures/zebraseek_input_interface.png){width=90%}

## Higher observed recall in a benchmark of 74 cases

The evaluation set comprised 74 cases spanning 19 diseases, obtained by matching Phenopacket Store v0.1.25 records to facial images in GestaltMatcher Database. The recorded diagnosis served as the reference label; the stated system inputs were facial images, HPO findings and sex. Top-k recall indicates whether the recorded diagnosis appeared among the first k predictions from each method.

ZebraSeek had the highest observed recall at every reported cutoff (Fig. 4). Recall\@1 was 67.6% (50/74), compared with 63.5% (47/74) for PubCaseFinder, 31.1% (23/74) for GestaltMatcher and 18.9% (14/74) for both SemanticSearch and the direct LLM. At rank five, ZebraSeek reached 79.7% (59/74), compared with 71.6% (53/74), 50.0% (37/74), 35.1% (26/74) and 33.8% (25/74) for PubCaseFinder, GestaltMatcher, the direct LLM and SemanticSearch, respectively. Relative to PubCaseFinder, the observed differences were 4.1 percentage points at rank one and 8.1 percentage points at rank five, corresponding to net increases of three and six correctly prioritized cases.

These are descriptive comparisons within the reported benchmark. No confidence intervals, repeated-run variability or significance claims are included in this analysis. The comparison also reflects different input modalities across methods and is not a controlled estimate of the effect of LLM integration alone.

![**Top-k diagnostic recall across five methods.** Top-k recall is the percentage of 74 cases whose recorded diagnosis appears within the first k predictions. The same denominator is used at all cutoffs; this figure reports aggregate results without uncertainty estimates.](figures/figure2_recall.png){width=100%}

## Component tools retrieve complementary correct candidates

Among the 59 cases correctly prioritized by ZebraSeek at rank five, the recorded diagnosis was also present in PubCaseFinder's top five for 48 cases, in SemanticSearch's for 25, in the direct LLM's for 26 and in GestaltMatcher's for 35 (Fig. 5). Only 13 of these cases were recovered by all four component tools. The largest exclusive patterns after this four-tool overlap were PubCaseFinder alone (10 cases) and GestaltMatcher alone (seven cases). A further three cases had the recorded diagnosis only in the SemanticSearch candidate list.

ZebraSeek therefore recovered 11 cases in which PubCaseFinder did not retrieve the diagnosis within its top five. Conversely, five cases recovered by PubCaseFinder were missed by ZebraSeek. The difference between these two discordant groups accounts for the net gain of six cases over PubCaseFinder at rank five. This distinction matters: the final list extended coverage beyond the strongest individual component while also losing some of that component's correct candidates.

The observed overlaps support complementary candidate availability, but do not identify the causal contribution of any individual modality. For example, the seven successful cases with GestaltMatcher-only correct candidates motivate a matched evaluation without facial analysis; they do not substitute for that ablation. The integration process may also change its ranking when any component is removed.

![**Component overlap among the 59 ZebraSeek successes at rank five.** Each column represents an exclusive combination of component tools whose top-five lists contained the recorded diagnosis. Connected filled circles identify the tools in each combination; grey circles indicate absence. Bar heights show case counts. The totals at left are conditional on ZebraSeek success and are not the full-cohort recalls of the component tools.](figures/figure3_overlap.png){width=100%}

## Candidate coverage and retention account for different failures

ZebraSeek did not include the recorded diagnosis in its top five for 15 cases (Fig. 6). In eight, none of the four component top-five lists contained the diagnosis. These cases expose a coverage limitation in the candidate lists supplied to integration. In the remaining seven, the diagnosis was available from a component but absent from the final list: five had a correct PubCaseFinder-only candidate and two had a correct GestaltMatcher-only candidate. All seven losses therefore involved a diagnosis retrieved by only one component. The aggregate results do not locate the loss within normalization, initial ranking, verification or final selection.

Across the reported overlap patterns, at least one component contained the correct diagnosis in 66 of 74 cases (89.2%). This union is a descriptive measure of candidate coverage with up to 20 entries per case, not a top-five method or a validated performance target. Its difference from ZebraSeek's 59 successful cases identifies seven potentially recoverable diagnoses already present in the inputs.

The 15 failures were concentrated in two of the 19 disease labels: cardiac, facial, and digital anomalies (OMIM:618164; 10 cases) and a label abbreviated as neurodevelopmental disorder with coarse facies (OMIM:618505; five cases). This concentration motivates disease-stratified evaluation in addition to case-level averages.

![**Correct-candidate availability among the 15 ZebraSeek failures at rank five.** Eight cases had no correct candidate in any component's top-five list. Five had a correct candidate only in PubCaseFinder and two only in GestaltMatcher. The latter seven cases distinguish failure to retain an available diagnosis from absence of that diagnosis in all initial lists.](figures/figure4_failures.png){width=85%}

## Fixed top-five component inputs exclude recoverable diagnoses from later integration

The current ZebraSeek workflow receives only the first five candidates from each component. Because later ranking and verification cannot reconsider a disease that was never passed downstream, the fixed input depth creates a retrieval bottleneck distinct from the retention failures described above. To characterize that bottleneck, we performed a hackathon analysis using Phenopacket Store v0.1.27 linked to facial images, comprising 368 patients, 462 images and 54 recorded disorders. This is an image-level candidate-acquisition analysis rather than an end-to-end ZebraSeek benchmark; multiple images can correspond to the same patient.

PubCaseFinder covered 73.4% of the 462 image-level instances at rank five, 78.1% at rank ten and 83.5% at rank 30. GestaltMatcher covered 30.3%, 34.6% and 45.0%, respectively. The deduplicated PubCaseFinder--GestaltMatcher union increased from 77.5% at rank five to 82.7% at rank ten and 89.0% at rank 30 (Fig. 7). The important observation is that the candidate pool available to ZebraSeek changes materially when the specialist rankings are explored beyond five. The fixed top-five design therefore leaves a measurable set of potentially useful diagnoses inaccessible to downstream reasoning.

![**Deeper specialist rankings expose candidates hidden by a fixed top-five input budget.** Exact-OMIM inclusion was evaluated for 462 facial-image instances linked to 368 patients across 54 disorders. Bars show candidate coverage for PubCaseFinder (PCF), GestaltMatcher (GM) and their deduplicated union at increasing retrieval depths. The union increased from 77.5% at top five to 89.0% at top 30. This figure characterizes the candidate pool available before ZebraSeek integration; it is not an end-to-end diagnostic-performance comparison.](figures/expanded_candidate_depth_recall.svg){width=100%}

## Basic candidate-acquisition strategies quantify the coverage--burden trade-off

Simply forwarding every deep-ranked candidate to the existing verification pipeline is not an attractive solution. At rank 30, PubCaseFinder and GestaltMatcher together can contribute almost 60 unique diseases per image-level instance, each of which may require normalization, evidence retrieval and LLM-based comparison. The practical problem is therefore to acquire enough candidates from each modality-specific ranking without treating every deep candidate as equally worthy of downstream processing.

This problem is constrained by the way the modalities enter ZebraSeek. PubCaseFinder operates on HPO information and GestaltMatcher on facial images, and their scores are tool-specific rather than calibrated across components. Candidate acquisition therefore cannot be reduced to applying one shared threshold to a common multimodal score. We instead compare simple strategies for deciding how many candidates to accept from each ranking.

Fixed-depth conditions provide reference points (Table 1). PCF@30 reached 83.55% coverage with 30 candidates on average. The deduplicated union of PCF@30 and GM@30 reached 88.96% coverage but produced 57.57 unique candidates on average. Two preliminary zero-shot LLM policies selected depths per input. The input-only policy achieved 84.38% coverage with 19.28 candidates on average, whereas the policy that also received tool results achieved 84.60% with 18.18 candidates on average. The zero-shot conditions include 461 image-level instances and are treated as basic feasibility baselines rather than evidence that LLM-based selection is optimal.

An oracle-style reference uses the known diagnosis to choose the smallest sufficient depths whenever the correct diagnosis is available within the evaluated rankings. It reaches the same 88.96% coverage as exhaustive PCF@30 plus GM@30 while retaining 2.66 candidates on average. This oracle is not an executable diagnostic method and is not presented as a performance target. It indicates that substantial headroom exists between a fixed exhaustive candidate budget and the minimum candidate set that would have been sufficient in retrospect.

**Table 1 | Candidate coverage and average deduplicated candidate count in the expanded analysis.** The `+` sign denotes a deduplicated union of the two accepted rankings, not arithmetic addition.

| Selection condition | Correct-diagnosis coverage | Mean unique candidates | n |
| --- | ---: | ---: | ---: |
| PCF@5 | 0.7338 | 5.00 | 462 |
| PCF@10 | 0.7814 | 10.00 | 462 |
| PCF@30 | 0.8355 | 30.00 | 462 |
| PCF@5 + GM@5 | 0.7749 | 9.66 | 462 |
| PCF@10 + GM@5 | 0.8160 | 14.58 | 462 |
| PCF@30 + GM@30 | 0.8896 | 57.57 | 462 |
| LLM depth, input only | 0.8438 | 19.28 | 461 |
| LLM depth, input + tool results | 0.8460 | 18.18 | 461 |
| Oracle minimum-depth reference | 0.8896 | 2.66 | 462 |

The candidate count in Table 1 is a proxy for downstream workload, not a direct measurement of compute. If PubCaseFinder or GestaltMatcher returns its top 30 in a single request, accepting a shallower depth does not make that upstream tool execution cheaper. The intended saving is in the number of diseases passed to external search, LLM verification and final ranking. Actual token use, latency, API calls and monetary cost remain separate end-to-end evaluation measures.

## Hackathon implementation strengthened traceable candidate handling

The hackathon implementation also strengthened the structured-output contract used between candidate generation, ranking and verification. Candidate decisions are tied to stable candidate identifiers rather than unconstrained disease-name generation, and provenance fields are carried with the candidate record. The revised schema additionally requires source references, including URLs where available, so that evidence used during verification can remain attached to its retrieval source.

This change supports ZebraSeek's original goal of a reviewable differential, but it is distinct from candidate-acquisition performance. A URL field does not by itself establish that a retrieved source exists, supports the associated claim or was interpreted correctly. Citation fidelity and expert review remain separate evaluation targets. The immediate implementation goal is to make candidate identity and evidence provenance explicit and less likely to be lost during LLM-mediated transformations.

# Discussion

ZebraSeek connects facial and clinical phenotype tools to an LLM workflow for producing a compact, reviewable disease differential. In the original 74-case evaluation, its final list had higher observed recall than each individual component. The scientific interpretation rests on the paired outcomes: 11 diagnoses were recovered beyond PubCaseFinder's top-five coverage, while five diagnoses retrieved by PubCaseFinder were lost. The improvement is therefore a balance between complementary candidate availability and imperfect retention, not an unconditional benefit from adding tools.

The hackathon work addresses a different but adjacent failure mode: useful diagnoses that never enter the integration stage. The current workflow accepts only the top five candidates from each specialist component. Because ZebraSeek operates across heterogeneous modalities through specialist tools rather than through one calibrated shared representation, the system must decide which ranked disease candidates to bring forward from each tool. The expanded analysis makes this candidate-acquisition problem visible and measurable.

The expanded v0.1.27 analysis shows that deeper PCF and GM rankings contain additional correct diagnoses beyond the fixed top-five pool, while exhaustive deep retrieval greatly expands the downstream candidate set. These observations define a practical tension for ZebraSeek: a shallow candidate budget limits what later reasoning can recover, whereas an exhaustive candidate budget increases the amount of evidence retrieval and LLM comparison required. The appropriate candidate depth is therefore part of the system design rather than a neutral preprocessing choice.

The basic fixed-depth, zero-shot and oracle-reference comparisons are an initial validation of this framing. They show that coverage and candidate burden can vary substantially under different acquisition policies, but they do not establish a final adaptive algorithm. In particular, the oracle uses the reference diagnosis and only quantifies retrospective headroom. The current zero-shot LLM policies are baselines. Candidate-acquisition policies can subsequently be compared with fixed-depth combinations, rules based on within-tool rank or score shape, feature-based or learned gating, and sequential stop/continue strategies under patient-wise development and held-out evaluation.

This candidate-acquisition work complements rather than replaces the original ZebraSeek contribution. The original benchmark demonstrates complementary retrieval, candidate retention and a higher observed final recall within its evaluation setting. The hackathon analysis identifies an upstream source of avoidable blindness in that architecture and establishes measurements for improving it. The structured-output revision simultaneously strengthens provenance by preserving candidate identifiers and source URLs through downstream processing. Together, these changes move ZebraSeek toward a workflow that is effective in candidate integration, economical in what it chooses to verify and explicit about where its evidence came from.

These aims should be distinguished from existing multimodal models. PhenoScore and GestaltMML already establish important precedents for integrating facial and clinical representations [@PhenoScore2023; @GestaltMML2026]. ZebraSeek instead combines proposals from specialist tools with LLM-based integration and external-information checks. Its proposed value is not a new facial representation or the first multimodal approach, but a modular workflow in which candidate acquisition, candidate retention, downstream verification and provenance can be examined separately.

Several limitations constrain the present interpretation. The original benchmark is retrospective, small and selected for availability of both phenopackets and facial images. The expanded analysis contains 462 images from 368 patients, so image-level observations are not independent patient-level tests. The reported 54 disorders remain unevenly represented, and the zero-shot candidate-acquisition analysis contains one fewer instance than the fixed-depth analyses. No controlled end-to-end comparison has yet shown that an adaptive acquisition policy improves final ZebraSeek Recall@5, latency, token use or monetary cost. Repeated-run variability, disease-stratified performance and patient-wise held-out evaluation are also required.

Literature-derived cases additionally require careful consideration of information overlap. Source publications, related patients or query images may be represented in phenotype resources, facial reference galleries, model training corpora or verification-time retrieval. Removing explicit diagnoses from the query is necessary but insufficient to rule out these routes. Independent cases and transparent provenance are needed to test generalization; expert evaluation is additionally required to assess explanations and any effect on diagnostic decisions. The present findings do not establish molecular diagnostic yield, clinical benefit or equitable performance.

The resulting research question is broader than whether adding modalities improves accuracy: how can complementary specialist evidence be acquired deeply enough to avoid preventable candidate loss, integrated selectively enough to remain practical, and presented with enough provenance to be independently reviewed? The current ZebraSeek implementation, original 74-case benchmark and hackathon candidate-acquisition analysis provide an initial framework for answering these questions rather than a completed clinical validation.

# Online Methods

## Study design and original case selection

The original study retrospectively evaluated 74 literature-derived cases covering 19 diseases. Phenotypic descriptions, sex and recorded diagnoses were obtained from Phenopacket Store v0.1.25, a corpus built using the GA4GH Phenopacket representation [@PhenopacketStore2025]. Cases were linked to facial images in GestaltMatcher Database, a resource for facial phenotyping [@GMDB2024], by matching records corresponding to the same individual across the two resources.

## Expanded candidate-acquisition analysis

The hackathon analysis used Phenopacket Store v0.1.27 and matched facial-image data, yielding 368 patients, 462 facial-image instances and 54 recorded disorders. Candidate coverage was evaluated at the image-instance level because multiple images can correspond to one patient. PubCaseFinder and GestaltMatcher rankings were examined to a maximum depth of 30. Exact-OMIM coverage was defined as the fraction of evaluated instances for which the recorded OMIM diagnosis was present in the accepted deduplicated candidate set.

The analysis is constrained by heterogeneous specialist outputs. PubCaseFinder uses HPO information, whereas GestaltMatcher uses facial images. Their internal scores may have different meanings and scales and are not assumed to be directly comparable. The common object available to downstream ZebraSeek integration is therefore the ranked disease candidate, together with tool-specific rank, score and provenance metadata.

For an instance $x_i$, let $R_j(x_i)=(c_{ij1},\ldots,c_{ijK_j})$ be the ranking returned by candidate generator $T_j$. A candidate-acquisition policy chooses an accepted depth $k_{ij}$ for each generator. The downstream candidate set is

$$
C_{\pi}(x_i)=\bigcup_j\{c_{ij1},\ldots,c_{ij k_{ij}}\},
$$

with duplicate diseases removed. Coverage is

$$
\mathrm{Coverage}(\pi)=\frac{1}{N}\sum_i \mathbf{1}[y_i\in C_{\pi}(x_i)].
$$

The practical objective is to retain high candidate coverage while reducing the mean deduplicated candidate count, or ultimately the measured downstream computational cost. Candidate count and actual compute cost are reported separately because the two are not equivalent. In the present implementation PubCaseFinder and GestaltMatcher can return deep rankings in a single execution, so accepted depth primarily changes the number of candidates entering later search, LLM verification and ranking stages rather than the cost of the upstream tools themselves.

## Candidate-acquisition comparison conditions

Fixed-depth baselines applied the same accepted depth to all instances. The reported conditions include PCF@5, PCF@10, PCF@30, and deduplicated PCF--GM unions at selected depths. Mean candidate count was calculated after deduplication across the two component rankings.

The zero-shot LLM conditions asked an LLM to choose candidate depths per input. One condition used input information only; a second also received component-tool results. Aggregate coverage and mean candidate counts are reported for 461 image-level instances in these conditions.

The oracle minimum-depth condition is a retrospective reference. It uses the known diagnosis and its position in each ranking to choose the smallest accepted candidate set that still contains the correct diagnosis whenever that diagnosis is available within the maximum evaluated depths. It is used only to estimate how much downstream candidate burden could theoretically be reduced by perfect instance-specific acquisition and is not an executable diagnostic method.

## Input preparation and reference diagnoses

ZebraSeek used facial images, HPO findings and recorded sex. The reference diagnosis was used for evaluation rather than intentionally supplied as a model input. HPO provides standardized identifiers for phenotypic abnormalities [@HPO2024]. The workflow can also consider explicitly recorded negative findings.

## Interface documentation

The application interface supports Phenopacket import, observed and excluded findings, recorded sex, age of onset and facial-image upload. The results interface exposes component outputs, tentative candidates, external-information checking and final disease candidates.

## Candidate generation

PubCaseFinder generated candidates from HPO findings using phenotype-based disease matching [@PubCaseFinder2018]. GestaltMatcher generated candidates from facial images [@GestaltMatcher2022]. SemanticSearch compared phenotype information with embeddings of disease descriptions obtained from Mondo, which integrates disease terminology across resources [@Mondo2026]. The direct LLM component used HPO findings and sex in a zero-shot setting. Each component supplied up to five candidates in the original ZebraSeek benchmark. The expanded candidate-acquisition analysis separately examined PubCaseFinder and GestaltMatcher to rank 30.

## Candidate integration, verification and provenance

The original integration stage received up to 20 candidate entries with source ranks and scores and used an LLM to rank candidate diseases. A verification stage related candidates to the available phenotype information and consulted external medical information, including PubMed. The workflow then generated a final top-five ranking and explanatory text.

During the hackathon the structured-output contract was strengthened to preserve candidate identity and provenance through these stages. Candidate decisions are represented with candidate identifiers rather than relying only on unconstrained disease-name text, and source-reference fields include URLs where available. This structure is intended to make evidence provenance and candidate transformations auditable; factual correctness and citation fidelity remain separate evaluation targets.

## Evaluation metrics and descriptive analysis

For the original benchmark, top-k recall was the fraction of 74 cases for which the recorded diagnosis occurred among the first k predictions, with k ranging from one to five. The expanded acquisition analysis instead uses candidate coverage: whether the exact reference OMIM diagnosis appears anywhere in the deduplicated accepted candidate set. These quantities answer different questions and are not directly interchangeable.

The overlap summaries distinguish successful ZebraSeek cases from its failures and use the component top-five lists. Candidate availability denotes presence of the recorded diagnosis in at least one component top-five list; retention denotes its continued presence in the final top-five list when initially available.

The expanded analysis reports candidate coverage and mean unique downstream candidate count as separate axes. Candidate count is treated as a measure of downstream burden rather than as a direct measurement of API calls, token use, wall-clock time or monetary cost.

## Ethics and data governance

The benchmarks are secondary analyses of literature-derived cases and associated facial images. This manuscript reports aggregate figures, schematics and an unpopulated interface screenshot and does not redistribute patient photographs or populated patient records.

# Data availability

The aggregate values used for the original figures are provided in `paper/data/aggregate_results.json`. The hackathon candidate-acquisition summary is provided in `paper/data/adaptive_candidate_depth_summary.csv`. These files contain aggregate evaluation values rather than patient-level source data. Phenopacket Store is described in the cited resource paper [@PhenopacketStore2025]. Facial-image access is governed by GestaltMatcher Database. The manuscript repository does not redistribute the underlying patient images.

# Code availability

The manuscript source and scripts used to reproduce its aggregate figures are available at [the manuscript repository](https://github.com/PubCaseFinder/biohackathon-2026-zebraseek-paper). The ZebraSeek implementation is developed at [708san/AI_AgentWithLangGraph](https://github.com/708san/AI_AgentWithLangGraph), whose public README describes the rare-disease diagnosis pipeline, Phenopacket runner and optional prompt/node logging. The manuscript figure-generation scripts reproduce aggregate study summaries; they are not the diagnostic implementation.

# Acknowledgements

# Author contributions

# Competing interests

# Additional information

# References