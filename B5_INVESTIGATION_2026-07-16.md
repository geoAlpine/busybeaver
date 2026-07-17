# B5 investigation — the Track B de-risking front (2026-07-16)

**Machine.** `B5 = 1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD`

**VERDICT: (b) BRAID-BOUND. B5 is no easier than x2/B1.**
The register doubling is REAL and its law is CONFIRMED (`9·2^k−1`, 7 doublings),
but the per-doubling step cost is **Θ(4^k)** — the same quadratic braid that
blocks B1/x2. The `2^k mod M` gate does **not** exist. B5 does **not** de-risk
Track B.

Two [OBSERVED] claims in the Track B scope are **REFUTED** by this probe:
the "**constant reset 14**" (the resets double: `3·2^k+2`), and the implied
**braid-freedom**. The register law itself survives.

No machine decided. No label upgraded.

---

## 0. Transition table — verified against the string, cell for cell

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

## 1. Global growth: linear space, quadratic time

From the blank tape (`x2b5_records.py`, exact, O(1)/step):

* Left and right excursion records are **symmetric**: 1086 each at 2·10⁶ steps, positions ±1086.
* The tape extends **+3 cells per side per macro-sweep**; sweep cost grows **linearly** in width (~11×width).
* Hence `steps = Θ(width²)`, `width = Θ(register)`. Measured at 12·10⁶ steps: `step/R² ≈ 10.5`, `width/R ≈ 4.9`.

`width ~ √steps` is **consistent with a Θ(4^k) braid** (register 2^k at time 4^k)
and does not by itself distinguish it from anything. It is not evidence either way.

## 2. THE TRAP: the running-max envelope is a misleading statistic

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

## 3. The register law and the braid — DECISIVE (`x2b5_braid.py`)

Register := longest run of `1`s, sampled at left-record milestones in state `C`.
Deep teeth, from the blank tape, exact bigint, to 3·10⁷ steps:

| k | peak | `9·2^k−1` | floor | `3·2^k+2` | depth | `3(2^(k+1)−1)` | step | **ratio** |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 17 | 17 | 8 | 8 | 9 | 9 | 2 887 | — |
| 2 | 35 | 35 | 14 | 14 | 21 | 21 | 11 187 | 3.875 |
| 3 | 71 | 71 | 26 | 26 | 45 | 45 | 45 015 | 4.024 |
| 4 | 143 | 143 | 50 | 50 | 93 | 93 | 184 287 | 4.094 |
| 5 | 287 | 287 | 98 | 98 | 189 | 189 | 758 021 | 4.113 |
| 6 | 575 | 575 | 194 | 194 | 381 | 381 | 3 119 459 | 4.115 |
| 7 | 1151 | 1151 | 386 | 386 | 765 | 765 | 12 802 029 | 4.104 |

**All three laws exact for k = 1..7 — seven doublings, ≥6 as required:**

* `peak_k  = 9·2^k − 1`  ✅ **the [OBSERVED] register law is CONFIRMED**
* `floor_k = 3·2^k + 2`  ❌ **the [OBSERVED] "constant reset 14" is REFUTED**
* `depth_k = 3(2^(k+1) − 1) = peak_k − floor_k`

### 3.1 The braid — the load-bearing measurement

**Step ratio per doubling → 4.10, stable across k = 3..7.**

* linear odometer (braid-free) ⟹ ratio **2**
* quadratic shrinking-comb braid ⟹ ratio **4**

The measurement is **4**, not 2, and it is not drifting toward 2 (4.024 → 4.104 over
four doublings; the mild excess over 4 is a lower-order correction). **Each doubling
of B5's register costs 4× the steps.** B5's doubling phase is **NOT** a linear
odometer with fixed-size per-tick transport. It carries the **same Θ(4^k) grind as
B1's TOPGRIND**.

> **B5 is ejected INTO B1's difficulty class, not out of it.**
> This is the answer to the load-bearing question, and it is negative.

### 3.2 Why "reset 14" was seen — the exact mechanism

The teeth fire in an **inverted cascade** in the run-up to milestone `2^j`. Around
milestone 512 the resets fire at 449, 481, 497, 505, 509, 511 = `512 − (2^(m−1)−1)`,
with depths 381, 189, 93, 45, 21, 9 — deepest **first**. Milestone gaps between
resets of equal depth are **exact powers of two** (depth 21: 32, 64, 128, 256;
depth 45: 64, 128, 256; depth 93: 128, 256; depth 189: 256).

Consequently the **k=2 tooth — peak 35, floor 14 — recurs verbatim at every single
cascade, forever, and it is the most frequent deep tooth.** A probe that samples the
frequent shallow teeth sees floor **14** recur unchanged indefinitely and concludes
"constant reset 14". The rare deep teeth (`floor_k = 3·2^k + 2` → 8, 14, 26, 50, 98,
194, 386) are the real dynamics and they **double**. The [OBSERVED] label was read
off the shallow limb of a sawtooth whose deep limb doubles.

## 4. Halt-trigger analysis, and the `2^k mod M` gate — **NO**

`x2b5_halt.py`, 4·10⁶ steps: **59 040** entries into `F`; the symbol `F` then read
was `1` in **59 040 / 59 040** cases. Zero halt-gate failures. The run-tail strictly
right of the cell `E` read is **never 0** and is always ≡ 1 or 2 (mod 3)
(observed tails: 1, 2, 4, 5, 7, 8, 10, 11, ≥12).

**The `2^k mod M` decidability gate does not exist for B5.** Concretely:

1. The halt trigger is **not** a predicate on the register value. It fires on a
   **local** configuration (`E` reads the final `1` of a run) at an arbitrary point
   mid-sweep. Nothing reduces "does `9·2^k−1` hit a fatal residue class mod M" to it.
2. The register **never resets to a constant**, so there is no fixed residue to test:
   the reset itself is `3·2^k+2`, i.e. the "reset residue" is a second doubling
   sequence, not a constant. The premise of the proposed gate is false.
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

## 6. The structure that survives — a congruence invariant (NOT a proof)

The one genuinely new asset. At **every** left-record milestone in state `C`
(`x2b5_invariant.py`, 441 milestones, 3·10⁶ steps):

* **(I1)** the tape is `1^a₁ 0 1^a₂ 0 … 0 1^aₙ` — **every** gap is exactly one `0`. 0 violations.
* **(I2)** **every** run length `aᵢ ≡ 2 (mod 3)**, except exactly **two** boundary runs. 0 violations (histogram: 439 milestones with exactly 2 exceptions, 2 with 1).
* **(H)** the halt gate never fires. 0 failures.

Note `peak_k = 9·2^k−1 ≡ 2 (mod 3)` and `floor_k = 3·2^k+2 ≡ 2 (mod 3)` — both
laws are **consistent with (I2)**, as they must be.

**Why this matters.** (I1)+(I2) are **local congruence** statements. If (I1)+(I2)
are inductively preserved by one sweep, and if they **imply** (H), then B5 never
halts — and **that argument never mentions the register, the doubling, or the
Θ(4^k) transport**. It is a closed-tape-language / CTL-shaped argument that could
in principle **bypass the braid entirely**.

**This is a CANDIDATE ROUTE, NOT A RESULT. Two obligations are OPEN and unverified:**

1. **(I2) ⟹ (H) is NOT established.** I verified (H) holds *observationally*; I did
   **not** show the congruence forces it. `E`'s landing phase within a run must be
   pinned down, and I have not pinned it.
2. **The inductive step of (I1)+(I2) is NOT verified.** It is only checked to hold
   *at milestones* over 441 sweeps — observational, exactly the evidence class the
   roadmap says is not a proof. **The sweep rewrite is precisely where the Θ(4^k)
   comb lives**, so the braid may well re-enter inside the induction — the same way
   `descentGlue`'s TOPGRIND re-entered inside the x2 descent (commit `ebec409`).
   I have no evidence it does not.

I explicitly do **not** claim this route works. It is the only non-dead direction
the probe surfaced, and it is worth exactly one scoping pass before Track B spends
anything further on B5.

## 7. Answers to the three decisive questions

1. **Carry-transparent and braid-free?** Carry-transparent: yes (exact ×2 envelope,
   register `9·2^k−1`, 7 doublings). **Braid-free: NO.** Phase step-count growth is
   **Θ(4^k)** (ratio 4.10), not linear. **This was the load-bearing question and it
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

## 9. Probes (all committable, repo root)

| file | role |
|---|---|
| `x2b5_sim.py` | predecessor's exact-bigint simulator; table **verified correct** |
| `x2b5_peaks.py` | predecessor's sampled sawtooth probe (superseded — sampling at K=25 blurs the teeth) |
| `x2b5_shape.py` | exact tape dumps |
| `x2b5_records.py` | O(1)/step excursion records → linear space, quadratic time |
| `x2b5_reg.py` | running-max envelope — **the misleading statistic of §2**, kept as the trap's exhibit |
| `x2b5_halt.py` | halt-trigger / F-entry census |
| `x2b5_sweep.py` | shift-rule search (negative: no uniform prefix+BLOCK^n skeleton) |
| `x2b5_rle.py` | run-length coordinates → (I1)/(I2) |
| `x2b5_invariant.py` | invariant + halt-gate test, 441 milestones |
| `x2b5_braid.py` | **the decisive probe** — peak/floor/depth laws and the 4× ratio |

Reproduce the verdict: `python x2b5_braid.py 30000000`.

---

**No machine decided. No label upgraded.**
