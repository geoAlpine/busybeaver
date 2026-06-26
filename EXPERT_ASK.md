# One-sided recurrence vs equidistribution for a single rank-1 *p*-adic orbit — short expert ask

> ## Does any theorem **separate** a one-sided shrinking-target / recurrence bound from full equidistribution for a **single specified** orbit of a rank-1 expanding map — or are they equivalent in difficulty?

*That is the whole question (details in Q0). Everything else is context and what we have ruled out.
**We would value most being told where this is wrong** — a sharper "no" is as useful as a "yes".*
*(framed via its BB(6)/Antihydra instance, but the question is the dynamical one in the title)*
*One page. A specialist should be able to answer the boxed question yes/no/"closest known result" without
reading anything else. Fuller context: `STATE_FOR_REVIEW.md`. **Convention (stated once): every factual claim
below is machine-checked in exact integer/2-adic arithmetic; anything not so is labelled "measured" or "open".**
We therefore drop per-claim "verified" tags.*

> **If you only answer one thing, please answer Q0.**

## The setup (3 sentences)
For the integer orbit `c_{n+1} = ⌊3 c_n / 2⌋`, `c_0 = 8`, let `E_n = #{i<n : c_i even}`. The Turing machine
"Antihydra" (a BB(6) holdout) never halts **iff the running even-density `E_n/n ≥ 1/3` for all `n`**
(equivalently `3E_n − n ≥ 0 ∀n`); conjecturally the density → 1/2. Deciding this is in the class of **Mahler's
3/2 problem (1968)** — we are *not* asking you to solve that, but to locate the precise residue below.

## What reduces to what
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
  periodic points of all periods, which violate the needed visit-count bound.
- **Non-shadowing / "spread out" does not suffice.** We *construct* (full-branch coding + inverse branches) an
  orbit that is dense in `ℤ₂`, fully supported, aperiodic — maximally non-shadowing — yet `avg jump = 3.10 > 2`.
  So the condition must pin the empirical measure to **Haar specifically**, not merely "non-concentrated."
- **Growth/counting is circular.** The telescoping `2c'_{j+1}−1 = (3/2)^{D_j}(3c'_j−1)` gives
  `log b_J = log(3/2)(J + Σ D_j) + O(1)`, but independently `n = #even+#odd = J + Σ D_j` — the same identity, so
  `Σ D_j` cancels and yields no inequality.
- **Standard single-orbit-equidistribution mechanisms are unavailable:** unique ergodicity (F has a continuum of
  invariant measures), rank-≥2 measure rigidity (the orbit is rank 1, one map `×3/2`), Weyl/van der Corput
  (closed on the multiplicative recurrence `(3/2)^n`).
- **The unconditional Diophantine (Baker) route is blocked at the source.** Deep cylinders ⟺ self-collisions
  `v2(c'_i−c'_j) ≥ k`, but the orbit terms `c_n = (3^n c_0 − T_n)/2^n` (`T_n` the parity-history carry) have
  **height `≈ n·log₂3`, unbounded** — so they are *not* fixed-height S-units and p-adic Baker does not apply
  (see Q2). Empirically the orbit even **self-separates at exactly the random rate** `2^{−k}`.
- **No finite-order obstruction exists (measured, 4 independent ways).** The orbit is statistically
  indistinguishable from i.i.d. uniform at every tested finite order: mod-`p` residues at the CLT rate, mod-`p²`
  uniform, lag-`k` mutual information `≈ 0` (a base-`p` digit-bijection makes each `k`-step joint law *equal* the
  `mod p^{k+1}` cylinder law), block-entropy rate `= log p`, random-rate self-separation. So **every finite-order /
  elementary argument is provably insufficient** — only an infinitary (effective-`log₂3`) input can decide it. This
  is *why* the question funnels to single-orbit equidistribution and nothing weaker survives.

## The question
> **Q0 (the complete-proof frontier — ask this first).** Non-halting needs only the **one-sided** bound
> `avg jump ≤ 2` (running), where `avg jump = (1/J)Σ_j v2(c'_j − 1/3)` is the orbit's average 2-adic proximity
> to the single point `1/3 ∈ ℤ₂` — equivalently a **one-sided shrinking-target / recurrence estimate**
> `N_k/J ≤ C·2^{−k}` (visit frequency to the shrinking ball `2^{−k}` around `1/3`) summing to `≤ 2`. The true
> value is `≈ 1` (a **factor-2 margin**) and the condition is *strictly weaker* than equidistribution (we
> exhibit non-Haar orbits with `avg jump ∈ (1,2)`). **Important nuance (we initially over-localized this).** The
> *realized* excess of the generic orbit (`avg jump − 1 ≈ 0.004`) sits at small `k` — but that is a property of the
> *generic* orbit, **not** of the margin *proof*: an adversarial orbit with `q = P(D≥k+1)/P(D≥k) > ½` has excess
> `q^k − 2^{−k} > 0` at **every** `k`, decaying only like `q^k`, so the deep tail contributes materially once
> `avg jump > 2`. Hence ruling out budget overflow needs one-sided cylinder-frequency control at **all** `k`, not
> only small `k`; the factor-2 margin relaxes the **threshold** (`Σ ≤ 1` vs `→ 0`) but **not the scale-range** of
> control — the same discrepancy class as equidistribution (verified by direct decomposition). *(So please read any
> "small-`k`" hint below as describing the generic orbit's realized value, not the proof's requirement.)* The bound is, **observed across all tested natural integer seeds**, uniform: every such seed gives `avg jump ≈ 1`, `N_2/J ≈
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
> differences are S-unit-*like* but **not** S-units: we verified the exact identity `c_n = (3^n c_0 − T_n)/2^n`
> with `T_n = Σ_{i<n} 3^{n−1−i} 2^i r_i` (`r_i` the parity bits), and **`height(T_n) ≈ n·log₂3` grows linearly**,
> so the orbit terms are nested-floor values of **unbounded height** — standard **p-adic Baker** (which bounds
> `v2(2^a 3^b − 2^c 3^d)` for a *fixed* finite set of algebraic numbers) **does not apply at the source.** The
> sharpened question: **is there any Diophantine tool bounding `v_p` of differences of nested-floor / β-expansion
> values generated by a fixed algebraic `μ=3/2` (unbounded height) — a "Baker for orbits of `⌊μ·⌋`"** — or is the
> unbounded height a genuine wall? (Empirically the orbit self-separates exactly at the random rate `2^{−k}`, max
> collision depth at the birthday scale — so there is no better-than-random separation to leverage either.)

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
reason is as valuable as a reference; experts often explain a "no" more sharply than a "yes.") **And if the
question is itself malformed or mis-reduced — how would you reformulate it?** (We may be overlooking an existing
theorem, or a gap in the reduction; either correction is exactly what we want.)

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
   > **Q3′ (meta):** is the **"moving middle digit"** a *recognized standalone problem* with a name/literature of
   > its own, distinct from Mahler 3/2? If there is no such concept, that absence is itself worth knowing — it may
   > be the right way to frame this whole class.

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
