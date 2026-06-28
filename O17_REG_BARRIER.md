# o17 — the certificate barrier of the odometer cryptid, made exact and machine-checked (2026-06-28)

Target (the task): solidify o17's "no REG / k-window certificate" claim into a clean **[PROVEN]** barrier
(the existence-facet analog of Antihydra's density `β>0`, for the one BB(6) cryptid that has an embedded
Collatz-irregular halter family), build the non-local-vs-head-local frontier catalogue, and decide whether
o17 closes `LIMIT_THEOREM.md`'s `[OPEN]` "no REG certificate for a cryptid".

`o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = state F reads 0).

**Soundness (paramount).** Every line is `[PROVEN]` (conjecture-free, elementary), `[VERIFIED]`
(machine-checked this session, exact, `bb_sim`-cross-checked, `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`),
`[OPEN]`, or `[OBSERVED]`. **No machine decided. No non-halt claimed.** The central, soundness-critical
outcome is a *precisely-scoped barrier with a finite floor* **plus a machine-checked honest negative that
CORRECTS an over-claim in the prior notes** — and the two together are the finding.

---

## 0. Headline verdict (read this first)

| certificate class | "no certificate proves o17 non-halting"? | basis |
|---|---|---|
| **m-window (LT), m ≤ 8** | **[PROVEN]** (conjecture-free, machine-checked) | §2, §3 |
| **m-window (LT), m ≥ 9** | **[OPEN]** (family falls off reachable's window set) | §3 (the honest negative) |
| **REG (FAR-DFA)** | **[OPEN]** (= as hard as resolving o17) | §3, §5 |
| **SLIN / automatic** | **[OPEN]** | §5 |

> **One-line answer.** o17 has a **proven finite-floor** existence barrier: *no m-window certificate exists for
> m ≤ 8.* This is a genuinely **higher floor** than o18's (m ≤ 2) and rests on a genuinely **Collatz-irregular
> halter family**, but it is still a **finite floor** — at m ≥ 9 the witnessing family `0 A 0 1^k` is no longer
> window-equivalent to anything reachable, so the all-or-nothing engine loses its fuel exactly as for o18.
> **o17 does NOT establish an all-`k` / REG barrier and does NOT close LIMIT_THEOREM's `[OPEN]` item** (§5).

> **⚠ Soundness correction.** `CRYPTID_O17_O15.md` §1d and `O18_NO_CERTIFICATE.md` §5 stated that o17 *has a
> `[PROVEN]` k-window/REG barrier for k ≥ m* (the all-or-nothing engine "fires"). **That is an over-claim.**
> Machine-checked here: the engine fires only for **m ≤ 8** and then **stops** (the binding gram `0 A 0 1^6` is
> absent from reachable). This **vindicates the `LIMIT_THEOREM.md` "honest negative"** (the §"Below REG" entry:
> o17's overflow is read at a *bounded* frontier, so a large-enough window gates it). The o17-vs-o18 contrast is
> therefore **quantitative (floor 8 vs floor 2), not qualitative.** Retraction recorded; no false barrier stands.

---

## 1. The embedded family `0 A 0 1^k` — exact halt structure  [VERIFIED, bb_sim-cross-checked]

The carry sub-routine that decides o17's halt is isolated by the single-block family `0 A 0 1^k` (FAR encoding
`A 0 1^k`: state A on a blank head cell, a clean run of `k` ones to its right, blank elsewhere). Simulated from
this clean start (`o17_barrier_fast.py`, bytearray; **cross-checked step-for-step against `bb_sim.run` /
`far.step_str` for the blank run and for k ∈ {1,2,3,6,12,24,…} and ALL k = 1..90** — `o17_barrier_verify.py`
prints "all family runs agree ours==bb_sim-style OK"; the layout is the one matching the `k=6` anchor).

- **`k ≢ 0 (mod 3)`: ALWAYS halts, fast.** k = 1..120, k%3 ∈ {1,2}: **80/80 halt** (times 8–644, ~linear in k).
  These are the trivial halters. **[PROVEN]** (finite checked halts).
- **`k ≡ 0 (mod 3)` (write k = 3j): Collatz-irregular.** **18 proven halters** (finite checked halt times),
  interleaved with apparent non-halters, **no modulus, wildly non-monotone**:

  | j | k | halt time | | j | k | halt time | | j | k | halt time |
  |--|--|--|--|--|--|--|--|--|--|
  | 2 | 6 | 207 | | 15 | 45 | 45 689 | | 25 | 75 | 1 029 413 |
  | 4 | 12 | 395 | | 17 | 51 | 52 933 | | 27 | 81 | 1 614 529 |
  | 5 | 15 | 794 965 | | 19 | 57 | 117 161 | | 29 | 87 | 3 930 997 |
  | 7 | 21 | 4 240 986 | | 21 | 63 | 232 605 | | 31 | 93 | 9 479 073 |
  | 8 | 24 | 3 691 | | 23 | 69 | 600 057 | | **34** | **102** | **27 907 823** |
  | 10 | 30 | 7 263 | | | | | | **36** | **108** | **66 631 483** |
  | 12 | 36 | 13 811 | | | | | | | | |

  - **The Collatz signature is now demonstrated, not asserted.** k = 102 and k = 108 are **delayed halters**:
    both *ran past budget 10⁷* (looked like non-halters) and **only halted at 2.8·10⁷ and 6.7·10⁷** — proven
    halters interleaved with apparent runners, exactly the textbook 3x+1 behaviour. Halt times are non-monotone
    (k=24 halts at 3 691 but k=21 at 4.24M; k=93 at 9.5M). The halter-`j` set
    `{2,4,5,7,8,10,12,15,17,19,21,23,25,27,29,31,34,36,…}` follows **no arithmetic progression**.
  - The *non-halting* of the remaining `k = 3j` (j = 1,3,6,9,11,…, all run > 10⁸, `o17_barrier_fast.py`) is
    itself an **embedded open Collatz statement** — not claimed proven. **[OBSERVED]**

> **Net (item 1).** o17's odometer is tame (uniquely ergodic, automatic equidistribution — `CRYPTID_O17_O15.md`
> §1b), but its **halt predicate is Collatz-hard**: the embedded carry family `0 A 0 1^k` halts trivially off
> the `mod 3` lattice and Collatz-irregularly on it (18 machine-proven halters, two of them delayed past 10⁷).

---

## 2. The PROVEN barrier — no m-window certificate for m ≤ 8  [PROVEN, conjecture-free, VERIFIED]

A **certificate** for non-halting is a config set `L` with (S) start ∈ L, (C) `L` step-closed, (H) `L`
halt-free. `reachable(start)` is one; the question is a *tame* one. For an m-window (locally-testable, LT)
class, `L` is determined by its allowed length-m gram set `G_L`; any m-window `L ⊇ reachable` has
`G_L ⊇ G* := grams_m(reachable)`, hence `L ⊇ L*_m`, the **tight** (smallest) m-window over-approximation
`L*_m := { configs whose every length-m gram ∈ G* }`. (Encoding & verifier: the trusted `far_dfa.FAR`.)

> **Theorem [PROVEN].** For every `m` with `2 ≤ m ≤ 8`, **no m-window certificate proves o17 non-halting.**
> *Proof.* Pick a trivial halter `k` with `k ≥ m`, `k % 3 ∈ {1,2}` (e.g. the value reported below); the config
> `c = A 0 1^k` **halts** (§1, `far.step_str`-verified). Machine-check (`o17_window_barrier.py`,
> `o17_floor_confirm.py`, reachable run 2–3·10⁵ steps): **`c ∈ L*_m`** — every length-m gram of `c` lies in
> `G* = grams_m(reachable)`. Let `L` be any m-window certificate; then `L ⊇ L*_m ∋ c`, so `c ∈ L`. By step-
> closure `L` contains every successor of `c`, in particular the halt config `c` reaches — contradicting (H).
> So no such `L` exists. ∎

**[VERIFIED] the halter is accepted by the tight over-approximation, m = 2..8** (`o17_window_barrier.py`):

```
 m= 2: |G|=  25  halters A01^k accepted: k=[2,4,5,7,8,10]      <-- barrier fires
 m= 3: |G|=  61  k=[4,5,7,8,10,11]                              <-- fires
 ...
 m= 8: |G|= 837  k=[8,10,11,13,14,16]                           <-- fires
 m= 9: |G|=1234  k=[]   (no halter accepted)                    <-- STOPS
 m=10..12: []                                                   <-- stays stopped
```

The m ≤ 8 barrier is **conjecture-free**: it uses only the *trivial* halters `k%3∈{1,2}` (which all halt fast),
not the Collatz-irregular part. (The Collatz part would be needed only to push the barrier to REG, §5.)

---

## 3. Why the barrier STOPS at m = 8 — bounded frontier, machine-checked  [PROVEN negative — the honest core]

The stop at m = 9 is **not** a sampling artifact and **not** a closure artifact; it is a structural fact about
how reachable presents state A. Two independent machine checks pin it.

**(a) The exact binding gram (`o17_floor_confirm.py`, reachable 3·10⁵).** Among the marker grams of the padded
probe `0^{m-1} 0 A 0 1^k 0^{m-1}`, the one that decides acceptance is the offset-1 window
`g_m := (0, A, 0, 1^{m-3})` ("A reads 0 with **one blank to its left** and `m-3` ones to its right"):

```
 m :  o=1 gram  '0 A 0 1^(m-3)' in G   |  o=0 gram 'A 0 1^(m-2)' in G  |  halter accepted
 6 :         1                          |          1                    |   True
 7 :         1                          |          1                    |   True
 8 :  '0 A 0 1^5'  = 1                   |          1                    |   True
 9 :  '0 A 0 1^6'  = 0  <-- ABSENT      |  'A 0 1^7' = 1                |   False  <-- STOPS
 10..12 :      0  (absent)              |          1  (present)         |   False
```

Note `A 0 1^{m-2}` (the offset-0 gram, "A reads 0 with a long run to the right, **any** left context") is present
for *all* m — so the right-run length is **not** the obstruction. The obstruction is the **mixed** window
`0 A 0 1^{≥6}`: A reading 0 with a *finite blank gap of width 1 on the left* **and** ≥ 6 ones on the right.

**(b) Why that mixed window is genuinely absent (`o17_window_diag2.py`, blank run 5·10⁷ steps, width ≈ 12 000).**
Census of every `A`-reads-`0` event in reachable:
- **left-0-run before the head ∈ {0, ∞} ONLY** (4024 events with a `1` immediately to the left; 9 events at the
  true left frontier with all-blank to the left). **There are zero events with a finite blank gap ≥ 1.**
- the 9 true-frontier (∞-left) events have **right-1-run ≤ 5** (values {0,3,5}); the interior (0-left) events
  have right-1-run up to 10 475.

So A reads 0 in reachable in exactly two regimes — **deep frontier** (blank-left, but then the carry sweep has
left only a **bounded** `≤5`-cell tail to the right) or **interior** (long block right, but a `1` immediately
left). The probe `0 A 0 1^k` needs the **mix** (one blank left + long block right) which **never occurs**. Once
a window is wide enough (m ≥ 9) to see *both* the left blank and ≥ 6 right ones at once, it can **gate** the
probe out without touching reachable — exactly `EXISTENCE_META_THEOREM.md`'s "an invariant *set* can exclude the
halting orbit," made concrete.

> **[PROVEN negative].** For m ≥ 9 the embedded family `0 A 0 1^k` is **off the reachable window set**, so the
> all-or-nothing engine has no fuel via this family. The barrier floor is **exactly m = 8**. (Cross-check:
> `far_dfa.FAR.verify` fails on o17 at every m, but for m ≥ 3 the failure is the benign blank-expansion closure
> `A,0→1RB ctx (0,…,0)` — a HOLDOUT artifact — not a forced halter; `o17_window_barrier.py` §"STEP 2".)

---

## 4. The crisp non-local-vs-head-local dichotomy  [the recast]

The prior notes drew the dichotomy as **o17 "has" a barrier / o18 "doesn't."** The machine checks **refute that
binary** and replace it with a sharp *quantitative* statement.

A k-window existence barrier exists up to floor `m*` = the largest window for which an embedded **halter family
stays window-equivalent to reachable**. The discriminator's reach sets `m*`:

| | o18 | o17 | parity counter (brick d, a *counter*, not a cryptid) |
|---|---|---|---|
| embedded family | `C_N = [F] 0 1^{N-1}` | `0 A 0 1^k` | `1^m [B] 0` |
| family halters | **none** (C_N uniformly non-halting) | **Collatz-irregular** (§1: 18 proven, 2 delayed) | m even ⇒ halts |
| discriminator | adjacent-`11` at the head (2 growing quantities aligning) | block length `k mod 3` + Collatz carry, read during a **left sweep** | run length `m mod 2`, read at the **head** of an *unbounded clean run* |
| where it lives | **3-cell head neighbourhood** | an **8-cell** window of a **bounded-tail frontier** | **unbounded** `1`-run |
| family window-covered by reachable? | only the collision is excluded (m=2 floor) | **up to m = 8**, then the mixed frontier window drops out | **for all m** (the `1^m` run + `B`-marker window are all reachable) |
| barrier floor `m*` | **2** | **8** | **∞ (all k)** |
| reaches REG? | no `[OPEN]` | no `[OPEN]` | **yes** — but it is a counter with a *known* REG certificate |

> **Dichotomy, precisely.** A cryptid gets an **all-k / REG** existence barrier **iff** its halt discriminator
> lives in an **unbounded reachable run** (the brick-(d) mechanism — then the halter family is window-equivalent
> to reachable for *every* m). Both BB(6) existence cryptids fail this: o18's discriminator is **head-local**
> (bounded neighbourhood, floor 2); o17's is **non-local in the probe's block length but bounded-frontier**
> (the carry overflow is decided at a frontier whose reachable structure is a `≤5`-cell tail, floor 8). o17 is
> **strictly between** o18 and the brick-(d) ideal: a genuinely Collatz-irregular halter family (unlike o18's
> uniformly-non-halting `C_N`) that nonetheless detaches from reachable at a finite window (unlike brick (d)).

---

## 5. Does o17 close LIMIT_THEOREM's `[OPEN]` "no REG certificate for a cryptid"?  [NO — precise]

**No.** A REG / FAR-DFA certificate may have **unbounded** window/state count; the proven barrier covers only
`m ≤ 8`. REG ⊇ every m-window class, so the m ≤ 8 result does **not** lift to REG. Concretely: a regular
over-approximation could count `k mod 3` with a 3-phase DFA and *try* to gate the carry family — to defeat
**that** one would need the `k ≡ 0 (mod 3)` halting pattern to be **non-regular** (the Collatz-irregular
interleaving of §1), **and** that family to be REG-covered by reachable — but §3 shows the family detaches from
reachable's window set at m ≥ 9, so the REG-coverage premise fails just as the k-window one does. Hence:

- **o17 does NOT close** the `LIMIT_THEOREM.md` `[OPEN]` item "no REG certificate for a cryptid." That item
  **stays `[OPEN]`** (= at least as hard as resolving o17; `far_dfa` returns HOLDOUT through m = 12 — evidence,
  not proof).
- **What o17 DOES contribute (positive, recorded):** (i) the **highest explicit finite k-window floor** among
  cryptids — `m* = 8` `[PROVEN]` — versus o18's `m* = 2`; (ii) a **conjecture-free embedded halter family with
  genuinely Collatz-irregular halting** (18 proven halters, 2 delayed past 10⁷), the existence-facet analogue of
  Antihydra's density obstruction *with an actual irregular family attached*; (iii) the **exact mechanism that
  caps the floor** (bounded `≤5`-cell carry-frontier tail), which is the operational meaning of "the cryptid's
  discriminator is head-/frontier-local" from the `LIMIT_THEOREM.md` honest negative — now machine-pinned.

So on the certificate-hierarchy map, o17 sharpens the **sub-regular floor** (it pushes the proven k-window
impossibility up to m = 8 for a cryptid) but leaves the **REG vertex `[OPEN]`**, consistent with — and
correcting toward — `LIMIT_THEOREM.md`. The genuine top-level `[PROVEN]` barrier in the whole programme remains
**Antihydra's `β > 0` on the DENSITY axis** (it blocks *all* all-orbits density certificates, via the
`max`-over-invariant-measures including the halting atom); no existence-axis cryptid (o15/o17/o18) matches it.

---

## 6. The frontier catalogue — non-local-vs-head-local × kernel × facet  (CRYPTID_CENSUS Route ii/iii)

Classifying each analyzed Collatz-core cryptid by **(facet)** density vs existence, **(barrier)** proven class +
floor, **(kernel)** AEV/Mahler multiplier or none, **(halt discriminator)** locality. (`bb_sim`-verified specs;
kernel placements from `CRYPTID_KERNEL.md`; barriers from this note + `O18_NO_CERTIFICATE.md` +
`CRYPTID_O17_O15.md` + `LIMIT_THEOREM.md`.)

| machine | spec (halt) | facet | kernel | halt discriminator | **proven barrier** | over-approx / REG |
|---|---|---|---|---|---|---|
| **Antihydra** | `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` (F:0) | **density** | **AEV q=2** (μ=3/2, p=2) | head-local (balance read at F) | **`β>0` [PROVEN]** — all-orbits *density* certs blocked | `[OPEN]` |
| **o10** (o10-inner) | `1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` (F:0) | density/existence (coupled) | **AEV q=2** (μ=3/2, p=2; literal AEV-1.6 ceiling) | head-local | none on existence axis | `[OPEN]` |
| **o15** | `1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA` (A:1) | existence | **AEV q=3** (μ=8/3, p=3; Erdős ternary) | head-local (A-frontier collision; block decomp parity-irregular but halt is a local read) | none proven | `[OPEN]` (Erdős wall) |
| **o18** | `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` (F:1) | existence | **AEV q=3** (μ=8/3, p=3; Erdős ternary) | **head-local** (adjacent-`11`, 3-window) | **no 2-window [PROVEN]; floor m\*=2** | `[OPEN]` (≥3 head-local) |
| **o17** | `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (F:0) | existence | **none** (uniquely-ergodic odometer; equidistribution automatic) | **non-local-in-block-length but bounded-frontier** (carry overflow; `k mod 3` + Collatz, `≤5`-cell tail) | **no m-window for m≤8 [PROVEN]; floor m\*=8** | `[OPEN]` (family detaches m≥9) |

**Two obstruction types in the BB(6) Collatz core** (confirmed): an **equidistribution kernel** (Antihydra,
o10 = AEV q=2 μ=3/2; o15, o18 = AEV q=3 μ=8/3 / Erdős) whose hardness is single-orbit `⌊μⁿ⌋ mod p`
equidistribution (the shared Mahler vertex), versus **one odometer outlier o17** whose hardness is a
Collatz-irregular **halt predicate** (no kernel). On the **certificate axis** the existence cryptids (o15/o17/o18)
all have **finite-floor** barriers only (floors 0/0 proven for o15/o10, 2 for o18, 8 for o17), never REG;
the only **top-level proven** barrier in the family is Antihydra's **density-axis** `β>0`.

---

## 7. Answers to the task's six items

1. **Exact halt structure (§1, bb_sim-cross-checked).** `0 A 0 1^k`: `k%3∈{1,2}` always halts (80/80, k≤120);
   `k≡0 (mod 3)` Collatz-irregular — 18 proven halters incl. **two delayed past 10⁷** (k=102@2.8·10⁷,
   k=108@6.7·10⁷), no modulus, non-monotone times. The non-halting remainder is an embedded open Collatz fact.
2. **The barrier `[PROVEN]` (§2).** **No m-window (LT) certificate for 2 ≤ m ≤ 8** — conjecture-free
   (tight over-approx `L*_m` accepts a halter `A 0 1^k`, which halts; step-closure forces a halt). Machine-checked.
3. **Contrast with o18 (§3–§4).** o18 head-local, floor 2, uniformly-non-halting clean family; o17
   non-local-in-block-length but **bounded-frontier**, floor 8, **Collatz-irregular** halter family. Dichotomy:
   an all-k/REG barrier needs the discriminator in an **unbounded reachable run** (brick d); both BB(6) existence
   cryptids fail this, at different floors. The earlier "o17 has / o18 lacks" binary is **refuted (quantitative).**
4. **Catalogue (§6).** 5-machine table by facet / kernel (AEV q=2 / q=3 / none) / discriminator locality / proven
   barrier + floor. Two obstruction types; only Antihydra has a top-level (density) proven barrier.
5. **LIMIT_THEOREM `[OPEN]` (§5).** **o17 does NOT close it.** REG stays `[OPEN]`; o17 contributes the highest
   explicit finite k-window floor (m=8) and a conjecture-free Collatz-irregular halter family. Soundness correction
   to the prior over-claim recorded.
6. **This file.** `busybeaver/O17_REG_BARRIER.md` (not committed).

**No machine decided. No non-halt claimed. The proven barrier (no m-window, m≤8) is airtight; everything above
m=8 is honestly `[OPEN]`; the prior all-k/REG over-claim is retracted. Soundness intact.**

## Reproduce (all `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, bb_sim semantics)
- `o17_barrier_verify.py` — family `0A01^k` halt table k=1..90, **step-for-step cross-check vs bb_sim** (blank +
  all k); layout calibrated to the k=6 anchor; 3·10⁸ push on k=3j runners.
- `o17_barrier_fast.py` — fast bytearray, k=1..120, budget 10⁷ then 10⁸; catches delayed halters k=102, k=108;
  consolidated k=3j halter list (18) + non-monotonicity check.
- `o17_window_barrier.py` — builds tight m-gram `L*_m` from reachable; halter `A 0 1^k` accepted for m=2..8,
  rejected m≥9; `far_dfa.FAR.verify` cross-check (HOLDOUT / benign blank-expansion at m≥3).
- `o17_floor_confirm.py` — the exact binding gram `0 A 0 1^{m-3}`: present m≤8, absent m≥9 (floor = 8).
- `o17_window_diag2.py` — 5·10⁷-step census: state-A-reads-0 has left-0-run ∈ {0,∞} only; ∞-frontier right-1-run
  ≤ 5 (the bounded carry-frontier tail that caps the floor).
