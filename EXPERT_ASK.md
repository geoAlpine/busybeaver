# A single-orbit equidistribution question (2-adic, rank-1) — short expert ask
*One page. A specialist should be able to answer the boxed question yes/no/"closest known result" without
reading anything else. Fuller context: `STATE_FOR_REVIEW.md`; all assertions below are machine-verified (exact
integer/2-adic arithmetic) or labelled measured/open.*

## The setup (3 sentences)
For the integer orbit `c_{n+1} = ⌊3 c_n / 2⌋`, `c_0 = 8`, let `E_n = #{i<n : c_i even}`. The Turing machine
"Antihydra" (a BB(6) holdout) never halts **iff the running even-density `E_n/n ≥ 1/3` for all `n`**
(equivalently `3E_n − n ≥ 0 ∀n`); conjecturally the density → 1/2. Deciding this is in the class of **Mahler's
3/2 problem (1968)** — we are *not* asking you to solve that, but to locate the precise residue below.

## What reduces to what (verified)
Take the renewal subsequence `c'_j = c/2` at even steps. The induced map `F(c') = ⌊3c'/2⌋`-type acts on `ℤ₂`
and is **full-branch, piecewise-affine, expanding, Haar-preserving** (a Gibbs–Markov map): on
`P_D = {v2(3c'−1)=D}`, `F(c') = (3^{D+1}c' − 3^D + 2^D)/2^{D+1}`, slope `(3/2)^{D+1}`, zero distortion, each
branch onto all of `ℤ₂`. We verified the **exact identity** `Σ_{j<J} v2(3c'_j−1) = #odd steps`, so with
`avg jump := (1/J)Σ_{j<J} v2(3c'_j−1)`:
```
even-density = 1/(1 + avg jump),   and the non-halt criterion is exactly   avg jump ≤ 2.
```
Haar gives `avg jump = 1`. So non-halt ⟺ **the single orbit's empirical measure puts the right (Haar) mass on
the low cylinders** — concretely `(1/J)Σ_j 1[c'_j ≡ r mod 2^k] → 2^{−k}` enough that `Σ_k N_k ≤ 2J`.

## What we have already ruled out (so you can skip these)
- **The transfer-operator spectral gap alone does not suffice.** It is a property of `(F, Haar)` only
  (orbit-blind); `F` has fixed points on every branch (`0, 1/5, 5/19, 19/65, …`, exact 2-adic integers) and
  periodic points of all periods, which violate the needed visit-count bound. (Verified.)
- **Non-shadowing / "spread out" does not suffice.** We *construct* (full-branch coding + inverse branches) an
  orbit that is dense in `ℤ₂`, fully supported, aperiodic — maximally non-shadowing — yet `avg jump = 3.10 > 2`.
  So the condition must pin the empirical measure to **Haar specifically**, not merely "non-concentrated."
- **Growth/counting is circular.** The telescoping `2c'_{j+1}−1 = (3/2)^{D_j}(3c'_j−1)` gives
  `log b_J = log(3/2)(J + Σ D_j) + O(1)`, but independently `n = #even+#odd = J + Σ D_j` — the same identity, so
  `Σ D_j` cancels and yields no inequality. (Verified.)
- **Standard single-orbit-equidistribution mechanisms are unavailable:** unique ergodicity (F has a continuum of
  invariant measures), rank-≥2 measure rigidity (the orbit is rank 1, one map `×3/2`), Weyl/van der Corput
  (closed on the multiplicative recurrence `(3/2)^n`).

## The question
> **Q0 (the complete-proof frontier — ask this first).** Non-halting needs only the **one-sided** bound
> `avg jump ≤ 2` (running), where `avg jump = (1/J)Σ_j v2(c'_j − 1/3)` is the orbit's average 2-adic proximity
> to the single point `1/3 ∈ ℤ₂` — equivalently a **one-sided shrinking-target / recurrence estimate**
> `N_k/J ≤ C·2^{−k}` (visit frequency to the shrinking ball `2^{−k}` around `1/3`) summing to `≤ 2`. The true
> value is `≈ 1` (a **factor-2 margin**) and the condition is *strictly weaker* than equidistribution (we
> exhibit non-Haar orbits with `avg jump ∈ (1,2)`). The whole difficulty localizes to **small `k` (`k=2,3`,
> i.e. the orbit's frequency mod `4` and mod `8`)** — the large-`k` tail is a separable p-adic-Baker target
> (Q2). Crucially the bound is **seed-universal**: every natural integer seed gives `avg jump ≈ 1`, `N_2/J ≈
> 0.25`, `N_3/J ≈ 0.125` (spread `< 1%`); seed 8 is not special — so the obstruction is a property of the *map*,
> not a seed pathology.
> **The question:** *Does any known technique **distinguish** a one-sided shrinking-target / recurrence bound
> from full equidistribution for a single orbit of a rank-1 expanding map?* I.e. is there a setting where the
> one-sided (margin) bound is **provably attainable while equidistribution is open** (a separating example), or
> a theorem that the two are **equivalent in difficulty**? Concretely: any *one-sided recurrence / shrinking-
> target estimate*, sub-additivity, or Lyapunov/drift on the renewal map bounding visit frequency to a fixed
> small cylinder *from one side* without proving the exact frequency. **This decides whether a complete proof is
> reachable without Mahler 3/2.**
>
> **Q1 (the equidistribution wall, if Q0 is "equivalent in difficulty").** Is there *any* mechanism in the literature that forces a **single** rank-1 orbit of an
> expanding `×(2^a/3^b)`-type Gibbs–Markov map on `ℤ_p` to equidistribute (empirical measure → Haar), given a
> **Diophantine input on `log₂3`** — beyond the rank-≥2 scope of Furstenberg/Rudolph/Lindenstrauss and beyond
> the off-diagonal reach of Fourier/large-sieve? If not, what is the **closest** known result and the exact gap?
>
> **Q2 (fallback, possibly easier).** Independently of Q1: the *large-k* part of the obstruction is an
> anti-clustering / separation bound on orbit differences, `#{(i,j): v2(c'_i − c'_j) ≥ k} = O(J²/2^k)`. The
> differences are S-unit-like. Does **p-adic Baker / linear forms in logarithms** give an unconditional lower
> bound on `v2(c'_i − c'_j)` (hence the separation bound)? (Note: this tail is *not* what binds `avg jump` — the
> small-k equidistribution is — but a clean unconditional result here would still be a genuine partial.)

**Expected answer format.** A useful reply could be (i) a reference showing the one-sided/equidistribution
distinction is known or *impossible* in this setting; (ii) a counterexample / argument explaining why the
one-sided shrinking-target bound is *as hard as* equidistribution here; or (iii) a technique that plausibly
attacks the small-`k` shrinking-target estimate directly. A pointer ("see X, Y") is plenty — no write-up needed.

## Why this is well-posed (not "please solve Mahler")
The point of the reduction is that the obstruction is now **localized**: it is exactly *single-orbit empirical
measure → Haar at the low cylinders* of an explicit Gibbs–Markov map, with every soft/elementary route
explicitly closed. A "no, that needs full equidistribution" is as useful to us as a "yes, see X." Either pins
the next move.

## Where to ask
- **bbchallenge community** (the Antihydra holdout is theirs): Discord / forum threads, contributors working on
  cryptids. They have the exact same reduction and will know of any partial result.
- **An ergodic-theory specialist** in the Gibbs–Markov / transfer-operator (Aaronson–Denker) tradition, or in
  effective equidistribution / `×2 ×3` dynamics — Q1 is squarely theirs.
- **An analytic number theorist** (linear forms in logarithms / S-unit equations) — Q2 is squarely theirs.
- **MathOverflow** with tags `ergodic-theory`, `equidistribution`, `p-adic-analysis`, `nt.number-theory` — Q1
  and Q2 are each a clean self-contained MO question.
- **ChatGPT / an LLM as first-pass triage** — to surface candidate theorems and names before spending a human
  expert's attention.
