# Single-orbit equidistribution for a rank-1 hyperbolic automorphism of an S-arithmetic solenoid — expert ask

*For a homogeneous-dynamics / equidistribution specialist. One page; the boxed question is the point. The object
is purely dynamical; the motivation (a Busy-Beaver / "Antihydra" non-halting problem) is at the end. All
"verified" facts are machine-checked. **We would value most being told where this is wrong or incomplete** — in
particular whether the obstruction is really what we think, or whether a known result reaches further.*

> **If you only answer one thing, please answer the boxed Q.**

## The object
Let `R = ℤ[1/6]`, embedded diagonally in `G = ℝ × ℚ₂ × ℚ₃` as a cocompact lattice (product formula). Let
```
X = G / ℤ[1/6]          (a compact S-arithmetic solenoid, S = {∞,2,3}),
A : X → X,  A(x) = (3/2)·x      (3/2 ∈ ℤ[1/6]ˣ, so A is a well-defined automorphism).
```
`A` is **hyperbolic**: the dilations are `|3/2|_∞ = 3/2` and `|3/2|₂ = 2` (**expanding**) and `|3/2|₃ = 1/3`
(**contracting**); no neutral direction (product `= 1`). Hence `A` is **ergodic and mixing** w.r.t. Haar, so for
**Lebesgue-a.e.** `x` the orbit `{Aⁿx}` equidistributes (Birkhoff).

Fix the **specific** point `x₀ = ` image of `1 ∈ R` (equivalently any nonzero integer seed; the BB(6) instance
is `8`).

> ## Q. Does the single orbit `{Aⁿ x₀ : n ≥ 0}` equidistribute toward Haar on `X`?
> Equivalently: is `x₀` a **generic** (non-exceptional) point for this rank-1 hyperbolic action — and is there
> **any** mechanism (effective equidistribution; a Margulis-function / non-escape-of-mass argument; a Diophantine
> input on `log₂3`) that forces a **single specified algebraic** orbit of a **cyclic** hyperbolic action to
> equidistribute, where measure rigidity (rank ≥ 2) does not apply? Or is this provably out of current reach?

## The precise locus — `amenable ∩ hyperbolic` (our own engine survey)
We ground every single-orbit engine against `A`; they fail for **one** reason, which we phrase as a clean
trichotomy you may find familiar:
- **amenable + isometric** (a rotation `x↦x+α`, an odometer): tractable — Weyl / unique ergodicity;
- **non-amenable + hyperbolic** (a rank-≥2 `×p,×q` / Cat-map action): tractable — measure rigidity;
- **`A = ×(3/2)`: amenable + hyperbolic** — a **rank-1 Anosov automorphism** (the acting group is the *solvable,
  amenable* `ℤ[1/6] ⋊ ⟨3/2⟩`; genuine stable `(ℚ₃)` + unstable `(ℝ,ℚ₂)` manifolds). **This intersection *appears
  to be* an empty spot in the toolbox** (we would be glad to be corrected): amenability seems to block the
  rigidity engines (Furstenberg/Lindenstrauss/BFLM all need a non-amenable / semisimple second direction), and
  hyperbolicity blocks the rotation/Weyl engines. **Is there any single-orbit equidistribution result for a
  specified point of an *amenable hyperbolic* (rank-1 Anosov) toral / solenoid automorphism?** (We could not even
  manufacture an effective second direction from the renewal structure: the natural non-abelian semigroup it
  generates is `ℤ[1/6] ⋊ ⟨3/2⟩` — *solvable*, hence amenable, hence no spectral gap.)

## Why this is not covered by the standard tools (what we believe is ruled out)
- **Rank-1 ⇒ no measure rigidity.** `⟨A⟩` is cyclic; Furstenberg/Rudolph–Johnson/Lindenstrauss rigidity needs two
  multiplicatively-independent maps (rank ≥ 2). Einsiedler–Lindenstrauss (JMD 2008) note rank-1 carries a rich
  family of invariant measures and **invariant Cantor sets** — so `A` has many non-Haar ergodic measures
  (we exhibit explicit non-Haar Bernoulli measures and points generic for them).
- **a.e. is the wrong quantifier.** Koksma (1935): `{θⁿ}` equidistributes for a.e. `θ`; this is exactly the
  a.e.-over-starting-point statement and says nothing about the named `x₀`.
- **Single-orbit positive results need a large acting group.** Bourgain–Furman–Lindenstrauss–Mozes (JAMS 2011)
  get individual-orbit torus equidistribution, but for a **non-abelian semigroup**, not a cyclic `⟨A⟩`.
- **Effective equidistribution** (Lindenstrauss–Mohammadi 2022 and successors) is for **unipotent / higher-rank**
  orbits — not a single cyclic hyperbolic orbit.
- The `ℝ`-projection of the orbit is exactly `{(3/2)ⁿ}` — so **Q contains Mahler's 3/2 problem (1968)** as its
  archimedean shadow. *The reason we ask a dynamicist:* the full solenoid carries the **extra contracting
  3-adic (stable) direction** absent from the bare `{(3/2)ⁿ}` — **does that hyperbolic structure give any
  leverage the real projection alone does not?**

## What we have pinned (verified, so you can skip these)
- `x₀` is **not eventually periodic** and **not** a preimage of the (3-power-denominator) singular set — both are
  Haar-null rational sets that every integer seed avoids automatically.
- **No permanent trapping** (a *single-orbit* lemma we proved): periodic points are 2-adically **repelling**
  (the action expands at the prime 2, `|3/2|₂ = 2`), so an approach to a periodic orbit at 2-adic depth `m` is
  **transient** — it decouples within `O(m)` steps and cannot persist. Hence no orbit is asymptotic to a periodic
  cycle unless it is eventually periodic, and the *periodic* part of the exceptional set is rigorously excluded.
  (Sharp form on the induced renewal map `F` — `A` restricted to its 2-adic return times: `v₂(Fᵗx − p) =
  v₂(x − p) − t(D+1)`, branch `D`.) The **positive-entropy** Cantor-set part of the exceptional set is what
  remains — and is the open question.
- Empirically, **every** tested natural integer seed equidistributes (visit frequencies to cylinders match Haar
  to `< 1%`); the difficulty is the standard **a.e.→specific** gap for a named point, not a pathology of `x₀`.

## Expected answer format
A pointer is plenty. Useful: (i) any theorem (or named conjecture) giving single-orbit equidistribution for a
cyclic hyperbolic action under a Diophantine/algebraic hypothesis; (ii) the **precise reason** the rank-1
single-orbit case is out of reach (a sharper "no" than "rank-2 is needed" — e.g. what the contracting 3-adic
direction can and cannot buy); (iii) whether the S-arithmetic (vs purely-real Mahler) framing is known to help.

## Motivation (the instance)
For the integer orbit `c_{n+1} = ⌊3c_n/2⌋`, `c₀ = 8`, the Busy-Beaver machine "Antihydra" (a BB(6) holdout) never
halts iff the running density of even terms stays `≥ 1/3` forever. The even-density is governed by the digit of
`(3/2)ⁿ` at a **moving (diagonal) position**, i.e. by the equidistribution of `{Aⁿ x₀}` above. A proof that `x₀`
is generic would decide this BB(6) machine; we have reduced the machine to exactly the boxed Q and verified the
reduction.
