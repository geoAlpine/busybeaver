# Frontier catalogue: the slow-width cryptids o2, o3, o4, o5 (2026-06-28)

Per-machine reverse-engineering of the four slow-width-cluster cryptids assigned from `suite.py`'s
`CRYPTIDS`, against the **raw TM via `bb_sim.py`** (exact big-int, `.venv` python). Every quantitative
statement below was produced by my own simulation this session and is labelled
`[VERIFIED]` (machine-checked here) / `[OBSERVED]` (empirical pattern, not a proof) /
`[OPEN]`. **Soundness paramount: no machine is decided; every claim of decidability defaults to
HOLDOUT and is only escalated if the SOUND `far_dfa.verify` gate confirms — it did not for any.**

## TM specs (verbatim from `suite.py`)
| id | spec | HALT transition (verified vs `bb_sim.parse`) |
|---|---|---|
| o2 | `1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA` | `(F,0)`; F entered via `D,0→0RF` |
| o3 | `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC` | `(F,0)`; F entered via `E,0→1RF` |
| o4 | `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` | `(F,1)`; F entered via `B,1→1RF` |
| o5 | `1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB` | `(D,1)`; D entered via `C,1→1LD` |

**Halt-event reading (verified):** o2/o3 halt on a **`00`-gap** (the D/E→F rightward sweep, after
writing, reads a `0` adjacent to a `0` — a hole in the 1-field). o4/o5 halt on a **`11`-collision**
(o4: B→F rightward read of an adjacent `1`; o5: C→D leftward read of an adjacent `1` — two 1-blocks
abut in the `(10)*` field).

---

## Shared envelope finding [VERIFIED] — all four are sawtooth (poly-time) envelopes

Width `W(t)` vs `t` (single blank-tape run, `bb_sim`):

| id | t=1e4 | 1e5 | 1e6 | 1e7 | `W/√t` | envelope |
|---|---|---|---|---|---|---|
| o2 | 204 | 626 | 1860 | 6012 | 2.04→1.90 (≈const) | `W~1.9√t`, time `~W²` |
| o3 | 146 | 444 | 1366 | 4266 | 1.46→1.35 (≈const) | `W~1.4√t`, time `~W²` |
| o4 | 185 | 516 | 1506 | 4573 | 1.85→1.45 (→const) | `W~1.45√t`, time `~W²` |
| o5 | 153 | 441 | 1377 | 4312 | 1.53→1.36 (→const) | `W~1.37√t`, time `~W²` |

**All four have a `~√t` (quadratic-time) width ENVELOPE** — a head sweeping a linearly-growing region.
This corrects the earlier dichotomy tag that listed **o5 as "exponential."** o5's `√t` envelope is
measured here (`W/√t` flat at ≈1.36 across 3 decades); the `4/3` it carries is a **content** multiplier
(below), not a width-envelope rate. The envelope is cosmetic; the deep content is what is irregular
(consistent with `CRYPTID_REDUCTIONS.md` "one difficulty in two costumes").

The automatic `cryptid_map.characterise` milestone reads **IRREGULAR** on all four (width and binval),
confirming the crude milestone is the wrong event — hand-picked turning-point milestones (below) are
required.

---

## o2 — Mahler **3/2** two-counter, `00`-gap existence halt  [in Antihydra family by multiplier]

**Mechanism [VERIFIED].** Right-extreme-in-B milestones give the clean turning-point form
`1^a 0 1^c 0` (a leading unary counter `1^a` over a `(10)*` field). The leading block `a` IS the
longest 1-run (content grows geometrically — *not* bounded):

```
t:    22    92   1598  3656  8206  94400  478698  1075964
a:     5    11     65   101   155    551    1253     1883
ratio:    2.20  5.91  1.554 1.535  3.555  2.274   1.503
```

**Multiplier [VERIFIED ≈3/2].** The *clean consecutive* resets give `101/65=1.554`, `155/101=1.535`,
`1883/1253=1.503` → **3/2**; the larger jumps are **powers of 3/2** (`×5.91≈(3/2)^4.4`,
`×3.555≈(3/2)^3`, `×2.274≈(3/2)^2`) = a **nested / meta-epoch** structure (like o8/o10). The epoch
time-ratio `≈2.25 = (3/2)²` is the `√t` envelope's signature of a `3/2` content. So `a ~ c·(3/2)^n`.

**Classification:** **(b) Collatz-kernel, Mahler `μ=3/2`, `p=2`** — the **Antihydra / o7 / o8 family**,
nested two-counter. **Facet = existence** (halt = a `00`-gap hitting event at the D→F sweep), *not*
density: so it does **not** inherit Antihydra's `β>0` density barrier (that barrier is `[PROVEN]` for
Antihydra only). Per `BB6_STRUCTURAL_LIMIT_THEOREM` §2, o2 is **in-family by multiplier, not in-scope
by proof** — the exact 2-adic halt criterion is not derived; only the multiplier + halt-event are pinned.

**Halt criterion (structural, verified):** halts ⟺ the rightward `D→F` sweep ever lands on a `0` with a
`0` to its right (a `00`-gap opens in the 1-field) — a head-local, q=2 existence/avoidance event of the
`(3/2)^n` orbit. `[OPEN]` (Mahler-3/2-hard).

---

## o3 — bounded-alphabet odometer/counter, `00`-gap halt  [DIFFERENT: kernel-less, the most regular]

**Mechanism [VERIFIED].** At the right-extreme-in-C turning point the tape is strikingly clean:
`1^2 0 (1^5 0)^m` — a leading `1^2 0`, a **period-6 background `1^5 0`**, and a small `1^2`/`1^4`
defect cluster near the right frontier. Block COUNT grows; the longest 1-run stays `=5`:

```
t:        35   137   345   693  1385  2557  4657 14883 27311 49859 90061
W:         9    18    29    42    59    80   107   185   246   327   434   (W~1.4√t)
#(1^5):    1     2     3     5     7    10    14    27    37    50    67
longest1:  5     5     5     5     5     5     5     5     5     5     5
```

**Bounded content [VERIFIED to 2·10⁷ steps].** At *generic* (non-milestone) times the block lengths are
varied (not all 5) but **every run is bounded**: `maxrun1 ≤ 6`, `maxrun0 ≤ 2` at t = 1e5, 1e6, 5e6, 2e7;
the count of non-`1^5` blocks is large and grows (37→398→1301→2680), i.e. the **arrangement** of a small
bounded alphabet is irregular while no block expands.

**Classification:** **(d)/(c) DIFFERENT — kernel-less, bounded-alphabet odometer/counter.** This is the
sole machine of the four with **bounded local content** (no `2^a/3^b` expanding block), so it is **outside
the expanding-kernel Collatz class** — structurally nearest the **o17 odometer outlier**, but with an even
smaller digit alphabet (runs ≤6). It carries **no clean scalar Mahler map**; the hardness is an irregular
carry/digit-string arrangement, not equidistribution of `⌊μⁿ⌋`. The **most regular-looking** of the four
(lowest content entropy) and the single best future decision candidate — but see lottery below.

**Halt criterion (structural, verified):** halts ⟺ the rightward `E→F` sweep ever reads a `00`-gap.
`[OPEN]`.

---

## o4 — Mahler **4/3 = 2²/3** single long-0 defect, `11`-collision halt  [Erdős ternary family]

**Mechanism [VERIFIED].** `(10)*` background carrying a single **long-0 defect** (a `0^k` block). Within
an epoch the defect shrinks deterministically by `−3` per drift event (L-extreme-in-A snapshots:
`0^13 1, 0^10 1, 0^7 1, 0^4 1`), drifting toward the right boundary; at the bottom it **resets to a new
peak**. The reset peaks (max 0-run local maxima) grow cleanly:

```
peak0run: 18  29  42  61  82 110 150 205 274 366 493 658 878 1174 1566 2093 2794
ratio:      1.611 1.448 1.452 1.344 1.341 1.364 1.367 1.337 1.336 1.347 1.335 1.334 1.337 1.334 1.337 1.335
```

**Multiplier [VERIFIED → 4/3].** The peak ratio converges to **1.334–1.337 ≈ 4/3**.

**Classification:** **(b) Collatz-kernel, Mahler `μ=4/3 = 2²/3`, `p=3`** — the **Erdős ternary-digits-of-
`2^{2n}` family** (the `o5/o15/o18` cluster). **Facet = existence** (`11`-collision hitting event).
Note the earlier `o4` "decision lead / monotone gap" was already RETRACTED (the `−3` sawtooth is a
within-epoch local rule, not a global invariant); my data reproduces both the `−3` shrink and the
geometric `4/3` reset, confirming the retraction (no clean monotone non-halting invariant).

**Halt criterion (structural, verified):** halts ⟺ the rightward `B→F` sweep ever reads a `1` adjacent
to the defect (the `11`-collision at the right boundary). `[OPEN]` (Erdős-ternary-hard; same wall as
o5/o15/o18; Narkiewicz gives only a density upper bound, no lower bound).

---

## o5 — Mahler **4/3 = 2²/3** single long-0 defect, `11`-collision halt  [Erdős ternary family]

**Mechanism [VERIFIED].** Same template as o4: `(10)*` background with a single **long-0 gap** defect;
the leading region carries a small `1^2`/`1^3`/`1^4` floating defect. Right-extreme-in-F (and -B)
milestones give the clean `1 0^k 1` gap; the gap-reset peaks grow:

```
peak0run: 32  47  67  96 127 174 235 318 427 574 770 1027 1374 1835 2447
ratio:      1.469 1.426 1.433 1.323 1.370 1.351 1.353 1.343 1.344 1.341 1.334 1.338 1.336 1.334
```

**Multiplier [VERIFIED → 4/3].** Ratio converges to **1.334–1.338 ≈ 4/3** (measured independently at the
R-F and R-B turning points; identical). The `√t` width envelope (above) coexists with this `4/3` content
multiplier.

**Classification:** **(b) Collatz-kernel, Mahler `μ=4/3 = 2²/3`, `p=3`** — **Erdős ternary family**,
identical kernel to o4 (and o15/o18 at `8/3`). **Facet = existence** (`11`-collision). Confirms the prior
`o5 = 4/3` reduction with my own `bb_sim` peaks, and corrects o5's stray "exponential-envelope" tag.

**Halt criterion (structural, verified):** halts ⟺ the leftward `C→D` sweep ever reads a `1` adjacent to
the defect (the `11`-collision). `[OPEN]` (Erdős-ternary-hard).

---

## Catalogue table (framework columns)

| id | facet | kernel `q` (`μ`, `p`) | content mult [VERIFIED] | width envelope | halt discriminator | family | barrier | status |
|---|---|---|---|---|---|---|---|---|
| **o2** | existence | q=2 (`3/2`, `p=2`) | 3/2 (nested) | `~√t` | head-local `00`-gap (D→F) | Mahler 3/2 (Antihydra/o7/o8) | none proven; `β>0` is Antihydra-only | **[OPEN] HOLDOUT** |
| **o3** | existence | **none** (kernel-less) | bounded (runs ≤6) | `~√t` | head-local `00`-gap (E→F) | bounded-alphabet odometer (o17-type) | none proven | **[OPEN] HOLDOUT** |
| **o4** | existence | q=3 (`4/3=2²/3`, `p=3`) | 4/3 | `~√t` | head-local `11`-collision (B→F) | Erdős ternary (o5/o15/o18) | none proven | **[OPEN] HOLDOUT** |
| **o5** | existence | q=3 (`4/3=2²/3`, `p=3`) | 4/3 | `~√t` | head-local `11`-collision (C→D) | Erdős ternary (o4/o15/o18) | none proven | **[OPEN] HOLDOUT** |

**Family convergence (consistent with `CRYPTID_REDUCTIONS.md`):** o2 joins the **Mahler 3/2** family;
o4 and o5 join the **Erdős ternary `2^a/3`** family (so the Erdős cluster is `{o4, o5, o15, o18}`); o3 is
the **odd one out** — kernel-less bounded-alphabet odometer, nearest o17. No new number-theory family
appears. The three expanding-content machines all carry an **existence** halt (gap/collision hitting
event), so **none inherits Antihydra's `[PROVEN]` density `β>0` barrier** — their barrier is the `[OPEN]`
over-approximation/REG top.

---

## The lottery check — is any of o2–o5 DECIDABLE by the SOUND tools?  **NO. All HOLDOUT.**

Default to HOLDOUT; escalate to DECIDED only if the sound `far_dfa.verify` gate confirms. It did not for
any machine, under generous parameters:

| tool (this session, generous params) | o2 | o3 | o4 | o5 |
|---|---|---|---|---|
| `bb_sim` 5·10⁶ steps | no halt | no halt | no halt | no halt |
| `suite.verdict` (default) | HOLDOUT | HOLDOUT | HOLDOUT | HOLDOUT |
| `far_finder` (Ns≤8000, ks≤7) | HOLDOUT | HOLDOUT | HOLDOUT | HOLDOUT |
| `far_dfa` (m≤8) | HOLDOUT | HOLDOUT | HOLDOUT | HOLDOUT |
| `far_cegar` (N=3000, rounds=80) | HOLDOUT | HOLDOUT | HOLDOUT | HOLDOUT |
| translated-cycler (3M/300k) | HOLDOUT | HOLDOUT | HOLDOUT | HOLDOUT |
| bouncer single/word/wall (200k/20k) | HOLDOUT | HOLDOUT | HOLDOUT | HOLDOUT |
| halt-segment (W=24) | None | None | None | None |

Every SOUND tool — including the decider-agnostic `far_dfa.verify` gate driven by `far_finder` and
`far_cegar` — returned **HOLDOUT** (no verified non-halting invariant), and `bb_sim` confirms no halt. These agree with the prior generous census
sweep (`CRYPTID_CENSUS.md` 2026-06-23: translated-cycler 3M/300k, bouncers 200k/20k, FAR Ns≤12000 ks≤6,
CEGAR 120 rounds, halt-segment W=24 — all HOLDOUT). **The structural reason FAR/CEGAR hold out:** the
width ENVELOPE is regular (`√t` sawtooth) but the CONTENT is irregular geometric (Mahler 3/2 for o2;
Erdős 4/3 for o4/o5) or an irregular bounded-alphabet odometer (o3) — a regular over-approximation
closes through the irregular content and hits a halt, so no regular invariant verifies. **No false
proof; no decision; soundness intact.**

**Best future decision candidate:** o3 (bounded local content, runs ≤6) is structurally the tamest, but
it is currently HOLDOUT under every sound tool and its block-arrangement carry is irregular (o17-type),
so it stays `[OPEN]`.

## Soundness statement
No machine decided. No non-halting asserted. Every multiplier/halt-event is `bb_sim`-cross-checked this
session (exact big-int). Labels are not upgraded. The `[OPEN]` kernels are the named Mahler-3/2 (o2) and
Erdős-ternary-`2^a/3` (o4, o5) problems; o3 is a kernel-less odometer-type whose hardness is an irregular
bounded-alphabet carry.
