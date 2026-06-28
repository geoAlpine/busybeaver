# nested-Collatz 第2構造 [PROVEN] + direction 二分 + (B) 統合・arXiv 評価（2026-06-29）

3トラック並行。**結果: nested-Collatz を第2 structural class として [PROVEN] 定式化（catalogue が two-axis 構造に完成）、
direction は outer orbit 上の Borel-Cantelli 二分で決まる、(B) doc に floor-mirror bridge+訂正 dominance 統合済、arXiv 道筋確定。
誤証明ゼロ・decision なし・健全性 self-catch 1件。**

## W1【新 [PROVEN] 構造】nested-Collatz 第2 class（`NESTED_COLLATZ_STRUCTURE.md`）
- **定義**: nested-Collatz machine = (inner clean T_μ on even/admissible subseq) ⊗ (outer counter の roll-over が refill を fire→inner 再 seed、refill seed 列 {B_e} は doubly-exp・非 eventually-periodic) ⊗ (halt が outer refill alignment に couple、inner epoch 内では構造的に不可能)。**9 instances: o2,o7,o8,o10-full,o11,o12,o13,o14,o16（全 μ=3/2）**。
- **Blocking Theorem**: (i)[PROVEN 定義的] halt は inner epoch 内で起きない→単一 inner 軌道に halt site なし→単一軌道 AEV では「M halts」と等価にならない (ii)[PROVEN 構造的] halt は **outer reseed family {O_e}**（各 doubly-exp seed B_e の fresh inner 軌道）を quantify、1軌道でない (iii)[PROVEN for o10]（exact criterion+inner eat 長 2m−8 always even）/[CONDITIONAL/VERIFIED] 他8。
- **exact predicate が要するもの**: **単一軌道 AEV（per-epoch parity-at-underflow）⊗ outer refill map（doubly-exp piecewise-affine）⊗ reseed 上の Borel-Cantelli existence test（summable target を破る effective 等分布要）**。第1因子=Axis-1 in-scope object、後2因子=irreducible excess。**= AEV + Borel-Cantelli-over-restarts**。
- **two-axis 分類確定**: **Axis 1（単一軌道 in-scope, 4機械）**{Antihydra,o10-inner,o18,o15}＝machine 全体が1 inner-orbit AEV 事象、exact reduction [PROVEN]、Antihydra に β>0 barrier。**Axis 2（nested-Collatz, 9機械）**＝halt は ∞ reseed 上の outer alignment、composite/existence、over-approximation [OPEN] top、direction [OPEN]。
- **placement**: nested-Collatz は in-scope cryptid の **strictly above**（単一軌道 AEV を sub-factor に含み doubly-exp outer + BC over restarts を加える）。**o10 が pivot**（inner=最 clean Axis-1, full=canonical Axis-2）。bb_sim 検証済。

## W2 direction 二分（`NESTED_DIRECTION.md`）
- **discriminator は inner parity でない**（全機械が parity-safe inner＝inner では never halt）。**outer refill 軌道上の per-epoch halt 確率 scaling = Borel-Cantelli 二分**:
  - **divergent（p_e≈const>0, fixed-measure target）⇒ HALT-leaning**: **o10 のみ**（forced b-underflow, m-parity ~fair coin ~1/3, B-window 間で非減衰）。BC-II は単一軌道に独立性なく [OPEN]。
  - **convergent（p_e→0, thin/spontaneous-defect target）⇒ NON-HALT-leaning**: o2,o7,o8,o11,o12,o14,o16（00-gap collision/phase race、defect-free field に defect が自発出現要、neighbor=1 が数千 visit）。
  - **unclear**: o13（parity-of-run target だが outer scaling 未抽出）。
- **[訂正] o10(~1/3) vs o13(~0) の差は structural と未確立**＝confounded+small-sample（o10 の 1/3 は **outer** halt-prob、o13 の ~0 は **inner** safe-rate＝o10 も持つ事実、o13 の per-outer-collapse halt-prob は未抽出、outer epoch ~4 のみ reachable）。**o13 direction は genuinely [OPEN]、o10 同様 halt-leaning の可能性も**。前 session の「o13 は逆 signal」を慎重化。
- **健全性 self-catch**: ad-hoc o13 entry 構成が mixed parity→unfaithful-context artifact と判明→unit-tested doc 値を引用（REDUCE_O2_O7_O8 §5 撤回の教訓再適用）。

## W3 (B) 統合 + arXiv 評価（`BB6_STRUCTURAL_LIMIT_THEOREM.md` 更新）
- **§8.1 floor-mirror bridge [PROVEN] 追加**: 厳密 conjugacy Tc=R∘Tf∘R, R(x)=−x（証明 ⌈y⌉=−⌊−y⌋）、floor/ceiling 等分布が軌道ごと equivalent（exact measure-preserving isomorphism）、D 列 literally 同一（独立再検証 200k steps 0 例外, mean D=1.996270, freq(D≥2)=0.499660）、floor cryptid 群が AEV 1.6(3/2) 下に（bridge [PROVEN]/conjecture [OPEN]、cosmetic seed-sign quantifier 誠実明記）。
- **§8.2 訂正 dominance [CONDITIONAL]**: 全10 μ=3/2 が ⌊3x/2⌋ kernel 共有、**2 exact 直結（Antihydra,o10-inner [CONDITIONAL] 決定）、他8 は o10-full 級 nested-refill reduction も要 [OPEN]**。「all ten share the kernel, 2 reduce exactly, 8 through a nesting layer」。in-scope=4 不変、「1予想で全10即決」と言わない。
- **§8.3 nested-Collatz cross-ref [VERIFIED]**（9機械, inner-3/2/outer-doubly-exp signature, o13≡o10 twin, direction [OPEN]）。NESTED_COLLATZ_STRUCTURE.md は W1 が並行作成済＝cross-ref 有効。
- scope 一貫（β>0=Antihydra のみ, in-scope=4, nested-Collatz=9 incl o10-full）、label upgrade なし。
- **arXiv 評価**: **internal record として READY**（self-contained, 全 label, scope 厳守, numerics 機械検証）。**arXiv standalone math note は NOT YET**: ①1-2 focused note に split（Thm1-3+§8 を1本、5階層 hierarchy Thm4 を独立 note に）②各 [PROVEN] の full proof を inline（sketch/[VERIFIED] 数値依存の箇所、CF⊊CS は arXiv:1901.03913 を input として cite）③外部 citation（ergodic-opt の Mañé/Conze-Guivarc'h/Bousch locator, bbchallenge TM spec）+ label→TM 定義表。**writeup work であって新数学でない**。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[PROVEN] nested-Collatz 第2構造**: 9機械を Axis-2（単一軌道 AEV ⊗ doubly-exp outer refill ⊗ BC over restarts）と定式化、Blocking Theorem で in-scope でない理由を [PROVEN]/[CONDITIONAL] に。catalogue が **two-axis 構造に完成**（Axis-1 in-scope 4 / Axis-2 nested-Collatz 9 / odometer 2 / 他 base 4）。
2. **[構造] direction 二分**: nested-Collatz の halting direction は outer orbit 上の BC（divergent→halt / convergent→non-halt）、o10 のみ明確 halt-leaning、o13 含む他は [OPEN]。**o13≠o10 の旧主張を慎重化**（small-sample/confounded）。
3. **(B) 統合済 + arXiv 道筋確定**: floor-mirror bridge[PROVEN]+訂正 dominance+nested-Collatz を doc に、internal record READY、arXiv は writeup work（split+inline proof+citation）。
4. **[健全性] W2 が unfaithful-context artifact を self-catch**（規律維持）。

## 完全証明の現在地（two-axis 完成後）
- **(B) 完成・two-axis catalogue・floor-mirror bridge [PROVEN]・docs 統合・arXiv 道筋確定**。BB6 frontier の構造が**完全に解剖**された:
  - **Axis-1 in-scope（4）**: 単一軌道 AEV、Antihydra に β>0 PROVEN barrier。
  - **Axis-2 nested-Collatz（9, μ=3/2）**: AEV + BC-over-restarts、strictly above、direction [OPEN]（o10 halt-leaning）。
  - **odometer（2: o3,o17）**: kernel-less、Collatz-irregular halt。
  - **他 base（4: o4,o5=4/3, o15,o18=8/3, Space Needle=5/2）**。
- **(A) = AEV/Mahler 等価、近道なし**（floor=ceiling [PROVEN], 全構造攻撃 closed）。
- **精密 headline**: BB6 Collatz core = AEV 1.6 の 4 base-instance + 2 構造 axis（single-orbit / nested-restart）+ 2 odometer、3/2 が支配（10/17, conjugacy で統一）、Antihydra のみ proven barrier。

## 次の生きた一手（候補）
1. **arXiv split の実行**: Thm1-3+§8（kernel placement+floor-mirror）を1 note、5階層 hierarchy を独立 note に分割し、各 [PROVEN] の full proof を inline（最大の writeup gap）。
2. **odometer 2体（o3,o17）の最終特徴付け**（保留中、catalogue の唯一の未 finalize axis＝完全分類仕上げ）。
3. **nested-Collatz の BC-over-restarts を1命題に**（Axis-2 の exact predicate の形＝AEV⊗doubly-exp⊗BC を conditional theorem に）。
4. label→TM 定義表 + 外部 citation locator（arXiv 化の機械的残務）。
