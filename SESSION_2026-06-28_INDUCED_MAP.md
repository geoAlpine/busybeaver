# induced 奇写像への4攻撃 — [PROVEN] Syracuse 定理 と壁の最大局在化（2026-06-28, 続）

GAP LEMMA が局在化した induced 奇写像 `T(o) = 3^{D−1}(3o−1)/2^D`（D=v₂(3o−1)、o₀=27 ← c₀=8→12→18→27）を
4角度（Collatz 共役・一方向 drift・Tao 法・residue 構造）で攻撃。**新 [PROVEN] 定理＋壁の最大局在化を獲得。誤証明ゼロ。**

## 標的の正しい形（重要）
証明に必要なのは even-density **≥ 1/3**（= balance_n=3E_n−n≥0）であって =1/2 ではない＝**一方向**。
renewal 恒等式で **even-density = 1 − 1/(mean D)** ⟹ **even-density ≥ 1/3 ⟺ mean D ≥ 3/2**（D≥1 ゆえ危険は D=1 過多のみ）。

## 4角度の結果

### E1. Collatz / Lagarias 2-adic 共役（`INDUCED_COLLATZ_CONJUGACY.md`）
- **[PROVEN/cited]** Lagarias 共役 `Q_∞: ℤ₂→ℤ₂`, `Q_∞(x)=Σ t_k 2^k`（t_k=parity of T^k x）は測度保存同相で T を 2-adic shift に
  共役（Bernstein–Lagarias 1996; Matthews–Watts ergodic/Bernoulli）。our induced map は 3^{D−1} で dressed した Syracuse 3x−1。
  → Haar-a.e. で D geometric(2^{-k}, mean 2)。
- **共役は壁を verbatim relocate（lower しない）**：Q_∞ は solenoidal で o₀ の有限 prefix は計算可能だが、「Q_∞(o₀) が 2-adic
  normal」= 我々の等分布標的と**文字通り同一**。a.e.-vs-specific が共役内部に再出現。
- **[PROVEN 一方向 reduction（共役非依存・GAP LEMMA arithmetic）]**: D=1⟺o≡1 mod4, D≥2⟺o≡3 mod4 ⟹
  `mean D ≥ 1 + freq(o≡3 mod4)`。だが Haar で freq=1/2 厳密＝**zero margin**（数値 1.4997<1.5）。
  robust 版は1項追加: **freq(D≥2)+freq(D≥3) ≥ 1/2**（mod4 AND mod8、Haar margin 1/4）。

### E2. 一方向 drift（`INDUCED_ONESIDED_DRIFT.md`）— **[PROVEN] 厳密公式＋最大局在化**
- **[PROVEN] 厳密公式**: D=Σ_{k≥1}1{D≥k}, D≥k⟺o≡3^{−1} mod 2^k ⟹ **mean D = Σ_{k≥1} freq(o ≡ 3^{−1} mod 2^k)**
  （数値で Σ=mean D 一致）。k=1 項≡1, k=2 項=freq(o≡3 mod4)。
- **最小十分命題（壁の最大局在化）**: k≥3 項は全て ≥0 ゆえ、標的全体は単一一方向命題
  **`liminf freq(o ≡ 3 mod 4) ≥ 1/2`** で十分。
- **residue map は bijection でない**: base map T は mod 2^k で厳密 2-to-1（full-shift 拡大）、induced map は mod 2^k で
  関数ですらない（増大する lookahead 要）→ 有限 permutation/counting で Haar は強制されない。
- **still (A) に還元**: budget は renewal tautology（等式で一方向 bound でない）、conditional mean E[D'|D≥k] は
  flat-to-decreasing（2.00→1.91, k=1..7）で floor を与えず。

### E3. Tao 対数密度法（`INDUCED_TAO_METHOD.md`）
- Tao 2019（arXiv:1909.03562）: ほぼ全 N（**対数密度**、**出発点**で平均）。単一軌道の時間統計を出さない。
  Syracuse 確率変数で v₂ geometric・iterate が mod 3^n で一様化。**出発点アンサンブル理論**。
- 「ほぼ全 n（単一軌道）」版は単一軌道 mod 2^k 等分布（=Mahler line(5)）を要求＝壁そのもの。一方向・1/3 slack・almost-all-n の
  緩和すべて還元（method は単一軌道/一方向 output を出さない）。
- Krasikov–Lagarias x^{0.84}（2003）: 出発整数の count、転送せず。unconditional な単一軌道事実は D≥1, mean D≥1
  （even-density≥0）のみで標的に遠い。
- 数値: liminf running-mean D は 1.5 を割らない（worst prefix slack +2.5、margin ~+0.5）が OBSERVED。

### E4. residue 構造（`INDUCED_RESIDUE_STRUCTURE.md`）— **[PROVEN] 新定理**
- **[PROVEN 新定理]**: induced 奇写像 `T(o)=3^{D−1}(3o−1)/2^D` は **odd 2-adic units ℤ₂^* 上で Haar 保存・exact/Bernoulli、
  D_j は i.i.d. geometric 2^{-d}（mean 2）**。branch-by-branch 証明（各 cylinder A_d は測度 2^{-d}、ℤ₂^* 全体へ bijective、
  2-adic Jacobian 2^d）＋決定的有限列挙（min=max=1022）。→ induced map は正真正銘の exact Syracuse 型系（既知の
  Collatz-on-ℤ₂ shift 共役の 3x−1・×3^{D−1} twist 版）。**測度論側は完全に PROVEN**。
- **だが residue map は非単射 full-branch SHIFT**（permutation でない、image 厳密に小、2–3 preimage、o mod 2^k は o' mod 2^k を
  決めない、read-window が毎ステップ上方シフト）→ single-cycle covering も pigeonhole lock も無し。Haar 保存は shift の
  full-branch 性で、a.e. 等分布を ergodic 定理経由でのみ与える（測度ゼロ除外、o₀ について無言）。**(A) に還元**。
- ×3-rotation（T_n mod 2^k, 実は period 2^{k−5}、doc の 2^{k−2} は loose）は carry/low bits に住み parity（moving-middle,
  Θ(n) 離れ）と disjoint、induced map は low bits を捨て high bits を引く→o_j mod 2^k は j で非周期。opening なし。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN 新定理・E4]** induced 奇写像は ℤ₂^* 上で **exact・Haar 保存・Bernoulli、D i.i.d. geometric mean 2**。
   branch-by-branch + 有限列挙で証明。Antihydra の measure-theoretic 側を完全に確立（Syracuse 型系として同定）。
2. **[PROVEN 厳密公式・E2]** **mean D = Σ_{k≥1} freq(o≡3^{−1} mod 2^k)**、**even-density = 1 − 1/(mean D)**。
3. **★ 壁の最大局在化**: 完全証明の唯一の [OPEN] は**単一一方向 cylinder 命題**に縮約：
   **`liminf freq(o ≡ 3 mod 4) ≥ 1/2`**（zero-margin tight 版）／ robust には **`freq(D≥2)+freq(D≥3) ≥ 1/2`**（margin 1/4）。
   「even-density→1/2」から「induced Syracuse 軌道が o≡3 mod4 を liminf で半分以上踏む」まで縮んだ。
4. **[確認・4角度]** 壁は依然 single-orbit genericity を要する（residue map は shift で bijection でない／Tao・KL は ensemble／
   共役は relocate）。measure 側は PROVEN、残るは specific orbit o₀=27 の一方向 mod-4 頻度のみ。

## wall (B) 現在地（最終）
- structured/periodic → **[PROVEN] arithmetic 排除**（C3）。
- aperiodic → induced Syracuse 系（**[PROVEN] exact Haar 保存**, E4）の単一軌道 o₀=27 が **liminf freq(o≡3 mod4) ≥ 1/2**
  を満たすこと（E2）に純化。これ以外は全て PROVEN。

## 次の生きた一手（候補）
1. **`liminf freq(o ≡ 3 mod 4) ≥ 1/2`（最小命題）を直接攻める** — 一方向・mod-4・単一 cylinder。
   induced Syracuse 系の o mod 4 の2状態 sub-dynamics（o≡1→D=1, o≡3→D≥2）の遷移を、より高い mod 2^k lift で
   一方向 occupancy 下界が取れるか。zero-margin ゆえ robust 版 freq(D≥2)+freq(D≥3)≥1/2（margin 1/4）を主標的に。
2. **新定理（E4）を含め commit**（measure-theoretic 側の完全 PROVEN は記録価値大）。
3. h_limit ≥ log(3/2) エントロピー下界（D1 示唆）。
4. annealed tier を partial result 固定。
