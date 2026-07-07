# Coboundary / sub-action LP for the o4 odometer residue levels — machine-run, exact (2026-07-08)

*Queued housekeeping upgrade from `O4_GROWING_BUDGET_ASSESSMENT_2026-07-07.md` §3/§6: machine-run the o4 analogue
of `MINPROP_COBOUNDARY_LP.md` on residue levels mod `3^k`, upgrading the Route-2 transposition (`δ₋₁₄` kills the
sub-action route) from `[ASSESSED]` to `[PROVEN]`. Script `o4_coboundary_lp.py`, interpreter `.venv` python, **exact
`int`/`Fraction` arithmetic only, every claim assertion-checked** (any failure aborts; the run passed all
assertions, k = 1..8). NOT committed.*

---

## 0. One-line answer

The o4 residue-level sub-action LP is **INFEASIBLE at every level `k = 1..8`, and provably at all `k`**: the max
mean cycle of the level-`k` constraint graph is **exactly `+1` at every level**, attained **uniquely** by the
self-loop at the residue class of `−14 mod 3^k` — the dual obstruction is the atomic invariant measure **`δ₋₁₄`**
(the `[PROVEN]` integer fixed point `T(−14) = −14` of `O4_RUN_STRUCTURE_2026-07-07.md` §1) with
`∫ψ_o4 dδ₋₁₄ = +1 > 0`, exactly as claimed in the assessment's Route 2. The minimal feasible constant is
`c* = +1`: **the LP optimum equals the trivial pointwise bound `ψ ≤ 1` — residue structure extracts exactly
nothing below the free count `#1 ≤ n`.** Route-2's closure is hereby **`[PROVEN]`** (was `[ASSESSED]`); the o4
No-Structure mirror of `MINPROP_COBOUNDARY_LP.md` is complete. o4 itself remains `[OPEN]`.

---

## 1. Setup: potential, sign convention, and what feasibility would prove `[PROVEN, trivial]`

Odometer `3G′ = 4G + e(ρ)`, `ρ = G mod 3`, `e = {0:9, 1:14, 2:1}`; ledger `a′ = a + δ(ρ)`,
`δ = {1:−1, 2:+4, 0:+6}`. Set
> `ψ = −δ = 1{ρ=1} − 4·1{ρ=2} − 6·1{ρ=0}`   (the assessment's `ψ_o4`; values `{1:+1, 2:−4, 0:−6}`).

Ledger fatality at step `n` ⟺ prefix `Σ_{j<n} ψ(ρ_j) ≥ a₀ − 1`, so the ledger condition is "prefix Birkhoff sums
of `ψ` bounded above" (a fortiori `limsup (1/N)Σψ ≤ 0`). A **residue-level sub-action** is a `φ: ℤ/3^k → ℝ` with
> `ψ(G) ≤ φ(T(G) mod 3^k) − φ(G mod 3^k) + c`,  `c ≤ 0`,  **for all integers `G`**

(the sound over-approximation — a residue certificate cannot know which windows the specific orbit visits, exactly
as MINPROP's "pointwise for all odd `o`"). Telescoping: feasible ⟹ `Σψ ≤ 2‖φ‖_∞ + cN` for **every** orbit ⟹ the
ledger conjecture unconditionally (for `c < 0` outright; for `c = 0` up to a finite computable check). By LP
duality (difference constraints / max-mean-cycle, the identical MINPROP §2 mechanism): **feasible for some
`c ≤ 0` ⟺ the constraint graph has no positive-mean cycle; the minimal feasible `c` = the max mean cycle.**

**No tail truncation is needed** — a soundness *advantage* over Antihydra: `T(G) mod 3^k` is exactly determined by
`G mod 3^{k+1}` (one-symbol lookahead), whereas MINPROP's `D = v₂(3o−1)` is unbounded and needed the audited
`−3/2` tail treatment. The o4 level-`k` graph is exact, no undetermined branch.

## 2. The residue automaton — CORRECTION: not a permutation, but the full de Bruijn shift `[PROVEN, machine-verified k=1..8]`

The task brief's reading "T is a bijection on residues mod `3^k`" is **false** and was machine-refuted:
`T(a) mod 3^k ≠ T(a + 3^k) mod 3^k` for **every** residue `a` (the images differ by `4·3^{k−1} ≡ 3^{k−1}`), so
`T` is not even well-defined on `ℤ/3^k`. What the itinerary bijection (`O4_LEDGER_ANALYSIS` §2:
`{G mod 3^k} ↔ (ρ₀,…,ρ_{k−1})`, verified again here for k = 1..8) actually gives is: **T acts on windows as the
SHIFT**, and the level-`k` constraint graph (nodes `ℤ/3^k`, one edge per lift `r mod 3^{k+1}`, weight `ψ(r mod 3)`)
**is exactly the complete 3-ary de Bruijn graph `B(3,k)`**: node = window `w = (ρ₀…ρ_{k−1})`, edges
`w → w[1:]σ` for all `σ`, weight `ψ(w₀)`. Machine-verified edge-by-edge for k = 1..8, plus:

- **3-out / 3-in regular** (3 distinct targets per node; `T: ℤ/3^{k+1} → ℤ/3^k` exactly 3-to-1 onto);
- **strongly connected, diameter = k** (BFS both directions; max distance from any node = k); the seed class
  `43 mod 3^k` reaches `−14 mod 3^k` in ≤ k steps — **no domain-restriction dodge exists**;
- **cycle structure** (the honest replacement for "permutation cycle counts"): closed walks of length `L` ↔
  periodic itineraries of period `L`; **`trace(A^L) = 3^L` for every `L`** (machine-verified k ≤ 4, L ≤ 8; provable
  for all k via the bijection) — the zeta function is the full-3-shift's `1/(1−3t)` at every level. **Exactly 3
  self-loops at every level:** the branch fixed-point classes `−9, −14, −1 mod 3^k`, weights `−6, +1, −4` — exactly
  one positive.

## 3. Result: INFEASIBLE at every k; dual obstruction = `δ₋₁₄`, uniquely `[PROVEN]`

| `k` | `\|V\| = 3^k` | `\|E\| = 3^{k+1}` | verdict | max-mean cycle | obstruction | atom deleted: max-mean |
|---|---|---|---|---|---|---|
| 1 | 3 | 9 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 3` | `−4` |
| 2 | 9 | 27 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 9` | `−3/2` |
| 3 | 27 | 81 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 27` | `−2/3` |
| 4 | 81 | 243 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 81` | `−1/4` |
| 5 | 243 | 729 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 243` | `0` |
| 6 | 729 | 2187 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 729` | `+1/6` |
| 7 | 2187 | 6561 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 3^7` | `+2/7` |
| 8 | 6561 | 19683 | **INFEASIBLE** | `+1` | self-loop @ `−14 mod 3^8` | `+3/8` |

- **`max-mean = +1` exactly, all k `[PROVEN]`:** upper bound `max edge weight = +1`; lower bound the self-loop at
  `−14 mod 3^k` (the lift `≡ −14 mod 3^{k+1}` maps into the same class, weight `ψ(1) = +1`) — present at **every**
  level because `−14` is a genuine integer fixed point (`3·(−14) = 4·(−14) + 14`), level-independent, so the
  infeasibility holds **for all k**, not just k ≤ 8. Cross-checked by an independent exact algorithm (Karp,
  `Fraction` arithmetic) for k ≤ 6: value `= 1` on the nose.
- **Uniqueness `[PROVEN, k = 1..8]`:** a mean-`+1` cycle must use only weight-`+1` edges (max weight is 1), i.e.
  all-`ρ=1` sources; the induced weight-1 subgraph minus the `−14` loop is a **DAG** (Kahn) — so **the `δ₋₁₄`
  self-loop is the ONLY maximizing cycle at every level**. The maximizing cycle IS the class of `−14`, i.e. the
  all-`ρ=1` itinerary, confirming the assessment's Route-2 picture exactly; the sup over cycle averages does not
  merely persist — it is the **constant `+1` at every k** (no convergence question remains; the claimed value `+1`
  at `δ₋₁₄` is exact).
- **The LP value is the trivial bound:** min feasible `c* = +1` = the pointwise sup of `ψ`. Residue-level structure
  extracts **zero** margin below the free count `#1 ≤ n` — the exact dual restatement of the assessment §1's "the
  free first moment is the same object on both sides".

## 4. Pervasiveness has an exact LAW — the refinement `[PROVEN, exact, k = 1..8]`

Deleting the atom's node (`−14 mod 3^k`) from the graph, the max mean cycle is **exactly `(k−5)/k`** at every
level, attained by the cycles **shadowing the all-`ρ=1` itinerary with minimal interruption**: the word
`1^{k−1} 2` (k−1 drains, one refill), mean `((k−1)·1 − 4)/k`. Proof, fully machine-checked: lower bound = the
explicit cycle (edges verified in the graph); upper bound = an **exact analytic potential**
`φ(a) = −5·min(v₃(a + 14), k)` (`= −5 ×` the leading `ρ=1`-run of `a`'s window, by the run theorem — the potential
is precisely *3-adic proximity to the fixed point*), verified to satisfy the rescaled constraints
`k·ψ − (k−5) ≤ φ(v) − φ(u)` on every deleted-graph edge, with equality along the exhibited cycle. Karp cross-check
k ≤ 6 agrees exactly.

**Surprise vs Antihydra:** MINPROP found positive cycles surviving atom-deletion at every tested level; o4's
obstruction is **atom-concentrated at low levels** — for `k ≤ 4` deleting `δ₋₁₄`'s class restores feasibility
(`(k−5)/k < 0`), `k = 5` is exactly critical (`0`), and only for `k ≥ 6` do the shadowing cycles take over,
converging to `+1` from below (`1 − 5/k ↗ 1`). So the obstruction picture is refined, not changed: **at every
level the maximum IS at `−14`; the runner-up is its 3-adic shadow family, and pervasiveness sets in at `k = 6`
with the exact rate `1 − 5/k`.**

**The run-bound ladder (dual-side localization of the open core) `[PROVEN, exact at k = 6]`.** Restricting to the
subshift of itineraries with all `ρ=1`-runs `≤ R` (cycles = periodic words with runs `≤ R`; the level-6 filter is
exact for `R ≤ 5`), the max mean cycle is **exactly `(R−4)/(R+1)`**:

| runs ≤ R | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| max-mean | `−3/2` | `−2/3` | `−1/4` | `0` | `+1/6` |
| sub-action | feasible, `c<0` | feasible, `c<0` | feasible, `c<0` | feasible, `c=0` only | **INFEASIBLE** |

I.e. **an eventual run bound `v₃(W_n) ≤ 3` at run entries would DECIDE o4 through this very LP** (margin `−1/4`);
`R = 4` is exactly critical; `R ≥ 5` already carries the obstruction. Since `run(G) = v₃(G+14)` is expected
unbounded along the orbit (and nothing proven caps it below the `0.262n` archimedean cap), this is a
**localization, not a route**: it re-derives `O4_RUN_STRUCTURE` §4 ("the open content is the frequency of deep
3-adic returns") from the dual side, with the exact threshold **depth 4**. Observed longest run so far: 2.

## 5. The exact sound statement proved

> **`[PROVEN]` (negative).** For every `k ≥ 1` there is **no** `φ: ℤ/3^k → ℝ` and `c ≤ 0` with
> `ψ(G) ≤ φ(T(G) mod 3^k) − φ(G mod 3^k) + c` for all integers `G`; indeed the minimal feasible `c` is `+1`.
> Dual obstruction: the atomic `T`-invariant measure `δ₋₁₄` (integer fixed point, all-`ρ=1` itinerary,
> `∫ψ = +1 > 0`), realized at every level as the unique max-mean (= `+1`) cycle — a self-loop at `−14 mod 3^k`.
> The Birkhoff sums of `ψ` are not uniformly bounded above over all orbits: the constant orbit at `−14` has
> `Σψ = +N`. Machine-run k = 1..8 exact; level-independence by the integer fixed point. The bounded-residue
> sub-action route for the o4 ledger is **structurally dead**, mirror-identical to Antihydra's
> (`δ₁`, `+1/2`) ↦ (`δ₋₁₄`, `+1`).

This upgrades `O4_GROWING_BUDGET_ASSESSMENT_2026-07-07.md` §3 (Route 2) from `[ASSESSED]` to **`[PROVEN]`** and
completes the o4 mirror of the No-Structure corpus (`MINPROP_COBOUNDARY_LP.md` → this file;
`BB6_NO_STRUCTURE_THEOREM.md` §3(1) analogue at the B2 flagship). As there, the missing ingredient is exactly
what residues cannot carry: the specific seed's avoidance of the `−14`-shadowing cylinders — the
`NEW_MATH_PROGRAM.md` §3 quenched return-frequency object, unchanged.

## 6. Verdict (0 false proofs)

| question | answer | label |
|---|---|---|
| Is the o4 residue sub-action LP feasible at any `k` (⟹ unconditional ledger proof)? | **NO** — infeasible at every `k = 1..8` and provably all `k`; min feasible `c = +1`. | `[PROVEN]` |
| Dual obstruction | `δ₋₁₄` (integer fixed point `T(−14)=−14`, `ρ≡1`), self-loop weight `+1` at `−14 mod 3^k`, **unique** max-mean cycle at every level; `∫ψ_o4 dδ₋₁₄ = +1` exactly as assessed. | `[PROVEN]` |
| Is the residue automaton a permutation (task brief's reading)? | **NO** — `T` is ill-defined on `ℤ/3^k` (3-to-1 from level k+1); the graph is the complete de Bruijn shift `B(3,k)`, 3-regular, strongly connected, `trace(A^L) = 3^L`, exactly 3 self-loops (`−9, −14, −1`). | `[PROVEN]` |
| Sup of cycle averages across k — converges to what? | Constant `+1` at every k (attained, unique); with the atom deleted, exactly `(k−5)/k ↗ 1` (shadow cycles `1^{k−1}2`), positive only for `k ≥ 6`. | `[PROVEN]` |
| Truncation soundness | No truncation exists to audit: one-symbol lookahead is exact (advantage over MINPROP's tail branch). | `[PROVEN]` |
| Any conditional content extracted? | Run-bound ladder: sub-action feasible below run-depth 4 (`(R−4)/(R+1)`), infeasible from 5 — the open core localized to frequency of depth-`≥4` returns, dual-side. | `[PROVEN, exact]` (hypothesis itself `[OPEN]`, expected false) |

**Net.** Route-2 of the growing-budget assessment is now a theorem: the o4 excursion/sub-action register is closed
by exactly the Antihydra mechanism, with a *stronger* obstruction constant (`+1` vs `+1/2`), a *cleaner* graph (no
tail), an exact pervasiveness law, and an exact conditional threshold (run-depth 4). The o4 ledger conjecture and
the machine are untouched: this is an impossibility theorem about certificates, not progress toward a decision.

**No machine decided. No label upgraded.**

Script: `busybeaver/o4_coboundary_lp.py` (exact, assertion-checked; all assertions passed). Not committed.
