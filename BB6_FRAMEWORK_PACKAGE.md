# Antihydra (BB(6)) non-halting as single-orbit equidistribution of ×(3/2): a proven structural obstruction, placed in the ×2,×3 rigidity program

*Externally-shareable framework package. Assembled (2026-06-30) from the BB(6)/Antihydra program's
machine-verified reduction, its two impossibility meta-theorems, and its solenoid measure-rigidity placement.
**Soundness discipline.** Every claim is labelled `[PROVEN]` (machine-verified or elementary, in this program),
`[PROVEN-in-lit]` (established theorem cited from the literature), `[CONJECTURE]` / `[OPEN]` (not established).
No label is upgraded; no claim is made to prove the kernel `(K)`; the scope of every theorem is delimited
honestly. Numerical observations are flagged `[OBSERVED]` and never substitute for a proof.*

Audience: homogeneous dynamics / measure rigidity / number theory (AEV authors;
Einsiedler–Lindenstrauss–Host circle; the Tao circle). The package leads with what is proven and states the
precise place every known method breaks.

---

## 1. Abstract

Antihydra is a 6-state, 2-symbol Turing machine on the bbchallenge BB(6) frontier whose halting is equivalent
to a clean arithmetic-dynamical question about the orbit `c_0=8`, `c_{n+1}=⌊3c_n/2⌋`. We record an unbroken
chain of `[PROVEN]`, machine-verified equivalences reducing **Antihydra never halts** to **single-orbit
equidistribution of `c_n mod 2^k`** for the specified seed — the one-sided, single-level, single-orbit,
*floor-mirror* fragment of the Andrieu–Eliahou–Vivion (AEV) normality conjecture (arXiv:2510.11723), which
implies Mahler's 1968 3/2 problem. We then prove that this residual obstruction is **structural, not a gap in
technique**: a `[PROVEN]` *No-Structure-Only-Selection* theorem shows that no certificate drawn from the
bounded-residue (coboundary), all-orbits (topological/specification), or measure-level (annealed/ergodic)
registers can decide the criterion for the specified seed, because each such register assigns the seed the same
verdict it assigns to a genuinely *halting* orbit (the fixed point `o=1`, an ergodic-optimization maximizer of
weight `+1/2`). An obstruction dichotomy organizes ~20 independent attack routes as instances of one proven
boundary: *topological-closure / tail / first-moment determined* (free) versus *Haar-selecting within the
feasible invariant-measure set* (kernel-hard). Finally we place the kernel in the Rudolph–Johnson / Furstenberg
×2,×3 program: on the `(2,3)`-adic solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, `A=×(3/2)=M_3 M_2^{-1}` is a **rank-1 line in
the rank-2 host `⟨×2,×3⟩`**, and `(K)` is equivalent to genericity of the seed for `A`, which by the
**proven** Rudolph–Johnson theorem follows from **two** open inputs — `(AIU)` host-invariance upgrade and
`(ENT)` positive 2-adic measure entropy. Both are strictly weaker than `(K)`, both are `(K)`-hard, and we prove
they are logically **independent**. The package isolates these two inputs as the precise, expert-facing targets.

> **One sentence.** Antihydra non-halting reduces (machine-verified) to single-orbit equidistribution of the
> `×(3/2)`-orbit of `8`; we prove the obstruction is structural (No-Structure theorem) and reduce the kernel,
> on the `(2,3)`-solenoid, to two open inputs (AIU + positive entropy) that feed the **proven** Rudolph–Johnson
> theorem.

---

## 2. The reduction chain `[PROVEN, machine-verified]`

Antihydra's computation tracks the integer orbit `c_0=8`, `c_{n+1}=⌊3c_n/2⌋`, counting `E_n :=` (number of even
values among `c_0,…,c_{n-1}`). With **balance** `balance_n := 3E_n − n`, the machine **halts iff `balance_n < 0`
for some `n`** (a maintained counter underflows). The links below are each labelled with the powering lemma.

**Link 0 — Halting → density. `[PROVEN]`**
never halts `⟺ balance_n ≥ 0 ∀n ⟺ E_n/n ≥ 1/3 ∀n`. Sharp: if `liminf E_n/n < 1/3` then `balance_n→−∞` along a
subsequence and the machine halts, so the `1/3` threshold is exact.

**Link 1 — GAP LEMMA: induced odd map. `[PROVEN]`** (verified to `N=10^5`, 0 exceptions.)
For odd `c_i`, with `D := v_2(3c_i−1)`, the next odd value is reached in exactly `D` steps. This collapses the
orbit to its **induced odd return map**
> `T(o) = 3^{D−1}(3o−1)/2^D`, `D = D(o) = v_2(3o−1)`, started at **`o_0 = 27`** (from `8→12→18→27`).

**Link 2 — Renewal identity: density ↔ mean `D`. `[PROVEN]`**
Even steps are renewal points with inter-renewal gaps `=D`; Kac/renewal gives even-density `= 1 − 1/(mean D)`,
hence even-density `≥ 1/3 ⟺ mean D ≥ 3/2`.

**Link 3 — Valuation formula → one-sided cylinder form. `[PROVEN]`**
Since `3∈ℤ₂^*`, `D≥k ⟺ o≡3^{-1} (mod 2^k)`, so `mean D = Σ_{k≥1} freq(o≡3^{-1} mod 2^k)`, the `k=1` term `≡1`.
Thus `mean D ≥ 3/2 ⟸ freq(o≡3 mod 4) ≥ 1/2`, and `D=1⟺o≡1 mod 4`.

**The chain `[PROVEN]`:** non-halt `⟺` even-density `≥1/3` `⟺` `mean D ≥ 3/2` (these three mutually **equivalent**, Kac)
`⟸` `liminf freq(D≥2) ≥ 1/2` `⟸` single-orbit equidistribution of `c_n mod 2^k`. The last two links are `⟸`
(**sufficient, strictly stronger**), not `⟺`: `mean D = 1+Σ_{k≥2} freq(D≥k)`, so `freq(D≥2)≥1/2` (and the ψ-form,
which truncates the tail at `D≥3`) imply `mean D≥3/2` but not conversely; full equidistribution is stronger still.

**Measure side `[PROVEN]`.** `T` is **Haar-preserving, exact, and Bernoulli on `ℤ₂^*`**, with gap exponents
`D_j` i.i.d. geometric `P(D=d)=2^{−d}` (mean 2). Under Haar `mean D = 2 > 3/2` with CLT and exponential
large-deviation concentration; the entire remaining problem is whether the **single deterministic orbit `o_0=27`
is Haar-generic** (Lagarias 2-adic conjugacy; Bernstein–Lagarias 1996; Matthews–Watts).

**Example side `[PROVEN by arithmetic]`.** Periodic-itinerary exclusion (cycle points `c_0=N/(3^q−2^q)∈[0,1]`,
the only integers being `{0,1}`; the integer orbit is strictly increasing, hence reaches no cycle — verified all
2046 cycles of period `q≤10` + general bound); the Countdown Lemma (`φ(o)=v_2(o−1)` drops by 1 per `D=1` step);
the Dual-Repulsion Lemma (the fixed point `o=1` repels at both `∞` and `2`); the `v_3` identity
`v_3(o_{j+1})=D_j−1`.

> **Kernel `(K)` `[OPEN]`.** The non-halt-**equivalent** kernel is `mean D ≥ 3/2` `⟺` `liminf` even-density `≥1/3`
> (Kac). **Sufficient** (strictly stronger, `⟹`) forms: `liminf freq(o≡3 mod 4) ≥ 1/2`; the ψ-form
> `liminf_N (1/N)#{n<N : D(o_n)≥2} ≥ 1/2`; 3-adic `density{3|o_j}+density{9|o_j} ≥ 1/2`; single-orbit equidistribution
> of `c_n mod 2^k`; equidistribution of `8·(3/2)^n mod 1`.

A complete non-halting proof is `(K)` **together with** the finite check `balance_n ≥ 0` for `n≤N_0`, verified
to `N_0 = 2·10^5` (min balance `+2`). `(K)` is the **floor-mirror** of the AEV `p/q=3/2` instance (AEV uses the
ceiling `(3x+1)/2`; the `±1` flips parity, so the two are *not* literally conjugate; the GAP-LEMMA bookkeeping
is the bridge), and is **strictly weaker than AEV on three axes** (one-sided not two-sided; level `k=2` not all
`k`; one orbit not all `n`). No named conjecture sits at this weaker level: AEV is the weakest established-open
named conjecture that implies `(K)`.

---

## 3. The No-Structure-Only-Selection theorem `[PROVEN]`

This is the formal core: no certificate from the structural registers can prove `(K)`. Define the violation
observable `ψ(o) := ½ − 1{D≥2} − 1{D≥3}` (a function of `o mod 8`); then `(K) ⟺ limsup_N (1/N)Σ_{j<N} ψ(o_j) ≤ 0`.
The Haar mean is `∫ψ dHaar = −1/4`, so `(K)` holds on average / a.e.; the question is the one orbit.

**Three structural certificate classes.**
- **(C1) Bounded residue sub-action (coboundary):** a bounded `g:(ℤ/2^kℤ)^*→ℝ` with `ψ(o) ≤ g(T o)−g(o)` for
  **all** odd `o` (telescoping would give `(K)` for *every* orbit).
- **(C2) Universal / all-orbits:** any argument proving `limsup(1/N)Σψ ≤ 0` for every orbit (no data singling
  out `o_0`).
- **(C3) Measure-level / annealed:** any argument concluding from the invariant measure (Haar/Bernoulli ergodic
  theorem, decay of correlations, CLT) — a `μ`-a.e. statement.

> **Theorem (No structure-only selection of `o_0`). `[PROVEN]`** No certificate in (C1), (C2), (C3) proves `(K)`:
> 1. **(C1) infeasible.** No bounded `g` on any `(ℤ/2^kℤ)^*` satisfies `ψ ≤ g∘T − g` pointwise. By LP duality
>    (max-mean-cycle / Bellman–Ford), such `g` exists iff `sup_ν ∫ψ dν ≤ 0` over `T`-invariant `ν`; but the
>    fixed point `o=1` (`T(1)=1`, `D=1`, `ψ=+½`) gives the atom `δ_1` with `∫ψ dδ_1 = +½ > 0`, realized as a
>    weight-`+½` self-loop at residue `1` for every `k≥3`. Solved exactly (`Fraction` arithmetic, `k=3..12`,
>    level-independent, conservative tail treatment); the reachable residue component from `27 mod 2^k` is the
>    whole graph, so no residue-domain restriction evades it.
> 2. **(C2) impossible.** `T` is full-branch (each cylinder `A_d` maps onto `ℤ₂^*`), so it has the
>    **specification property**; by multifractal analysis (Takens–Verbitskiy; Sigmund) every interior Birkhoff
>    value of `1{D≥2}` is attained on a **full-Hausdorff-dimension** set of orbits, with extrema `0` (at `δ_1`)
>    and `1` (at the `ℤ₂`-fixed point `o=3/5`). Hence a full-dimension set of orbits has `liminf freq(D≥2)<½`:
>    `(K)` is non-universal.
> 3. **(C3) insufficient.** Exactness + Bernoulli give `(K)` for Haar-a.e. start, but `{o_0}` is countable hence
>    `μ`-null, and the non-generic set has full entropy and full Hausdorff dimension (Barreira–Schmeling 2000).
>
> Therefore any proof of `(K)` must use data **distinguishing** the orbit of `o_0` from the violating orbits —
> its magnitude / reachability / arithmetic — which is exactly single-orbit equidistribution `= (K)`.

**Honest scope.** The theorem rules out the entire free-side machinery (bounded residue sub-actions;
universal/all-orbits bounds; measure-level/annealed arguments) and localizes the irreducible content to one
named arithmetic statement. It does **not** prove `(K)` undecidable, independent, or false, and does **not**
preclude a proof that *does* use orbit-specific arithmetic. The one variant the LP does not kill is a
**magnitude-aware, unbounded** Lyapunov `g(o)=α log o + h(o mod 2^k)` (`α<0` coupling to the size drift
`D log(3/2)`); but it cannot see `δ_1` (where `log` is constant) as a global obstruction, so it works only as a
**conditional** certificate above a threshold, reintroducing the avoidance/genericity content `= (K)`. `[OPEN]`

**Why the obstruction is the *halting* fixed point.** A second, independent meta-theorem (shared-free-structure)
reaches the same conclusion from the contraction algebra: the halting fixed point `o=1` (`D≡1`) synchronizes
under the *same* free 3-adic contraction as the real orbit, so every "free" (finite-window / pathwise) condition
also holds at `o=1`; since `o=1` halts, no free condition can imply non-halting. The free part is blind to
`freq(D≥2)`, the sole discriminator. Both meta-theorems are the same obstruction seen twice: the maximizer of
the invariant simplex is the atom `δ_1`, and the free structure is shared with `o=1`. This is *why* every
structural attack (contraction, bootstrap, van der Corput, Mauduit–Rivat, twisted RPF, residue, coboundary,
adelic coupling) only relocated the gap.

---

## 4. The obstruction dichotomy `[PROVEN core + organizing principle]`

Across ~20 independent attack routes the proven/open boundary is always the **same** boundary. Let `Ω` = the
orbit closure of seed `8` under `A`. Three invariant-measure sets:
- **`M_orb`** = weak-* limits of the seed-8 empirical measures; **`(K) ⟺ M_orb = {Haar}`**.
- **`M_feas`** = invariant measures on `Ω` consistent with all PROVEN (topological + first-moment) constraints;
  `{Haar} ⊊ M_feas ⊊ M_sys` (specification keeps `M_feas` non-trivial).
- **`M_sys`** = the specification / ergodic-optimization set of the system, **full Hausdorff dimension**,
  containing the halting atom `δ_1` and every interior Birkhoff value `[PROVEN]`.

> **HARD direction (the rigorous core). `[PROVEN]`** Let `Φ` be a bounded empirical-measure functional, not
> constant on `M_feas`, with `Φ(Haar)` a `(K)`-target. Then no argument using only orbit-closure / topological /
> first-moment / annealed data proves `Φ(seed-8)=Φ(Haar)`; establishing it is equivalent to `M_orb={Haar} = (K)`.
> *Proof.* Such data is shared by every measure in `M_feas` (it *defines* `M_feas`), so any argument from it is
> constant on `M_feas` and cannot separate Haar from the others. `M_feas` genuinely contains non-Haar measures
> (ergodic optimization: `β = max_μ ∫(θ−ϕ)dμ = +½ > 0` attained off Haar; specification: every interior Birkhoff
> value on a full-dimension set). ∎

**FREE direction (observed organizing principle).** Every unconditionally proven result sits in one of two free
registers: **(R1) measure-constant / first-moment / annealed** (conservation laws and counts holding for all of
`M_feas`); **(R2) topological / tail / growth** (facts about `Ω` or the tail that are *not* measure functionals
and survive measure-degeneration). Neither register can reach a hard functional.

**Red-team correction (banked, `DICHOTOMY_REDTEAM.md`).** The naive biconditional "free `⟺` constant on `M`" is
**false on its free half**: e.g. `#even(n)≥0.89 log n`, subword complexity `≥1.71ℓ`, non-periodicity, and
top-digit equidistribution are all PROVEN yet *fail at `δ_1∈M_sys`* (they are topological/tail facts, not measure
functionals — `#even→∞` is finer than any empirical measure). Resolution: `M_sys` (which contains `δ_1`) is the
correct **HARD-side witness** but the wrong **FREE-side test**; the free side is determined by `Ω` plus the
universal identities (`M_feas`), and includes the topological/tail register. The HARD half is sound and
**proven-backed** (`β=+½` forbids any hard-but-constant counterexample). The clean boundary is
**topological-closure-determined (free)** vs **Haar-vs-`M_feas`-separating (hard)** — the topological-entropy /
measure-entropy split, promoted to the global organizing principle. Conditional "if X then halt" theorems and
the certificate-complexity hierarchy are a **separate register** (morphisms / descriptive invariants), free in
their own sense, orthogonal to the measure axis.

**Catalogue (every route is one instance of the single boundary).**

| Route | FREE side (proven) | HARD side (= (K)) | boundary crossed |
|---|---|---|---|
| Reduction chain | halt ⟺ even-density<1/3 | even-density value | identity vs frequency |
| Valuation budget | `ΣD_i=n` (1st moment) | density / `E[K²]` | 1st moment vs 2nd |
| Endogenous-UE | gap on EVEN block | ODD block `L_ann χ_odd≡0` | spectral vs frequency |
| Carry / 2nd diagonal | annealed marginal `=ν_{2/3}` (Rajchman) | quenched single-orbit | annealed vs quenched |
| AIU | `(K)⟹AIU` | `(×2)_*μ=μ` (host-inv) | constant vs Haar-selecting (neutral dir.) |
| ENT | topological entropy `=log2` | measure entropy `h_μ>0` | topological vs measure entropy |
| Non-atomicity | orbit avoids periodic (per-visit) | `μ` charges zero mass (occupancy) | avoidance vs occupancy |
| `E[K²]<∞` | `ΣK_i≤N` (count) | `ΣK_i²` (weighted tail) | 1st moment vs 2nd |
| separation | min-gap (birthday-scale) | density / occupancy | min-gap vs frequency |
| top-digit | top `Θ(log N)` digits (Weyl) | moving middle digit | leading vs diagonal |
| uniform AEV | a.e.-`α` (Koksma) | specified `α=8` | a.e. vs specified |
| computability | finite-state-random level | specific computable point | level vs point |

The durable contribution: this converts "we tried many things and they all failed" into "the proven and the open
are separated by a single, identified, **proven-to-be-real** boundary, and `(K)` is precisely the one functional
that crosses it."

---

## 5. The solenoid placement: `(K)` in the Rudolph–Johnson / Furstenberg ×2,×3 program

**The host `[PROVEN]`.** Let `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` (compact abelian S-arithmetic **solenoid**; `ℚ₂,ℚ₃` adjoined so
that `½,⅓` are invertible). For `u∈ℤ[1/6]^×` the multiplication `M_u` is an automorphism of `X` with dilations
`(|u|_∞,|u|_2,|u|_3)`. Then `M_2,M_3∈Aut(X)` commute and are hyperbolic, and

> `A := M_{3/2} = M_3 M_2^{-1}` is a **rank-1 line `ℤ·(−1,1)` inside the rank-2 host `Φ=⟨×2,×3⟩≅ℤ²`**,

with dilations `A:(3/2,2,1/3)` (hyperbolic, no neutral direction), `M_2:(2,1/2,1)`, `M_3:(3,1/3,1)`. The seed
`8∈ℤ[1/6]` embeds adelically; every weak-* limit `μ` of its `A`-orbit empiricals is `A`-invariant
`[PROVEN, Krylov–Bogolyubov]`, and **`(K) ⟺ μ = Haar`** (the rational point `8` is `A`-generic). The famous
×2,×3 rigidity **does act on this space** — the program's earlier "rank-2 unavailable" verdict was about the
group we *iterate* (`⟨3/2⟩`), and is wrong for the *host*.

**Two gaps to Haar (corrected; an earlier "one gap" claim was withdrawn).**
> **Lemma `[PROVEN]`.** (i) A `Φ`-invariant ergodic limit `μ` for seed `8` has **full support** (Berend
> topological set-rigidity + periodic-exclusion). (ii) `Φ`-invariant ergodic **+ positive entropy `h_μ(M_2)>0`**
> ⟹ `μ=`Haar (**Rudolph 1990 / Johnson 1992, solenoid form, arXiv:2101.11120**). The entropy hypothesis is
> essential; without it, forcing Haar from `Φ`-invariance is **Furstenberg's conjecture (OPEN)**.

Berend gives only a topological **set**-conclusion (full support), *not* a measure conclusion; equating the two
was the over-claim, now withdrawn. Concretely Berend applies to the **rank-2 host** orbit `{2^a 3^b·8}` (dense in
`X`), but gives **nothing** for the rank-1, virtually-cyclic `A`-orbit. Hence:

> **`(K) ⟺ μ=Haar ⟸ (AIU) ∧ (ENT)`**, the conjunction invoking the **proven** Rudolph–Johnson.

**(AIU) — Arithmetic Invariance Upgrade `[CONJECTURE]`.** The `A`-invariant limit `μ` is invariant under the full
host `⟨×2,×3⟩`, not merely under `A`. Equivalently `(×2)_*μ=μ`; equivalently (seed-shift form, `[PROVEN]`
reformulation) `μ` is constant on the `ℤ[1/6]^×`-coset of the seed, i.e. `μ_8=μ_16`.
- **Leafwise form `[PROVEN equivalence]`.** Disintegrating along the `A`-stable `ℚ₃`-foliation, AIU `⟺` the
  conditionals `μ_x^3` are `ℤ₃^*`-rotation-invariant (spherically Haar). (Uses: `2` is a primitive root mod
  `3^k`, so `⟨2⟩` is dense in `ℤ₃^*`.)
- **AIU is a NEUTRAL-direction statement.** The surplus invariance AIU needs is `×2` acting on the `ℚ₃` place,
  where `|2|_3=1` — an **isometric rotation, zero Lyapunov exponent, zero entropy**. The
  Einsiedler–Katok–Lindenstrauss high-entropy method manufactures invariance only along expanding/contracting
  coarse-Lyapunov directions that *carry* entropy; it is structurally blind to neutral (central) directions. The
  positive entropy `μ` carries lives at `∞/2` (the (K)-bit axis), **transverse** to the neutral `ℚ₃`-rotation AIU
  needs `[PROVEN — method-applicability obstruction]`. Host (1995) is the nearest partial but needs a *second
  multiplicatively-independent expanding ergodic* map (we have only `A`; `×2|_{ℚ₃}` is isometric), yields
  *a.e.-point normality* not measure-invariance, and is a.e. not the specified seed. The adelic coupling
  `v_3(o_{j+1})=D_j−1` makes the `ℚ₂`,`ℚ₃` disintegrations **deterministically dependent** — the wrong side for
  any joinings/disjointness argument.

**(ENT) — positive 2-adic measure entropy `[CONJECTURE]`: `h_μ(M_2)>0`.**
- **Direction settled `[PROVEN]`.** Haar has `h_Haar(M_2)=log2`, `h_Haar(A)=log3`. Hence `h_μ(M_2)=0 ⟹ μ≠Haar ⟹
  (K) FALSE`: **zero entropy is the (K)-false regime**, not a Furstenberg corner. *(An earlier draft hedged that
  the limit measure is "plausibly zero-entropy ⟹ a Furstenberg corner"; that was a sign error — it confused the
  lower bound `p(ℓ)≥1.71ℓ` with the sub-exponential upper bound `h_top=0` would require, and the measured
  complexity is full, `h_top=log2`. Retracted; see `LIMIT_MEASURE_ENTROPY.md`.)* So `h_μ(M_2)>0` is a
  **necessary** consequence of `(K)`, not strictly easier.
- **Ledrappier–Young `[PROVEN reduction]`.** With explicit constant Lyapunov exponents, `ENT ⟺ γ_∞^{(2)}>0` (a
  single conditional/transverse dimension `>0`) `⟺` the `A`-stable `ℚ₃`-conditionals are positive-dimensional
  (non-atomic). L–Y collapses ENT to one number `γ`; it does **not** lower-bound `γ`. Pressure gives only the
  vacuous upper bound `h_μ ≤ h_top=log2`; large-deviation and the proven Gibbs–Markov renewal give positivity
  only for Haar/SRB-typical points, never the named Haar-null seed. The obstruction is exactly
  **frequency-weighted/quenched (= equidistribution = (K)) vs unweighted/support/annealed (proven, rate ≥0)**.

**The two inputs are logically independent `[PROVEN]`.** `ENT ⇏ AIU` (non-atomic conditionals need not be
rotation-invariant; the AIU direction is neutral, beyond the high-entropy method's reach) and `AIU ⇏ ENT` (a
`Φ`-invariant zero-entropy measure satisfies AIU without ENT; `×2`, a `ℚ₃`-unit, cannot pin the entropy/valuation
law). Both are strictly weaker than `(K)` as statements, yet both are `(K)`-hard for *this* orbit with no proven
shortcut. The honest placement:

> **`(K)` follows from `AIU ∧ (h_μ(M_2)>0 ∨ Furstenberg)`.** The live route is the **positive-entropy branch via
> the proven Rudolph–Johnson** (`h_μ(M_2)>0 ⟹ μ` non-atomic automatically, so this branch needs only AIU + ENT).
> The Furstenberg branch needs three open inputs (AIU + non-atomicity + the open Furstenberg conjecture).

**Novelty (literature swept).** No result takes a single rank-1 sub-orbit of a rank-2 abelian solenoid
automorphism action and upgrades its empirical measure to the full rank-2 invariance. The literature has (i)
rank-2 rigidity on solenoids and (ii) rank-1 non-rigidity (Einsiedler–Lindenstrauss JMD 2008: uncountable simplex
of invariant measures, including positive-entropy ones — the structural reason no specified-point theorem
exists), but **not the bridge** between a rank-1 orbit and the rank-2 invariance class. AIU names that bridge.

---

## 6. Banked unconditional partials (the honest positive results)

All `[PROVEN]` for the specified seed unless marked `[PROVEN-in-lit]`; numerics re-verified at `N=3·10^5`,
exact big-int. Each lands strictly inside the **annealed / a.e. / wrong-order** tier; the gap column is the
quenched-single-orbit-positive-density content the kernel needs.

| # | Result | Status | Gap to `(K)` |
|---|---|---|---|
| 1 | `#even(n) ≥ 0.89 log n` (`c≈1/log₂2.17`, from growth `bitlen(c_p)=0.585p+O(1)`) — the single tightest unconditional density-style statement | `[PROVEN]` | `log n` floor vs needed `εn`; marginally consistent with even-density→0 |
| 2 | top-digit equidistribution: top `Θ(log N)` digits of `c_n` equidistribute; foothold reach `k(N)/log₂N ≈ 0.85` (CF-governed by `log₂3`) | `[PROVEN]` | reaches depth `Θ(log N)`; parity bit is the diagonal at depth `Θ(n)` |
| 3 | `3/2` non-Pisot ⟹ `ν_{2/3}` is **Rajchman** (`ν̂_{2/3}(ξ)→0`); effective decay `≥ logarithmic` and sharp | `[PROVEN-in-lit]` (Erdős–Salem; **Varjú–Yu** arXiv:2004.09358; Kershner) | qualitative/log; power rate is itself Mahler; annealed not quenched |
| 4 | `dim ν_{2/3} = 1` (Hausdorff = entropy dimension), unconditional | `[PROVEN-in-lit]` (**Hochman 2014**; rational `λ` ⟹ no exact overlaps) | annealed property of the measure; one orbit point has dimension 0; ℝ-place not the 2-adic ENT |
| 5 | subword-complexity floor `p(ℓ) ≥ 1.71ℓ` (slope `log₂/log(3/2)`); coding bijection `p(ℓ)=#{c_n mod 2^ℓ}`, full `=2^ℓ` to `ℓ=14` | `[PROVEN]` (Dubickas 2009 slope) | linear lower bound; consistent with both `h_top=0` and `=log2`; topological not frequency |
| 6 | Salem–Zygmund `|Σ_{n<N}e(ξ(3/2)^n)|=O(√(N log log N))`; transfer-operator quenched CLT for a.e. sequence | `[PROVEN-in-lit]` | a.e.-`ξ` / a.e.-sequence, not specializable to the one orbit |
| 7 | Vaaler L¹ minorant: `(K)` needs only `J=5` circle frequencies; per-frequency demand still `≥96%` single-orbit cancellation | `[PROVEN]` | reduces frequency count to finite; per-frequency `√N→o(N)` is still `(K)` |
| 8 | FLP spread `Ω(3/2) ≥ 1/3`; Zudilin `‖(3/2)^n‖ > 0.5803^n` (`n≥K`) | `[PROVEN-in-lit]` (FLP Acta Arith. 70 (1995); Zudilin 2007) | **support/spread or pointwise, never frequency** — numerically `1/3` coincides with ours but on an orthogonal axis (no bridge) |
| 9 | induced map exact Bernoulli (`D_j` i.i.d. geom, mean 2); valuation budget `Σv_2(3c_i−1)=n+v_2(c_n)−v_2(c_0)` | `[PROVEN]` | a.e.-Haar / first-moment |

**The ladder of strictly intermediate targets `[PROVEN structural]`:**
> `{orbit avoids periodic}` `[PROVEN]` `⊊` `{μ non-atomic}` `[OPEN]` `⊊` `{ENT: h_μ(M_2)>0}` `[OPEN, (K)-hard]`
> `⊊` `{(K): μ=Haar}` `[OPEN]`.
The first inclusion is proven strict and the gaps named: non-atomicity `⟺ sup_a μ_2(a+2^kℤ₂)→0` (vanishing max
cylinder occupancy; weaker than equidistribution's per-cell value), but the proven facts give only *per-visit
escape* (growth, non-periodicity, dual-repulsion countdown), not *zero return-density*; an atom needs only
positive-density re-entry `=` the refill-law tail `= (K)`-character. The proven budgets (`max run ≤ 0.585N`, mean
depth `≤1.585`) permit a single run of length `≈0.585N`, hence cannot exclude an atom.

**First-vs-second-moment characterization `[PROVEN]`.** A degree-1 depth potential telescopes its refill term to
a **count `≤N`** (free: the first-moment valuation budget, mean gap `≈2`). A degree-`≥2` potential telescopes to
a **tautology**: `Σ_n d_n = ½(ΣK_i² + ΣK_i)` and the quadratic telescope `ΣK_i² = 2Σ_n d_n − #{d≥1} + O(log²N)`
together reduce to the first-moment identity, so they carry **no** independent second-moment bound. The first
moment is a *count* (free); the second moment is an *energy* with no a-priori `O(N)` cap (one `K≈0.585N` run
breaks it), and capping it is exactly `E[K²]<∞ = μ({1})=0`-grade tail control `= (K)`-adjacent. This is the
concrete arithmetic face of the dichotomy's "1st moment free, 2nd moment hard."

---

## 7. The expert question (≈1 page)

**To: the AEV authors (Andrieu–Eliahou–Vivion) and the Einsiedler–Lindenstrauss–Host measure-rigidity circle.**

**Lead with the proven structure.** Antihydra non-halting reduces, by an unbroken chain of machine-verified
`[PROVEN]` equivalences (§2), to single-orbit equidistribution of the `×(3/2)`-orbit of `8` — the one-sided,
level-2, single-orbit floor-mirror fragment `(K)` of AEV Conjecture 1.6, which implies Mahler's 3/2 problem. We
have **proven** (§3) that this residual is *structural*: no bounded-residue (coboundary), all-orbits
(specification), or measure-level (annealed/ergodic) certificate can decide it, because each assigns the seed the
same verdict as the genuinely halting fixed point `o=1` (an ergodic-optimization maximizer, `β=+½`). We are not
asking you to solve Mahler 3/2; we are asking you to assess the **two precise inputs** to which the kernel
reduces, given that both feed a **proven** theorem.

**The object.** On the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, `A=×(3/2)=M_3 M_2^{-1}` is the rank-1 line `ℤ·(−1,1)`
inside the rank-2 host `⟨×2,×3⟩`. Let `μ` be any weak-* limit of the seed-8 `A`-orbit empiricals
(`A`-invariant, `[PROVEN]`). Then `(K) ⟺ μ=Haar`, and by the **proven** Rudolph–Johnson (solenoid form,
arXiv:2101.11120) this follows from:

> **(AIU)** `μ` is invariant under the full host `⟨×2,×3⟩`, not merely under `A`. Equivalently (leafwise) the
> `A`-stable `ℚ₃`-conditionals `μ_x^3` are `ℤ₃^*`-rotation-invariant (spherically Haar); equivalently (seed-shift)
> `μ_8=μ_16`. The surplus invariance lives on the `ℚ₃` place where `×2` is an **isometry** (`|2|_3=1`, **zero
> Lyapunov exponent**) — a *neutral / central* direction.
>
> **(ENT)** `h_μ(M_2) > 0` (positive 2-adic measure entropy). By Ledrappier–Young this is one conditional
> dimension `γ_∞^{(2)}>0`; it is a *necessary consequence of `(K)`* (zero entropy would refute `(K)`), hence not
> strictly easier, but strictly weaker as a proposition.

We have **proven** AIU and ENT are **logically independent**, and that with both, the proven Rudolph–Johnson
finishes (`h_μ(M_2)>0 ⟹ μ` non-atomic, so the live branch needs only AIU + ENT; the alternative needs the open
Furstenberg conjecture).

**Where the standard methods break (precise).**
- **Rigidity engines** (Furstenberg / Rudolph–Johnson / EKL high-entropy / BFLM / effective Ratner) need rank ≥ 2
  *or* a non-abelian acting semigroup with a spectral gap *or* unipotent divergence. We iterate a **rank-1,
  abelian, amenable, hyperbolic** map; rank-1 diagonal actions carry an uncountable simplex of invariant measures
  (Einsiedler–Lindenstrauss JMD 2008), so there is no rigidity of `⟨3/2⟩` to invoke. The host *is* rank-2, but
  our orbit is its rank-1 sub-orbit — hence the **AIU bridge** is exactly the missing piece.
- **The high-entropy method cannot supply AIU**: it propagates invariance only along entropy-carrying
  (expanding/contracting) coarse-Lyapunov directions, and the AIU direction is **neutral** (`×2` on `ℚ₃`). Host
  (1995) needs a second multiplicatively-independent *expanding* ergodic map (we have only `A`), outputs
  a.e.-normality not measure-invariance, and is a.e.-not-specified. The proven adelic coupling
  `v_3(o_{j+1})=D_j−1` makes the `ℚ₂`,`ℚ₃` disintegrations **deterministically dependent** — the wrong side for
  joinings/disjointness.
- **For ENT**: pressure gives only the vacuous upper bound `h_μ≤h_top=log2`; large-deviation and the proven
  Gibbs–Markov renewal give positivity only for Haar/SRB-typical points, never the named Haar-null seed. No
  proven structure lower-bounds the conditional dimension `γ`.
- **Self-similar-measure / fractal normality** (Algom–Baker–Shmerkin: Rajchman ⟹ a.e.-in-support normal;
  Hochman–Shmerkin) stops at the **a.e.-in-support** quantifier — the one we cannot use for a single specified
  algebraic orbit.

**Precise questions.**
- **Q-A (AIU).** For the `A=×(3/2)`-orbit of the specified point `8` on the `(2,3)`-solenoid, is the
  host-invariance upgrade — *the asymptotic invariance group of the single rank-1 orbit's limit measure exceeds
  its pointwise symmetry group by exactly `×2` (a neutral, zero-Lyapunov `ℚ₃`-rotation)* — tractable, or is the
  neutral-direction obstruction (no entropy to spend) genuinely fatal to every known invariance-upgrade
  mechanism?
- **Q-B (ENT).** Is positive 2-adic entropy `h_μ(M_2)>0` (equivalently a positive lower bound on the
  Ledrappier–Young conditional dimension `γ_∞^{(2)}`) reachable for this **explicit non-Pisot,
  transducer-generated** measure by any quenched method, given that every proven structure controls only
  unweighted/support/annealed quantities?
- **Q-C (framing).** Given that **both AIU and ENT feed the proven Rudolph–Johnson**, is "single rank-1 sub-orbit
  ⟹ rank-2 host invariance + positive entropy" a named/studied object, a known obstruction we have overlooked, or
  a genuinely empty spot between the rigidity and the Weyl toolboxes (amenable ∩ hyperbolic ∩ rank-1 ∩
  specified-point)? A sharp "no, here is why" is as useful as a "yes, see X"; if the reduction is malformed, the
  most valuable reply is how you would reformulate it.

> **One sentence.** For the `A=×(3/2)`-orbit of `8` on the `(2,3)`-solenoid, is either the host-invariance upgrade
> (AIU — a neutral, zero-Lyapunov direction) or positive 2-adic measure entropy (ENT) tractable for this explicit
> non-Pisot transducer-generated measure, given that both feed the *proven* Rudolph–Johnson theorem?

---

## 8. Citations

*Corrected attributions are flagged. Pins from `CITATIONS.md`; `[PROVEN-in-lit]` unless noted.*

**The kernel's literature home.**
- M. Andrieu, S. Eliahou, L. Vivion, *A Normality Conjecture on Rational Base Number Systems*,
  **arXiv:2510.11723** (2025). Conj. 1.2 (normality), Conj. 1.6 (equidistribution mod `q^k` for the ceiling map
  `T_{p/q}(x)=⌈px/q⌉`), Conj. 1.4 (generalized Mahler / Z_{p/q}-numbers); Thm 1.5 (Conj 1.2 ⟹ 1.4, for `p<q²` —
  holds at `3/2`), Thm 1.7 (Conj 1.2 ⟺ 1.6). `(K)` is the one-sided, level-2, single-orbit *floor-mirror* of the
  `p/q=3/2` instance. **`[OPEN]`** *(attribution = Andrieu–Eliahou–Vivion, confirmed.)*
- K. Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. **8** (1968) 313–321. **`[OPEN]`**
- S. Eliahou, J.-L. Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*,
  **arXiv:2504.13716** (2025; to appear C. R. Math.) — base-3/2 ↔ Collatz dictionary (structural, no density).
- A. Algom, *Recent progress on pointwise normality of self-similar measures*, **arXiv:2504.18192** (2025) —
  **exposition, Algom solo.** **Correction:** the underlying theorem (*Rajchman ⟹ μ-a.e. point normal to all
  bases*) is **Algom–Baker–Shmerkin**, *On normal numbers and self-similar measures*, Adv. Math. (2022),
  arXiv:2107.02699. The exposition lists *effective equidistribution* and *non-integer bases* as open — exactly
  our two axes; the result is **a.e.-in-support** (the quantifier we cannot use).
- A. Dubickas, *On integer sequences generated by linear maps*, Glasgow Math. J. **51** (2009) 243–252 (Thm 3:
  subword-complexity slope `log q/log(p/q)`); A. Dubickas, M. J. Mossinghoff, *Lower bounds for Z-numbers*,
  Math. Comp. **78** (2009) 1837–1851 (the "4/3 problem"); S. Akiyama, Ch. Frougny, J. Sakarovitch, *Powers of
  rationals modulo 1 and rational base number systems*, Israel J. Math. **168** (2008) 53–91.
- L. Flatto, J. C. Lagarias, A. D. Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. **70**
  (1995) 125–147 (spread `≥1/3` — **support axis, no bridge to density**).

**Measure rigidity / homogeneous dynamics (the placement).**
- D. Rudolph, *×2 ×3 invariant measures and entropy*, ETDS **10** (1990); A. Johnson, Israel J. Math. **77**
  (1992) — positive-entropy `⟨×2,×3⟩`-invariant ⟹ Haar. *(The theorem AIU+ENT feed.)*
- M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  **arXiv:2101.11120** — solenoid form of Rudolph–Johnson + leafwise measures.
- D. Berend, *Multi-invariant sets on tori / on compact homogeneous spaces* — topological set-rigidity
  (gives full support, **not** Haar).
- H. Furstenberg, *Disjointness in ergodic theory…* (1967) — the ×2,×3 measure conjecture. **`[OPEN]`**
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case*,
  JMD (2008) — rank-1 non-rigidity (uncountable invariant simplex, incl. positive entropy).
- B. Host, *Nombres normaux, entropie, translations*, Israel J. Math. **91** (1995) 419–428.
- F. Ledrappier, L.-S. Young, *The metric entropy of diffeomorphisms* I/II, Ann. Math. **122** (1985);
  Lind–Schmidt–Ward / Yuzvinskii, solenoid entropy `h(×u)=Σ_v log⁺|u|_v`.
- J. Bourgain, A. Furman, E. Lindenstrauss, S. Mozes, JAMS **24** (2011) 231–280 — non-abelian individual-orbit
  equidistribution (hypothesis fails: ours is abelian).
- M. Hochman, *On self-similar sets with overlaps and inverse theorems for entropy*, Ann. Math. (2014) —
  `dim ν_{2/3}=1`; M. Hochman, P. Shmerkin, Ann. Math. **175** (2012).
- T. Varjú, H. Yu, *Fourier decay of self-similar measures…*, arXiv:2004.09358; Kershner (1936) — effective
  (logarithmic) decay for rational `λ`.

**Reduction-chain / ergodic-optimization machinery.**
- J. C. Lagarias, Amer. Math. Monthly **92** (1985) 3–23; D. J. Bernstein, J. C. Lagarias, Canad. J. Math. **48**
  (1996) 1154–1169; K. R. Matthews, A. M. Watts, Acta Arith. **43** (1984) 167–175 — 2-adic Collatz conjugacy /
  Bernoulli.
- R. Mañé, Nonlinearity **9** (1996) 273–310; T. Bousch, Ann. IHP PS **36** (2000) 489–508 and Ann. Sci. ÉNS (4)
  **34** (2001) 287–311; O. Jenkinson, DCDS **15** (2006) 197–224, ETDS **39** (2019) 2593–2618;
  Conze–Guivarc'h (unpublished, c.1993, unpinnable) — ergodic optimization / sub-action theory.
- L. Barreira, J. Schmeling (2000) — full Hausdorff dimension of non-generic (irregular) sets.
- *Convention:* repo facts are machine-checked in exact integer / 2-adic arithmetic per the program's soundness
  policy. No proofs are claimed beyond the `[PROVEN]` labels above; `(K)` remains `[OPEN]`.

---

**No machine decided. No label upgraded.**
