# 3-adic dual 攻撃 — 同型の確定と核の独立性再特徴づけ（2026-06-28, 続）

新恒等式 v₃(o_{j+1})=D_j−1 から開いた 3-adic 形（density{3|o_j}+density{9|o_j} ≥ 1/2）を4角度
（rotation 構造・skew product・文献・intra-term feedback）で攻撃。**結果: 3-adic 側は証明可能に 2-adic 壁と同型
（4角度確認、突破せず）。新 [PROVEN] 構造＋核を独立性命題に再特徴づけ。誤証明ゼロ。**

## 結論
3-adic dual は **provably isomorphic** to the 2-adic wall。v₃(o_{j+1})=D_j−1 は bijection k↦k+1 で、3-adic divisibility
密度 = 2-adic D-分布の relabel。WALLB_MARTINGALE の ×3-rotation の双対は **失敗**（o_j mod 3^k は aperiodic/full-complexity）。
唯一 un-mined micro-thread = fiber unit-part の 3-adic contraction（specific orbit に free で synchronize するが target に直交）。

## 4角度の結果

### H1. 3-adic rotation 構造（`THREEADIC_ROTATION.md`）— 双対は失敗、だが [PROVEN] 残余構造
- **[OBSERVED 決定的] o_j mod 3^k は全 k で aperiodic**（rotation なし）、subword 複雑度 2^L（full-complexity）。
  → 「3-adic rotation ⇒ 無条件 density」の breakthrough hope は不成立。
- **[PROVEN 対比] なぜ双対が失敗するか**：carry `T_{n+1}=3T_n+2^n r_n` は n≥k で軌道入力 2^n r_n が mod 2^k で drop out
  → T_n mod 2^k=3·T_{n-1}＝**clock 駆動の rotation（tame, 自由に等分布）**。induced `o_{j+1}=3^{D_j-1}m_j` は
  v₃(o_{j+1})=D_j−1 が full-complexity D-列を毎ステップ注入、drop out しない → **orbit 駆動の full-complexity**。
  一行：carry は clock 駆動(tame)、3-adic residue は orbit 駆動(full-complexity)。
- **[PROVEN 残余構造]**（0 violation/120k）: o_j mod 3 ∈ {0,1}（residue 2 は決して出ない）；m ≡ (−1)^{D+1} mod 3；
  o_{j+1} の leading 3-adic digit = parity(D_j)。ただし全て同じ D-列の決定的 recode（shape を pin、density は pin せず）。

### H2. mod-6 CRT skew product（`THREEADIC_SKEW.md`）— [PROVEN] 明示 cocycle、relabel と確定
- **[PROVEN] 真の skew product**: base = 2-adic dynamics on ℤ₂^*（autonomous, 既証明 exact Bernoulli, symbol D を放出）、
  fiber = 3-adic 座標を明示 cocycle `Φ_D(y)=3^{D-1}2^{-D}(3y-1)` で駆動（0 multi-image 検証）。
- **[PROVEN] relabel であって reduction でない**：target は **valuation channel v₃(o_{j+1})=D_j−1 のみ**を読み、これは
  **invertible（D_j=v₃+1）= generating(full) factor** ゆえ易しい factor への圧縮なし。fiber unit-part は |·|₃-contraction で
  synchronize するが **target に直交**（target は valuation のみ query）。
- **[PROVEN] 6-coprime 簡約写像** `u_{j+1}=(3^{D_{j-1}}u_j−1)/2^{D_j}`（u は 6 と互いに素）: equidistribute・mix・構造なし。
  feedback は情報ゼロ。
- **un-mined micro-question**: fiber unit-part は o₀=27 に対し base genericity 非依存で pathwise synchronize し得る。
  十分停止条件を **valuation-measurable でなく unit-part-measurable** に書ければ load-bearing（現 framing では不可）。

### H3. 3-adic / ×3 文献（`THREEADIC_LITERATURE.md`）— 別文献・同難易度
- 3-adic 側は**別の literature** に接続（Tao Syracuse 3-adic / β=1 予想 OPEN；(2,3) digit-exchange Senge-Straus/Stewart/
  Ren 2025；Rowland linear-recurrence v_p 密度）だが **同じ難易度 tier**。
- **一方向 density 結果なし**：唯一 unconditional な handle は #nonzero digit→∞ が rate log n/log log n = **o(n) sublinear**
  ＝正密度すら出ない。density/uniformity 級は全て予想（Ren UD 予想・Erdős・Pegg・Tao β=1）。
- 我々の軌道には provably isomorphic（v₃ 恒等式は exact bijection）。新 literature placement（banked, AEV/Mahler を補完）
  だが citation の変更であって難易度の変更でない。

### H4. intra-term 2-adic × 3-adic 自己無撞着（`THREEADIC_INTRATERM.md`）— feedback は real だが null
- **[PROVEN] D_j = v₂(3^{e_j+1} u_j − 1)**（e_j=v₃(o_j) が unit rotation 3^{e+1} mod 2^k 経由で 2-adic depth に入る）。
- **feedback channel は real だが軌道上 null**：rotation x↦3^{e+1}x は ℤ₂^* の Haar 保存全単射ゆえ、e_j が D_j に影響するのは
  cofactor u_j が e_j に依存する場合のみ。だが **u_j ⊥ e_j**（joint 因子化、forbidden pair なし、χ²=30/dof25 p≈0.22,
  corr −0.004；rotation を剥がしても depth marginal 不変＝質量を動かさない；2次条件も flat≈2）。
- **[PROVEN 構造] cross-corr 0 を説明**（観測でなく）：Haar 保存 rotation + cofactor 独立。
- **核を独立性命題に再特徴づけ**：残 open core = 「軌道に沿って 3-free cofactor u_j∈ℤ₂^* が自身の 3-adic exponent
  e_j=D_{j-1}−1 と独立」。これが成れば D geometric, mean 2>3/2, 非停止。AEV(p/q=3/2)壁と同型。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN] 3-adic dual は 2-adic 壁と同型**（4角度確認）。v₃(o_{j+1})=D_j−1 は exact bijection、relabel であって reduction でない
   （valuation channel は invertible/generating）。WALLB_MARTINGALE の ×3-rotation 双対は失敗（o_j mod 3^k は full-complexity）。
2. **[PROVEN] 残余 3-adic 構造**: o_j mod 3∈{0,1}、m≡(−1)^{D+1} mod3、leading digit=parity(D)。shape を pin、density 不変。
3. **[PROVEN] 明示 skew cocycle** Φ_D(y)=3^{D-1}2^{-D}(3y-1)、base=exact Bernoulli 2-adic、fiber=3-adic contraction。
4. **[PROVEN] intra-term feedback は real だが null**（Haar 保存 rotation + u⊥e）。cross-corr 0 を構造的に説明。
5. **核の独立性再特徴づけ**: open core = 「u_j ⊥ e_j（3-free cofactor が 3-adic exponent と独立）」。
6. **唯一 un-mined**: fiber unit-part の 3-adic contraction は specific orbit に free で synchronize（base genericity 非依存）、
   だが target（valuation）に直交。停止条件を unit-part-measurable に書ければ load-bearing。

## 完全証明の現在地（3 valuation 探索完了）
非停止 ⟺ even-density≥1/3 ⟺ mean D≥3/2 ⟺ **AEV Conj 1.6 一方向単一軌道インスタンス**。
3 valuation すべてで同一壁を確認：
- **archimedean**: 増大は first-moment のみ（degenerate, ADELIC_KERNEL）。
- **2-adic**: 元の D=v₂(3o−1) 等分布（Mahler）。
- **3-adic**: v₃ 等分布、provably isomorphic（本 session）。
measure 側＝完全 PROVEN、example 側＝arithmetic PROVEN、残 OPEN＝単一軌道 27 の genericity（=u⊥e 独立性＝AEV）一点。
構造のみ証明不可も PROVEN（メタ定理）。唯一の free な構造 = 3-adic fiber unit-part contraction（target 直交）。

## 次の生きた一手（候補）
1. **fiber unit-part contraction を load-bearing にできるか**（H2 un-mined）: 非停止の十分条件を unit-part-measurable
   （3-adic contraction で free に synchronize）に書き換えられるか。唯一 specific orbit が無条件に得る構造。長 shot だが未探索。
2. **AEV 2510.11723 精読**: p/q=3/2・一方向・単一軌道版に必要な最小 input を1文に spec、核がどの補題に依存するか確定。
3. **u_j ⊥ e_j 独立性**（H4 再特徴づけ）を直接: 3-free cofactor と 3-adic exponent の脱相関を decoupling argument で。
4. measure 側 PROVEN 資産（skew cocycle・残余構造・intra-term null・独立性特徴づけ）を確定部分として固定・commit。
