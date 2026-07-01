# A mean-field theory of the Busy-Beaver Mahler cryptids: occupancy profiles, renormalization, and the golden-ratio Cramér exponent

*Draft paper (2026-07-01). Proof-complete write-up of the occupancy-profile theory (`OCCUPANCY_PROFILE_THEORY.md`,
red-teamed `OCCUPANCY_REDTEAM.md`; abstract `OCCUPANCY_THEORY_ABSTRACT.md`). All proofs below are elementary and
self-contained. This is a DESCRIPTIVE theory: it does not resolve the non-halting kernel `(K)` (Mahler 3/2 / AEV),
and its honest boundary — single-realization genericity — is stated in §7. Labels: results proved here are Theorems;
model results under the Haar/Bernoulli law are Propositions; the seed-orbit matches are Observations (exact big-int
numerics).*

---

## 1. Introduction

Antihydra is a 6-state, 2-symbol Turing machine on the bbchallenge BB(6) frontier. Its computation tracks the
integer orbit `c_0=8`, `c_{n+1}=⌊3c_n/2⌋`, with `E_n=#\{i<n: c_i \text{ even}\}`; the machine **halts iff
`balance_n:=3E_n-n<0` for some `n`** (a maintained counter underflows). Non-halting is thus equivalent to
`liminf_n E_n/n \ge 1/3`, the single-orbit even-density kernel `(K)` — the one-sided floor-mirror of the
Andrieu–Eliahou–Vivion normality conjecture and hence of Mahler's 3/2 problem (see `CRYPTID_KERNEL.md`,
`BB6_FRAMEWORK_PACKAGE.md`). Antihydra belongs to a family of BB(6) "Mahler cryptids" `\{μ=a/b : v_p(μ)=-1,\ b=p\
\text{prime}\}` (o10 at `μ=3/2`, o18/o15 at `μ=8/3`), all of whose non-halting reduces to single-orbit
equidistribution of `⌊μ^n⌋ \bmod p`.

This paper develops a **mean-field theory** of these cryptids centered on the *occupancy profile* of the induced-map
depths. We (i) give an exact identity expressing the even-count as cumulative 2-adic-cylinder occupancy (Thm 2.1);
(ii) exhibit a renormalization group on the space of depth laws with a fixed-point line of geometric laws, a single
relevant direction, and a family-wide form (Thm 3.1–3.3); (iii) show the halting question is a balance random walk
whose zero-drift criticality coincides with the RG-critical point (Thm 4.1), with an exact **golden-ratio Cramér
exponent** `θ^*=\logφ` for Antihydra generalizing to a two-parameter algebraic family (Thm 5.1–5.2); and (iv) verify
the seed orbit matches the annealed theory in every tested second-moment statistic (Obs 6.1). §7 states the honest
limitation: the theory is descriptive and annealed, and its quenched completion is exactly `(K)`.

**Setup.** Restrict to odd values: for odd `o`, with `D:=v_2(3o-1)\ge 1`, the next odd value is reached in exactly
`D` base steps, giving the *induced map* `T(o)=3^{D-1}(3o-1)/2^D` on `ℤ_2^\times`, started at `o_0=27`. Under Haar,
`T` is measure-preserving, exact, and Bernoulli with i.i.d. depths `P(D=d)=2^{-d}` (mean 2) (Bernstein–Lagarias).
Write `o_0,o_1,\dots` for the induced orbit, `D_j=v_2(3o_j-1)`, and `J(n)` for the number of odd values among
`c_0,\dots,c_{n-1}`.

## 2. The occupancy profile and the even-count identity

**Definition.** The *occupancy profile* is `N_k(J):=\#\{j<J : D_j\ge k\}` for `k\ge 1`. Since `3\inℤ_2^\times`,
`D_j\ge k \iff o_j\equiv 3^{-1}\ (\bmod\ 2^k)`, so `N_k(J)` counts visits of the induced orbit to the nested
2-adic cylinder `A_k=\{o\equiv 3^{-1}\bmod 2^k\}` (Haar measure `2^{-k}`; `A_1=` all odds, `N_1=J`).

**Theorem 2.1 (occupancy identity).** For all `n`, with `J=J(n)`,
`\#even(n) = \sum_{j<J}(D_j-1) = \sum_{k\ge 2} N_k(J)`, up to a boundary term `O(D_{J})` from the final incomplete
block.
*Proof.* Each induced step `j` consumes exactly `D_j` base steps: one odd value `o_j` followed by `D_j-1` even
values (the run `o_j, ⌊3o_j/2⌋,\dots` has `v_2` dropping by one per step until the next odd). Hence over the first
`J` induced steps there are `J` odd and `\sum_{j<J}(D_j-1)` even base values, and `n=\sum_{j<J}D_j` (valuation
budget). So `\#even(n)=\sum_{j<J}(D_j-1)`. Writing `D_j-1=\sum_{k\ge 2}\mathbf 1[D_j\ge k]` and summing gives
`\sum_{k\ge2}N_k(J)`. ∎

**Corollary 2.2.** `(K)\iff \liminf_J (\sum_{k\ge2}N_k(J))/J \ge 1/2 \iff \liminf_J \mathrm{mean}\,D \ge 3/2`. The
single-cylinder form `\liminf_J N_2(J)/J\ge 1/2` is *sufficient but strictly stronger* (`\Longleftarrow`), not
equivalent.

## 3. The renormalization group on depth-law space

**Theorem 3.1 (renormalization self-similarity, Haar).** The first-return map of `T` to `A_2=\{D\ge2\}` is again
exact Bernoulli, with renormalized depth law `P(D'=d)=2^{-(d-1)}` for `d\ge2`; equivalently `D'-1` has the original
law `2^{-e}`. Thus inducing on `A_2` reproduces `T` after a downward depth-shift of `1`, and the tower
`A_1\supset A_2\supset\cdots` is a renormalization group with `\mathrm{mean}\,D_{A_k}=\mathrm{mean}\,D+(k-1)`.
*Proof.* Under the i.i.d. law, the return word to `[D\ge2]` is `1^m d` (`m\ge0` ones then `d\ge2`); the renormalized
symbol `d` is independent of `m` with law `P(d)=2^{-d}/P(D\ge2)=2^{-(d-1)}`. Independence across returns is
inherited from the i.i.d. structure (Kac). ∎

**Theorem 3.2 (fixed-point line and relevant direction).** On the space of laws `p=(p_1,p_2,\dots)`, the
renormalization acts by `R(p)_e=p_{e+1}/(1-p_1)`. Every geometric law `p^{(a)}_e=a(1-a)^{e-1}` (`a\in(0,1)`) is a
fixed point (`\mathrm{mean}=1/a`); a general law flows under `R` to the geometric matching its tail rate (the head
is irrelevant). The linearization `DR|_{p^{(a)}}\,\delta_e=[\delta_{e+1}+p^{(a)}_e\,\delta_1]/(1-a)` is a weighted
shift with dominant (relevant) eigenvalue `1/(1-a)` and no discrete critical exponent (its spectrum is smooth along
the line).
*Proof.* `R(p^{(a)})_e=a(1-a)^e/(1-a)=p^{(a)}_e`. For general `p`, `R^n(p)_e=p_{e+n}/Z_n` re-weights the tail, so
`R^n(p)\to` the geometric with `p`'s tail rate. Linearization is direct; the eigenvalue `1/(1-a)` and the
continuous (weighted-shift) remainder are computed in `scratchpad/rg_linearized.py` (truncation artifacts flagged,
not used). ∎

**Theorem 3.3 (family-wide).** For every cryptid `μ` with `v_p(μ)=-1`, `T_μ=⌊μ\cdot\rangle` is a `p`-to-1 exact
endomorphism of `ℤ_p` (`CRYPTID_KERNEL.md`) with depth law geometric of mean `p`; the RG of Thm 3.2 is
`p`-independent, the family member sits at the fixed point `a=1/p`, and its linearized relevant eigenvalue is
`p/(p-1)`. (Verified `p=2,3` for `μ=3/2,5/2,8/3,4/3`, `scratchpad/family_rg.py`.)

## 4. The balance walk and its criticality

**Theorem 4.1 (drift and criticality).** The balance `B_n=3E_n-n` has, per induced step `j`, increment
`X_j=2D_j-3`; hence `B_n/n\to 2-3/\mathrm{mean}\,D`. The drift is `0` exactly at `\mathrm{mean}\,D=3/2`, i.e. at the
RG-critical fixed point `a=2/3`. Under Haar (`\mathrm{mean}\,D=2`) the drift is `+1/2` (supercritical).
*Proof.* Per induced step: `\Delta E=D_j-1`, `\Delta n=D_j`, so `\Delta B=3(D_j-1)-D_j=2D_j-3`; average with
`\mathrm{mean}\,D` and use `E_n/n\to 1-1/\mathrm{mean}\,D`. ∎

**Remark 4.2 (the elementary deficit).** A downward excursion of `B` by `s` requires an odd-run of length `s` (`s`
consecutive `-1` increments), and an odd-run at index `\approx n` has length `v_2(o-1)\le \log_2 c_n\approx 0.585n`
(magnitude bound), whereas the accumulated balance is `\approx 0.5n` at the *a.e.* drift. Since `0.585>0.5`, the
elementary bounds are consistent with **both** halting and non-halting (deficit `\approx1.17`). Moreover `drift>0`
for the seed orbit is itself `(K)`-grade, so the walk is only *a.e./empirically* supercritical.

## 5. The Cramér exponent

**Theorem 5.1 (golden-ratio Cramér exponent, Antihydra).** The downward-deviation (Lundberg) exponent `θ^*>0` of the
balance walk, defined by `E[e^{-θ^*X}]=1` with `X=2D-3` and `D\sim` geom(`2^{-d}`), is `θ^*=\logφ` where
`φ=(1+\sqrt5)/2`; equivalently `e^{-θ^*}=(\sqrt5-1)/2=1/φ`, and `P(\text{dip by }s)\approx φ^{-s}` in the i.i.d.
model.
*Proof.* `E[e^{-θX}]=e^{3θ}\sum_{d\ge1}e^{-2θd}2^{-d}=e^{3θ}\cdot\frac{e^{-2θ}/2}{1-e^{-2θ}/2}=\frac{e^{θ}}{2-e^{-2θ}}`.
Set `=1` and put `x=e^{-θ}`: `1/x=2-x^2`, i.e. `x^3-2x+1=0=(x-1)(x^2+x-1)`. The root in `(0,1)` is `x=(\sqrt5-1)/2=1/φ`,
so `θ^*=\logφ`. ∎

**Theorem 5.2 (two-parameter family).** For a general `m`-counter (halt `\iff` renewal density `<1/m`) on the prime
`p` (depth `\sim` geom mean `p`), the Cramér equation is `(p-1)x^m-px+1=0` (`x=e^{-θ^*}`), always divisible by
`(x-1)`. Special cases: `m=2\Rightarrow x=1/(p-1)`, `θ^*=\log(p-1)` (critical at `p=2`); `m=3\Rightarrow`
`(p-1)x^2+(p-1)x-1=0`, a quadratic irrational (`p=2`: `1/φ`; `p=3`: `(\sqrt3-1)/2`); for `p=2` the reciprocal root
`1/x` is the `(m-1)`-bonacci constant. Antihydra `(p,m)=(2,3)` is the golden-ratio member.
*Proof.* `E[e^{-θX}]=e^{mθ}\sum_{d\ge1}e^{-(m-1)θd}(1/p)(1-1/p)^{d-1}`; summing the geometric series and setting `=1`
gives, with `x=e^{-θ}`, `(1/p)/x=1-x^{m-1}(1-1/p)`, i.e. `(p-1)x^m-px+1=0`. Factor `(x-1)` and read the special
cases (verified symbolically, `scratchpad/pm_cramer.py`, `scratchpad/threshold_cramer.py`). ∎

## 6. The quenched orbit matches the annealed theory

**Observation 6.1.** For the seed-27 orbit (`N=3\cdot10^5`, exact big-int, `scratchpad/quenched_ldp2.py`): the
balance-walk drawdown obeys `P(\text{draw}=s)/P(s-1)\approx 0.62\approx 1/φ` for `s=1..11`; the depth tail is
`P(D\ge k)\approx 2^{1-k}` to four digits; and `D\ge8` events are Poisson-spread (mean gap `128.6\approx 2^7`,
coefficient of variation `1.02`). The orbit thus matches the annealed golden-ratio LDP in every *tested*
second-moment statistic to within sampling noise; no deviation is detected.

## 7. The honest boundary: single-realization genericity

The theory above is **descriptive and annealed**. Theorems 4.1, 5.1–5.2 concern the i.i.d./Haar model; Observation
6.1 is a finite-`N` empirical match. The kernel `(K)` — that the *deterministic* seed orbit attains the annealed
statistics it exhibits (equivalently, that its balance walk's quenched minimum stays `\ge0`) — is **not** proved and
**cannot** be reached at this level: by the No-Structure-Only-Selection theorem (`BB6_NO_STRUCTURE_THEOREM.md`), no
certificate constant on the invariant-measure/annealed data can separate the seed orbit from the halting fixed point
`δ_1` (an ergodic-optimization maximizer with `\int ψ\,dδ_1=+1/2`). A perfect annealed match cannot select one
orbit. In particular the Lundberg supermartingale `e^{-θ^*S_n}` has no exact deterministic (coboundary) realization,
as that is precisely the bounded sub-action the No-Structure theorem rules out. The residual is single-realization
genericity `=(K)=` Mahler 3/2 / AEV, generational and open.

## 8. Discussion

The value of the theory is architectural. Where the program's negative results (No-Structure theorem, the obstruction
dichotomy, the Coverage No-Go, decider-preemption) establish *why every existing tool fails*, this theory builds the
clean *structure* the eventual quenched tool must inhabit: a renormalization group with a geometric fixed-point line
and a single relevant coordinate; a halting transition realized as a random-walk drift criticality at the RG-critical
point; and exact algebraic constants — the golden ratio for Antihydra, the two-parameter `(p,m)` family across the
cryptids. It unifies the BB(6) Mahler core under one mean-field architecture and pins the residual precisely. The
open problem is the quenched completion, which equals the single-orbit equidistribution kernel `(K)`.

## References (pointers)

- Reduction & family: `BB6_FRAMEWORK_PACKAGE.md`, `CRYPTID_KERNEL.md`, `EVEN_COUNT_FLOOR.md`.
- No-Structure barrier: `BB6_NO_STRUCTURE_THEOREM.md`; decider-preemption: `DECIDER_PREEMPTION.md`; Coverage No-Go:
  `RANK1_AMENABLE_EQUIDISTRIBUTION.md`.
- Full development + numerics: `OCCUPANCY_PROFILE_THEORY.md` (§0–13); red-team `OCCUPANCY_REDTEAM.md`.
- Literature: Bernstein–Lagarias (2-adic conjugacy); Rudolph–Johnson (×2,×3); Andrieu–Eliahou–Vivion arXiv:2510.11723;
  Mahler (1968); bbchallenge Coq-BB5 arXiv:2509.12337. Full pins in `CITATIONS.md`.

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
