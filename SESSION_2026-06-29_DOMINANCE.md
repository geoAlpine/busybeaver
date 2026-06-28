# Mahler 3/2 支配の定量化 + L²-flattening 閉（2026-06-29）

「BB6 core ≈ Mahler 3/2」を厳密定量化（U2）し、唯一の speculative frontier（quenched L²-flattening）を probe（U3）。
**結果: 依存マップ確定（AEV 3/2 が 10/17≈59% を支配）、ただし「1予想⇒全10決定」は over-claim と訂正、L²-flattening は新 [PROVEN] 理由で閉。
誤証明ゼロ・decision なし。**（o3/o17 odometer 最終特徴付けは本ターン未実行＝前ターンで却下。）

## U2 Mahler 3/2 支配の定量化（`MAHLER_3_2_DOMINANCE.md`）

### 健全性訂正: μ=3/2 は 10 機械（9 でない）
CATALOGUE_IRREGULAR が o2 を落として「9」、BB6_STRUCTURAL §7.2 は o2 込みで 10。正しくは **10**:
Antihydra, o2, o7, o8, o10-inner, o11, o12, o13, o14, o16。総数 = 10(3/2)+1(5/2)+2(8/3)+2(4/3)+2(odometer)=**17**。

### per-machine kernel（10 機械）
全て map T_{3/2}=⌊3x/2⌋（floor）を共有、**例外 o10-inner は literal AEV ceiling ⌈3m/2⌉**、seed は相異。
**exact halt 還元を持つのは2体のみ（Antihydra density k=2 一方向 floor-mirror、o10-inner）**、他8体は **multiplier を pin するだけで exact 2^k predicate は [OPEN]**（in-family but not in-scope）。

### 「AEV 1.6(3/2) ⇒ 全10決定」は clean な valid implication でない（3 gap）
1. **ceiling vs floor**: AEV は ⌈3x/2⌉、9体は floor (3c−1)/2（parity-flip, 非 conjugate）→ **floor-mirror analog（formally 別予想）**が必要。o10-inner のみ literal ceiling。
2. **in-scope vs in-family**: 8体の exact halt predicate が [OPEN]（未導出）→ AEV はまだ formally に decide せず。
3. **density vs existence facet**: Antihydra の density kernel は qualitative AEV に **over-implied**（弱い一方向 k=2 fragment のみ要）だが、existence/hitting facet 勢は **summable target を破る effective rate**＝qualitative AEV 1.6 より**強い**入力が必要。
- **厳密 ledger: 2体 outright [CONDITIONAL] 決定（Antihydra, o10-inner）、8体は 還元完成 + effective-rate 強化を modulo に reduce**。
  moral な headline は健全、literal「1予想⇒全10」は over-claim（訂正）。

### frontier 依存マップ（named conjecture → 決定機械）
| conjecture | 機械 | 数 |
|---|---|---|
| **AEV 1.6 `3/2`**（floor-mirror; o10-inner は ceiling） | Antihydra, o10-inner（[COND] 決定）; o2,o7,o8,o11,o12,o13,o14,o16（kernel-input のみ） | **10** |
| AEV 1.6 `8/3`（q=3 Erdős） | o15, o18 | 2 |
| AEV 1.6 `4/3`（q=3 Erdős） | o4, o5 | 2 |
| AEV 1.6 `5/2`（q=2 easy p>q²） | Space Needle（all-orbits 回避 provably 不可＝confined Z_{5/2} 存在、specific-orbit のみ） | 1 |
| （kernel-less） | o3, o17（Collatz-irregular odometer; o17 floor m*=8） | 2 |
- **AEV(3/2) が dominant single conjecture: 17 中 10（≈59%）** がこれに hinge＝「essentially the single Mahler 3/2 problem」の精密定量。
- 最強統合: full AEV 1.6（全 base）は **15/17 を [CONDITIONAL] 決定**（odometer 2体以外）、ただし各 base は独立 open＝実務上 frontier は **4 open base-instance + 2 odometer**、3/2 が過半。
- **10体は「1 map・相異 seed の 10 distinct single-orbit instance、1つの all-orbits 予想（AEV 1.6 base 3/2）に subsume」**。per-orbit Mahler 結果なら1体ずつ decide。

## U3 quenched L²-flattening probe（`L2_FLATTENING_PROBE.md`）— 新 [PROVEN] 理由で閉
- 軌道の経験測度 μ_N（c_n mod 2^k）の C2/H2/largest atom/additive energy E/max Fourier、**全軸で random surrogate の 95% 帯内**（全 N∈{10²..10⁵}, k∈{4,6,8,10}）。flattening rate N^{-1.01}=random N^{-1.0}。
- additive energy E は **RANDOM**（E/uniform=1.000）、sub-random でも concentrated でもない（discriminator 検証: 固定点 o=1 → E/uniform=2^k）。self-generated non-concentration なし。
- **[PROVEN elementary・新] sharper な「なぜ死んでいるか」**: ℤ/2^k 上で **×3 は bijection（3 は unit）→ C2 と E を厳密 invariant に保つ → ×3 自己拡大の L²-flattening 寄与は ZERO**。唯一の flattening channel は 2-adic carry/shift（low bit drop + fresh high bit）、その制御＝**open Mahler/AEV そのもの**。flattening の 100% が carry=assumption に住む。→ §7 を clean に閉（kernel [OPEN] は不変）。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[定量・訂正] frontier 依存マップ確定**: AEV 3/2 → 10/17(≈59%, dominant)、full AEV → 15/17、odometer 2体は別。μ=3/2 は **10 機械**（9 でない、訂正）。「1予想⇒全10」は over-claim→2体 outright + 8体 modulo（floor-mirror/in-scope/effective-rate）。
2. **[PROVEN elementary] L²-flattening 閉**: ℤ/2^k 上 ×3 は bijection で C2/E invariant＝flattening 寄与ゼロ、全 flattening は carry=Mahler に。唯一の speculative frontier を sharp に閉。
3. （o3/o17 odometer 最終特徴付けは未実行＝前ターン却下。catalogue の odometer 行は既存分類のまま: o3 bounded-alphabet, o17 floor m*=8。）

## 完全証明の現在地（定量化後）
- **(B) 完成・カタログ完全 close・docs 統合済**。依存マップで定量化: **BB6 frontier の 59%(10/17) が単一 Mahler 3/2 に hinge**、full AEV で 15/17、残 2 は odometer。
- **(A) = AEV/Mahler 等価、近道なし**。speculative L²-flattening も [PROVEN] 理由で閉（×3 bijection）。唯一の live frontier は依然 effective single-orbit equidistribution（AEV/Mahler）。
- **精密 headline（訂正済）**: BB6 Collatz core = AEV Conj 1.6 の 4 base-instance のカタログ、**3/2 が過半（10/17）**、Antihydra のみ density facet で β>0 PROVEN barrier、full AEV が 15/17 を [CONDITIONAL] 決定、2 odometer は別 named（Collatz-irregular）。

## 次の生きた一手（候補）
1. **floor-mirror AEV 予想を明示的に定式化**（U2 gap#1）: 8 in-family 機械を in-scope にする鍵＝floor 版 AEV 1.6(3/2) を1命題に固め、ceiling↔floor の bridge（GAP-LEMMA v₂(3o−1)）で繋ぐ。
2. **8 in-family 機械の exact 2^k predicate を導出**（U2 gap#2、§3c 還元完成）＝in-scope set を 2→10 に拡大、「1 floor-mirror 予想⇒10機械」を clean な [CONDITIONAL] に。
3. （o3/o17 odometer 最終特徴付けは保留＝ユーザ判断待ち。）
4. (B)/依存マップを arXiv 最終形に（59% 定量 headline で強化）。
