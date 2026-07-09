# A census of the BB(6) Type-I cryptids: uniform reduction to one p-adic return-frequency problem

*Integrative paper-style synthesis. This document collects the campaign's results into a single map: what every
analyzed BB(6) cryptid IS (a q-adic depth process of an explicit ×p/q orbit), what is PROVEN about it (gate,
structure, depth axis, criticality position), and what remains OPEN (the frequency axis, uniformly (K)). It cites
the discovery notes and the Lean layer for each claim; it introduces no new claim. No machine is decided.*

## 0. Scope and status conventions

The BB(6) "cryptids" are 6-state Turing machines whose halting is undecided by all known certified deciders because
each encodes an open arithmetic problem. This census covers the **Type-I** family — value-odometer machines with a
rational multiplier p/q — comprising the 13 orbits analyzed in the campaign. Labels: `[PROVEN]` (complete elementary
proof + exhaustive machine verification), `[PROVEN, Lean]` (additionally checked in the Lean 4 layer, axiom audit
`[propext, Quot.sound]` only), `[PROVEN on grid]` (certified trace-template, red-team-audited, not yet Lean),
`[OBSERVED]`, `[OPEN]`. **No cryptid is decided.**

## 1. The three-part anatomy (uniform across the family)

Every analyzed cryptid decomposes as **GATE + STRUCTURE + PROTECTION** (`BB6_CRYPTID_SPECIES_2026-07-07.md`):
- **GATE `[PROVEN from the transition table]`** — a local halt condition with a forced predecessor chain, whose
  halt-relevant window census saturates small and safe (o18: 1 window, o15: 2, o3: 6, o17: 11, o4: 23). The gate is
  never the obstruction.
- **STRUCTURE** — the generation dynamics: a rigid certified template (o4/o3/o15/o18/o2/o11/o13/o14/o16), a pushdown
  3-adic odometer (o18), or provably no finite template (o17, unbounded generation shapes).
- **PROTECTION `[OPEN]`** — the single arithmetic conjecture that the gate never fires; uniformly a (K)-type
  frequency statement (§4).

## 2. The uniform reduction theorem `[PROVEN, Lean: Mirror.lean]`

Each machine, at its milestone variable v, iterates `T(v) = ⌊(p/q)v⌋ + c(v)` with `gcd(p,q)=1`; each branch is
affine, `b(v) = (pv+e)/q`, with integer fixed point `x = −e/(p−q)`.

**Theorem (uniform fixed-point run law).** Because p is a unit in ℤ_q, `b(v) − x = (p/q)(v − x)`, so `v_q(b(v)−x) =
v_q(v−x) − 1`; the maximal run of a branch from v is `v_q(v − x_branch)`, capped by `log_q|v−x|`.

Machine-checked abstractly (`vqn_unit_mul`: the coprime lemma; `run_closed_form`; `run_cap`), with all census machines
as one-line corollaries. For q=2 the fixed points close as `x_even = −2c_e`, `x_odd = 1 − 2c_o`.

## 3. The census

| machine | ×p/q | q-place | fixed points | run law | Lean |
|---|---|---|---|---|---|
| **o4** | ×4/3 | v₃ | (−9,−14,−1) | v₃(G−x_ρ) | machine→arithmetic **END-TO-END** (odometer + ledger) |
| **o3** | ×4/3 | v₃ | (roles swapped: a=odometer) | — | machine + body + generation map |
| **o15 / o18** | ×8/3 | v₃ | 1 | v₃(V−1) | machine + sweeps (o18); depth in Mirror |
| **o2** | ×3/2 (ceiling) | v₂ | (0,1) | v₂(y),v₂(y+1) | Link 0 certified; run law corollary |
| **o11** | ×3/2 | v₂ | (−8,−7) | v₂(m+8),v₂(m+7) | corollary |
| **o13** | ×3/2 | v₂ | (−14,−7) | v₂(a+14),v₂(a+7) | corollary |
| **o14** | ×3/2 | v₂ | (−12,−11) | v₂(a+12),v₂(a+11) | corollary |
| **o16** | ×3/2 | v₂ | (−4,−3) | v₂(s+4),v₂(s+3) | corollary |
| **o17** | — | — | none (no fixed point) | — | gate map (Python) |
| **Space Needle** | ×5/2 | v₂ | even 0; **odd none** | v₂(m) (even) | even-branch corollary |
| **Antihydra / o10** | ×3/2 | v₂ | (0,1) | v₂(c),v₂(c−1) | corollary |

Every Type-I cryptid is the **q-adic depth process of an explicit affine ×(p/q) orbit**. The q=2 machines and o2
share Antihydra's exact (p,q), differing only by the additive offset (the correction). **The sole exception is Space
Needle**, whose odd branch has no single fixed point (a v-indexed carry) — correspondingly the one non-(K)-seeded,
cumulative, ×5/2 machine.

## 4. The two secondary axes and the criticality boundary `[PROVEN ingredients; Lean criticality]`

- **Criticality** (cumulative-ledger machines): single-run fatality is excluded iff the integer condition
  `p+1 ≤ q^(β+1)` holds (β = budget slope) — the run-cap slope `log_q(p/q)` being below the budget slope. **o4**:
  `5 ≤ 3⁴` (excluded, `[PROVEN, Lean: o4_criticality_excluded]`). **Antihydra/o2**: β = ½ non-integer, ratio
  `log₂(3/2)/½ = 1.1699 > 1` — **the critical boundary the lemma cannot instantiate** (documented in Lean). The five
  sea machines (o11/o13/o14/o16, o15/o18) drain their budget deterministically, residue-decoupled, so the ratio is
  inapplicable in-epoch; their fatality is a per-epoch residue draw at doubly-exponentially sparse refills.
- **Ledger-memory:** *cumulative* (Antihydra, o2, o4, o3, Space Needle — the balance never re-seeds; non-halt-leaning
  when subcritical) vs *resetting* (o11/o13/o14/o16, o15/o18 — each refill re-seeds; a.s.-halt-leaning in the annealed
  model). The annealed halt/non-halt lean splits **exactly** along this axis, frontier-wide.

## 5. The open core, and why it is (K) in every coordinate `[OBSERVED, direct measurement]`

The uniform theorem controls the **depth** axis unconditionally. Every protection is the **frequency** axis: an
effective quenched bound on the frequency of deep q-adic returns (`v_q(v−x) ≥ ℓ`) of an explicit ×(p/q) orbit
(o4: multi-run conspiracy of returns G≡−14 mod 3^L; Antihydra: even-density ≥ 1/3 = the AEV Normality Conjecture,
arXiv:2510.11723). The run-depth sequence — by the theorem, the moving-diagonal q-adic digit of the orbit — is
measured **white** (autocorrelation ≤ 0.008) and **conditionally structureless** (`H(dₙ | last 3) = H(dₙ)` to 0.13%):
not finite-order Markov, no substitutive/automatic structure. Possessing any exploitable structure below the
first-moment tautology is equivalent to a sofic coding of a non-Pisot ×(p/q) expansion — exactly the banked-absent
ingredient (`FREQUENCY_AXIS_PROBE_2026-07-08.md`, `NEW_MATH_PROGRAM.md`). The margin ladder (Antihydra/o2 critical at
1.17; o4 freely subcritical at 0.087; the sea machines' sparse resetting draws; Space Needle's cumulative summable
lean) orders the *strength* of the ask; it opens no coordinate where the ask is easier than (K).

## 5b. Frontier completeness `[OBSERVED, census re-audit 2026-07-09]`

Of the **17 named open BB(6) cryptids** (Antihydra, Space Needle, o2–o5, o7, o8, o10–o18; Lucy's Moonlight halts and
is not a holdout), **16 are Type-I** — q-adic fixed-point depth processes of ×(p/q) branch maps — namely the 11 tabled
in §3 plus **o5 (×4/3), o8 (×3/2 nested), o12 (×3/2 sea)** (analyzed in the catalogue/sea notes, the same fixed-point
structure; o8's ×3/2 reset orbit reconfirmed). **The sole genuine outlier is o7:** its two branches carry DIFFERENT
multipliers (even ×3/2, fixed point −4, run v₂(a+4); odd a pure halving ×1/2, fixed point −3, run v₂(a+3)), so the
fixed-point trick applies per-branch but there is no single scalar ×(p/q) orbit whose q-adic digit is o7's run-depth
— o7 is **not (K)-seeded**; its protection is a **thin-set B2 reachability** wall (halt ⟺ a+3 = 2^k, fatal set of
relative measure 2^{−bitlen}→0), not a B1 frequency/(K) statement (correcting the 2026-07-05 2D map's "o7 = B1
density"). **Completeness verdict:** the strict claim "every cryptid is one ×(p/q) odometer" is FALSE (o7); the
correct claim — **every named open cryptid is a q-adic fixed-point depth process of ×(p/q) branch maps** — holds for
all 17, o7 included, with o7 the one two-multiplier B2 exception. Scope caveat: this is the *named* frontier; the
~1090 un-catalogued 6-state holdouts remain `[OPEN]`. (`O7_AND_CENSUS_COMPLETENESS_2026-07-09.md`.)

## 6. What is decided, and what is not

**Decided in Lean, machine-checked:** the uniform run-structure theorem and its census corollaries; the criticality
comparison and o4's subcritical exclusion; o4's full generation map (odometer + ledger derivation); o3's body and
generation map; o18's machine and sweeps. **Grid-certified (red-teamed, not yet Lean):** the o15/o18/o17 templates,
o2's Link 0, the sea machines' rule systems. **OPEN:** every machine's protection — one quenched q-adic
return-frequency statement per orbit, each equivalent to base-p/q normality of a specific seed; the whole family is
one problem in |family| coordinates. **No cryptid is decided.**

## References to the record
Anatomy/classification: `BB6_CRYPTID_SPECIES_2026-07-07.md`. Uniform theorem: `PAPER_MIRROR_LADDER.md`, `mirror_census.py`,
`lean/Mirror.lean`. Per-machine: `O4_*`, `O3_TEMPLATE_PORT`, `O15_*`, `O17_*`, `O18_*`, `X32_*` (o2/o7/o10),
`O11_REFILL_LAW`, `O13_O14_FIXEDPOINT`, `O16_SPACENEEDLE_FIXEDPOINT`, `ANTIHYDRA_LEDGER_UNIFICATION`. Frequency axis:
`FREQUENCY_AXIS_PROBE_2026-07-08.md`, `O4_COBOUNDARY_LP_2026-07-08.md`. Lean: `lean/{RunStructure,Template,Suffix,
Mirror,O3,O18}.lean`, `LEAN_STATUS_2026-07-07.md`. Kernel anchor: Andrieu–Eliahou–Vivion, arXiv:2510.11723
(`BB6_FRAMEWORK_PACKAGE.md`). Verification: `verify_all.py` (12 items, all PASS).
