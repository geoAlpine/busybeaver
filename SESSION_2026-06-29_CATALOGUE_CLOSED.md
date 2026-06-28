# frontier カタログ完全 CLOSE + (B) docs 統合 + 5/2 easy-regime（2026-06-29、06-28 マラソン続）

3トラック並行実施。**結果: irregular 5体が全て nested Mahler 3/2 と判明＝カタログ完全 close（structureless 残渣ゼロ）、
BB6 Collatz core は 3/2 支配の少数 multiplier に collapse、Space Needle(5/2) は easy-regime でも walled、(B) を docs 統合。
誤証明ゼロ・decision 主張ゼロ。**

## T3【最重要】irregular 5体 = nested Mahler 3/2（`CATALOGUE_IRREGULAR.md`）— gap CLOSED
「irregular/structureless」判定は **wrong(outer) event を読んでいた**。正しい inner milestone を読むと **5体全てに clean inner ×3/2
（μ=3/2, p=2）Mahler engine**＝o10 構造（inner clean ×3/2 を outer doubly-exponential refill が包む）。logged「irregular」軌道は outer refill。
- **o11**: leading 1^k over (10)^m sea、inner sea map **m→⌊3m/2⌋+4 exact 12/12**（2,7,14,25,…,1226）。最 clean。
- **o12,o13**: two-counter 1^a 0 1^b + sea、inner a 比 → **1.500**（a'=⌊3a/2⌋+3δ−1, δ=sea 消費と完全相関）。
- **o14**: two-counter + accreting 4,4,2 marker tail、a 比 → **1.503**（純 block 化せず＝旧 pure-block scan が見つけられなかった理由）。
- **o16**: T2 single-defect costume、s→⌊3s/2⌋+2 exact、比 → **1.50**（step −1 の o11）。
- **[VERIFIED] 新 multiplier なし、全て μ=3/2（Antihydra family）**。Mahler-3/2 family は **9 explicit members に**。
  全 HOLDOUT（clean inner ×3/2 は exact halt 基準を与えず、outer refill は doubly-exp で非 eventually-periodic＝o10 と同じ obstruction）。
  (d)structureless → **(b) nested Collatz-kernel μ=3/2** に再分類。[VERIFIED]（outer refill 未完全 model、o10 同様）。

## 完全 CLOSE した frontier カタログ（structureless 残渣ゼロ）
| μ | p | regime | 機械 | facet/barrier |
|---|---|---|---|---|
| **3/2** | 2 | hard(p<q²) | **Antihydra**(density, **β>0 PROVEN 唯一**), o2,o7,o8,o10-inner,**o11,o12,o13,o14,o16**(existence/nested) | **9 members** |
| **5/2** | 2 | **easy(p>q²)** | Space Needle | existence、walled |
| **8/3** | 3 | hard | o15,o18 | existence Erdős |
| **4/3** | 3 | hard | o4,o5 | existence Erdős |
| odometer | — | — | o3,o17 | kernel-less |

**収束（強化）**: BB6 Collatz core = **4 multiplier {3/2,5/2,4/3,8/3}**、実質 **Mahler 3/2 問題が支配（9 機械）** + 5/2,8/3,4/3 の cousins
+ odometer 2体。「~2–3 named families, not 19 problems」が確定。全て v_p(μ)=−1 expanding-kernel（BB6_STRUCTURAL_LIMIT_THEOREM が一括カバー）。

## T1 Space Needle (5/2) easy-regime（`SPACE_NEEDLE_5_2.md`）— 真の lead だが walled
- **K_SN（厳密 kernel）**: 非停止 ⟺ 特定 5/2-counter 軌道（T(x)=⌊5x/2⌋ on ℤ₂）が clopen carry-alignment set H を永久回避＝
  **existence/avoidance facet（q=2, μ=5/2＝o18 の q=3 carry-avoidance の類）**、Mahler-density でない。
- **easy regime(p=5>q²=4)で既知**: FLP/Bugeaud/Dubickas の **all-x spread ≥1/5**（Ω∈[1/5,2/3]）；Kaneko/Pollington の
  **confined 軌道 EXISTS（Z_{5/2}-numbers 存在）**（AEV Conj1.4 が p<q² を課す理由）。
- **K_SN を特定軌道に deliver せず、2つの致命的 gap**: (a) quantifier（all-x spread or some-x existence、特定 seed でない；しかも
  **confined 軌道が provably 存在＝all-orbits 論法は provably 不可能**＝hard cryptid と同じ壁）(b) facet mismatch（spread ≠ measure-zero 回避）。
- **verdict: Space Needle は decision で more tractable でない・decidable でない**（全 sound tool HOLDOUT）。easy regime は **literature/placement の
  genuine differentiator**（5/2 は well-studied p>q² 近傍の唯一の frontier multiplier）だが、同一の specific-orbit 壁 + facet mismatch。
  honest negative、soundness 健全。

## T2 (B) finalize + docs 統合
- **`BB6_STRUCTURAL_LIMIT_THEOREM.md` 更新**: class を {μ: v_p(μ)=−1}（4 multiplier 3/2,5/2,4/3,8/3）に拡張、完成 19-cryptid catalogue table
  （machine|μ|p|facet|regime|barrier|class）追加、regime 列（3/2,4/3,8/3 hard / 5/2 easy）。新 multiplier は **[VERIFIED]**（[PROVEN] でない）、
  in-scope exact-reduction set は {Antihydra,o18,o15,o10-inner} のまま。既存 label 不変。
- **`docs/theory_certification_hierarchy.md` 統合**: BB6 Collatz core = 4 named Mahler/Erdős multiplier の **完成カタログ**、Antihydra β>0 は
  spoofer/certificate メタ原理の **discrete・予想非依存・[PROVEN] avatar**（量子 genuineness 限界・SETI と並ぶ3つ目）。構造的統合であって
  reduction でない・decide せず・per-cryptid は [CONDITIONAL] と誠実明記。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[VERIFIED] frontier カタログ完全 CLOSE**: irregular 5体（o11-o16）が全て nested Mahler 3/2＝structureless 残渣ゼロ。
   Mahler-3/2 family 9 members。BB6 Collatz core は 4 multiplier、**Mahler 3/2 支配**に collapse。
2. **[HOLDOUT] Space Needle(5/2) not decidable**: easy regime(p>q²)は real な literature differentiator だが特定軌道壁 + facet mismatch +
   confined 軌道 provably 存在ゆえ all-orbits 不可。
3. **(B) finalize + docs 統合完了**: BB6_STRUCTURAL_LIMIT_THEOREM に完成 catalogue + class 拡張、theory_certification_hierarchy に anchor 統合。投稿形。
4. **全機械 HOLDOUT**（decidable な cryptid なし、soundness 健全）。

## 完全証明の現在地（カタログ完全 close 後）
- **(B) 構造的限界定理 = 完成・カタログ完全 close**: 全 cryptid を {3/2,5/2,4/3,8/3 expanding-kernel} + odometer に分類、structureless 残渣ゼロ、
  density barrier(Antihydra β>0)、5階層 hierarchy、docs 統合済。**BB6 Collatz core が encode する named number theory = 主に Mahler 3/2(+少数 cousins)** と確定。
- **(A) 個別 cryptid = AEV/Mahler 等価、近道なし**。5/2 も easy regime で walled（confined 軌道存在ゆえ all-orbits 不可、特定軌道は壁）。
- **新事実: BB6 Collatz core の難しさは本質的に「Mahler 3/2 問題 1つ」に集約**（9/17 機械が 3/2、残りは 5/2,4/3,8/3 の cousins + odometer 2）。
  ＝ BB6 frontier の難しさの源泉が単一の named 問題に pin された。

## 次の生きた一手（候補）
1. **o3/o17 odometer 2体の最終特徴付け**（kernel-less の唯一残り、decidability 再挑戦 or 別 named 問題への帰着）＝カタログの完全分類仕上げ。
2. **「BB6 Collatz core ≈ Mahler 3/2」を定量化**: 9 機械が同一 3/2 kernel に帰着することを exact reduction で固め（in-scope set 拡大）、
   1つの Mahler 3/2 が解ければ 9 機械が落ちる構造を投稿文書に。
3. quenched L²-flattening 小数値 probe（唯一の speculative frontier）。
4. (B) を arXiv/notes の最終形に磨く（カタログ完全 close で headline が強化された）。
