# Counter-automaton verifier for o4 — build turn 2: a VALIDATED sound period-p accelerator (2026-07-05)

*Turn 2 of the sound verifier build. Delivers a **validated, sound acceleration engine** that jumps o4's period-2
bouncer sweeps. It is proven correct by **exact step-for-step comparison to the concrete TM — matching state, step
count, head position, AND the full tape** over 2·10⁶ steps. This is the trustworthy engine the symbolic closure proof
(turn 3) will run on. SOUNDNESS: the accelerator is `[VALIDATED]`; o4 `[OPEN]` — **not decided** (the symbolic
one-generation closure is not yet done). No machine decided.*

## The accelerator `[VALIDATED, o4_accel_sound.py]`
Sound period-`p` acceleration (`p≤4`): at the head, simulate `p` micro-steps on a snapshot; **if** the head returns to
the **same state**, advanced by `δ≠0`, having **written every crossed cell back unchanged**, **then** it is a uniform
sweep — jump forward by as many whole cycles as the pattern ahead matches (each jumped cycle is *proven* identical to
executing it, since the cells are restored and the look-ahead pattern is verified). **Correctness is validated by exact
comparison to the concrete simulator:**
| `N` steps | concrete `(state, steps, pos)` | accelerator | full-tape match | jumps | steps jumped |
|---|---|---|---|---|---|
| 5·10³ | `(E,5000,−80)` | identical | ✓ | 78 | 1876 |
| 5·10⁴ | `(D,50000,−240)` | identical | ✓ | 293 | 22778 |
| 3·10⁵ | `(E,300000,−726)` | identical | ✓ | 749 | 144334 |
| 2·10⁶ | `(D,2000000,−1914)` | identical | ✓ | 1933 | 985442 |
**Every field matches, including the entire tape** — the accelerator is sound. It jumps `≈49%` of steps (the period-2
`B1F0`/`D1E0` sweeps), exactly the `O(G)` bouncer traversals that the counter-automaton proof must handle symbolically.

## Where this sits in the proof `[plan]`
- **Turn 1** (done): architecture (bouncer over base-4/3 counter) + halt-freeness reduced to a structural fact (`B`
  never faces `11`).
- **Turn 2** (done, here): a **validated sound accelerator** that jumps the `O(G)` sweeps.
- **Turn 3** (next): run one generation with the accelerator for `G` and `G+3` (same residue), record the **jump trace**
  (sequence of `(cycle, count)` jumps + concrete boundary steps); if the traces are **identical except jump-counts
  affine in `G`**, the generation is **uniform per residue class** ⟹ with the odometer `G'=⌊4G/3⌋+c` and turn-1's
  halt-freeness, **o4 is decided**. Until turn 3 closes, o4 is **not decided**.

## Verdict
**(b) — turn 2: a validated sound accelerator delivered.** It matches the concrete TM exactly (state/steps/pos/tape,
2·10⁶ steps) and jumps the `O(G)` bouncer sweeps — the engine for the symbolic closure. **o4 is not decided** (turn 3,
the uniform-per-residue jump-trace closure, remains). **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `o4_accel_sound.py`: period-`p` sound accelerator, `VALIDATED SOUND + accelerates` (exact match incl. tape to 2·10⁶).
  Basis: `O4_VERIFIER_BUILD_T1_2026-07-05` (bouncer/halt-free), `bouncer_prove_sound.py` (sound-sweep template).
