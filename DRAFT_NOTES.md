# ZebraSeek 初稿メモ

作成日：2026-09-11。研究を再実行した原稿ではなく、提供された要旨・発表資料・集計図から作成した英語初稿です。元のPan-Asian論文には変更を加えていません。

## 著者と投稿形式

- 筆頭は **Naoya Yoshikuwa**、最終著者は **Toyofumi Fujiwara**。添付の英語著者一覧からFujiwaraのみ末尾へ移し、その他の相対的な順序と所属番号を維持しています。
- Yoshikuwaの英語表記は提供された `ZebraSeek_authors_affiliations_en.md` に従いました。全員の氏名・所属の正式表記、所在地・国、ORCID、最終著者順は投稿前に確認してください。
- Corresponding author、CRediT貢献、助成金、利益相反は未確定です。先頭・末尾の著者という理由で役割を推定していません。
- Nature Geneticsの[Article案内](https://www.nature.com/ng/content)を2026-09-11に確認：Abstract 150語以内、本文4,000語以内、図表8点以内。見出しなしのIntroduction、Results、Discussion、Online Methodsで構成。
- AbstractはYAMLの `abstract: |` にあります。独立したConclusion節を設けず、Discussion最終段落に結論を置きました。
- PDFはBioHackrXivの書式・引用スタイルを保持しています。Nature Geneticsの組版を再現したものではありません。
- BioHackrXivのevent、会場・開催地・イベントURLは資料から確定できないためTODOです。repo名の2026だけからイベントを推測していません。
- `date` は初稿作成日です。PDFの標準欄に表示されるSubmitted/Published byは生成器の書式であり、実際の投稿・受理を意味しません。

## 使用した研究資料

| 資料 | 初稿に反映した内容 |
| --- | --- |
| `ZebraSeek_修士論文要旨.pdf`、2ページ | 入力、4ツール、LLM統合・検証、74症例、主要成績、成功・失敗内訳、先行文献 |
| `ZebraSeek_中間発表.pdf`、19ページ | SemanticSearchのMondo利用（p.9）、候補の順位・スコアと明示的陰性所見（p.11）、19疾患と症例対応付け（p.12）、失敗2疾患のラベル（p.16） |
| `ZebraSeek_authors_affiliations_en.md` | 11著者と7所属。ユーザー指定に従ってFujiwaraを最終著者へ移動 |
| `image (1).png` | 各手法のRecall@1〜5 |
| `image (2).png` | ZebraSeek成功59例の排他的なツール組合せと件数 |
| `image (3).png` | ZebraSeek失敗15例の内訳 |

元資料のハッシュは `paper/data/source_provenance.json` に記録しました。元PDFや日本語スライド自体は新repoに複製せず、英語本文と図を作成しています。図1は資料の構成図から作った模式図、図2〜4は集計値の描き直しです。患者写真、スライドの他論文由来の図、ロゴは転載していません。

## 数値の確認

| 手法 | Top 1 | Top 2 | Top 3 | Top 4 | Top 5 |
| --- | --- | --- | --- | --- | --- |
| PubCaseFinder | 47 | 49 | 52 | 52 | 53 |
| SemanticSearch | 14 | 18 | 19 | 25 | 25 |
| LLM (GPT-5.2) | 14 | 22 | 24 | 24 | 26 |
| GestaltMatcher | 23 | 30 | 33 | 36 | 37 |
| ZebraSeek | 50 | 53 | 55 | 57 | 59 |

分母はすべて74です。上表は図中の小数1桁の割合から一意に復元した整数で、生データから再集計した値ではありません。とくに中間順位の件数はcase-level出力との照合が必要です。

- 成功59例内のツール別正解数は48/25/26/35。これは全74例での成績とは異なります。
- 失敗15例は「全ツールなし8」「PubCaseFinderのみ5」「GestaltMatcherのみ2」。成功群と合算すると全体のTop 5件数53/25/26/37と一致します。
- PubCaseFinderとのdiscordanceはZebraSeekのみ成功11例、PubCaseFinderのみ成功5例。純増は6例＝8.1 percentage pointsです。
- 全構成ツールの候補の和集合に正解があるのは66/74＝89.2%。最大20候補を許す集計なので、Top 5の対照手法や実際に達成した精度としては扱いません。
- 失敗15例が2疾患に集中する点は発表資料の記述に従います。OMIM:618164が10例、OMIM:618505が5例。各疾患の全症例数・病名表記・評価時の同義語対応は要確認です。
- P値、信頼区間、複数回実行のばらつき、顔画像の因果的寄与は追加していません。

## 優先して埋める情報

1. **評価データと正解判定**：74例の対応表、疾患別件数、同一患者・同一家系、画像数、診断ラベルの根拠、同義語・疾患群・サブタイプの扱い。
2. **情報重複の確認**：顔画像の照合先から本人・重複画像を除外したか、元症例がPubCaseFinder等の資源や検証時の検索結果に入るか、ラベルを含むファイル名・caption等を除去したか。
3. **再現可能な実装**：ZebraSeekの実装repo/commit、HPO・Mondo・各DB/モデルのversion、GPT-5.2の正確なsnapshotと設定、全プロンプト、embeddingモデル、検索・再検証のルール、候補の追加可否と重複処理。
4. **次の解析**：同条件での顔画像なしablation、単純な順位統合との比較、統合・検証各段階のablation、疾患別評価、反復実行と対応のある比較、独立データでの評価、説明・引用の専門家評価。
5. **投稿の必須情報**：倫理審査または免除、顔画像の利用・外部サービス処理条件、Data/Code availability、著者貢献、利益相反、助成金、責任著者、BioHackrXivイベント情報。

Nature Geneticsを目標とする場合の研究拡張事項も含みますが、実施済みとは書いていません。現段階で主張できる中心は「74例における観察された候補順位の改善と、候補coverage/retentionの失敗分析」です。

## 引用文献

7件のDOIと書誌情報を一次論文・DOI/Crossref配信で確認しています。GMDB2024はResearch Squareの2024年version 1（preprint）として明記。発表資料が指す版・データリリースは別途確認してください。Mondo論文は2025年online publicationですが、現行の巻号は2026年なのでBibTeXはMondo2026としています。DeepRareとの数値の直接比較はしていません。

## 次回の編集方法

本文・著者・Abstractは `paper/paper.md`、文献は `paper/paper.bib`、図の数値は `paper/data/aggregate_results.json` で編集します。図の数値変更後に `python scripts/make_figures.py` を実行して図を更新します。`main` にpushするとBioHackrXiv PDFを再生成します。生成されたPDFだけを直接編集しないでください。
