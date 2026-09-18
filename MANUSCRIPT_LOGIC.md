# ZebraSeek manuscript logic

最終更新: 2026-09-19

この文書は、ZebraSeekプレプリントの**科学的ストーリー、主張の境界、図表の役割、編集判断を管理する正本**です。GPT、Codex、その他の編集者は `paper/paper.md` を変更する前に必ず本ファイルを確認してください。

`paper/paper.md` には読者向けの原稿だけを置きます。未確定情報、著者への質問、再現性TODOは `EDITORIAL_CHECKLIST.md` で管理します。

## 1. 一文で言うと何の研究か

ZebraSeekは、希少疾患診断で分散している臨床表現型、顔貌、疾患知識などを、それぞれに適した専門ツールから**疾患候補へ変換し、候補の出所を保ったままLLMで柔軟に統合・検証して、短く確認可能な鑑別リストへまとめる**モジュール型診断支援システムである。

本プレプリントでは、顔画像を「HPOだけでは十分に表現しにくい表現型情報を追加できる最初の画像モダリティ」と位置づける。元の74症例評価ではこの統合の有用性と候補保持の問題を示し、BioHackathon 2026ではさらに、異なる専門ツールから**どの候補をどこまで後段へ送るか**という効率的な候補探索・選択の問題を検討する。

## 2. 背景から主張までの論理

ストーリーは必ず次の順にする。

1. **希少疾患診断そのものが難しい。** 疾患数が多く、各疾患は稀で、表現型は不完全・年齢依存・非典型でありうる。患者は複数の診療科、検査、誤診を経る長い diagnostic odyssey を経験しうる。
2. **診断に使える情報は一種類ではない。** HPOで表現された臨床所見、顔貌、既報症例、疾患記述、遺伝情報、将来的には臓器画像などは異なる情報を持つ。
3. **顔画像にはHPOとは異なる実用的な価値がある。** 顔写真は追加の遺伝検査を必要とせず取得でき、画像解析により顔貌を定量的な表現へ変換できるため、専門家がすべてのdysmorphic featureを主観的に認識してHPOへ手入力することへの依存を下げられる。GestaltMatcherは顔貌空間で患者を照合し、学習時に含まれていない超希少疾患でも同一分子診断例のmatchingを可能にした。PEDIAは、顔画像由来の情報がclinical termsだけでは捉えきれない情報を含むことを示した。
4. **ただし「画像は客観的だから正しい」とは書かない。** 顔画像解析も撮影品質、年齢、人口集団、学習データ、model coverageの影響を受ける。主張するのは、画像が**人手の記述とは異なる機械可読な表現型情報**を提供しうること、そしてHPO annotationを補完しうることまでである。
5. **既存研究はマルチモーダル統合の価値をすでに示している。** PhenoScore、GestaltMML、PEDIAなどは顔貌・HPO・臨床情報・遺伝情報の組合せを示し、SHEPHERDはknowledge graphを用いる。したがって「複数モダリティを使うこと」自体をZebraSeekの新規性とはしない。
6. **既存の統合方法はさまざまである。** 例えばPEDIAは、画像・HPO・variant情報から得た複数の数値scoreをlinear SVMで統合する。これは有効な先行例だが、あらかじめ定義されたnumeric featuresの固定的な統合である。ZebraSeekでは、候補疾患、rank、tool-specific score、negative findings、外部情報などをLLMがcandidate levelで扱うため、異種出力をより文脈依存に統合できる設計を目指す。ただし、この柔軟性自体を「PEDIAより高性能」とは主張しない。LLM挙動への依存という新たな制約も伴う。
7. **LLM/agentic systemsはさらに広い情報統合と根拠提示を可能にしている。** DeepRareは多数の専門ツール・知識源を組み合わせ、検証可能な医療情報に紐づくreasoning chainを提示する。published formulationではfree text、HPO、VCF/genetic dataを入力とするが、顔画像は入力モダリティに含まれていない。
8. **したがってZebraSeekの問いは「multimodalか否か」ではない。** 重要なのは、HPO、顔画像、将来的には他の画像など、**性質もscore scaleも異なる専門ツールの出力を、共通のcandidate levelでどう保持し、どこまで後段へ送って、どう統合・検証するか**である。
9. **この運用上の問題は、既存のmultimodal fusionそのものとは区別して書く。** 「全く研究されていない」と断言しない。代わりに、既存研究の多くは表現の融合や最終予測性能を主眼とし、異種specialist rankingsから何件を後段LLM verificationへ送るかというcandidate-allocation problemは、少なくとも本研究が扱う形では明示的な評価対象になりにくかった、と表現する。
10. **ZebraSeekの価値は3軸で整理する。**
    - Effectiveness: 相補的な専門ツールの候補を統合し、単独ツールでは拾いにくい候補も最終鑑別へ残す。
    - Traceability: candidate ID、source tool、external source、URLを後段まで保持し、候補と根拠の由来を追えるようにする。
    - Efficiency: LLMによる検索・検証・ランキングに全候補を渡すのではなく、必要な候補だけを後段へ送る設計を目指す。
11. **元の74症例評価はEffectivenessの根拠である。** ZebraSeekはRecall@1 67.6%、Recall@5 79.7%。PubCaseFinder Top 5にない正解を11例回収した一方、PubCaseFinderが持っていた正解を5例失った。したがって、候補を広げる価値と、統合中に候補を失う問題の両方が存在する。
12. **顔画像の価値はこの74症例だけから因果的には断定しない。** GestaltMatcher-onlyで正解候補が得られた症例は顔画像の補完性を示唆するが、顔画像を除いたcontrolled ablationがないため、「顔画像のおかげで診断できた」とは書かない。
13. **現行ZebraSeekには構造的な限界がある。** 各componentからTop 5を取ることはヒューリスティックであり、Top 5より下の疾患は後段のLLMには見えない。一方、Top 30などをすべて渡せば、外部検索、LLM verification、rankingの対象が増える。
14. **入力モダリティのscoreは直接比較できない。** PubCaseFinderはHPO、GestaltMatcherは顔画像を扱い、scoreの意味・分布・尺度も異なる。現時点で共通に扱える主要な単位は `disease candidate + within-tool rank/score + source information` である。
15. **LLMの推論能力だけではこの問題を解けない。** LLMは候補統合・検証に有用だが、候補集合に存在しない疾患を選ぶことはできない。また候補数を増やすほど、後段search/verification/rankingの処理量は増える。したがって、LLMに渡す候補集合そのものを設計する必要がある。
16. **BioHackathon 2026の主眼はここにある。** Top 5でどの程度候補が漏れるのか、より深い順位まで見るとcoverageがどの程度増えるのか、その代わり後段へ渡るcandidate countがどの程度増えるのかを拡張データで調べ、症例ごとに必要な候補だけを選ぶ方向が有用かを検討する。
17. fixed depth、zero-shot LLM、known diagnosisを使うbest-case retrospective referenceは、**この問題を理解するための最初のbaseline**であり、比較自体が研究目的ではない。
18. structured outputの強化は別軸のhackathon contributionであり、candidate IDとsource URLを保持してtraceabilityを改善する。
19. **顔画像は最終地点ではなく最初の画像モダリティである。** Eye2Geneのように、網膜画像から遺伝子候補を生成するspecialist modelも存在する。将来的には、顔貌だけでなく網膜画像など異なる画像モダリティを、それぞれの専門modelからcandidate listへ変換し、ZebraSeekのcandidate-level architectureへ接続できる可能性がある。
20. **モダリティが増えるほどEfficiencyの問題は重要になる。** すべてのtool outputを無条件にLLMへ渡すのではなく、その患者で有用なmodality/candidateを選択して深掘りすることが、より多面的な診断支援へ拡張する際の研究課題になる。

## 3. 既存研究との位置づけ

### Facial phenotyping and multimodal phenotype models

GestaltMatcherはportrait imageをClinical Face Phenotype Spaceへ埋め込み、facial phenotype similarityを使ってrare-disease matchingを行う。学習セット外のultra-rare disorderでも同一分子診断例のmatchingを示している。

PEDIAはDeepGestaltのimage score、HPO-based similarity scores、variant deleteriousnessを含む5種類のscoreをlinear SVMで統合してgene prioritizationを行う。PEDIA自身も、frontal photographの情報がclinical termsを超える情報を持つと報告している。

PhenoScoreやGestaltMMLも、facial informationとstructured/clinical informationを組み合わせる価値を示している。これらはZebraSeekの新規性を否定する材料ではなく、画像由来のphenotypeが有用な独立情報源であることを示す基盤として扱う。

### Agentic / LLM systems

DeepRareはfree text、HPO、genetic testing results/VCFを入力し、多数の専門ツール・知識源をagenticに統合し、source-linked reasoningを提示する。published architectureの入力にはfacial imageは含まれていない。

ZebraSeekは、DeepRareより多くのツールを使うことを新規性とはしない。ZebraSeekが焦点を当てるのは、**modality-specific specialist outputsをcandidate levelで保持し、どの候補を後段のLLM integration / evidence retrievalへ送るかを設計対象にすること**である。

### PEDIAとの違いの表現

PEDIAはpredefined numeric featuresをlinear SVMで統合する。一方ZebraSeekは、candidate rank/score、source tool、patient findings、negative findings、external evidenceなど、異なる構造の情報をLLMが文脈に応じて参照できる。

この違いは「ZebraSeekの方が高度／優秀」とは書かない。正確には、**fixed linear score fusionよりも、heterogeneous candidate metadataとexternal evidenceを扱える柔軟なintegration interfaceを持つ**と表現する。その代わりLLM variability、hallucination、candidate loss、costという課題がある。

### Eye2Geneと将来拡張

Eye2GeneはFAF、infrared、SD-OCTなどのretinal imagesからinherited retinal diseaseのgene-level predictionsを生成する。画像由来predictionがHPO-only prioritizationを補完しうることを示しており、顔画像以外の画像モダリティがrare-disease prioritizationに寄与しうる具体例としてDiscussionで用いる。

ZebraSeekへ直接Eye2Geneを実装済みとは書かない。将来的にgene-level outputをdisease/gene candidate representationへ接続するためのmappingが必要である。

## 4. 今回のContribution

### Contribution A — candidate-level multimodal integration

- HPO、顔画像などを専門ツールで疾患候補へ変換する。
- 顔画像をLLMへ直接解釈させず、GestaltMatcherというspecialist modelを介して利用する。
- candidateごとにsource tool、rank/scoreを保持する。
- LLMで候補を統合し、external medical informationと照合する。
- raw modalitiesを1つのend-to-end modelへ直接融合するのではなく、specialist outputsを共通のcandidate levelで扱う。

### Contribution B — facial image as complementary phenotype evidence

- 顔画像はHPO annotationと異なる形でphenotypeを捉える。
- 自動image analysisにより、専門家が顔貌特徴をすべて言語化・HPO化することへの依存を減らせる。
- 74-case benchmarkのGestaltMatcher-only successful patternsは補完性を示唆するが、controlled facial ablationではない。

### Contribution C — 74症例での統合性能とfailure decomposition

- Recall@1: 50/74 (67.6%)。
- Recall@5: 59/74 (79.7%)。
- PubCaseFinder Top 5外から11例を回収し、PubCaseFinderが持っていた5例を失った。
- candidate availabilityとcandidate retentionを分けて考える必要性を示す。

### Contribution D — fixed Top 5の限界を拡張データで調べる

- Phenopacket Store v0.1.27 linked dataset: 368 patients / 462 images / 54 disorders。
- PCF/GMのdepthを広げるとcandidate coverageが上がる一方、後段へ渡るunique candidatesも増える。
- Fig. 7の主張は「Top 30で89%」そのものではなく、fixed Top 5がcandidate poolを制約していること。

### Contribution E — efficient candidate explorationの基礎評価

- fixed-depth conditions、zero-shot LLMによるcase-specific depth selection、known diagnosisを使うbest-case retrospective referenceを比較する。
- 目的はwinnerを決めることではなく、coverageとcandidate countのtrade-offを確認すること。
- zero-shot LLMはGPT-5.2 API、reasoning effort medium。
- zero-shot条件が461 instancesなのは、1件のimageがAPI content-safety policyでrejectされたため。
- final case-specific selection methodやend-to-end speed-upは今後の検証対象。

### Contribution F — structured outputによるsource traceability改善

- stable candidate IDで候補を扱う。
- source tool、evidence source、URLをstructured fieldsとして保持する。
- URL保持はcitation correctnessやmedical validityを自動的に保証しない。

## 5. 現状の限界として明示すること

- fixed Top 5はheuristicである。
- Top 5外の正解候補は現行pipelineでは後段から見えない。
- candidate数を増やすと後段のLLM/search workloadが増える可能性があるが、token/latency/costの実測はまだ必要。
- LLM ranking/verificationに性能が依存する。
- specialist tools間のscoreは直接比較できる共通尺度ではない。
- facial image analysisも撮影品質、年齢、demographic representation、reference gallery/model coverageの影響を受けうる。
- expanded analysisは462 images / 368 patientsで、同一patientの異なる時点の画像が含まれるためpatient-independent evaluationではない。
- zero-shot条件は461 instancesで、1 imageがAPI content-safety policyでrejectされた。
- case-specific selectionによるfinal Recall@5改善はまだ示していない。
- 74-case benchmarkは小規模retrospective evaluationである。
- leakage/gallery overlap、repeatability、expert evaluation、citation fidelityなど未解決項目がある。
- Eye2Gene等の追加画像モダリティはfuture directionであり、現行ZebraSeekへ統合して評価した結果ではない。

## 6. 主張しないこと

- 「ZebraSeekが初めてmultimodal rare-disease diagnosisを行った」
- 「ZebraSeekが初めてtraceable reasoningを実現した」
- 「既存研究では異なるモダリティの扱いが全く研究されていない」
- 「顔画像解析は完全に客観的でbiasがない」
- 「顔画像ならHPOが不要になる」
- 「DeepRareにはtraceabilityがない」
- 「DeepRareは画像を絶対に扱えない」— published formulationでfacial imageがinputに含まれていない、と限定する。
- 「PEDIAよりZebraSeekの方が高性能／高度である」— integration mechanismの柔軟性の違いとして記述する。
- 「Top 30で89%なのでZebraSeekのaccuracyが89%」
- 「zero-shot LLMによるdepth selectionが最良」
- 「known diagnosisを使ったbest-case referenceの2.66 candidatesが実運用で達成できる」
- 「候補数が減ればtoken/latency/costが必ず減る」と実測なしで断定する。
- 「今回adaptive selectionを完成した」
- 「顔貌を使ったことが特定症例の成功原因」とablationなしで因果的に断定する。
- 「Eye2GeneをZebraSeekに統合済み」と書かない。

## 7. 用語

- **Recall@k**: 最終ranked outputの上位k件に正解が含まれる割合。
- **Candidate coverage**: 後段へ取り込むcandidate setのどこかに正解が含まれる割合。
- **Candidate availability**: integration前のcomponent candidate listsに正解が存在すること。
- **Candidate retention**: integration前に存在した正解候補がfinal shortlistにも残ること。
- **Candidate-list depth**: 各tool rankingの上位何件までを後段へ取り込むか。
- **Verification**: 取得済みcandidateをpatient findingsやexternal sourcesと照合する後段処理。
- **Traceability / source information**: candidateやevidenceがどのtool/source/URLから来たかを追跡できること。
- **Image-derived phenotype evidence**: raw imageをspecialist modelで解析して得るcandidate/score。画像自体をLLMが直接診断することとは区別する。

`coverage` を end-to-end `Recall@5` と呼ばない。`candidate count` を実測compute costと同義にしない。「objective」という語で画像解析を無批判に優位化しない。

## 8. 図表の役割

- **Fig. 1**: complementary candidate availabilityとretentionの概念。異なるmodalityが異なるcandidateを拾いうることを示す。
- **Fig. 2**: ZebraSeek workflow。specialist candidate generation → LLM integration → verification → final Top 5。顔画像はGestaltMatcher経由でcandidateへ変換される。
- **Fig. 3**: interface。clinical input、facial image、component outputs、final candidatesをreviewできることを示す。
- **Fig. 4**: 74-case benchmarkのobserved Recall@1–5。
- **Fig. 5**: successful casesにおけるcomponent overlap。補完性を示すが、各modalityのcausal effectではない。
- **Fig. 6**: 15 failuresのcandidate availability。coverage failureとretention failureを分ける。
- **Fig. 7**: expanded datasetでretrieval depthを広げたとき、後段に利用可能なcandidate setがどう変わるか。end-to-end performanceではない。
- **Table 1**: candidate selection baselinesごとのcoverageとmean candidate count。完成アルゴリズムのwinnerを示す表ではない。

## 9. セクションごとの論理

### Abstract

希少疾患診断の難しさ → HPOとfacial imageをspecialist toolsでcandidateへ変換するZebraSeek → 74-case結果 → fixed Top 5とcandidate-selection problem → traceability improvement、の順にする。顔画像はHPOを置き換えるものではなく、画像由来の補完情報と表現する。

### Introduction

rare-disease diagnostic problem → HPOとfacial imageの補完性 → facial imageのpractical/quantitative value → prior multimodal methods → PEDIAのfixed numeric fusionとLLM candidate-level integrationの違い → DeepRareのagentic integrationとpublished input modalities → heterogeneous specialist outputsをどう選択・統合するかというZebraSeekのproblem → current limitation → BioHackathon objective、の順にする。

### Results

既存74-case resultsの数値・図表は変更しない。facial evidenceの価値を説明する際も、Fig. 5のGestaltMatcher-only casesをcontrolled ablationの代わりに使わない。

### Discussion

1. ZebraSeekのcandidate-level modular integrationとfacial phenotypeの意味。
2. PEDIA等のmultimodal methodsとの違いを「fixed score fusion vs flexible candidate/evidence integration」として説明。
3. DeepRareを強いagentic/traceable prior workとして認めつつ、published formulationではfacial image inputがないことを述べる。
4. heterogeneous specialist rankingsのcandidate-selection problemをBioHackathon解析へつなぐ。
5. facial imageをfirst stepとし、Eye2Gene等のretinal imaging specialist modelsを将来的に接続する方向を述べる。
6. modalityが増えるほどcase-specific candidate/modality selection、traceability、cost measurementが重要になると結ぶ。

## 10. 編集ガードレール

- 文献由来の事実は、その記述の直後に対応するcitationを置く。
- 「簡単」「客観的」「未研究」「柔軟」といった語は絶対表現にしない。
- facial imageの利点は、`easy acquisition / reduced dependence on manual feature encoding / information beyond HPO terms`を中心にする。
- PEDIAとの比較はarchitectureの違いであり、性能比較ではない。
- DeepRareの画像非使用は`published input formulation`に限定する。
- Eye2Geneはfuture directionとして扱い、現行ZebraSeekの結果に混ぜない。
- 新しいmodalityを増やすこと自体を新規性にせず、**heterogeneous specialist outputsをcandidate levelで選択・統合・追跡する設計**を中心にする。
