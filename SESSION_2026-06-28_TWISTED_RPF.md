# twisted RPF 作用素 L_t の構成・数値化・framing（2026-06-28）

attack d が示唆した「core = twisted-transfer スペクトルギャップ ρ(L_t)<1」を、3角度（構成・熱力学形式・
quenched skeptic）で並列に検証。**結果: 健全性訂正 ＋ core の構造の鋭い同定。誤証明ゼロ。**

## 健全性訂正（前ターンの過剰主張を捕捉）
前セッション `SESSION_2026-06-28_QUENCHED_ATTACK.md` の「**ρ(L_t)<1 ⇔ ‖F‖<1 ⇔ Mahler**」は**誤り**。
正しくは **ρ(L_t)<1 ⇔ annealed cancellation（= Link B, 既に [PROVEN]）**。請求前に捕捉・撤回。

## 3角度の結果

### 1. 構成・数値化（`TWISTED_RPF.md`, `twisted_rpf.py`）
- `next_state(s,b,k) = (⌊3s/2⌋ + b·2^{k-1}) mod 2^k` を exhaustive に確認 = ×(3/2) carry-phase 写像
  `φ_{n+1}=(3/2)φ_n+e_n/4` の k ビット離散化。s/2^k は**位相 φ**（先頭ビット）。
- 3 種の twist 作用素を構成（bit-injection 指標 / diag 指標 / Ruelle 作用素）。
- **[OBSERVED, artifact-free] ρ(L_t) は収束するが rate が誤り**：Lt_inject/Lt_diag → **0.717 ≈ cos(π/4)**
  （k=4→12 で 0.75→0.717）、decay 2^{−0.48n}。Lt_ruelle = 1.000000 厳密（atomic δ₀ 不動点）。
  → **時間一様な有限作用素は「frozen-angle」しか符号化できず、動く角 (3/2)^j を運べない**。
  Mahler rate 2^{−n} を再現しない（matrix iteration は N=1 でのみ Φ と一致、以後 2/π=∫|cos πx|dx に plateau、
  周波数 (3/2)^N が即 alias）。AUDIT_CONTRACTION の drift-to-1 とは別（ρ は収束する）＝**構造的失敗**。

### 2. 熱力学形式 framing（`THERMO_FORMALISM.md`）— 重要な refinement
- **「非格子」条件は2つある**（混同が罠）：
  - **flow 作用素（相関減衰）**: roof = −log λ = log(3/2) = **定数 → 周期が格子 → この鎖は初手で失敗**。
  - **self-similar Fourier 作用素**: 非算術性 = **非Pisot**（3/2 は満たす）、ξ_N=(3/2)^N/8→∞ で評価＝正しい
    大周波数 regime → **viable・citable**。だが ρ(L_ξ)<1 はそこで **literally |ν̂_{2/3}(ξ)|→0 = annealed Φ
    = 既証明 Erdős–Salem Link B**（effective log rate 付）。→ **ρ(L_t)<1 ⇔ annealed、Mahler でない**。
- **pressure は効かない**：確率保存作用素ゆえ leading eigenvalue=1、**P=0 厳密＝熱力学的 slack ゼロ**。
  twist は虚（unitary 指標）、ギャップは**純粋に振動 cancellation（=Dolgopyat/Mahler 入力）から来るしかない**。
- 非コバウンダリ（commit 794b450）は**必要だが非格子より厳密に弱い**（trivial b=0 を消すのみ）、annealed tier のみ供給。
- citable: Solomyak 1906.12164 / Li–Sahlsten 1910.03463 / Varjú–Yu（Rajchman⟺非Pisot, 多項式 rate は
  Diophantine で zero-dim 例外集合外＝2/3 に特殊化不可）; Naud Ann.ÉNS 2005（NLI で resonance-free strip）;
  Dolgopyat Ann.Math.1998（非格子/UNI）; Bourgain–Dyatlov 1704.02909（非線形+sum-product）。

### 3. quenched skeptic 監査（`QUENCHED_OPERATOR_AUDIT.md`）— relocated wall
- **scenery は compact に閉じる（無限メモリではない）**：`e_j = parity(T^j c₀)` は (ℤ₂, T),
  `T(c)=(3c−c mod 2)/2` の位相的 factor（compact ℤ₂、Haar=SRB）。→「自己生成＝無限メモリ」は**偽**。
- **twist は閉じない**：成長する (3/2)^j 重みが **×(3/2) 円写像**を強制 → **古典 Banach 空間（BV/Hölder/smooth）で
  スペクトルギャップなし**。フォーク：mod 2^k 切詰 → 有限・ギャップ有だが = Haar = annealed（j>k の twist 捨象）／
  全 twist ビット保持 → ×(3/2) = Mahler。**両立しない**。
- **ρ(L_t)<1 は equilibrium-generic（a.e.）のみ**で c₀=8 を選ばない（Tao a.e.→specific の壁）。
- annealed（ensemble Φ ~2^{−N}, ただしその指数 rate 自体 ⟨log|cos|⟩=−log2 = 等分布 = Mahler 強度）vs
  quenched（single-orbit time avg A(N) ~N^{−1/2}, i.i.d. surrogate と区別不能）＝**異なる平均・異なる rate**。
  名指し軌道への証明可能 bound は trivial O(1)、観測 N^{−1/2} との差が問題全体。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[訂正・健全性]** ρ(L_t)<1 ⇔ **annealed** cancellation（Link B 既証明）であって Mahler ではない。前主張撤回。
2. **[PROVEN 構造]** Mahler core は **escaping・非再帰な周波数軌道 (3/2)^j→∞ の性質**で、**有限転送作用素の
   スペクトルギャップとして存在しない**（時間一様作用素は frozen-angle のみ／×(3/2) は古典空間でギャップなし）。
   ＝なぜ有限・熱力学形式法が core を短縮できないかの**演算子論的な明確な理由**。
3. **[PROVEN 構造]** scenery（パリティ）は compact ℤ₂ 上 (ℤ₂,T) の位相的 factor（Haar=SRB）。無限メモリでない。
4. **[PROVEN 構造]** P=0 厳密（slack ゼロ）；非Pisot/非コバウンダリは annealed tier のみ供給；flow-roof は格子。

## 新しい攻撃面（vocabulary が開いたもの・攻撃面を狭めない）
- 正しい対象は**無限次元 ×(3/2) / ν_{2/3} 転送作用素**（= 非Pisot Fourier 減衰問題そのもの）。
  攻撃は**anisotropic/Blaschke Banach 空間上の Ruelle 共鳴・resonance-free strip**（Pollicott–Naud,
  Bandtlow–Naud, Baladi）＝ vdC/MR/Bernoulli とは**別の新攻撃面**。ただし target は同じで [OPEN] 義務2つ
  （ギャップ=Mahler／名指し軌道=Tao a.e.→specific）を明示的に背負う。
- **annealed の citable な effective log rate** は banking 済（Link B + Varjú–Yu）。

## 次の生きた一手（候補）
1. **無限次元 ×(3/2) 転送作用素の resonance-free strip** を Naud/Bandtlow–Naud の枠で攻める（新攻撃面）。
2. **a.e.→specific の壁を直接**：c₀=8 を選ぶ機構（計算可能点の等分布、effective Tao）を別途攻める
   ＝3 つの監査が共通に指す「もう一方の壁」。core は実は **(A) ギャップ=Mahler と (B) 名指し軌道選択** の
   2 枚の壁に分解されている。(B) を単独で攻める価値。
3. annealed tier を厳密 partial result として固める（非Pisot ⇒ annealed balance, log rate, 0.7748 閉形式）。
