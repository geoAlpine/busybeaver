# wall (B) 深掘り — a_n⊥b_n と非原子的例外集合（2026-06-28, 続）

wall (B) を、前回出た弱い標的 a_n⊥b_n を軸に4角度で深掘り。
**結果: [PROVEN] 前進1つ（非原子的例外集合の structured 半分を arithmetic で排除）＋ bilinear 経路の決定的決着＋健全性訂正。誤証明ゼロ。**

## 4角度の結果

### C1. 脱相関の構造・文献（`WALLB_DECORR_STRUCTURE.md`）
- a_n⊥b_n は「digital function の joint distribution/独立性」**ジャンルだが定理は存在しない**。既発表の脱相関結果
  （Bésineau, Kim, Drmota, Drmota–Mauduit–Rivat Duke 2020, Hofer–Iacò–Tichy）は全て**乗法独立な2つの base**
  （log q₁/log q₂ 無理）から独立性を引く＝Riesz 積/相互特異性。我々は **同一 base 2・同一乗数 3/2・同一位置 n** で
  第2の base がない → 文献のエンジンが構造的に使えない＝単一乗数フロンティア（2504.18192 Problem 3）。[OPEN]
- **最有望な弱化 = 条件付/innovation 形 `E[(−1)^{a_n} | F_{n−1}] = o(1)`**（martingale 差、「最新位相が carry 重み付き過去から
  decouple」）。各因子の等分布より厳密に弱い（1つの条件付1次モーメント vs 全区間）。だが閉ループ r=a⊕b が同じ
  (3/2)^n Mahler 位相に再アンカー、coupling_brick は大域/測度（局所でない）decoupling のみ実現可、と honest caveat。
- 数値（N=200000）: cross-corr `A_r·√M`=O(1) で符号振動＝独立2均衡 digital function と同じ √-cancellation。
  lagged corr(a_n,b_{n+k}) k=−12..12 全て white（on-lag +0.17σ）。surrogate（Thue-Morse/Rudin-Shapiro/独立 carry）と
  **区別不能**＝conspiracy なし。

### C2. joint への bilinear van der Corput（`WALLB_BILINEAR_VDC.md`）— 決定的決着
- **厳密整数恒等式（0 mismatch, 再検証済）**: `8·3^n = 2^n c_n + T_n`（c_n=実軌道）。2^{n+1} で割ると
  **`φ_a(n) − φ_b(n) = c_n/2 mod 1 = r_n/2 ∈ {0, ½}`**。→ 2位相は **phase-locked**（fast part 4(3/2)^n を完全共有）。
- ⟹ **`(−1)^{a_n}(−1)^{b_n} = (−1)^{r_n}` 厳密** ⟹ cross-correlation `C_N ≡ W_N/N` 恒等的。
- **[CLOSED] bilinear/type-II 経路**: 差モード（diagonal）は fast (3/2)^n velocity=0 で消えるが、残差は raw parity
  `r_n ∈ {0,½}`＝微分なき2値ステップで vdC テスト空虚。和モードは lacunary のまま。**a/b 分割は原理的に help しない
  ——積が parity kernel に厳密 re-fuse**。前回の「a_n⊥b_n は dodgeable な弱い標的」は幻と判明（健全性訂正、SESSION_WALL_B 反映）。
- net asset: 恒等式 `φ_a−φ_b=c_n/2` は **joint object に parity r_n を超える自由度がない**ことを示す＝分割戦略の原理的限界を確定。

### C3. 非原子的例外集合の排除（`WALLB_NONATOMIC.md`）— **[PROVEN] 前進**
非原子的偏り軌道（empirical 測度が ν(odd)≠1/2, ν∉{δ₀,δ₁} に集積）を ergodic 分解で2分：
- **structured 半分（eventually-periodic itinerary）= [PROVEN] arithmetic で排除（真の gain）**：
  パリティ coding は単射（検証済）→ eventually-periodic itinerary ⟺ eventually-periodic 点。
  T の周期-q cycle は `c0 = N/(3^q − 2^q)`, `N = Σ 2^j 3^{q-1-j} e_j ≤ 3^q − 2^q`（等号は all-odd）→
  **全 cycle 点は [0,1] 内、整数なのは両端点（=atoms）のみ**。非原子的周期 cycle は (0,1) の奇分母有理数で
  整数 c0≥2 になり得ない（例 (001)^∞ = 4/19；q≤10 の全2046 cycle で網羅検証＋一般 bound）。
  整数軌道は厳密増大（T(c)−c=⌊c/2⌋≥1）→ 周期点に到達しない → **itinerary は eventually-periodic でない**。
  非循環・等分布不仮定。**旧 micro-asset（atoms=period-1 のみ）を全周期に強化**。
- **unstructured 半分（aperiodic, 非Haar ν に Birkhoff-generic）= (A) Mahler に還元**（2-adic valuation budget
  `Σ_odd v2(3c_i−1)=n+v2(c_n)−v2(c0)`、偏り p≠1/2 ⟹ avgD_odd≠2 = cylinder 頻度 = 等分布。純 arithmetic 障害なし）。
- 数値（option c: 偏り整数軌道は存在するか）: 4000 start 探索（max|z|=3.51=fair-coin Gaussian 端値）、強制偏り start
  全て balance に減衰、最偏候補も延長で消失（z: −3.51→+1.36→−0.22, avgD_odd→2）。**偏り整数軌道は観測されず**。

### C4. effective 有限証明（`WALLB_EFFECTIVE.md`）— 健全性訂正
- **「1/6 effective tail」は単独では何も保証しない**＝proven implication の**仮説**であって proven bound でない。
  [PROVEN] は (i) 有限 check `balance_n≥0` (n≤N₀) と (ii) 初等代数 `|dev|<1/6 ⟹ balance>0` のみ。
  `|E_n/n−1/2|<1/6` 自体は **[OPEN]**（slack 付きの標的の言い換え）。liminf≥1/3 すら unconditional には未証明。
- **self-improving bootstrap は証明可能に不在**：automatic（subword 複雑度 p(k)=2^k 最大）・sofic（3/2 非Pisot ⇒ β-shift
  非 sofic, Frougny）・有限巡回群帰着（T_n は S-unit でない、=BC 機構不在）の3経路とも閉。bootstrap は §3.6
  effective-equidistribution 定理に**ならざるを得ない**＝line (5) を短絡しない。bbchallenge の「regular 証明書なし」壁と同一。
- **FLP の 1/3 は support/spread bound で frequency/density bound でない**＝prompt の前提が wrong-axis。
  1/3↔1/3 一致は numerology（両方 ×3 の 3 由来、別軸）。真のギャップは **kind であって size でない**：
  proven={top Θ(log N) digit effective + support≥1/3}（両軸とも不足）、必要=中間 digit の effective **frequency**=wall (B)。
- 生産的閉：解析的壁と bbchallenge の certificate 壁を**統一**（共に full-complexity/non-sofic）。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN 前進・C3]** 整数 Antihydra 軌道は **eventually-periodic itinerary を全周期で排除**（cycle 点は (0,1) 奇分母有理数、
   整数は atoms のみ；軌道は厳密増大）。→ wall (B) の例外集合のうち **structured（周期的）半分を arithmetic で kill**、
   残るは aperiodic（full-complexity）半分＝Mahler のみ。等分布不仮定の真の縮小。
2. **[PROVEN 構造・C2]** `8·3^n = 2^n c_n + T_n` ⟹ `(−1)^{a_n+b_n}=(−1)^{r_n}` 厳密。a/b 分割は原理的に help せず
   （cross-corr が parity kernel に恒等 re-fuse）。bilinear/type-II 経路 [CLOSED]。前「弱い標的」楽観を訂正。
3. **[OPEN・C1]** digit-carry 脱相関は単一乗数フロンティアの定理なし領域。最弱の真の reformulation=
   条件付 `E[(−1)^{a_n}|F_{n−1}]=o(1)`（martingale 差）だが同じ Mahler 位相で終端。
4. **[健全性訂正・C4]** 1/6 tail は標的であって定理でない；FLP 1/3 は support であって frequency（1/3→1/2 は wrong-axis）；
   effective bootstrap は証明可能に不在；wall (B) は bbchallenge の no-regular-certificate 壁と統一。

## wall (B) の現在地（明確化）
wall (B)（名指し点 (3/2)^n 等分布）の例外集合は **2分**された：
- **structured/periodic** → **[PROVEN] arithmetic で排除**（C3, 真の (B)-単独 gain）。
- **aperiodic/full-complexity** → Mahler (A) に還元。
→ 残る wall (B) は「**aperiodic・full-complexity と既知の軌道が、非Haar 測度に Birkhoff-generic でないこと**」に純化。
   周期的障害は消えた。これが (A) と独立に取れた (B) の前進。

## 次の生きた一手（候補）
1. **条件付/innovation 形 `E[(−1)^{a_n}|F_{n−1}]=o(1)`（C1）を martingale/予測子の枠で攻める** — 最弱の真の reformulation。
   carry filtration F_{n−1} に対する最新位相 a_n の予測不能性。Mahler に終端するが、部分 conditional 評価が取れるか。
2. **C3 の aperiodic 半分を、full-complexity という既知事実をレバーに攻める**（subword 複雑度 2^k は等分布の必要条件側、
   十分性に何が要るか）。
3. wall (B) 成果を含め commit（structured 半分の [PROVEN] 排除は記録価値大）。
4. annealed tier（非Pisot⇒balance, log rate, 0.7748）を partial result として固定。
