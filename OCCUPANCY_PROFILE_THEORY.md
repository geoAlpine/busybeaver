# Foundation of the occupancy-profile theory (the new theory's scaffolding, built solo) (2026-06-30)

*First foundation block of the multi-year, self-contained ("we do it ourselves") theory-building effort. It does
NOT advance the frontier toward `(K)`; it sets up the central object cleanly, states the provable scaffolding, and
isolates the single open axiom the theory must eventually supply. HONEST SCOPE: every provable lemma here is either
the today-proven identity or the known Haar/Bernoulli structure; the open core is quenched = `(K)`. This is durable
framework-foundation work, NOT new progress on the kernel. SOUNDNESS labels throughout. NOT committed by default.*

> **[RED-TEAM VERDICT, `OCCUPANCY_REDTEAM.md`: CONFIRMS facts, phrasing caveated.]** All eight bricks (R,F,W,L,U,C,Q,N)
> independently re-verified with exact arithmetic (golden ratio / n-bonacci via `sympy`; `θ*=logφ` gives MGF `=1.0000`;
> all numerics reproduced). No false theorem, no mislabelled `[PROVEN]`, no annealed→quenched leak, no claim of progress
> toward `(K)`. Four phrasing fixes applied: **(1)** §10 (C3) the "`Σ_J φ^{-J} ≈ 1.7·10⁻⁴`" was literally false (the
> full sum is `φ`); corrected to an offset-dependent post-transient tail. **(2)** §11 "i.i.d.-indistinguishable" softened
> to "matches i.i.d. in all *tested* second-moment statistics to within sampling noise at `N=3·10⁵`". **(3)** §1 (S4)
> `⟺` → `⟸` (`freq(D≥2)≥½` is sufficient/strictly-stronger, not equivalent). **(4)** §7 the drift `+½` is the
> **a.e./Haar value, unproven for the orbit** (drift`>0` is itself `(K)`-grade); "morally certain" tagged `[HEURISTIC]`.

---

## 0. The central object

For the induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, `o_0=27`, with odd values `o_0,o_1,…` and gaps
`D_j=v₂(3o_j−1)`, define the **occupancy profile**

> `N_k(J) := #\{ j < J : o_j ≡ 3^{-1} \ (\mathrm{mod}\ 2^k) \} = #\{ j<J : D_j ≥ k \}`,  for `k ≥ 1`.

`N_k(J)` counts how many of the first `J` odd values lie in the nested 2-adic cylinder `A_k=\{o≡3^{-1}\bmod2^k\}`
(Haar measure `2^{-k}`, but `A_1`= all odds so `N_1=J`). The profile `N_1 ≥ N_2 ≥ N_3 ≥ …` is the central object;
the kernel is a single statement about its top-level asymptotics.

## 1. Provable scaffolding `[PROVEN]`

- **(S1) Even-count identity.** `#even(n) = Σ_{k≥2} N_k(J(n)) = Σ_{j<J}(D_j−1)`, `J(n)=#odd values < n`. (Verified
  exact, `scratchpad/rung2.py`, `N=3·10⁵`, boundary diff `3`.) `EVEN_COUNT_FLOOR.md` §1.
- **(S2) Budget.** `Σ_{k≥1} N_k = Σ_j D_j = n + O(1)` (valuation budget); with `N_1=J`, this gives
  `#even = n − J = Σ_{k≥2}N_k` and `mean D = n/J = (Σ_k N_k)/N_1`.
- **(S3) Nesting & cylinder form.** `N_{k+1} ≤ N_k` (nested cylinders); `D_j≥k ⟺ o_j≡3^{-1}\bmod 2^k` (`3∈ℤ₂^×`,
  framework Link 3) — so the profile is *literally* cumulative cylinder occupancy.
- **(S4) The kernel in profile terms.** `(K) ⟸ liminf_J N_2(J)/J ≥ 1/2` (the ψ-form / `freq(D≥2)≥½` **sufficient,
  strictly stronger** case — `⟸`, not `⟺`), and the genuine equivalence is with the full sum:
  `(K) ⟺ mean D ≥ 3/2 ⟺ liminf_J (Σ_{k≥2}N_k)/J ≥ 1/2`. So the **entire kernel is the top-rung asymptotic density of
  the profile.**

## 2. The Haar/a.e. structure the profile inherits `[PROVEN-in-lit / a.e.]`

Under Haar on `ℤ₂^×`, `T` is exact and Bernoulli with `D_j` i.i.d. `P(D=d)=2^{-d}` (Bernstein–Lagarias). Hence:
- **(H1)** `N_k(J)/J → 2^{-(k-1)}` a.s. (SLLN); the profile is geometric with ratio `½` at every level.
- **(H2)** the first-return time to each `A_k` is geometric (memoryless), mean `2^{k-1}` for `A_k` (mean `2` for
  `A_2`); the induced-on-`A_k` map is again exact Bernoulli (Kac).
- *Observed for the specified orbit `o_0=27`* (`scratchpad/occupancy.py`, `J=3·10⁵`): `N_k/J = 0.4985, 0.2485,
  0.1237, …` vs Haar `2^{-(k-1)}`; `N_{k+1}/N_k ≈ 0.50` at every level; `A_2`-return-time distribution
  `74399, 37497, 18790, …` (geometric, halving), mean `2.006`. The orbit's profile matches Haar to `O(1/√J)` —
  `[OBSERVED]`, not proven.

## 3. The single open axiom `[OPEN = (K)]`

Everything provable above is either the exact identity (§1) or the Haar/a.e. law (§2). The theory's one missing
input is the **quenched** version of (H1) at the top rung, for the specified orbit:

> **(Q) Quenched top-rung occupancy.** `liminf_J N_2(J)/J ≥ 1/2` for `o_0=27` (equivalently `liminf` of the full
> profile sum `≥ ½`, equivalently `mean D ≥ 3/2`). **This is exactly `(K)` = Mahler 3/2 / AEV.**

`EVEN_COUNT_FLOOR.md` proves there is **no unconditional rung between** the elementary floor (the magnitude ceiling
gives only `N_2(J) ≥` the `Θ(log)`-grade bound via single-visit depth) and (Q): improving the occupancy lower bound
past `log` requires the visit *frequency*, which is (Q) itself. So the profile theory's provable part stops exactly
at the Haar law + the magnitude floor, and (Q) is the generational axiom.

## 4. Honest status & the genuine open sub-problems we can chip at (solo, long-haul)

This foundation is a clean *reorganization*, not new frontier progress: its provable lemmas are the known Haar
structure, and (Q) = `(K)`. Stated plainly so no future reader over-reads it. What it *does* give the multi-year
solo effort is a precise, minimal object and a list of genuinely-open construction sub-problems that are narrower
than `(K)` and might admit partial internal progress over time (each still hard, none known):
- **(P1)** the *quenched* first-return map to `A_2` — is its return-time generating function controllable from the
  orbit's specific 2-adic arithmetic, even partially? (The Haar version is geometric; the quenched version is the
  frontier.)
- **(P2) — ATTEMPTED 2026-06-30, COLLAPSES.** Tested whether a *finite-level* self-consistency gives a monotone
  level-`K` conditional lower bound on `N_2/J`. **Verdict: (P2) collapses; the finite-level object is ill-posed.**
  Two `[PROVEN]`-grade reasons:
  - **Non-closure.** The induced map `T` does **not** descend to `ℤ/2^K`: `D=v₂(3o−1)` is unbounded, so for
    `o≡3^{-1}\bmod 2^K` (the deepest cylinder) the successor `T(o)\bmod 2^K` is undetermined by `o\bmod 2^K`. There
    is therefore no finite-state self-map to run a self-consistency on; this non-descent to a finite quotient is
    exactly the non-integrality of `3/2` (`CORE_SPECIFIED_POINT_INPUT.md`) — the core obstruction itself.
    *(Soundness note: a quick truncated residue-graph computation gave erratic, model-dependent reachable sets
    (`8/8, 4/16, 9/32, 64/64, …` across `K`) — these are ARTIFACTS of the broken truncation, not findings, and were
    discarded. The discipline caught it: erratic = buggy model, not structure.)*
  - **δ₁ feasibility (the established result).** Even in the program's *proper* residue-optimization (No-Structure
    theorem, Fraction arithmetic, conservative tail, `k=3..12`), the halting fixed point `o=1` (`D≡1`,
    `freq(D≥2)=0`) is a feasible `T`-invariant measure with `β=∫ψ=+½`. So the proper level-`K` conditional lower
    bound on `N_2/J` is `0` for every `K` — **no monotone improvement, no positive floor.** This is the same δ₁
    obstruction as §3 of `BB6_NO_STRUCTURE_THEOREM.md`, now seen on the finite-level-self-consistency angle.
- **(P3)** the exact carry structure `S_n` feeding the profile — a bookkeeping question, fully internal.
These are the honest hand-holds for "doing it ourselves," with no pretense that any is `(K)`.

## 5. The renormalization-group structure of the profile (brick, 2026-07-01)

A genuine structural layer of the theory, found by building the first-return map to `A_2` (`scratchpad/p1_return.py`,
`N=4·10⁵` induced steps).

> **(R1) Renormalization self-similarity `[PROVEN under Haar; OBSERVED quenched]`.** The first-return map
> `T_{A_2}: A_2 → A_2` (`A_2=\{D≥2\}`) is again **exact Bernoulli**, with renormalized depth law
> `P(D'=d)=2^{-(d-1)}` for `d≥2` — i.e. `D'-1` has the *original* geometric law `2^{-e}` (`e≥1`). Hence
> **`T_{A_2} ≅ T` after a depth-shift by `1`.** More generally inducing on `A_k=\{D≥k\}` reproduces `T` after a
> depth-shift by `k-1`, giving a **renormalization group** on the tower `A_1 ⊃ A_2 ⊃ A_3 ⊃ ⋯`.
> *Proof (Haar):* Kac inducing of the geometric Bernoulli shift on the cylinder `[D≥2]`; the return word is
> `1^m d` (`d≥2`), the renormalized symbol is `d`, independent of the `1`-run, with law `2^{-(d-1)}`. ∎
> *Observed (quenched, the seed-27 orbit):* `freq(D'=d)=0.5024, 0.2496, 0.1237,…` (vs `2^{-(d-1)}`), return-time to
> `A_2` geometric (`99771,50055,25143,…`, mean `2.001`), and `I(D'_i;D'_{i+1})=0.00069 ≈` shuffle `0.00071`
> (memoryless). `[OBSERVED]`

> **(R2) The kernel under renormalization `[PROVEN]`.** `mean D_{A_k} = mean D + (k-1)`: each renormalization step
> adds exactly `1` to the mean depth. So the kernel quantity `mean D` is *renormalization-covariant* (shifts by a
> constant per level), and `(K)` (`mean D ≥ 3/2`) is a statement about the base level of an exactly self-similar
> tower.

> **(R3) Honest scope — symmetry, not contraction `[ARGUED]`.** This renormalization is a **symmetry**, not a
> contraction: the renormalized problem (`T_{A_2}`-genericity of the induced seed) is *equally hard* — it is the
> same specified-orbit Bernoulli-genericity problem one level up. This is exactly why the scale bootstrap
> "regresses infinitely" (`CORE_CARRY_LEVER.md` §12) and why the cross-scale renormalization cocycle is a
> **coisometry** with `‖Φ‖≡1` (`EUE_COISOMETRY_NOGO_THEOREM.md`): no contraction is manufactured. So (R1)–(R2) are
> genuine *architecture* of the occupancy-profile theory — the self-similar tower the eventual `(K)`-tool must
> respect — but **not, by themselves, a lever**: using them requires breaking the symmetry with orbit-specific
> (seed-27) data, which is `(K)`.

**Net (R):** the profile theory has an exact renormalization-group symmetry `A_k`-tower with `mean D` shifting by
`+1` per level (provable under Haar, observed quenched). It unifies three prior facts (Kac-Bernoulli inducing, the
infinite bootstrap regress, the coisometry `‖Φ‖=1`) as one self-similarity, and is a durable architectural brick.
It is a symmetry, so the lever still needs the seed-specific input = `(K)`.

## 6. The RG flow on depth-law space — fixed-point line, relevant direction, criticality (brick, 2026-07-01)

Pushing the renormalization from a single map to the **space of depth laws** `p=(p_1,p_2,…)` gives a clean
renormalization-group flow. The induce-on-`A_2`+shift operation acts on laws as
> **`R(p)_e = p_{e+1}/(1-p_1)`** (`e≥1`)  —  peel the `D=1` mass, renormalize, shift down by one.

- **(F1) Fixed-point LINE `[PROVEN, exact]`.** *Every* geometric law `p_e^{(a)} = a(1-a)^{e-1}` (`a∈(0,1)`) is a fixed
  point of `R`, not only Haar (`a=½`): `R(p^{(a)})_e = a(1-a)^e/(1-a) = a(1-a)^{e-1} = p_e^{(a)}`. Verified exactly
  (`Fraction`, `a=½,⅓,⅔,¼`). Mean depth on the line is `1/a`.
- **(F2) The relevant direction is the TAIL RATE `[verified]`.** A general law flows under `R` to the geometric
  fixed point matching its **tail decay rate**: the head (`p_1,p_2,…`) is washed out (irrelevant), only the
  asymptotic ratio survives. *Verified:* a perturbed law with tail `r=0.4` flows in 2 steps to `a=1-r=0.6`,
  `mean D = 1/(1-r) = 1.667` (exact convergence). So depth-law space RG-collapses to **one relevant coordinate**, the
  tail rate `1-a`.
- **(F3) The kernel is a criticality condition `[PROVEN reframing]`.** `(K)` (`mean D ≥ 3/2`) `⟺` `a ≤ 2/3` `⟺`
  tail rate `1-a ≥ 1/3`. The halting fixed point `δ_1` is `a=1` (mean `1`, all `D=1`, fastest-decaying / no tail);
  Haar is `a=½` (mean `2`); the **halting transition sits at the critical fixed point `a=2/3` (mean `3/2`)**. So on
  the first-moment / asymptotic-law level, non-halting vs halting is a *position on the RG fixed-point line*, and
  `(K)` asks which fixed point the seed-27 orbit's depth law flows to.

> **(F4) Honest scope `[ARGUED]`.** This RG governs the **asymptotic mean depth law** (first-moment level): which
> geometric fixed point the *empirical* depth law approaches. It does **not** establish, for the specific seed-27
> orbit, (i) that the orbit actually sits at a fixed point with `a≤2/3` (a quenched convergence statement), nor
> (ii) the **liminf / fluctuation** control that `(K)` needs beyond the mean — the running even-density can dip
> below `1/3` (halting) even if the asymptotic mean depth is `≥3/2`, a second-moment / large-deviation phenomenon
> the mean-flow RG does not see. So (F1)–(F3) are a clean *first-moment architecture* (and a genuine reframing of
> `(K)` as criticality in the tail rate), not a proof: the quenched seat + the fluctuation control are exactly the
> open `(K)`.

**Net (F):** depth-law RG ⇒ a fixed-point line of geometrics (`mean=1/a`), a single relevant coordinate (tail rate),
and `(K)` as the criticality `a≤2/3`. This is the sharpest *architectural* statement of the kernel yet — it is a
first-moment / mean-level structure; the quenched seat and the second-moment fluctuation control remain `(K)`.

## 7. The balance walk: criticality = zero drift, and why the elementary bounds are consistent with halting (brick, 2026-07-01)

The fluctuation/second-moment side (the gap (F4)) is the **balance walk** `B_n = 3E_n − n` (`E_n=#even<n`); the
machine **halts ⟺ `B_n < 0` for some `n`**. This connects the RG criticality to a random-walk transition and pins
exactly why elementary bounds cannot close `(K)`.

- **(W1) Drift = `2 − 3/mean D`, critical at the RG point `a=2/3` `[PROVEN]`.** `E_n/n → 1 − 1/\mathrm{mean}D`, so
  `B_n/n → 3(1−1/\mathrm{mean}D) − 1 = 2 − 3/\mathrm{mean}D`. *Verified* (`scratchpad/balance_walk.py`, `N=6·10⁵`):
  `B_n/n → 0.49632` vs predicted `0.49631`. The drift is `0` exactly at `mean D = 3/2` `⟺ a=2/3` — **the RG-critical
  fixed point is the zero-drift point of the balance walk.** Haar (`meanD=2`, `a=½`) gives drift `+½` (supercritical);
  `meanD<3/2` gives negative drift (halts). So the halting transition is a *drift-sign change*, a textbook
  random-walk criticality, sitting exactly at the RG-critical `a=2/3`.
- **(W2) The orbit is decisively supercritical `[OBSERVED]`.** Increments are bounded `{+2 (even), −1 (odd)}`,
  variance `2.25`. The running minimum of `B_n` (after the `n≤30` transient) is the **constant `17`, attained at
  `n=45` and never approached again** across `N = 10³,10⁴,10⁵,6·10⁵` — drift dominates fluctuations completely; the
  walk's infimum is achieved early and it escapes to `+∞`. Worst running even-density `0.4566` (margin `0.123` above
  the `1/3` halting threshold).
- **(W3) Why elementary bounds DO NOT close it — the `0.585 > 0.5` gap `[PROVEN consistency]`.** A downward excursion
  of size `s` in `B` requires an **odd-run of length `s`** (`s` consecutive `−1` increments). The odd-run lemma +
  magnitude give run length `≤ v₂(c−1) ≤ log₂ c_n ≈ n·log₂(3/2) = 0.585n`. But the accumulated balance at index `n`
  is only `≈ (\text{drift})·n = 0.5n`. Since **`0.585n > 0.5n`**, a single near-maximal odd-run placed late could
  drop `B` by `0.585n` against an accumulated `0.5n` — driving it **negative**. Hence the elementary facts (drift
  `+½` from the a.e. mean, run ceiling `0.585·index` from magnitude) are **consistent with BOTH halting and
  non-halting**: they fail to close the question by the factor `0.585/0.5 = 1.17`. Non-halting needs the odd-runs to
  be genuinely *short* (`< 0.5n` at every scale; empirically `max = 20`), i.e. depth-tail control `= (K)` — the same
  wall as `EVEN_COUNT_FLOOR.md` (run length `= v₂ =` near-halt) in dynamical-walk language.

**Net (W):** the halting question is a walk with bounded increments whose downward excursions are odd-runs of length
up to `0.585·index`; the RG-critical `a=2/3` is its zero-drift point. **Crucial caveat on the drift.** The drift
`+½` (and hence "supercritical") uses `mean D = 2`, which is the **a.e./Haar value — NOT proven for the seed-27
orbit**; indeed `drift > 0` for the orbit is *itself* `(K)`-grade (it is even-density `≥ 1/3+`). So the balance walk
is only **empirically/a.e. supercritical** (running min `= 17` constant is `[OBSERVED]`). Even granting the a.e. drift
`0.5`, the elementary run ceiling `0.585·index` exceeds it (`0.585 > 0.5`), so a late near-maximal run could overcome
it — the elementary bounds are consistent with both halting and non-halting, failing to close by `1.17×`. Both
missing pieces — the drift lower bound AND the run upper bound — are `(K)`-grade (depth-tail control). This unifies
the RG criticality (§6), the even-count floor (`EVEN_COUNT_FLOOR.md`), and the halting criterion into one walk
picture, and quantifies the elementary deficit (`1.17×`).

## 8. Linearized RG at the fixed points — NO discrete critical exponent (brick, negative, 2026-07-01)

Tested whether the halting transition is an RG **critical phenomenon** with a universal exponent, by linearizing
`R` at the fixed-point line. With `p^{(a)}_e=a(1-a)^{e-1}`, the linearization is
`(DR\,\delta)_e = [\delta_{e+1} + p^{(a)}_e\,\delta_1]/(1-a)` (a weighted backward shift plus a rank-one term).

- **(L1) Dominant relevant eigenvalue `= 1/(1-a)` `[OBSERVED, robust]`.** Numerically (`scratchpad/rg_linearized.py`,
  truncation `K=80`) the top eigenvalue is exactly `1/(1-a)` (`2.0` at Haar, `3.0` at `a=2/3`, `1.5` at `a=1/3`) — the
  tail-rate relevant direction, scaling the relevant coordinate by `1/(1-a)` per renormalization.
- **(L2) NO discrete critical exponent at `a=2/3` `[verdict]`.** The dominant eigenvalue `1/(1-a)` varies
  **smoothly** through `a=2/3` (no singularity, no special value); the rest of the spectrum is the **continuous
  spectrum of a weighted shift** (the apparent band `≈1.17–1.27` and "many relevant eigenvalues" are truncation
  artifacts, not real — flagged, not used). So the criticality at `a=2/3` is **not** a feature of the RG flow's
  spectrum; it lives **only in the drift observable** (the balance walk's zero-drift point, §7). The
  "critical-phenomenon-with-universal-exponent" hope does **not** materialize.
- **(L3) Honest takeaway.** The theory's architecture is now coherent and closed at the mean-field level: a
  renormalization line of geometric fixed points with one smooth relevant direction (tail rate, eigenvalue
  `1/(1-a)`), and a separate **drift observable** whose sign change at `a=2/3` (`meanD=3/2`) is the halting
  transition. There is no extra hidden critical structure to exploit; the kernel remains the quenched seat + the
  `0.585>0.5` fluctuation gap = `(K)`.

**Net (today's bricks R,F,W,L):** the occupancy-profile theory has an exact renormalization symmetry (R), an RG flow
with a fixed-point line and tail-rate relevant direction (F), a balance-walk criticality at the zero-drift point
`a=2/3` with the quantified `0.585>0.5` elementary deficit (W), and a smooth linearized RG with no discrete critical
exponent (L). This is a coherent first-moment / mean-field architecture for the kernel; everything quenched +
second-moment is `(K)`.

## 9. The mean-field architecture is family-wide (brick, 2026-07-01)

The bricks (R), (F), (L) are **not Antihydra-specific**: they port to the entire BB(6) Mahler cryptid family
`{μ : v_p(μ)=−1}` (the shared kernel of `CRYPTID_KERNEL.md`: `T_μ(x)=⌊μx⌋` is a `p`-to-1 exact endomorphism of
`ℤ_p` for every such `μ`).

- **(U1) Geometric depth law `q=1/p`, mean `p` `[PROVEN-in-family / OBSERVED]`.** The gap (depth) law is geometric
  `P(D=d)=(1/p)(1-1/p)^{d-1}` (mean `p`), a direct consequence of the `p`-to-1 exact endomorphism. *Verified*
  (`scratchpad/family_rg.py`, `N=3·10⁵`): `3/2,5/2` (`p=2`, geom `q=½`, mean `2`), `8/3,4/3` (`p=3`, geom `q=⅓`,
  mean `3`: `0.333,0.222,0.148,…`).
- **(U2) Renormalization shifts mean by `+1`, all members `[OBSERVED]`.** Inducing on `{D≥2}` shifts the mean depth
  by exactly `+1` for every member (`2→3` at `p=2`; `3→4` at `p=3`) — the `A_k` renormalization tower (R) is
  family-wide.
- **(U3) Universal RG, member sits at `a=1/p` `[PROVEN]`.** The RG operator `R(p)_e=p_{e+1}/(1-p_1)` on depth-law
  space is `p`-independent; its fixed-point line (all geometrics) is universal; the family member at prime `p` sits
  at the fixed point `a=1/p` (mean `p`), with linearized relevant eigenvalue `1/(1-a)=p/(p-1)` (`2` at `p=2`, `3/2`
  at `p=3`).
- **(U4) Only the criticality threshold is per-machine `[scope]`.** The halt-criticality (W) — the zero-drift point
  of the machine's balance/halt observable — is machine-specific (Antihydra: even-density, `meanD=3/2 ⟺ a=2/3`;
  o18: frontier-bit; o15: block-collision — `CRYPTID_KERNEL.md`). The *shared* structure is the RG fixed-point line
  + relevant direction; each machine's halt predicate selects a critical point on it.

**Net (U):** the occupancy-profile / RG mean-field architecture is a **single unified theory for the BB(6) Mahler
core** (Antihydra, o10-inner, o18, o15, …), not an Antihydra coincidence: one RG fixed-point line of geometric depth
laws, each family member at `a=1/p`, relevant eigenvalue `p/(p-1)`, with per-machine halt-criticality. This upgrades
`CRYPTID_KERNEL.md`'s "one kernel, one obstruction" to "one kernel, one obstruction, **one mean-field RG
architecture**."

## 10. Second-moment / large-deviation layer — the golden-ratio Cramér exponent (brick, 2026-07-01)

The fluctuation layer above mean-field: the balance walk's downward-deviation exponent, exactly.

Per induced step `j` (spanning `D_j` base steps: one odd `+` `D_j-1` evens), the balance increment is
`X_j = 3(D_j-1) - D_j = 2D_j - 3` (mean `2·\mathrm{mean}D - 3 = +1` at Haar; **bounded below by `-1`**, at `D=1`).
Halting `⟺` the partial sums of `X_j` go negative. For a positive-drift walk the downward-deviation probability is
governed by the **Cramér/Lundberg exponent** `θ^*>0` solving `E[e^{-θ^*X}] = 1`.

- **(C1) The exponent is `θ^* = \log φ` (golden ratio), EXACTLY `[PROVEN]`.** With `D~`geom(`2^{-d}`),
  `E[e^{-θX}] = e^{θ}/(2 - e^{-2θ})`; setting `=1` and `x=e^{-θ}` gives `x^3 - 2x + 1 = 0 = (x-1)(x^2+x-1)`, whose
  relevant root is `x = e^{-θ^*} = (\sqrt5-1)/2 = 1/φ`. Hence **`θ^* = \log φ`**, `φ=(1+\sqrt5)/2`, and the balance
  walk's downward excursions decay as `P(\text{dip by }s) ≈ φ^{-s} = ((\sqrt5-1)/2)^s ≈ 0.618^s`.
- **(C2) Verified on the orbit `[OBSERVED]`.** The seed-27 orbit's increments `2D_j-3` have mean `0.9948` (`≈+1`),
  min `-1`, and `E[e^{-θ^*X}] = 1.0009 ≈ 1` (the i.i.d. tilt matches); the induced partial-sum running minimum is
  bounded (`12`, after burn-in), i.e. the walk escapes — consistent with non-halting.
- **(C3) The annealed halting heuristic `[HEURISTIC, annealed]`.** With balance `B_J ≈ J` (drift `+1`/induced step),
  the i.i.d. halting-probability proxy is a **tail sum from a post-transient offset** `J_0`,
  `Σ_{J≥J_0} φ^{-B_J} ≈ Σ_{J≥J_0} φ^{-J}` — small and finite (`≈1.7·10^{-4}` at `J_0=20`, `≈7.3·10^{-4}` at `J_0=17`;
  the value is offset-dependent, NOT a clean constant — the naive full sum from `J=1` is just `φ`). The point is only
  that it is small: the probabilistic "non-halting is near-certain" statement. This is the **annealed / a.e. wall** —
  it treats the depths as i.i.d.; the quenched single orbit's actual minimum is `(K)`.

> **(C4) Scope.** `θ^*=\log φ` is an *exact, provable* structural constant of the Antihydra-class balance walk, and
> the LDP gives the precise annealed non-halting heuristic. It is **annealed** (i.i.d. depths) — the quenched seat
> (the real orbit's depths are deterministic, not i.i.d.) is `(K)`. The exponent is **halt-predicate-specific** (like
> the criticality (W)/(U4)): `θ^*=\log φ` is the `3/2` / even-density-`≥1/3` value; other family members have their
> own Cramér exponent from their own increment law.

**Net (C):** the second-moment layer yields the **exact golden-ratio Cramér exponent `θ^*=\log φ`** for the
Antihydra balance walk (`P(\text{dip }s)≈φ^{-s}`), verified on the orbit, giving the precise annealed non-halting
heuristic (`≈1.7·10^{-4}`). A clean, exact, provable structural constant — and the boundary is sharp: the LDP is
annealed, the quenched minimum is `(K)`.

## 11. The quenched orbit obeys the golden-ratio LDP — i.i.d.-indistinguishable at second order (brick, 2026-07-01)

Tests whether the *deterministic* seed-27 orbit actually realizes the annealed golden-ratio LDP of §10
(`scratchpad/quenched_ldp2.py`, exact big-int, `N=3·10⁵`).

- **(Q1) Drawdown decays at `1/φ` `[OBSERVED]`.** The balance walk's drawdown `runmax−B_n` has
  `P(\text{draw}=s)/P(\text{draw}=s-1) ≈ 0.62` for all `s=1..11` (`0.6215, 0.6161, 0.6211, 0.6145, 0.6258, 0.6075,
  0.6159, 0.6016, 0.6283, 0.6268, 0.6170`) — matching `1/φ = 0.6180` (the §10 exponent) to within sampling noise;
  the tail `s≥12` wobbles on small counts. So the **quenched orbit obeys the golden-ratio LDP**.
- **(Q2) Depth tail is exactly geometric `[OBSERVED]`.** `P(D≥k) = 0.49980, 0.24937, 0.12425, 0.06191, …` vs
  `2^{1-k} = 0.5,0.25,0.125,…` — geometric (Haar) to 4 digits; `max D = 17`.
- **(Q3) Large depths are Poisson-spread (no clustering) `[OBSERVED]`.** `D≥8` events (`n=1167`) have mean gap
  `128.6` (vs `2^7=128`) and **coefficient of variation `1.022 ≈ 1.0`** — the i.i.d./Poisson value. The rare
  large-depth events that drive halting risk are *not* clustered.

> **(Q4) Reading.** At the **second-moment / large-deviation level**, the deterministic orbit **matches the annealed
> i.i.d. model in every tested second-moment statistic to within sampling noise at `N=3·10⁵`**: its drawdown law
> (`1/φ`), depth tail (`2^{1-k}`), and large-depth spacing (Poisson, `CV≈1`) show no detectable deviation. (This is a
> finite-`N` empirical match, not a proof of full indistinguishability — untested higher statistics or larger `N`
> could in principle deviate.) It *sharpens the heavy-tail / i.i.d.-adversary point* (`EXCURSION_SYNTHESIS.md`): no
> *tested* second-moment statistic separates the orbit from i.i.d., so the gap to `(K)` is **the single-realization
> (quenched-genericity) issue** — proving that the deterministic sequence *attains* the i.i.d. statistics it
> empirically exhibits. That attainment is exactly `(K)`; nothing in the second-moment structure closes it (it
> confirms, with no tested deviation, that the orbit *behaves* annealed).

**Net (Q):** the quenched orbit matches the §10 golden-ratio LDP in every tested second-moment statistic at
`N=3·10⁵` (drawdown `1/φ`, tail `2^{1-k}`, Poisson large-depths), with no detected deviation. This makes non-halting
*morally certain* **`[HEURISTIC]`** and pins the residual gap as single-realization genericity `= (K)`. The
second-moment layer is **descriptively complete and matches (empirically)**, but — exactly as the No-Structure theorem
forbids — a perfect annealed match cannot select the one orbit.

## 12. The Cramér exponent is an n-bonacci constant — golden ratio is the Antihydra (3:1) member (brick, 2026-07-01)

Generalizing §10 from the Antihydra `1/3` threshold to a general `m`-counter (halt `⟺` even-density `< 1/m`, balance
`B = mE - n`). The per-induced-step increment is `X = m(D-1) - D = (m-1)D - m` (drift at `meanD=2` is `m-2`). The
Cramér equation `E[e^{-θ^*X}]=1` becomes, with `x=e^{-θ^*}`,

> **`x^m - 2x + 1 = 0`**, which always factors `= (x-1)(x^{m-1}+x^{m-2}+\dots+x-1)`; the relevant root solves
> `x^{m-1}+\dots+x-1 = 0`, and **`1/x` is exactly the `(m-1)`-bonacci constant**.

- **(N1) The family `[PROVEN, exact]`** (`scratchpad/threshold_cramer.py`):
  - `m=2`: `x=1`, `θ^*=0` — **critical, no decay** (the even-density-`<½` threshold is the zero-drift point at
    `meanD=2`; consistent with §7 criticality).
  - `m=3` (**Antihydra**, the 3:1 even-counter): `x = (\sqrt5-1)/2 = 1/φ`, `θ^* = \logφ` — the **golden ratio**
    (`= 2`-bonacci / Fibonacci constant `1.618…`).
  - `m=4`: `1/x = 1.83929…` (**tribonacci**); `m=5`: `1.92756…` (tetranacci); `m=6`: `1.96595…` (pentanacci); …
    `1/x → 2` as `m→∞`.
- **(N2) Reading.** The halting-threshold `m` indexes the Cramér exponent through the `(m-1)`-bonacci constants;
  Antihydra sits at the **simplest non-trivial counter (3:1)**, whose constant is the **golden ratio**, and `m=2` is
  exactly the critical (zero-drift) boundary. So `θ^*=\logφ` is not an accident of Antihydra but the Fibonacci member
  of a clean algebraic family parameterized by the counter ratio.

> **(N3) Scope.** Still the *annealed* LDP exponent (per threshold); the quenched single-orbit minimum is `(K)`. The
> `n`-bonacci structure is an exact, attractive descriptive constant of the balance-walk, not a step toward selecting
> the orbit.

**Net (N):** the balance-walk Cramér exponent of the `m`-counter is `\log` of the `(m-1)`-bonacci constant; Antihydra
`(m=3)` is the golden-ratio/Fibonacci member, `m=2` the critical boundary, `1/x→2` as `m→∞`. A clean exact family
placing `φ`; annealed, with the quenched seat `= (K)`.

## 13. The full two-parameter `(p,m)` Cramér family — golden ratio at Antihydra `(2,3)` (brick, 2026-07-01)

Combining the prime-`p` family (§9: depth `~` geom mean `p`) with the counter ratio `m` (§12) gives the general
Cramér exponent. With increment `X=(m-1)D-m` and `D~`geom(mean `p`), `E[e^{-θ^*X}]=1` becomes, with `x=e^{-θ^*}`,

> **`(p-1)x^m - p x + 1 = 0`**, always divisible by `(x-1)`; the relevant root `x∈(0,1)` gives `θ^*=-\log x`.
> (`p=2` recovers `x^m-2x+1` of §12.)

- **(P1) Exact values `[PROVEN, sympy-verified]`** (`scratchpad/pm_cramer.py`):
  - `m=2`: `(x-1)((p-1)x-1)`, root `x=1/(p-1)`, `θ^*=\log(p-1)` (`=0` at `p=2` — critical).
  - `m=3`: `(x-1)((p-1)x^2+(p-1)x-1)`, a **quadratic irrational**: `p=2 → x=(\sqrt5-1)/2=1/φ` (golden);
    `p=3 → x=(\sqrt3-1)/2`, `1/x=\sqrt3+1=2.732…`.
  - general `m`: `(x-1)((p-1)(x^{m-1}+\dots+x)-1)`.
- **(P2) Placement.** The BB(6) Mahler cryptids' balance-walk Cramér exponents form a clean **two-parameter algebraic
  family** indexed by `(prime p, counter ratio m)`; **Antihydra `(2,3)` is the golden-ratio point**, the `p=2` slice
  is the `n`-bonacci family, the `p=3` slice starts `(\sqrt3-1)/2`, and `m=2` is `\log(p-1)` (critical at `p=2`).

> **(P3) Scope `[HONEST]`.** These are **annealed** Cramér exponents. For `p≠2` the "`m`-counter" is the *analogous*
> `p`-adic-renewal threshold, a clean **template**; the *actual* o18/o15 exponents depend on their real
> (machine-specific) halt predicates (frontier-bit / block-collision, `CRYPTID_KERNEL.md`), which are not literal
> `m`-counters — so `(p=3,m)` here is the template value, not a claim about o18's exact exponent. The quenched seat
> is `(K)` throughout.

**Net (P):** the second-moment layer's Cramér exponent is a two-parameter algebraic family `(p-1)x^m-px+1=0`, unifying
the whole BB(6) Mahler core, with Antihydra `(2,3)` the golden-ratio member and explicit quadratic-irrational /
`n`-bonacci values elsewhere. Annealed template; quenched `= (K)`. **No machine decided. No label upgraded.** `(K)`
remains `[OPEN]` = Mahler 3/2 / AEV.
