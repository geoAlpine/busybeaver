# Sharpening the 2-adic valuation budget — can carry-counting exclude a persistent parity bias? (2026-06-28)

*ARITHMETIC attack on the aperiodic half of wall (B) (the half `WALLB_NONATOMIC.md` left `[REDUCES TO (A)]`).
Target: tighten the budget `Σ_{odd i} v2(3c_i−1) = n + v2(c_n) − v2(c_0)` to EXCLUDE a persistent parity
density `p ≠ 1/2` for `c_{n+1}=⌊3c_n/2⌋` WITHOUT assuming equidistribution. Numerics `.venv` only
(`wallb_valuation_sharp.py`, `wallb_valuation_escape.py`). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

There IS a genuine new exact structural fact — **the gap from each odd step to the next odd step equals
`D_i = v2(3c_i−1)` exactly** `[PROVEN]` — and it shows precisely **why the budget is loose**: the budget is
the *renewal tautology* "(#renewals)·(mean gap) = total time," which pins only the **first moment** of the
depth distribution and nothing else. The remaining question — "is the frequency of deep steps capped below
the Haar value?" — is **exactly** a single-orbit cylinder-frequency statement and **does reduce to
equidistribution**. We searched hard for an arithmetic self-correction (anti-correlation in the depth
sequence) that would force the mean without equidistribution and found **none** (depths behave like i.i.d.
geometric: zero lag-correlation, flat conditional means, deep seeds lose all depth memory in O(1) steps).
**Brutally honest:** the budget cannot be sharpened to an unconditional exclusion; it bottoms out at
equidistribution. The gain is a sharper, cleaner *localization* of the wall, plus one PROVEN exact lemma.

---

## 1. The exact GAP LEMMA — the real structural content `[PROVEN, non-circular]`

> **Lemma.** Let `c_i` be odd and `D = D_i = v2(3c_i−1) ≥ 1`. Then the next `D−1` steps are even and step
> `i+D` is the next odd step. I.e. **the gap to the next odd step equals `D_i` exactly.**

*Proof.* `3c_i−1 = 2^D m` with `m` odd, so `c_{i+1} = (3c_i−1)/2 = 2^{D−1} m`. For `t = 0,…,D−1`, an even
step sends `c_{i+1+t} = 3^t 2^{D−1−t} m` (each even step is `×3/2`, lowering `v2` by 1). The valuation
`D−1−t` is `>0` (even) for `t<D−1` and `=0` (odd) at `t=D−1`, i.e. `c_{i+D}=3^{D−1}m` is the next odd. For
`D=1`, `c_{i+1}=m` is odd, gap `=1=D`. ∎ (VERIFIED exactly over `N=10^5` for `c_0=8, 2^{200}`, and a deep seed:
`gap == D_i` held with no exception, `wallb_valuation_sharp.py`.)

**Corollaries.**
- The **budget is a tautology.** If odd steps occur at `t_1<t_2<…`, then `t_{j+1}−t_j = D_{t_j}`, so
  `Σ_{odd} D = Σ(t_{j+1}−t_j) = t_last − t_first = n + O(log)`. The identity
  `Σ_{odd}v2(3c_i−1)=n+v2(c_n)−v2(c_0)` carries **no arithmetic information beyond "gap = D"**;
  `p_odd · avgD_odd = 1` is just `(#renewals)·(mean gap)/n`. (Measured `p·avgD = 1.00000` to 5 dp.)
- The **induced (odd-to-odd) map** is `o_{j+1} = 3^{D−1}(3o_j−1)/2^D`, `D=v2(3o_j−1)` — a Syracuse-type
  accelerated map; one return multiplies by `≈(3/2)^D`. The bias question is entirely about the **long-run
  distribution of `D` along this induced orbit.**

This is the genuine gain: it converts "bias `⇔` `avgD≠2`" (a statement about a *mean*) into the exact
statement that **the entire wall is the shape of one distribution — the law of `v2(3o−1)` over the induced
odd orbit.**

---

## 2. Why the budget is LOOSE (made precise) `[PROVEN]`

The budget pins `Σ D = n+O(log)`, i.e. the **first moment** `avgD_odd ≈ 1/p_odd`. With each `D_i ≥ 1` the
only unconditional consequence is the trivial `#odd ≤ 1.585n` (`VALUATION_BUDGET.md`). The looseness is
structural, not a missing inequality:

- `D_i = v2(3c_i−1)` is a **per-step random-looking depth**; the budget constrains only its *sum*, not its
  *distribution*. Two orbits with identical `ΣD` can have wildly different depth histograms — hence different
  `p_odd` are a priori compatible with the same budget total. (This is exactly the `[1,1.585]` window of
  `WALLB_NONATOMIC.md §3`.)
- `{D_i ≥ k} = {c_i ≡ 3^{-1} \bmod 2^k}` — a 2-adic ball of relative measure `2^{1−k}` among odds (because
  `3` is a unit, `3c≡1 mod 2^k` fixes `c` mod `2^k`). So **deep step ⟺ orbit in a thin cylinder.** The budget
  says nothing about cylinder *occupation frequency*; that is the missing ingredient.

---

## 3. Can the deep-step frequency be bounded ARITHMETICALLY? `[REDUCES TO EQUIDISTRIBUTION]`

A persistent bias `p_odd < 1/2` forces `avgD_odd = 1/p_odd > 2`, i.e. an **excess** of deep steps over the
Haar geometric law `P(D=k)=2^{−k}` (mean 2). Equivalently, by §2, the induced odd orbit must spend **excess
density in the thin cylinders** `{o ≡ 3^{-1} \bmod 2^k}`. Bounding the frequency of `D≥k` away from the Haar
value `2^{1−k}` is, *by definition*, controlling the orbit's cylinder frequencies mod `2^k` = **single-orbit
equidistribution**. There is no arithmetic identity that caps it; the only unconditional cap is the trivial
`D≥1`. So the "persistent bias ⟹ thin-set confinement" implication is real and exact, but **excluding the
confinement = proving equidistribution.** No arithmetic shortcut exists at the level of the budget.

**The one place a shortcut could have hidden — and does not.** A genuine arithmetic gain would be a
*self-correcting law*: a deep step deterministically (or in conditional mean) forcing shallow successors, so
that the mean is pinned at 2 regardless of equidistribution. We tested this directly (§4) and it is **absent**:
the depth sequence is statistically indistinguishable from i.i.d. geometric (no lag correlation, flat
conditional means, no memory of a forced deep seed beyond one step). So there is no hidden self-correction;
the funnel to equidistribution is genuine, not an artifact of a weak argument.

**Partial structural positive (not a bound).** For the *extremal* cylinder representatives — the canonical
minimal inverse `o_0 = 3^{-1} mod 2^K` (maximal possible `D_0 ≈ K`) — the very next depth is **forced**:
`D_1 = 1` for **every** `K=10..44` tested (`wallb_valuation_escape.py`). So the deepest points *do* self-correct
deterministically to the shallowest cylinder in one step. This is a real arithmetic anti-correlation, but only
at the measure-zero extremal points; it does not extend to a uniform bound over the generic deep cylinder, and
hence does not lift to a mean bound.

---

## 4. Numerics — the depth sequence is i.i.d.-geometric, confinement self-destructs `[OBSERVED]`

`wallb_valuation_sharp.py`, `wallb_valuation_escape.py`, exact big-int, `N=10^5–2·10^5`.

**(A) GAP LEMMA exact** for all tested starts (`c_0=8`, `2^{200}`, deep seed): `gap == v2(3c_i−1)`, no exception.

**(B) Depth law = geometric (Haar), all starts.** `c_0=8`: `avgD_odd=2.006`, `p_odd=0.4984`, `p·avgD=1.00000`.
Empirical `P(D=k)` vs `2^{−k}` agree to 3 dp for `k=1..8`; thin-set `freq(D≥k)/2^{1−k} ∈ [0.99,1.01]`. Same
for `2^{200}` and a 40-bit deep seed.

**(C) NO self-correction in depth (the decisive negative).**
- `corr(D_j, D_{j+1}) = −0.0065` (and `≈0` at lags 2,3,5) — i.e. **zero**.
- Conditional mean `E[D_{j+1} | D_j=k]` is **flat at ≈2** for `k=1..6` (2.01, 1.99, 1.99, 2.02, 1.97, 1.93) —
  the i.i.d. signature: a deep step carries **no** predictive pull on the next depth.

**(D) Confinement self-destructs.** Seeding `o_0 ≡ 3^{-1} mod 2^K` (`D_0 ≈ K = 20,40,80`): after the one
forced deep step, `mean(D_1,D_2,…) → ≈2` immediately (1.95, 2.08, 1.77); the seed depth leaves **no memory**.
Longest run of consecutive odd steps with `D≥2` (orbit pinned to `o≡3 mod 4`) over `2·10^5` induced steps is
**16**, matching the geometric extreme `log2(2·10^5)≈17.6` — **no anomalous confinement.**

`[OBSERVED]` The induced depth process is empirically i.i.d. geometric (mean 2 ⟹ `p=1/2`), with no
arithmetic anti-correlation that a proof could exploit short of equidistribution. (Finite `N` proves nothing
about the limit; `E` is exactly what is invisible to finite tests.)

---

## 5. Verdict

| question | answer | label |
|---|---|---|
| Why is the budget loose? | It is the renewal tautology `(#renewals)·(mean gap)=total time` (gap `= D_i` exactly, §1); it pins only the **first moment** of the depth law, not its shape. | `[PROVEN]` |
| Can deep-step (large-`v2`) frequency be bounded arithmetically? | No. `freq(D≥k)` = cylinder frequency of the induced orbit in `{3o≡1 mod 2^k}`; capping it below Haar `2^{1−k}` **is** equidistribution. Only the trivial `D≥1` is unconditional. | `[REDUCES TO (A)]` |
| Is "persistent bias ⟹ thin-set confinement" excludable without equidistribution? | The implication is exact and real, but excluding the confinement = proving the induced orbit equidistributes mod `2^k`. No self-correcting arithmetic law exists (depths are i.i.d.-geometric: zero correlation, flat conditional means, no seed memory). **Reduces to equidistribution.** | `[REDUCES TO (A)]` |
| Numerics | Depth law geometric, `p·avgD=1` tautologically, confinement self-destructs in O(1) steps, longest deep run matches the geometric extreme. | `[OBSERVED]` |

**Net.** Consistent with `WALLB_NONATOMIC.md`: the aperiodic biased half is operatively identical to wall (A)
= Mahler. The new contribution is **sharper localization, not a breach**:

### New micro-asset banked `[PROVEN]`
*The gap from each odd step to the next equals `v2(3c_i−1)` exactly (Lemma §1). Hence the 2-adic valuation
budget is the renewal tautology `(#renewals)·(mean gap)=total time`, and the **entire** non-atomic aperiodic
wall is precisely one statement: the law of `v2(3o−1)` over the induced odd orbit `o_{j+1}=3^{D−1}(3o_j−1)/2^D`
equals the geometric (Haar) law `2^{−k}` — equivalently, that orbit equidistributes in the cylinders
`{o≡3^{-1} mod 2^k}`. A persistent parity bias is exactly an excess occupation of these thin cylinders, with
no first-moment or self-correction shortcut.*

### Live next angle
The depth law is i.i.d.-geometric empirically with **zero lag-correlation**, yet the deepest extremal points
(`o≡3^{-1} mod 2^K`) self-correct **deterministically** to `D_1=1` (§3). The only un-mined arithmetic is
whether this extremal self-correction can be upgraded from the measure-zero deepest points to a *one-sided
inequality on a conditional mean* over a positive-measure deep cylinder (e.g. `E[D_{j+1} | D_j ≥ k] ≤ 2`
provably for some `k`) — which, if it held with a strict gap, would cap `avgD` and could give the one-sided
`avgD < 3/2`-type bound without full equidistribution. Current numerics show the conditional mean is flat at
2 (no gap), so this is a long shot, but it is the one concrete arithmetic statement not yet shown literally
identical to equidistribution.
