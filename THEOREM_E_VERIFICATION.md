# One-page verification request: is Theorem E a genuine weakening, or growing-window equidistribution in disguise?

> ## The one question. Theorem E reduces "Antihydra never halts" to: *the single orbit `c_n=⌊8(3/2)^n⌋` has power-saving character-sum cancellation `|Σ_{n<N}ψ(c_n)|≤C N^{1−δ}` (some `δ>0`) for all nontrivial Dirichlet `ψ` of conductor `≤ N^δ`.* **Is this hypothesis genuinely weaker than full mod-`2^k` equidistribution of the orbit, or is "cancellation for all conductors `≤ N^δ`" already equivalent in difficulty (a growing-window equidistribution)?** A clean "weaker / same-difficulty / equivalent, because…" is exactly what we need.

*Self-contained; the boxed question is the point. All [PROVEN] claims are machine-checked in exact 2-adic arithmetic.*

## Setup (3 lines)
`c_{n+1}=⌊3c_n/2⌋`, `c_0=8`. Non-halt ⟺ running even-density `≥1/3`. Let `D_n=v2(3c_n−1)` for odd `c_n`; the
exact **valuation budget** `Σ_{i<n,odd}D_i = n+v2(c_n)−v2(c_0)` gives **non-halt ⟺ `avgD_odd≥3/2`** (Haar value 2).

## Theorem E [PROVEN reduction]
Write `avgD_odd = 2 − Σ_{k≥1}δ_k`, `δ_k = 2^{−(k−1)} − P(D≥k\mid odd)` (verified decomposition; for seed 8 every
`δ_k>0` — low cylinders are *under*-visited, so only `δ_k>0` can lower `avgD_odd`). Two rigorous per-scale bounds:
- **(geometric)** `δ_k ≤ 2^{−(k−1)}` always (since `P(D≥k\mid odd) ≥ 0`);
- **(character)** `|δ_k| ≤ max_{ψ≠1 mod 2^k} |avgψ_odd|`, where `avgψ_odd = (1/O_N)Σ_{n<N,odd}ψ(c_n)` (exact
  character expansion of the cylinder indicator `1[c≡3^{−1} mod 2^k]`).

**Claim.** If there are `δ>0, C` with `|Σ_{n<N,odd}ψ(c_n)| ≤ C N^{1−δ}` for every nontrivial `ψ` of conductor
`≤ N^δ`, then with `K*` defined by `2CN^{−δ}=2^{−(K*−1)}` (so `K*≈δ\log_2 N`):
```
Σ_{k:δ_k>0} δ_k  ≤  Σ_{k≤K*} 2CN^{−δ}  +  Σ_{k>K*} 2^{−(k−1)}  =  O(N^{−δ}\log N),
```
hence `avgD_odd ≥ 2 − O(N^{−δ}\log N) ≥ 3/2` for `N≥N_0` ⟹ **non-halt**. *Any* power saving `δ>0` suffices, and
only at **low** moduli (conductor `≤ N^δ`).

## The two things to check
1. **Is the reduction correct?** The crossover argument bounds the *positive* deviations (the only ones that lower
   `avgD_odd`) by the *minimum* of the geometric and character bounds; the geometric bound caps the tail `k>K*`,
   the character bound caps `k≤K*`, and the sum is `O(N^{−δ}\log N)`. Is this sound? (We believe yes; independent
   check wanted.)
2. **THE CORE QUESTION (boxed above).** The hypothesis asks for cancellation at *all* conductors `≤ N^δ` —
   a window that **grows with `N`**. Is that already tantamount to mod-`2^k` equidistribution for `2^k≤N^δ` (i.e.
   the same difficulty as the full problem on a growing window), or is "some power saving `δ>0`" genuinely weaker
   than "discrepancy `→0` at every fixed scale"? Concretely:
   - *Weaker?* It only needs `δ>0` cancellation (not `o(1)` discrepancy with the true exponent), and only the
     **positive** (under-visited) deviations matter (the sign-restriction in the reduction). A non-equidistributing
     orbit with the *right one-sided* behaviour could satisfy it.
   - *Same difficulty?* "Power saving for all conductors up to a growing `N^δ`" may be exactly a quantitative
     equidistribution statement, with no known way to get it without proving equidistribution.
   Our reading (to be confirmed/refuted): **strictly weaker as a *target*, but plausibly the same *difficulty
   class*** — analogous to one-sided recurrence vs equidistribution, where the one-sided bound is weaker yet no
   tool delivers it without the two-sided one.

## Why it still matters either way
- If **genuinely weaker**: Theorem E hands analytic number theory a sharply-posed prize — *any* power saving at low
  2-power moduli for the explicit orbit `⌊8(3/2)^n⌋`, with a number (`δ>0`) and a scale range (`≤N^δ`).
- If **same difficulty**: that is itself the cleanest possible statement of where Antihydra sits — it pins the
  problem to "low-moduli character cancellation along one `⌊μ·⌋`-orbit", a precise Weyl/Gowers-type target, and
  tells us not to expect a shortcut below full equidistribution.

## What we know around it (so you can skip)
- Closest known: **Tao (2019)** controls the same 3-adic skew-walk character statistic but at **log-density-1 over
  seeds**, never one seed; **Flatto–Lagarias–Pollington (1995)** gives only a *range* bound for a single seed. The
  single-orbit case is the open **Mahler 3/2 / 2025 normality conjecture** (arXiv:2510.11723).
- The orbit is i.i.d.-indistinguishable at every finite order; van der Corput is closed; it is multiplicatively
  structureless in `n` (uncorrelated with `λ(n)`, flat over `n≡a(q)`) — so Vaughan/bilinear have no entry point.

**Reply format.** A one-line verdict on the boxed question (weaker / same-difficulty / equivalent-because) plus, if
possible, a pointer to the nearest technique (post-Tao-2019) for low-conductor character cancellation along a
deterministic `⌊μ·⌋`-orbit. A sharp "no shortcut, here is why" is as valuable as a route.
