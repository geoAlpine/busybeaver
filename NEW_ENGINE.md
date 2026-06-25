# Inventing a new engine — design-space map for amenable-hyperbolic single-orbit equidistribution (2026-06-26)
*Stepping into the invention. The engine survey (`ENGINE_SURVEY.md`) showed the wall is `amenable ∩ hyperbolic`
(a rank-1 Anosov single orbit) — no existing engine lives there. This file is the honest exploration of what a
**new** engine must do: the most promising attempt, where it reduces to the wall, and the **precise irreducible
requirement** it isolates. It does **not** claim to invent the tool (that is the multi-year frontier); it maps
the invention space and names the unprecedented core. `new_engine.py`.*

## The constraints a new engine must respect (from the survey)
- **no rank-2 / non-amenability** — the acting group is the solvable `ℤ[1/6]⋊⟨3/2⟩` (amenable); kills
  rigidity/Fourier/entropy/expansion engines.
- **no a.e.** — must pin the *single specified* algebraic seed.
- **no rotation/Weyl** — `×(3/2)` is hyperbolic (expanding), not isometric; van der Corput is closed.
- **compact phase space** — `X` is a compact solenoid, so Margulis-function / non-escape-of-mass arguments are
  *vacuous* (no mass escapes; the issue is equidistribution *within* `X`).

## The most promising attempt — the two-scale bootstrap (and where it reduces to the wall)
The 2-adic engine is unusually clean: `c ↦ ⌊3c/2⌋` is **exactly 2-to-1** (verified: every state `mod 2^k` has
exactly 2 preimages `mod 2^{k+1}`), so the `k`-step map `(b_{n-1},…,b_{n-k}) ↦ c_n mod 2^k` is a **bijection**
`{0,1}^k ↔ ℤ/2^k` (`δ(P^k)=0`). Hence:
> **equidistribution `mod 2^k`  ⟺  the diagonal-bit sequence `b_n = ⌊(3/2)^n⌋ mod 2` is `k`-distributed**
> (all `k`-tuples equally frequent).
A bootstrap `k → k+1` would close the problem **if** `k`-distribution implied `(k+1)`-distribution. It does
**not**: the step needs the `(k+1)`-th diagonal bit to be **uniform given the previous `k`** — *one fresh bit of
randomness per scale* — which `k`-distribution does not supply. So the bootstrap is **not self-closing**; each
scale needs the same `(H)`-type input, and the base case `k=1` *is* the even-density (the whole problem). The
bootstrap reduces to the wall — but **cleanly isolates the irreducible requirement.**

## ★ The irreducible requirement (the precise unprecedented core)
> A new engine must supply, **non-circularly**, the **conditional uniformity of the next binary digit of
> `⌊(3/2)^n⌋` given the previous ones** — i.e. *one fresh bit of randomness per scale, from a single
> deterministic algebraic seed.*

Equivalently: **prove the explicit deterministic sequence `b_n = ⌊(3/2)^n⌋ mod 2` is normal** (or even just
1-distributed). This is the crispest possible statement of what is missing, and it is exactly the class where
almost nothing is known: provably-normal sequences are **special constructions** (Champernowne `0.123456789101112…`,
Korobov, Bailey–Crandall-type) built *to be* normal; a *given* arithmetic sequence like `⌊(3/2)^n⌋ mod 2` is
never provably normal (this is the content of Mahler 3/2 / Borel's normality frontier).

## Other candidate engines, and why each reduces (honest)
- **Arithmetic / height of the seed.** The seed `1` (or `8`) is algebraic but of *minimal* height/complexity — if
  anything that makes it *more* likely exceptional (simple points are often special), so "too complex to be
  exceptional" is unavailable. Galois-orbit equidistribution (Bilu/SUE) needs the *Galois* orbit; `1` is rational
  (trivial Galois orbit). No traction.
- **Self-consistency / fixed point on empirical-measure limits.** The orbit's empirical limit `ν` is `A`-invariant;
  the renewal structure relates `ν mod 2^k` to `ν mod 2^{k+1}` — but only via the same fresh-bit input `(H)`.
  Circular.
- **Random-model coupling.** Showing the orbit is statistically indistinguishable from a random model *is* the
  equidistribution. Circular.
- **Effective genericity with summable error.** Would need effective single-orbit equidistribution with an error
  decaying in `n` for a fixed-height seed — but no such effective statement exists for an amenable-hyperbolic
  action (it is the wall). N/A.

## Dissection: constructed normals vs `⌊(3/2)^n⌋` — the arithmetic sequence is "too random to certify"
We compared the three proof routes to normality against our sequence (`new_engine.py` extended):

| constructed normal | proof mechanism (the certificate it exploits) | what `⌊(3/2)^n⌋ mod 2` lacks |
|---|---|---|
| **Champernowne** `.123…101112…` | **COUNTING / enumeration** — blocks are *written out*; count occurrences directly | no enumerative construction (it is a *given* dynamical orbit, not a concatenation) |
| **Korobov / Davenport–Erdős** | a **tractable Weyl-sum** bound for the constructed phase | its Weyl sum is the **Mahler sum** `Σe(t(3/2)^n)` — van der Corput **closed** |
| **Stoneham** `Σ b^{−c^n}c^{−n}` | **self-similar / recursive digit blocks** | **full subword complexity**, no recursive/self-similar block structure |

**The counterintuitive verified finding.** At `N=2·10^5`, `⌊(3/2)^n⌋ mod 2` is **far more uniform** than
Champernowne (density `0.4998` vs `0.531`; block-deviation `0.007–0.16` vs `0.21–0.67`) and has **zero
autocorrelation** (`≈0` vs Champernowne's `−0.017…−0.005`). So the arithmetic sequence is **more genuinely
random-looking** — and *that is exactly why it is unprovable.* Champernowne is provably normal **because** it
converges slowly with **exploitable local structure** (the integer-boundary enumeration) that the proof *counts*;
`⌊(3/2)^n⌋` has **no such structure to grab.**

**The deep lesson (for the new engine).** Provable normality has always come from a **designed certificate**
(enumeration / tractable phase / self-similarity) baked into the sequence — never from "being random." A *given*
arithmetic sequence carries **no certificate, only its generating dynamics** (here the rank-1 Anosov map). So the
new engine's task is sharper than "prove normality": it is **prove normality with no certificate, from the
intractable generating dynamics alone** — which no existing normality theorem does (all of them use a certificate).
The arithmetic sequence's *superior* randomness is the precise measure of *how little* structure a proof has to
work with. This is why it is the frontier.

## What this gives the multi-year programme
A new engine is **possible in principle only if** one can extract *fresh per-scale randomness from a deterministic
algebraic seed* without circularity — a genuinely unprecedented capability. The clean `δ(P^k)=0` / bijection
structure means the problem is *exactly* "one fresh bit per scale," with no other obstruction — so any future
mechanism for **provable normality of an explicit `⌊(p/q)^n⌋`-type sequence** would plug straight in and resolve
Antihydra, the whole `v_p(μ)=−1` cryptid family, and Mahler `3/2` at once. Honest status: such a mechanism does
not exist; the design space is now mapped and the irreducible core named. 0 false proofs.
