# WALL (B): do growth + carry exclude NON-ATOMIC biased 2-adic orbits? (2026-06-28)

*The ONE wall-(B) sub-question not literally identical to Mahler (A). Background: the a.e. equidistribution
theorem fails only on a Lebesgue-null exceptional set E. The **atomic** members of E (eventually-constant
parity, `delta_0=c_0` / `delta_1=c_1`) are already `[PROVEN]` excluded (`WALL_B_SELF_SELECTION.md` §2b:
integer `c0>=2` grows, never returns to `{0,1}`). The remaining E-members are **non-atomic**: itinerary
recurrent (parity returns, never freezes) yet **biased** (Birkhoff parity average != 1/2). Question: does the
specific arithmetic of `c_{n+1}=floor(3c_n/2)` (integer, growing) rule out sitting on such a non-atomic biased
point WITHOUT proving full equidistribution? Every line labelled. Numerics `.venv` only
(`wallb_nonatomic.py`, `wallb_periodic.py`). Zero false proofs. NOT committed.*

---

## 0. One-line answer

The non-atomic biased set **splits in two**, and the arithmetic kills exactly one half:

- **STRUCTURED half** (eventually-**periodic** itinerary, e.g. parity `(001)^∞`, density 1/3): `[PROVEN]`
  **excluded by arithmetic** — a clean, non-circular, general theorem strictly stronger than the atom
  exclusion. **This is the genuine new gain.**
- **UNSTRUCTURED half** (aperiodic itinerary, Birkhoff-generic for a non-Haar invariant measure with biased
  parity): `[REDUCES TO (A)]` — the bias `<=>` `avgD_odd != 2` via the exact 2-adic valuation budget, a
  cylinder-frequency statement = Mahler. **No arithmetic gain here.**
- **Numerics (option (c), "biased integer orbits exist"): not supported.** Over 4000 integer starts (and
  forced-bias starts) every biased window is **transient** — bias decays at the fair-coin `~N^{-1/2}` rate,
  `avgD_odd -> 2` exactly. No persistent-bias integer orbit found.

So the answer to the assignment's trichotomy is **(a) for the structured half, (b) for the unstructured
half** — a sharper outcome than "it all reduces to equidistribution."

---

## 1. Characterization of the non-atomic biased orbits  `[PROVEN / standard]`

System `(ℤ₂, T, c0=8)`, `T(c)=(3c − (c mod 2))/2 = "×3/2"`, itinerary `e_n = T^n c0 mod 2` under the
partition `ℤ₂ = {even}⊔{odd}`. (On ℕ this is `c_{n+1}=⌊3c_n/2⌋`, `e_n=c_n mod 2`.) "Equidistribution" =
the single orbit is generic for Haar, i.e. parity density 1/2.

A **non-atomic biased orbit** is a point whose empirical measures `(1/N)Σ_{n<N} δ_{T^n x}` accumulate at a
`T`-invariant measure `ν` with `ν(odd) ≠ 1/2` and `ν ∉ {δ₀,δ₁}` (parity not eventually constant). By the
ergodic decomposition these split into two structurally different classes:

| class | invariant measure `ν` | itinerary | where it lives |
|---|---|---|---|
| **structured** | periodic-orbit measure (uniform on a finite `T`-cycle) | eventually **periodic**, e.g. `(001)^∞` | `ℚ`-points / algebraic, *countable* |
| **unstructured** | a non-Haar ergodic `ν` with biased parity | **aperiodic**, Birkhoff-generic for `ν` | the full-dimensional, **non-sofic, uncharacterizable** part of `E` (`WALL_B_EXCEPTIONAL_SET.md` §2: `3/2` non-Pisot ⇒ β-shift not even sofic ⇒ no finite-state / Diophantine characterization) |

The **coding `x ↦ (e_n)` is injective** (`wallb_periodic.py` (1), VERIFIED bijection `Z/2^{k+1} ↔` itineraries
of length `k+1`, all `k≤11`): `e_0..e_k` reveals `c0 mod 2^{k+1}` (because `c_{n+1} mod 2` depends on
`c_n mod 4`). Hence **eventually-periodic itinerary ⟺ eventually-periodic point** `T^{M+q}x = T^M x`. This is
what lets the structured half be attacked arithmetically.

---

## 2. The arithmetic lever — structured half EXCLUDED  `[PROVEN, general, non-circular]`

**Periodic points of `T` are non-integers (except the atoms).** A period-`q` cycle with parity pattern
`(e_0,…,e_{q-1})` is the unique solution of `c0 = T^q(c0)`; since `T` is affine on each branch
(`c_{n+1} = (3/2)c_n − e_n/2`),
```
   c0  =  N / (3^q − 2^q),     N = Σ_{j=0}^{q-1} 2^j · 3^{q-1-j} · e_j.
```
The denominator `3^q − 2^q` is **odd**, so every cycle point lies in `ℤ₂`. The key bound:
```
   0 ≤ N ≤ Σ_{j=0}^{q-1} 2^j 3^{q-1-j} = 3^q − 2^q        (geometric sum; equality iff all e_j = 1).
```
Therefore **`c0 = N/(3^q−2^q) ∈ [0,1]`, and is an integer ⟺ `c0 ∈ {0,1}` ⟺ the atoms** (`N=0` all-even,
`N=3^q−2^q` all-odd). Every **non-atomic** periodic cycle has `c0 ∈ (0,1)` — a genuine 2-adic rational with
odd denominator, **never a positive integer ≥ 2**.

VERIFIED exhaustively (`wallb_periodic.py` (3)): all `2046` self-consistent cycles for `q=1..10` are
non-integers except `0,1`; e.g. the **biased** period-3 cycle `(001)^∞` (parity density 1/3) is `c0 = 4/19`,
the biased `(0001)^∞` is `8/65`, etc. The closed-form bound makes this a theorem for **all** `q`, not just
the checked range.

**Conclusion (the gain).** An integer orbit with `c0≥2` is **strictly increasing** (`T(c)−c = ⌊c/2⌋ ≥ 1`,
VERIFIED `c∈2..10^5`), hence `c_M < c_{M+q}` for every `q≥1`, so it can never equal a (fixed) periodic point.
By injectivity its itinerary is therefore **not eventually periodic**.
```
   [PROVEN, NON-CIRCULAR]  The integer Antihydra orbit has an itinerary that is NOT eventually periodic.
   ⇒ it is excluded from EVERY eventually-periodic (structured) non-atomic biased orbit — biased or not —
     not merely from the two atoms.  No equidistribution is assumed.
```
This **strictly strengthens** the banked micro-asset ("not attracted to the atoms `{0,1}`" = period-1 only):
the same elementary arithmetic (growth) now removes **all** periods at once. It kills the entire *countable,
structured/algebraic* slice of the non-atomic exceptional set.

---

## 3. The unstructured half REDUCES to (A)  `[REDUCES TO MAHLER]`

The remaining non-atomic biased orbits are **aperiodic** with a persistent parity density `p ≠ 1/2`. The
exact **2-adic valuation budget** (`VALUATION_BUDGET.md`, verified to `n=10^5`) pins what such a bias means:
```
   Σ_{i<n, c_i odd} v2(3c_i − 1)  =  n + v2(c_n) − v2(c0)      [exact identity]
   ⇒  (odd-density) · avgD_odd  =  1 + v2(c_n)/n − v2(c0)/n,   avgD_odd = mean over odd steps of v2(3c_i−1).
```
A persistent bias `p_odd ≠ 1/2` therefore **forces** `avgD_odd = (1+δ)/p_odd ≠ 2`, where `δ = lim v2(c_n)/n`.
But Haar gives `avgD_odd = 2` (geometric law `P(v2(3c−1)=k)=2^{-k}`). So:
```
   non-atomic persistent bias  ⟺  avgD_odd ≠ 2  ⟺  the depths v2(3c_i−1) over odd steps deviate from the
   Haar mean  ⟺  the orbit's cylinder-frequencies c_i mod 2^k deviate from Haar  =  equidistribution failure.
```
There is **no pure-arithmetic obstruction** forcing `avgD_odd = 2`; this is exactly the cylinder-frequency /
`{(3/2)^j}`-exponential-sum cancellation = wall (A) = Mahler. **The unstructured half is operatively
identical to (A).** Honest: the budget gives no leverage here beyond what the carry sum already encodes.

**What the budget DOES give unconditionally (a real but weak constraint, not an exclusion):** from
`0 ≤ v2(c_n) ≤ log2(c_n) ≈ 0.585n`,
```
   1 − v2(c0)/n  ≤  (odd-density)·avgD_odd  ≤  1.585 + o(1).        [UNCONDITIONAL]
```
So a bias is **not arbitrary** — `p_odd` and `avgD_odd` are rigidly coupled in a bounded window — but the
window is too wide to exclude `p_odd ≠ 1/2`.

---

## 4. Numerics — is there a biased integer orbit? (option (c))  `[OBSERVED: no; bias always transient]`

`wallb_nonatomic.py`, exact big-int arithmetic.

**(A) Sweep, tail even-density (last half), `N=20000`, 26 integer starts** (small, `2^k`, binary patterns,
random 30–300 bit). Fair-coin sd `≈ 0.0050`. All `c0≥2` give `|z| ≤ 2.08` (mean `z=+0.245`, `max|z|=2.08`) —
**indistinguishable from a fair coin**; only the atom `c0=1` fires (`z=−100`, already excluded).

**(B) Transience of forced bias.** Forced-cluster starts decay to balance, bias staying within fair-coin range:

| start | even-dens `N=500 → 60000` | max sliding-`W2000` bias (fair-coin ≲ 0.0335) |
|---|---|---|
| `2^200`  | `0.690 → 0.500` | 0.0325 |
| `2^1000` | `1.000 → 0.506` | 0.0275 |
| `c0=8`   | `0.504 → 0.499` | 0.0295 |

The cluster is **diluted/outgrown, not actively corrected** (consistent with `WALL_B_SELF_SELECTION.md` §4).

**(C) Valuation coupling holds exactly.** `c0=8`: `p_odd=0.5009, avgD_odd=1.9962, p·avgD=0.9999`; random 120-bit
and `2^200` likewise `p≈1/2, avgD_odd≈2, p·avgD≈1, v2(c_n)=O(1)` (`δ≈0`). No start shows `avgD_odd` away from 2.

**(D) Targeted hunt, 4000 starts, length 6000.** Max `|z|=3.51` — exactly the Gaussian-extreme expectation
(`√(2 ln 4000)≈4.07`) for that many fair coins, i.e. **no anomaly**. The most-biased candidate
(`c0=789487276821`, `z=−3.51` at `N=6000`) **loses its bias on extension**: `z = −3.51 → +1.36 → −0.22` at
`N = 6000, 20000, 60000`. **Every observed bias is transient.**

`[OBSERVED]` No persistent-bias integer orbit exists in any tested range; biased windows are transient and
`avgD_odd → 2`. This **does not support option (c)** (biased integer orbits exist) and is consistent with
option (b) + the equidistribution conjecture. (Finite `N` proves nothing about the limit — `E` is exactly the
set invisible to any finite test.)

---

## 5. Verdict on the trichotomy (the assignment's question)

| non-atomic biased sub-class | status | which option |
|---|---|---|
| eventually-**periodic** itinerary (structured/algebraic, *countable*) | **`[PROVEN]` excluded by arithmetic** (periodic points `∈(0,1)`, non-integer; integer orbit grows ⇒ not eventually periodic) — strictly weaker than equidistribution, non-circular | **(a) PROVABLE** |
| **aperiodic** persistent-bias (unstructured, full-dim non-sofic `E`) | `[REDUCES TO (A)]` — bias `⟺ avgD_odd ≠ 2 ⟺` cylinder-frequency / `{(3/2)^j}` cancellation = Mahler | **(b) EQUIVALENT** |
| any biased integer orbit actually existing | `[OBSERVED]` none found; all bias transient, `avgD_odd→2` | **(c) NOT supported** |

**Net.** The non-atomic question is **not monolithic**. Growth + carry **do** exclude a genuine, previously
unbanked slice — *all* eventually-periodic (structured) biased orbits, by a clean general arithmetic theorem
(periodic points are odd-denominator rationals in `(0,1)`, the integer orbit grows past them) — strictly more
than the atoms. The rest (aperiodic biased orbits) is **operatively identical to wall (A)**: no arithmetic
shortcut, it is the `avgD_odd = 2` / Mahler cancellation. Numerically no biased integer orbit is observed.
So wall (B)'s non-atomic remainder is **honestly bisected**: one piece closed by arithmetic, one piece `=`
Mahler. No false proof; the gain is real but does not breach (A).

### New micro-asset banked  `[PROVEN]`
*The integer Antihydra orbit's parity itinerary is **not eventually periodic** (general proof: a period-`q`
cycle of `T` is `N/(3^q−2^q) ∈ (0,1)` for any non-atomic pattern, hence non-integer; the integer orbit grows
strictly and never reaches it). This excludes the entire **structured/eventually-periodic** slice of the
non-atomic exceptional set — strictly stronger than the atom exclusion — leaving only the **aperiodic**
biased orbits, which equal wall (A) = Mahler (`avgD_odd = 2`).*

### Live next angle
The structured slice fell to "periodic points are non-integers + growth." The aperiodic slice is `avgD_odd=2`.
The only conceivable further arithmetic gain would attack a **graded** version: can growth + the budget bound
`p·avgD_odd ∈ [1, 1.585]` exclude bias of a *specific magnitude* (e.g. the non-halt threshold `even-density ≥ 1/3`
⟺ `avgD_odd ≥ 3/2`) by an arithmetic, non-density argument? That is the `avgD_odd ≥ 3/2` one-sided form
(`VALUATION_BUDGET.md`) — the natural target for a future second-moment/energy attack, and the only piece of
the aperiodic half not yet shown literally identical to full equidistribution.
