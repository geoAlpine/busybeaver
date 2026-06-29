# BB(6) 構造的限界定理 (Result B) — 完成インデックス（2026-06-29）

**(B) は完成（record/preprint grade）。** BB(6) Collatz frontier が encode する数学を完全分類し、
「個別 cryptid がなぜ構造的に解けないか」を厳密化した、cryptid を解かずに成立する独立成果。

## 投稿可能な2本（submission/record grade）
- **`PAPER_MAIN.md`** — 還元 + barrier + kernel 配置。Thm1 厳密還元（in-scope 4: Antihydra=**[PROVEN] outright**,
  o10-inner/o18/o15）/ Thm2 induced-map exact Haar Bernoulli / Thm3 Antihydra density β=+1/2 ergodic-opt barrier /
  §6 AEV 1.6 fragment + floor-mirror conjugacy bridge / Thm5 nested-Collatz Blocking。citation 全 pin。
- **`PAPER_HIERARCHY.md`** — 予想非依存の5階層 certification-complexity hierarchy（star-free⊊REG⊊SLIN⊊2-automatic⊊CF⊊CS）、
  各 witness TM + full proof、certificate floor m*=2(o18)/m*=8(o17)、spoofer meta + [OPEN] cryptid top。

## 支える PROVEN 結果（証拠 doc）
- `TM_EXTRACTION_PROOFS.md` — Antihydra raw TM → c'=⌊3c/2⌋ + halt 基準の FULL hand-proof（[PROVEN]）。
- `FLOOR_MIRROR_CONJECTURE.md` — floor ≡ ceiling（Tc=R∘Tf∘R, R(x)=−x）[PROVEN] bridge、floor cryptid を AEV 1.6(3/2) 下に統一。
- `NESTED_COLLATZ_STRUCTURE.md` + `NESTED_COLLATZ_THEOREM.md` — Axis-2 第2構造（9機械）と conditional theorem（halt⟺BC-over-restarts）。
- `O18_EXTRACTION_PROOF.md` — o18 unconditional macro-map [DISPROVEN]（epoch 7 で破れ）、Antihydra が unique flagship である構造的理由。
- `MAHLER_3_2_DOMINANCE.md` — 依存マップ（AEV 3/2 → 10/17、full AEV → 15/17）。
- `CITATIONS.md` — pinned reference 一覧。
- `BB6_STRUCTURAL_LIMIT_THEOREM.md` — 全体統合（両 paper の親 doc）。

## two-axis frontier カタログ（17機械、structureless 残渣ゼロ）
| class | 機械 | kernel |
|---|---|---|
| **Axis-1 in-scope（4）** | Antihydra(β>0), o10-inner, o18, o15 | 単一軌道 AEV |
| **Axis-2 nested-Collatz（9）** | o2,o7,o8,o10-full,o11,o12,o13,o14,o16 | AEV + BC-over-restarts |
| **odometer（2）** | o3, o17 | kernel-less, Collatz-irregular |
| **他 base（含）** | o4,o5=4/3; o15,o18=8/3; SN=5/2 | AEV q=3 / 5/2 |

4 multiplier {3/2,5/2,4/3,8/3}、全て v_p(μ)=−1 expanding-kernel。3/2 が支配（10/17）。

## (B) の唯一の [OPEN]（B 自身の境界、A とは別軸）
- 「cryptid に REG certificate なし」= over-approximation 軸の top（floor m*=2,8 は PROVEN、REG 頂点は [OPEN]）。

## 残り（非数学・record stance に整合）
- author block / ORCID（[[reference_orcid]] 認証待ち、公開前に確認）
- repo filename 参照を公開版では ancillary note に（記録版では不要）
- 既知の外部依存2件を honest disclose 済（CF⊊CS=Pálvölgyi 1901.03913 / Conze-Guivarc'h unpublished）

**結論: (B) DONE（record-grade）。以後は (A)=(K)=Mahler 3/2 に全力。**
