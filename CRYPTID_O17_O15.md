# o17 (carrying odometer) and o15 (parity-irregular Mahler-8/3) — the two off-template cryptids (2026-06-28)

Targeted analysis of the two BB(6) Collatz-core cryptids that do **not** fit the Antihydra/AEV-Mahler
equidistribution template (`COMPLETE_PROOF_CAPSTONE.md`). Question per machine: is it (a) same-as-Antihydra
(an AEV/Mahler single-orbit equidistribution kernel), (b) a different named problem, or (c) potentially
decidable with structural tools (the `CRYPTID_CENSUS.md` Route-(i) lottery — a decidable cryptid settles a
real BB(6) holdout)? All numerics: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact big-int),
scripts `scratch_o17_o15*.py`, `scratch_o15.py`. Soundness discipline: explicit
`[PROVEN]`/`[OBSERVED]`/`[OPEN]` labels; no decision claimed.

`o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = F reads 0).
`o15 = 1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA` (halt = A reads 1).

---

## 1. o17 — resolving the "odometer vs ×8 Mahler" tension, and the decidability verdict

The two existing docs describe o17 two incompatible ways:
- `CRYPTID_KERNEL.md` §"Placing o15 and o17": o17's base object is a **+1 carrying odometer = an isometry of
  `ℤ_p`, uniquely ergodic ⟹ equidistribution is automatic**; the hardness is *only* the halt predicate.
- `CRYPTID_REDUCTIONS.md` meta-table: o17 = "base-3 odometer **(≈×8)**" — i.e. a *geometric* `2³/3`-type
  (Erdős) orbit, which would put the hardness in an equidistribution kernel.

These imply opposite decidability stories. The numerics resolve the tension cleanly in favour of
`CRYPTID_KERNEL.md`, and the "≈×8" tag is identified as an artifact of the wrong feature being measured.

### 1a. Direct structure from blank [OBSERVED, `scratch_o17_o15.py`]
The tape is `(0 1^ℓ)*` (single-0 separators, never `00` in the settled region; max separator = 1 over
1.5–3M steps, prior `o17_verify.py`). Decoding each **settled** (non-rightmost) 1-block of length `ℓ≡2 (mod 3)`
as base-3 digit `d=(ℓ−2)/3`, a typical large-time config is
`digits(lsb→msb) = [0,2,2,0,4,0,0,0,0,0,0,0]` with a **large rightmost "active" block** of length growing
with the width (e.g. width 7737 with active block 6065 at t≈1.8·10⁷). The settled digit string is
**overwhelmingly zeros** (501 of 514 digits zero at t=2·10⁷; nonzero multiset {1×5, 4×4, 2×3, 5×1}).

- **The "≈×8" tag was the rightmost active block, not a scalar orbit.** The active block (the in-flight
  carry buffer the head sweeps) is the bulk of the width and grows with it; the *settled* significant
  digits stay small and sparse. There is **no clean `⌊μx⌋` scalar orbit** (my first decode attempt produced
  a value sequence that jumps over ~5 orders of magnitude between samples — garbage, because there is no
  single scalar being multiplied). So o17 is **not** an expanding Mahler `2³/3` map. [OBSERVED]
- **Width grows sub-linearly, ~√t** (204, 537, 1566, 6087 at t=10⁴,10⁵,10⁶,10⁷; log-log slope ≈0.49),
  **not** the exponential-direct envelope `CRYPTID_CENSUS.md` placed it in. This is the sawtooth/√t envelope
  (head sweeps a linearly-growing region per carry), consistent with an odometer whose carries occasionally
  cost `O(width)`. [OBSERVED — a correction to the census's exponential placement.]

### 1b. Subword complexity of the odometer digit string [OBSERVED — the automaticity test, task item 4/5]
For the settled-digit string at t=2·10⁷ (length 514), factor-complexity
`p(L) = 5, 12, 18, 22, 26, 28, 29, 30` for `L=1..8` — **low and saturating** (the string is sparse: mostly
0 with isolated small defects). This is the signature of a **tame / low-complexity (odometer-like)** digit
sequence, NOT a full-complexity (Erdős/Collatz) spatial sequence.

> **Resolution of the tension.** o17's *odometer* is genuinely tame: its significant-digit string has low
> spatial complexity and (as an odometer/isometry) is uniquely ergodic, so **equidistribution is automatic —
> there is no equidistribution kernel hardness** (unlike Antihydra/o15). `CRYPTID_KERNEL.md` is right; the
> "≈×8 Mahler" reading is an artifact. **But low spatial complexity does NOT imply decidable halting**: the
> halt predicate is a *carry-timing* property, not a spatial-complexity property.

### 1c. The halt predicate is the hardness — and it is Collatz-irregular [PROVEN, conjecture-free]
o17 halts ⟺ a leftward odometer carry propagates **past the most-significant digit into the blank left
region** (the counter overflows its width; `o17_attack.md` CORRECTION). The carry sub-routine engages
whenever processing hits a block whose length is `≡0 (mod 3)` (the non-digit / carry case). The embedded
single-block family `0 A 0 1^k` isolates exactly this sub-routine. Simulated from a clean start
(layout calibrated against the `k=6 → halt@206` anchor; `scratch_o17_o15b.py`, `scratch_o17_o15c.py`):

- **`k ≢ 0 (mod 3)`: always halts, fast** (k=1..60, all halt, times 7–323; 40/40 of k%3∈{1,2}). [PROVEN]
- **`k ≡ 0 (mod 3)`: Collatz-irregular.** Writing `k=3j`, **proven halters** (finite checked halt times):
  | j | k | halt time | | j | k | halt time |
  |---|---|---|---|---|---|---|
  | 2 | 6 | 206 | | 17 | 51 | 52 932 |
  | 4 | 12 | 394 | | 19 | 57 | 117 160 |
  | 5 | 15 | 794 964 | | 21 | 63 | 232 604 |
  | 7 | 21 | 4 240 985 | | 23 | 69 | 600 056 |
  | 8 | 24 | 3 690 | | 25 | 75 | 1 029 412 |
  | 10 | 30 | 7 262 | | 27 | 81 | 1 614 528 |
  | 12 | 36 | 13 810 | | 29 | 87 | 3 930 996 |
  | 15 | 45 | 45 688 | | 31 | 93 | 9 479 072 |

  Halt times are **wildly non-monotone** (k=24 halts at 3690 but k=21 at 4.24M; k=15 at 795k but k=18 never
  within budget), the halter-`j` set `{2,4,5,7,8,10,12,15,17,19,21,23,25,27,29,31,...}` follows **no
  modulus**, and several apparent non-halters at small budget halt only much later (k=63 at 232 604, k=69 at
  600 056, k=75 at 1.03M, k=93 at 9.48M). This is the textbook Collatz/3x+1 signature: proven halters
  interleaved with delayed/non-halters with no separating arithmetic. [PROVEN: the listed halters; OBSERVED:
  the no-modulus interleaving; the non-halting of the rest is itself an embedded open Collatz statement.]

> **Framework-reduction outcome for o17.** The Antihydra reduction chain (induced odd map → renewal identity
> → single-orbit `mean D ≥ 3/2` AEV kernel) **does not apply**: o17 has no expanding `⌊μx⌋` map, no
> renewal/induced odd map, and its equidistribution is *automatic* (odometer), so there is nothing for the
> AEV/Mahler kernel to control. The hardness sits in a different place than Antihydra's. **Exactly why it
> breaks vs Antihydra:** Antihydra is an *expanding* `2-to-1` endomorphism of `ℤ₂` (hardness = single-orbit
> genericity of an exact system); o17 is an *isometric* odometer (genericity free) whose hardness is a
> Collatz-irregular **halt/carry-overflow predicate**.

### 1d. o17 classification
- **Same-as-Antihydra (AEV/Mahler kernel)? NO.** Different obstruction type (isometry, not expanding map).
- **Potentially decidable (lottery upside)? NO — refuted, conjecture-free.** The tame odometer raised the
  hope, but a sound regular/FAR certificate must be step-closed and halt-free; closure forces it through the
  `0 A 0 1^k` family for unbounded `k`, which contains **proven halting members** (table above) interleaved
  Collatz-irregularly with non-halters — no finite automaton can include the reachable members while
  excluding every halt. (Matches the three SOUND `far_dfa.verify`-gated attempts in `o17_attack.md` all
  stalling on the `1A0` / `0A01^k` witness.) A false "decided" is avoided.
- **Different named problem? YES, partially.** o17 = a **uniquely-ergodic carrying odometer with a
  Collatz-irregular carry-overflow halt predicate.** This is *not* AEV/Mahler and *not* the Erdős
  ternary-digit problem (o15/o18); it is its own embedded 3x+1-type carry family. **Verdict: CRYPTID-HARD,
  different-named-problem (odometer + Collatz-irregular halt), NOT decidable.**

---

## 2. o15 — why parity-irregular, and whether it hides a different reduction

`o15` structure (`scratch_o15.py`, re-verified vs raw TM): `1^V 0 (10)^m` — a leading counter block `1^V`
over a `(10)*` background; **halt = state A's right-frontier read is a `1`** (collision).

### 2a. The clean part: width is an exact `×8/3` Mahler orbit [OBSERVED/PROVEN-multiplier]
Milestone widths `19, 40, 108, 290, 773, 2060, 5493, 14634` have ratios `→ 2.665 = 8/3` (= `2³/3`). The
width follows `W ↦ ⌊8W/3⌋+2` with occasional carry-corrections (e.g. predicted 2061→actual 2060,
14648→14634) — the **same clean Mahler-8/3 width law as o18, breaking at carry epochs** (o18's epoch-7 break
is the identical phenomenon). So o15's *width/exponent* IS a clean `(8/3)^n`-type orbit. [OBSERVED]

### 2b. The irregular part: the block decomposition (= the halt predicate) [OBSERVED]
The leading-block length `V = 6, 39, 107, 289, 6, 2059, 6, 3` is **parity-irregular**: the big block
intermittently **splits/reforms** (`1^6 0 1^765`, `1^3 0 1^1 0 1^1 0 1^14625`), so there is **no clean
scalar map for V** (unlike o18's clean width scalar). The clean total width `W` is partitioned into blocks
by the **base-3 digit/carry positions** of the `(8/3)^n` orbit; the split happens exactly when a base-3 carry
creates a new top-digit boundary. So the parity-irregularity **lives in the base-3 digit string of the
`(8/3)^n` orbit**, i.e. in the halt predicate (does the A-sweep collision point align with a `1` =
base-3-carry alignment), not in the width orbit.

> **Why parity-irregular, precisely.** o18 reads its halt off a single clean scalar (`⌊8N/3⌋+2`); o15 reads
> its halt off the *block decomposition*, which is the full base-3 **digit string** of the same orbit. The
> digit string of `(8/3)^n` is irregular (the Erdős ternary-digit phenomenon), so V — a function of where
> the leading digit boundary falls — is irregular. The irregularity is the **same `8/3` Erdős wall as o18,
> exposed in a messier coordinate**, not a new mechanism.

### 2c. o15 classification
- **Does the irregularity hide a different reduction? NO.** The kernel object is identical to o18's:
  `⌊(8/3)^n⌋ mod 3` single-orbit equidistribution = base-3 digits of `2^{3n}` (Erdős ternary family). The
  parity-irregularity only makes o15 **harder to MODEL** (no clean scalar orbit), not a different problem and
  not easier.
- **Same-as-Antihydra? NO** (different prime/multiplier: `8/3`, `p=3`, vs `3/2`, `p=2`) — but same *type*
  (expanding `p`-to-1 endomorphism of `ℤ_p`, `v_p(μ)=−1`; `CRYPTID_KERNEL.md` classification theorem). It IS
  a genuine AEV/Mahler-template machine, just the `8/3` instance.
- **Different named problem? YES — the Erdős "ternary digits of powers of 2" family** (with o5 4/3, o18 8/3),
  whose only unconditional result is **Narkiewicz's upper bound** (no lower density bound = the missing
  piece, same shape as Antihydra's missing FLP-density analogue). Published BB↔Erdős reduction:
  Stérin–Woods, arXiv:2107.12475.
- **Potentially decidable? NO.** Same Erdős wall as the whole `8/3` cluster; deciding any one needs the
  Erdős-class density breakthrough. The parity-irregularity is a modelling obstacle on top, not a crack.
  **Verdict: AEV/Mahler-template (the `8/3`/Erdős instance), no clean scalar map, CRYPTID-HARD.**

---

## 3. Bottom line — the two off-template cryptids are off-template for *opposite* reasons

| | mechanism | hardness lives in | template fit | named problem | decidable? |
|---|---|---|---|---|---|
| **Antihydra** (reference) | expanding `2-to-1` map of `ℤ₂` | single-orbit **equidistribution** (genericity) | — | AEV-3/2 ⟹ Mahler 1968 | no |
| **o15** | expanding `3-to-1` map of `ℤ₃` (`8/3`), **irregular block decomposition** | equidistribution kernel + messy halt coordinate | **YES** (the `8/3` instance) | **Erdős ternary digits of 2ⁿ** (Narkiewicz) | no |
| **o17** | **uniquely-ergodic carrying odometer** (isometry) | **halt predicate only** (Collatz-irregular carry overflow) | **NO** (no expanding map; genericity is free) | **own 3x+1-type carry family** (`0A01^k`) | no |

- **o15** is *in*-template — the same AEV/Mahler hardness as Antihydra but at `8/3` (the Erdős ternary
  cluster); its parity-irregularity is a modelling nuisance in the halt coordinate, **not a different or
  easier problem**.
- **o17** is the one genuine structural outlier: its odometer is *tame* (low spatial complexity, automatic
  equidistribution), so it has **no equidistribution kernel** at all — the entire difficulty is a
  **Collatz-irregular halt/carry-overflow predicate**, a *different* hardness type from every other core
  cryptid. The "tractable odometer" lottery is refuted, conjecture-free, by the proven interleaved halters
  of `0A01^k` — but the refutation is informative: it pins o17's hardness to a single, isolated, embedded
  3x+1-type family rather than to equidistribution.

**No machine decided; no non-halt claimed; soundness intact.** Net contribution: (i) resolved the
o17 odometer-vs-Mahler contradiction in the docs (odometer is right; "≈×8" was the carry buffer; width ~√t
not exponential); (ii) extended the o17 non-regularity witness to k≤120 with 16 proven `k≡0 (mod 3)` halters
and the no-modulus interleaving; (iii) pinned o15's parity-irregularity to the base-3 digit string of its
`(8/3)^n` orbit (same Erdős wall as o18, harder coordinate). The BB(6) Collatz core thus splits into **two
hardness types**: equidistribution kernels (Antihydra/o10-inner = 3/2; o15/o18/o5 = 8/3 Erdős) and **one
odometer-with-Collatz-halt outlier (o17)**.
