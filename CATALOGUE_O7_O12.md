# Frontier catalogue — cryptids o7, o8, o11, o12 (slow-width cluster)

*Per-machine reverse-engineering against the raw TM (`bb_sim` / `cryptid_map`), 2026-06-28. Soundness
paramount; labels `[PROVEN]`/`[CONDITIONAL]`/`[OPEN]`/`[OBSERVED]`/`[VERIFIED]` enforced. **No machine is
decided; no non-halting asserted.** Numerics with `.venv/bin/python` (exact integers); every milestone orbit
is produced by faithful simulation from the blank tape (same parse + step semantics as `bb_sim.py`).*

## Exact specs (verbatim from `suite.py` CRYPTIDS) and halt transitions

| id | spec | halt transition | entered via |
|---|---|---|---|
| o7 | `1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC` | **F reads 0** (`F: 0→---`) | `C: 0→1LF` |
| o8 | `1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE` | **F reads 0** (`F: 0→---`) | `E: 0→1LF` |
| o11 | `1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF` | **C reads 0** (`C: 0→---`) | `B: 0→1LC` |
| o12 | `1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB` | **F reads 0** (`F: 0→---`) | `E: 0→1RF` |

All four run `> 5·10⁷` steps with no halt (`bb_sim.run`, 50M; o11 left 8511 ones, o12 7013, o7 4350, o8 5211).

---

## §0. LOTTERY CHECK (highest-stakes) — all four HOLDOUT under the sound tools

Run with generous parameters; **default HOLDOUT, DECIDED only if the sound verifier confirms AND the cryptid
gate passes.** Neither happened for any machine.

| machine | `far_dfa.prove` (ms 2–6, N≤3000) | `far_finder.prove` (ks 2–6, N≤5000) | `far_cegar.prove` (rounds 120, N 2000) |
|---|---|---|---|
| o7 | HOLDOUT | HOLDOUT | HOLDOUT (not closed, \|negs\|=120) |
| o8 | HOLDOUT | HOLDOUT | HOLDOUT |
| o11 | HOLDOUT | HOLDOUT | HOLDOUT |
| o12 | HOLDOUT | HOLDOUT | HOLDOUT |

**Verdict [PROVEN, this run]: NONE of o7, o8, o11, o12 is decidable by our sound tools.** No sound certificate
exists in range; the soundness gate held (no false `NEVER_HALTS`). Consistent with `BB6_PREP` (our deciders
settle 0 real holdouts) and `CRYPTID_CENSUS` UPDATE 2026-06-23 (slow-width 15 all genuinely hard).

---

## §1. o7 — two unary counters, Mahler **μ = 3/2** (Antihydra family) — class (b)

**Genuine dynamics [VERIFIED vs raw TM].** Milestone = **left-extreme in state D**; the tape is exactly two
unary counters `0 1^a 0 1^b` (Antihydra shape). The cryptid_map auto-tag ("IRREGULAR") is the wrong event:
it reads the raw L-extreme width series `3,6,9,14,15,…` which mixes intra-sweep snapshots. The **real growth
event is the clean reset** `0 1^a 0 1` (b=1), where the right counter has been fully ground down.

Sweep mechanics: each D-milestone moves `b → b−1`, `a → a+1`; when `b` reaches 1 the epoch **resets**
(`a → 1`, `b →` large) — the balance/Hydra two-counter pattern.

**Clean-reset orbit `a` (b=1) [VERIFIED]:** `6, 11, 16, 26, 41, 49, 58, 89, 103, 131, 166, 251, 316, 476,
716, 1076` (major resets). Major-epoch sub-chain `316 → 476 → 716 → 1076` has ratios
**1.506, 1.504, 1.503 → 3/2** (widths `319,479,719,1079`).

- **Classification: (b) Collatz-kernel `T_μ`, μ = 2/3⁻¹ → 3/2, p = 2** — the **Antihydra / Mahler-3/2 family**
  (with Antihydra, o10-inner, o8). Width envelope `w/√t ≈ 0.70–0.84` (sawtooth), exponential reset content.
- **Halt criterion [structural, VERIFIED reachable form]:** halts ⟺ state F ever reads `0`. F is entered only
  by `C:0→1LF`; the read is a **head-local 2-adic carry/alignment event** of the `(3/2)ⁿ` two-counter orbit
  (the analogue of Antihydra's `v₂(c_n−1) ≥ balance_n+1`). The **exact 2-adic predicate is NOT separately
  derived** (matches `CRYPTID_REDUCTIONS.md` Tier-1: "reduced to family + multiplier," not exact criterion).
- **Status [OPEN], Mahler-3/2-hard.** In-family by multiplier; **not in-scope** for the §3 exact reductions of
  `BB6_STRUCTURAL_LIMIT_THEOREM.md` (only Antihydra/o18/o15/o10-inner have exact halt criteria). Not decidable
  by sound tools (§0).

---

## §2. o8 — two unary counters, Mahler **μ = 3/2, nested** (Antihydra family) — class (b)

**Genuine dynamics [VERIFIED vs raw TM].** Milestone = **left-extreme in state A**; tape = two unary counters
`0 1^a 0 1^b` (Antihydra shape). Same `b→b−1, a→a+1` sweep then reset. The real growth event is again the
clean reset `0 1^a 0 1`.

**Clean-reset orbit `a` (b=1) [VERIFIED]:** `2, 4, 7, 10, 16, 25, 30, 46, 70, 106, 160, 241, 273, 309, 331,
415, 520, 781, 809, 912`. The inner sub-chain `70 → 106 → 160 → 241` has ratios **1.514, 1.509, 1.506 → 3/2**;
but the orbit also has **larger meta-jumps** (e.g. `520 → 781 ≈ ×1.5` after a near-flat run `241→273→309→331`),
i.e. a **nested / meta-epoch** structure (like o10): an inner ×3/2 chain inside an outer meta-cycle.

- **Classification: (b) Collatz-kernel, μ = 3/2, p = 2 (nested)** — the **Antihydra / Mahler-3/2 family**.
  Width envelope `w/√t ≈ 0.65–0.82` (sawtooth).
- **Halt criterion [structural, VERIFIED reachable form]:** halts ⟺ state F reads `0` (F entered only by
  `E:0→1LF`); head-local 2-adic alignment of the nested `(3/2)ⁿ` orbit. Exact predicate not derived (nested
  outer meta-structure not fully modeled, as with o10).
- **Status [OPEN], Mahler-3/2-hard (nested).** In-family by multiplier; not in-scope for exact reductions. Not
  decidable by sound tools (§0).

---

## §3. o11 — leading counter over a `(10)*` sea, **irregular geometric collapse** — class (d)

**Genuine dynamics [VERIFIED vs raw TM].** Milestone = **right-extreme** (states cycle A,B,E,F). Tape =
`0 1^k 0 (10)^m` — a **leading unary counter `1^k`** over a `(10)*` background carrying a small `0²` defect.
The R-extreme states A/E/F sweep the `(10)*` sea, slowly transferring it into / out of the leading block.

The auto-extractor finds **~1518 near-linear milestones** = the wrong event (the per-sweep `(10)*` reshuffling).
The **genuine growth event is the clean collapse** `0 1^k 0` (the whole `(10)*` sea ground into one block).

**Clean-collapse orbit `k` [VERIFIED]:** `3, 9, 26, 303` at times `t = 10, 47, 272, 28101` (next collapse
beyond 60M steps). Ratios **3.0, 2.9, 11.65** — **irregular, no clean multiplier**; inter-collapse times
`×4.7, ×5.8, ×103` (super-quadratic). Width envelope `w/√t ≈ 2.0` (sawtooth/poly-time envelope).

- **Classification: (d) too irregular for a clean reduction** — single-leading-counter-over-`(10)*` (the `T2`
  template of `CRYPTID_REDUCTIONS.md`), **irregular geometric content** (collapse value grows geometrically in
  magnitude but with no clean `2^a/3^b` ratio across the 4 observed epochs). Distinct from the clean Mahler-3/2
  pair o7/o8.
- **Halt criterion [structural]:** halts ⟺ state C reads `0` (C entered only by `B:0→1LC`); a head-local
  defect/boundary-collision event. No clean scalar orbit map ⇒ no exact arithmetic predicate derivable here.
- **Status [OPEN].** Not decidable by sound tools (§0). Bouncer/FAR correctly hold out: the **envelope is
  regular (`~√t`) but the content is irregular geometric** — the signature flagged in `CRYPTID_CENSUS`.

---

## §4. o12 — two-block head over a `(10)*` sea, **irregular geometric collapse** — class (d)

**Genuine dynamics [VERIFIED vs raw TM].** Milestone = **left-extreme in state C** (≈1292 visits). Tape =
`0 1^a 0 1^b 0 (10)^m` — a **two-block head** `1^a 0 1^b` over a `(10)*` background. Within an epoch the head
shuttles content between the two blocks and the `(10)*` sea (`01^2 01^4 0…` → `01^8 01^4 0…` → … → `01^k`),
producing ~2348 near-linear milestones (the wrong, auto-detected event).

The **genuine growth event is the clean collapse** `0 1^k` (head fully condensed into a single block).

**Clean-collapse orbit `k` [VERIFIED]:** `4, 10, 28, 370` at times `t = 17, 95, 565, 58083` (next beyond 60M).
Ratios **2.5, 2.8, 13.2** — **irregular, no clean multiplier**; inter-collapse times `×5.6, ×5.9, ×103`.
Width envelope `w/√t ≈ 1.5–2.0` (sawtooth/poly-time envelope).

(Note the near-parallel with o11: collapse orbits `o11: 3,9,26,303` vs `o12: 4,10,28,370` — same
"≈triple a few times, then a ~13× jump" shape; both are single-/two-block heads grinding a `(10)*` sea, the
two `T2`-template costumes of the same irregular-geometric difficulty.)

- **Classification: (d) too irregular for a clean reduction** — two-block-head-over-`(10)*`, irregular geometric
  content. No clean `2^a/3^b` ratio over the observed epochs.
- **Halt criterion [structural]:** halts ⟺ state F reads `0` (F entered only by `E:0→1RF`); head-local
  defect/boundary event. No clean scalar map ⇒ no exact predicate derivable here.
- **Status [OPEN].** Not decidable by sound tools (§0). Regular envelope + irregular content ⇒ FAR/bouncer
  correctly hold out.

---

## §5. Catalogue placement (frontier columns)

| machine | facet | kernel `q` (μ, p) | growth event (genuine) | multiplier | barrier / over-approx | discriminator (halt) |
|---|---|---|---|---|---|---|
| **o7** | density-type | **q=2** (μ=3/2, p=2) | 2-counter reset `0 1^a 0 1` | **3/2** [VERIFIED] | none proven; REG `[OPEN]` | F reads 0 (head-local, 2-adic align) |
| **o8** | density-type | **q=2** (μ=3/2, p=2, nested) | 2-counter reset, nested meta-epoch | **3/2 inner** [VERIFIED] | none proven; REG `[OPEN]` | F reads 0 (head-local) |
| **o11** | — | none (irregular) | `(10)*`-sea collapse `0 1^k 0` | irregular (3,9,26,303) | none proven; REG `[OPEN]` | C reads 0 (defect/boundary) |
| **o12** | — | none (irregular) | `(10)*`-sea collapse `0 1^k` | irregular (4,10,28,370) | none proven; REG `[OPEN]` | F reads 0 (defect/boundary) |

**Convergence (consistent with `CRYPTID_REDUCTIONS.md` / `BB6_STRUCTURAL_LIMIT_THEOREM.md`):**
- **o7, o8 join the existing Mahler-3/2 / Antihydra family** (clean ×3/2 reset orbits) — no new family. They are
  *in-family by multiplier, not in-scope* (no exact halt criterion derived; the in-scope set is
  {Antihydra, o18, o15, o10-inner}).
- **o11, o12 are `T2` single-defect-over-`(10)*` machines with irregular geometric content** — the sawtooth
  (`~√t`) width envelope hiding an irregular geometric collapse orbit. No clean scalar map; class (d).
- **No machine is a different named problem; none is TAME/decidable.** The two costumes (clean-Mahler counter vs
  irregular-geometric defect) are the same deep difficulty per the Stage-1 conclusion.

## §6. Soundness statement
Every numeric orbit above is machine-checked with exact integers via faithful simulation from the blank tape
(identical parse/step semantics to `bb_sim.py`). The sound verifiers (`far_dfa`, `far_finder`, `far_cegar`)
returned HOLDOUT on all four with generous parameters; **no `DECIDED` is claimed, no non-halting asserted.**
The "×3/2" tags for o7/o8 are `[VERIFIED]` multiplier observations on the reset sub-chain, **not** exact halt
criteria. o11/o12 collapse orbits are `[VERIFIED]` but `[OPEN]` and irregular. The lottery did not hit:
**none of o7, o8, o11, o12 is decidable by the sound tools.**
