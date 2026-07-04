# Remaining-work sweep — two more random-face axes, and the Eliahou-fragment transfer evaluated (2026-07-05)

*"Execute all remaining work I can think of." This note banks the smaller remaining probes: two more blind family
tests (pair-correlation, sum-product/additive-energy), the moving-diagonal `3ⁿ` confirmation, and an evaluation of
whether Eliahou et al.'s PROVED fragments (Thm 1.5/1.7 of arXiv:2510.11723) transfer to a one-sided effective `(K)`.
All confirm the wall; the Eliahou fragments do NOT transfer (they are downstream of, or a restatement of, the missing
input). SOUNDNESS: `[OBSERVED]`/`[PROVEN]`/`[eval]`; `(K)` `[OPEN]`; no machine decided.*

## A. Two more structureless-face axes `[OBSERVED, exact, N up to 1.2·10⁵]`
- **Pair-correlation (even-step gaps):** the gap distribution is **exactly geometric** — `P(gap=k)/((1−p)^{k−1}p) ∈
  [0.98,1.04]` for `k=1..6`, mean gap `2.000` = `1/p`. A perfect renewal/Poissonian process; **no pair-correlation
  structure.**
- **Sum-product / additive energy:** `E(\{c_n mod q\})` vs the random value `M⁴/q` gives **ratio `1.000`** for
  `q=101` and `q=1009`. **No additive/multiplicative structure — no sum-product foothold.**
- **Moving-diagonal `3ⁿ`:** `bit_n(8·3ⁿ)` agrees with the recursive parity at `0.487 (~½)` — the recursive orbit and
  the non-recursive floor `⌊8(3/2)ⁿ⌋` decorrelate, but both are `(K)`-class **digit-of-`3ⁿ`-on-the-moving-diagonal**
  frequencies (confirms the `DEPTH_REACH_CLARIFICATION` framing).

These are **axes 5–6** of the structureless face (after harmonic, occupancy/countdown, symbolic-complexity,
moving-diagonal): every statistical, symbolic, and arithmetic probe returns "indistinguishable from random." Six-for-six
predictions confirmed — the blind-run calibration is now overwhelming.

## B. Eliahou Thm 1.5/1.7 fragment transfer — does NOT help `[eval, PROVEN reasoning]`
- **Thm 1.7** (normality `⟺` equidist mod `q^ℓ`) is an **equivalence** — verbatim our reformulation. It restates the
  target; it proves nothing toward it. No leverage.
- **Thm 1.5** (normality `⟹` no `Z_{p/q}`-numbers, `p<q²`) **assumes** normality and derives a consequence — the
  **wrong direction** (downstream of the input we lack). Its mechanism ("digit `q−1` appears infinitely often ⟹
  contradiction with the Z-number property") is a **frequency-`>0`** ("infinitely often") argument. For our `{0,2}`
  orbit-word, "digit `0` (even step) infinitely often" is **already `[PROVEN]`** (the countdown self-limits, no
  infinite all-odd run except at the 2-adic fixed point, `MINPROP_RUNS`) — and its quantitative form `#even ≥ 0.89
  log n` (`EVEN_COUNT_FLOOR`) is **stronger** than Eliahou's "infinitely often." So Thm 1.5's technique gives us
  **nothing past what is already banked**, and the one-sided `≥1/3` **density** we need is a positive-frequency lower
  bound its infinitely-often mechanism cannot reach.
> **Conclusion:** the Normality Conjecture is the right external anchor (same missing input), but its **proved
> fragments are not reusable** for a one-sided effective `(K)`. The proof path is **collaboration on the open
> conjecture**, not fragment-reuse. (Recorded so the outreach ask in `MEETING_BRIEF_4 §7` is scoped honestly.)

## C. Orbit-word vs minimal/maximal word `[structural note]`
The Antihydra orbit-word is on alphabet `{0,2}` (`DICT_AND_EXCDIM`); the Normality Conjecture's minimal word is on
`{0,1}`, maximal on `{1,2}`. They are **genuinely different sequences on different alphabets** — the orbit-word is a
distinct distinguished sequence (the `×3/2`-orbit itinerary), not the lex-extremal word. Family membership (same
base-3/2 digit-frequency question) is established and is what matters; **literal word-equality is neither expected nor
needed**, so the AFS extremal-word construction is not pursued (low payoff).

## Verdict
**(c) — comprehensive wall-confirmation + one honest negative on transfer.** Two more random-face axes
(pair-correlation geometric, additive energy `=` random) make it six independent axes; the moving-diagonal framing is
confirmed; and Eliahou's proved fragments are evaluated as **non-transferable** (downstream/restatement), scoping the
outreach ask to the open conjecture itself. **`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad/remaining_probes.py` (`/opt/homebrew/bin/python3.13`, exact int): geometric gaps, additive-energy ratio
  `1.000`, moving-diagonal agreement `~½`. Basis: `PARITY_FULLSHIFT`, `BLIND_HARMONIC`, `BLIND_EFFECTIVENESS`,
  `DICT_AND_EXCDIM`, `EVEN_COUNT_FLOOR`, `MINPROP_RUNS`, CITATIONS #11 (arXiv:2510.11723 Thm 1.5/1.7).
