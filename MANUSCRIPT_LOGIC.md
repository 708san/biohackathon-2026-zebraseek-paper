# ZebraSeek manuscript logic

最終更新: 2026-09-18

この文書は、ZebraSeekプレプリントの**科学的な論理・主張の境界・図表の役割を管理する正本**です。GPT、Codex、その他の編集者が `paper/paper.md` を変更する前に、まずこの文書を確認してください。新しい結果によって論理が変わる場合は、本文を先に場当たり的に書き換えるのではなく、まず本ファイルの論理を更新します。

`paper/paper.md` は投稿原稿だけを置く場所です。TODO、編集メモ、著者への質問、未確定情報は `EDITORIAL_CHECKLIST.md` で管理します。`DRAFT_NOTES.md` と `SCIENTIFIC_RATIONALE.md` は過去の検討過程と文献調査を残す参考資料であり、2026-09-18以降の主張管理では本ファイルを優先します。

## 1. このプレプリントの中心となるストーリー

ZebraSeekの中心的な価値は、単に「顔画像とHPOをLLMに入れる」ことではありません。異なる種類の患者情報を扱う専門ツールが返す疾患候補を、LLM（Large Language Model／大規模言語モデル）による統合と外部情報による検証につなぎ、**短く、確認可能で、出所を追跡できる鑑別候補**として提示するモジュール型ワークフローであることです。

論理は次の順でつなぎます。

1. 希少疾患では、HPOで表現された臨床所見、顔貌、疾患記述などが同じ疾患を同じ強さで支持するとは限らない。
2. ZebraSeekは、PubCaseFinder、GestaltMatcher、SemanticSearch、direct LLM predictionなど、異なる役割を持つ候補生成ツールを利用する。
3. 元の74症例評価では、複数の候補源を統合した最終Top 5が単一コンポーネントより高いobserved recallを示した。同時に、正解候補を新たに回収するケースと、入力候補に存在した正解を統合中に失うケースの両方が存在した。
4. したがってZebraSeekの性能は、少なくとも **candidate availability（候補が統合前に存在するか）** と **candidate retention（存在した候補を最終候補まで保持できるか）** に分けて考える必要がある。
5. 現行アーキテクチャにはさらに上流の制約がある。各ツールからTop 5だけを受け取るため、Top 5より下に正解疾患があっても、後段のLLM推論・検証はそれを救えない。
6. DBCLS BioHackathon 2026では、この**固定Top 5による候補漏れ**を現実的な問題として調べる。目的は「Top 30で何%だった」という数字自体を主張することではなく、Top 5による漏れがどの程度あり、より深い順位まで見るとcoverageがどの程度増え、その代わり後段に渡す候補数がどれだけ増えるかを定量化することである。
7. 深い順位の候補をすべて後段へ渡すと、外部検索、LLMによる検証、最終ランキングで処理する疾患数が増える。したがって、症例ごとに各ツールから**何件の候補を取るか**を決める必要がある。
8. 今回の固定深度、zero-shot LLMによる深度選択、既知の正解診断を使ったbest-case retrospective referenceは、この問題設定の基本的な検証・ベースラインであり、完成した症例別選択法ではない。
9. 同時にstructured outputを強化し、candidate ID、出所、URLなどのsource informationを後段まで保持することで、ZebraSeek本来のtraceability（追跡可能性）を強化した。

## 2. 今回のContributionとして主張すること

### Contribution A — 元のZebraSeekの設計と74症例評価

- 顔画像、HPOなど異なる入力を、それぞれの専門ツールを介して疾患候補に変換し、LLMで統合・検証する。
- 74 literature-derived cases / 19 diseasesで、ZebraSeekはRecall@1 50/74 (67.6%)、Recall@5 59/74 (79.7%)を示した。
- PubCaseFinderのTop 5にない正解を11例回収した一方、PubCaseFinderが持っていた正解を5例失った。
- 「候補を広げること」と「候補を保持すること」を分けて解析できることが重要である。

### Contribution B — 固定Top 5による候補漏れの定量化

- 現行ZebraSeekでは各componentのTop 5のみが統合対象であり、それより下の疾患は後段推論から見えない。
- Phenopacket Store v0.1.27を用いた拡張解析（368 patients / 462 images / 54 disorders）で、PCFとGMのランキング深度を変え、候補集合のcoverageがどのように変化するかを調べた。
- Fig. 7の意味は「Top 30で89.0%」そのものではなく、**Top 5とより深いランキングで、後段統合に利用できる候補集合が実質的に変わる**ことを示す点にある。

### Contribution C — 各ツールから何件の候補を取るかという基本検証

- PCF@30 + GM@30をすべて使うとcoverageは高いが、平均57.57 unique candidatesを後段へ渡す。
- 固定した深度、zero-shot LLMによる症例別の深度選択、既知の正解診断を使ったbest-case retrospective referenceを比較し、coverageと候補数が選び方によって大きく変わることを確認する。
- best-case retrospective referenceは正解ラベルを使うため、実行可能な診断手法でも目標性能でもない。**理想的に選べた場合に、候補数をどこまで減らせる可能性があるか**を測るためだけに使う。
- zero-shot LLMはpreliminary baselineであり、優位性・最適性を主張しない。

### Contribution D — 出所を保持するstructured output

- candidate identityを自由文の疾患名生成に依存させず、stable candidate IDで扱う。
- candidate source、evidence source、URLなどをstructured outputに保持する。
- これはtraceabilityを強くする実装上のContributionである。
- URLを保持したことだけでは、引用が実在する、主張を支持する、医学的に正しい、ということまでは証明しない。

## 3. このプレプリントで主張しないこと

以下は本文で断定しない。

- 「Top 30で89%なのでZebraSeekが89%の診断精度を達成した」
- 「候補深度を選ぶ数式化そのものが新規アルゴリズムである」
- 「zero-shot LLMが最良の候補選択法である」
- 「既知の正解診断を使ったbest-case referenceの平均2.66 candidatesが実際に達成可能である」
- 「症例ごとに候補数を変えることで、最終ZebraSeek Recall@5が改善した」
- 「候補数が少ないので実際のtoken、latency、API costが減った」と、実測なしで断定すること
- 「4ツールは4つの独立した証拠源である」
- 「顔画像を使ったために特定症例が診断できた」と、顔画像なしの対照比較なしで因果的に主張すること
- 臨床的有用性、分子診断yield、患者アウトカム、equitable performanceを確立したという主張

## 4. 問題設定の重要な制約

ZebraSeekは異なる種類の入力を1つの**直接比較できる共通スコア**で扱っているわけではありません。

- PubCaseFinder: 主にHPO / clinical phenotype
- GestaltMatcher: facial image
- SemanticSearch: phenotype informationとdisease-description embedding
- direct LLM: HPO + sexなど

各ツールのscoreの意味・分布・尺度は異なり、PCF scoreとGM scoreをそのまま同じ閾値で比較できるとは仮定しません。したがって、この段階で共通して扱える主な単位は、**disease candidate + within-tool rank/score + source metadata**です。

また、PCFやGMがTop 30を1回の実行で返す場合、採用する件数を少なくしてもupstream tool自体の実行時間は必ずしも減りません。現在想定する効率化は、主に後段のexternal evidence retrieval、LLM verification、final rankingへ渡す候補数の削減です。

## 5. 用語を混同しない

- **Recall@k**: 最終的なranked outputの上位k件に正解が含まれる割合。
- **Candidate coverage**: 最終順位とは別に、後段へ取り込んだcandidate setのどこかに正解が含まれる割合。
- **Candidate availability**: 統合前のcomponent candidate listsに正解が存在すること。
- **Candidate retention**: 統合前に存在した正解候補がfinal shortlistにも残ること。
- **Candidate-list depth**: 各component rankingの上位何件までを後段へ取り込むか。
- **Verification**: 取得済み候補を患者所見や外部情報と照合する後段処理。
- **Traceability / source information**: 候補がどのツール・情報源・URLから来たかを追跡できること。

`coverage` を end-to-end `Recall@5` と呼ばない。`candidate count` を実測compute costと同義にしない。

## 6. 図表の役割

現在のPDFの図表構造は維持する。

- **Fig. 1**: complementary candidate availabilityとretentionという概念を示す。確率や独立性は主張しない。
- **Fig. 2**: ZebraSeek workflow。specialist candidate generation → LLM integration → verification → final Top 5。
- **Fig. 3**: interface。入力・component output・最終候補をreviewできる構成を示す。
- **Fig. 4**: 元の74-case benchmarkにおけるobserved Recall@1–5。
- **Fig. 5**: 59 successful casesにおけるcomponent overlap。補完性を示すが、各modalityの因果効果ではない。
- **Fig. 6**: 15 failuresのcandidate availability。coverage failureとretention failureを分ける。
- **Fig. 7**: expanded datasetでretrieval depthを広げたとき、後段に利用可能なcandidate setがどう変わるかを示す。end-to-end performanceではない。
- **Table 1**: 各ツールから何件の候補を取るかというstrategyごとのcoverageとcandidate countの基本比較。`+` は重複疾患を除いたunionを意味し、加算ではない。

## 7. セクションごとの論理

### Introduction

背景 → specialist tools / multimodal prior work → ZebraSeekのcandidate-level integration → 異なるツールのscoreを直接比較できない制約 → fixed Top 5の限界 → BioHackathon 2026で「各ツールから何件取るか」を調べた、という順にする。

### Results 1–6

元のZebraSeekの結果を主役として維持する。74症例のobserved performance、補完性、candidate availability/retentionの流れを崩さない。

### Results 7

fixed Top 5では後段に届かない正解候補が存在することをexpanded analysisで可視化する。Fig. 7はここで使う。

### Results 8

候補を深く取りすぎると後段へ渡す候補数が増えるため、基本的なselection strategiesを比較する。Table 1は完成アルゴリズムの勝者決定ではなく、問題が実際に存在し、選び方によってcoverageと候補数が変わることを示す。

### Results 9

structured outputによるcandidate identity / source URL / source information保持を説明する。診断coverageとは別軸の実装Contributionとして扱う。

### Discussion

元のZebraSeekの成果 → fixed Top 5による候補漏れ → coverageと候補数のtrade-off → basic baselineの意味 → source traceability改善 → limitation → future work、の順にする。

### Online Methods

問題設定・評価条件・既知の実装事実だけを書く。未確定事項や「後で調べること」は本文に書かず、`EDITORIAL_CHECKLIST.md`へ移す。

## 8. 今回ハッカソンで実施したこと / これから行うこと

### 実施したこと

- Phenopacket Store v0.1.27に評価範囲を拡張。
- PCF / GMについて、どの順位まで候補を見るかとcandidate coverageの関係を解析。
- 固定した候補深度ごとのcoverageとunique candidate countを算出。
- zero-shot LLMに症例ごとの候補深度を選ばせる基本条件を実行。
- 既知の正解診断を使ったbest-case retrospective referenceで、理想的に選べた場合に候補数をどこまで減らせる可能性があるかを確認。
- candidate IDベースのstructured outputとsource URL保持を強化。

### 今後行うこと

- 固定深度の全条件とsimple heuristicを整理する。
- tool内のrank、scoreの大きさ、scoreの落ち方などを使う単純な選択法を比較する。
- patient informationやtool resultの特徴を使うfeature-based selectionを比較する。
- 候補をさらに取るか止めるかを順番に判断する方法を検討する。
- patient-wise development/test splitでselection strategyの選択と最終評価を分離する。
- 症例ごとの候補選択をZebraSeek full pipelineへ入れ、最終Recall@5、candidate retention、token、latency、API calls、monetary costを測る。
- source URLやcitationが実際に主張を支持しているかを専門家評価する。

## 9. GPT / editor向け編集ルール

1. `paper/paper.md` にTODO、編集者への質問、未確定事項、作業指示を書かない。
2. 不明な事実は推測で埋めず、`EDITORIAL_CHECKLIST.md` に移す。
3. 新しい結果を追加するときは、その数値が「system performance」「candidate coverage」「既知の正解診断を使ったbest-case reference」のどれかを明示する。
4. 元の74-case resultsとFigs. 1–6のストーリーを、明確な理由なしに削除・弱体化しない。
5. Fig. 7 / Table 1をZebraSeek final performanceとして扱わない。
6. 新しいselection strategyが出ても、別のtest setでの評価なしに「improved」「optimal」「superior」と断定しない。
7. traceabilityとexplanation correctnessを区別する。
8. 原稿の見出し・図表順などPDF構造を変更する場合は、変更目的を明示して著者確認を取る。
9. 読者が機械学習の専門用語を知っている前提にしない。`oracle`、`headroom`、`candidate burden`、`gating`、`policy`のような語は、通常の英語で具体的に何をしているか書ける場合は使わない。
10. 専門用語が必要な場合は、初出で意味を説明する。新しい略語は、繰り返し使用して可読性が上がる場合だけ導入する。
