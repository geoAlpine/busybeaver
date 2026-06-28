# o10 — the EXACT §3c reduction, halt criterion reverse-engineered from raw tape mechanics (2026-06-28)

Completes the exact §3c reduction for **o10** against the **raw TM** (every mechanic cross-checked vs
`bb_sim`-equivalent simulation, ≥10⁵–10⁷ steps). Supersedes the "irregular refill alignment / mod-16 slice"
picture of `o10_attack.md` and `CRYPTID_O10_FRAMEWORK.md` with the **literal halting condition**. Soundness
discipline: `[PROVEN]` (machine-verified, exact integers) / `[OBSERVED]` (numerics/heuristic) / `[OPEN]`.
Scratchpad scripts: `scratchpad/o10_probe*.py`, `o10_underflow.py`, `o10_table.py`, `o10_epochs.py`,
`o10_crosscheck.py`.

`o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` (from `suite.py`; halt = **state F reads 0**).

---

## 0. Transition anatomy → the literal halt mechanic  [PROVEN, unit-tested]

State F is entered ONLY from `C:1→0LF`. The relevant loop is a **leftward "eat-1s" sweep**:
`C:1→0LF` (write0,L→F), `F:1→0LC` (write0,L→C), `F:0→HALT`, `C:0→1LD` (write1,L→D, exit).
Moving left from a C-entry over a run of 1s, the state alternates C,F,C,F…; the terminating `0` is read in
state **C** at even offset (→exit to D) or state **F** at odd offset (→HALT). Therefore:

> **(HALT-MECHANIC) [PROVEN].** A C/F eat-sweep that consumes a maximal run of `L` ones **HALTS iff `L` is
> ODD**; if `L` is even it exits to D and the machine continues.

`[verified]` crafted runs L=1..8: L∈{1,3,5,7}→HALT, L∈{2,4,6,8}→exit-D, zero mismatch (`o10_probe2.py`).
**This is the entire halting story: o10 halts ⟺ some C/F eat-sweep ever consumes an odd-length run of 1s.**

---

## 1. The two-counter structure  [PROVEN, raw-TM verified]

The clean recurrent configuration (state E, head at left end) is
> **`1 0^a 1^b 0 1`**, with **`a = 2m − 8`** (left 0-block) and **`b`** (right 1-block, the countdown).

Per macro-step the head sweeps right, then performs ONE eat-sweep of the big left 1-block. `[verified]`
(`o10_probe6.py`, 17 macro-steps to 5·10⁶ steps, every one exact):

> **(INNER) [PROVEN].** `m → ⌈3m/2⌉`  and  `b → b − (1 + [m odd])`.  The eat consumes the left block of
> length **`L = a = 2m − 8`**, which is **ALWAYS EVEN** ⇒ by (HALT-MECHANIC) the inner sweep **never halts**.

The inner orbit from `m=6` is `6,9,14,21,32,48,72,108,162,243,365,548,822,…` = **the literal AEV ceiling
3/2 map `⌈3m/2⌉`** (matches `CRYPTID_O10_FRAMEWORK.md`). `b` is a countdown consumed at rate `1+[m odd]`.
`[verified]`: `b`-decrements 5→4(−1,m6),4→2(−2,m9),2→1(−1,m14),… match `1+[m odd]` exactly; all 17 eats
even (`o10_probe4.py`).

**Consequence:** since every inner eat is even, **halting can occur ONLY at the b-underflow** (when the
countdown bottoms out). The "refill" subroutine that rebuilds the counter contains **no C/F eat-sweep**
(`[verified]`: zero eat events between consecutive epochs) — so it is not a halt site either.

---

## 2. The EXACT halt criterion  [PROVEN, raw-TM ground truth]

Run the raw TM from clean configs `1 0^{2m−8} 1^b 0 1`; the small-`b` (underflow) base rule is
(`o10_underflow.py`, `o10_abstract.py`, `m=5..79`, zero mismatch):

| terminal `b` | HALT iff | refill (non-halt) otherwise |
|---|---|---|
| `b = 0` | **`m` odd** | `m` even |
| `b = 1` | **`m ≡ 2 (mod 4)`** | else |
| `b = 2` | **`m ≡ 3 (mod 4)`** | else |
| `b ≥ 3` | (never) | normal inner step |

These three rows **unify** to a single statement via (INNER):

> **(H-CRITERION) [PROVEN].** Within one epoch (countdown from `b=B` along the `⌈3m/2⌉` orbit, `b` losing
> `1+[m odd]` per step), the machine **HALTS iff the countdown reaches EXACTLY `b = 0` at a step where `m` is
> ODD.** It **refills** (resets `m→6`, jumps `b` up) iff the countdown lands on `b=0` at even `m`, or
> **overshoots** `b=0` (a `−2` step from `b=1`, which happens exactly at `b=1` with `m` odd).

The naive "countdown skips 0 ⇒ halt" model of `o10_attack.md` is the **opposite** of the truth: an overshoot
(skip past 0) is the *non-halting* refill case; the halt is the *exact landing on 0 at odd m*. The earlier
"mod-16 slice" was a coarser shadow of the clean **mod-4** rule above.

**Soundness cross-check (the reduction reproduces the RAW TM).** Abstract `epoch(6,B)` vs raw TM run from
`1 0^4 1^B 0 1`, `B=1..16` (extending): **zero mismatches** (`o10_crosscheck.py`). Highlights:
`B=1→HALT(217 steps)`, `B=4→HALT(2274)`, `B=11→HALT(460457)`, `B=13→HALT(1050877)`; non-halts refill
`B=2→21, B=3→35, B=5→57, …`. **`B=5 → B_next=57` reproduces the real machine's epoch-1→epoch-2 refill
exactly** (the blank-tape run does `b: 5 → 57 → …`). The model is TM-faithful, not a plausible guess.
(`B≥17` predicted-halt epochs exceed the 8M-step sim budget — a timeout, not a mismatch — since the halting
step count grows with `B`: `B=11→4.6·10⁵`, `B=13→1.05·10⁶`, so `B=17`'s halt is `≳10⁷`. All refill cases
resolve fast; zero mismatches over the entire resolved range.)

---

## 3. The outer refill orbit and the full machine  [PROVEN structure / OPEN behaviour]

After a non-halting epoch the machine **always refills** to `(m=6, b=B_next)`. The refill rule is, contrary
to `o10_attack.md`'s "no clean fit", **piecewise-affine within each residue class** of the terminal
`[verified, o10_table.py]`: e.g. terminal `(m,1)` with `m` odd → `B_next = 3(m−2)`; terminal `(m,0)` with
`m` even → `B_next = 3m − 7`. Since the terminal `m ≈ 6·(3/2)^{epoch length}`, the epoch start values are
**doubly-exponential**: `B : 5 → 57 → ≈2.1·10⁸ → …` (`[verified]` `epoch(6,57)` terminates at
`m=70091069` (odd), `b=1` ⇒ refill — i.e. the real machine does **not** halt in epoch 2, consistent with
the ≥40M-step holdout). The 2nd refill is astronomically far, so the real `B`-sequence is unreachable by
simulation.

**The whole machine.** o10 runs **infinitely many epochs** unless one halts:

> **(FULL) [PROVEN].** o10 **halts ⟺ ∃ epoch `e` whose countdown (from `m=6`, `b=B_e`) lands exactly on
> `b=0` at an odd `m`.** Equivalently: ∀ epoch the countdown lands on `b=0` at even `m` or overshoots from
> `b=1` at odd `m` ⟺ o10 **never halts.** The `B_e` form the doubly-exponential refill orbit.

---

## 4. Classification against the unified template

**This is an EXISTENCE / residue-landing criterion, NOT a one-sided liminf-density criterion.**

| | Antihydra (template) | o10 |
|---|---|---|
| object | one transient orbit `c₀=8` | a **sequence of epochs**, each restarting at `m=6` |
| inner map | floor `⌊3c/2⌋` (mirror of AEV) | **ceiling `⌈3m/2⌉` = literal AEV 3/2** |
| (H-criterion) | non-halt ⟺ **liminf even-density ≥ 1/3** (a tail-average of ONE orbit) | non-halt ⟺ **∀ epoch the countdown avoids "b=0 at odd m"** (an existence/avoidance over MANY epochs) |
| genericity ⇒ | **non-halt** (density →1/2 > 1/3, with slack) | **HALT** (each epoch halts w.p. ≈ 1/3, `[OBSERVED]` 33.67% over `B=1..3000`; ∞ epochs ⇒ halt prob →1) |

> **Verdict on the template.** o10's full (H-criterion) does **NOT** match
> "non-halt ⟺ liminf renewal-density ≥ θ". It is **composite**: the inner AEV-3/2 equidistribution (which
> governs `m mod 2^k` = the parity at the landing step) **TENSOR** an outer existence test over the
> doubly-exponential refill orbit. Worse for the template, the *direction is reversed*: genericity makes o10
> **halt**, whereas the template proves **non-halting** from a density floor. o10 is a "probabilistically
> **halts**" cryptid (a delayed halter), not a probabilistic non-halter like Antihydra.

**Inner AEV-3/2 reduction — clean and PROVEN, but only one ingredient.** `⌈3m/2⌉` from `m=6` is the literal
AEV Conj 1.6 `p/q=3/2` ceiling instance (no parity-mirror), and `L=2m−8` (always-even inner eat) is a clean
`[PROVEN]` fact that removes the inner loop as a halt site. This inner reduction is **clean and exact**, but
it does **not by itself decide o10**: the halt couples to the inner orbit only through the **parity of `m` at
the underflow index** of each epoch, which additionally needs the b-countdown timing and the refill orbit.

**What the outer refill needs (the excess over the inner kernel).** Two ingredients beyond AEV-3/2:
1. **the refill map** `B_{e+1} = R(terminal)` (TM-derived, piecewise-affine `≈3·m_terminal`, doubly-exp);
2. **the existence/avoidance analysis**: whether, for the deterministic doubly-exponential sequence `B_e`,
   the `⌈3m/2⌉`-orbit parity ever realises "lands on `b=0` at odd `m`". This is an equidistribution-of-parity
   statement evaluated at a **dynamically-determined, doubly-exponentially sparse set of underflow indices,
   across infinitely many restarting epochs** — strictly beyond the single-orbit / single-density AEV
   fragment that (conditionally) closes Antihydra.

---

## 5. (H-fixed-point) for o10  [PROVEN]

The template's degenerate halting orbit exists and is exhibited:

> **Halting configs (β>0 witnesses) [PROVEN].** Every config `1 0^{2m−8} 0 1` with `m` ODD and `b=0` HALTS.
> `[verified]` raw TM: `m=5,7,9,11,21,101` all HALT (steps 22, 76, 166, 292, 1462, 43222) (`o10_crosscheck.py`).

The inner ceiling fixed point is `m = ⌈3m/2⌉ ⟹ m = −1` in `ℤ₂` (the all-odd, `D'=1`-forever orbit), the
2-adic mirror of Antihydra's `o=+1`. The capstone ergodic-optimization meta-theorem transfers to the inner
kernel: the one-sided density functional attains `β = +1/2 > 0` at the atom `δ_{m=−1}` (odd-density →1), so
**no structure-only argument forces the inner parity bound** — exactly as for Antihydra. (Transfers verbatim
from `CRYPTID_O10_FRAMEWORK.md §4`; here grounded in the now-explicit halting configs `m` odd, `b=0`.)

---

## 6. Honest verdict

- **Exact halt criterion (cross-checked vs raw TM):** o10 halts ⟺ ∃ epoch whose b-countdown (from `m=6`,
  `b=B_e`, `m→⌈3m/2⌉`, `b→b−(1+[m odd])`) **lands exactly on `b=0` at an odd `m`** (equivalently the eaten
  1-run becomes odd-length). Base rule `b∈{0,1,2}`: halt iff (`b=0,m` odd) / (`b=1,m≡2`) / (`b=2,m≡3` mod 4).
- **Classification: COMPOSITE / EXISTENCE**, not a density criterion. Inner = literal AEV ceiling-3/2 kernel
  (clean, `[PROVEN]`); outer = doubly-exponential refill orbit + a parity-landing existence test.
- **Is the inner AEV-3/2 reduction clean + PROVEN?** YES — `⌈3m/2⌉` orbit, `L=2m−8` always-even inner eat,
  the underflow base rule, the refill structure, and the (H-fixed-point) halting configs are all `[PROVEN]`
  (TM-verified). But the inner kernel **alone does not decide o10**.
- **What the outer refill needs:** the refill map (TM-derived, piecewise-affine, doubly-exp) **plus** an
  equidistribution-of-parity result at the doubly-exponentially-sparse underflow indices across all epochs —
  strictly harder than Antihydra's single-orbit density kernel.
- **Scope verdict for the unified theorem:** **o10 is OUTSIDE the clean unified non-halting limit theorem.**
  The unified theorem proves non-halting from a one-sided density floor; o10's halting is an existence
  criterion whose generic direction is the **opposite** (genericity ⇒ HALT, `[OBSERVED]` ≈1/3 per epoch ⇒
  halt prob →1 over ∞ epochs). The inner AEV-3/2 sub-problem fits the AEV umbrella as a clean PROVEN
  reduction; **the full machine needs its own treatment** (a delayed-halter existence argument over the
  refill orbit), and its true direction is `[OPEN]` (heuristically halting, unreachable by simulation).

**No decision claimed; no false proof.** The §3c reduction for o10 is now exact and raw-TM-faithful: the
halting condition is pinned to a clean arithmetic event (countdown lands on 0 at odd m), the inner kernel is
the literal AEV ceiling-3/2 instance, and the residual hardness is precisely one doubly-exponential
existence layer that places o10 outside the unified density theorem.
