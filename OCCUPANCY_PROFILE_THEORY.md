# Foundation of the occupancy-profile theory (the new theory's scaffolding, built solo) (2026-06-30)

*First foundation block of the multi-year, self-contained ("we do it ourselves") theory-building effort. It does
NOT advance the frontier toward `(K)`; it sets up the central object cleanly, states the provable scaffolding, and
isolates the single open axiom the theory must eventually supply. HONEST SCOPE: every provable lemma here is either
the today-proven identity or the known Haar/Bernoulli structure; the open core is quenched = `(K)`. This is durable
framework-foundation work, NOT new progress on the kernel. SOUNDNESS labels throughout. NOT committed by default.*

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
- **(S4) The kernel in profile terms.** `(K) ⟺ liminf_J N_2(J)/J ≥ 1/2` (the ψ-form / `freq(D≥2)≥½` sufficient
  case) and more sharply `mean D ≥ 3/2 ⟺ liminf_J (Σ_{k≥2}N_k)/J ≥ 1/2`. So the **entire kernel is the top-rung
  asymptotic density of the profile.**

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
first-moment / mean-level structure; the quenched seat and the second-moment fluctuation control remain `(K)`. A
natural long-haul next brick: the **linearized RG at the critical fixed point `a=2/3`** (is the halting transition a
critical phenomenon with a characteristic exponent? does the second-moment / fluctuation operator have a computable
spectrum there?). **No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
