# Zenodo release workflow

## 初回アップロード（手動、いちばん確実）

1. **アカウント**: https://zenodo.org → Log in（GitHub / ORCID / メールのどれでも）
2. **New Upload** → `zenodo/bb6-cryptid-frontier-v1.0.zip` をドラッグ&ドロップ
3. フォーム入力（`metadata.json` の内容を転記）:
   - Resource type: **Dataset**
   - Title: *The BB(6) Cryptid Frontier: Certified Templates, Ledger Reductions, and a Unified p-adic Return Problem*
   - Publication date: 2026-07-08 / Version: 1.0
   - Creators: **Aoki, Yosuke** — Affiliation: GeoAlpine LLC（ORCID があれば追加推奨）
   - Description: metadata.json の `description` を貼り付け
   - License: **Creative Commons Attribution 4.0**
   - Keywords: busy beaver, BB(6), halting problem, Collatz-like maps, rational base number systems,
     normality conjecture, p-adic dynamics, certified deciders, Lean 4
   - Related works: `arXiv:2510.11723` — relation: *Cites*
4. **（推奨）DOI を先に予約**: フォームの DOI 欄で "Get a DOI now" → 予約された DOI を
   `zenodo/CITATION.cff` と `README_ZENODO.md` の "Cite as" に書き込み → `build_package.py` で
   zip 再ビルド → アップロードし直し（Files 欄で差し替え）→ これで配布物自体に自分の DOI が入る
5. **Save draft → Preview で確認 → Publish**（⚠️ 公開は取り消し不能。ファイル差し替えは以後
   "New version" でのみ可能）

## 継続反映（git 更新 → Zenodo）

### 方式B（推奨・導入済み）: タグ駆動の API リリース

リポジトリを非公開のまま、**キュレーション版だけ**を新バージョンとして届ける方式。

1. 一度だけ: zenodo.org → アバター → **Applications → Personal access tokens** →
   scopes `deposit:write` + `deposit:actions` でトークン作成 → シェルに
   `export ZENODO_TOKEN=...`（**絶対にコミットしない**）
2. 一度だけ: 初回デポジットの **record id** を `zenodo/.zenodo_record_id` に書く
   （手動アップロードした場合。レコード URL `zenodo.org/records/<ID>` の数字）
3. 以後、リリースしたいタイミングで:
   ```
   git tag v1.1 && git push origin v1.1        # 任意（記録用）
   ZENODO_TOKEN=... python3 zenodo/zenodo_release.py --version 1.1
   ```
   → パッケージ再ビルド+自己完結テスト → Zenodo に新バージョンの **DRAFT** 作成。
   Web で確認して Publish（または `--publish` を付けて即公開）。
   全バージョンは **concept DOI** で束ねられ、引用は常に最新版に解決される。
4. お試しは `--sandbox`（sandbox.zenodo.org、別トークンが必要）

> 毎コミット自動ではなく**タグ = 意図的なリリース操作**に紐付けるのが安全設計
> （公開は不可逆・DOI は乱発しない）。

### 完全自動化（導入済み）: GitHub Actions on tag

`.github/workflows/zenodo-release.yml` により、**`v*` タグを push するだけ**で CI が
パッケージをビルド（自己完結テスト込み）し、Zenodo に新バージョンを作成する。

一度だけの設定（GitHub リポジトリの Settings → Secrets and variables → Actions）:
1. **Secret** `ZENODO_TOKEN` = Zenodo の personal access token（deposit:write + deposit:actions）
2. **Variable** `ZENODO_RECORD_ID` = `21252622`
3. （任意）**Variable** `ZENODO_AUTOPUBLISH` = `1` にすると Publish まで全自動
   （⚠️ 不可逆。未設定なら DRAFT 止まり = Web で確認して Publish する安全運転）

以後のリリースはこれだけ:
```
git tag v1.1 && git push origin v1.1
```

### 方式A（代替）: GitHub → Zenodo 連携

Zenodo の GitHub 連携（zenodo.org → GitHub settings で対象リポジトリを ON）を使うと、
**GitHub Release を切るたびに自動で新バージョン+DOI** が発行される。
⚠️ ただし: (1) リポジトリを **public** にする必要がある、(2) アーカイブされるのは
**リポジトリ全体のスナップショット**（キュレーション版ではない全 ~800 ファイル）。
全公開に切り替える判断をした場合のみ選択肢。現在の方針（キュレーション公開）には方式Bが適合。

> **運用メモ (2026-07-08):** v1.0.1 のテスト draft（uploads/21253229）は削除せず放置中。
> Zenodo は未公開の新バージョン draft を concept ごとに1つしか持てないため、次の
> `zenodo_release.py` 実行時は newversion が既存 draft を返す場合がある — スクリプトは
> その draft のファイルを削除してから新 zip を上げる設計なので、そのまま v1.1 として
> 使い回されて問題ない。
