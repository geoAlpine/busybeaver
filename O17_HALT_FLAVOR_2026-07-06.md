# o17 halt-flavor pinned — the o4 template+ledger lens applied: gate YES, template NO, δ-map NO; verdict (iii) "sparse-gate carry-timing" (2026-07-06)

*Task: decide whether o17 (`1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`, halt = F reads 0) is (i) o4-style
template+ledger, (ii) Antihydra-style B1 density, or (iii) genuinely different — re-testing the old "B1-leaning
(marker-parity density)" reading and the B2_DECISION_FORK correction against the new o4 decomposition
(`O4_TEMPLATE_CLOSURE`/`O4_LEDGER_ANALYSIS`: rigid template + finite-residue ledger `a′=a+δ(ρ)` with drift).
SOUNDNESS: every claim labeled `[PROVEN]`/`[OBSERVED]`/`[OPEN]`; nothing about halting decided. Interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`; scripts `o17_halt_reduction_2026-07-06.py`,
`o17_generation_template_2026-07-06.py`, `o17_ledger_flavor_2026-07-06.py`. Not committed.*

---

## 1. Halt-relevant reduction — the local gate, proven and censused

**(a) `[PROVEN from table]`** F is entered ONLY by `(D,0)→0LF`; D is entered ONLY by `(A,1)→1LD`. Chasing the
two forced steps: **o17 halts ⟺ the configuration `0 0 [1]_A` occurs** (state A reads a 1 whose two left
neighbors are both 0). Local safety condition, the exact formal analogue of o4's "B never on left-1 of `11`":
> **A never reads a 1 with `0 0` immediately to its left.**

**(b) `[OBSERVED, 2·10⁷-step blank run]`** (`o17_halt_reduction_2026-07-06.py`): 3,741,622 D-entries; **4,712
F-entries (near misses), every one safe** (`1 0 [1]_A` — F reads 1). The radius-5 window set at F-entries
**saturates at 11 windows by step 706** and all have the same reading: the head sits at the left end of a
1-block with a **single-0 separator** and the previous block's 1 beyond it. So interior safety = the
single-0-separator language invariant (the milestone normal form of `O17_CORE_TRANSDUCER` §1, seen live);
the only place the invariant cannot protect is the **left frontier** (infinite 0-run) — which is exactly the
proven marker-parity gate (`O17_CORE_TRANSDUCER` §7(I): frontier arrival in D ⟺ leading block even ⟺ halt).
**Zero frontier F-entries in 2·10⁷ steps** (and none to 3·10⁸, §3c).

**(c) `[PROVEN, 5-step concrete trace]` — new identification:** after 5 steps the blank orbit is exactly
`0 [A]0 1 1 1 0` = the core-family seed `A 0 1^3`. **o17's blank-tape halting problem IS the k=3 (j=1) member
of its own Collatz-irregular family `0 A 0 1^{3j}`** — the family is not just an embedded probe set; the real
orbit is its first hard member. (Blank gate steps = j=1 gate steps + 5, cross-checked to 3·10⁸.)

## 2. Structure — the o4 template premise FAILS `[OBSERVED]`

Generation := one odometer tick (right-end `(E,0)` reversal). Per-generation event streams, sweep-collapsed and
hashed exactly as in the o4 template discovery (`o17_generation_template_2026-07-06.py`):
- o4: **O(1) shape classes** (1 prefix + 1 body + 3 suffixes), only counters vary.
- o17 blank orbit: **69 distinct shapes in 1,006 generations, 91 in 1,635 — new shapes appear indefinitely**
  (last new one at generation 1,556); shape token-length ranges 15 → 3,620 (grows with carry depth); core seeds
  L=9, L=15 identical picture (67/765, 54/462).
- **Second-level compression collapses NOTHING** (69→69, 91→91): the deep-carry excursions are not repetitions
  of any fixed block — there is no `prefix·body^r·suffix`, and no template-of-templates with a counter vector.

This is the structural content of the √step growth: o4's linear bouncer has an O(1)-dimensional generation
state (G, a); o17's generation state is the **whole growing digit string** (`O17_CORE_TRANSDUCER` §3: the
string LENGTH is irreducible). A 1-counter (or any fixed-arity) rigid template is **incompatible** with it.

## 3. The flavor call — testing the "parity bit = ledger?" reading

**(a) The bit is NOT a density.** The old "B1-leaning (bit density = (K))" reading is wrong in the density
sense: the marker bit is emitted by a **deterministic 3-state automaton** `{3→{3,5}, 5→{3,8=HALT}}` with a
`[PROVEN]` 1-bit gate read (prior notes) — no equidistribution statement anywhere. This confirms the
`B2_DECISION_FORK` correction (o17 ∈ carry-timing, not B1).

**(b) But it is NOT an o4 ledger either — no finite-residue δ-map `[OBSERVED, fresh and broader than §7.2]`.**
Pooling all 18 marker-5 branch events (5→3 vs 5→8) across 22 seeds (`o17_ledger_flavor_2026-07-06.py`):
27 single features (`n mod k` k≤12, `m mod k`, `S mod k` k≤6, `d1,d2`, last digit, seed j) plus all small
residue pairs — **every genuine finite residue leaves the branch ambiguous**. The two flagged "deciders" are
vacuous: digit-sum `S` takes 18 distinct values on 18 samples, and the last digit `dl ≈ n − c` is the
free-running counter (unbounded, seed-specific — a full state coordinate, not a residue). Same for the 3→{3,5}
branch (31 events: nothing decides). o4's `δ(G mod 3)` has **no analogue**: the branch driver is the entire
carry cascade.

**(c) And there is no drift margin — the margin lives in TIMING, not in a ledger value `[OBSERVED]`.**
o4's safety quantity `a` drifts +3/generation away from the fatal threshold (ruin η^a). o17's "ledger state"
is the 3-state marker automaton: distance-to-fatal is **permanently ≤ 1** whenever a gate fires (5 is one step
from 8) — there is no quantity to run a ruin analysis on. What actually protects the orbit is that gates
(true-frontier returns) **thin out super-exponentially**: blank orbit gates at steps 5, 22, 44, 101, 314, 724,
2,005, 1,072,566 — then **none up to 3·10⁸**; runners j=3, j=6: last gate at 15,484 / 20,189, none to 6·10⁷.
Gate thinning is irregular even in tick time (j=1: n = 0,1,5,11,21,533,…) — the carry-to-top events are the
**moving target** of the fork's carry-timing definition, quantified. Whether any given orbit sees infinitely
many gates is itself `[OPEN]` and entangled with the core (it is the carry-history question).
Exposure record: the blank orbit has faced the fatal-adjacent state (marker 5 at a gate) exactly **twice ever**
(steps 44 and 724), surviving both; pooled family stats 5→8 : 5→3 = 11 : 7 (halter-enriched sample, not a rate).

## 4. Verdict — (iii), genuinely different: **sparse-gate carry-timing**

| o4 decomposition piece | o17 |
|---|---|
| local safety condition (seam window) | **YES `[PROVEN]`** — `0 0 [1]_A`, near-miss windows saturate (11) |
| deterministic 1-bit gate read (not a density) | **YES `[PROVEN, prior]`** — marker parity, 3-state automaton |
| rigid template prefix·body^r·suffix | **NO `[OBSERVED]`** — unbounded shape classes, level-2 collapse fails |
| finite-residue δ-map / ledger `a′=a+δ(ρ)` | **NO `[OBSERVED]`** — all residues ambiguous; drivers are unbounded coordinates |
| drift margin / ruin constant | **NONE** — distance-to-fatal ≤1 at every gate; protection = gate sparsity `[OPEN]` |

o17 has the **gate half** of the o4 decomposition but neither the template half nor a δ-map, and no drift.
So: **the B2 "arithmetic" wall does NOT uniformly bottom out in a (K)-shaped ledger — o17 is the in-family
counterexample.** Its non-halt statement has the form: *"the sparse, irregularly-timed sequence of carry-to-top
events never delivers an increment at marker 5"* — a carry-timing/moving-target condition (Fork B2 of
`B2_DECISION_FORK`, vindicated against both the old B1/density reading and the new template+ledger category).
Within the frontier taxonomy o17 now sits alone: deterministic gate like o4, no ledger like o4, no density like
Antihydra — the hardness is **when** the odometer's carry reaches the top, and that timing is the full
unbounded string state. If a fourth category name is wanted: **template-free carry-timing with a proven 1-bit
gate**.

## 5. Honest scope
- Nothing new decided; the k≡0 (mod 3) family halting pattern stays Collatz-irregular `[OPEN]`; runners' caps
  (6·10⁷ here) prove nothing (k=102/108 halted past 10⁷ before).
- All template/ledger negatives are `[OBSERVED]` over the stated ranges (1,635 generations; 18+31 branch
  events, 22 seeds); the gate reduction (§1a) and the blank≡j=1 identification (§1c) are `[PROVEN]` finite checks.
- The one prior-note tension resolved: "marker-parity density = (K)" (2D classification) was already corrected
  to carry-timing by `B2_DECISION_FORK`; this note re-derives that correction through the template lens and
  strengthens it (the bit is deterministic-automaton-valued, so no density statement even exists to be (K)-hard).

## Reproduce
- `o17_halt_reduction_2026-07-06.py` — table chase (F/D unique predecessors), 2·10⁷ blank census: 4,712 safe
  F-entries, 11-window saturation curve, window dump.
- `o17_generation_template_2026-07-06.py` — per-tick event-stream compression + shape/level-2 hashing (blank,
  L=9, L=15); run with arg = step cap.
- `o17_ledger_flavor_2026-07-06.py` — 22-seed milestone/marker itineraries, branch-determinism search
  (singles + pairs), 5-visit recurrence, 3·10⁸-step blank frontier-gate census (9 gates, 0 in state D).
- Blank≡j=1: 5-step trace inline (§1c); gate-step offset +5 cross-check in the two gate censuses.

**No machine decided. No label upgraded.**
