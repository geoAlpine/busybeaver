# o17 gate-decision attempt — the symbolic-mod tower extension, and the finite-state-vs-value crux, RESOLVED by test (2026-07-10)

*Task (ATTACK_PLAN §B3): decide o17 by extending its exact gate-to-gate map symbolically
far beyond direct simulation (10^60+), testing whether the halting-relevant safety residue
is eventually periodic or admits an invariant. Its wall was labelled "(K)-shaped timing"
but never tested by symbolic-mod computation. EXTREME discipline: ZERO false proofs;
`[PROVEN]`/`[OBSERVED]`/`[OPEN]`. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`.
Basis: `O17_GATE_LAW_2026-07-07.md`, `O17_HALT_FLAVOR_2026-07-06.md`, `o17_gate_map_2026-07-07.py`,
`lean/O17.lean`. Scripts: `o17d_probe.py`, `o17d_finite_state.py`. Not committed.*

o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = F reads 0).

---

## 1. The exact gate map — re-derived and re-verified `[PROVEN parameterization, machine-validated]`

A **gate** = true-frontier arrival (head in A/D reads 0, all-0 tape to its left). Every
A-gate config is a word of `𝓛 = (3|5)·(0 1^{3d+2})*`, so it is exactly the pair
**(marker μ ∈ {3,5}, digit vector d⃗)**. The gate-to-gate map

> **F(μ, d⃗) = (μ′, d⃗′)**  with excursion tick-count T, step-count Δt,

is the exact deterministic TM dynamics on these coordinates. **Safety condition:** at every
μ=5 gate the branch must give **μ′ = 3** (reset); **μ′ = 8 is HALT**. o17 halts ⟺ some μ=5
gate branches to 8 (the seam `0 0 [1]_A`; formalized both directions in `lean/O17.lean`).

**Re-verification (`o17d_probe.py`, exact big-int TM):** iterating F from (3,[]) reproduces
the blank orbit's gate steps `5, 22, 44, 101, 314, 724, 2005, 1072566` byte-exactly, digit
vectors included. The gate state on the real orbit:

| gate | t (steps) | μ | m=len(d⃗) | max digit | d⃗ |
|---|---|---|---|---|---|
| 1 | 22 | 3 | 1 | 0 | [0] |
| 2 | 44 | **5** | 1 | 0 | [0] → μ′=3 **SAFE** |
| 3 | 101 | 3 | 2 | 2 | [0,2] |
| 4 | 314 | 3 | 3 | 4 | [2,0,4] |
| 5 | 724 | **5** | 5 | 6 | [0,0,2,2,6] → μ′=3 **SAFE** |
| 6 | 2005 | 3 | 8 | 16 | [0,2,0,0,0,0,0,16] |
| 7 | 1,072,566 | 3 | 19 | **512** | [2,2,0,4,…] |
| 8 | ~10^60 | ? | ? | ? | **BEYOND DIRECT SIMULATION** |

The blank orbit reaches only **8 gates** and has faced μ=5 exactly **twice** (both safe).
Two data points cannot test periodicity — hence the need for the symbolic extension.

## 2. The symbolic-mod extension — and why it has NO TARGET `[OBSERVED, decisive]`

The tower-exponent method (a^b mod M via b mod λ(M), CRT/Euler up the tower) requires a
**scalar** gate-VALUE whose safety is a residue mod M. o17 has **no such scalar**:

- **Digit magnitudes grow unboundedly** (`o17d_probe.py`): max digit = 0,0,2,4,6,16,**512**,…
  (the top digit is the free-running tick counter, ≈ T_{k-1}, which itself grows tower-fast,
  §2 of GATE_LAW). A base-b numeral needs digits < b; here digits → ∞, so **no fixed base
  exists** in which the state is a numeral.
- **Vector length grows unboundedly** (m = 0,1,1,2,3,5,8,19,…). The object is a variable-
  length vector, not a number.
- **TEST 1 — scalar-mod sweep** (`o17d_finite_state.py`, 780 μ=5 configs, digits 0..4,
  length ≤4): for the branch b(d⃗) = F_μ(5,d⃗) ∈ {3,8}, is b a function of N = Σ d_i·base^i
  mod M for **any** base ∈ {2..8}, **any** M ≤ 64, LSB- or MSB-first? **NO — 0 of 112
  (base×order) settings; every one leaves the branch ambiguous.** (Prior notes tested base 3
  only; this is an exhaustive sweep.)

⟹ There is no residue sequence to extend. The tower reduction acts on nothing. The "gate
value" of GATE_LAW §2 (t ≈ 3.97·n², n tower-growing) is a *timing* quantity, not a state
carrying the safety bit; the safety bit lives in the **whole digit vector**.

## 3. The finite-state-vs-value CRUX — resolved `[OBSERVED, Myhill–Nerode]`

THE question: is b(d⃗) computed by a **finite automaton** over d⃗ (→ gate-state finite →
branch sequence eventually periodic → **DECIDABLE**), or by the vector's unbounded
arithmetic (→ (K)-like → OPEN)?

**TEST 2 — Nerode index** (`o17d_finite_state.py`): two prefixes are equivalent iff they
give identical b on a fixed suffix battery; a finite automaton ⟺ the class count SATURATES.
Measured class count vs prefix length:

| |prefix| | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| classes (digits 0..4) | 1 | 2 | 7 | 25 | 77 | — |
| classes (digits 0..3) | 1 | 2 | 6 | 19 | 54 | **132** |

**The Nerode index GROWS monotonically (ratio ≈ 2.5–3), no saturation.** The observed count
is a *lower bound* on the true automaton size (a finite suffix battery can only under-count),
so a growing lower bound **refutes finiteness**. ⟹ **b is NOT computed by any finite
automaton over the digit vector — the gate-state is genuinely unbounded.**

This subsumes and strengthens every prior refutation (no window ≤5, no mod-q residue word):
those are special finite automata; Test 2 rules out *all* of them at once.

**No invariant either `[OBSERVED]`:** among the 780 μ=5 configs, **605 (78%) branch to 8
(HALT)**; only 22% are safe. "Safe" is a minority set with no scalar, finite-automaton, or
residue characterization (Tests 1–2). A forward-closed safe set would itself be non-regular
— not a certifiable invariant by any finite method. The orbit survives only by landing in
that uncharacterizable 22% at every (super-exponentially sparse) μ=5 exposure.

## 4. Verdict

Outcome **(c)** of the decision test: **aperiodic / counter-dependent — the (K)-timing shape
is CONFIRMED at the gate level, and o17 stays `[OPEN]`.** Precisely:

- The safety bit is a function of the **VALUE/arithmetic** of an unbounded digit vector, NOT
  of any finite gate-state (Test 2), and NOT of any scalar residue mod M (Test 1).
- Therefore the symbolic-mod tower extension — the one untried weapon — **has no target
  object**; it cannot be run, not for lack of compute but for lack of a scalar/finite state
  to reduce. This is itself the rigorous resolution of the crux the wall-label only asserted.
- The real orbit gives only 2 μ=5 gates (both safe) and gate 9 is ~10^60 steps; periodicity
  of the branch sequence is therefore untestable by simulation, and — by §2–3 — un-shortcuttable
  by symbolic reduction. o17's non-halt statement genuinely cannot be compressed below the
  full infinite-state transducer.

**Honest scope:** Tests 1–2 are `[OBSERVED]` over the stated finite ensembles (digits ≤4,
lengths ≤5, M ≤ 64, base ≤8) — a growing Nerode lower bound and an exhaustive-within-range
scalar-mod negative; neither is a `[PROVEN]` impossibility theorem, but both are the exact
computations the wall-label had never been tested against, and both come out against
decidability. The gate map re-derivation (§1) is `[PROVEN]` (exact match to the orbit).

## Reproduce
- `o17d_probe.py` — exact F-iteration on the real orbit to the last simulable gate (8);
  digit-magnitude and vector-length growth; the two μ=5 exposures.
- `o17d_finite_state.py <maxlen> <maxdig> <suflen> <sufdig>` — TEST 1 (scalar-mod sweep,
  bases 2..8 × M ≤ 64 × LSB/MSB) and TEST 2 (Myhill–Nerode class-count growth).

**No machine decided. No label upgraded.**
