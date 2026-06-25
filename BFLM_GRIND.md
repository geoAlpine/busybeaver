# Frontier grind: why the BFLM mechanism does not adapt to our rank-1 action — SELF-DUALITY (2026-06-26)
*Grinding the most promising single-orbit tool (Bourgain–Furman–Lindenstrauss–Mozes, JAMS 2011) against our
problem. Result: a precise, BFLM-internal reason the rank-1 adaptation fails — the action is **self-dual** — plus
why the "renewal-pseudorandomness as a random-walk substitute" idea is circular, and the exact positive residue.
All structural facts exact; `bflm_grind.py`.*

## BFLM's mechanism (what we are trying to import)
For a non-abelian semigroup `Γ ⊂ SL_d(ℤ)` acting on the torus, BFLM prove the empirical measure
`ν_N = (1/N)Σ_{n<N} δ_{γ_n x}` equidistributes (unless `x` is rational-structured) by **Fourier decay**:
`ν̂_N(ξ) = (1/N)Σ_n χ_{Â^n ξ}(x)`, and the **dual orbit `{Â^n ξ}` spreads** (random-walk non-concentration on
the Zariski-dense `Γ`), forcing `ν̂_N(ξ) → 0`. The decay is *driven by the dual action being large*.

## The obstruction for us: the action is SELF-DUAL [exact]
`A = ×(3/2)` on `X = (ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`; pairing `χ_ξ(x)=e(⟨ξ,x⟩)`. Then
```
χ_ξ(Ax) = χ_ξ((3/2)x) = e(⟨ξ,(3/2)x⟩) = e(⟨(3/2)ξ, x⟩) = χ_{(3/2)ξ}(x)   ⇒   Â = ×(3/2).
```
**The dual action is the same map `×(3/2)`.** So BFLM's "make the dual orbit `{(3/2)ⁿ ξ}` spread" is the **same
rank-1 equidistribution problem** as the primal one — the Fourier-decay argument is **circular**.

- Empirically the coefficients *do* decay: `|ν̂_N(ξ)| = |(1/N)Σ e(ξ(3/2)ⁿ)| ≈ 0.4–1.2 / √N` (verified, exact
  fractional parts) — equidistribution holds. But this is exactly the **Mahler/Weyl sum**, and BFLM cannot
  *prove* the decay here because the dual orbit is rank-1 self-dual: there is **no random walk to force it**.
- **BFLM breaks the circularity with a rank-2 non-abelian `Γ`** (the dual action is *larger* than the primal, so
  the dual orbit genuinely spreads and avoids low frequencies). Our `⟨A⟩` is **rank-1, cyclic, self-dual** — no
  such break. *(This is the same fact as "the orbit uses only the self-dual combination `×3/2`, not the
  multiplicatively-independent pair `×2, ×3`" — rank-2 is exactly what the orbit does not carry.)*

## Why the renewal-pseudorandomness substitute is circular
The plan was: the renewal itinerary `(D_j)` is pseudorandom (verified — full subword complexity, `U²`-uniform),
so use it as the "random walk" that BFLM needs. It fails for two compounding reasons:
1. The randomness BFLM needs lives in the **dual frequency orbit `{(3/2)ⁿ ξ}`**, not in the primal itinerary; and
   the dual orbit's spreading **is** the equidistribution we are trying to prove (self-duality).
2. The pseudorandomness of `(D_j)` is itself the **conclusion** (a pseudorandom orbit = an equidistributed orbit),
   not an available **input** — using it assumes what we want. So it cannot seed the Fourier-decay argument.

## The positive residue (what BFLM-style *does* give)
Over **short times** the dual orbit `{(3/2)ⁿ ξ}` does spread before the self-reference bites, which recovers
exactly the **`Θ(log N)` foothold** (top via Weyl, bottom via the `×3`-coset) of `EFFECTIVE_TOPDIGIT.md`. The
self-duality is precisely what **caps** the Fourier-decay method at `Θ(log N)`: it cannot supply *long-time* dual
spreading, which is what reaching the moving middle digit (`Θ(n)`) requires.

## What this tells the multi-year programme
The BFLM/Fourier route to single-orbit equidistribution needs, specifically, to **break the self-duality of
`×(3/2)`** — i.e. to manufacture an *effective second, multiplicatively-independent direction* (a rank-2-like
input) that the cyclic orbit does not natively carry, or to replace the Fourier-decay engine with a non-self-
referential one (entropy / additive-combinatorial). This is a **sharper target than "adapt BFLM"**: it is
"defeat self-duality for a single rank-1 orbit." Honest status: no such second direction is available, and
manufacturing one is the open frontier — but the obstacle is now named in the tool's own language. 0 false proofs.
