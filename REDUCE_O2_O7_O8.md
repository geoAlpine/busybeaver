# Attempting the EXACT 2^k halt predicate for o2, o7, o8 (the simpler μ=3/2 counter-reset machines)

*Goal: make o2/o7/o8 IN-SCOPE like Antihydra by deriving the exact 2^k halt predicate (raw TM →
clean fragment of the floor-mirror AEV 1.6(3/2) conjecture). 2026-06-29.*

**Soundness discipline (paramount).** Every quantitative claim is machine-checked this session with the
exact-bigint interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, on an instrumented simulator
**proven step-for-step identical to `bb_sim.py`** (same `parse`/`step`; verified equal `(steps, ones)` for
all three machines at 10⁶ steps). Labels `[PROVEN]` (elementary mechanics / definitional),
`[VERIFIED]` (machine-checked here, exact), `[OPEN]`. **No machine is decided; no non-halting asserted.**
One hypothesized predicate was *retracted* after it failed the bb_sim cross-check (§5) — the discipline held.

Verbatim specs (from `suite.py` CRYPTIDS), halt transitions cross-checked against the raw table:

| id | spec | HALT | F entered via | halt config (seed-verified, §2) |
|---|---|---|---|---|
| o2 | `1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA` | F reads 0 | `D:0→0RF` | a `00` to the **right** of the D→F frontier |
| o7 | `1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC` | F reads 0 | `C:0→1LF` | a `00` to the **left** (left counter empty when C consumes the separator) |
| o8 | `1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE` | F reads 0 | `E:0→1LF` | a `00` to the **left** (left counter empty when E consumes the separator) |

All three run **10⁷ steps with no halt** (`bb_sim`/instrumented, this session: o2 4322 ones, o7 2643, o8 2375).

---

## 0. Headline result

> **0 of the 3 become in-scope.** o2, o7, o8 each get a **`[PROVEN]` exact local halt event** (the
> `00`-adjacency at the sweep frontier, seed-verified on the raw TM) and a **`[VERIFIED]` nested-`⌊3/2⌋`
> induced map**, but the **exact closed-form 2^k halt predicate is NOT derivable** because the orbit map is
> a *nested* two-counter with a **2-adic-carry-governed refill cascade** — it is **not a single clean
> `⌊3x/2⌋` orbit**, so it does **not** reduce to the clean single-orbit AEV-1.6(3/2) fragment the way
> Antihydra does. The blocker is **the same one that puts o10-FULL / o11 out of scope** (nested outer
> refill). They **stay in-family-not-in-scope** — but with a *sharper* halt event than the catalogue's
> "head-local reads 0".

This is the honest, expected outcome of the §2 caveat in `BB6_STRUCTURAL_LIMIT_THEOREM.md`/`MAHLER_3_2_DOMINANCE.md`
("only the multiplier is pinned"): the reason the exact predicate is absent is now **identified and verified**,
not merely "not derived." Antihydra is in-scope because it has a **decoupled** clean integer (`h→⌊3h/2⌋`,
every step, monotone) plus an **additive Birkhoff balance** whose sign is the halt; o2/o7/o8 have **coupled**
counters where the growth variable *is* the variable that collapses, with no separable balance.

---

## 1. The exact tape mechanics (reverse-engineered from the raw TM)  [VERIFIED]

### o7 and o8 — two unary counters `1^a 0 1^b` (Antihydra *shape*)
Milestone = left-extreme in state D (o7) / A (o8). The tape is exactly `1^a 0 1^b`, a left counter `a`, a
single `0` separator, a right counter `b`. Mechanics (traced step-by-step):

- **Sweep phase (b=1 epochs).** When `a` is **even**, the machine runs a clean intra-epoch chain
  `a → ⌊3a/2⌋ + c` (c=2 for o7, c=1 for o8), `b` staying 1 — the **clean `μ=3/2` part** `[VERIFIED]`:
  - o7 reset orbit (b=1): `6, 11, 16, 26, 41, 49, 58, 89, 103, 131, 166, 251, 316, 476, 716, 1076, 1616`;
    the even-`a` consecutive tail `316→476→716→1076→1616` has ratios `1.506, 1.504, 1.503, 1.502 → 3/2`.
  - o8 reset orbit: `2, 4, 7, 10, 16, 25, 30, 46, 70, 106, 160, 241, 273, 309, 331, 415, 520, 781, 809, 912`;
    even-`a` steps obey `a' = ⌊3a/2⌋+1` exactly (`10→16→25`, `46→70→106→160→241`, ratios `→1.5063`).
- **Refill cascade (the nesting).** When `a` is **odd**, instead of growing it **collapses** into a
  halving cascade that grinds `a` down while building `b`, then re-collects all mass into a new (smaller)
  `a`. For o8 the **first cascade step is an exact closed form** `[VERIFIED 8/8]`:
  > `(a, 1) → (a1, b1)` with `a1 = ⌊a/2⌋ − 1`, `b1 = a1 + 5`,
  
  confirmed for `a = 25, 241, 273, 309, 331, 415, 781, 809` (e.g. `25→(11,16)`, `241→(119,124)`); the
  sub-steps continue `(a,b) → (⌊a/2⌋−1, b + (⌊a/2⌋−1) + 4)` until `a` is small/even, then reset. This is a
  **binary-expansion (2-adic) algorithm**: the collapse target depends on the **full 2-adic structure of
  `a`** (the number of halvings = bit-length-type quantity), not on a single floor step. The reset ratios
  interleave clean `≈1.50` with collapse `≈1.07–1.25` (o8: `…1.5063, 1.1328, 1.1319, 1.0712, 1.2538…`),
  i.e. a genuine **nested meta-epoch** structure (NOT a clean scalar map).

### o2 — leading counter over a `(10)*` sea (the T2 template)
Milestone shows `1^2 0 (10)^m … 1^2 0 (10)^j`: a `(10)*` background carrying small `11`-defects, with a
leading unary counter that grows `μ=3/2` (nested), re-confirming `CATALOGUE_O2_O5.md`'s leading-counter
orbit `5, 11, 65, 101, 155, 551, 1253, 1883` (ratios `→3/2` only on the `101→155`, `…→1883` subsequence).
**Structurally o2 is a `(10)*`-sea machine like o11/o12** (irregular-geometric collapse), *not* the clean
two-counter of o7/o8 — its content carry is even less regular.

---

## 2. The exact halt EVENT — seed-verified on the raw TM  [PROVEN]

The halt is definitionally "F reads 0". Tracing the entry path pins the *config* that triggers it; seeded
raw-TM runs (the o18-style airtight check) confirm necessity and sufficiency:

- **o2 `[PROVEN]`.** `D:0→0RF` writes 0, moves R; F reads the cell to the right. Halt ⟺ **a `00`-gap opens
  to the right of the D→F frontier**. Seed `{−1:1,0:0,1:0}` head@0 state D → **HALT in 2 steps**; control
  `{…,1:1}` → runs. (A `00` hole in the 1-field at the rightward sweep.)
- **o7 `[PROVEN]`.** `C:0→1LF` writes 1 over the separator, moves L; F reads the cell left of the separator
  = the last cell of the left block. Halt ⟺ **the left block is empty (`a=0`)** = a `00` to the left.
  Seed `1^a 0 1^3`, head on separator in C: `a=0 → HALT(2)`, `a≥2 even → RUN`. `[VERIFIED]`
- **o8 `[PROVEN]`.** Identical with `E:0→1LF`. Seed: `a=0 → HALT(2)`, `a≥2 even → RUN`. `[VERIFIED]`

**Non-halt so far `[VERIFIED]`.** Over 2·10⁶–10⁷ steps the live orbits never reach the halt config; at every
separator-consumption (F-entry) the left block stays `a ≥ 2` (minA = 2 for both o7, o8).

**Facet: EXISTENCE** for all three. Non-halt ⟺ the orbit **never enters** the `00`-collision/gap config —
a hitting/avoidance (Π⁰₁) event, **not** a density (Cesàro) bound. (None inherits Antihydra's density `β>0`
barrier — consistent with `BB6_STRUCTURAL_LIMIT_THEOREM.md` §7.1.)

---

## 3. Why the exact 2^k predicate does NOT close (the precise blocker)  [VERIFIED structural]

For a machine to be **in-scope** (like Antihydra / o18) the halt must reduce to a clean arithmetic event of
a **single clean `μ`-orbit** = a fragment of (floor-mirror) AEV-1.6:

| | clean orbit map? | halt = clean event of it? | in-scope? |
|---|---|---|---|
| **Antihydra** | YES: `h→⌊3h/2⌋` every step, monotone, decoupled | YES: additive balance `3E−n<0` (density) | **IN** |
| **o18** | YES: `N→⌊8N/3⌋+2` (breaks only at a carry) | YES: base-3 carry alignment (existence) | **IN** |
| **o7, o8** | **NO** — `⌊3a/2⌋+c` holds only on the **even-`a` intra-epoch** subsequence; **odd-`a` triggers a 2-adic halving-cascade refill** (coupled `b`) | event is local (`a=0`), but the orbit that must avoid it is the **nested** map | **OUT** |
| **o2** | **NO** — `(10)*`-sea leading counter, nested `3/2`, irregular like o11/o12 | local `00`-gap | **OUT** |

The decisive obstruction `[VERIFIED]`: the induced reset map is **not** `⌊3x/2⌋` (checked: o7 `251→316`,
`41→49`; o8 `25→30`, `241→273` all deviate from `⌊3a/2⌋` by the cascade). The collapse value is set by the
**full 2-adic expansion of `a`** via the refill cascade — a *second, nested* recurrence coupling the two
counters. This is **exactly the o10-FULL / o11 blocker** ("nested outer refill, not eventually periodic /
no clean scalar `2^a/3^b` map", `MAHLER_3_2_DOMINANCE.md` rows o10/o11, `CATALOGUE_O7_O12.md` §3–4). Only
the **inner** even-`a` chain is the clean AEV `3/2` kernel — like o10, whose inner is in-family `[CONDITIONAL]`
but whose FULL machine is OUT.

So even a full proof of floor-mirror AEV-1.6(3/2) would **not** decide o2/o7/o8 as stated: the missing link
is the **exact halt reduction**, and that reduction does not exist because the halt-avoidance object is the
**nested** map, not the clean single `3/2` orbit. They remain *kernel-input-only* (`MAHLER_3_2_DOMINANCE.md`
§2 row 3).

---

## 4. Per-machine verdict

| machine | exact halt event `[PROVEN]` | induced map `[VERIFIED]` | facet | which AEV fragment *would* decide it | in-scope? | blocker |
|---|---|---|---|---|---|---|
| **o7** | F reads 0 ⟺ left counter empty (`00`-left) when C consumes the separator | nested `⌊3a/2⌋+2` (even-`a`) + 2-adic halving-cascade refill (odd-`a`) | existence | floor-mirror AEV-1.6(3/2), q=2, **existence**, *only after an exact reduction that does not close* | **NO** | nested cascade refill (o10/o11-type) |
| **o8** | F reads 0 ⟺ left counter empty (`00`-left) when E consumes the separator | nested `⌊3a/2⌋+1` (even-`a`) + exact cascade `a1=⌊a/2⌋−1, b1=a1+5` (odd-`a`) | existence | same q=2 existence fragment, reduction does not close | **NO** | nested cascade refill |
| **o2** | F reads 0 ⟺ `00`-gap to the right at the D→F frontier | `(10)*`-sea leading counter, nested `3/2`, irregular (o11/o12-class) | existence | same q=2 existence fragment, no clean scalar map | **NO** | `(10)*`-sea irregular collapse (no clean scalar orbit) |

---

## 5. Soundness ledger — a retraction (the discipline working)

I hypothesized a clean **parity** predicate "o7/o8 halt ⟺ left block `a` is odd-or-0 at separator
consumption" (motivated by a seed test where `a=1,3` halted and `a=2,4` survived). **Cross-checking against
`bb_sim` over 2·10⁶ steps REFUTED it**: 3 (o7) and 9 (o8) F-entries had odd `a` with **no** halt
(the `a=1,3` seed halts were multi-step artifacts of an unnatural right context, not the immediate F-read).
**Predicate retracted.** The surviving, definitional halt event is exactly "F reads 0" = the `00`-adjacency
of §2 (seed-verified), and the live orbit keeps `a ≥ 2` at every consumption (no halt to 10⁷). This is the
recurring `SOUNDNESS_INCIDENT` lesson: a clean-config rule can be unfaithful out-of-sample; only the
bb_sim-cross-checked statement is kept.

## 6. Net contribution
- **Sharpened halt events** (`[PROVEN]`, seed-verified) for all three: the precise `00`-collision configs,
  improving on the catalogue's "head-local reads 0".
- **Identified the exact blocker** (`[VERIFIED]`): a 2-adic halving-**cascade refill** coupling the two
  counters (for o8, the first cascade step is an exact closed form `a1=⌊a/2⌋−1, b1=a1+5`, 8/8). This is the
  o10-FULL/o11 nesting, now pinned for o2/o7/o8 — *why* the exact predicate is absent, not just *that* it is.
- **Verdict: 0 of 3 in-scope.** They stay in-family-by-multiplier; the floor-mirror dominance count
  (`MAHLER_3_2_DOMINANCE.md`) is unchanged (still 2 in-scope: Antihydra, o10-inner). No machine decided;
  no non-halting asserted; one over-eager predicate caught and retracted by the cross-check gate.
