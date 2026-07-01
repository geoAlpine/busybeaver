# A mean-field theory of the BB(6) Mahler cryptids: the occupancy profile, its renormalization group, and the golden-ratio Cramér exponent — paper-grade synthesis (2026-07-01)

*Consolidation of the eight-brick occupancy-profile theory (`OCCUPANCY_PROFILE_THEORY.md`, sections 0–12,
red-teamed `OCCUPANCY_REDTEAM.md`) into a self-contained, paper-grade statement. This is a **descriptive theory**
of the BB(6) Mahler cryptids' non-halting question; it does NOT prove `(K)` (= Mahler 3/2 / AEV). Its value is a
clean, verified architecture that reduces the halting question, at the mean-field and second-moment levels, to a
single **single-realization genericity** statement, and exhibits exact structural constants (the golden ratio / the
`n`-bonacci family). SOUNDNESS: `[PROVEN]` = exact algebra or a Haar/Kac model theorem; `[OBSERVED]` = exact big-int
numerics; `[HEURISTIC]` = annealed/i.i.d.-model. No label upgraded; the quenched core is `[OPEN] = (K)`.*

---

## Abstract

For the BB(6) cryptid family `{μ : v_p(μ)=-1}` (Antihydra `μ=3/2`, `p=2`; o18/o15 `μ=8/3`, `p=3`; …), whose shared
kernel is the single-orbit equidistribution of `⌊μⁿ⌋ mod p` (`CRYPTID_KERNEL.md`), we develop a mean-field theory
centered on the **occupancy profile** `N_k(J)=#\{j<J : D_j≥k\}` of the induced-map depths `D_j`. We prove: (i) an
exact even-count identity `#even = Σ_{k≥2}N_k`; (ii) a **renormalization group** on depth-law space with a
fixed-point line of geometric laws, one relevant direction (the tail rate), and the family member at `a=1/p`; (iii)
that the halting question is a **balance random walk** whose zero-drift criticality coincides with the RG-critical
point, with an exact **golden-ratio Cramér exponent** `θ^*=\logφ` for Antihydra, generalizing to the `(m-1)`-bonacci
constants across counter ratios `m`. We verify the quenched seed-27 orbit matches this annealed theory in every
tested second-moment statistic. The residual — that the deterministic orbit *attains* the annealed statistics it
exhibits — is single-realization genericity `= (K)`, which the theory does not (and, by the No-Structure theorem,
cannot at this descriptive level) close.

## The results, as a theorem list

**T1 (occupancy identity) `[PROVEN]`.** `#even(n)=Σ_{j<J(n)}(D_j-1)=Σ_{k≥2}#\{j<J: o_j≡3^{-1}\bmod 2^k\}` — the
even-count is cumulative occupancy of the nested `2^{-k}`-cylinders. (Verified exact, boundary `O(1)`.)

**T2 (renormalization group) `[PROVEN under Haar / OBSERVED quenched]`.** The first-return map to `A_2=\{D≥2\}` is
exact Bernoulli with the depth shifted by `1`; the `A_k`-tower is a renormalization group with `\mathrm{mean}D`
`+1` per level. On depth-law space `R(p)_e=p_{e+1}/(1-p_1)` has a **fixed-point line** (all geometric laws,
`\mathrm{mean}=1/a`), a single **relevant** coordinate (the tail rate), and linearized relevant eigenvalue
`1/(1-a)`; no discrete critical exponent (smooth through criticality).

**T3 (family-wide) `[PROVEN-in-family]`.** T2 ports to the whole `\{v_p(μ)=-1\}` family: depth law geometric with
`\mathrm{mean}=p`, member at `a=1/p`, relevant eigenvalue `p/(p-1)`. Only the halt-criticality threshold is
per-machine.

**T4 (balance-walk criticality) `[PROVEN drift-formula; a.e./HEURISTIC supercriticality]`.** Halting `⟺` the balance
walk `B_n=3E_n-n` goes negative. Its drift is `2-3/\mathrm{mean}D`, zero exactly at `\mathrm{mean}D=3/2` (`a=2/3`,
the RG-critical point). **Caveat:** `\mathrm{drift}>0` for the seed-27 orbit is itself `(K)`-grade (a.e. value
`+½`); the elementary run ceiling `0.585·\mathrm{index}` exceeds the a.e. drift `0.5·\mathrm{index}`, so elementary
bounds are consistent with both halting and non-halting (deficit `1.17×`).

**T5 (golden-ratio Cramér exponent) `[PROVEN exact]`.** The balance walk's downward-deviation exponent solves
`E[e^{-θ^*X}]=1`, `X=2D-3`, giving `x^3-2x+1=(x-1)(x^2+x-1)=0`, `x=e^{-θ^*}=1/φ`, so `θ^*=\logφ`. For a general
`m`-counter, `x^m-2x+1=(x-1)(x^{m-1}+\dots+x-1)=0` and `1/x` is the **`(m-1)`-bonacci constant** — Antihydra
(`m=3`) is the golden-ratio/Fibonacci member, `m=2` the critical boundary.

**T6 (quenched match) `[OBSERVED]`.** The seed-27 orbit matches the annealed golden-ratio LDP in every tested
second-moment statistic at `N=3·10⁵` (drawdown ratio `≈1/φ`, depth tail `≈2^{1-k}`, large-depth spacing Poisson
`CV≈1.0`), with no detected deviation.

## Honest scope (what this is NOT)

- **Not a proof of `(K)`.** T4's supercriticality and the T5 LDP are **annealed** (a.e./i.i.d.); T6 is a finite-`N`
  empirical match. The quenched single-orbit minimum staying `≥0` is `(K)` and is not established.
- **Cannot select the orbit at this level.** By the No-Structure theorem, a perfect annealed/measure match cannot
  distinguish the seed orbit from the halting fixed point `δ_1`; the theory is descriptive, not selective.
- **The residual is exactly single-realization genericity** = the deterministic orbit attaining its own empirical
  (annealed-matching) statistics = `(K)` = Mahler 3/2 / AEV.

## Place in the program & why it is worth recording

This is the **positive/architectural** companion to the program's negative results (No-Structure theorem,
Coverage No-Go, decider-preemption): where those pin *why every tool fails*, this builds *the clean structure the
eventual tool must inhabit* — a renormalization group with an exact fixed-point line, a criticality that is a
random-walk drift transition, and exact algebraic constants (golden ratio, `n`-bonacci). It unifies the BB(6)
Mahler core under one mean-field architecture, exhibits the halting transition as a critical phenomenon in a precise
sense, and quantifies the elementary deficit (`1.17×`) and the annealed non-halting heuristic. It is a genuine,
verified, self-contained theory layer — the multi-year program's first — with the honest boundary that its
quenched completion is the generational kernel. **No machine decided. No label upgraded.** `(K)` remains `[OPEN]` =
Mahler 3/2 / AEV.
