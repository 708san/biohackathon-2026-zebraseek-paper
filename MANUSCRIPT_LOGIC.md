# ZebraSeek manuscript logic

最終更新: 2026-09-19

この文書は、ZebraSeekプレプリントの科学的ストーリー、主張の境界、図表の役割、編集判断を管理する正本です。`paper/paper.md` を変更する前に確認し、未確定事項は `EDITORIAL_CHECKLIST.md` に置きます。

## 1. 一文で言うと何の研究か

ZebraSeekは、HPOで表現された臨床所見、顔画像、疾患知識などをそれぞれに適した専門ツールで疾患候補へ変換し、**candidate identity と source provenance を保ったままLLMで統合・検証するモジュール型希少疾患診断支援システム**である。

本プレプリントでは、顔画像を最終目的ではなく、HPOとは異なる情報を提供する「最初の画像モダリティ」と位置づける。元の74症例評価で相補的候補を統合する価値と候補保持の問題を示し、BioHackathon 2026では、異種の専門ツールから**どの候補を何件後段へ送るか**という効率的なcandidate selectionの問題を定量化する。

## 2. Introduction の必須ストーリー

Introductionは次の順番で読むと自然になるようにする。

1. **希少疾患診断そのものの困難**から始める。疾患が稀で多様、表現型が不完全・年齢依存・非典型であり、diagnostic odysseyが起こる。
2. **HPO-based prediction の既存基盤**を先に示す。HPOそのものに加えて、Phenomizer、PubCaseFinder、LIRICAL、Exomiserのような代表的ツールを紹介し、structured phenotypeによる候補生成・ランキングが既に重要な診断基盤であることを示す。
3. **画像はHPOとは異なるphenotype sourceである**と展開する。GestaltMatcherは顔画像、Eye2Geneは網膜画像、Bone2Geneは手X線画像を専門モデルで処理し、画像からcandidateや表現型情報を得る方向性を示す。
4. 画像の利点は「客観的だから正しい」ではなく、**manual feature recognition / verbalization / HPO encodingへの依存を減らし、定量的・機械可読な補完情報を得られること**と表現する。subtle patternやHPOだけでは十分に表現されない情報を拾える可能性を述べる一方、image quality、age、population representation、training/reference-set coverageの影響を明示する。
5. **multimodal integration自体は先行研究がある。** PhenoScore、GestaltMML、PEDIA、SHEPHERDを公平に紹介する。
6. **PEDIAは強い先行例として扱う。** image / phenotype / molecular scoresをlinear SVMで統合する。ZebraSeekとの差は「PEDIAが単純で劣る」ではない。PEDIAのfusion ruleはpredefined numeric featuresに対する固定的な線形統合であり、ZebraSeekはtoolごとに異なるcandidate identity、rank/score、patient context、negative findings、external evidenceなどをcandidate levelで扱える、より拡張可能なintegration interfaceを目指す。これはflexibilityの主張であり、accuracy superiorityの主張ではない。
7. **LLM/agentic prior workも公平に示す。** DeepRare、RareAgents、MEDDxAgentを紹介する。DeepRareは多数のtool/knowledge sourcesとsource-linked reasoningを持つ強い先行研究であり、ZebraSeekを「初のagentic / traceable system」とはしない。published formulationではfree text、HPO、genetic testing/VCFが入力で、facial photographは入力モダリティに含まれていない。
8. ここからZebraSeekの問いを定義する。新規性は「multimodalだから」ではなく、**異なるspecialist modelsのranked outputsを共通candidate levelへ写像し、sourceを保持し、どの候補をどこまで後段へ送るかまで設計対象にすること**にある。
9. current Top 5 heuristicを説明し、候補が浅すぎると正解を後段から見えなくし、深すぎるとsearch / verification / ranking対象が増えるというtrade-offへつなぐ。
10. BioHackathon 2026はこのtrade-offを調べる。fixed depth、zero-shot LLM、known-diagnosis best-case referenceは問題を理解するためのbaselineであって、baseline比較自体が研究目的ではない。

## 3. Citation placement rule

- 文献由来のtool / method / resultは、**そのtool名または対応する具体的記述の直後**にcitationを置く。
- 複数ツールを1文で並べる場合でも、各toolの直後に対応するcitationを置く。
- 例: `GestaltMML [citation] ... PEDIA [citation] ... SHEPHERD [citation] ...`
- `DeepRare [citation]`, `RareAgents [citation]`, `MEDDxAgent [citation]` のように、どのcitationがどのsystemを支えるか曖昧にしない。
- 異なる研究を説明した後、文末にまとめてcitation bundleを置く書き方は避ける。

## 4. 画像モダリティの位置づけ

### GestaltMatcher / facial phenotyping

- 顔画像は専門家がすべてのdysmorphic featuresを手でHPO化することへの依存を下げうる。
- GestaltMatcherはfacial phenotype spaceを用いたmatchingを行い、training set外のultra-rare disordersにもgeneralizationを示している。
- PEDIAはfrontal photographにclinical termsだけでは捉えきれない情報が含まれることを示した。
- ただし、74-case ZebraSeek結果だけから「顔画像が成功原因」と因果的に断定しない。GestaltMatcher-onlyで正解候補があった症例は補完性を示唆するが、controlled ablationではない。

### Eye2Gene / Bone2Gene

- Eye2Geneはretinal imagingからinherited retinal diseaseのgene-level predictionsを生成する代表例として使う。
- Bone2Geneはhand radiographsからrare bone diseaseを検出・鑑別するspecialist imaging modelの例として使う。
- これらは「ZebraSeekに既に実装済み」と書かない。**将来的にcandidate-level interfaceへ接続しうる例**として使う。
- 顔画像を「multimodal integrationの完成形」ではなく、より多面的な画像統合へ進むstarting pointとして位置づける。

## 5. ZebraSeekの価値

ZebraSeekの価値は次の3軸で一貫して説明する。

- **Effectiveness**: modality-specific specialist toolsが拾う相補的候補を統合する。
- **Traceability**: candidate ID、source tool、external source、URLを後段まで保持し、候補と根拠の由来を追えるようにする。
- **Efficiency**: 全candidateをLLM/search/verificationへ流すのではなく、患者ごとに必要なcandidateだけを後段へ送る設計を目指す。

モダリティが増えるほど3つ目のEfficiencyが重要になる。face + HPOでのcandidate-depth解析は、将来のretinal / skeletal / other specialist modalities統合に向けた最初のtractable test caseとして説明する。

## 6. 74-case benchmark の主張

- 74 cases / 19 diseases。
- ZebraSeek Recall@1 = 50/74 (67.6%)。
- ZebraSeek Recall@5 = 59/74 (79.7%)。
- PubCaseFinder Recall@5 = 53/74 (71.6%)。
- ZebraSeekはPubCaseFinder top 5外の正解を11例回収した一方、PubCaseFinderが持っていた正解を5例失った。net +6。
- ZebraSeek failure 15例のうち、8例はどのcomponent top 5にも正解なし、7例は正解候補がcomponentにあったがfinal top 5で失われた。
- component top-5 unionに正解があるのは66/74 = 89.2%。これはcandidate coverageであり、final top-5 accuracyではない。

この結果は「candidate availability」と「candidate retention」を分けて考える必要性を示す。

## 7. BioHackathon expanded analysis の主張

- Phenopacket Store v0.1.27 linked dataset: 368 patients / 462 facial images / 54 disorders。
- 同一patientの複数imageは異なるage / time pointで、patient-level phenotype annotationは共通。したがってexpanded analysisはimage-instance level。
- PCF@5 = 0.7338、PCF@10 = 0.7814、PCF@30 = 0.8355。
- PCF@5 + GM@5 = 0.7749。
- PCF@30 + GM@30 = 0.8896、mean unique candidates = 57.57。
- zero-shot LLM depth selection: GPT-5.2 API, reasoning effort medium。
  - input only: coverage 0.8438, 19.28 candidates, n=461。
  - input + tool results: coverage 0.8460, 18.18 candidates, n=461。
  - 1件少ないのは1 imageがAPI content/safety policyでrejectされたため。
- known-diagnosis retrospective minimum-depth reference: coverage 0.8896, 2.66 candidates, n=462。これは実行可能な診断法ではない。

主張は「Top 30でaccuracy 89%」ではなく、**fixed Top 5がcandidate poolを制限し、深い順位には回収可能な候補がある一方、全候補を渡すとdownstream candidate countが増える**ことである。

## 8. Cost / efficiency の境界

- candidate countはdownstream workのproxyであり、compute costそのものではない。
- PCF/GMがTop 30を1回で返す場合、accepted depthを浅くしてもupstream tool call自体は安くならない。
- 期待される削減対象はexternal retrieval、LLM verification、final ranking等の後段処理。
- token use、latency、API calls、monetary costを測定するまでは「効率が改善した」と断定しない。

## 9. Structured output の主張

- candidate decisionsをstable candidate IDで扱う。
- source tool、source fields、URLを後段まで保持する。
- free-form outputによるcandidate identity lossやsource detachmentを減らす設計である。
- URLが存在することはcitation fidelityやmedical correctnessの保証ではない。

## 10. 主張しないこと

- ZebraSeekが初のmultimodal rare-disease diagnosis systemである。
- ZebraSeekが初のtraceable / agentic diagnostic systemである。
- DeepRareにtraceabilityがない。
- image analysisが客観的でbias-freeである。
- 顔画像が特定症例の成功原因である（ablationなし）。
- PEDIAがnaive / inferiorである、またはZebraSeekの方がaccuracyで優れる。
- PEDIAが「disease relationshipを考慮しない」と一般化する。比較はfusion interfaceの違いに限定する。
- Eye2Gene / Bone2Geneが現在のZebraSeekに統合済みである。
- Top 30 candidate coverageをZebraSeek final accuracyとして扱う。
- zero-shot LLM depth selectionが最良である。
- 2.66 candidatesが実運用で達成可能である。
- candidate count減少だけでtoken / latency / cost削減を証明したとする。

## 11. Whole-manuscript audit

大きな編集では必ず `plan → edit → whole-manuscript audit → revise` を回す。最低限、Abstract、Introduction、Resultsの橋渡し、Discussionを連続して読み、以下を確認する。

1. rare-disease diagnostic problem → HPO tools → specialist imaging → multimodal fusion → LLM/candidate-level integration → ZebraSeek、の順序が自然か。
2. HPO benchmark candidates（Phenomizer、PubCaseFinder、LIRICAL、Exomiser）がIntroductionで先に紹介されているか。
3. GestaltMatcher、Eye2Gene、Bone2Geneが「specialist imaging modelsが増えている」という広いストーリーに寄与しているか。
4. PEDIAを弱く描きすぎず、fixed linear score fusionとZebraSeek candidate-level integrationの違いを正確に書いているか。
5. DeepRare、RareAgents、MEDDxAgentをfairに位置づけているか。
6. citationが対応するtool / claimの直後にあるか。
7. 74-case end-to-end Recallとexpanded candidate coverageを混同していないか。
8. BioHackathonの目的がbaseline contestではなく、efficient candidate explorationの可能性検討になっているか。
9. future outlookがfaceだけで終わらず、retinal / skeletal / other modalityへ自然につながっているか。
10. evidenceを超えたfirst / superior / objective / efficient等の断定がないか。
