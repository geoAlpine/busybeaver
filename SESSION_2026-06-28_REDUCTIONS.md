# o10/o18/o15 §3c 還元の完成 — 統一定理は2-facet/2-axis に分裂（健全性訂正）（2026-06-28）

統一限界定理を o18/o15/o10-inner で conditional → PROVEN にする試み。各 raw TM から §3c 還元を完成し
trusted sim（bb_sim）と照合。**結果: 還元は PROVEN だが、family が density/existence の2 facet に分裂し
2つの LIMIT_THEOREM 軸に乗ると判明。β>0 barrier の PROVEN scope は Antihydra のみ（前主張を訂正）。
新 [PROVEN] 成分（unconditional annealed Borel-Cantelli-I 非停止）獲得。誤証明ゼロ。**

## 健全性訂正（請求前に捕捉）
前 `UNIFIED_LIMIT_THEOREM.md` は o18/o15 を density β>0 barrier 下に置いた＝**MISLABEL・撤回**。
o18/o15 は density underflow で停止せず **EXISTENCE 事象（base-3 carry alignment が *いつか* 起きる=Borel-Cantelli/Erdős facet）**で停止。
2^a/3^b kernel は family-wide 共有だが **facet（density vs existence）が governing axis を決める**。同 file 冒頭に訂正 banner。

## 各還元の結果（全て bb_sim 照合済）

### o10（`O10_REDUCTION.md`）— OUT of scope、方向が REVERSED
- **[PROVEN] 厳密 halt 基準**（L=1..8 unit-test + 実軌道 5×10⁶ 照合）: o10 halts ⟺ C/F leftward eat-sweep が
  **奇数長の 1-run を消費**。clean config `1 0^{2m−8} 1^b 0 1`, 内側 m→⌈3m/2⌉（**文字通り AEV ceiling 3/2**）, b→b−(1+[m odd])。
  内側 eat 長 L=2m−8 は**常に偶数**→内側ループは halt しない。**(H-criterion): epoch は b-countdown が奇 m で b=0 に着地すると halt**
  （base rule m=5..79 + composition B=1..16 で 0 mismatch、B=5→57 が実機 epoch1→2 refill に一致）。
- **分類: COMPOSITE/EXISTENCE**、一方向 density 基準でない。内側 AEV-3/2 還元は clean+PROVEN だが o10 を単独で decide しない。
- **方向が逆**: genericity は o10 を **HALT** させる（各 epoch が w.p.≈1/3 で halt[OBSERVED 33.67%/B=1..3000]、無限 epoch で halt-prob→1）。
  ＝**「確率的に停止する」遅延 halter**で Antihydra 型の確率的 non-halter でない。**o10 FULL は統一定理の OUT**、真の方向は OPEN（heuristic に停止）。
- (H-fixed-point) [PROVEN]: 退化 config（m 奇, b=0）は halt、内側固定点 m=−1（Antihydra o=+1 の 2-adic mirror）、β=+1/2 transfer（内側のみ）。

### o18（`O18_REDUCTION.md`）— 還元 CLEAN+PROVEN、existence-type
- **[PROVEN] 厳密 halt 基準**（2×10⁸ step 照合, 10 F-entry 全 read 0, 0 collision; planted control で機構直接確認）:
  o18 halts ⟺ state F が 1 を読む ⟺ leftward D/F sweep frontier が既存 1 に着地（**隣接-11 left-frontier carry alignment**）。
- **[PROVEN] existence-type**: non-halt ⟺ bad set 𝓑={k: carry aligns} が有限/空。**density は証明可能に不十分**（𝓑 は density 0
  だが空でない、1回の alignment=halt）。Borel-Cantelli skeleton: Σ_{k≥7} Haar(B_k) = 1.54×10⁻⁴ < ∞。Erdős ternary facet
  （Narkiewicz は上界のみ、有限性は未知）。固定点 N=−1。**還元（raw TM→base-3 carry の existence 基準）は CLEAN+PROVEN**。
  o18 は **(K_o18) = AEV Conj1.6 の q=3・単一軌道・floor-mirror・existence/Erdős fragment [OPEN]** に PROVEN-reduced。

### o15（`O15_REDUCTION.md`）— o18 と同 Erdős kernel、messier coordinate、in-scope
- **[PROVEN] 厳密 halt 基準**（bb_sim と step-for-step 一致, 120M step, planted control）: o15 halts ⟺ rightward F→A handoff が
  `11` を読む（2つの 1-block が abut）＝**right-frontier collision（o18 の mirror）**。
- width は clean `W↦⌊8W/3⌋+2`（o18 と同写像・別 seed・固定点 N=−1）、**parity-irregularity は block 分解＝(8/3)^n 軌道の
  base-3 digit 列に宿る**（separator 位置=carry-boundary）。**同 Erdős kernel・同 AEV q=3 existence facet、messier coordinate のみ**。
  model 化は harder だが number theory は同一。**in-scope of existence-version、別扱い不要、還元 clean+PROVEN**。

### existence メタ定理（`EXISTENCE_META_THEOREM.md`）— THE 核心 + 訂正
- **existence-version template**: (E-criterion) 非停止 ⟺ 軌道が clopen halting set H を永久回避（Π⁰₁ tail-avoidance/Borel-Cantelli）；
  (E-hitting) H≠∅ かつ ある軌道が H に入る；structure-only 証明 = 前進不変 over-approximation L（x₀∈L, T(L)⊆L, L∩H=∅）＝
  LIMIT_THEOREM §1 の certificate object そのもの。
- **density ほど clean に no-structure-only を与えない（重要 finding）**: density barrier は PROVEN（β>0, max over μ が
  全測度を数える）。existence object は不変**集合**で、**集合は単に halting 軌道 y_* を除外できる**→(E-hitting) は avoidance
  certificate を block しない。**β が無い**。existence barrier は **LIMIT_THEOREM の over-approximation/記述複雑度軸（[OPEN]）に
  正確に帰着**。[PROVEN] なもの: open H で非停止軌道の閉包は前進不変かつ H と disjoint（閉 over-approximation は常に存在）、tame なものが
  あるかが問題。
- **easier or harder? DUAL（軸で分裂）**:
  - **annealed/measure 側: existence は EASIER・unconditional に PROVABLE** — ΣHaar(B_n)≍Σ(8/3)^{-n}<∞ ゆえ
    **Borel-Cantelli I（独立性不要）で Haar-a.e. seed 非停止**[新 PROVEN]。（o18_bc.py の「B-C は独立性要」注を訂正＝B-C I は無条件。）
  - **解析 input 軸: existence は厳密に WEAKER input** — summable target を破る effective 等分布（density の positive liminf は
    eternally tight）。両者 OPEN だが existence の target は弱い。
  - **barrier 軸: existence は HARDER** — no-structure-only barrier が open（β なし）。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[健全性訂正] β>0 barrier の PROVEN scope は Antihydra のみ**。o18/o15 は density facet でなく existence facet で、
   barrier は OPEN over-approximation 軸。前 UNIFIED の mislabel を撤回（status 不変、全 open）。
2. **[PROVEN] 還元3本**: o10（composite/existence, 内側 AEV-ceiling-3/2 clean）・o18（existence, 隣接-11 alignment）・
   o15（existence, mirror collision, 同 Erdős kernel）。全て bb_sim 照合済。
3. **[PROVEN 新成分] unconditional annealed Borel-Cantelli-I 非停止**（o18/o15: Haar-a.e. seed 非停止, ΣHaar(B_n)<∞ 独立性不要）。
   + 閉 over-approximation 補題。
4. **[PROVEN 構造的洞察] family は 2-facet/2-axis に分裂**: density(3/2: Antihydra=PROVEN barrier / o10-inner conditional)
   ／existence(8/3: o18,o15=OPEN over-approx barrier + 新 B-C I)／o17=kernel-less。**o10 FULL は OUT（確率的に停止する遅延 halter）**。
5. **[訂正] 統一定理は「family-wide PROVEN」でなく「density facet で PROVEN barrier、existence facet は別軸で OPEN barrier + 部分 PROVEN」**。
   より正確で richer な像。CRYPTID_CENSUS の named-number-theory カタログは完成度が上がった（各 cryptid の facet・axis・kernel が確定）。

## 完全証明・限界定理の現在地（訂正後）
- **Antihydra**: 非停止 ⟺ density mean D≥3/2 ⟺ AEV q=2 density fragment。measure 側 PROVEN・example 側 arithmetic PROVEN・
  no-structure-only **PROVEN（β>0）**。残 OPEN = 単一軌道 genericity（Mahler/AEV）。
- **o18/o15**: 非停止 ⟺ AEV q=3 existence/Erdős fragment。還元 PROVEN・annealed B-C I 非停止 PROVEN（Haar-a.e.）・
  no-structure-only **barrier は OPEN（over-approx 軸）**。残 OPEN = 単一軌道 existence（Erdős ternary）+ tame certificate 有無。
- **o10**: 内側 AEV-ceiling-3/2 clean+PROVEN だが FULL は composite で**確率的に停止**＝統一定理 OUT、方向 OPEN。
- **o17**: odometer、kernel-less、別問題。

## 次の生きた一手（候補）
1. **existence facet の barrier（over-approximation 軸）を1機械で攻める**: o18 に tame（REG/FAR）certificate が無いことを
   embedded-family 非正則性で PROVEN にできるか（density 側の β>0 に対応する existence 側の proven barrier を1本立てる）。
2. **annealed B-C I を quenched 化**（o18/o15 の真 frontier）: summable target を特定軌道で破る effective 等分布
   （density 版より弱い input、existence facet の有利性を exploit）。
3. **o10 の「確率的に停止」を厳密化**: 内側 AEV-3/2 の genericity が各 epoch w.p.1/3 halt → 無限 epoch で halt を、
   Borel-Cantelli II（発散側）で attack できるか（o10 を halter として decide する lottery upside）。
4. 2-facet/2-axis カタログを `docs/theory_certification_hierarchy.md` と統合・投稿文書化。
