# B5 investigation — the Track B de-risking front (2026-07-16)

**Machine.** `B5 = 1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD`

**VERDICT: (b) BRAID-BOUND. B5 is no easier than x2/B1.**
The register doubling is REAL and its law is CONFIRMED (`9·2^k−1`, **8 doublings**),
but the per-doubling step cost is **Θ(4^k)** — the same quadratic braid that
blocks B1/x2. The `2^k mod M` gate does **not** exist. B5 does **not** de-risk
Track B.

> **This document was CORRECTED after commit `885f6de`.** The first version's
> "decisive probe" had a broken instrument (§0.2). **The braid-bound verdict is
> unaffected and has been independently reproduced by the coordinator.** Several
> sub-claims were bug artifacts and are **withdrawn** — see §0.2 for the exact
> ledger of what survived and what did not.

No machine decided. No label upgraded.

---

## 0.1 Transition table — verified against the string, cell for cell

| state | on 0 | on 1 |
|---|---|---|
| A | `1RB` | `0LB` |
| B | `1LC` | `1LB` |
| C | `1RD` | `1LA` |
| D | `0RE` | `0RE` |
| E | `0RA` | `1RF` |
| F | `---` **HALT** | `1RD` |

The predecessor's table in `x2b5_sim.py` is **correct**; I re-derived it from the
string independently before using it. `F` is reachable only from `E` reading a `1`
(`E:1->1RF`). Therefore:

> **HALT ⟺ ∃ a time when `E` reads a `1` at cell `p` and cell `p+1 = 0`.**
> Equivalently: **`E` must never read the LAST `1` of a run of `1`s.**

This is the exact and only halt trigger. It is a **local tape condition**, not an
arithmetic condition on a register — see §4.

## 0.2 CORRECTION LEDGER — the broken instrument

**The bug.** In the first version of `x2b5_braid.py` (and `_sawtooth`, `_invariant`,
`_rle`, `_sweep`) the milestone loop updated `lo` but **never updated `hi`**, which
stayed at its initial `0`. Every tape scan therefore ran over `range(lo, 0+1)` — the
**LEFT half-tape only**. B5's tape is **mirror-symmetric about the origin** (§6), so
these probes silently measured a half-tape quantity that looked entirely plausible.
The "decisive probe" had a broken instrument. **This is exactly the failure mode
this program guards against, and it was caught by the coordinator's independent
re-derivation, not by me.**

Fixed by deriving the scan extent from the cells dict itself
(`extent()` / `maxrun_full()` in `x2b5_sim.py`), so no caller bookkeeping can
truncate. `x2b5_reg.py` / `x2b5_records.py` updated both bounds and were never
affected; `x2b5_halt.py` performs no extent scan and was never affected.

| claim | status |
|---|---|
| `peak_k = 9·2^k − 1` (17…2303) | ✅ **SURVIVES** — exact, k=1..8, unchanged by the fix |
| **Θ(4^k) braid; B5 braid-bound** | ✅ **SURVIVES** — step column *byte-identical* before/after; independently reproduced |
| no `2^k mod M` gate | ✅ **SURVIVES** — rests on the halt trigger (§4), which never used the broken scan |
| (H) halt gate never fires | ✅ **SURVIVES** — `x2b5_halt.py` does no extent scan |
| (I1) all gaps `== 1` | ✅ **SURVIVES** — re-verified on the FULL tape, 0 violations |
| `floor_k = 3·2^k + 2` (8,14,26,…) | ❌ **ARTIFACT — WITHDRAWN.** True floors: 16,28,46,88,166,328,646,1288 |
| `depth_k = 3(2^(k+1) − 1)` | ❌ **ARTIFACT — WITHDRAWN.** True depths: 1,7,25,55,121,247,505,1015 |
| "reset 14 = the k=2 tooth recurring verbatim" | ❌ **WITHDRAWN — mechanism lost.** True `floor_2 = 28`, not 14. See §3.2 |
| (I2) every run `≡ 2 (mod 3)` bar 2 boundary runs | ❌ **ARTIFACT — WITHDRAWN.** 171/441 milestones violate it on the full tape |
| §6 congruence route "could bypass the braid" | ❌ **DOWNGRADED** — its load-bearing premise (I2) is gone |

Why the step column was immune: milestone detection keys on `lo` and `state == 'C'`
only. `hi` never enters it. The bug corrupted the *register values* read at each
milestone, not *when* milestones fire — so the peaks (a max, dominated by the
symmetric half) and the timings both survived, while the floors (a min, sensitive to
the discarded half) did not. **That is luck, not method.**

## 1. Global growth: linear space, quadratic time

From the blank tape (`x2b5_records.py`, exact, O(1)/step — **unaffected by the bug**):

* Left and right excursion records are **symmetric**: 1086 each at 2·10⁶ steps, positions ±1086.
* The tape extends **+3 cells per side per macro-sweep**; sweep cost grows **linearly** in width (~11×width).
* Hence `steps = Θ(width²)`, `width = Θ(register)`. Measured at 12·10⁶ steps: `step/R² ≈ 10.5`, `width/R ≈ 4.9`.

`width ~ √steps` is **consistent with a Θ(4^k) braid** (register 2^k at time 4^k)
and does not by itself distinguish it from anything. It is not evidence either way.

## 2. THE TRAP: the running-max envelope is a misleading statistic

*(This section is unaffected by the bug — `x2b5_reg.py` scanned the full tape.)*

`x2b5_reg.py` tracks the running maximum of `maxrun`. It climbs by **+3 per record**,
arithmetically — 191, 194, 197, … 287, 290, … 1070 — and marches **straight through**
575 and 1151 without doubling. Read alone, this *looks like a refutation* of the
`9·2^k−1` law, and I initially recorded it as one.

**It is not.** The register is a **sawtooth**. The envelope is the *recovery* limb
(+3 per milestone); the **peaks of the deep teeth** are the real dynamics. Both
statements are true simultaneously. The envelope hides the doubling.

A second trap compounds it: **every `9·2^k−1` is ≡ 2 (mod 3)**, and the register's
`+3` climb passes through **every** value ≡ 2 (mod 3). So a probe that samples the
register sparsely and tests membership in the `9·2^k−1` family gets **free hits at
every k** — the match carries **zero** information. Both the naive confirmation
and the naive refutation of the register law are artifacts. Only the **tooth
structure** (§3) is decisive.

## 3. The register law and the braid — DECISIVE (`x2b5_braid.py`, corrected)

Register := longest run of `1`s over the **full** tape, sampled at left-record
milestones in state `C`. Deep teeth, blank tape, exact bigint, to 6·10⁷ steps:

| k | peak | `9·2^k−1` | floor | `5·2^k+6/8` | depth | `2^(k+2)−7/9` | step | **ratio** |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 17 | 17 | 16 | 16 | 1 | 1 | 2 887 | — |
| 2 | 35 | 35 | 28 | 28 | 7 | 7 | 11 187 | 3.875 |
| 3 | 71 | 71 | 46 | 46 | 25 | 25 | 45 015 | 4.024 |
| 4 | 143 | 143 | 88 | 88 | 55 | 55 | 184 287 | 4.094 |
| 5 | 287 | 287 | 166 | 166 | 121 | 121 | 758 021 | 4.113 |
| 6 | 575 | 575 | 328 | 328 | 247 | 247 | 3 119 459 | 4.115 |
| 7 | 1151 | 1151 | 646 | 646 | 505 | 505 | 12 802 029 | 4.104 |
| **8** | **2303** | **2303** | **1288** | **1288** | **1015** | **1015** | **52 366 089** | **4.090** |

**Laws exact for k = 1..8 — eight doublings:**

* `peak_k  = 9·2^k − 1`  ✅ **the [OBSERVED] register law is CONFIRMED**
* `floor_k = 5·2^k + 6` (k odd) / `5·2^k + 8` (k even) — **re-derived from corrected data**
* `depth_k = peak_k − floor_k = 2^(k+2) − 7` (k odd) / `2^(k+2) − 9` (k even)

**On the floor law's status.** It was fitted on k=1..7 and then **tested
out-of-sample at k=8**: predicted `peak 2303 / floor 1288 / depth 1015` before
running, and all three hit exactly. That is a genuine prediction, not a fit. It is
nonetheless an **[OBSERVED] law over 8 points with a parity split** — I do **not**
claim it proven, and the parity dependence is unexplained. It is not load-bearing
for any verdict below.

### 3.1 The braid — the load-bearing measurement

**Step ratio per doubling → 4.09, stable across k = 3..8.**

* linear odometer (braid-free) ⟹ ratio **2**
* quadratic shrinking-comb braid ⟹ ratio **4**

The measurement is **4**, not 2, and it is not drifting toward 2 (4.024 → 4.090 over
five doublings; the mild excess over 4 is a lower-order correction). **Each doubling
of B5's register costs 4× the steps.** B5's doubling phase is **NOT** a linear
odometer with fixed-size per-tick transport. It carries the **same Θ(4^k) grind as
B1's TOPGRIND**.

This is the one number the whole investigation turns on, and it is the one number
the bug **could not** touch: the step column is byte-identical before and after the
fix, and the coordinator reproduced it against an independent from-scratch
parser+simulator.

> **B5 is ejected INTO B1's difficulty class, not out of it.**
> This is the answer to the load-bearing question, and it is negative.

### 3.2 Where "reset 14" comes from — **UNRESOLVED**

The first version of this document asserted a mechanism: that the k=2 tooth
(peak 35, **floor 14**) recurs verbatim at every cascade, so a probe sampling the
frequent shallow teeth would report "constant reset 14". **That mechanism is
withdrawn.** On the corrected full tape `floor_2 = 28`, not 14. The floors **do**
still grow (≈×2 per k: 16, 28, 46, 88, 166, 328, 646, 1288), so **"the reset is not
constant 14" is very likely still true** — but I no longer have a mechanism, and

> **the origin of the roadmap's [OBSERVED] "reset 14" is UNEXPLAINED. I do not
> assert a mechanism I cannot re-derive.**

What *is* structurally real (corrected data): the teeth fire in an **inverted
cascade** in the run-up to milestone `2^j` — around milestone 512 the resets fire at
449, 481, 497, 505, 509, 511 = `512 − (2^(m−1)−1)`, deepest **first**, and milestone
gaps between resets of equal depth are **exact powers of two**. That cascade shape is
independent of the register values the bug corrupted.

**One unverified lead, recorded as a lead only.** My own half-tape bug produced
`floor_2 = 14` exactly. Whether the roadmap's [OBSERVED] 14 arose from a similar
truncated scan is **pure speculation — I have not inspected that probe.** It is a
concrete, cheap thing to check (`grep` the roadmap's probe for the same `lo`/`hi`
asymmetry) and nothing should be built on it until someone does.

## 4. Halt-trigger analysis, and the `2^k mod M` gate — **NO**

*(`x2b5_halt.py` performs no extent scan — unaffected by the bug.)*

4·10⁶ steps: **59 040** entries into `F`; the symbol `F` then read was `1` in
**59 040 / 59 040** cases. Zero halt-gate failures. The run-tail strictly right of
the cell `E` read is **never 0**.

**The `2^k mod M` decidability gate does not exist for B5.** Concretely:

1. The halt trigger is **not** a predicate on the register value. It fires on a
   **local** configuration (`E` reads the final `1` of a run) at an arbitrary point
   mid-sweep. Nothing reduces "does `9·2^k−1` hit a fatal residue class mod M" to it.
2. The register **never resets to a constant** — the reset is itself a doubling
   sequence (`≈5·2^k`), so there is no fixed residue to test. The premise of the
   proposed gate is false. *(This conclusion is robust to the bug: it needs only that
   the floors grow, which both the buggy and corrected data show.)*
3. Even granting a register predicate, the halt condition is decided by the
   **transport**, not the value — and the transport is the Θ(4^k) comb of §3.1.
   `2^k mod M` is eventually periodic and would be decidable; **B5's halt condition
   is not of that form**, so the periodicity buys nothing. There is no period to
   compute and no fatal residue to test — the question is malformed for B5.

## 5. Ejection check — B5 is NOT opaque

No digit-coupled branch to an opaque orbit and no value-proportional reset were
detected. Halting is **not** a base-2 return-frequency problem, so B5 does **not**
fall to the (K)-wall / H₂ = Mahler 3/2 kernel. B5 stays inside Track B's
carry-transparent island — it is simply **braid-bound within it**. The ×2 envelope
is exact and clean; it is the *cost* of the doubling, not its shape, that kills the
front. This is precisely the failure mode the roadmap warned of: **an exact ×2
envelope does not preclude a quadratic transport.**

## 6. Tape structure — what survives, and the WITHDRAWN invariant

**Structure (corrected, full tape, `x2b5_rle.py`).** The tape is **mirror-symmetric
about the origin** — which is precisely why the half-tape bug looked plausible. The
register run appears **3×** on the full tape, not once.

* **(I1) SURVIVES.** The tape is `1^a₁ 0 1^a₂ 0 … 0 1^aₙ` — **every** gap is exactly
  one `0`. Re-verified on the FULL tape: **0 violations / 441 milestones**.
* **(H) SURVIVES.** The halt gate never fires: **0 failures**.
* **(I2) REFUTED — WITHDRAWN.** The claim "every run `≡ 2 (mod 3)` except exactly two
  **boundary** runs" was read off the left half-tape. On the full tape
  (`x2b5_invariant.py`, corrected): **171 / 441 milestones violate it**, with up to
  **5** exceptional runs (histogram `{1:57, 2:213, 3:132, 4:37, 5:2}`).

**Is anything weaker true?** (`x2b5_mod3.py`, 622 milestones, full tape.) The count
of runs `≢ 2 (mod 3)` **does not grow** with the orbit — it stays `≤ 5` across every
window. But the exceptions are **not confined to the boundary**: up to **4** are
strictly interior. So the clean, local, boundary-only congruence is gone; what
remains is a **bounded-exception observation with no mechanism**.

**Consequence for §6's route.** The first version pitched this as a candidate route
that could *bypass the braid*, because (I1)+(I2) were local congruence statements
that never mention the register or the transport. **That pitch is withdrawn**: its
load-bearing premise (I2) is false. A bounded-but-unstructured exception set does not
obviously force (H), and I have no mechanism connecting them. The three obligations
— (a) that the exception count is *really* bounded rather than growing beyond my
window, (b) that boundedness implies (H), (c) that the sweep preserves it — are all
**OPEN and unaddressed**, and the sweep rewrite is exactly where the Θ(4^k) comb
lives, so the braid may re-enter inside any such induction as it did in `descentGlue`
(commit `ebec409`).

**I claim nothing here.** This is now an observation, not a route.

## 7. Answers to the three decisive questions

1. **Carry-transparent and braid-free?** Carry-transparent: yes (exact ×2 envelope,
   register `9·2^k−1`, 8 doublings). **Braid-free: NO.** Phase step-count growth is
   **Θ(4^k)** (ratio 4.09), not linear. **This was the load-bearing question and it
   answers negative.**
2. **Halting a decidable `2^k mod M` condition?** **NO.** The gate is a local tape
   condition; the reset is not constant; there is no fatal residue class and no
   period to compute. The proposed reduction is malformed for B5.
3. **Anything eject B5 from transparency?** No — B5 is **not** opaque and does not
   hit the (K)-wall. It is ejected *within* Track B, into B1's difficulty class.

## 8. Consequence for the Track B scope

`TRACK_B_ROADMAP_2026-07-16.md` §2.3 lists B5 as *potentially braid-free /
B1-independent = the de-risking front*. **That is now refuted.** B5 is
braid-bound and B1-**dependent** in difficulty: any weapon that cracks B5's
Θ(4^k) transport would very likely crack B1's, and vice versa. **B5 is not a
cheaper first target and the de-risking front does not exist where the scope
placed it.** The ~3-distinct-problems count of commit `59749fb` should be
re-examined: B5 has merged into the B1 problem.

The de-risking value here is **negative and real**: Track B cannot buy its way
around the doubling braid by picking a friendlier machine in this island. The
braid is a property of the island, not of B1.

**Method note for the front.** Two of this investigation's four structural
sub-claims were artifacts of a single unasserted assumption (`hi` is maintained),
in a probe labelled "decisive". The register law and the braid ratio survived only
because they are max/timing statistics; every min-statistic built on the same scan
was wrong. Any future Track B probe that scans a two-sided tape should derive its
extent from the tape itself, and any [OBSERVED] label resting on a one-sided scan
of a mirror-symmetric orbit should be re-checked — **including the roadmap's own
`reset 14`**, whose origin is now unexplained (§3.2).

## 9. Probes (all committable, repo root)

| file | role |
|---|---|
| `x2b5_sim.py` | predecessor's exact-bigint simulator; table **verified correct**. `extent()`/`maxrun_full()` added as the bug-proof scan helpers |
| `x2b5_peaks.py` | predecessor's sampled sawtooth probe (superseded — K=25 sampling blurs the teeth) |
| `x2b5_shape.py` | exact tape dumps (uses `Tape`, tracks both bounds — unaffected) |
| `x2b5_records.py` | O(1)/step excursion records → linear space, quadratic time (unaffected) |
| `x2b5_reg.py` | running-max envelope — **the misleading statistic of §2**, kept as the trap's exhibit (unaffected) |
| `x2b5_halt.py` | halt-trigger / F-entry census (no extent scan — unaffected) |
| `x2b5_sweep.py` | shift-rule search (negative: no uniform prefix+BLOCK^n skeleton) — **fixed** |
| `x2b5_rle.py` | run-length coordinates → (I1) — **fixed** |
| `x2b5_invariant.py` | invariant + halt-gate test — **fixed**; now **refutes** (I2) |
| `x2b5_mod3.py` | **new** — tests whether any *bounded* mod-3 invariant survives (weakly, without mechanism) |
| `x2b5_sawtooth.py` | reset cascade / inverted-cascade structure — **fixed** |
| `x2b5_braid.py` | **the decisive probe** — peak/floor/depth laws and the 4× ratio — **fixed** |

Reproduce the verdict: `python x2b5_braid.py 60000000` (k=1..8, ratio → 4).

---

**No machine decided. No label upgraded.**
