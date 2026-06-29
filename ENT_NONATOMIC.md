# Is the Antihydra limit measure μ NON-ATOMIC? — the qualitative precursor to positive entropy (2026-06-29)

*WEAPONS_AUDIT style. Target: the QUALITATIVE precursor strictly weaker than ENT (`h_μ(M₂)>0`) — is the
empirical limit measure `μ` of the single `⟨3/2⟩`-orbit (`c₀=8`, `c_{n+1}=⌊3c_n/2⌋`) on the `(2,3)`-solenoid
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` **non-atomic** (no point masses)? Non-atomicity is necessary for positive entropy
(at the level of ergodic components) and is the most likely place for a genuine UNCONDITIONAL partial.
SOUNDNESS PARAMOUNT: every claim labelled; (K) NOT proven; no label upgraded. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/nonatomic.py` (exact big-int, N=10⁵, <2s).
NOT committed.*

---

## 0. ONE-LINE VERDICT

**Non-atomicity of `μ` is NOT delivered by any PROVEN structure — it is OPEN, verdict (b), with a SHARP
obstruction, and it sits STRICTLY between the proven facts and (K).** The reduction is clean and `[PROVEN]`:
for an `A`-invariant probability measure an atom forces a **periodic orbit** of `A`, so
> `μ` non-atomic  ⟺  `μ` charges no `A`-periodic orbit  ⟸  the `ℤ₂`-marginal `μ₂` charges no `T`-periodic
> point  ⟺  **`sup_a μ₂(a+2^kℤ₂) → 0`** (the *max* 2-adic cylinder occupancy vanishes as `k→∞`).

The proven facts (orbit **grows**, is **not eventually periodic** = excluded from every cycle `N/(3^q−2^q)`,
**dual-repulsion** escape from the fixed points) prove the orbit *avoids* and is *never trapped on* a periodic
orbit, and that every visit to a 2-adic ε-ball around a fixed point is **self-terminating** (countdown: `v₂`
strictly drops each shallow step). But that is *per-visit escape*, NOT *zero return-density*: an atom is
excluded by **positive-density re-entry**, and bounding the frequency of deep re-approaches is exactly the
occupancy/refill-law = **Mahler-character** quantity. So "avoids periodic points" `[PROVEN]` ⊊ "non-atomic"
`[OPEN, = sup-occupancy→0]` ⊊ "occupancy = Haar value" `[= (K)]`. Numerically `sup_a μ₂(2^k-cyl) ≈ (1…3)·2^{−k}
→ 0` and fixed-point residence `freq(v₂(c_n−1)≥k)` **halves per `k`** — strong evidence of non-atomicity, but
it is the SAME equidistribution evidence read on the occupancy axis, not a proof. **No machine decided. No
label upgraded.**

---

## 1. PRECISE MEANING of "μ non-atomic" and the reduction to sup-occupancy `[PROVEN]`

`μ` is `A`-invariant `[PROVEN, Krylov–Bogolyubov]` with `A=×(3/2)` the hyperbolic solenoid automorphism
(dilations `(3/2, 2, 1/3)` at `(∞,2,3)`). An **atom** at `p∈X` is `μ({p})=a>0`; equivalently the orbit spends
positive density of time in *every* neighbourhood of `p`:
`liminf_N (1/N)#{n<N : Aⁿx₀∈B(p,ε)} ≥ a` for all `ε>0`.

> **Reduction Lemma `[PROVEN]`.** For an `A`-invariant probability measure, **atoms can only sit on periodic
> orbits of `A`.** *Proof.* `A` is an automorphism, so `μ({Aⁿp})=μ({p})=a` for all `n∈ℤ`. If `p` is not
> periodic the points `{Aⁿp}_{n∈ℤ}` are distinct, each of mass `a>0` ⟹ infinite total mass, contradiction. ∎
> Hence **`μ` non-atomic ⟺ `μ` gives zero mass to every `A`-periodic orbit.**

The periodic points of `A=×(3/2)` are exactly the rational `ℤ[1/6]`-points; on the integer/`ℤ₂` side they are
the cycle points `c₀ = N/(3^q−2^q) ∈ {0,1}∪(0,1)` of `WALLB_NONATOMIC.md §2`.

**Projection to the bit-place (the (K)-axis).** An atom of `μ` projects to an atom of each marginal:
`μ({p})=a ⟹ μ₂(\{p₂\}) ≥ a`. The `ℤ₂`-marginal `μ₂` is `T`-invariant (`T(c)=(3c−(c mod 2))/2`, the
deterministic-orbit factor), and the same argument (using `T_*μ₂=μ₂`, forward images have non-decreasing mass)
gives: **atoms of `μ₂` ⟺ (eventually) `T`-periodic points.** Therefore
```
   μ₂ non-atomic   ⟹   μ non-atomic ,        and
   μ₂ non-atomic   ⟺   sup_{a∈ℤ₂} μ₂(a+2^kℤ₂) → 0   as k→∞ .          [PROVEN equivalence]
```
The right side is the **vanishing of the MAXIMUM 2-adic cylinder occupancy** — genuinely WEAKER than
equidistribution, which demands `μ₂(a+2^kℤ₂)=2^{−k}` for **every** `a` (the per-cell value), whereas
non-atomicity needs only the **max over `a`** to be `o(1)`. This is the precise sense in which non-atomicity is
a *qualitative precursor* to (K).

---

## 2. What the PROVEN structure gives — and the exact line it stops at `[PROVEN] / [OPEN]`

| proven fact | what it proves about atoms | does it give non-atomicity? |
|---|---|---|
| integer orbit **grows** `T(c)=⌊3c/2⌋>c` (`WALL_B_SELF_SELECTION §2b`) | orbit never **equals** a periodic point `∈(0,1)`; not attracted to atoms `{0,1}` | **NO** — avoids ≠ zero density near |
| itinerary **not eventually periodic** (`WALLB_NONATOMIC §2`, cycle pts `N/(3^q−2^q)∈(0,1)`, non-integer) | orbit is never **trapped** on any periodic orbit | **NO** — clustering without trapping is not excluded |
| **dual-repulsion** at `o=1`: `\|o−1\|_∞×3/2`, `\|o−1\|_2×2`, `v₂(o−1)` drops by 1 per shallow step (`REPELLER_ESCAPE §1`) | every visit to the 2-adic ε-ball `{v₂(c_n−1)≥k}` is **self-terminating in ≤ k−1 steps** (countdown) | **NO** — bounds *per-visit length*, not *re-entry frequency* |

**The sharp obstruction.** Combining the above, an atom of `μ₂` at a periodic point `p` could arise *only* from
**positive-density re-entry** into shrinking balls of `p` (the orbit keeps coming back), never from staying
(every visit self-terminates by expansion: `\|·\|_2` and `\|·\|_∞` both expand at a repelling fixed point;
`A` is hyperbolic). Quantitatively, for the fixed point `o=1`,
```
   freq{ c_n ≡ 1 mod 2^k }  =  freq{ v₂(c_n−1) ≥ k }  =  (1/N) Σ_{shallow runs} max(d_run − k + 1, 0),
```
where `d_run` = top depth of the run = (run length)+1. The orbit re-enters `{v₂≥k}` once per shallow run of
depth `≥k`; **the residence density is governed by the run-length / refill-law tail**, which is precisely
`E_deep` = mean 2-adic re-approach to 1 (`REPELLER_ESCAPE §2`) = single-orbit genericity = occupancy = (K).

**Why the unconditional budgets are too weak.** The valuation budget (`VALUATION_BUDGET`) gives unconditionally
`Σ_runs d_run ≤ 2N` (mean depth `≤1.585`) and the divisibility bound `2^{L+1}≤c_n<8(3/2)ⁿ ⟹` **max run
`L ≤ 0.585·n`** (a positive integer divisible by `2^{L+1}` is `≥2^{L+1}`). These bound *per-visit* length but
**permit a single run of length `≈0.585N`**, which alone would put residence `≈0.585` into `{v₂≥k}` for every
`k<0.585N`. To force `sup-occupancy → 0` one must exclude a positive-density family of *deep* re-approaches
(max run `=o(N)`, in fact the observed `O(log N)`), and that is itself the occupancy/Diophantine statement.
**No proven structure closes this; the obstruction is the refill-law tail = Mahler character.** `[OPEN]`

> **Net.** `{orbit avoids periodic points}` `[PROVEN]`  ⊊  `{μ non-atomic}` `[OPEN]` = `{sup_a μ₂(2^k-cyl)→0}`
> ⊊  `{μ₂ equidistributes}` `[=(K)]`. Non-atomicity is a *new, strictly intermediate* target — weaker than
> (K), stronger than everything proven — but it is **not** reached by growth/non-periodicity/repulsion, which
> deliver per-visit escape, not zero return-density.

---

## 3. The gap NON-ATOMIC → POSITIVE ENTROPY (even granting non-atomicity) `[PROVEN structural]`

Non-atomicity is **necessary** for positive entropy (an ergodic component with an atom is the uniform measure
on a periodic orbit, entropy 0) but far from **sufficient**:

| level | statement (on the 2-adic occupancy `f_k(a)=μ₂(a+2^kℤ₂)`) | strength |
|---|---|---|
| avoid periodic pts | orbit never lands on / is trapped by a cycle point | `[PROVEN]` |
| **non-atomic** | `sup_a f_k(a) → 0`  (no single cell heavy; support spreads to `→∞` cells) | `[OPEN]` |
| **positive entropy** ENT | `−Σ_a f_k(a)log f_k(a) ≳ ck` (mass spread over `2^{Ω(k)}` cells, **balanced**) | `[OPEN, (K)-hard]` |
| (K) = Haar | `f_k(a)=2^{−k} ∀a` | `[OPEN]` |

The gap **non-atomic → positive entropy** is exactly the **support-count vs frequency-weighted-count**
distinction of `POSITIVE_ENTROPY_ATTACK §3`, one notch lower: non-atomicity only requires the support to
spread over a *super-constant* number of cells (`sup f_k → 0` is compatible with support on `poly(k)` cells, or
even a Cantor set of **dimension 0**), whereas positive entropy requires `2^{Ω(k)}` cells carrying *balanced*
mass (`−Σf log f` linear in `k`). A **non-atomic, zero-entropy** measure is the standard counterexample
(self-similar Cantor measure of dimension 0: no atoms, yet `h=0`). In leafwise terms (`AIU_JOININGS §3.1`):
positive entropy `h_μ(A)>0` ⟺ the `A`-stable `ℚ₃`-leaf **conditionals** `μ_x³` are non-atomic — a STRONGER
"non-atomic" (of the conditionals, ⟺ positive dimension) than the GLOBAL non-atomicity targeted here. So even
the conditional non-atomicity needed for ENT is a strict upgrade over global non-atomicity. **Closing
non-atomic would not close ENT; one would still need positive-dimensional / balanced exponential spreading.**

---

## 4. NUMERICS — residence frequency in shrinking balls (`scratchpad/nonatomic.py`, N=10⁵) `[OBSERVED]`

**(A) Max 2-adic cylinder occupancy `sup_a freq(c_n≡a mod 2^k)`** — the exact non-atomicity probe:
```
 k:    1      2      3      4      6      8      10      12      14    ...  24
sup_a: .5016  .2513  .1260  .0638  .0164  .00447 .00129  .00043  .00019    .00003
×2^k:  1.00   1.01   1.01   1.02   1.05   1.14   1.32    1.76    3.11      (undersampling)
```
`sup_a freq → 0` cleanly; `sup_a·2^k = O(1)` while `2^k≪N` (drifts up only past `k≈14` where `2^k>N`, a pure
finite-sample artifact — `#distinct/2^k` falls off as `1−e^{−N/2^k}`). **No 2-adic atom in range.**

**(B) Max 3-adic occupancy** `sup_b freq(c_n≡b mod 3^j)`: identical decay (`.5016,.2513,.1260,…,.00072` at
`j=11`). **(C) Joint 2-adic×3-adic balls** (solenoid-ball proxy): `.0164 (k4,j2) → .00003 (k14,j7)` — decays
with ball size. No joint atom.

**(D) Residence at the FIXED POINT** `freq(v₂(c_n−1)≥k)` (2-adic ball of radius `2^{−k}` around `o=1`):
```
 k:    1      2      3      4      6      8      10     12     14     ...
freq:  .498   .248   .123   .0606  .0145  .00349 .00091 .00034 .00017
ratio: —      .498   .497   .491   .487   .492   .514   .642   .708   (>½ tail = undersampling)
```
**Halves per `k`** (≈`2^{−k}`) → 0: the most-repelling candidate atom carries no observable mass.

**(E) Max shallow run** over `N=10⁵`: **19** (≈`log₂N=16.6`), vs the unconditional bound `0.585N=58500`. The
runs are empirically `O(log N)` (genericity), but **only the weak `O(N)` bound is proven** — exactly the gap of
§2.

`[OBSERVED]` Everything is consistent with `μ` non-atomic (sup-occupancy → 0, fixed-point residence → 0), but
this is the SAME equidistribution evidence the program already has (`LIMIT_MEASURE_ENTROPY §4`), now read on the
occupancy/atom axis. Finite `N` cannot certify the `k→∞` limit; the exceptional behaviour, if any, is invisible
to any finite test.

---

## 5. HONEST VERDICT

| ask | answer | label |
|---|---|---|
| precise meaning of "μ non-atomic" | `μ` charges no `A`-periodic orbit ⟺ (suffices) `μ₂` charges no `T`-periodic point ⟺ `sup_a μ₂(a+2^kℤ₂)→0` (max 2-adic cylinder occupancy vanishes); strictly weaker than equidistribution (max vs per-cell) | `[PROVEN equivalence]` |
| relation to proven facts | atoms ⟺ periodic points (`[PROVEN]`); orbit grows / not eventually periodic / dual-repels ⟹ **avoids and is never trapped on** periodic orbits + every fixed-point ε-ball visit self-terminates — *per-visit escape* | `[PROVEN]` |
| **is μ non-atomic provable?** | **NO from proven structure.** Avoidance ≠ zero residence density; an atom needs only positive-density **re-entry**, whose frequency = run-length/refill-law tail = occupancy = Mahler. Unconditional budgets (`max run ≤0.585n`, mean depth `≤1.585`) bound per-visit length, **not** re-entry density. | **(b) OPEN, sharp obstruction** |
| non-atomic → positive entropy gap | non-atomic = `sup f_k→0` (support spreads, possibly dim 0); ENT needs `−Σf_k log f_k ≳ ck` (balanced spread over `2^{Ω(k)}` cells). Non-atomic ⇏ positive entropy (dim-0 Cantor counterexample). Conditional (leafwise) non-atomicity ⟺ ENT is a further strict upgrade. | `[PROVEN structural]` |
| numerics | `sup_a freq(2^k-cyl) ≈ (1…3)·2^{−k}→0`; fixed-point residence halves per `k`; max run 19≈log₂N. Consistent with non-atomic; equidistribution evidence, not proof. | `[OBSERVED]` |

**Disposition.** Verdict **(b): non-atomicity is OPEN with a precise obstruction**, and it is NOT a free
partial — it is genuinely sandwiched `{avoid periodic}[PROVEN] ⊊ {non-atomic}[OPEN] ⊊ {(K)}`. The clean
`[PROVEN]` gains are (i) the **reduction** atoms⟺periodic-orbits, collapsing "non-atomic" to a single
sup-occupancy statement on the bit-place, and (ii) the **per-visit self-termination** (no atom from staying;
only from re-entry), which localizes the entire obstruction to *re-entry frequency*. But that frequency is the
refill-law / run-length tail = single-orbit genericity = occupancy = Mahler. So non-atomicity does **not**
yield an unconditional partial here; it reduces — like every other route — to (a strictly weaker shadow of)
**(K)**, with no proven shortcut. The hoped-for "non-atomic provable when positive-entropy is not" fails for
THIS orbit because the only mechanism (hyperbolic per-visit escape) gives per-visit, not per-density, control.

---

## Sources
- Repo: `POSITIVE_ENTROPY_ATTACK.md` (ENT (K)-hard, weighted vs unweighted count), `LIMIT_MEASURE_ENTROPY.md`
  (ENT necessary for (K); entropy = RJ/Furstenberg selector; full per-bit entropy data), `AIU_JOININGS.md`
  (§3.1 ENT ⟺ stable `ℚ₃`-conditionals non-atomic, Ledrappier–Young; AIU = conditionals rotation-invariant),
  `REPELLER_ESCAPE.md` (dual-repulsion, countdown, refill law `E_deep`), `WALL_B_SELF_SELECTION.md` (growth,
  not attracted to atoms), `WALLB_NONATOMIC.md` (cycle points `N/(3^q−2^q)∈(0,1)`, not eventually periodic),
  `VALUATION_BUDGET.md` (`Σ depths`, `0≤v₂(c_n)≤0.585n`), `NEWMATH_DIAGONAL_RENORM.md` (non-Pisot no-atom of `A`).
- Literature `[PROVEN-in-lit]`: atoms of invariant measures ⟹ periodic support (elementary ergodic theory);
  Ledrappier–Young / Margulis–Ruelle (stable conditional non-atomicity ⟺ positive stable entropy); Rudolph
  (1990) / Johnson (1992), arXiv:2101.11120 (solenoid RJ); Lind–Schmidt–Ward (solenoid entropy
  `h(×u)=Σ_v log⁺|u|_v`). Furstenberg (1967) `×2,×3` `[OPEN]`. Mahler 3/2 / AEV Conj 1.6 at α=8 `[OPEN]`.
- Numerics: `scratchpad/nonatomic.py` (exact big-int, N=10⁵, <2s): `sup_a freq(2^k-cyl)`, 3-adic & joint
  occupancy, fixed-point residence `freq(v₂(c_n−1)≥k)`, max shallow run.

No machine decided. No label upgraded.
