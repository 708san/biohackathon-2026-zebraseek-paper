# ZebraSeek editorial checklist

最終更新: 2026-09-18

このファイルは、`paper/paper.md` に混ぜない**未確定情報・著者への確認事項・再現性TODO・投稿準備タスク**を管理します。科学的な主張の正本は `MANUSCRIPT_LOGIC.md` です。

## 管理ルール

- `paper/paper.md` には投稿原稿として読める文章だけを置く。
- 不明な事実は推測して本文に書かない。
- 未解決事項はこのチェックリストに残す。
- 解決した項目は、根拠となるcommit、file、URL、著者回答などを併記して完了扱いにする。
- 新しい実験結果が論文の主張を変える場合は、先に `MANUSCRIPT_LOGIC.md` を更新する。
- 一般的でない機械学習用語はできるだけ避け、何をしているかを具体的な言葉で書く。

## 解決済み

- [x] DBCLS BioHackathon 2026 metadata
  - event: `BH26JP`
  - name: `DBCLS BioHackathon 2026`
  - URL: `https://2026.biohackathon.org/`
  - location: `Matsuyama, Japan, 2026`
- [x] ZebraSeek implementation repositoryをCode availabilityに追加
  - `https://github.com/708san/AI_AgentWithLangGraph`
- [x] Table 1のunion記号がPDFで崩れる問題を修正
  - table labelは `PCF@5 + GM@5` のように表記
  - captionで `+` = duplicate diseasesを除いたcombined candidate listsと定義
- [x] expanded analysisのaggregate summaryをrepoに保存
  - `paper/data/adaptive_candidate_depth_summary.csv`
- [x] expanded retrieval-depth figureをrepoに保存
  - `paper/figures/expanded_candidate_depth_recall.svg`
- [x] zero-shot条件がn=461になった理由を確認
  - 462 imagesのうち1画像がAPIのcontent/safety policyにより拒否され、zero-shot LLM条件では評価できなかった。
- [x] zero-shot candidate-depth selectionのモデル設定を確認
  - GPT-5.2 API
  - reasoning effort: `medium`
  - exact promptは今回のpreprint本文には詳述しない。
- [x] expanded analysisの複数画像の意味を確認
  - 368 patientsに対して462 facial images。
  - 同一患者の複数画像は異なる時点・年齢で撮影された画像である。
  - patient-levelのphenotype annotationsは同一患者内で共通だが、facial imageと画像時点のageは異なりうる。

## A. expanded analysis of candidate-list depth

### A1. zero-shot LLM depth-selection run

- [x] n=462ではなくn=461になった1 instanceの理由を確認する。
  - 1 image-level instanceがAPI content/safety policyで拒否されたため。
- [x] zero-shot LLMのmodelを確認する。
  - GPT-5.2 API, reasoning effort `medium`。
- [ ] exact promptをrepoに保存するか決める。
  - 今回のpreprint本文では詳細promptは記載しない方針。
- [ ] 選択可能なcandidate depthを記録する。例: 0/5/10/20/30など。
- [ ] temperature、sampling、retry ruleを記録する。
  - reasoning effortは `medium` と確認済み。
- [ ] parse failure / API failure / timeout時の扱いを記録する。
- [ ] input-only conditionとinput + tool-results conditionで渡したfieldを列挙する。

### A2. image-level / patient-level definition

- [x] 368 patients / 462 imagesにおける複数画像の意味を確認する。
  - 同一patientの複数画像は異なるtime point / ageの画像。
  - phenotype annotationsは同一patient内で共通。
  - facial imageと画像時点のageはimageごとに異なりうる。
- [x] 同一patient内の複数画像の扱いをMethodsに記述する。
- [ ] patient-wise aggregationまたはseparate patient-wise test evaluationを追加するか決める。
- [ ] 54 disordersの一覧とimage/patient denominatorsを保存する。

### A3. candidate-set construction

- [ ] exact OMIM matchingのnormalization ruleを保存する。
- [ ] PCFとGMのduplicate diseaseをどのIDレベルで除いたか記録する。
- [ ] tieがある場合のrank cutoff処理を記録する。
- [ ] toolが30候補未満しか返さない場合の扱いを確認する。
- [ ] 既知の正解診断を使って最小candidate depthを求めるbest-case retrospective referenceのexact algorithmをevaluation scriptとして保存する。

## B. original 74-case benchmark

### B1. case selection / matching

- [ ] Phenopacket Store v0.1.25とGestaltMatcher Databaseのcase-matching procedureを記録する。
- [ ] source publicationとcase identifiersを保存する。
- [ ] inclusion / exclusion criteriaを記録する。
- [ ] 74 casesのpatient数とimage数の関係を確認する。
- [ ] duplicate patient / related individualの扱いを確認する。
- [ ] selection dateとGestaltMatcher Database release/versionを確認する。
- [ ] 19 disease labelsと各denominatorをcase-level dataから再確認する。

### B2. leakage / gallery overlap

- [ ] GestaltMatcher galleryからquery individualまたはduplicate imageを除外したか確認する。
- [ ] 元症例・source publicationがPubCaseFinderやverification-time searchに含まれる可能性を監査する。
- [ ] phenotype queryへdiagnosis-bearing fields、gene、variant、file name、caption等が入っていないことを確認する。

### B3. aggregate results validation

- [ ] Fig. 4の74-case Recall@1–5をcase-level outputsから再集計する。
- [ ] Fig. 5 component overlapをcase-level outputsから再集計する。
- [ ] Fig. 6 failure categoriesをcase-level outputsから再集計する。
- [ ] repeated runsがある場合はrun-to-run variabilityを記録する。
- [ ] disease normalization、synonym、subtypeの正解判定ruleを明文化する。

## C. ZebraSeek implementation / reproducibility

### C1. evaluated version

- [ ] 報告値を生成した `708san/AI_AgentWithLangGraph` のcommit SHAまたはreleaseを特定する。
- [ ] Python/environment/dependency versionsを保存する。
- [ ] PubCaseFinder endpoint/versionを記録する。
- [ ] GestaltMatcher model、endpoint、gallery versionを記録する。
- [ ] SemanticSearchのMondo release、indexed fields、embedding model、similarity ruleを記録する。
- [ ] direct LLM / ranking / verification / final-output各stageのmodel snapshotを確認する。

### C2. prompts and orchestration

- [ ] original 74-case runで使用した全promptをarchiveする。
- [ ] candidate normalization / duplicate-removal ruleを記録する。
- [ ] verification stageがnew candidateを追加できるか確認する。
- [ ] verification対象候補数とstopping ruleを記録する。
- [ ] PubMed / external search query constructionとretrieval dateを記録する。
- [ ] text truncation、error handling、retryのruleを記録する。

### C3. structured output / source tracking

- [ ] current structured-output schemaを保存する。
- [ ] stable candidate IDのfieldとvalidation ruleを記録する。
- [ ] evidence source / URL fieldのschemaを記録する。
- [ ] candidate identityがnormalization・ranking・verification・final output間でどう保持されるかをコード上で確認する。
- [ ] out-of-list candidate generationを防ぐcandidate-ID-based structured outputの評価値を、本文へ追加するか著者間で決める。
- [ ] URL existence / citation fidelity / claim supportの評価方法を決める。

## D. 各ツールから何件の候補を取るか：次の実験

- [ ] fixed-depth combinationsを系統的に比較する。
- [ ] simple rulesを比較する。
  - within-tool rank
  - score magnitude / score drop
  - rank/score shape
- [ ] patient informationやtool resultsの特徴を使うfeature-based selectionを比較する。
- [ ] 2つのselection案を直接比較するpairwise methodを使うか決める。
- [ ] 候補をさらに取るか止めるかを順番に判断する方法を比較する。
- [ ] patient-wise development/test splitを固定する。
- [ ] selection strategyの選択はdevelopment setのみで行い、test setを最終評価まで触らない。
- [ ] case-specific candidate selectionをfull ZebraSeek pipelineに接続する。
- [ ] end-to-end Recall@1/5、candidate retentionを比較する。
- [ ] input/output tokens、wall-clock latency、API calls、monetary costを実測する。

## E. Interface / deployment

- [ ] manuscriptで示したweb applicationのURL/versionを確認する。
- [ ] evaluated code commitとweb deployment versionの対応を確認する。
- [ ] benchmarkで実際に使ったinterface fieldsを確認する。
- [ ] external servicesへのdata processing、storage、retention条件を確認する。

## F. Ethics / data governance

- [ ] secondary literature-derived case evaluationについて倫理審査またはexemption determinationが必要か確認する。
- [ ] 該当する場合、institution / reference numberを記録する。
- [ ] GestaltMatcher facial imagesの利用・再利用・表示条件を確認する。
- [ ] 外部LLM/APIへ画像または臨床情報を送る場合のgovernanceを確認する。
- [ ] manuscript repoがpatient photographsを再配布していないことを維持する。

## G. Data availability / code availability

- [ ] Phenopacket Store v0.1.25 / v0.1.27のexact release linkを記録する。
- [ ] GestaltMatcher Databaseのexact access/release informationを記録する。
- [ ] 許可可能ならcase-matching manifestを公開する。
- [ ] patient-wise split manifestをrepoに追加する。
- [ ] case-level prediction/scoring recordsを公開可能な範囲で追加する。
- [ ] exact prompts、structured schemas、evaluation scriptsをrepoへ追加する。

## H. submission metadata（著者確認が必要）

- [ ] corresponding authorを確定する。
- [ ] corresponding author email / contact detailsを確定する。
- [ ] 全著者のfinal institutional addressを確認する。
- [ ] ORCIDを確認する。
- [ ] CRediT（Contributor Roles Taxonomy／著者貢献分類）statementを作成・全著者承認する。
- [ ] funding / grant identifiersを確認する。
- [ ] acknowledgementsを承認する。
- [ ] competing interests / COI（Conflict of Interest／利益相反）を全著者から確認する。
- [ ] AI-assisted draftingに関する開示が投稿先で必要か確認し、必要なら著者承認済み文言を作る。

## I. paper.mdへ戻す条件

このチェックリストの項目は、次の条件を満たした場合のみ本文へ反映する。

1. 根拠となるdata / code / author confirmationが存在する。
2. `MANUSCRIPT_LOGIC.md` の主張境界と矛盾しない。
3. editor-facing wordingではなく、読者向けのMethods / Results / metadataとして書ける。
4. 新しい主張の場合は、必要なevaluationが完了している。
