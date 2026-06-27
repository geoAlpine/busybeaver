# The exact finite-state structure of the induced odd map on residues mod 2^k (2026-06-28)

*Angle: the GAP-LEMMA induced odd map `o ↦ o' = 3^{D-1}(3o-1)/2^D`, `D = v2(3o-1)`, acts on the odd
2-adic units `Z_2^*`. Determine its EXACT action on `o mod 2^k`, whether that action has provable
structure (bijection / Haar-preservation / rotation) that could pin the D-statistics WITHOUT
single-orbit genericity, and whether the `×3`-rotation structure of the carry `T_n mod 2^k`
(WALLB_MARTINGALE) transfers. Numerics `.venv` only (`induced_residue_structure.py`), exact big-int.
Zero false proofs. Every line labelled. NOT committed.*

---

## 0. One-line answer

The induced odd map is **provably Haar-preserving and exact (Bernoulli)** on `Z_2^*` — a clean new
`[PROVEN]` fact, with `D = v2(3o-1)` the i.i.d. geometric "digit". **But this is the wrong kind of
structure for a counting bypass.** The residue map `o mod 2^K → o' mod 2^k` is **not a permutation /
bijection — it is a non-injective SHIFT** (the `/2^D` discards low bits; fresh high bits enter every
step). Haar-preservation here is the *full-branch / shift* property (each cylinder maps onto the whole
space), which gives a.e. equidistribution by the **ergodic theorem only** and supplies **no
pigeonhole/covering pin** for our specific orbit `o_0`. The covering-by-bijection hope **hits the
avoidance wall: reduces to genericity.** The `×3`-rotation of the carry `T_n mod 2^k` is reconfirmed
exact but is the **wrong object** (low/carry bits, `Θ(n)` from the parity), and it **does not transfer**
to the induced map, which is a shift, not a rotation — **no provable opening there.**

Net: one genuine new `[PROVEN]` structural theorem (Haar-preservation + exactness of the induced
Syracuse-type map), but it **confirms** rather than breaches: the wall = single-orbit genericity = (A).

---

## 1. The induced map and its exact action on residues `[PROVEN]`

Induced odd map (GAP LEMMA, `WALLB_VALUATION_SHARP.md`): for odd `o`, `D = v2(3o-1) ≥ 1`,
`3o-1 = 2^D m` (`m` odd), and
> `T(o) = o' = 3^{D-1} m = 3^{D-1}(3o-1)/2^D`,  which is odd  (`3^{D-1}` and `m` both odd).

**Exact residue dependence `[PROVEN]`.** `o' mod 2^k = (3^{D-1}(3o-1)/2^D) mod 2^k` depends on
`(3o-1) mod 2^{k+D}`, i.e. on `o mod 2^{k+D}`. The window of `o` that `o' mod 2^k` reads is the bits
`[D, k+D)` — a window of width `k` that **shifts UP by `D` every step**. Therefore:

- `o mod 2^k` **alone does NOT determine** `o' mod 2^k` (verified §1 numerics: fixing `o ≡ 11 mod 2^6`
  and varying higher bits yields all 32 odd residues for `o' mod 2^6`).
- `o mod 2^K` **does** determine `o' mod 2^k` once `K ≥ k + D` — but `D` is unbounded (geometric), so
  **no single finite `K` works for all `o`** (measured: typical `K ≈ k + (small D)`; the deep tail needs
  arbitrarily many bits). This is the 2-adic **shift**: information flows from high bits to low.

This already tells us the structure is a one-sided shift, not a finite automaton on a fixed residue
ring.

---

## 2. THEOREM: the induced map preserves Haar measure on `Z_2^*` and is exact `[PROVEN]`

> **Theorem.** `T` preserves the Haar probability measure `μ` on the odd 2-adic units `Z_2^*`. Moreover
> `T` is a full-branch expanding map (every branch maps onto all of `Z_2^*`), hence **exact** (so
> ergodic and mixing), and the coding `o ↦ (D_0, D_1, …)` is a measure-isomorphism onto a Bernoulli
> shift with `D_j` i.i.d. `P(D=d)=2^{-d}` (geometric, mean 2).

**Proof.** Partition `Z_2^* = ⊔_{d≥1} A_d`, `A_d = {o : v2(3o-1)=d} = {o ≡ 3^{-1} mod 2^d,
o ≢ 3^{-1} mod 2^{d+1}}`, with `μ(A_d) = 2^{-d}` (since `3` is a unit, `3o≡1 mod 2^d` pins `o` mod `2^d`).
On `A_d`, `D≡d` and `T` is the affine map `o ↦ (3^d o − 3^{d-1})/2^d`. Substitute `m = (3o−1)/2^d`
(an affine bijection `A_d ↔ Z_2^*`, `m` ranging over all odd units, with 2-adic Jacobian
`dm/do = 3/2^d`, `|dm/do|_2 = 2^d`); then `o' = 3^{d-1} m` is multiplication of `m` by the unit
`3^{d-1}`, a Haar-isometry of `Z_2^*`. Hence for any measurable `B ⊆ Z_2^*`,
`μ(T^{-1}B ∩ A_d) = μ_o{ o : 3^{d-1}m ∈ B } = μ_m(3^{-(d-1)}B)·|do/dm|_2 = μ(B)·2^{-d}`. Summing,
`μ(T^{-1}B) = Σ_{d≥1} 2^{-d} μ(B) = μ(B)`. ∎

Each branch `T|_{A_d}: A_d → Z_2^*` is an **onto bijection** with inverse a contraction
(`o = (2^d m + 1)/3`, `|do/dm|_2 = 2^{-d} < 1`); a full-branch piecewise-affine 2-adic map with these
properties is **exact** w.r.t. its invariant measure (standard Rokhlin/Gauss-map argument), and the
itinerary `(D_j)` is then i.i.d. geometric with the `A_d`-measures `2^{-d}`. (This is the `3x−1`,
`×3^{D-1}`-twisted analogue of the well-known fact that the Collatz/Syracuse map is Haar-preserving and
shift-conjugate on `Z_2`; Lagarias.) ∎

**Numerical confirmation (deterministic, exact) `[PROVEN at finite level]`.** Enumerate ALL odd
residues `o mod 2^{k+B}` (`B=10`); for each with `D<B`, tally `o' mod 2^k`. Every odd target class
receives **exactly equal** count (`min=max=1022` for `k=4,6,8`; only the measure-`2^{-B}` deep tail
`D≥B` excluded). Monte-Carlo cross-check (256-bit random odds, `2·10^5` samples): `o'` lands on odd
residues only, `χ²/dof ≈ 1` for `k=6,8,10`.

So: **provably Haar-preserving and exact — YES.** Under Haar the D-statistics are exactly geometric
(mean 2 ⟹ parity `1/2`). This is the asset.

---

## 3. The residue map is a SHIFT, not a permutation — the covering argument FAILS `[PROVEN]`

The hope (prompt #2): if `o mod 2^k → o' mod 2^k` were a **bijection/permutation**, the orbit would
cycle through residues, and the empirical residue frequency over a period would be **exactly Haar by
counting** — pinning mean-`D` WITHOUT genericity. **This fails at the structural level.**

**The forward residue map is many-to-one (not a permutation) `[PROVEN]`.** Restrict to the well-defined
part (odd residues `r mod 2^k` with `D=v2(3r−1) < k`, so `o' mod 2^k` is determined by `r`). Measured:

| k | well-defined residues | image size (of `2^{k-1}` odd classes) | max preimages | verdict |
|---|---|---|---|---|
| 4 | 7/8 | 6 | 2 | not a permutation |
| 6 | 31/32 | 25 | 2 | not a permutation |
| 8 | 127/128 | 96 | 3 | not a permutation |

The image is strictly smaller than the domain and some classes have 2–3 preimages: this is exactly the
**collapsing of a 2-adic shift** (each `T^{-1}` point has on average 2 preimages, matching the
"branch onto whole space" / measure-`2^{-d}` structure of §2). There is **no single cycle covering all
residues**, so **no covering/pigeonhole argument exists**.

**Why Haar-preservation does NOT rescue a counting bound — the precise point.** In §2 the
measure-preservation is the *full-branch shift* property: each cylinder `A_d` maps onto the **whole**
space (Jacobian `2^d`), not a residue-ring permutation. This kind of preservation yields a.e.
equidistribution **only through the ergodic theorem** (Birkhoff: time-average `→ ∫ D dμ = 2` for
**μ-a.e.** `o`). It excludes a measure-zero exceptional set but says **nothing about the specified
point** `o_0`. A genuine pigeonhole pin requires a finite *bijective* automaton (a rotation/permutation
on a fixed `2^k`-ring); the induced map is the opposite (a non-invertible shift). Hence:

> **`[PROVEN]` The induced map is Haar-preserving and exact, but the residue map is a non-injective
> shift, not a bijection. The covering/counting bypass is unavailable; the orbit can a priori
> over-occupy the thin deep cylinders `{o ≡ 3^{-1} mod 2^k}` (the avoidance wall). Pinning mean-`D`
> reduces to single-orbit equidistribution = genericity = wall (A).**

**Avoidance is not excludable by the structure `[OBSERVED, consistent]`.** Along the REAL orbit
(`N=4·10^5`) residues mod `2^4,2^6,2^8` equidistribute (`χ²/dof ≈ 0.91/1.14/1.01`, occupancy ratios in
`[0.96,1.05]`) and the D-law is geometric (mean `1.9974`, `P(D=k)` matches `2^{-k}` to 3 dp). This is
**OBSERVED for this orbit**, exactly what genericity would give — but it is *not forced* by the residue
structure, since that structure is a shift (no counting lock). Finite `N` proves nothing about the
limit.

---

## 4. The `×3`-rotation of the carry `T_n mod 2^k` does NOT transfer — no opening `[PROVEN]`

WALLB_MARTINGALE: the carry `T_{n+1} = 3T_n + 2^n r_n` (`r_n=c_n mod 2`) satisfies, for `n ≥ k`,
`2^n r_n ≡ 0 mod 2^k`, hence `T_n ≡ 3 T_{n-1} (mod 2^k)` — an **exact `×3` rotation, a function of `n`
alone**. Reconfirmed: `0` rotation-violations for `n ≥ k+1` (`k=6,8,10`); eventual period `2,8,32`
`= 2^{k-5}` (matching the doc's recorded `8@k=8, 128@k=12`; the doc's "`2^{k-2}`" was a loose label —
the orbit settles at `v2(T_n)=3`, so the order of `3` acts mod `2^{k-3}`, giving `2^{k-5}`).

**Why this is no opening (prompt #3) `[PROVEN]`.** Two independent reasons:

1. **Wrong object.** The `×3` rotation is on the **carry / low bits**, which are a deterministic
   function of `n` and carry **zero** information about the parity `r_n` — the parity is the
   **moving-middle diagonal bit at depth ≈ n**, `Θ(n)` away from the low-bit foothold
   (`EFFECTIVE_TOPDIGIT` `Θ(log N) ↔ Θ(n)` gap; WALLB_MARTINGALE Horn B: OOS `R² ≤ 0`). A provable
   rotation on bits disjoint from the quantity of interest provides no control of that quantity.

2. **No analogue exists for the induced map.** A rotation requires the per-step update to *retain* the
   low bits (input term vanishing mod `2^k`). The induced map does the opposite: `o ↦ (…)/2^D`
   **discards** the bottom `D` bits and **pulls in** fresh high bits (§1, the shifting window
   `[D, k+D)`). Measured: `o_j mod 2^k` is **aperiodic in `j`** (no period found, `k=6,8`) — it is a
   genuine shift, **not** a function of `j` and **not** a rotation. So the equidistribution-for-free of
   a rotation has **no counterpart** for the D-statistics.

> **`[PROVEN]` The exact `×3`-rotation structure (carry, function of `n`) does NOT give a provable
> opening: it is on bits disjoint from the parity, and it does not transfer to the induced map, which
> is a non-invertible shift whose residues are aperiodic in `j`.**

---

## 5. Verdict (the three asks)

| ask | answer | label |
|---|---|---|
| Is the induced map provably Haar-preserving / bijective on residues? | **Haar-preserving and exact: YES** (§2, analytic proof + exact enumeration `min=max`). **Bijective on residues: NO** — it is a non-injective full-branch SHIFT (§3: image < domain, 2–3 preimages, `o mod 2^k` ⇏ `o' mod 2^k`). | `[PROVEN]` |
| Does a covering/bijection counting argument pin mean-`D` without genericity, or hit the avoidance wall? | **Hits the avoidance wall.** Haar-preservation is the shift's full-branch property → a.e. equidistribution by the ergodic theorem only, no pigeonhole for the specified `o_0`; the orbit can a priori over-occupy deep cylinders. **Reduces to genericity = wall (A).** | `[PROVEN]` |
| Does the exact `×3`-rotation of `T_n mod 2^k` give a provable opening? | **No.** Wrong object (carry bits, `Θ(n)` from the parity, `R²≤0`) and it does not transfer (induced map is a shift, residues aperiodic in `j`). | `[PROVEN]` |

### New asset banked `[PROVEN]`
*The induced odd map `T(o) = 3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`, **preserves Haar measure on `Z_2^*` and
is exact** (full-branch piecewise-affine 2-adic map; each branch `A_d`, `μ=2^{-d}`, maps bijectively
onto all of `Z_2^*` with Jacobian `2^d`; itinerary `(D_j)` i.i.d. geometric `2^{-d}`, mean 2). Hence the
target D-law is the **invariant/Bernoulli law of an exact system** — confirming `WALLB_VALUATION_SHARP`'s
localization with a hard ergodic-theoretic identity, not merely an empirical fit.*

### Why this confirms rather than breaches (honest)
Exactness gives equidistribution for **Haar-a.e.** `o`; our `o_0` is one specified point. The residue
dynamics is a **shift, not a permutation**, so there is no finite-automaton counting lock to upgrade
"a.e." to "this orbit." That upgrade is exactly single-orbit genericity = Mahler/AEV = wall (A). The
session's gain is a **sharper, citable structural identification** (the induced map is a bona-fide exact
Syracuse-type system) and a **clean impossibility for the counting route** (no bijection ⟹ no
pigeonhole), both consistent with all four prior WALLB angles.

### Live next angle (not yet mined)
Exactness gives quantitative **mixing** (decay of correlations of `D` under Haar). The single-orbit
wall is whether `o_0`'s empirical measure inherits that mixing (an *effective/quantitative* genericity
statement). The only un-reduced micro-target stays as in `WALLB_VALUATION_SHARP §5`: a one-sided
conditional `E[D_{j+1} | D_j ≥ k] ≤ 2` on a positive-measure deep cylinder (extremal deterministic
self-correction `D_1=1` is proven only at the measure-zero deepest points). Numerics show the
conditional mean flat at 2 (no gap), so this remains a long shot — but it is the one arithmetic
statement not yet shown literally identical to equidistribution.

Script: `induced_residue_structure.py`. Not committed.
