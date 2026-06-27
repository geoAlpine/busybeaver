# AEV 2510.11723 精読 — 核の正確な文献位置と最良経路（2026-06-28, 続）

残る genericity 核そのもの = AEV 予想を精読。論文を実際に取得し3角度で分析。
**結果: 我々の核 = AEV Conj 1.6（floor mirror）の triple-fragment（一方向・単一 level k=2・単一軌道）と確定。
AEV は2025/10 の conjecture paper（解析的 handle ゼロ）で部分結果なし。最良経路 = effective Fourier-decay rate
（ただし annealed/quenched gap は既知のまま）。誤証明ゼロ。**

## 論文の正体（J1）
**arXiv:2510.11723**, M. Andrieu, S. Eliahou, L. Vivion（=AEV 確認）, *"A Normality Conjecture on Rational
Base Number Systems"*, v1 2025-10-06 / v2 2026-04-07, math.NT+CO。rational-base 数体系（Akiyama-Frougny-
Sakarovitch）の minimal/maximal word の正規性。**写像は CEILING `T_{p/q}(x)=⌈px/q⌉`**（floor でない）。

### verbatim 核心命題
- **Conj 1.6**: 「p>q≥1 互いに素。全 n>0・全 k≥0 で、`T_{p/q}(x):=⌈px/q⌉` 反復列 (T^l(n))_l は mod q^k の
  residue class で equidistributed」＝**全軌道 mod q^k 等分布**。3/2 では ⌈3x/2⌉ の全軌道が mod 2^k 等分布。
- **Conj 1.2**: minimal/maximal word が正規。**Conj 1.4**: p<q² で Z-number 不在（3/2 で = Mahler 1968 Z-number 予想）。
- **Thm 1.7 [PROVEN]**: Conj 1.2 ⇔ 1.6（正規性 ⇔ 等分布）。**Thm 1.5 [PROVEN]**: p<q² で Conj 1.2 ⇒ 1.4。
- **p<q² は 3/2 で成立**（3<4）→ Conj ⇒ Mahler。

### proven/open 境界・方法
- PROVEN: 構造的同値（Thm 1.7, 1.5）のみ。OPEN: Conj 1.2/1.4/1.6 すべて、全 base（3/2 含む）。
- 方法: **combinatorics on words + 計算機実験のみ**。ergodic 理論・transfer 作用素・指数和・Fourier いずれも**不在**。
  解析的等分布は完全に open。3/2 に unconditional な結果**ゼロ**（10^6 letter の数値実験のみ、discrepancy は Philipp LIL 様）。

## 核 ↔ AEV の正確な dictionary（J2）
- **AEV は CEILING `(3x+1)/2`（奇）、Antihydra は FLOOR `(3x−1)/2`（奇）**。±1 が parity を flip → **literally conjugate でない**
  （even 枝は同一）。これが bookkeeping を v₂(3o−1) で回す理由。我々の GAP-LEMMA が橋。
- 我々の induced 奇写像 = floor-T_{3/2} 軌道の奇整数への return map。AEV 全軌道の sub-object。
- even-density = mod-2(k=1) 頻度、freq(o≡3 mod4) = mod-4(k=2) 頻度、mean D=Σ_k freq(o≡3⁻¹ mod 2^k) = 全 mod-2^k
  residue profile = Conj 1.6 の q=2 データ。
- **AEV 正規性 = 各 class 頻度ちょうど q^{-k}（two-sided・全 level・全 n）**。
- **我々の核は3軸で厳密に下**：①一方向(≥1/2) vs two-sided(=1/2) ②単一 level k=2 vs 全 k ③単一軌道(o₀=27) vs 全 n。

### 最小 lemma（核）
**IF `liminf_N (1/N)#{n<N: o_n≡3 mod4} ≥ 1/2`（≡ liminf even-density≥1/3 ≡ mean D≥3/2）＋有限 check
THEN Antihydra 非停止**。= **AEV Conj 1.6（floor mirror）の p/q=3/2・level k=2・一方向・単一軌道 fragment**。
full AEV は =1/2 で margin 付き closure。

### AEV は fragment を証明するか — NO
PROVEN は Thm 1.7（同値）と Thm 1.5（conjecture からの片方向）のみ。**unconditional な residue-frequency 結果は
一方向すら存在せず**。weaker 版は AEV で**未言及・open**。

## 方法・部分結果 hunt（J3）
- AEV proven 結果は初等/組合せのみ、conjecture は**計算機実験のみ**で支持。解析的 handle ゼロ。
- 部分結果: (a)一方向 density 下界 (b)特定軌道 effective 等分布 (c)単一軌道の正密度時刻集合 (d)log3/log2 条件付 —
  **すべて NONE proven**。量的結果(Koksma, Aistleitner LIL/CLT)は全て **metric(ほぼ全 x)**、軌道 27 に無言。
  Aistleitner: 特定 x の {x^n} u.d. は「notoriously difficult, few partial results」、typical x の metric **下界すら無い**。
- FLP Ω(3/2)>1/3 は **range（位相的閉包）であって density でない**。Dubickas subword-complexity は richness で frequency でない。両方 wrong axis。
- **hard regime p<q²(3/2: 3<4)で特定 3/2-軌道の unconditional liminf even-density>0 は存在しない**。{(3/2)^n} mod1 は
  稠密すら未証明。正の結果は easy regime p>q² のみ（3/2 で方法が構造的に破綻）。

### 最有望技法（J3 提案）＋ 健全性 caveat
- J3 提案: **3/2 非Pisot に紐づく effective Fourier-decay / 指数和 cancellation を弱い ≥1/3 標的へ**。
  我々は既に [PROVEN] (984f70f): 3/2 非Pisot ⇒ ν_{2/3} Rajchman(Fourier→0)。missing = **effective POWER decay rate
  |ν̂(t)|≤C|t|^{-a}**（bare Rajchman でなく rate）。rate → Erdős–Turán → liminf even-density≥1/2−O(decay)、1/3 を margin で clear。
  rate の出所候補: Streck（非Pisot Bernoulli convolution の power decay, 代数 parameter）, Varjú-Yu, Brémont, Bourgain-Dyatlov。
- **⚠ 健全性 caveat（NONPISOT_FOURIER_CHAIN Link C と照合）**: ν_{2/3} の Fourier decay は **annealed(i.i.d. 重み)**＝
  measure 側。軌道 even-density は **quenched** Weyl 和 Σe(h·4·(3/2)^n) を要する。Erdős–Turán は**軌道自身**の Weyl 和を要し、
  ν̂_{2/3} はそれを直接 bound しない（Link C で「analogy, broken link」と確定済）。→ effective rate は我々が既に得た
  **annealed floor Φ(N)≲N^{-a}** を与えるが、quenched 軌道 density には同じ gap が残る。J3 の楽観はこの gap を跨いでいる。
  **正直な評価: AEV 精読は新 breakthrough 経路を出さず、既知の annealed/quenched 壁を再確認した**。

## このセッションの bankable な結論（誤証明ゼロ）
1. **核の正確な文献位置確定**: 我々の核 = **AEV Conj 1.6（floor mirror）の triple-fragment**（一方向・level k=2・単一軌道）。
   AEV は2025/10 の conjecture paper、解析的 handle ゼロ、部分結果なし、Conj 自体が58年来の Mahler Z-number 予想を含意。
2. **floor vs ceiling 関係を精密化**: AEV=⌈3x/2⌉(parity 反転)、Antihydra=⌊3x/2⌋、conjugate でない、GAP-LEMMA(v₂(3o−1))が橋。
3. **部分結果は文献に皆無**（一方向 density すら）。WALLB_EFFECTIVE/KERNEL_FINAL の「特定軌道 liminf even-density>0 なし」を AEV が再確認。
4. **最有望解析技法 = effective power Fourier-decay rate**（Streck/Varjú-Yu）だが、**annealed/quenched gap（NONPISOT Link C）は
   未解決のまま**＝AEV 精読は既知壁の再確認で新経路を出さず（J3 楽観に健全性 caveat）。

## 完全証明の最終 capstone 像
非停止 ⟺ even-density≥1/3 ⟺ mean D≥3/2 ⟺ **AEV Conj 1.6（floor mirror）の一方向・level-2・単一軌道 fragment**。
- measure 側 = 完全 PROVEN（exact Haar 保存 Bernoulli Syracuse 系）。
- example 側 = arithmetic PROVEN（周期排除・Countdown・Dual-Repulsion・v₃ 恒等式）。
- 構造のみ証明不可 = 2 独立メタ定理 PROVEN（β=+1/2 at o=1 / free 構造は o=1 共有）。
- **残 OPEN = 核 = 2025/10 の名前付き予想（AEV）の triple-weakened fragment、解析的 handle は文献に存在せず、
  唯一の候補(effective Fourier rate)も annealed/quenched gap を跨げない**。
= **完全証明は「1つの brand-new 名前付き予想の最弱 fragment を除いて全 PROVEN」という状態に到達**（remarkable, 投稿可能）。

## 次の生きた一手（候補）
1. **annealed/quenched gap を正面から**（NONPISOT Link C の broken link）: ν_{2/3} の effective decay を軌道自身の Weyl 和へ
   push する quenched 化。これが唯一の解析的 missing link で、AEV も跨げていない真の frontier。
2. **AEV の組合せ richness 経路**（Conj 1.2 側、subword complexity）: 数値で cheap な部分進捗が可能と AEV 自身が示唆、
   一方向 fragment に組合せ的下界が付くか。
3. **floor-mirror Conj 1.6 を AEV 著者に伝える / 一方向 single-orbit fragment を独立命題として定式化**（記録・投稿）。
4. **全 PROVEN 還元鎖 + 残 OPEN(AEV fragment) を投稿可能な capstone 文書に統合**（完全証明の現在地を1本に）。
