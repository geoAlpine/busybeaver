# floor-mirror ≡ AEV（[PROVEN] conjugacy）+ in-scope 拡大試行（2026-06-29）

3トラック並行：①floor-mirror AEV 予想の定式化+bridge ②o2/o7/o8 exact 還元 ③o11-o16 exact 還元。
**結果: [PROVEN] floor↔ceiling は conjugacy R(x)=−x で EQUIVALENT（gap#1 CLOSED）、だが in-scope 拡大は 0/8（全 8 機械が o10-full 型 nested blocker）。
誤証明ゼロ・decision なし・健全性 self-catch 1件。**

## V1【genuine PROVEN 前進】floor-mirror ≡ AEV（`FLOOR_MIRROR_CONJECTURE.md`）
- **FM(3/2) [OPEN]**: 「Tf(x)=⌊3x/2⌋ の全軌道が mod 2^k 等分布」。fragment（弱→強）: single-orbit ⊂ level-k ⊂ one-sided ⊂ density ⊂ effective-rate。
  **Antihydra は最弱（single-orbit, level k=2, one-sided, o₀=27）のみ要**。
- **[PROVEN] bridge: floor↔ceiling EQUIVALENT**。厳密恒等式 **`Tc(x) = −Tf(−x)`**（∵⌈y⌉=−⌊−y⌋）= `Tc = R∘Tf∘R`, R(x)=−x。
  R は ℤ₂ の Haar 保存 involution で ℤ/2^k を permute → 等分布が軌道ごとに transfer。
  **最強検証: induced depth 列が literally 同一 `D_l^floor(27) = D_l^ceil(−27)`（200k steps, 0 例外）**＝Antihydra の load-bearing 統計が verbatim に carry。GAP-LEMMA D=v₂(3o∓1) が bridge、v₃(o)=D−1 も transfer。
- **residual**: conjugacy は floor-positive → ceiling-**negative** に写す（positive→positive でない）。equivalence は全 ℤ₂（sign-symmetric）上で literal、AEV の positive-only 文との差は **seed-sign quantifier のみ**（cosmetic、conjecture が sign-blind との標準期待下で閉）。
- **AEV(3/2) ⟹ floor 版**: 全 ℤ₂ 上 [PROVEN] biconditional、AEV literal positive-only 版へは [CONDITIONAL]（sign 拡張）。
- → **gap#1（floor-mirror が AEV と formally 別予想）は CLOSED**: floor cryptid 群は **同一 named 予想 AEV 1.6(3/2) の下に**（proven conjugacy、cosmetic sign 除き）。

## V2 o2/o7/o8 exact 還元（`REDUCE_O2_O7_O8.md`）— 0/3 in-scope、blocker 確定
- bb_sim と step-for-step 一致の instrumented sim で実施。**[PROVEN seed-verified] 厳密 halt 事象**: o7/o8 は `00`-left（左 counter 空で C/E が separator 消費）、o2 は `00`-gap right。
- **[VERIFIED] induced map**: o7 reset 6,11,16,…/o8 reset 2,4,7,…、clean `⌊3a/2⌋+c` は **even-a inner 部分列のみ**、odd-a は **2-adic halving-cascade refill**（target が a の全 2-adic 展開に依存）を fire。
- **load-bearing blocker**: o2/o7/o8 は **coupled counters**＝⌊3x/2⌋ が even-a inner chain でしか成立せず、odd-a で nested refill（o10-full/o11 nesting と同型）。**回避対象は nested map で clean 3/2 軌道でない → full floor-mirror AEV でも decide せず**。**in-family-not-in-scope のまま、count 不変**。
- **健全性 self-catch**: o7/o8 に clean parity predicate を仮説→ bb_sim 2×10⁶ で **FAIL（3, 9 mismatch）→ 撤回**（SOUNDNESS_INCIDENT 規律）。definitional な `00`-event のみ survive。

## V3 o11-o16 exact 還元（`REDUCE_O11_O16.md`）— 0/5 in-scope、全て o10-full 型
- 各機械 [VERIFIED] inner map + [PROVEN unit-tested] 厳密 halt mechanic（previously「reads 0」のみ）。
- **decisive: 全 5 機械で halt 事象が inner epoch から構造的に absent ＝ outer refill に couple（o10-full と同型）**。precursor neighbor は全 visit で `1`（o11 2330/2330, o12 3516/3516, o14 1996/1996）＝inner では never trigger。
- **新: o13 = o10 の exact structural twin**（D→E eat-sweep が EVEN-length run 消費で halt；o10 は leftward eat-sweep が odd で halt）。o13 inner は all-odd（safe）7214/7214＝o10 の always-even inner eat の analog。clean exact predicate（「∃ even-run sweep で halt」）だが outer refill `3,6,10,64` で composite/blocked。
- **direction [OPEN] 全 5**。o13 は o10 と**逆 signal**（o13 非停止寄り vs o10 ~1/3-per-epoch 停止寄り）だが outer epoch ~4 しか reachable、abstract outer model 抽出不可で per-epoch 確率割当不能。
- **tally: 0 in-scope, 5 in-family, 0 confirmed halter**。scope set {Antihydra,o18,o15,o10-inner} 不変。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[PROVEN] floor-mirror ≡ AEV（conjugacy R(x)=−x, Tc=−Tf(−x)）**: D 列 literally 同一（0 例外）。**gap#1 CLOSED**＝floor cryptid 群は同一 named 予想 AEV 1.6(3/2) の下に（cosmetic sign quantifier 除き）。dominance headline 強化。
2. **[honest negative] in-scope 拡大は 0/8**: o2,o7,o8,o11-o16 全てが **o10-full 型 nested blocker**（clean ⌊3x/2⌋ は inner even-subseq のみ、halt は outer refill に couple）。**full floor-mirror AEV でも decide せず**、in-scope set は 4（{Antihydra,o18,o15,o10-inner}、うち 3/2 は 2）。
3. **[VERIFIED 新] o13 = o10 の exact twin**（eat-sweep even-run halt、逆 direction signal）。8 機械の厳密 halt mechanic を sharpen。
4. **[健全性] V2 が failed predicate を bb_sim で捕捉・撤回**（規律維持）。

## 完全証明の現在地（floor-mirror 後）
- **(B) 完成 + gap#1 CLOSE**: floor cryptid 群が **conjugacy で AEV 1.6(3/2) に統一**（proven bridge）。BB6 frontier の 10/17 が AEV(3/2) の kernel を共有（全 ⌊3x/2⌋ を run）、full AEV で 15/17。
- **in-scope（exact reduction）= 4 機械**（Antihydra, o10-inner, o18, o15）。残り 8 の μ=3/2 機械は **multiplier 共有だが exact predicate が nested refill で blocked（o10-full barrier、各々 o10 並みに hard、一部は o10 同様 probabilistic halter の可能性 [OPEN]）**。
- **精密 dominance（訂正済）**: AEV 1.6(3/2)（+floor bridge）は Antihydra & o10-inner を [CONDITIONAL] 決定；他 8 は **AEV に加えて nested-refill reduction（o10-full 級）も**要。10 機械全てが ⌊3x/2⌋ kernel を共有する意味で「Mahler 3/2 が支配」は健全、ただし「1予想で全10即決」でなく「全10が同 kernel・2 が exact 直結・8 が nesting 越し」。
- **(A) = AEV/Mahler 等価、近道なし**（floor=ceiling と判明、5/2 も walled、L²-flattening も閉）。

## 次の生きた一手（候補）
1. **nested-refill（o10-full 型）の統一構造を1命題に**: o2,o7,o8,o10-full,o11-o16 が共有する「inner clean ⌊3x/2⌋ + outer doubly-exp refill、halt は outer alignment」を抽象化＝**第2の named 構造（nested-Collatz）として catalogue 化**（in-scope にはできないが、なぜ blocked かを [PROVEN] 構造に）。
2. **o13/o10 の direction 対比を精密化**（o13 非停止寄り vs o10 停止寄り）＝nested-Collatz の方向決定が何に依存するか。
3. **floor-mirror bridge を BB6_STRUCTURAL_LIMIT_THEOREM に組込**（gap#1 CLOSE を本文に、dominance を「AEV 1.6(3/2) 1予想が 10 機械の kernel を支配」と更新）。
4. (B)/依存マップ + floor-mirror bridge を arXiv 最終形に。
