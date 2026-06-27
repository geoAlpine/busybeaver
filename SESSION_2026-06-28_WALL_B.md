# wall (B)（名指し軌道選択 = Tao a.e.→specific）単独攻撃（2026-06-28）

core を分解した2枚の壁のうち (B) を、Mahler (A) を所与として4角度で並列攻撃。
**結果: (B) の本質が大きく精密化 — (B) は自己参照でなく explicit な 8·3^n に宿る + 新しい(より弱い)標的 a_n⊥b_n 出現。誤証明ゼロ。**

## 4角度の結果

### B1. 例外集合の特徴付け（`WALL_B_EXCEPTIONAL_SET.md`）— 近道なし確定
- b=3/2 では例外集合 E は**特徴付け不能・membership 判定不能**（normality/Diophantine/連分数いずれの特徴付けも存在しない；
  E は Lebesgue-null だが**完全 Hausdorff 次元**・自己相似）。整数 base（Wall の定理で E=非正規数、特徴付け可）と鋭い対比。
- 「c₀=8 は E に属すか?」は論理的に「{4(3/2)^n} は等分布するか?」と**同一** = oracle 不在。explicit な x=4 すら Mahler 級 open。
- 数値: x=4 の discrepancy は generic random x の中央値と各 N で一致（むしろやや一様）。anomaly なし。

### B2. 自己参照による選択（`WALL_B_SELF_SELECTION.md`）— 循環、だが PROVEN micro-asset
- 軌道は (ℤ₂, T, c₀=8), T(c)=(3c−(c mod2))/2 の単一前方軌道。閉ループ ψ_{n+1}={(3/2)ψ_n+e_n/4}, e_n=1[ψ_n∈奇半]。
  Koksma の「a.e. x」は1点軌道上で空虚 → a.e.→specific の壁そのもの。
- **[REFUTED 大域]** 最クラスタ配位 δ₀(c=0)・δ₁(c=1) は self-consistent 不動点 → クラスタは self-consistency で排除されない。
- **[PROVEN micro-asset]** 整数 c₀≥2 は非有界に増大 → **クラスタ atom {0,1} に決して吸引されない**。
  → 等分布の失敗があるなら**非原子的 Diophantine クラスタリングに限る**。証明が排除すべき例外集合を
  （等分布を仮定せず）**atom 分だけ厳密に縮小**。
- クラスタ破壊の含意「偏ったパリティ ⇒ (3/2)^j 重み carry 和が再均衡」= Mahler core そのもの＝**ここで循環**（bias 仮説 inert, gain≈0）。
- 数値: 能動的復元力なし。強制クラスタは**start 非依存の極限法則で希釈**されるだけ（その法則こそ証明対象）。

### B3. specific-point 等分布の文献（`WALL_B_SPECIFIC_LITERATURE.md`）— 正確な文献配置
- a.e.→specific を越える既存枠は2つ＋near-miss: ①構成的正規数（Champernowne 等、digit を**設計**、整数 base、我々は軌道所与で不可）
  ②**Bailey–Crandall Stoneham**（特定定数 α_{b,c} の b-正規性を**証明**、Wall 基準+hot-spot、唯一の「特定点+力学的等分布+証明済」成功）
  ③near-miss: Rajchman ⟹ self-similar 測度の**pointwise** 正規性（arXiv:2504.18192）— ν_{2/3} で発火するが ν-a.e. のみ。
- **Bailey–Crandall が b=3/2 で壊れる正確な理由**（漸化は y_{n+1}=b·y_n+r_n の**全く同じ形**, b=3/2）：
  ①整数 b は bx mod1 が Lebesgue 保存・full shift だが b=3/2 は β-変換, Parry 測度≠Lebesgue, 制約 shift
  ②**3/2 非Pisot ⇒ β-shift は sofic ですらない**（Frougny: automaton⟺Pisot）= 有限状態 digit 構造なし
  ③**決定的: Stoneham が無条件なのは b^{c^m}α が有限巡回群 (ℤ/c^nℤ)* の b^k mod c^n に帰着するから。
    非整数 b=3/2 では b^k mod c^n が無意味＝有限群帰着が存在しない**（PROOF_STATUS §2 の T_n が S-unit でないのと同質）。
- **正確な文献配置（重要）**: Antihydra wall (A)+(B) は arXiv:2504.18192 の **Problem 1(effective rate)+Problem 3(非整数 base)**
  = 分野自身の open problem と**文字通り一致**。AEV 2025（arXiv:2510.11723）Conj 1.2/1.6 = 我々の壁の言い換え。
  → Antihydra は active frontier の**名前付き特殊例**。外部 tool でなく同じ open。

### B4. どの部分が wall (B) を担うか（`WALL_B_WHICH_PART.md`）— 最大の精密化
- a/b 分解は faithful（実 Hydra 軌道パリティと N=60000 で 100% 一致、offset 0）。
- **[PROVEN] wall (B) は explicit な半分 a_n = bit_n(8·3^n) に既に完全に宿る**：厳密整数恒等式（n<20000, 0 mismatch）
  `a_n=0 ⟺ {4·(3/2)^n}∈[0,½)`, `{4(3/2)^n}=(8·3^n mod 2^{n+1})/2^{n+1}`。
  → 「名指し点 (3/2)^n 等分布」は**自己参照と無関係**、非自己生成の explicit a_n に incarnate。
  自己生成は b_n に全部住む（= wall A の quenched 側）。**(B) の framing 訂正: 名指し点は explicit 8·3^n であって軌道の自己選択でない。**
- **[OBSERVED] a_n と b_n は交差脱相関**（Pearson −0.0014 ≈ 0, PROOF_STATUS §3.2 と一致）。
- **新しい(より弱い)標的**: 停止は r_n のみ依存 → 証明に必要なのは `A_r→0 ⟺ a_n ⊥ b_n`（漸近直交）**のみ**で、
  **各々の均衡より弱い**。a_n⊥b_n かつ b_n 均衡なら a_n が均衡せずとも A_r→0。
  → **a_n の specific-point Mahler は厳密には dodgeable**（b_n + 脱相関 経由で explicit (3/2)^n 点に触れずに済む経路）。
  [CONDITIONAL]: a_n⊥b_n の証明は両 (3/2)^n 構造を結合、おそらく同程度に hard。**真の binding object = joint a_n⊥b_n 脱相関**（壁 A と B を結合）。
  > **⚠ 精密化 2026-06-28（後続 WALL_B_DEEP, C2 で判明）**：「dodge」は幻。厳密整数恒等式
  > `8·3^n = 2^n c_n + T_n` ⟹ `φ_a − φ_b = c_n/2 = r_n/2 ∈ {0,½}` ⟹ **(−1)^{a_n}(−1)^{b_n} = (−1)^{r_n} 厳密**。
  > つまり a_n⊥b_n の cross-correlation は raw kernel `(1/N)Σ(−1)^{r_n}` と**恒等的に同一**で、b_n 経由で
  > explicit 点を回避する経路は存在しない（積が parity kernel に re-fuse）。a_n⊥b_n は「a_n と b_n を各々均衡」
  > より弱いが、**新しい easier object ではなく even-density 標的そのもの**。bilinear/type-II 経路は [CLOSED]。
- 数値 rate（N=60000）: a_n slope −0.399, b_n −0.479（clean √-cancellation 最接近）, r_n −0.397。A_r ≈ A_a·A_b ≈ 0。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN 訂正]** wall (B)（名指し点 (3/2)^n 等分布）は**自己参照でなく explicit な a_n=bit_n(8·3^n) に宿る**。
   恒等式 `a_n=0 ⟺ {4(3/2)^n}∈[0,½)`。前 framing「(B)=自己生成軌道の選択」を訂正。
2. **[PROVEN micro-asset]** 整数 c₀≥2 はクラスタ atom {0,1} に吸引されない → 排除すべき例外集合を非原子的 Diophantine に縮小。
3. **[PROVEN/文献]** b=3/2 で E は特徴付け・判定不能；Bailey–Crandall は非整数 base の有限群帰着不在で壊れる（3点とも非Pisot）。
4. **[新標的・潜在的に弱い]** 証明に必要なのは a_n⊥b_n（joint 脱相関）のみで各均衡より弱い。壁 A・B を結合する binding object。
5. **[文献配置]** Antihydra (A)+(B) = arXiv:2504.18192 Problem 1+3 / AEV 2025 Conj の名前付き特殊例 = active frontier。

## 次の生きた一手（候補）
1. **新標的 a_n⊥b_n（joint 脱相関）を直接攻める** — 各均衡より弱い唯一の binding object。explicit digit と
   self-generated carry の漸近直交。coupling_brick の既存材料を再利用。**最も新しく潜在的に最短**。
2. **micro-asset を拡張**: 整数増大 + carry 構造が**非原子的** recurrent-but-unbalanced 2-adic 軌道も排除するか
   （B2 が残した (B) の唯一 (A) と非同一な sub-question）。
3. arXiv:2504.18192 の Rajchman⟹pointwise-normality を**非整数 base に拡張**する path を track（分野の Problem 3）。
4. annealed tier（非Pisot⇒balance, log rate, 0.7748 閉形式）を partial result として固定。
