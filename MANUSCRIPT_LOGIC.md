# ZebraSeek manuscript logic

最終更新: 2026-09-18

この文書は、ZebraSeekプレプリントの**科学的ストーリー、主張の境界、図表の役割、編集判断を管理する正本**です。GPT、Codex、その他の編集者は `paper/paper.md` を変更する前に必ず本ファイルを確認してください。

`paper/paper.md` には読者向けの原稿だけを置きます。未確定情報、著者への質問、再現性TODOは `EDITORIAL_CHECKLIST.md` で管理します。

## 1. 一文で言うと何の研究か

ZebraSeekは、希少疾患診断で分散している臨床表現型・顔貌・疾患知識を、それぞれに適した専門ツールから**疾患候補として取得し、候補の出所を保ったままLLMで統合・検証して、短く確認可能な鑑別リストへまとめる**モジュール型診断支援システムである。

本プレプリントでは、元の74症例評価でこの統合の有用性と候補保持の問題を示し、BioHackathon 2026ではさらに、固定Top 5というヒューリスティックが作る候補漏れと、より深く探索したときの候補数増大を調べ、**必要な候補を効率よく取得してから統合する設計の可能性**を検討する。

## 2. 背景から主張までの論理

ストーリーは必ず次の順にする。

1. **希少疾患診断そのものが難しい。** 疾患数が多く、各疾患は稀で、表現型は不完全・多様である。患者は複数の医療機関・検査を経る長い diagnostic odyssey を経験しうる。
2. **診断に使える情報は一種類ではない。** HPOで表現された臨床所見、顔貌、既報症例、疾患記述、遺伝情報などは異なる情報を持ち、単一のツールだけでは候補を取りこぼすことがある。
3. **既存研究はマルチモーダル統合の価値をすでに示している。** PhenoScore、GestaltMML、PEDIAなどは顔貌・臨床情報・遺伝情報の組合せを示し、SHEPHERDは知識グラフを用いる。したがって「複数モダリティを使うこと」自体をZebraSeekの新規性とはしない。
4. **LLM/agentic systems はさらに広い情報統合と根拠提示を可能にしている。** 特にDeepRareは多数の専門ツール・知識源を組み合わせ、検証可能な文献等に紐づく reasoning chain を提示している。したがって「traceabilityそのものが過去に存在しなかった」とは主張しない。
5. **一方、既存手法の主眼は異なる。** 表現を直接融合するmultimodal model、知識グラフモデル、広範なagentic orchestrationは存在するが、ZebraSeekが扱う実務上の問いは、異なる専門ツールが返した候補を共通の疾患候補レベルで保持し、どのツールから来たかを追跡しながら、後段で検証する候補を選んで統合することである。
6. **ZebraSeekの価値は3軸で整理する。**
   - Effectiveness: 相補的な専門ツールの候補を統合し、単独ツールでは拾いにくい候補も最終鑑別へ残す。
   - Traceability: 候補ID、候補を出したツール、外部情報源、URLを後段まで保持し、最終候補の由来を追えるようにする。
   - Efficiency: LLMによる検索・検証・ランキングに全候補を渡すのではなく、必要な候補だけを後段へ送る設計を目指す。
7. **元の74症例評価はEffectivenessの根拠である。** ZebraSeekはRecall@1 67.6%、Recall@5 79.7%。PubCaseFinder Top 5にない正解を11例回収した一方、PubCaseFinderが持っていた正解を5例失った。したがって、候補を広げる価値と、統合中に候補を失う問題の両方が存在する。
8. **現行ZebraSeekには構造的な限界がある。** 各componentからTop 5を取ることはヒューリスティックであり、Top 5より下の疾患は後段のLLMには見えない。一方、Top 30などをすべて渡せば、外部検索、LLM verification、rankingの対象が増え、token、latency、API利用等の負担が増える可能性がある。
9. **さらに、入力モダリティは共通表現として直接比較できない。** PubCaseFinderはHPO、GestaltMatcherは顔画像を扱い、scoreの意味も異なる。現状で共通に扱える主要な単位は `disease candidate + within-tool rank/score + source information` である。
10. **LLMの推論能力だけに依存して解決できない。** LLMは候補統合・検証に有用だが、候補集合に存在しない疾患を選ぶことはできず、候補数を増やすほど推論・検索の負担も大きくなる。したがって、LLMを強くするだけでなく、LLMに渡す候補集合を設計する必要がある。
11. **BioHackathon 2026の主眼はここにある。** Top 5でどの程度候補が漏れるのか、何位まで見るとcoverageが増えるのか、候補数がどの程度増えるのかを拡張データで確認し、症例ごとに必要な候補だけを取得する設計が有用かを検討する。
12. fixed depth、zero-shot LLM、既知の正解診断を使うbest-case retrospective referenceは、**この問題を理解するための最初のbaseline**であり、比較自体が研究目的ではない。
13. structured outputの強化は別軸のhackathon contributionであり、candidate IDとsource URLを保持して、ZebraSeekのtraceabilityを改善する。

## 3. 既存研究との位置づけ

### Multimodal phenotype models

PhenoScore、GestaltMML、PEDIAなどは、顔貌・HPO・臨床テキスト・遺伝情報などを組み合わせる価値を示している。これらはZebraSeekの競合であると同時に、multimodal rare-disease diagnosisの先行研究である。

本文では「既にあるのでZebraSeekに新規性がない」という書き方をしない。代わりに、**既存研究が何を可能にし、ZebraSeekがどの別の設計課題に焦点を当てるか**を説明する。

### Agentic / LLM systems

DeepRareはHPO、遺伝情報、専門診断ツール、文献・疾患DB等を広く統合し、検証可能なsourceに紐づくreasoningを提示する。DeepRareはtraceable reasoningの強い先行研究であり、「ZebraSeekが初めて根拠追跡を行う」とは書かない。

一方、DeepRareの主眼は広範なagentic orchestrationとself-reflective diagnosisであり、その論文自体も、phenotype informationをaggregateに扱う現在のknowledge searchから、よりrefined/adaptiveなretrievalへの拡張をfuture workとして挙げている。ZebraSeekのBioHackathon解析は、**modality-specific specialist rankingsから何件の候補を後段へ送るか**という、より限定された実装上の問題を定量化する。

MEDDxAgentなどもexplainable/interactive diagnosisを扱うため、ZebraSeekの価値は「explainable AIそのもの」ではなく、**専門ツールのcandidate provenanceを保つcandidate-level integrationと、その候補集合を効率よく構成する設計**として表現する。

## 4. 今回のContribution

### Contribution A — ZebraSeekのcandidate-level multimodal integration

- HPO、顔画像などを専門ツールで疾患候補へ変換する。
- 候補ごとにsource tool、rank/score等を保持してLLMへ渡す。
- 外部情報と照合してTop 5と説明を生成する。
- raw multimodal inputsを単一モデルに直接融合するのではなく、specialist outputsを共通のdisease-candidate levelで統合する。

### Contribution B — 74症例での統合性能とfailure decomposition

- Recall@1: 50/74 (67.6%)。
- Recall@5: 59/74 (79.7%)。
- PubCaseFinder Top 5外から11例を回収し、PubCaseFinderが持っていた5例を失った。
- candidate availabilityとcandidate retentionを分けて考える必要性を示す。

### Contribution C — fixed Top 5の限界を拡張データで調べる

- Phenopacket Store v0.1.27 linked dataset: 368 patients / 462 images / 54 disorders。
- PCF/GMのdepthを広げるとcandidate coverageが上がる一方、後段へ渡るunique candidatesも増える。
- Fig. 7の主張は「Top 30で89%」ではなく、**Top 5という固定値がcandidate poolを制約しており、より深い順位に回収可能な候補が存在する**ことである。

### Contribution D — 効率的な候補取得の可能性を検討する基礎評価

- fixed-depth conditions、zero-shot LLMによる症例別depth selection、known diagnosisを使うbest-case retrospective referenceを比較する。
- 目的はwinnerを決めることではなく、coverageとcandidate countの関係を確認し、症例別に候補数を変える余地を測ること。
- 最終的なcase-specific selection methodやend-to-end speed-upは今後の検証対象。

### Contribution E — structured outputによるsource traceability改善

- stable candidate IDで候補を扱う。
- source tool、evidence source、URLをstructured fieldsとして保持する。
- out-of-list disease generationやnormalization lossを抑える方向に設計する。
- URL保持はcitation correctnessやmedical validityを自動的に保証しない。

## 5. 現状の限界として明示すること

- fixed Top 5はheuristicである。
- Top 5外の正解候補は現行pipelineでは後段から見えない。
- candidate数を増やすと後段のLLM/search workloadが増える可能性があるが、token/latency/costの実測はまだ必要。
- LLM ranking/verificationに性能が依存する。
- specialist tools間のscoreは直接比較できる共通尺度ではない。
- expanded analysisは462 images / 368 patientsで、patient-independent evaluationではない。
- zero-shot条件は461 instancesであり、1件少ない理由は要確認。
- adaptive/case-specific selectionによるfinal Recall@5改善はまだ示していない。
- 74-case benchmarkは小規模retrospective evaluationである。
- leakage/gallery overlap、repeatability、expert evaluation、citation fidelityなど未解決項目がある。

## 6. 主張しないこと

- 「ZebraSeekが初めてmultimodal rare-disease diagnosisを行った」
- 「ZebraSeekが初めてtraceable reasoningを実現した」
- 「DeepRareにはtraceabilityがない」
- 「Top 30で89%なのでZebraSeekのaccuracyが89%」
- 「zero-shot LLMによるdepth selectionが最良」
- 「known diagnosisを使ったbest-case referenceの2.66 candidatesが実運用で達成できる」
- 「候補数が減ればtoken/latency/costが必ず減る」と実測なしで断定する
- 「今回adaptive selectionを完成した」
- 「顔貌を使ったことが特定症例の成功原因」とablationなしで因果的に断定する

## 7. 用語

- **Recall@k**: 最終ranked outputの上位k件に正解が含まれる割合。
- **Candidate coverage**: 後段へ取り込むcandidate setのどこかに正解が含まれる割合。
- **Candidate availability**: 統合前のcomponent candidate listsに正解が存在すること。
- **Candidate retention**: 統合前に存在した正解がfinal shortlistにも残ること。
- **Candidate-list depth**: 各tool rankingの上位何件までを後段へ取り込むか。
- **Traceability / source information**: 候補・根拠がどのtool/source/URLから来たか追跡できること。
- **Verification**: 取得済み候補を患者所見・外部医学情報と照合する後段処理。

`candidate coverage` と end-to-end `Recall@5` を混同しない。candidate countと実測compute costを混同しない。

## 8. 図表の役割

PDF構造は原則維持する。

- Fig. 1: complementary candidate availabilityとretention。
- Fig. 2: ZebraSeek workflow。specialist tools → candidate-level integration → external-information verification → final Top 5。
- Fig. 3: interfaceとreviewability。
- Fig. 4: 74-case observed Recall@1–5。
- Fig. 5: 59 successful casesのcomponent overlap。
- Fig. 6: 15 failuresにおけるcoverage failure / retention failure。
- Fig. 7: deeper tool rankingsに回収可能候補があること。end-to-end performanceではない。
- Table 1: coverageと後段へ渡すcandidate countの関係を見るbaseline table。

## 9. セクションごとの論理

### Abstract

rare-disease diagnostic problem → ZebraSeek value → 74-case result → current fixed-depth/LLM limitation → BHで効率的candidate explorationの可能性を検討 → structured output/source tracking改善、の順。

### Introduction

1. diagnostic odysseyとrare-disease diagnosisの難しさ。
2. phenotype/facial/genetic/knowledge informationの補完性。
3. multimodal prior workが示した価値。
4. DeepRare等のagentic/traceable work。
5. それでも残る「specialist candidate outputsをどう選択・統合・追跡するか」という設計課題。
6. ZebraSeek overview/value。
7. current limitations: heuristic Top 5、LLM workload/reasoning dependence、non-comparable tool scores。
8. BH2026 objective。

### Results

元のFig. 1–6と74-case storyを主役として維持し、その後にFig. 7/Table 1でcandidate-list depthの問題とbaseline analysisを追加する。

### Discussion

1. ZebraSeekのvalueをEffectiveness / Traceability / Efficiencyの3軸で再提示。
2. 74-caseから得たintegrative benefitとretention problem。
3. fixed Top 5というupstream limitation。
4. BH baselineが示すcase-specific selectionの余地。
5. prior workとの差は「multimodal/traceableの初出」ではなくcandidate-level modular integration + selective downstream processing。
6. limitations。
7. future work: full pipelineでRecall/token/time/cost/source fidelityを測る。

## 10. 編集ループ

原稿編集は一回書いて終わりにしない。以下を最低2回繰り返す。

### Step 1: Plan

- 今回の編集目的を1–3文で定義する。
- 変更するsectionと、変えてはいけないfigure/resultを確認する。
- 新しい事実主張はprimary sourceで確認する。

### Step 2: Edit

- `MANUSCRIPT_LOGIC.md` を先に更新する。
- `paper/paper.md` を読者向け文章として編集する。
- 不明事項は `EDITORIAL_CHECKLIST.md` へ移し、本文にTODOを書かない。

### Step 3: Whole-manuscript audit

Abstract → Introduction → Results → Discussionを通読し、以下を確認する。

1. 背景からZebraSeekが必要になる理由が自然につながるか。
2. ZebraSeekのvalueがEffectiveness / Traceability / Efficiencyとして説明できるか。
3. prior workを過小評価したり、誤ったfirst claimをしていないか。
4. BH analysisが「baseline比較が目的」に見えず、効率的candidate explorationを検討するための基礎評価になっているか。
5. 74-case resultsとexpanded coverage analysisを混同していないか。
6. limitationが本文の主張と対応しているか。
7. editor-facing text/TODOがpaperに混ざっていないか。

### Step 4: Revise

監査で見つかった問題を修正し、再度Step 3を行う。変更後もPDFのsection order、Fig. 1–7、Table 1の構造を壊さない。
