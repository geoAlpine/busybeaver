# Antihydra (BB(6)) non-halting = a one-sided Normality Conjecture on rational base 3/2 — a one-page outreach abstract

*A self-contained statement of the problem and its exact place in the rational-base / Mahler-3/2 literature, for a
number theorist or ergodic theorist (in particular the rational-base-numeration community). Everything below is either
elementary-and-checked or literature-anchored; the one open kernel is stated as open.*

## The problem
The Antihydra Turing machine is the smallest open problem on the Busy Beaver scale: deciding `BB(6)` requires deciding
whether it halts. It does **not** halt iff the following holds `[elementary reduction, PROVEN]`:

> Iterate `H(c)=⌊3c/2⌋` from `c₀=8`. Let `E_n` = number of **even** `c_k` among `k<n`. Then `B_n := 3E_n − n ≥ 0`
> for all `n` — i.e. the even-steps never fall below a `1/3` density (equivalently, the odd-steps never exceed `2/3`).

Numerically the even-density is `≈ 0.4998` to `n=10⁶` (margin `~0.167` above the required `1/3`); `min_n B_n = 0`.

## Exact place in the literature `[verified]`
`⌊3c/2⌋` is the **shift of the rational base `3/2` number system** (Akiyama–Frougny–Sakarovitch 2008). The base-`3/2`
digit `a₀(c)=2c mod 3` read **along the orbit** lives on the alphabet `{0,2}` — digit `1` is arithmetically forbidden
(`⌊3c/2⌋ ≡ 0 mod 3` if `c` even, `≡ 1` if `c` odd, never `≡ 2`) — and **digit-`0` frequency equals exactly the
even-density.** Hence:

> **Antihydra non-halting `⟺` the base-`3/2` orbit-word of seed `8` has digit-`0` frequency `≥ 1/3`** — the **one-sided
> form of the Normality Conjecture on rational base number systems** (Andrieu–Eliahou–Vivion, arXiv:2510.11723, 2025),
> whose Theorem 1.7 is the equivalence "normality `⟺` equidistribution mod `2^ℓ`," and whose full statement (digit
> frequency `= 1/2`) implies our `≥ 1/3` outright.

It is the same family as Mahler's `Z`-numbers (1968), Flatto's `Z_{p/q}` (1992), and the Collatz-inspired `4/3` problem
(Dubickas–Mossinghoff 2009). Dynamically it is **single-orbit equidistribution of `×(3/2)` on the `(2,3)`-solenoid** —
a **rank-1 amenable hyperbolic** action.

## Why it is hard, precisely `[the one open kernel]`
- **The needed statement is single-orbit and effective at exponential depth.** Controlling `B_n≥0` needs the deep
  odd-runs to be `o(0.5n)`; the elementary magnitude ceiling gives only `≤ 0.585n` — a `1.17×` gap that **is** the
  single-orbit residue-avoidance `c_n ≢ 1 mod 2^{0.5n}`. Resolving it needs equidistribution of the moving-diagonal
  digit of `3ⁿ` at depth `Θ(n)` — **exponentially below** any discrepancy horizon (`N` points equidistribute mod at
  most `2^{log₂N}`, a hard counting ceiling).
- **The orbit is "deterministic yet random."** Six independent probes (Weyl sums `~√N`, discrepancy `~N^{-1/2}`,
  correlations at noise floor, geometric occupancy, **full-2-shift** subword complexity, additive energy `=` random)
  all return "indistinguishable from a fair coin" — there is no structure for a structure-based proof to grip, yet the
  single specified orbit still needs certifying.
- **Current tools miss it by design.** Effective single-orbit equidistribution is, in current mathematics, a **rank-≥2
  / positive-entropy** phenomenon (Lindenstrauss school, 2024–25). The `×(3/2)`-solenoid is **rank-1, amenable,
  non-Pisot (⇒ non-sofic)**; the modern `×2×3` frontier (Burton–Panangaden 2024) is itself only *reformulating* (via
  Baumslag–Solitar C\*-algebras). No effective-equidistribution result reaches a rank-1 amenable single orbit.

## The ask
An **effective normality (or one-sided digit-frequency `≥1/3`) rate** for the base-`3/2` orbit-word — equivalently
effective single-orbit equidistribution for `×(3/2)` on the `(2,3)`-solenoid with an exponential moving-diagonal rate.
This would decide Antihydra, and is a direct strengthening of the Normality Conjecture's target. We have verified the
dictionary, the reductions, and (numerically) that every internal/annealed/structural route provably stops short; the
missing input is genuinely new mathematics of exactly the rank-1-amenable / Furstenberg-`×2×3` kind.

*Contact / full materials: the BB(6) frontier program (notes: `MEETING_BRIEF_4`, `CROSSING_STRATEGY`,
`DICT_AND_EXCDIM`, `FRONTIER_LIT`, `CITATIONS`). External: arXiv:2510.11723, 2504.13716, 2410.22701.*
