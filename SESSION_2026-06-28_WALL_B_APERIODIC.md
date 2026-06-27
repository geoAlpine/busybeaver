# wall (B) aperiodic 半分への4攻撃 — GAP LEMMA と系の同定（2026-06-28, 続）

C3 が structured 半分を arithmetic で kill した後、残る **aperiodic/full-complexity 半分**（=非Haar 測度に Birkhoff-generic）を
4角度（不変測度・valuation 鋭化・martingale・renewal）で攻撃。**4本とも aperiodic 半分 = Mahler (A) に収束を確認、
だが新 [PROVEN] 補題1つ＋系の同定＋構造の局在化を獲得。誤証明ゼロ。**

## 4角度の結果

### D1. 不変測度・intrinsic ergodicity（`WALLB_INVARIANT_MEASURES.md`）— 系の同定（共役トラップ回避）
- **[PROVEN/standard] 関連する系の正しい同定**：Antihydra の系は **2-adic ×3/2 写像 T(c)=⌊3c/2⌋ on ℤ₂ ＝ full 2-shift に共役**
  （エントロピー log2、単射 itinerary coding で検証済）。その MME = Bernoulli(1/2) = **Haar、parity=1/2 厳密**。MME と Haar が一致。
  - **conflation トラップを明示排除**：**β=3/2 区間写像 (3/2)x mod1 は別系**（non-sofic β-shift, エントロピー log(3/2),
    MME=Parry 測度、その下で P(digit=1)≈0.1995≠1/2, Gel'fond-Parry 公式 0.19945）。これを「系」と取り違えると parity≠1/2 に
    なるが、それは関連系でない。標的測度（=full shift の MME=Haar）は正しい。
- **[PROVEN] full complexity ≠ unbiased**：MME は一意（Parry/Bowen, Climenhaga-Thompson 2012）だが**特定軌道を選ばない**
  （Barreira-Schmeling 2000: 非 MME-generic 点は full entropy + full Hausdorff 次元）。subword 複雑度 2^k は support/topological、
  genericity は frequency＝独立。full-support biased Bernoulli(p) は複雑度 2^k かつ偏り parity（反例検証）→ 複雑度では排除不可。
  MME-genericity を強制＝単一軌道等分布＝wall (A)。
- net: 不変測度の simplex から **WALLB_NONATOMIC の trichotomy を独立に再導出**（structured=arithmetic out / aperiodic full-support
  =Mahler）＝同じ分割の第2の概念的確認。新角度候補: エントロピー下界 h_limit ≥ log(3/2) の部分抽出。

### D2. 2-adic valuation の鋭化（`WALLB_VALUATION_SHARP.md`）— **[PROVEN] GAP LEMMA（新補題）**
- **[PROVEN] GAP LEMMA**：奇 c_i で `D = v2(3c_i−1)` とすると、**次の奇ステップまでの gap がちょうど v2(3c_i−1) に等しい**
  （3c_i−1=2^D m, m 奇 ⟹ c_{i+1}=2^{D−1}m, その後 D−1 回 halving で次の奇）。N=10^5 まで例外ゼロで検証。
  → budget `Σ_odd v2(3c_i−1) = n + v2(c_n) − v2(c_0)` は **renewal 恒等式「(#renewal)·(平均 gap)=総時間」に collapse**。
    `p_odd·avgD_odd = 1` は「gap=D」以上の arithmetic content を持たない＝**looseness の正確な理由**。
- **large-v2 頻度は arithmetic に bound 不可（(A) に還元）**：3 は 2-adic unit ゆえ `{D_i≥k}={c_i≡3^{−1} mod 2^k}`、奇の中で
  相対測度 `2^{1−k}` の cylinder。`freq(D≥k)` を bound＝induced 軌道の cylinder 頻度制御＝単一軌道等分布。trivial な D≥1
  （#odd ≤ 1.585n）のみ unconditional。
- 数値: depth 列は i.i.d.-geometric（mean 2 ⟹ p=1/2）、corr≈0、`E[D_{j+1}|D_j=k]` は k=1..6 で flat≈2（memory なし）、
  深 seed 軌道は1ステップで depth memory 消失。**self-correcting law なし**＝bias 排除は (A) に還元。
- **本物の positive**: 極値最深点 `o_0≡3^{−1} mod 2^K` は **決定的に self-correct**（K=10..44 で D_1=1）＝genuine arithmetic
  anti-correlation、ただし測度ゼロの極値 cylinder でのみ（uniform/conditional-mean bound に lift せず）。
- **banked [PROVEN]**: GAP LEMMA は非原子的 aperiodic 壁全体を **「induced 奇写像 `o_{j+1}=3^{D−1}(3o_j−1)/2^D` 上で
  v2(3o−1) が geometric 則に従う」一文に局在化**。次の唯一未採掘 arithmetic = 一方向 conditional `E[D_{j+1}|D_j≥k]≤2`
  を positive-measure cylinder で（現状 flat≈2 で gap なし、long shot）。

### D3. martingale / compensator（`WALLB_MARTINGALE.md`）
- **[PROVEN, 確率モデル内] 分解**: `W_N = C_N + M_N`、`M_N`=有界差 martingale ⟹ Azuma で `M_N=O(√(N log N))` **無料**。
  → 障害は全て predictable **compensator** `C_N = Σ E[(−1)^{r_n}|F_{n−1}]` ＝条件付均衡 `E[(−1)^{r_n}|F_{n−1}]=o(1)`。
  caveat: Azuma 無料分は真の確率測度がある場合のみ＝単一決定論軌道には無い。
- **Goldilocks filtration なし（Mahler に再 collapse）**：parity `r_n=c_n mod2=bit_{n+3}(3^n)`＝moving-middle 対角ビット。
  Horn A（low bits of c は bit0=r_n を含む→compensator=全和、vacuous）／Horn B（low bits of T_n は **n のみの関数**＝
  exact ×3 rotation, period 2^{k−2}, 0 violation 検証→無情報→W_N≈M_N=元の決定論和=Mahler）。「現 parity を含まずに予測する」
  filtration は存在しない（parity は深さ≈n、有限 F_{n−1} の foothold から Θ(n) 離れる＝EFFECTIVE_TOPDIGIT の Θ(log N)↔Θ(n) gap）。
- 数値: 任意の coarse predictor の compensator は √N ノイズ、k 増で smaller O(1) predictable part を**発達させない**（overfit のみ）。

### D4. renewal + aperiodicity（`WALLB_RENEWAL_APERIODIC.md`）
- **[PROVEN: gain なし] C3 の aperiodicity は renewal-CLT を特定軌道へ前進させない**：renewal-CLT の欠損は gap 列の量的 mixing/
  stationarity、aperiodicity は測度ゼロの定性的排除でそれを供給しない。残る壁（aperiodic full-complexity biased）自体が aperiodic。
  surrogate S4（biased coin, aperiodic）が反例（mean_gap=2.51≠2, parity 和が線形増大）。
- **[PROVEN: 恒等式] Kac は tautology に退化**：特定軌道で `Σg_i=N` ⟹ `mean_g·even-density ≡ 1`（10桁で 1.0000000000）。
  「mean return→2」は「even-density→1/2」と**文字通り同一**、一歩も弱くない。return-time 分布→Geometric(1/2) は Haar cylinder
  頻度＝(A)。
- 数値（実軌道, N=4·10^5）: mean_g=2.0037, even-density=0.4991, 積=1.0000000000、|Σ(2−g_i)|/√K=1.65=O(1)、
  gap autocorr≤0.0034、return-time 分布 Geometric(1/2) に3桁一致。OBSERVED であり aperiodicity から導出不可。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN 新補題・D2] GAP LEMMA**: 奇 c_i から次の奇までの gap = v2(3c_i−1) 厳密。aperiodic 壁全体を「induced 奇写像で
   v2(3o−1) が geometric」一文に局在化。budget は renewal 恒等式に collapse（looseness の正確な理由）。
2. **[PROVEN/standard・D1] 系の同定**: 関連系=2-adic ×3/2 ≅ full 2-shift、MME=Haar、parity=1/2 厳密。β=3/2 区間写像
   （Parry, 0.1995）は別系＝conflation トラップ明示排除。full complexity ≠ unbiased（Barreira-Schmeling）。trichotomy 独立再導出。
3. **[PROVEN・D3] martingale 分解**: W_N=Azuma 無料 martingale + compensator、Goldilocks filtration なし。
   T_n mod 2^k は n のみの関数（×3 rotation, period 2^{k−2}）。
4. **[PROVEN 恒等式・D4] Kac**: mean_g·even-density≡1。return-time 実測 Geometric(1/2)。aperiodicity は renewal に直交。
5. **[確認] aperiodic 半分 = Mahler (A)** を4独立角度（測度 simplex・valuation・martingale・renewal）で収束確認。

## wall (B) 現在地（更新）
例外集合 = structured/periodic（**[PROVEN] arithmetic 排除**, C3）＋ aperiodic/full-complexity（**= Mahler (A)**, 4角度確認）。
aperiodic 壁は GAP LEMMA で **「induced 奇写像上の v2(3o−1) の geometric 則」一文に局在化**。
唯一未採掘の arithmetic micro-target = 一方向 conditional `E[D_{j+1}|D_j≥k]≤2`（極値 cylinder の決定的 self-correction
D_1=1 は確認済、positive-measure への lift が long shot）。

## 次の生きた一手（候補）
1. **GAP LEMMA の induced 奇写像 `o_{j+1}=3^{D−1}(3o_j−1)/2^D` を主対象に** — v2 の geometric 則を、極値 self-correction
   （D_1=1）を positive-measure cylinder の一方向 conditional 不等式へ lift できるか。唯一未採掘の arithmetic。
2. **h_limit ≥ log(3/2) のエントロピー下界**（D1 示唆）を部分抽出。
3. ここまで（GAP LEMMA, C3 周期排除, 系同定）を **commit**（[PROVEN] 資産が複数蓄積）。
4. annealed tier を partial result として固定。
