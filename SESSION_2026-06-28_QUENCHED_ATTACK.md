# quenched (3/2)^j Korobov 和への4攻撃 — 標的の精密化と新 bankable 成果（2026-06-28）

監査が同定した core（quenched 自己生成 (3/2)^j 指数和 = Mahler/AEV）を、構造的に異なる4攻撃で並列に攻めた。
4本とも core を Mahler に確認したが、**新しい [PROVEN] 成果3つ**と**次の具体的再定式化**を生んだ。誤証明ゼロ。

## 対象
carry bit を支配する quenched Korobov 和 `S_n = Σ_j e_{n-1-j}(3/2)^j`（重み e = 軌道自身のパリティ）。
等価に tan-和 `Σ_j w_j tan(π{(3/2)^j/4})`。その cancellation = even-density→1/2 = 唯一の [OPEN] 行(5)。

## 4攻撃の結果

### a. van der Corput / Weyl differencing（`ATTACK_VDC.md`）— [CLOSED 予想非依存]
- **障害を1つの不等式に確定**：vdC k階微分テストは `max|f^{(k)}|/min|f^{(k)}| = (3/2)^{b-a} = O(1)` を要するが、
  実際は範囲長に対し**指数増大**。Weyl differencing は同じ lacunary 和に**不動点的に写像**し次数を下げない（gap比 3/2>1）。
- **特定 ξ への最良 unconditional bound = trivial O(N)**（o(N) すら未知；(3/2)^n mod 1 の稠密性すら未証明）。
  構造定理は FLP1995（Ω(3/2)≥1/3、support spread であって cancellation でない）と a.e./metric の Salem-Zygmund・
  Algom-Chang-Wu-Wu 2025（単一 ξ に特殊化不可）のみ。
- **相関重みは HURT**：観測 cancellation 率 `N^{1/2}`（random surrogate と区別不能＝generic 挙動）。だが vdC で
  証明可能なのは `N^{1.0}`。**観測 N^{1/2} と証明可能 N^{1.0} の差＝問題そのもの**。

### b. 自己無撞着ブートストラップ（`ATTACK_BOOTSTRAP.md`）— 操作的に循環、だが構造的収穫
- 帰納段に必要な評価 = `A(0,N)=(1/N)Σ(-1)^{bit_n(T_n)}` の o(1) = **Mahler そのもの**（過去 imbalance 仮説は inert）。
- **構造的収穫（新事実）**：障害は**力学にない**ことを数値で確定。復元力なし（corr≈±0.005）、feedback gain≈0、
  `D` は十分統計でない。→ **障害は静的 base 項 A(0,N) に純粋に局在**。因果律（e_n は過去のみ依存）が
  spurious 不動点 δ₀,δ₁ を除去（measure 経路を沈めたもの）。clean な [CONDITIONAL on Mahler] 安定性。

### c. Mauduit–Rivat digit 機構（`ATTACK_MAUDUIT_RIVAT.md`）— 正しい言語、難所を局在化
- MR の心臓（Cauchy-Schwarz + vdC differencing → carry 伝播補題 → 周期 detour s_λ → averaged Fourier 
  `Σ_h|F_λ(h)|=O(q^{ηλ})`, η<1/2）を抽出。適用定理：n²（MR Acta 2009）、素数（MR Annals 2010）、
  Müllner normality、Spiegelhofer、Konieczny。
- **難所を局在化（新事実）**：carry 漸化 `T_{n+1}=3T_n+2^n e_n` は split する。**加法注入 +2^n e_n は MR-tame**
  （局在単一桁加法）。**×3 乗法が壁**（H1 失敗：`3^{n+r}-3^n=3^n(3^r-1)` は 3^n と同オーダー、桁局在しない）。
  → MR は「自己生成ビットでなく**複合幾何 carry ×3 が hard**」と機械的に確定。
- transfer する唯一成分 `F_λ(h)=Π|cos π(α-h/2^i)|` は幾何 ray 上で exp_sum 積 = annealed/Rajchman（easy tier）。

### d. 繰り込み / 0.7748 の構造（`ATTACK_RENORMALIZATION.md`）— **最大の収穫**
- **[PROVEN, 60桁検証] 0.7748 の閉形式**：`C = Π_{m≥1} cos((π/4)(2/3)^m) = √2·ν̂_{2/3}(1/8) = 0.774846171700205…`。
  新しい超越数でなく ν̂_{2/3} の再利用。head=Φ(N)、tail=N非依存=C の cascade で比は**強制**。
- **[PROVEN] 新しい effective floor**：幾何 ladder `log ξ_N ≈ N·ln(3/2)` により、Varjú–Yu の log-in-ξ Rajchman が
  **N に対し多項式 `Φ(N) ≲ N^{−a}`** になる（naive log-in-N より厳密に良い）。**bankable な annealed 下界**。
  ただし観測は指数 `Φ(N)≈2^{−N}`（−lnΦ/N→ln2、N=32768 検証）＝Mahler。self-similarity（恒等式）は N^{−a}→2^{−N} を架けない。
- **次の具体形（新角度）**：quenched 版 = **twisted Ruelle–Perron–Frobenius 作用素** L_t（Antihydra パリティ力学を
  指標 e((3/2)^k/4) で twist）。core を「twisted-transfer スペクトルギャップ問題」として再定式化。
  > **⚠ 訂正 2026-06-28（後続 TWISTED_RPF セッションで判明、健全性）**：ここの主張
  > 「ρ(L_t)<1 ⇔ quenched cancellation ⇔ ‖F‖<1 ⇔ **Mahler**」は**誤り**。正しくは
  > **ρ(L_t)<1 ⇔ annealed cancellation（= Link B, 既に [PROVEN]）**。有限 twisted-carry 作用素は
  > 時間一様なので「動く角 (3/2)^j」を運べず、ρ(L_t)→cos(π/4)≈0.717（rate 2^{−0.48n}）に収束＝frozen-angle
  > であって Mahler rate 2^{−n} ではない。詳細・正しい結論は `SESSION_2026-06-28_TWISTED_RPF.md`。

## このセッションの bankable 成果（誤証明ゼロ）
1. **[PROVEN]** 0.7748 = √2·ν̂_{2/3}(1/8)（閉形式・60桁）。annealed↔Fourier 対応は exact identity。
2. **[PROVEN]** annealed effective floor `Φ(N) ≲ N^{−a}`（Varjú–Yu + 幾何 ladder; log でなく多項式）。
3. **[PROVEN 構造]** 障害は力学でなく静的 base 項 A(0,N) に局在（bootstrap）；難所は ×3 幾何 carry（MR）；
   vdC は予想非依存に [CLOSED]（lacunarity 不等式）。
4. **[新角度]** core = twisted RPF 作用素のスペクトルギャップ ρ(L_t)<1 = ‖F‖<1。具体的演算子問題に。

## 次の生きた一手（攻撃面を狭めない）
- **twisted RPF 作用素 L_t を実際に構成・数値化**（attack d の示唆）。Antihydra パリティ symbolic dynamics の
  転送作用素を指標 twist し、スペクトル半径 ρ(L_t) を測る。‖F‖≈0.04 との整合・ギャップの有無を見る。
  これは ‖F‖<1 を「測る量」から「演算子のスペクトル問題」へ昇格させ、thermodynamic-formalism の道具
  （Ruelle, Parry-Pollicott, Naud の共鳴）を開く。**本命の次手**。
- annealed floor N^{−a} を partial result として banking（citable）。
- MR の split（加法 tame / ×3 wall）を使い、×3 wall 専用の局所評価を Liu-Mauduit 系で攻める。
