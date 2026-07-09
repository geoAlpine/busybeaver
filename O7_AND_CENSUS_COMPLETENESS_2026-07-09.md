# o7's full treatment + the BB(6) cryptid-census completeness check (2026-07-09)

*Two tasks. (A) The complete reduction chain for o7 — the machine the 2026-07-05 2D map misclassified as
"B1 density, ×3/2" and the 2026-07-08 cleanup began to correct: o7 is a thin-set B2 machine whose two
branches carry two different multipliers. (B) A completeness scan: enumerate the full BB(6) named-cryptid
holdout set, tag each by coverage, and state honestly whether the Type-I census is complete. Model: the
Antihydra/o2 5-link chain (`BB6_FRAMEWORK_PACKAGE.md`, `X32_CLEANUP_2026-07-08.md`). SOUNDNESS: every claim
labeled `[PROVEN given the automaton]` / `[OBSERVED]` / `[OPEN]`; exact big-int
(`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`); scripts `o7c_o7_chain.py`, `o7c_census_probe.py`.
No machine decided.*

## 0. Headline

| item | result |
|---|---|
| **o7 chain** | 5 links, Antihydra-parallel but B2. Gate `[PROVEN from table]`, milestone automaton `[OBSERVED 0-mismatch]`, halt ⟺ `a+3 = 2^k` ⟺ `oddpart(a+3)=1` `[PROVEN given automaton]`, thin-set protection `[OPEN]`. |
| **o7 is NOT (K)-seeded / NOT Type-I** | its two branches carry **two different multipliers** — even branch `×3/2` (fixed pt −4, run `v₂(a+4)`), odd branch a **pure halving `×1/2`** (fixed pt −3 on `u=a+3`, run `v₂(a+3)`). A Type-I cryptid has ONE `p/q` on both branches. `[PROVEN given automaton, 0 violations to 2·10⁵]` |
| **fixed-point trick** | applies to **each branch separately** (both fixed points integral, both run laws exact) but there is **no single value orbit** whose q-adic depth process it drives — the mechanism fragments. |
| **census** | 17 named open cryptids. **16 are Type-I ×p/q depth processes** (13 in `PAPER_CENSUS.md` + o5/o8/o12 analyzed in the catalogue/Mahler-sea notes). **o7 is the sole genuine non-Type-I.** Lucy's Moonlight = HALTS (a decided false-proof gate test, not a holdout). |
| **completeness verdict** | **NOT complete in the strict "every cryptid is a single ×p/q odometer" sense — o7 is one documented outlier.** It IS complete in the weaker sense that every open cryptid is a **q-adic (fixed-point-trick) depth process of ×p/q branch maps**; o7 simply mixes two multipliers and carries a B2 thin-set wall rather than a B1 frequency wall. |

---

## 1. TASK A — o7's complete chain

`o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC` (halt `F,0`; unique edge into F: `C,0→1LF`).

### Link 0 — machine ⟺ milestone automaton `[OBSERVED, 0-mismatch]`
Milestone: state **D** at the left frontier reading the `0` left of the first block; tape `0 1^a 0 1^b`
(the Antihydra two-counter shape). Automaton (`x32_o7_reduction.py`, banked 29 raw + 124 seeded, 0-mismatch;
re-checked here 30 blank milestones to 2·10⁷ steps, 0 mismatches):
```
a=1                 -> HALT
a=3                 -> (b+5, 1+[b odd])          (special exit)
a even >= 2         -> (3a/2 + 1 + b, 1)          EVEN branch: pumps b into a, resets ledger to 1
a odd  >= 5         -> ((a-3)/2, b + (a+5)/2)      ODD branch: drains a into b
```

### Link 1 — the two fixed points and the two run laws `[PROVEN given automaton; 0 violations to 2·10⁵]`
- **EVEN chains** (`b` re-seeds to 1, so `a` is autonomous): `a ↦ 3a/2 + 2`, i.e. on `x = a+4`, `x ↦ 3x/2`.
  **Multiplier 3/2, fixed point x=0 (a=−4), chain length `v₂(a+4)`** — the family fixed-point law, ratio 3/2.
- **ODD cascades:** `a ↦ (a−3)/2`, i.e. on `u = a+3`, `u ↦ u/2` exactly. **Multiplier 1/2, fixed point u=0
  (a=−3), cascade length `v₂(a+3)`** (truncated only when `oddpart(a+3) ∈ {1,3}` hits the `a=1`/`a=3` special
  branches — verified: exactly the 30 such seeds in `[5,2·10⁵)`, no automaton violation).

### Link 2 — HALT ⟺ `a+3 = 2^k` (the gate, exactly) `[PROVEN given automaton]`
Inside a cascade `u=a+3` halves each step; it ends at `a_exit = oddpart(a+3) − 3`, or reaches `a=1` (HALT)
iff `u` was a pure power of two. Hence:
> **o7 HALTS ⟺ some milestone has `a+3 = 2^k` (k≥2) ⟺ `oddpart(a+3) = 1`.**
`b` is **never tested by any branch** — it has no ledger role in the halt (contrast Antihydra/o2, where the
balance counter `b`'s return to 0 IS the halt). Re-confirmed on the seeded raw-TM grid.

### Link 3 — the protection (thin-set) `[OPEN]`
The fatal set `{u = 2^k}` is **one point per dyadic scale** — relative measure `2^{−bitlen(u)} → 0`, a
measure-zero target in the 2-adic limit. Non-halt ⟺ the orbit never lands on it. Margins (500k milestones,
`o7c_o7_chain.py`): value grows ~0.20 bits/milestone; `v₂(a+3)` at entries is geometric (`0.50/0.25/0.13`,
max depth 22 at 10⁶); **`min oddpart(a+3) = 7`, at n=2, never smaller** — the odd part is regenerated at every
cascade entry and its bit-length tracks `bitlen(u) − O(log n)`, so it never approaches 1. Annealed
Borel–Cantelli `Σ 2^{−0.2n} < ∞` — the annealed model survives outright (contrast Antihydra's delicate `η^B`).

### The (K)-seeded question, answered precisely
o7 is **×3/2-flavored but genuinely different.** The clean Type-I test (`PAPER_MIRROR_LADDER.md` §1) requires
each branch to be `b(v)=(pv+e)/q` with the **same** `(p,q)`; Antihydra's are `3v/2` and `(3v−1)/2`, both `×3/2`.
o7's are `3x/2` (even) and `(x+1)/2` (odd) — the odd branch is a **pure halving `×1/2`**, a *different*
multiplier. So:
- The **fixed-point trick applies to each branch** (both fixed points integral: −4 even, −3 odd; both run laws
  exact `v₂(a+4)`, `v₂(a+3)`) — this is why o7 *looks* like a ×3/2 machine locally.
- But it **breaks at the "single value orbit" requirement:** there is no scalar `v` iterating one `×(p/q)`
  whose q-adic depth sequence is o7's run-depths. The value alternates `×3/2` (even chains, expanding) and
  `×1/2` (odd cascades, contracting), coupled through `b`. Consequently the protection is **not** a frequency
  of deep returns (B1/(K)) but **thin-set reachability** (B2): `oddpart=1` AND full-depth return *simultaneously*
  — one geometric-tail event, not an accumulated density.

**Species / class.** GATE saturates small and safe. STRUCTURE: coupled two-counter, two multipliers, no single
odometer. PROTECTION: **thin-set hitting (B2 reachability)**, margin = odd-part growth rate (~0.20 bits/gen),
LEDGER-MEMORY: **none** (`b` untested) — the implicit 2-adic-tail object is **reset per entry**, kin to o15's
cylinder species, not Antihydra/o2's cumulative balance. The criticality ratio (run-cap/budget) is
**inapplicable**: there is no scalar budget to exhaust. o7 is not on the Antihydra ladder; its wall is
generalized-Collatz `2^k`-reachability. Fatal probes: `oddpart(a+3)` never dropped below 7 in 10⁶ milestones;
the `a=3` branch (`oddpart=3`) had 0 hits — no cheap fatal seed exists on the blank orbit.

---

## 2. TASK B — census completeness

### The full BB(6) named-cryptid holdout set (`suite.py` CRYPTIDS, minus champion + Lucy)
**17 open cryptids:** Antihydra, Space Needle, o2, o3, o4, o5, o7, o8, o10, o11, o12, o13, o14, o15, o16, o17,
o18. (`BB6 champion` = known halter; **Lucy's Moonlight = HALTS** — a decided machine used as a false-proof
gate in `suite.py`, `SOUNDNESS_INCIDENT.md`; NOT an open holdout.)

### Coverage table

| machine | ×p/q | wall | Type-I? | where analyzed |
|---|---|---|---|---|
| Antihydra, o10 | ×3/2 | B1 density | yes | PAPER_CENSUS |
| o2 (ceiling) | ×3/2 | B1 density | yes | PAPER_CENSUS / X32_CLEANUP |
| o11, o13, o14, o16 | ×3/2 sea | B2 (residue draw) | yes | PAPER_CENSUS / MAHLER_SEA |
| **o8** | ×3/2 nested | B2 reachability | yes | CATALOGUE_O7_O12 (`[VERIFIED]`); **re-confirmed here** |
| **o12** | ×3/2 sea | B2 (residue draw) | yes | MAHLER_SEA_CLASSIFICATION (`[VERIFIED]`) |
| o4 | ×4/3 | B2 reachability | yes | PAPER_CENSUS (Lean end-to-end) |
| o3 | ×4/3 (odometer) | B2 reachability | yes | PAPER_CENSUS |
| **o5** | ×4/3 | B2 reachability | yes | CATALOGUE_O2_O5 (`[VERIFIED]`) |
| o15, o18 | ×8/3 | B2 (string/tower) | yes | PAPER_CENSUS |
| Space Needle | ×5/2 | B2 (cumulative) | yes (odd branch has no fixed pt) | PAPER_CENSUS |
| o17 | — (no fixed pt) | B1-leaning parity | yes (kernel-less odometer) | PAPER_CENSUS |
| **o7** | **×3/2 even / ×1/2 odd** | **B2 thin-set** | **NO — two multipliers** | this note + X32_CLEANUP |

**o5/o8/o12 are Type-I but were simply never added to the `PAPER_CENSUS.md` table** (o5 = o4's ×4/3 Erdős
twin; o8 = ×3/2 nested Antihydra twin; o12 = o13's ×3/2-sea twin, `a-start ⌊3a/2⌋+c, c=3δ−1`). Independent
re-confirmation this run (`o7c_census_probe.py`): o8's state-A clean-reset orbit reproduces the banked values
`…160,241,273,309,331,415,520,781,809,912…` with inner ratios `1.500/1.501/1.502 → 3/2` exactly. (The generic
max-run auto-probe reproduces the documented **wrong event** — the √t envelope — for all four, honestly logged;
o5/o12's clean multipliers rest on the banked hand-milestone `[VERIFIED]` extractions, not re-derived here.)

### Completeness verdict
- **Strict form ("every BB(6) cryptid is a single ×p/q value odometer"): FALSE — o7 is a documented outlier.**
  Its even branch is ×3/2 and its odd branch is a pure ×1/2 halving; no single multiplier governs it, and its
  wall is thin-set `2^k`-reachability, not a frequency/density statement.
- **Weaker form ("every open BB(6) cryptid is a q-adic fixed-point-trick depth process of ×p/q branch maps"):
  holds for all 17** — including o7, whose *branches* obey the fixed-point run law (just with two different
  multipliers). Every protection is an orbit-specific quenched statement (B1 density for the ×3/2 balance
  machines; B2 reachability/thin-set for the rest); none is finitely decided.
- **Caveat (unchanged):** this is the **named** frontier. The 1104-holdout mass (`BB6_FRONTIER_CENSUS`) is only
  structurally surveyed (`[OBSERVED]` growth/block proxies); the trichotomy's extension to the ~1090 un-analyzed
  machines is `[OPEN]`. The named census is a lower bound on the family's variety — and o7 shows that variety
  already includes a two-multiplier B2 outlier that the earlier 2D map had mislabeled.

---

## 3. Soundness ledger
- o7: gate `[PROVEN from table]`; milestone automaton `[OBSERVED, 0-mismatch]` (30 blank + banked 29 raw + 124
  seeded); branch multipliers, run laws, cascade `u→u/2`, halt criterion `[PROVEN given automaton]`, 0 violations
  (2·10⁵ exhaustive + 2·10⁷ raw). The two-multiplier break is the one genuinely new structural claim; it is
  exact, not statistical. Thin-set protection `[OPEN]`; depth/odd-part margins `[OBSERVED]`; Borel–Cantelli
  heuristic.
- Census: coverage tags cite the banked notes; o8's ×3/2 reset independently reproduced this run; o5/o12 rest on
  banked `[VERIFIED]`; the generic auto-probe's noisy ratios are flagged as the wrong-event artifact and carry
  no weight. Lucy's Moonlight's HALTS status per `SOUNDNESS_INCIDENT.md` / `BB6.md`.
- Nothing strengthens any non-halting claim. o7's chain terminates in the `[OPEN]` thin-set wall; the completeness
  verdict decides nothing. Nothing committed.

## Reproduce (`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
- `o7c_o7_chain.py [raw=2·10⁷] [n=5·10⁵]` — branch multipliers (the Type-I break), halt criterion on the blank
  raw orbit, thin-set margins.
- `o7c_census_probe.py [cap=8·10⁶]` — generic auto-probe (wrong-event demo) + o8's proper state-A clean-reset
  orbit (independent ×3/2 re-confirmation).

**Halting stays `[OPEN]` for o7 and every cryptid. No machine decided. No label upgraded.**
