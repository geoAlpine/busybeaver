# The second-moment budget — is there an exact identity bounding mean depth? (2026-06-29)

*Angle: the first-moment valuation budget `Σ_{odd i<n} v₂(3c_i−1) = n + v₂(c_n) − v₂(c_0)` is an EXACT
telescoping identity that controls the FIRST moment of the jump/entry depths `K` (mean gap ≈ 2). Question:
is there an analogous EXACT identity (or one-sided inequality) controlling the SECOND moment `Σ_i K_i²`
(equivalently `Σ_n v₂(c_n−1)` = mean depth × N)? If yes ⇒ `E[K²]<∞` ⇒ mean depth bounded ⇒ `μ({1})=0`
UNCONDITIONALLY — a genuine new partial. If no, the precise reason the 2nd moment resists while the 1st is
free. Orbit `c_{n+1}=⌊3c_n/2⌋`, `c_0=8`, depth `d_n=v₂(c_n−1)`. Numerics exact big-int, `.venv`, N≤2·10⁵.
SOUNDNESS: every line labelled; no (K) claim. NOT committed.*

---

## 0. One-line verdict

**Verdict (b): there is NO proven second-moment / linear-sum identity, and the reason is sharp.** A quadratic
2-adic potential `Q(c_n)=d_n²` *does* telescope exactly (verified, 0 interior exceptions), but its identity
expresses `Σ_i K_i²` in terms of `Σ_n d_n` — and **these are the SAME object** (`Σ_n d_n = ½(ΣK² + ΣK)`).
The quadratic telescope, combined with the PROVEN geometric countdown run-sum, is **algebraically identical
to the first-moment identity** (a tautology `0=0`), carrying NO information that bounds the second moment.
The first moment is free because its telescope's refill term is a **count `≤ N`**; the second moment is
`(K)`-hard because its telescope's refill term is the second moment itself, which has **no a-priori `O(N)`
cap** — the refill depths `K_i` are injected by the moving-middle-digit (Mahler core) with no compensating
bounded potential. So `μ({1})=0` is NOT obtained as a free partial here. **It reduces to `(K)`-adjacent tail
control**, exactly as `NONATOMIC_FIXEDPOINT.md` states.

---

## 1. The first-moment budget, and WHY it telescopes for free

Two complementary 2-adic valuations live on the orbit (`c_n` and `c_n−1` cannot both be even):
- `v₂(c_n)` — divisibility of `c_n` (positive ⟺ `c_n` even),
- `d_n := v₂(c_n−1)` — the **depth** (positive ⟺ `c_n` odd, `c_n>1`).

**The countdown structure `[PROVEN]` (verified 0 exceptions to N=2·10⁵).** If `d_n=a≥1` (`c_n` odd), then
`c_{n+1}−1 = (3c_n−1)/2 − 1 = 3(c_n−1)/2`, so `d_{n+1}=a−1`: the depth decrements by exactly 1 each step
until `d=1`, whose successor is even (`d=0`). The orbit visits depth `≥1` only in **contiguous countdown
runs** of entry depth `K`: it realises depths `K, K−1, …, 1`, then `0`. The jump from `0` back up to a fresh
entry depth `K` (a "refill", at the even-step `c_n=2c'` with `v₂(c_n)=1`) is the **only randomness** — its
height `K = v₂(3c'−1)` is the moving-middle-digit / Mahler core.

**The first-moment budget `[PROVEN]` (VALUATION_BUDGET.md; here re-verified exact, §5).** Telescoping
`v₂(c_{i+1})−v₂(c_i)` (= `−1` on even steps, `= D_i−1` on odd steps, `D_i=v₂(3c_i−1)`) gives
> `Σ_{odd i<N} v₂(3c_i−1) = N + v₂(c_N) − v₂(c_0)`.

Equivalently, the **degree-1 telescope of the depth itself** (`Q=d_n`): summing `Δd_n` (= `−1` on each
`d≥1` step, `= +K_i` at each refill, `=0` on flat even steps):
> **`Σ_i K_i = #{n<N : d_n ≥ 1} + (d_N − d_0)`.   `[PROVEN, verified exact §5]`**

**Why it is FREE.** The refill sum `Σ K_i` equals a **count** `#{d_n≥1} ≤ N`, automatically. So
`Σ K_i ≤ N + O(log N)`: the first moment of `K` is bounded by `N` for free, with no genericity input. This
is the renewal first moment `E[K] · (#refills) ≤ N`, i.e. mean gap ≈ 2 — a tautology, exactly as
`VALUATION_BUDGET.md §"funnel"` and `renewal_attack §8` already noted ("`Σ D_i = n−j` is a tautology").

---

## 2. The second-moment identity attempt

The target (NONATOMIC_FIXEDPOINT.md): `μ({1})=0 ⟸ Σ_n d_n = O(N)` (mean depth bounded) `⟺ E[K²]<∞`. Within a
single countdown run of entry depth `K` the depth sum is the deterministic triangle, giving the
**geometric run-sum `[PROVEN]`**:
> **`Σ_n d_n = Σ_i K_i(K_i+1)/2 = ½ Σ_i K_i² + ½ Σ_i K_i`.   `[verified exact §5]`**

So `Σ_n d_n` (mean depth × N) and `Σ K_i²` are the **same object** up to the first moment `ΣK_i`.

**Candidate quadratic potential `Q(c_n)=d_n²`.** Increment on a countdown step `a→a−1` is
`(a−1)²−a² = −(2d_n−1)`; at a refill `0→K` it is `+K²`; flat even step `0`. Summing:
> **`Σ_i K_i² = 2 Σ_n d_n − #{d_n≥1} + (d_N² − d_0²)`.   `[PROVEN telescope, verified exact §5]`**

This *is* an exact identity (verified, 0 interior exceptions). Other candidates collapse identically:
`Q=d(d+1)/2` (= the per-state run-tail) telescopes to the same content; the bounded 2-adic potential
`Q=2^{−d_n}` has increment `+2^{−d}` on countdown / `(2^{−K}−1)` on refill, telescoping to
`Σ_i(1−2^{−K_i}) = Σ_{d≥1} 2^{−d_n} + O(1)` — a *bounded-per-term* sum (`≤ #refills`) that says nothing
about the heavy tail (it under-weights exactly the large-`K` events that drive `E[K²]`).

---

## 3. The exact obstruction: why the telescope closes on itself

Substitute the geometric run-sum `Σ_n d_n = ½(ΣK² + ΣK)` into the quadratic-telescope identity:
```
ΣK²  =  2·½(ΣK² + ΣK) − #{d≥1} + (d_N²−d_0²)
     =  ΣK² + ΣK − #{d≥1} + (d_N²−d_0²),
```
which reduces to `0 = ΣK − #{d≥1} + (d_N²−d_0²)` — i.e. (up to the `O(log²N)` boundary term) it is **exactly
the first-moment identity `ΣK = #{d≥1}`**. `[verified §5: the three residuals are 0 whenever d_N=0]`

**This is the precise obstruction.** Any potential that is a function of the current depth `d_n` telescopes
into (countdown decrements) + (refill injections). The refill injections are `Σ K_i^p` (the `p`-th moment);
the countdown decrements sum to the *same* `p`-th moment (the deterministic triangle). The telescope therefore
**closes on itself** and contains no more than the first-moment identity.
- `p=1` is **free**: the refill sum equals a **count** `#{d≥1} ≤ N` — a quantity bounded by `N` for a reason
  external to the orbit's statistics (you can't have more than `N` positive-depth steps).
- `p=2` is **`(K)`-hard**: the identity equates `ΣK²` to `2Σd_n` — but `Σd_n` is *itself* the second moment,
  NOT a count. There is **no a-priori `O(N)` cap** on `Σ_n d_n = Σ_n v₂(c_n−1)`: a single deep refill
  `K_i ≈ 0.585·n` is permitted by the only PROVEN length bound (`K_i ≤ log₂c_n ≈ 0.585n`, VALUATION_BUDGET §
  "unconditional range"), and one such run contributes `K_i² ≈ 0.34N²` to `ΣK²`, i.e. `ΣK²/N → ∞`, mean depth
  unbounded, atom `μ({1}) ≥ 0.585` — **consistent with every proven identity**. Capping `Σd_n` by `CN` is
  precisely `E[K²]<∞` = tail control on the refill depths = single-orbit equidistribution of the
  moving-middle-digit = `(K)`-adjacent.

In one line: **the first moment is a count (free); the second moment is an energy, and the exact identities
only relate it to itself.** No exact 2-adic identity, and no bounded/sub-stochastic potential, converts the
proven first-moment budget into a second-moment bound — consistent with `MINPROP_RUNS §3` (the renewal closed
form `freq(D=1)=1−1/E_deep` has no one-sided margin), `M4_P2_RESULT` (integrality is rigidity-only,
bias-blind; `avgD×density` is an identity bounding neither factor), and `renewal_attack §8` (the bookkeeping
`ΣD=n−j` is a tautology).

---

## 4. Verdict (a)/(b)/(c)

| option | claim | status |
|---|---|---|
| (a) proven 2nd-moment/linear-sum identity ⇒ `μ({1})=0` partial | a bound `Σ_n v₂(c_n−1) ≤ CN` | **NOT achieved** |
| **(b) no such identity, with precise reason** | **state-depth potentials telescope `ΣK^p` to itself; only `p=1` is a free count `≤N`; `p=2` equals `Σd_n` which has no proven `O(N)` cap (one `K≈0.585n` run breaks it)** | **THIS** |
| (c) reduces to (K) | `Σd_n=O(N) ⟺ E[K²]<∞ ⟺` refill-depth tail control = moving-middle-digit equidist. | yes, (b) bottoms out here |

So `μ({1})=0` is **[OPEN]**, not a free unconditional partial. The exact gap: a degree-1 valuation telescope
yields a sum that is a **count** (≤ N, free); the degree-2 telescope yields a sum that is the **second moment
itself** (no free cap). Nothing in the proven 2-adic arithmetic bridges count → energy.

---

## 5. Numerics `[OBSERVED, exact big-int, ek2_budget.py]`

All four telescoping identities are **exact** (residuals are 0 when the orbit ends cleanly `d_N=0`, and are
the predicted `O(d_N)=O(log N)` boundary terms when truncated mid-run, e.g. d_N=2 at N=5·10⁴):

| N | first-moment budget | countdown exc. | `ΣK=#{d≥1}+(d_N−d_0)` | geo run-sum `Σd=ΣK(K+1)/2` | quad telescope | `Σd==½(ΣK²+ΣK)`? |
|---|---|---|---|---|---|---|
| 2·10⁴ | exact | 0 | exact (Δ0) | exact (Δ0) | exact (Δ0) | yes (d_N=0) |
| 5·10⁴ | exact | 0 | Δ=−1 (d_N=2) | Δ=−1 | Δ=−3=−(2d_N−1) | (d_N=2) |
| 10⁵ | exact | 0 | exact (Δ0) | exact (Δ0) | exact (Δ0) | **yes** (d_N=0) |
| 2·10⁵ | exact | 0 | exact (Δ0) | exact (Δ0) | exact (Δ0) | **yes** (d_N=0) |

**The tautology confirmed** (N=10⁵, 2·10⁵, both `d_N=0`): `Σd_n = ½(ΣK²+ΣK)` holds exactly AND `ΣK=#{d≥1}`
holds exactly ⇒ the quadratic telescope `ΣK² = 2Σd−#{d≥1}` is identical to these — no independent content.

**The quantities of interest (bounded numerically, unbounded by proof):**

| N | mean depth `Σd/N` | `ΣK²/N` | max `K` | `log₂N` |
|---|---|---|---|---|
| 10⁵ | 0.9897 | 1.4810 | 20 | 17 |
| 2·10⁵ | 0.9940 | 1.4881 | 20 | 18 |

`Σd/N ≈ 0.99` and `ΣK²/N ≈ 1.48` are **stable/bounded**; `maxK ≈ log₂N`; occupancy
`f_k = 0.500, 0.250, 0.124, 0.061, 0.030, 0.0146, 0.0071, 0.0035, 0.0018, 0.0009` (geometric `≈2^{−k}→0`).
All consistent with `E[K²]<∞`, mean depth bounded, `μ({1})=0` — **evidence, not proof**: the same
equidistribution-flavoured data finite N can never upgrade, and the proven identities permit the heavy-tail
escape (a single `K≈0.585N` run) that this data merely happens not to exhibit.

---

## Sources

- `VALUATION_BUDGET.md` — the PROVEN first-moment budget `Σ_{odd}v₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)`; the
  unconditional range `K_i ≤ log₂c_n ≈ 0.585n`; the "funnel" / tautology of the first moment.
- `NONATOMIC_FIXEDPOINT.md` — the reduction `μ({1})=0 ⟸ Σd_n=O(N) ⟺ E[K²]<∞`; the first-vs-second-moment gap.
- `MINPROP_RUNS.md` — countdown Lemma `φ→φ−1` `[PROVEN]`; renewal closed form `freq(D=1)=1−1/E_deep`, no
  one-sided margin (the same "closes on itself" phenomenon for the deep-refill mean).
- `M4_P2_RESULT.md` — `avgD×density` is an identity bounding neither factor; integrality = rigidity, bias-blind.
- `antihydra_renewal_attack.md §7,§8` — depth = renewal process; `ΣD=n−j` tautology; jumps random-walk
  (no supermartingale / conserved quantity), partial sums `~√N`.
- `ek2_budget.py` (scratchpad) — exact big-int verification of all four telescoping identities and the
  tautology, N≤2·10⁵.

No machine decided. No label upgraded.
