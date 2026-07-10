# o4 non-halting — search for a genuinely NEW reformulation (2026-07-10)

*Meta-goal: CHANGE THE QUESTION, not the tool. Find a condition EQUIVALENT to "o4 never halts" that is NOT the
frequency statement `freq{3|W_n} ≤ 4/5`, and that might admit a different proof (combinatorial / order-theoretic /
algebraic / a different observable). Interpreter `.venv` python, exact `int`/`Fraction`, every structural claim
assertion-checked (`o4_equivalents_search.py`, all passed). STRICT labels. NOT committed.*

Setup: `3G'=4G+e(ρ)`, `ρ=G mod 3`, `e={0:9,1:14,2:1}`; `W=G+14`, `ρ=1⇔3|W`, `run(G)=v₃(W)`; ledger `a'=a+δ`,
`δ={1:−1,2:+4,0:+6}`, `ψ=−δ`. Prefix walk `S_n=Σ_{j<n}ψ(ρ_j)`; **`a_n = a₀ − S_n`**; halt ⇔ `S_n ≥ a₀−1` ⇔
`a_n ≤ 1`. Closed identity `a_n = a₀ + 4n − 5#1 + 2#0` (verified exact to N=2×10⁵).

## 1. The KNOWN equivalents are ONE inequality on ONE walk `[PROVEN, verified]`

| # | equivalent | exact form | flavor |
|---|---|---|---|
| (a) | ledger never underflows | `a_n ≥ 2 ∀n` | additive budget |
| (b) | frequency bound | `freq{3∣W_n} = #1/n ≤ 4/5` (asympt.) | Cesàro density |
| (c) | multi-run conspiracy | `Σ_run v₃(W_entry) < a₀−1+…` prefix-wise | run-depth sum |

All three are the single statement **`S_max := sup_n S_n ≤ a₀−2`** (since `a_n=a₀−S_n`, `#1=Σ_run v₃`). On the real
orbit `S_max=1`, attained at gen 0; margin to the fatal level `a₀−2=15` is 14. (b) is the *asymptotic drift* proxy
for this finite running-max condition; they are not identical (b is a Cesàro limit, the true condition is a
finite-time extremum), but (b)-with-margin ⟹ (a). This is the baseline: the frequency statement is one face of a
first-passage problem.

## 2. NEW equivalents searched, each with tractability verdict

**N1 — Running-max / first-passage (order-theoretic).** Non-halt ⟺ `M:=sup_n S_n ≤ a₀−2`. `M` is a *single integer*
determined by the orbit; a genuinely different **observable** (an extreme value, not an average). On a non-halting
orbit `M` is attained in a **bounded early window** (verified: `M=1` at gen 0, `S` never within 5 of `M` after gen 1),
because drift `−3/gen` + the proven run-cap `v₃≤0.262n` bound every future upcrossing. *Tractability:* bounding `M`
= bounding the largest large-deviation of the same density; the one honest gain is that non-halt follows from ANY
effective `freq{3∣W}≤4/5−ε` past a computable gen `n₀` (the subcritical margin, already known). **Not a new route.**

**N2 — Well-founded descent / rank.** Non-halting is *not* termination, so there is no ordinal descent to exhibit.
The only order-theoretic certificate is an **inductive invariant** `a≥2`, which IS the conjecture; and
`O4_COBOUNDARY_LP` `[PROVEN]` that no finite-state (residue) inductive invariant exists (max-mean cycle `+1` at the
`−14` self-loop). **Route closed.**

**N3 — Nonlinear invariant `Φ_n = S_n + 5·v₃(W_n)`** (potential `φ=−5v₃`, the `O4_COBOUNDARY_LP §4` sub-action on the
de Bruijn graph with the `−14` atom deleted). On the real orbit `max Φ_n = 5` (bounded ⇒ the certificate **holds on
this orbit**), because runs stay shallow (max depth 12). But a deep return `v₃(W)=L` makes `Φ` jump by `~5L`, so
**boundedness of `Φ` ⟺ a frequency bound on deep 3-adic returns ⟺ (K)**; the inequality fails exactly at the integer
fixed point `−14` (all-`ρ=1`). This is the best "different-flavor" (nonlinear, magnitude-reading) object — and it
still reduces. **Not a new route** (confirms the growing-sub-action no-go, `O4_NEWMATH_BUILD §4`).

**N4 — Diophantine / algebraic shape.** Halt ⟺ `5#1 − 2#0 ≥ 4n + a₀ − 1` — a **linear inequality in the counts**.
There is **no exponential / S-unit / linear-forms equation**. Contrast o7: halt ⟺ `3^v·oddpart − 1 = 2^k`, an
S-unit equation Baker could in principle touch. **The Baker / S-unit / Diophantine-reachability route is
STRUCTURALLY INAPPLICABLE to o4** — o4's halt is not an equation-hitting, it is a count-threshold.

**N5 — Topological 3-adic avoidance (the thin-vs-density crux).** By the itinerary bijection, fatal itineraries ↔
fatal seed-classes mod `3^L`. Machine-computed the fatal **fraction** of length-`L` itineraries: it **converges to a
POSITIVE constant** `η^{a₀−1}` (`η=0.334895`): e.g. `a₀=2 → 0.33489`, `a₀=3 → 0.11215`, stable from `L=16`. So the
fatal set is **FAT** (positive measure `≈η^{a₀−1}`, exponentially many `≈η^{a₀−1}·3^L` classes), *dense* (fatal
patterns exist at every level), and the safe set is a **positive-measure nowhere-dense Cantor set**. Non-halt ⟺
seed 43 lands in this fat Cantor set — a **large-deviation (density) avoidance**, NOT a thin (measure-zero)
reachability target. (o7's obstruction `{2^k}` is measure-zero/thin — the opposite.)

**N6 — Halting-side semidecidability.** The halt set is r.e.; its emptiness is exactly the conjecture; no new
characterization emerges.

## 3. The decisive structural finding (why nothing escapes)

`a_n` is an **additive functional** of the itinerary and halt is a **level-crossing of a FIXED threshold by a
strongly-drifting sum**. By Cramér, a level-crossing of a drifting additive functional is intrinsically a
**first-moment / large-deviation (density)** event — the fatal set is *fat* (§N5, `η^{a₀−1}>0`). This is
categorically different from the **thin-reachability** band (o7, Space Needle: hit `2^k`, an S-unit, measure-zero),
where a genuinely different Diophantine/Baker route is at least conceivable. Every reformulation above — extreme
value (N1), rank (N2), nonlinear invariant (N3), algebraic (N4), topological (N5) — re-expresses the SAME fat
density event. **No searched equivalent opens a non-(K) route.** The search's positive yield is the *reason*:
o4's halt is provably density-species (additive-functional level-crossing) with no thin/Diophantine escape hatch —
it is firmly the least-protected instance of the (K)/base-4/3-normality band, not a hidden member of the
o7-style reachability band.

**No machine decided. No label upgraded.**

Script: `o4_equivalents_search.py` (exact, all assertions passed). Not committed.
