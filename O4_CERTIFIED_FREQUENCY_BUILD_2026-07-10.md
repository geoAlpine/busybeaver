# Porting certified trace-templates / bounded-episode induction to the FREQUENCY axis of o4 (2026-07-10)

*Genuine build. The campaign's signature technique (certified trace-templates + bounded-episode induction,
`PAPER_TEMPLATE_METHOD.md`) decided o4's **structure** — `C(k) → C(k+2)` for all k by finite base + 2-step
induction. The coboundary LP (`O4_COBOUNDARY_LP_2026-07-08.md`) decided the **ledger** potential. Neither was
ever pointed at the **fatal frequency functional** itself, `freq{3|W_n} = #1/n`, fatal ⟺ `≥ 4/5`
(`O4_NEWMATH_BUILD_2026-07-09.md`). Here I port certified induction to that functional: can a FINITE certified
computation on the reload map's finite quotients bootstrap to an eventual bound `freq ≤ 4/5 − ε`, deciding o4?
Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact `int`/`Fraction`, every claim
assertion-checked; script `o4_certified_frequency.py`, all assertions passed. NOT committed. STRICT labels.*

---

## 0. One-line verdict

**[PROVEN, negative]** The frequency sub-action LP on `B(3,k)` — the finite certified computation on the reload
map's depth-k quotient — has max-mean cycle **exactly `1` at every `k = 1..6` (and provably all k)**, attained
uniquely by the `δ₋₁₄` all-`ρ=1` self-loop. The certified frequency bound is `freq ≤ 1 ⩾ 4/5` at every level: a
**PLATEAU at 1, never crossing below `4/5`**. Higher memory does not improve it (the LP already optimizes over
*all* depth-k potentials, linear or nonlinear); the only lever that drops the bound below `4/5` is an **external
run-length hypothesis**, i.e. exactly the (K)-hard input. The honest prior is confirmed exactly: **a finite
computation cannot imply the infinite frequency bound, because the inductive invariant it would need is precisely
what the extremal `δ₋₁₄` orbit denies.** **No machine decided. No label upgraded.**

---

## 1. The port: what "certified induction on frequency" is

The template method proves a config transition for *all* k by a finite base + fixed-step induction. Its
sub-action/LP shadow (the linear certified-induction version) proves a Birkhoff bound for *all orbits* by a finite
graph computation: a potential `φ` and constant `c` with

> `Φ(G) ≤ φ(TG mod 3^k) − φ(G mod 3^k) + c`  for **all integers G**,

telescopes to `(1/N)Σ Φ ≤ c + o(1)` on every orbit. Certified-induction = "the increment of `φ` pays for `Φ`
each step, checked on a finite graph." For the **frequency** functional the observable is the fatal indicator
`Φ = 1{ρ=1}` (recall `ρ=1 ⟺ 3|W`, `#1 = Σ_run L`), and `min feasible c = max-mean cycle of B(3,k)` under the
**frequency weight** `w = 1{source window ρ₀ = 1}`. The reload-map state `(branch, unit w ∈ ℤ_3^×)`
(`RELOAD_MAP_UNIFIED_2026-07-09.md`) is infinite; a *finite certified computation* is exactly its depth-k
quotient `ℤ/3^k`, which by the itinerary bijection **is** the de Bruijn graph `B(3,k)`. So "finite certified
computation on the reload map" = "the `B(3,k)` frequency LP." This is the never-tested port.

## 2. THE KEY COMPUTATION — exact `B(3,k)` max-mean-cycle frequency bound, k = 1..6

| k | \|V\|=3ᵏ | \|E\|=3ᵏ⁺¹ | **freq max-mean cycle** | extremal object | freq bound vs 4/5 |
|---|---|---|---|---|---|
| 1 | 3 | 9 | **1** | `δ₋₁₄` self-loop @ `−14 mod 3` | `1 > 4/5` |
| 2 | 9 | 27 | **1** | `δ₋₁₄` self-loop @ `−14 mod 9` | `1 > 4/5` |
| 3 | 27 | 81 | **1** | `δ₋₁₄` self-loop @ `−14 mod 27` | `1 > 4/5` |
| 4 | 81 | 243 | **1** | `δ₋₁₄` self-loop @ `−14 mod 81` | `1 > 4/5` |
| 5 | 243 | 729 | **1** | `δ₋₁₄` self-loop @ `−14 mod 243` | `1 > 4/5` |
| 6 | 729 | 2187 | **1** | `δ₋₁₄` self-loop @ `−14 mod 729` | `1 > 4/5` |

`[PROVEN, exact, machine-verified + Karp cross-check k=1..6; level-independent by the integer fixed point]`.
Upper bound: max edge weight `= 1` ⟹ every cycle mean `≤ 1`. Lower bound: `−14` is the genuine integer fixed
point `T(−14) = −14`, all-`ρ=1` itinerary, so its self-loop carries weight `1` at every level — a mean-`1`
cycle. Uniqueness (`[PROVEN, k=1..6]`): a mean-`1` cycle uses only weight-`1` edges = all-`ρ=1` sources; the
induced weight-`1` subgraph minus the `−14` loop is a DAG (Kahn) — the `δ₋₁₄` loop is the **only** maximizer.

**The bound PLATEAUS at `1` for every k. It never decreases with k, never approaches the annealed `1/3`, and
never crosses `4/5`.** The certified frequency bound is the trivial `freq ≤ 1`. This is the outcome the brief
flagged as fatal to the method (item 3): the extremal `δ₋₁₄` cycle realizes `freq → 1` at *every* level,
growth-independent — the exact frequency-axis mirror of what `O4_COBOUNDARY_LP` found for the ledger (max-mean
`+1`). The frequency version is even cleaner: `1` = the trivial pointwise bound, so residue/reload structure
extracts **zero** margin below the free count `#1 ≤ n`.

## 3. Higher-memory / nonlinear certificate — subsumed, and the fixed-point reason

The brief asks to go beyond linear: a degree-2 or window-k potential. **This gains nothing, provably.** The
max-mean-cycle duality already optimizes over *all* functions `φ: ℤ/3^k → ℝ` — the most general depth-k-memory
certificate of **any** functional form. A degree-d polynomial in the window's indicators is itself just some
function on `ℤ/3^k`, already inside the LP's variable class; "nonlinear in the indicators" does not enlarge the
class at fixed depth. The *only* genuine lever is memory depth k — and that is exactly the k-sequence of §2,
constant `1`. A window-m certificate is a linear potential on `B(3, k)` at larger k; the hierarchy is the k-column,
which plateaus.

The structural reason no certificate of any form (bounded, unbounded, linear, nonlinear) escapes is the
**fixed-point obstruction**, verified in-script: any sound `φ` valid for all integers must hold at `G = −14`
(`T(−14) = −14`, `ρ = 1`), giving `1 = Φ(−14) ≤ φ(−14) − φ(−14) + c = c`, so **`c ≥ 1`**. The `δ₋₁₄` orbit is a
genuine integer orbit with `freq ≡ 1 > 4/5`; every sound certificate must dominate it. Dropping the inequality at
`−14` = using the specific seed's avoidance of the `−14`-shadow cylinders = the quenched (K) object. (This
transposes `O4_NEWMATH_BUILD` §4 and `MAGNITUDE_LYAPUNOV` from the ledger to the frequency functional intact.)

## 4. The self-improving hierarchy — improves only in R (the OPEN input), never in k

The one way the bound drops below `4/5` is an **external** hypothesis capping the `ρ=1` run length. On the
subshift `{all ρ=1 runs ≤ R}`, the exact frequency max-mean cycle is `R/(R+1)` (extremal word `1^R 2`):

| runs ≤ R | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **freq max-mean** | `1/2` | `2/3` | `3/4` | `4/5` | `5/6` |
| ledger max-mean `(R−4)/(R+1)` | `−3/2` | `−2/3` | `−1/4` | `0` | `+1/6` |
| decides o4? | yes | yes | **yes** | critical | no |

`[PROVEN, exact, k=6]`. `freq = R/(R+1)` crosses `4/5` exactly at `R = 4` (critical); `R ≤ 3` would DECIDE o4
(`3/4 < 4/5`). The two functionals share the identical threshold — verified affinely, `ledger = 5·freq − 4` on the
`ρ=2`-filler extremal cycle — because both are maximized by the *same* all-`ρ=1` invariant, on which the ledger's
`−4,−6` terms are invisible. Crucially, **raising the window k at fixed R does not lower `R/(R+1)`** (verified
k-independent: `R=2` gives `2/3` for k=3..6; `R=3` gives `3/4` for k=4..6). So the hierarchy self-improves only as
R decreases — an eventual *run-depth* bound, which is the (K)-hard input `O4_COBOUNDARY_LP` §4 and
`O4_RUN_STRUCTURE` §4 already localized. The unconditional situation is `R = ∞`, i.e. `R/(R+1) → 1`: the plateau
of §2. The observed longest run on the real orbit is 2; nothing proven caps it below the `0.262n` archimedean cap.

## 5. Honest assessment (brief item 3)

The max-mean-cycle bound **plateaus at `1`, above `4/5`, at every finite k**, and the plateau is realized by the
`δ₋₁₄` extremal cycle at every level, growth-independent — exactly the `O4_COBOUNDARY_LP` picture on the
frequency functional. Therefore **certified induction CANNOT decide o4 on the frequency axis.** The `δ₋₁₄`
all-`ρ=1` fixed point is a genuine `T`-invariant object the finite certificate always sees (its self-loop is in
`B(3,k)` at every k); excluding it is precisely the seed's quenched avoidance of the `−14`-shadow cylinders =
(K). There is no inductive invariant on the reload map's finite quotients that separates the real orbit from the
`δ₋₁₄` orbit — which is the exact thing (K) supplies and a finite computation cannot. The nonlinear/higher-memory
attempt does not strictly improve: the LP is already the optimal certificate of any form at each depth, and the
depth-hierarchy is the constant `1`. Extrapolation therefore does **not** cross `4/5`; it is flat at `1`.

This is a sharp, exact impossibility statement about certificates on the frequency axis — the missing mirror of
the campaign's structure result — not progress toward a decision. It confirms the honest prior at the operator
level: the finite computation lacks the inductive invariant, and the invariant it lacks is named exactly (`δ₋₁₄`
separation = base-4/3 quenched cylinder frequency = (K)).

## 6. Verdict table (0 false proofs)

| question | answer | label |
|---|---|---|
| Frequency sub-action LP on `B(3,k)`, k=1..6, max-mean cycle | **`1` at every k** (Karp cross-checked; level-independent by `T(−14)=−14`) | `[PROVEN]` |
| Does it improve toward a decision (`< 4/5`) as k grows? | **No — plateau at `1`**, never crosses `4/5` | `[PROVEN]` |
| Extremal object | `δ₋₁₄` all-`ρ=1` self-loop @ `−14 mod 3^k`, **unique** max-mean cycle | `[PROVEN, k=1..6]` |
| Does higher-memory / nonlinear certificate strictly improve? | **No** — LP already ranges over all depth-k `φ`; depth-hierarchy is constant `1`; fixed-point forces `c ≥ 1` | `[PROVEN]` |
| Self-improving in what parameter? | Only in the run bound R (`R/(R+1)`, crosses `4/5` at R=4); NEVER in window k | `[PROVEN, exact]` (hypothesis `R ≤ 3` itself `[OPEN]`, expected false) |
| Can certified induction decide o4 on the frequency axis? | **No** — the `δ₋₁₄` invariant is always seen; excluding it = (K) | `[PROVEN, negative]` |

**Net.** The signature technique, ported to the frequency functional it was never applied to, yields an exact
impossibility mirror of its structure success: `B(3,k)` frequency max-mean cycle `≡ 1`, a plateau above `4/5`, the
`δ₋₁₄` cycle a genuine invariant the finite certificate cannot exclude without (K). o4 and the machine are
untouched.

**No machine decided. No label upgraded.**

Script: `o4_certified_frequency.py` (exact, assertion-checked; all assertions passed). Not committed.
