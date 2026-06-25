# One-sided recurrence vs equidistribution for a single rank-1 *p*-adic orbit — short expert ask

> **Status (2026-06-26):** a first expert consultation judged the formulation **correct** and the problem **genuinely Mahler-class**; the obstruction is *specified-point genericity*, not recurrence. Canonical statement + verdict: `CANONICAL_PROBLEM.md`.
*(framed via its BB(6)/Antihydra instance, but the question is the dynamical one in the title)*
*One page. A specialist should be able to answer the boxed question yes/no/"closest known result" without
reading anything else. Fuller context: `STATE_FOR_REVIEW.md`; all assertions below are machine-verified (exact
integer/2-adic arithmetic) or labelled measured/open.*

> **If you only answer one thing, please answer Q0.**

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
> (Q2). The bound is, **observed across all tested natural integer seeds**, uniform: every such seed gives `avg jump ≈ 1`, `N_2/J ≈
> 0.25`, `N_3/J ≈ 0.125` (spread `< 1%`), so seed 8 is not a special pathology — the difficulty is the standard
> a.e.→specific gap. (This is an observation, not evidence that a structural argument exists; a *universal* one
> provably does not — see "already ruled out" below.)
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

**Already ruled out for Q0 (so you can skip these).** A *universal* (orbit-independent) one-sided certificate —
Foster–Lyapunov drift, sub-additive potential, `V(F(c')) ≤ V(c') − v2(3c'−1) + b` — **cannot** prove
`avg jump ≤ 2`: the bound is *false for some `ℤ₂` orbits* (we construct one with `avg jump = 3.1`), and
telescoping any such `V` along it forces `b ≥ 3.1 > 2`. So any proof must use **seed-specific genericity**; the
live question is whether the *weak one-sided moment* `E_{μ_J}[D] ≤ 2` (margin 2) is provable for seed 8 when
full equidistribution (`E[D] → 1`) is not.

**Expected answer format.** A useful reply could be (i) a reference showing the one-sided/equidistribution
distinction is known or *impossible* in this setting; (ii) a counterexample / argument explaining why the
one-sided shrinking-target bound is *as hard as* equidistribution here; or (iii) a technique that plausibly
attacks the small-`k` shrinking-target estimate directly. A pointer ("see X, Y") is plenty — no write-up needed.
**And if the answer is simply "no, it's as hard as equidistribution" — what is the precise obstruction?** (A
reason is as valuable as a reference; experts often explain a "no" more sharply than a "yes.")

**Sharpened closing form (a yes/no a specialist can answer):** *If no such separation is known for a natural
single rank-1 orbit, is the correct obstruction that the one-sided bound is still controlled by the fixed
low-cylinder (`mod 4`, `mod 8`) frequencies — hence requires **specific-orbit genericity**, not merely
recurrence — in a **non-uniquely-ergodic full-branch** system where spectral/probabilistic tools only control
measures, never a specified point's empirical measure?* *(Our provisional reading, from a first consultation, is
**yes** — confirmation or a counter-pointer wanted.)*

## Why this is well-posed (not "please solve Mahler")
The point of the reduction is that the obstruction is now **localized**: it is exactly *single-orbit empirical
measure → Haar at the low cylinders* of an explicit Gibbs–Markov map, with every soft/elementary route
explicitly closed. A "no, that needs full equidistribution" is as useful to us as a "yes, see X." Either pins
the next move.

## The wall's three equivalent faces (pick the one your specialty answers)
1. **Ergodic/dynamics:** rank-1 single-orbit effective equidistribution of `⌊μ^n⌋ mod p` (Q0/Q1 above).
2. **Additive/Diophantine:** the one-sided shrinking-target / `v2(c'_i−c'_j)` separation (Q2).
3. **Analytic-NT / digits [NEW]:** equidistribution of a **moving middle digit** `bit_{cn}(a^n)` of `a^n` in base
   `b` (`0<c<log_b a`), along ONE orbit, **beyond the `Θ(log N)` top/bottom footholds**. We *proved* the
   footholds are exactly `Θ(log N)` (Weyl on `{n log₂3}` for the top; `×3`-coset for the bottom) and *verified*
   van der Corput is **closed** on the Mahler sum (differencing returns `t'(3/2)^n`, same family, `O(1)·√N`, no
   gain). **Q3: does ANY method — high-order van der Corput, effective metric theory, digital exponential-sum
   estimates — reach a moving middle digit of `a^n` beyond `Θ(log N)`?** (Predicted: no; a clean *no* is as
   useful as a yes — it pins the wall as "moving-middle-digit-beyond-`Θ(log N)`", sharper than "solve Mahler".)

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
