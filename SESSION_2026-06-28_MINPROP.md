# 最小命題 freq(D≥2)+freq(D≥3) ≥ 1/2 への4攻撃 — なぜ構造のみでは解けないかの [PROVEN] メタ結果（2026-06-28, 続）

induced Syracuse 系の最小一方向命題 `ψ := 1{o≡1 mod4} − 1{o≡3 mod8} − 1/2` の時間平均 ≤ 0
（⟺ freq(D≥2)+freq(D≥3) ≥ 1/2 ⟺ even-density ≥ 1/3 ⟺ 非停止）を4角度で攻撃。
**結果: 「構造のみ(全軌道一様)の証明は不可能」を正確な理由とともに [PROVEN]。新 [PROVEN] 補題2つ。誤証明ゼロ。**

## メタ結果（決定的・F1+F3+F4 が独立に同一結論）
**[PROVEN・標準理論] 一方向命題が全軌道で成立 ⟺ `β(ψ) := max_{T-不変測度 μ} ∫ψ dμ ≤ 0`**
（Mañé/Conze–Guivarc'h/Bousch の sub-action 理論; ergodic optimization）。
- **β(ψ) = +1/2 > 0**、達成するのは**固定点 o=1**（T(1)=1, D=1 forever）。ψ は現在の D のみの関数で +1/2(D=1)/−1/2(D=2)/−3/2(D≥3)。
- o=1 は **D=1 forever ⟺ even-density 0 ⟺ 停止軌道**。全軌道一様の bound は「全軌道が非停止」を証明することになるが、
  **停止軌道（o=1）は実在する** → 全軌道一様の証明は**原理的に存在しない**。
- **Haar の 1/4 slack は無関係**：feasibility は max_μ で決まり、達成測度は atomic δ₁(+1/2) であって Haar(−1/4) でない。
→ **open core は還元不能に orbit-specific**。これまでの全構造攻撃（contraction/bootstrap/vdC/MR/twisted RPF/residue/coboundary）が
  「relocate するだけ」だった理由を**1つの定理で説明**：構造のみの証明は偽命題「全軌道非停止」も証明してしまう。

## 4角度の結果

### F1. coboundary/Lyapunov LP（`MINPROP_COBOUNDARY_LP.md`）— INFEASIBLE、理由は o=1
- `ψ(o) ≤ g(T(o)) − g(o)` の有限 LP（difference constraints, max-mean-cycle で双対）を k=3..12 で Fraction 厳密に解く。
  **全 k で INFEASIBLE**。双対障害 = **o=1 の self-loop（weight ψ(1)=+1/2）**、全 k で max-mean-cycle=+1/2。
- tail 切詰は監査済 sound（未決定 residue は全て D≥3, ψ=−3/2 の最有利値、conservative full-branch edge で処理、0 violation）。
  infeasibility は determined な +1/2 self-loop が駆動、tail 非依存。
- 残る変種 = 非有界 magnitude-aware Lyapunov `α·log o + h(o mod 2^k)`（α<0 で size drift D·log(3/2) に結合）[OPEN]
  ——ただし avoidance/genericity を再導入。

### F2. run 構造（`MINPROP_RUNS.md`）— [PROVEN] 補題2つ
- **[PROVEN] Countdown Lemma**: φ(o)=v₂(o−1) とすると D=1 ステップで φ→φ−1 厳密。
  → **m 連続 D=1 ⟺ o_start ≡ 1 mod 2^{m+1}**（測度 2^{−(m+1)} の薄 cylinder）、run 長 = v₂(o_start−1)−1 厳密。
  実軌道 o₀=27 で全 75139 run が一致、例外ゼロ、最長 run=19。**self-limiting**（無限 D=1 run は off-orbit 固定点 o=1 のみ）。
- **[PROVEN] 閉形式**: **freq(D=1) = 1 − 1/E_deep**（E_deep = deep ステップでの v₂(o_next−1) の平均）。
  freq(D=1)≤1/2 ⟺ E_deep≤2。E_deep は conditional cylinder occupancy/genericity 量（Haar 値=Σa2^{−a}=2）。
  → target を**疎な deep-substep 上の conditional mean の閉形式**に書き換え（最鋭の局在化）。一方向 margin なし（占有に還元）。

### F3. ergodic optimization（`MINPROP_ERGODIC_OPT.md`）— メタ結果の核
- 上記メタ結果を確立。**β(ψ)=+1/2、達成は o=1=停止固定点**。numerically ψ は D のみの関数（0 mismatch, o<2·10⁶）、
  Haar で D_j i.i.d.（full shift）ゆえ β=max_d ψ(d)=ψ(1)=+1/2。constant-D 2-adic 固定点 o_d=3^{d−1}/(3^d−2^d) も max +1/2。
- **生きた継続（重要）**：o=1 は**拡大 induced map の repelling 固定点**で、整数軌道 27 は増大ゆえ**決して入らない**。
  → target が「27 が D=1 優勢領域（o≡1 mod4）に Cesàro 密度 <1/2 しか滞在しない」に upgrade ＝ 全等分布より厳密に弱い。
- entropy/pressure gap（正エントロピー Haar vs 零エントロピー周期 maximizer、‖F‖<1 と結合）も継続候補。

### F4. exact-Bernoulli coupling / specification（`MINPROP_COUPLING.md`）— [PROVEN] 非一様性
- **[PROVEN] specification ⟹ bound は非一様（全 Hausdorff 次元の軌道で偽）**。full-branch ゆえ specification、
  観測量 1{D≥2} の ergodic-opt 極値は 0（o=1）と 1（o=3/5∈ℤ₂, D=2 forever）の両固定点で実現、任意 freq∈[0,1] の軌道を構成。
  → 命題は非可算個の軌道で偽、o₀=27 は arithmetic に singled out 必須 = wall (A)。
- **[PROVEN] 特定 start に coupling なし**：27=…011011 は固定 eventually-zero 2-adic tail＝**entropy source なし**＝
  coupling すべき確率空間がない。expansion/sensitivity は coupling でない。coupling rate = 特定点の effective 等分布 = 壁 verbatim。
- 数値: running freq−1/2 は両側対称、70% の prefix で 1/2 を**下回る**＝構造的一方向 floor なし、極限のみ予想 1/2。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN メタ定理] 構造のみ(全軌道一様)の証明は不可能**：ergodic-opt の β(ψ)=+1/2>0、達成は停止固定点 o=1。
   全軌道 bound = 偽命題「全軌道非停止」。→ open core は還元不能に orbit-specific。全構造攻撃が relocate した理由を説明。
2. **[PROVEN] Countdown Lemma**（F2）: m 連続 D=1 ⟺ o≡1 mod 2^{m+1}、run 長=v₂(o−1)−1、self-limiting。
3. **[PROVEN] 閉形式**（F2）: freq(D=1)=1−1/E_deep。target を deep-substep の conditional mean に局在化。
4. **[PROVEN] specification ⟹ 非一様**（F4）: 命題は全次元の軌道で偽、o₀=27 を arithmetic に分離必須。特定 start に entropy source なし。
5. **生きた継続**: o=1 は repelling 固定点で整数軌道 27 は増大ゆえ入らない → 「27 は D=1 領域に密度 <1/2」(等分布より弱い)。

## 構造の最終像（重要）
open core が orbit-specific である理由が**証明された**：障害は停止固定点 o=1。構造（測度保存・exactness・specification）は
**両方の固定点（停止 o=1 と非停止）を許す**ので、構造のみでは 27 がどちらの genericity を持つか決められない。
**唯一の生きた道 = archimedean（27 は増大＝∞ へ escape、o=1 から repelled）と 2-adic（D=1 run ⟺ o の 2-adic で o=1 へ近接、
Countdown Lemma）を結ぶこと**。この2つの valuation の独立性こそ Mahler 障害の本体。整数増大（archimedean, PROVEN）を
2-adic proximity-to-1 の密度 bound に変換できれば突破——できなければ Mahler。

## 次の生きた一手（候補）
1. **archimedean escape × 2-adic proximity の結合**（F3 継続）: 27 の整数増大（c_n~(3/2)^n, PROVEN）が、Countdown Lemma 経由で
   o≡1 mod 2^k cylinder（=o=1 への 2-adic 近接）の Cesàro 占有を一方向に bound するか。2 valuation 結合＝Mahler の核を直撃。
2. **magnitude-aware Lyapunov `α log o + h(o mod 2^k)`**（F1 残し）: size drift を coboundary に組み込む非有界 sub-action。
3. annealed/measure 側の PROVEN 資産（exact Haar 保存、閉形式、Countdown）を完全証明の確定部分として固定・commit。
