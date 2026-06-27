# The minimal open kernel of Antihydra (BB(6)) — one page for an external reader
> **We found a reduction and an obstruction map. Can your tools reach this kernel?**
*A single proposition whose proof would decide the Busy-Beaver machine "Antihydra". Stated so that a
specialist can judge in minutes whether their tools apply. We are NOT claiming a solution and NOT claiming
new mathematics is provably required; we present a reduction and the precise place where known methods, as
far as we have found, stop. All [PROVEN] items are machine-checked in exact integer/2-adic arithmetic.*

## Setup (3 lines)
Integer orbit `c_{n+1} = ⌊3 c_n / 2⌋`, `c_0 = 8` (so `c_n = ⌊8·(3/2)^n⌋`-type, `c_n ∼ A·(3/2)^n`).
Let `E_n = #{ i<n : c_i even }`. **[PROVEN]** The Turing machine *Antihydra* never halts **iff**
`3E_n − n ≥ 0` for all `n`, i.e. the running even-density `E_n/n ≥ 1/3`. (Conjecturally `→ 1/2`.)

## The kernel (the minimal open proposition)
> **(K)** For this single specified orbit, the empirical distribution of `c_n mod 2^k` converges to
> uniform for each fixed `k` — equivalently, the **moving diagonal binary digit** `b_n = ⌊8·3^n/2^n⌋ mod 2`
> (`= bit_{n−3}(3^n)`) has asymptotic density `1/2` (i.e. the induced binary sequence is *simply normal*; the
> mod-`2^k` form for all `k` is full equidistribution).

Proving (K) — in fact merely keeping the even-density `≥ 1/3` — decides Antihydra. (K) is the equidistribution
of `{(3/2)^n}`-type data, the family of **Mahler's 3/2 problem (1968)**; the base-`3/2` instance of the normality
conjecture of **Andrieu, Eliahou & Vivion, "A Normality Conjecture on Rational Base Number Systems"
(arXiv:2510.11723, 2025)** — who conjecture that "every minimal and maximal word is normal over an appropriate
subalphabet", and note implications for the existence of `Z`-numbers (Mahler 1968), `Z_{p/q}`-numbers (Flatto
1992), and the Dubickas–Mossinghoff "4/3 problem" (2009). *(All a recognized open frontier.)*

## A strictly weaker *sufficient* form (so you can aim lower)
**[PROVEN reduction]** Non-halting follows from: *for some `δ>0` and `C`, the character sum
`|Σ_{n<N} ψ(c_n)| ≤ C N^{1−δ}` for every nontrivial Dirichlet character `ψ` of low 2-power conductor
(`≤ N^δ`).* Any power saving `δ>0` at low moduli suffices (via an explicit `δ→margin` map). *(Caveat:
we believe this is a genuinely weaker target but plausibly the same difficulty class — the leading
`conductor-4` term is already the moving-middle-digit.)*

## Where known methods stop (as far as we have found)
(K) is the equidistribution of a **single specified orbit of a rank-1 expanding ("amenable-hyperbolic")
map** `×(3/2)` on `ℤ_2`. The recurring obstacle is the **a.e. → specified** gap. In the existing
vocabulary, the obstacle is a **closed-loop identification bias**: the digit we must control is generated
by the very dynamics we would use to control it, so the natural surrogate (an i.i.d./shuffled "annealed"
copy) is solvable while the real "quenched" single realization is not — the structure of a **self-induced
quenched disorder** (deterministic-spin-glass / merit-factor type).
- **Fourier / Weyl / Gowers / van der Corput:** the differencing operator fixes `(3/2)^n` at every degree
  (no degree reduction); these reach only the top `Θ(log N)` digits. The relevant machinery is the
  **Mauduit–Rivat carry lemma + Gowers-norm** analysis for digits of multiplicatively-structured
  sequences — it controls a digit correlated with *bounded* carry, but here the target digit is a
  carry-sum of the **entire** parity history.
- **Transfer-operator spectral gap:** controls the orbit only at the **Haar / a.e.** level (decay of
  correlations, via Lasota–Yorke / Keller–Liverani); we have not found a way to descend it to the
  specified algebraic orbit (the per-scale **injection** term, not the contraction, is the wall).
- **Measure rigidity (×2,×3 / Furstenberg–Rudolph–EKL):** needs a second multiplicatively-independent map
  (rank ≥ 2); `×(3/2)` is self-dual (rank 1).
- **p-adic Baker / S-units:** the orbit terms `c_n=(3^n c_0−T_n)/2^n` have height `≈ n·log_2 3`, **unbounded**.
- **Sarnak–Möbius / automatic-sequence normality:** need *zero* topological entropy; the orbit's binary
  sequence is **measured** to have high/near-full subword complexity (consistent with positive entropy), so it
  does not appear to be a zero-entropy/automatic sequence. In effective-ergodic-theory terms the orbit is
  **computable** (hence never Martin-Löf random), so a.e./genericity theorems exclude it by construction —
  the same wall as **open normality** of `π`, `e` (finite-state dimension).
- **Closest *unconditional digit* result:** **Drmota–Spiegelhofer (arXiv:2501.00850, 2025)** prove, via
  Schlickewei's *p*-adic Subspace Theorem, that the longest equal-bit block of `3^n` is `o(n)`. This is
  the strongest unconditional statement we found about the actual digits of `3^n`. It does **not** transfer
  to the orbit: the orbit's relevant integer is **not** `3^n` but `8·3^n − T_n`, where `T_n` is the
  parity-history **carry-sum** (`T_n ≡ 8·3^n mod 2^n` by integrality; height `≈ n·log_2 3`); the longest
  even-run `= v_2(8·3^n − T_n) − n`. The Subspace Theorem controls an `S`-unit / pure power; `T_n` is a
  self-generated carry-sum, not of that form — so the tool stops **exactly at `T_n`** (the closed-loop
  term). *(Verified: orbit ≠ `⌊8·(3/2)^n⌋`; `T_n` congruence machine-checked; the orbit's longest run is
  empirically `≈ log_2 n`, far below the provable `o(n)`.)*
- **Closest positive result:** **Tao (2019, Forum Math Pi)** controls the *same* 3-adic skew-random-walk
  statistic, but for a **log-density-1 set of seeds**; we do not currently know a method descending it to
  one specified seed.

## Two empirical anchors (measured, not proven)
- The orbit is statistically indistinguishable from i.i.d. fair coins at every finite order tested
  (mod-`2^k` discrepancy at the CLT rate; lag-mutual-information `≈0`; full block entropy; passes a
  **next-bit test** on every handle we tried). So no finite-order / elementary statistic separates it
  from a "random" sequence.
- Conditioning the moving-middle digit on the controllable data — the top digits (`{n log_2 3}`, even
  deep into the continued fraction) or the low 2-adic digits — shows **no measurable bias** (operator
  norm at the noise floor). So we have not found a *handle*: the controllable ends do not predict the
  middle digit, in our measurements. (The annealed / shuffled-**surrogate** copy *is* tractable — the gap
  between surrogate and real orbit is exactly the closed-loop bias above.)

## The question for you
Does your toolbox give **effective equidistribution (or any one-sided density bound) for a single
specified orbit** of a rank-1 expanding `p`-adic / `⌊(p/q)·⌋` map — possibly from a Diophantine input on
`log_2 3` — or a precise reason it cannot? Equivalently: can you control a **self-induced quenched
disorder** (a deterministic sequence whose disorder is generated by its own dynamics) below the annealed
surrogate — i.e. break the **closed-loop identification bias** for one realization? We would value most a
pointer to a near-miss, a known obstruction we have overlooked, or a field (symbolic dynamics, p-adic
harmonic analysis, random dynamical systems, additive combinatorics, **statistical physics of
self-induced disorder / low-autocorrelation binary sequences**) where an isomorphic "specified-orbit
genericity" notion lives. A sharp "no, because …" is as useful to us as a "yes, see X."

*(Fuller context, the reduction chain, and the per-method obstruction map are available on request;
this page is the kernel.)*
