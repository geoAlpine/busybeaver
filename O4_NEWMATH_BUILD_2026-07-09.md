# o4 new-math build — the a-priori quenched return-frequency estimate: what the growing budget + proven run-cap actually buy, and the exact residual obstruction (2026-07-09)

*Genuine construction attempt on the easiest rung of the (K) wall, using the NEW weapons (uniform fixed-point /
run-cap theorem, subcritical margin, coboundary LP, white run-depth) that post-date the logged no-gos. Interpreter
`.venv` python, exact big-int; every numeric claim assertion-checked in `o4_newmath_build.py` (all passed, N=2×10⁵).
STRICT labels. Attempts 1–3 of the brief executed IN ORDER. Result: one genuine structural CONSTRUCTION (the fatal
functional is exactly re-identified, sharper than the assessment's "density-burst adversary"), a precise NEW
distinction from Antihydra, and an exact residual obstruction. No route to a decision. NOT committed.*

---

## 0. One-line verdict

**[CONSTRUCTED-partial]** o4's fatality is exactly a **level-1 (shallow) cylinder LARGE-DEVIATION frequency**:
`freq{3 | W_n} ≥ 4/5` (2.4× the annealed 1/3). The two NEW a-priori weapons — the proven run-cap
`v₃(W_n) ≤ 0.262n` and the magnitude bound `Σⱼv₃(Wⱼ) ≤ 0.131n²` — both constrain the **depth support** and the
**quadratic second moment**, which are provably **ORTHOGONAL** to the fatal **linear first moment** `#1 = Σ_run L`.
I construct **two explicit fatal adversary families** (shallow-burst and cap-saturating deep-tiling) that each
respect BOTH new bounds while driving `#1/n` to `5/6` and to `1` respectively. The subcritical margin is real and
strictly weakens the ask (any bound `< 4/5`, vs Antihydra's zero-margin `1/3`), but the residual is the SAME
species: an effective **one-sided single-orbit large-deviation bound on a level-1 cylinder frequency** of the base-
4/3 odometer. **No machine decided. No label upgraded.**

---

## 1. Setup and the exact fatal threshold `[PROVEN, verified]`

Odometer `3G' = 4G + e(ρ)`, `ρ=G mod 3`, `e={0:9,1:14,2:1}`; `W=G+14`, `ρ=1 ⇔ 3|W`, `run(G)=v₃(W)` (run theorem).
Ledger `a'=a+δ`, `δ={1:−1,2:+4,0:+6}`; `ψ=−δ`; **fatal (halt) ⇔ prefix `Σψ ≥ a₀−1`**. Identity
`a_n = a₀ − #1 + 4#2 + 6#0` (verified exact every generation to N=2×10⁵).

> **Fatal threshold `[PROVEN, exact]`.** Cheapest filler is `ρ=2` (cost 4 < ρ=0's 6): `5#1 ≥ 4n+a₀`, i.e.
> **`#1/n ≥ 4/5`** (mixed/ρ=0 filler only raises it, to `6/7`). Equivalently, positive drift along the coboundary
> ladder `1ᵐ2` has mean `(m−4)/(m+1) > 0 ⇔ m ≥ 5` — reproducing the LP threshold (`O4_COBOUNDARY_LP` §4) from the
> orbit side.

Real orbit (seed G=43): `#1/N = 0.33386`, `E[run length] = 1.5001` (annealed exactly 3/2), ledger `+2.9966/gen`,
min ledger over the run `= 16`, max run-depth `= 12` at gen 84 800 (cap `0.262N = 52 380`), `Σv₃/N² = 3×10⁻⁶`.
The margin to fatality is enormous and the orbit sits **at the annealed first moment**.

## 2. The central CONSTRUCTION — fatal = level-1 cylinder large deviation; the two new weapons are orthogonal to it `[CONSTRUCTED-partial]`

`#1 = #{j≤n : 3 | Wⱼ}` is a **level-1 cylinder count**. Two independent decompositions:

- **First moment (fatal):** `#1 = Σ_{ρ=1 runs} L`, `L = v₃(W_entry)`. Linear; this is the fatal functional.
- **Magnitude (available):** `Σ_{j≤n} v₃(Wⱼ) = Σ_run L(L+1)/2 ≤ log₃∏Wⱼ ≈ 0.131 n²`, because `Wⱼ ≈ 57(4/3)ʲ`
  for EVERY orbit (the ±5,±13 perturbations are O(1)). Quadratic; a **second-moment** functional.

**Orthogonality lemma `[CONSTRUCTED-partial]`.** The two proven weapons control only depth-support and the
quadratic moment, both vacuous in the fatal direction:

1. **Run-cap `v₃ ≤ 0.262n`** bounds the *support* of a single run's depth. But `#1 ≥ 4/5·n` is reachable with runs
   of depth `5` (`5 ≪ 0.262n` for `n≥20`): the cap never binds.
2. **Magnitude vs fatal, quantified by Cauchy–Schwarz.** With `R ~ cn` runs, `(Σ L)² ≤ R·Σ L²` and
   `Σ L² ≤ 0.26 n²` give only `Σ L ≲ n^{3/2}` — superlinear, weaker than the fatal `0.8 n` by a factor `√n`. The
   quadratic magnitude moment cannot bound the linear fatal moment from above. (In Antihydra's excursion route the
   contested energy `E[K²]` at least *matched* the fatal quantity's degree yet was clustering-blind; for o4 the one
   a-priori magnitude functional has the WRONG degree for the fatal count.)

**Two explicit fatal adversaries respecting BOTH weapons (constructed, verified):**

| adversary | itinerary | `#1/n` | max depth vs cap | `Σv₃/n²` vs 0.131 | fatal? |
|---|---|---|---|---|---|
| **A** shallow-burst | `(1⁵2)*` | `0.833` | `5 ≤ 0.262n` ✓ | `1.2×10⁻⁵` ✓ | **yes** |
| **B** deep-tiling | `Lᵢ=⌊0.262 sᵢ⌋`, one `2` between | `→1` | at equality ✓ | `0.058` ✓ | **yes** |

Both are realized by explicit seed classes mod `3^n` (bijection, `O4_LEDGER_ANALYSIS` §2). **Neither the run-cap nor
the magnitude bound excludes `#1/n → 1`.** This is a strict *sharpening* of the assessment's density-burst adversary:
we now have the exact functional (`level-1 cylinder`), the exact orthogonality mechanism (support + wrong-degree
moment), and TWO cap-respecting witnesses (one shallow, one saturating the cap at equality).

## 3. Attempt 1 result — the run-cap kills a class that was never fatal `[OBSTRUCTION, precise]`

The brief's hope: does a heavy-tail adversary respecting `run ≤ 0.262n` AND first-moment-matched still exist? Both
fatal conditions are first-moment (mean-depth / cylinder-frequency) statements — Antihydra's is
`E[D] < 3/2` (`#even/n = 1 − 1/E[D] < 1/3`), o4's is `#1/n ≥ 4/5`. The **decisive distinction is the MARGIN**, and it
flips the adversary type:

> **Antihydra (zero margin):** the fatal boundary passes THROUGH the annealed mean (`E[D] = 3/2` exactly), so a
> **matched-mean** adversary sits ON the boundary — critical, undecidable at first order — and the excursion route
> then needed the SECOND moment `E[K²]` to try to push off, dying there against the heavy tail.
> **o4 (margin 2.4×):** a matched-mean adversary has `#1/n = 1/3 ≪ 4/5` — safely NON-fatal. The o4 fatal adversary
> can therefore NOT be a matched-mean heavy tail; it must be a genuine **WRONG-FREQUENCY (large-deviation) orbit**,
> `#1/n → 4/5`.

The run-cap genuinely DOES exclude the one adversary class Antihydra could not (a single over-cap catastrophic run,
`O4_RUN_STRUCTURE` §2) — but that class was never o4's fatal mode; the fatal mode is a shallow high-frequency
conspiracy (adversary A) or a cap-saturating tiling (adversary B), both cap-legal and both wrong-frequency. **The
run-cap lands on an empty target.** Precise missing ingredient: an upper bound on the *large-deviation frequency* of
the level-1 cylinder, about which the cap (a support statement) is structurally silent.

## 4. Attempt 2 — weighted / budget-growing sub-action on B(3,k) `[OBSTRUCTION = δ₋₁₄, growth-proof]`

Can a sub-action *allowed to grow with the budget* close where the bounded one (max-mean `+1`, `O4_COBOUNDARY_LP`)
failed? **No, and the reason is growth-independent.** Any `φ` (bounded OR unbounded) obeying the sound pointwise
inequality `ψ(G) ≤ φ(TG)−φ(G)+c` **for all integers G** must obey it at the integer fixed point `−14`
(`T(−14)=−14`, `ψ=+1`): `1 ≤ 0 + c`, forcing `c ≥ 1 > 0` — no telescoping upper bound on `Σψ`. Growth cannot evade a
*fixed* point: the constant orbit at `−14` is a genuine orbit the certificate must dominate. The only escape is to
drop the inequality at `−14`, i.e. use the specific seed's avoidance of the `−14`-shadow cylinders — quenched, the
open object. A growing sub-action that *is* the ledger `a_n` merely restates the target: its unconditional lower
bound is the conjecture (and fatal orbits exist, so no unconditional bound exists). This transposes
`MAGNITUDE_LYAPUNOV` (growing sub-actions charge only the free count) intact. **Route closed at δ₋₁₄, unchanged by
the subcritical margin** (the margin lowers the *required constant* from the fatal threshold, but the obstruction is
the *sign* `c ≥ 1 > 0` at the fixed point, threshold-independent).

## 5. Attempt 3 — moving-diagonal 3-adic digit / base-4/3 normality `[OBSTRUCTION = quenched digit frequency]`

`d_n = v₃(W_n)`, `W_n ≈ 57·(4/3)ⁿ`, so `d_n` is the moving-diagonal 3-adic digit of a `×4/3` orbit — the exact base-
**4/3** sibling of Antihydra's base-3/2 (the "4/3 problem" of the AEV normality umbrella, `NEW_MATH_PROGRAM` §9).
Halting `⇔` base-4/3 digit-0 frequency `≥ 4/5`. The run-cap supplies a genuine NEW **a-priori per-digit support
constraint** (digit at position `n` has value `≤ 0.262n`) that the annealed digit theorems (Drmota–Spiegelhofer,
Mauduit–Rivat) do not use — but those theorems are for the *sequence* `(p/q)ⁿ`, annealed, and give no **one-sided,
single-orbit, large-deviation** frequency bound. Quenching the annealed statement to the seed-57 orbit is exactly the
missing step; the support constraint reads one digit's *magnitude*, never the *frequency* across `j ≤ n`. **Route
reduces to effective one-sided base-4/3 normality for one orbit** — same species as (K), different base.

## 6. What was CONSTRUCTED, what obstructs (summary)

| item | content | label |
|---|---|---|
| Exact fatal threshold | `#1/n ≥ 4/5` (`ρ=2` filler); ladder `(m−4)/(m+1)` reproduced orbit-side | `[PROVEN, verified]` |
| Fatal functional identified | level-1 cylinder count `#1 = Σ_run L`, a **first moment** | `[CONSTRUCTED]` |
| Orthogonality lemma | run-cap = depth-support, magnitude = quadratic 2nd moment; C–S gap `n^{3/2} ≫ n` | `[CONSTRUCTED-partial]` |
| Two cap-legal fatal adversaries | shallow-burst `#1/n=5/6`; deep-tiling `#1/n→1` at cap equality | `[CONSTRUCTED, verified]` |
| NEW distinction from Antihydra | MARGIN flips the adversary: Antihydra zero-margin ⇒ matched-mean is critical (heavy-tail killer); o4 margin 2.4× ⇒ matched-mean non-fatal, adversary is **wrong-frequency large deviation** | `[CONSTRUCTED-partial]` |
| Attempt 1 (run-cap potential) | cap excludes only the never-fatal single deep run; empty target | `[OBSTRUCTION]` |
| Attempt 2 (growing sub-action) | δ₋₁₄ fixed point forces `c ≥ 1`; growth-independent | `[OBSTRUCTION, PROVEN mechanism]` |
| Attempt 3 (base-4/3 digit) | reduces to one-sided single-orbit base-4/3 normality | `[OBSTRUCTION]` |

## 7. The exact residual obstruction — sharper than "it's (K)"

> **Missing ingredient (precise).** An a-priori upper bound `freq_{j≤n}{3 | Wⱼ} ≤ 4/5 − ε` for the *specific* seed-57
> orbit — a **one-sided LARGE-DEVIATION bound on a single level-1 cylinder frequency** of the affine `×4/3` 3-adic
> orbit. Three sharpenings over "it is (K)":
> 1. It is a **first-moment-order** statement: the gap is a density CONSTANT (`4/5` vs annealed `1/3`), NOT a
>    moment-degree upgrade — o4 needs no second moment at all (`O4_GROWING_BUDGET_ASSESSMENT` §1: refill-sum ≡
>    drain-count closes the second moment to `0=0`). Antihydra's un-pre-empted route by contrast had to climb to the
>    second moment `E[K²]` (excursion energy) and died there.
> 2. It tolerates a **huge margin**: any effective `< 4/5` suffices vs Antihydra's exact `1/3` zero-margin. Because
>    the margin holds the fatal boundary far from the annealed mean, the target is a *lossy large-deviation upper*
>    bound (may lose a factor `2.4×`), not equidistribution — a genuinely weaker analytic object.
> 3. Both new weapons are **provably orthogonal** to it (support + wrong-degree moment); the remaining tool must read
>    the seed's arithmetic in the level-1 direction — the `NEW_MATH_PROGRAM` §3 quenched-frequency object at its
>    lowest rung (base 4/3, level 1, one-sided, margin 2.4).

Why no existing tool delivers it: a single level-1 cylinder frequency for one orbit is exactly single-orbit
equidistribution; **large-deviation upper bounds require either an invariant measure (the orbit is one point) or a
transfer estimate that reads more than the first moment/support (both weapons max out there)**. The subcritical
margin says we may lose a constant factor — but no known method produces even a *lossy* one-sided cylinder-frequency
bound for a single amenable `×(p/q)` orbit without the annealed→quenched crossing (`NEW_MATH_PROGRAM` §8.7: no
Gauss-map coordinate, non-Pisot + amenable).

## 8. Verdict

The growing budget + proven run-cap buy exactly **one genuine gain over Antihydra, now made precise**: the large
margin (`4/5` vs zero) holds the fatal boundary far from the annealed mean, so o4 stays first-moment-order (no energy
bridge needed) and the fatal adversary is forced from a matched-mean heavy tail into a **wrong-frequency large
deviation** — a strictly lower rung. Everything the two new a-priori weapons
control (depth support, quadratic moment) is **orthogonal** to that first-moment fatal direction, witnessed by two
explicit cap-legal fatal adversaries. No potential, weighted sub-action, or digit argument crosses the gap; the
residual is a one-sided, margin-2.4, level-1, base-4/3 single-orbit large-deviation frequency bound — the sharpest
statement yet of o4's open core, and a strict weakening of (K) that is nonetheless of the identical species and blocked
by the identical annealed→quenched wall.

**No machine decided. No label upgraded.**

Scripts: `o4_newmath_build.py` (exact, all assertions passed, N=2×10⁵). Not committed.
