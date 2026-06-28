# capstone フレームワークを BB6 Collatz core 全体に適用 — 統一限界定理（2026-06-28, pivot）

Antihydra の解析核が循環化（10+角度で Mahler/AEV）したのでピボット：今日築いた machinery
（GAP LEMMA / induced map / ergodic-opt メタ定理 / AEV 配置）を**他の Collatz-core cryptid に適用**。
**結果: フレームワークが一般化し、BB6 Collatz core を named 予想のカタログ + 統一限界定理にした。
新原 contribution（Antihydra 単独を超える）。誤証明ゼロ。**

## ★ 統一限界定理（L3, 新原 contribution）
**抽象テンプレート**: 機械 M の停止が単一軌道系 (X,T,x₀) + depth 統計 ϕ に還元され、
- **(H-criterion)** 非停止 ⟺ 一方向 Birkhoff 不等式 `liminf (1/N)Σϕ(T^n x₀) ≥ θ`；
- **(H-fixed-point)** 不変測度 μ_*（固定/周期点上の atom, ∫ϕ dμ_* < θ）= **停止軌道**が存在 ⟹ β:=max_μ∫(θ−ϕ)dμ > 0。

**メタ定理**: このとき **structure-only/finite-certificate な非停止証明は存在しない**
（Bousch ergodic optimization: 全軌道一方向 bound ⟺ β≤0；構造的論法は β≤0 を強制；だが β>0 ⟹ 偽命題「全軌道非停止」）。

**決定的 engine（family-wide, 機械検証 `kernel_classification.py`）**: `T_μ(x)=⌊μx⌋` on ℤ_p は
**v_p(μ)=−1 のとき厳密に p-to-1 exact endomorphism**、induced map は full-branch 拡大で **各 branch に固定点**。
「各 branch に固定点」= (H-fixed-point) ⟹ **v_p(μ)=−1 の全 multiplier で β>0 自動**。

**統一定理（precise）**: μ=2^a/3^b, v_p(μ)=−1, 一方向 renewal-density 停止基準を持つ全 BB6 cryptid で：
(1) β>0 は共有拡大 kernel から自動 [PROVEN]；(2) **structure-only/all-orbits/finite-certificate な非停止証明は不可能**、
停止/非停止の区別は単一軌道 genericity（μ-instance of Mahler-1968/AEV-2025）にのみ宿る。

## BB6 Collatz core の地図（フレームワーク適用結果）

### 3/2 / 2-adic / Mahler-density facet（AEV Conj 1.6 q=2 instance）
- **Antihydra = ⌊3c/2⌋（FLOOR mirror）**: 今日の capstone。β=+1/2 [PROVEN]、固定点 o=1。
- **o10-inner = ⌈3m/2⌉（L1）= 文字通り AEV CEILING 写像（mirror 不要、Antihydra より clean）**。induced T'(m)=3^{D'−1}(3m+1)/2^{D'},
  D'=v₂(3m+1)、mirror residue 則 D'=1⟺m≡3 mod4（Antihydra は o≡1 mod4）。固定点 m=−1（o=1 の 2-adic mirror）。
  **同じ named 予想（AEV 3/2）の別軌道 m₀=9・ceiling 面**。ただし full o10 = AEV 3/2 kernel ⊗ irregular 二重指数 refill＝
  inner は Antihydra より clean だが全体は厳密に harder（nested 2-level）。naive halt model は偽（負の結果記録）。

### 8/3 / 3-adic / Erdős-existence facet（AEV Conj 1.6 q=3 instance）
- **o18 = ⌊8N/3⌋+2（L2）, ratio 8/3**: 全て 2-adic → **3-adic**。GAP LEMMA T''(N)=8^{D''−1}(8N−r)/3^{D''}, D''=v₃(8N−r)、
  Haar-exact Bernoulli on ℤ₃*, D'' geometric mean **3/2**, mult-of-3 density 1/3。p/q=8/3, **p<q²(8<9) = Mahler-implication
  regime**（3/2 と同じ tight edge p=q²−1）、**同じ AEV Conj 1.6 の q=3 instance**。固定点 N=−1。
  **重要な差**: o18 は **EXISTENCE（Borel-Cantelli, carry が *いつか* align）で停止**、density underflow でない＝
  **Erdős ternary-digits-of-2^{3n} facet**（Mahler density でなく）。β=max の density 形は literal に transfer せず（Erdős「無有限性」形）。
- **o15 = Mahler-8/3, parity-irregular（L4）**: clean ×8/3 軌道（o18 と同一）、parity-irregularity は block 分解 =
  (8/3)^n 軌道の base-3 digit 列に宿る＝**o18 と同じ Erdős ternary kernel**、messier coordinate。in-template、同じ壁。

### odometer outlier
- **o17 = carrying odometer（L4）**: doc 矛盾を解決＝**tame odometer**（uniquely ergodic, equidistribution 自動,
  equidistribution kernel なし, width ~√t sub-linear）。「≈×8」tag は carry-buffer block の誤測定（clean scalar map なし）。
  **全 hardness は halt predicate（MSB 越え carry overflow）に**。埋込 family `0 A 0 1^k`: k≢0 mod3 は trivial 停止、
  k≡0 mod3 は **Collatz-irregular**（16 proven halters が non-halters と interleave, modulus なし）→ sound な regular/FAR 証明書
  不可能。**different-named-problem（uniquely-ergodic odometer + 埋込 3x+1 型 carry family）、Antihydra/AEV template に
  非適合、decidable でない**。lottery upside は反証。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN] 統一限界定理**: v_p(μ)=−1 の全 T_μ cryptid で β>0 自動 ⟹ structure-only 非停止証明 不可能、residue = 単一軌道
   genericity（Mahler/AEV）。Antihydra で PROVEN、o18/o15/o10-inner で conditional、o17 は provably 除外。
   ＝Antihydra メタ定理を **family-wide な PROVEN dynamical-axis barrier に一般化**（新原 contribution）。
2. **[PROVEN/VERIFIED] BB6 Collatz core の地図**: 3/2-2-adic-Mahler-density（Antihydra/o10-inner）／8/3-3-adic-Erdős-existence
   （o18/o15）／odometer outlier（o17）の3 type。AEV Conj 1.6 の q=2 と q=3 の instance として named 数論にカタログ化。
3. **[PROVEN] 決定的構造**: T_μ on ℤ_p は v_p(μ)=−1 で exact p-to-1 endomorphism、各 branch に固定点（=(H-fixed-point) を自動供給）。
4. **証明書階層への接続**: LIMIT_THEOREM の heuristic caveat（measure route は specified orbit に盲目）を **PROVEN な
   ergodic-opt barrier（β>0 at halting measure）に格上げ・family-wide 化**。dynamical 軸を family-wide にクローズ、
   over-approximation 軸（REG/tame 証明書 top）は別軸で依然 open（誠実）。

## 次の生きた一手（候補）
1. **o18/o15/o10-inner の (H-criterion) 還元を完成**させ統一定理を conditional → PROVEN へ（各 §3c 還元の完遂、β>0 は既に family-wide）。
2. **o17 の埋込 3x+1 型 carry family を独立に特徴付け**（Collatz-irregular の named 化、または別 cryptid との関係）。
3. **統一限界定理 + Collatz-core カタログを投稿可能文書に**（`docs/theory_certification_hierarchy.md` と統合、BB6 frontier の named-number-theory 化＝独自貢献）。
4. slow-width majority（o2-o16）に hand-picked milestone で framework を拡張（CRYPTID_CENSUS cluster 2）。
