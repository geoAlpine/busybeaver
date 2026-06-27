# archimedean × 2-adic 結合 と 最終核（2026-06-28, capstone）

Mahler 障害の核心「archimedean escape × 2-adic proximity の結合」を4角度（adelic/product formula・Baker 対数一次形式・
repeller 歪曲・最終核 synthesis）で攻撃。**結合は壁を破らず（degenerate と判明）、だが新 [PROVEN] 補題2つ＋
完全証明の最終最小核を文献上に正確に位置づけ。誤証明ゼロ。**

## 結論（4角度の収束）
2つの valuation の結合は **height レベルで degenerate**（zero 追加制約）。Mahler 障害は**唯一 refill digit 則 E_deep≤2 に集中**。
完全証明の残る [OPEN] = **AEV normality 予想（arXiv:2510.11723, Conj 1.6）の p/q=3/2・単一軌道・一方向インスタンス**。
他は全て PROVEN。「構造のみ証明不可」（前 session メタ定理）と整合。

## 4角度の結果

### G1. adelic / product formula（`ADELIC_COUPLING.md`）
- **[PROVEN] product formula は first-moment のみ**（log o_n ≈ (ΣD_j)log(3/2)、ratio 0.99999989）、D-分布に制約なし。
  これは N=2^D·m（算術の基本定理）に過ぎない。
- **[PROVEN] 新恒等式**: 3∤(3o−1) ゆえ **v₃(o_{j+1}) = D_j − 1**（0 例外, 2·10⁵ steps）。
  → 2-adic depth を 3-adic 可除性に re-encode：最小命題 ⟺ **density{3|o_j} + density{9|o_j} ≥ 1/2**。
  障害は o_j の 2-adic place と o_{j+1} の 3-adic place で product-formula-locked。難易度の同型であって還元でない。
- Furstenberg/Rudolph/Lindenstrauss ×2×3 は**測度剛性のみ**、仮説未充足（単一軌道は正エントロピー jointly-invariant 測度を
  供給しない、Furstenberg 予想自体 open）→ 単一軌道命題なし。新 live thread: density{3|o_j} への 3-adic dual 攻撃。

### G2. Baker 対数一次形式（`BAKER_LINFORMS.md`）
- **[PROVEN-lit] FLP 1/3 は support/spread**（symbolic dynamics 由来, Baker でない）。Mahler Z-numbers、‖(3/2)^n‖ 下界
  （Zudilin 0.5803^n, Padé 由来）は全て individual-term/support、**density は皆無**。
- **一方向 density bound は導けない**：density は Weyl 和 `Σ e(hθ(3/2)^n)` の cancellation/power-saving を要するが、
  Baker/Padé は pointwise 下界（super-close return なし）＝和で zero cancellation。averaged-vs-pointwise 障壁＝open 等分布。
- 数値: 証明済 individual 下界は問題から **~2500 bits 離れ**（指数スケールで動作、density 問題は O(1) スケール）。

### G3. repeller escape / 歪曲（`REPELLER_ESCAPE.md`）— [PROVEN] Dual-Repulsion Lemma
- **[PROVEN] Dual-Repulsion Lemma**: 各 D=1 ステップで `o'−1 = (3/2)(o−1)` 厳密 → **|o−1|_∞ ×3/2 かつ |o−1|_2 ×2**
  （Countdown）。adelic 積 |o−1|_∞·|o−1|_2 ×3。**o=1 は両 valuation で同時に repel**（300174/300174 検証）。
- re-approach/refill は一方向 bound を**与えない**：freq(D=1)=1−1/E_deep、E_deep=refill=2-adic digit=occupancy=Mahler。
- **combined adelic-height Lyapunov は degenerate**：v₂=1 が全 deep step 開始で成り立つため、2 valuation の balance が
  trivial ΣD 恒等式に collapse、**zero 追加制約**。両者 repel ゆえ正重み adelic 距離は D=1 で減らない、負の archimedean 重み
  （=magnitude-aware Lyapunov α log o + h(o mod 2^k)）が必要で genericity 再導入。**Mahler 障害は refill digit 則 E_deep≤2 に集中**。

### G4. 最終核 + 文献位置（`KERNEL_FINAL.md`）
- **最小核（最鋭）**: **induced 3/2-Syracuse 軌道 o₀=27 の mean D ≥ 3/2**（⟺ c₀=8 の liminf even-density ≥ 1/3）。
- **条件付定理（clean）**: Antihydra は停止しない ⟺ `liminf (1/N)#{n<N: D(o_n)≥2} ≥ 1/2` ＋ 有限 check（n≤N₀ で balance_n≥0）。
  逆も成立（liminf even-density<1/3 ⟹ balance→−∞ で停止、1/3 閾値は厳密）。Haar 下（T exact, mean D=2, PROVEN）では余裕で成立、
  全内容は単一軌道 27 が Haar-generic か否か。
- **文献の正確な位置**: 唯一の named home = **AEV normality 予想（arXiv:2510.11723, Conj 1.6）**＝⌈(3/2)x⌉ の単一軌道 mod 2^k 等分布。
  我々の核はその **p/q=3/2・単一軌道・mod-2^k インスタンス**。FLP/Mahler は **support 軸（直交）**。AEV は Mahler/Flatto/Akiyama/
  Dubickas-Mossinghoff の傘。
- 我々の核は AEV より**厳密に弱い**（一方向・≥1/3 で =1/2 でない）が、その弱いレベルに named 予想なし → AEV が最弱の named。
- **公表された一方向/density 結果で特定軌道の liminf even-density ≥1/3（or >0）を与えるものは無い**（FLP=support、Tao=出発点
  ensemble、KL=出発整数 count、Birkhoff=軌道は transient で不変確率測度なし）。唯一 unconditional な単一軌道事実は mean D≥1
  （even-density≥0）。**核は genuinely open、stop 固定点 o=1 の proven 障害で orbit-specific**。
- **FLP spread → density の既知ルートなし**（軌道は full spread でも empirical 測度が集中し得る=メタ定理の δ₁ drift）。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN] Dual-Repulsion Lemma**: D=1 で |o−1|_∞ ×3/2、|o−1|_2 ×2、adelic 積 ×3。o=1 は両 valuation で repel。
2. **[PROVEN] 新恒等式 v₃(o_{j+1}) = D_j − 1**：最小命題 ⟺ density{3|o_j}+density{9|o_j} ≥ 1/2（3-adic 形）。
3. **[PROVEN/definitive negative] archimedean × 2-adic 結合は height レベルで degenerate**（zero 追加制約、trivial ΣD に collapse）。
   Mahler 障害は唯一 refill digit 則 E_deep≤2 に集中。Baker/Padé は density から ~2500 bits 離れ（averaged-vs-pointwise 障壁）。
4. **[最終核確定] 完全証明 = AEV 予想（2510.11723）の p/q=3/2・単一軌道・一方向インスタンス、他は全 PROVEN**。
   核は AEV より弱い（一方向 ≥1/3）が named 予想はその上の AEV のみ。

## 完全証明の現在地（今日の到達点 = capstone）
非停止 ⟺ even-density≥1/3 ⟺ mean D≥3/2（induced 3/2-Syracuse 軌道 o₀=27）⟺ **AEV Conj 1.6 の一方向単一軌道インスタンス**。
- **measure 側 = 完全 PROVEN**（induced map は exact・Haar 保存・Bernoulli, E4）。
- **example 側 = arithmetic で PROVEN**（周期軌道排除 C3、Countdown Lemma、Dual-Repulsion）。
- **残 [OPEN] = 単一軌道 27 の Haar-genericity（AEV）一点**。しかも「構造のみでは証明不可」が PROVEN（メタ定理、障害 o=1）。
攻撃面は3本 valuation（archimedean/2-adic/3-adic）全て探索し、結合は degenerate と確定。核は名前付き active-frontier 予想に着地。

## 次の生きた一手（候補）
1. **3-adic dual 攻撃**（G1 の v₃(o_{j+1})=D_j−1）: density{3|o_j} を 3-adic 側から。intra-term の 2-adic×3-adic 自己無撞着
   （v₂(3o−1)=D & v₃(o)=D_prev−1, cross-corr 0 だが intra-term 未探索）を突く。唯一 un-mined thread。
2. **magnitude-aware Lyapunov α log o + h(o mod 2^k)**（F1/G3 残し）: size drift を組み込む非有界 sub-action（genericity 再導入だが
   一方向 ≥1/3 の弱さが効くか）。
3. **AEV 2510.11723 を精読**し、p/q=3/2・一方向版に必要な最小 input を1文に spec.（核が AEV のどの補題に依存するか）。
4. measure 側 PROVEN 資産（exact Haar 保存・Countdown・Dual-Repulsion・v₃ 恒等式・条件付定理）を完全証明の確定部分として固定・commit。
