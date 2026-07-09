# The uniform reload map — an exact excursion theory for the whole {2,3}-smooth cryptid family (2026-07-09)

*Genuine construction. Extends the exact Antihydra reload map (NEWMATH_SOLENOID_BUILD §1,
`scratchpad/reload_verify.py`) to EVERY family member, using the campaign's uniform fixed-point theorem
(PAPER_MIRROR_LADDER §1: run depth `d = v_q(v−x)`). One uniform formula, verified on each machine's real
orbit; a classification of the reload maps; a cross-machine transfer verdict with the exact handle. STRICT
soundness: `[PROVEN]` / `[CONSTRUCTED-partial]` / `[OBSERVED]` / `[OPEN]`. Numerics
`scratchpad/reload_unified.py`, interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int,
≥2·10⁴ runs/machine, 0 mismatch. Not committed.*

---

## 1. The uniform reload map `[CONSTRUCTED — derived + verified, 0 mismatch across the family]`

**Derivation (from the uniform fixed-point theorem).** Each branch is affine `b(v)=(pv+e)/q` with integer
fixed point `x=−e/(p−q)`; run depth `d_i=v_q(v_i−x_{b_i})` (PAPER §1, `[PROVEN]`). Define the **reload unit**
> `w_i = (v_i − x_{b_i}) / q^{d_i} ∈ ℤ_q^×`  (the q-adic higher-bit residual, a unit).

Draining the run `d_i` steps gives, exactly, `b^{d_i}(v_i)−x_{b_i} = (p/q)^{d_i}(v_i−x_{b_i}) = p^{d_i} w_i`, so
the exit — which is the entry `v_{i+1}` of the **next** branch `b_{i+1}` — is `v_{i+1}=x_{b_i}+p^{d_i}w_i`.
Hence, with the **fixed-point offset** `Δ_i = x_{b_i} − x_{b_{i+1}}`:

> ### UNIFORM RELOAD MAP  `d_{i+1} = v_q( p^{d_i}·w_i + Δ_i )`,  `w_{i+1} = ( p^{d_i} w_i + Δ_i ) / q^{d_{i+1}}`

parametrized entirely by **(p, q, {x_branch})**. `a := p mod q^∞` is the ℤ_q^×-unit multiplier; `b := Δ_i`
is the offset from the branch geometry. This is the exact deterministic recursion of the excursion process
(depth, reload-unit) as a skew product on `{branches} × ℤ_q^×`.

**Verification on real orbits `[CONSTRUCTED-partial — 0 mismatch]`** (`reload_unified.py`, PART 1). For each
machine, on ≥2·10⁴ maximal runs: the run law `d_i=v_q(v_i−x)`, the exit identity `x+p^{d_i}w_i = v_{i+1}`, the
reload-depth recursion, and the reload-unit recursion **all match with 0 exceptions**:

| machine | ×p/q | place | branch fixed pts | offset Δ_{e→o} | runs | mismatches |
|---|---|---|---|---|---|---|
| Antihydra | 3/2 | ℤ_2 | (0, 1) | −1 | 20032 | 0 |
| o2 (ceiling) | 3/2 | ℤ_2 | (0, −1) | +1 | 20032 | 0 |
| o11 | 3/2 | ℤ_2 | (−8, −7) | −1 | 19953 | 0 |
| o16 | 3/2 | ℤ_2 | (−4, −3) | −1 | 20099 | 0 |
| o14 | 3/2 | ℤ_2 | (−12, −11) | −1 | 19923 | 0 |
| o13 | 3/2 | ℤ_2 | (−14, −7) | **−7** | 20056 | 0 |
| o4 | 4/3 | ℤ_3 | (−9,−14,−1) | multi-branch | 26873 | 0 |
| o15 (ideal) | 8/3 | ℤ_3 | x∉ℤ (via `v₃(5V+c)`) | queue-dep. | 26526 | run law only |

o4 realizes the uniform map with **three** branches (a genuine `{0,1,2}×ℤ_3^×` skew product); o15's four
branches keep V integer but the fixed points are non-integer 3-adic (`x=−c/5∈ℤ_3`), so only the run law
`d=v₃(5V+c)` verifies from V alone — the reload (branch selection) is queue-dependent (O15 §6), so o15 is
`[CONSTRUCTED-partial: depth axis ports; reload closes only relative to the queue transducer]`.

---

## 2. Classification of the reload maps `[CONSTRUCTED]`

**(a) Same place, same map — different seed.** The offset `Δ` is the only free parameter among the ×3/2
machines, and it is a shift-invariant of the branch geometry (gap between the two fixed points). **Antihydra,
o11, o16, o14 all have gap 1** — in the mirror coordinate `W=v−x_{even}` they reproduce the *identical*
canonical engine `W↦⌊3W/2⌋` (even `3W/2`, odd `(3W−1)/2`), verified 0 mismatch/3000 (PART 3a). They are the
**SAME dynamical system on different seeds** `W₀`. **o2 (ceiling)** has gap 1 with flipped sign
(`Δ=+1`): the same reload map up to the negation conjugacy `w↦−w` on ℤ_2^×. **o13** has **gap 7**
(fixed points −14,−7) — a shift-invariant, so o13 is a *genuinely different* reload map at the same place
(not shift/negation-conjugate to the gap-1 class). So the ×3/2 family is **one reload map (gap-1) plus one
variant (o13, gap-7)**, all on ℤ_2^×.

**(b) Cumulative vs resetting — in reload-unit terms `[CONSTRUCTED-partial / MODEL]`.** *Cumulative* machines
(Antihydra, o2, o4, o3, Space Needle) run **one continuous ×p/q orbit**: the reload units `w_i` are a single
deterministic ℤ_q^×-recursion — every unit fixed by its predecessor (correlated). *Resetting* sea machines
(o11/o13/o14/o16, o15) **re-seed the inner ×3/2 sea to the constant 2 at every refill** and read one decisive
residue `T^{e_n}(2) mod 4` at a **doubly-exponentially sparse, self-determined index** `e_n≈(3/4)T^{e_{n−1}}(2)`.
Consecutive decisive draws are separated by ~10¹⁴ steps of the same map, so they **decorrelate** — measured
lag-1 autocorrelation ≈ 0 (PART 4). This is the mechanism behind the annealed halt-lean splitting exactly along
the cumulative/resetting axis (BB6_CRYPTID_SPECIES). **Honest caveat:** the sampled residues being i.i.d. IS
the per-orbit equidistribution of `{T^i(2) mod 4}` along a sparse subsequence — i.e. **(K) itself**. The
resetting structure makes the *annealed model* i.i.d.; the quenched truth is (K)-hard. `[MODEL, not theorem]`.

**(c) o4 vs Antihydra: same map at different (p,q), not a different species.** o4's ×4/3 reload map (growing
budget, ρ/β=0.087) and Antihydra's ×3/2 (constant budget, critical 1.17) are the **same uniform map at
(p,q)=(4,3) vs (3,2)**. The "growing budget" is a *ledger/criticality* attribute (a different axis); the
reload-unit dynamics are structurally the same critical ℤ_q^×-equidistribution problem — o4 in ℤ_3^×,
Antihydra in ℤ_2^× — with **no margin slack in the unit dynamics itself** (both need full equidistribution).

---

## 3. Cross-machine leverage — the exact handle, re-examined `[CONSTRUCTED — verdict: no transfer]`

The prior finding ("no bound transfers: nonlinear floor map + neutral-uniform") is now sharpened with the
explicit reload maps, testing every plausible reduction:

1. **Does o4's ×4/3 reload map factor through / bound a ×3/2 reload map?** **No.** o4's map lives in ℤ_3^×,
   Antihydra's in ℤ_2^× (the depth reads the *expanding* p-adic place, and (p,q)-swap interchanges which finite
   place expands — NEWMATH §2.1). There is **no continuous ring map ℤ_2→ℤ_3**, so the two reload dynamics have
   no functional relation. Illustrated (PART 3b): the depth sequences are v₂-valued vs v₃-valued objects of
   different p-adic character.

2. **Margin monotonicity in the easy direction?** **No.** The margin (subcritical o4 → critical Antihydra) is
   a **budget-axis** quantity (§2c); the reload-unit equidistribution is on the orthogonal **frequency axis**,
   where the uniform map is equally critical at every (p,q) (no margin parameter enters `d_{i+1}=v_q(p^{d_i}w_i+Δ)`).
   There is no "easy end" on the axis that carries the bound — matching the AIU_NEUTRAL deformation-uniformity
   result (NEWMATH §2.2).

3. **Does one machine's reload-unit equidistribution IMPLY another's?** **No — the sharpest form of the wall.**
   Even for Antihydra/o11/o16/o14, which are the *literally identical* reload map, the open content is the
   equidistribution of **this orbit's** units in ℤ_2^× — a **per-seed** statement. Two seeds of the *same map*
   give statistically **unrelated** reload-unit residue sequences (measured cross-correlation −0.010…−0.018 at
   mod 4/8/16, PART 3b). So **identity of the dynamical system transfers no bound**: single-orbit
   equidistribution does not propagate between seeds, let alone between places. A genuine reduction would need
   one orbit's normality to force another's; nothing in the exact handle provides it.

**Verdict:** the explicit reload maps make the family a single uniform object `d_{i+1}=v_q(p^{d_i}w_i+Δ)`, and
they make the *reason for no transfer* exact and structural — different places (o4 vs Antihydra), a
budget-axis-only margin, and per-seed (not per-map) open content. Every route lands independently on the
per-orbit (K) wall = ℤ_q^×-equidistribution of the reload units = one-sided normality on base p/q
(Mahler 3/2 / AEV Conj 1.6). No cross-machine reduction is real; each machine's protection is its own
equidistribution statement.

---

## 4. What was built (summary)

- **A uniform reload map** `d_{i+1}=v_q(p^{d_i}w_i+Δ)` parametrized by (p,q,offset), derived from the uniform
  fixed-point theorem, verified 0-mismatch on the real orbit of every family member (≥2·10⁴ runs each).
  `[CONSTRUCTED]`
- **A classification:** the ×3/2 family is one reload map (gap-1: Antihydra/o11/o16/o14, o2 by negation) plus
  o13 (gap-7); cumulative machines have a correlated single ℤ_q^×-recursion, resetting sea machines a sparse
  decorrelated sample (annealed-i.i.d. as a MODEL, quenched = (K)). `[CONSTRUCTED / MODEL]`
- **A cross-machine verdict:** no reduction — different places, budget-only margin, per-seed open content;
  identity of the map transfers nothing. `[CONSTRUCTED]`

Reproduce: `scratchpad/reload_unified.py` (PART 1 uniform verification; PART 2 classification; PART 3
same-map/different-seed + place mismatch + transfer test; PART 4 cumulative/resetting correlation). Basis:
`scratchpad/reload_verify.py`, `NEWMATH_SOLENOID_BUILD_2026-07-09.md`, `PAPER_MIRROR_LADDER.md`,
`O4_RUN_STRUCTURE_2026-07-07.md`, `O11_REFILL_LAW_2026-07-08.md`, `O13_O14_FIXEDPOINT_2026-07-08.md`,
`O15_FIXEDPOINT_2026-07-07.md`.

No machine decided. No label upgraded.
