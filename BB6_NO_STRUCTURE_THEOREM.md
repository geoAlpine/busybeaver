# The No-Structure-Only-Selection Theorem — formal core of the framework (2026-06-30)

*Formal write-up of the HARD direction of the obstruction dichotomy (`BB6_OBSTRUCTION_DICHOTOMY.md`): a precise theorem that
no certificate drawn from the structural (residue / all-orbits / measure-level) registers can prove the Antihydra
non-halting criterion, with the gap localized to a single named arithmetic statement. Assembled from two already-proven,
already-audited ingredients: the coboundary-LP infeasibility (`MINPROP_COBOUNDARY_LP.md`) and the specification
non-universality (`MINPROP_COUPLING.md`). SOUNDNESS: every step labelled; the theorem is [PROVEN]; its scope is delimited
honestly (it does NOT prove (K) undecidable, and does NOT preclude an orbit-arithmetic proof). NOT committed by default.*

---

## 1. Setup

Antihydra reduces (machine-verified chain, `COMPLETE_PROOF_CAPSTONE.md`) to the **induced odd map** on `ℤ₂^*`:
`T(o) = 3^{D−1}(3o−1)/2^D`, `D = D(o) := v₂(3o−1) ≥ 1`, seed `o₀ = 27`. `T` is [PROVEN] Haar-preserving, exact, and
Bernoulli, with `(D_j)` i.i.d. geometric `P(D=d)=2^{−d}` under Haar (`INDUCED_RESIDUE_STRUCTURE.md`). Define the
**violation observable**
> `ψ(o) := ½ − 1{D≥2} − 1{D≥3}`  (a function of `o mod 8`: `ψ=+½` if `D=1`, `−½` if `D=2`, `−3/2` if `D≥3`).

[PROVEN] `(1/N)Σ_{j<N} ψ(o_j) = ½ − (1/N)Σ_{j<N}[1{D_j≥2}+1{D_j≥3}]`, so
> **the criterion (K):** `limsup_N (1/N)Σ_{j<N} ψ(o_j) ≤ 0`  ⟺  `liminf mean D ≥ 3/2`  ⟺  even-density `≥ 1/3`  ⟺
> **Antihydra never halts**.

`(K)` is the assertion that the orbit of `o₀=27` has time-average `ψ`-value `≤ 0`. The Haar mean is `∫ψ\,dHaar = −1/4`
(a 1/4 margin) — so `(K)` holds *on average / a.e.*; the question is the single specified orbit.

---

## 2. The three structural certificate classes

A "structure-only certificate" is any of the three registers that the dichotomy's FREE side comprises:

- **(C1) Bounded residue sub-action (coboundary) certificate:** a bounded `g:(ℤ/2^kℤ)^* → ℝ` (any `k`) with
  `ψ(o) ≤ g(T(o) mod 2^k) − g(o mod 2^k)` for **all** odd `o`. (If it existed, telescoping gives `Σψ ≤ 2‖g‖_∞` for
  *every* orbit ⟹ unconditional `(K)`.)
- **(C2) Universal / all-orbits certificate:** any argument proving `limsup (1/N)Σψ ≤ 0` for **every** orbit of `T` (or
  every orbit in a structurally-defined class containing `o₀`) — i.e. a bound that does not use data singling out `o₀`.
- **(C3) Measure-level / annealed certificate:** any argument that concludes from the invariant measure (Haar/Bernoulli
  ergodic theorem, decay of correlations, CLT) — yielding the conclusion for **μ-a.e.** orbit.

These exhaust the FREE-side machinery (R1 measure-constant/first-moment/annealed; R2 all-orbits/topological); HARD-side data
(the orbit's specific magnitude/arithmetic) is by definition outside them.

---

## 3. The theorem

> **Theorem (No structure-only selection of `o₀`).** No certificate in classes (C1), (C2), (C3) proves `(K)`. Concretely:
> 1. **(C1) is infeasible** — there is **no** bounded `g` on any `(ℤ/2^kℤ)^*` with `ψ ≤ g∘T − g` pointwise. `[PROVEN]`
> 2. **(C2) is impossible** — `(K)` is **non-universal**: a full-Hausdorff-dimension set of `T`-orbits violates it
>    (`liminf mean D < 3/2`), including the genuine fixed point `o=1`. `[PROVEN]`
> 3. **(C3) is insufficient** — the Haar/Bernoulli structure gives `(K)` only for **μ-a.e.** orbit, and `{o₀}` is
>    `μ`-null (a countable set), lying in the full-dimension non-generic set. `[PROVEN]`
>
> Hence any proof of `(K)` must use information distinguishing the orbit of `o₀=27` from the violating orbits — i.e. the
> orbit's specific magnitude / reachability / arithmetic. That residual is exactly single-orbit equidistribution of
> `c_n mod 2^k` = Mahler 3/2 / AEV Conj 1.6 = `(K)` itself.

**Proof.**

*(1).* The constraints `ψ(o) ≤ g(b)−g(a)` (`a=o mod 2^k, b=T(o) mod 2^k`) are difference constraints; by LP duality
(max-mean-cycle / Bellman–Ford), a bounded `g` exists **iff** the residue constraint digraph has no positive-mean cycle,
**iff** `sup_ν ∫ψ\,dν ≤ 0` over `T`-invariant measures `ν`. The fixed point `o=1` (`T(1)=1`, `D=1`, `ψ(1)=+½`) is an
atomic invariant measure `δ₁` with `∫ψ\,dδ₁ = +½ > 0`, realized as a **weight-`+½` self-loop at residue `1` for every
`k≥3`**. So `sup_ν ∫ψ ≥ +½ > 0` and the LP is infeasible at every level. This was solved **exactly** (`Fraction`
arithmetic) at `k=3..12` with the conservative full-branch tail treatment (the undetermined residue set is `2^{−(K−k)}` of
all residues and consists entirely of `ψ=−3/2` edges, so the infeasibility is tail-independent), and the driving
self-loop is level-independent. Moreover deleting node `1` leaves further positive-mean cycles, all **reachable in residues
from `27 mod 2^k`** (the reachable component is the whole graph), so no residue-domain restriction evades it.
(`MINPROP_COBOUNDARY_LP.md` §2–4.) ∎(1)

*(2).* `T` is a full-branch map: each cylinder `A_d` (`Haar 2^{−d}`) maps **onto** all of `ℤ₂^*`
(`INDUCED_RESIDUE_STRUCTURE.md`), so the system has the **specification property**. By multifractal analysis
(Takens–Verbitskiy; Sigmund), for the continuous observable `φ=1{D≥2}` the set of realized Birkhoff averages is the full
interval `[min_ν ∫φ, max_ν ∫φ]`, and **every interior value is attained on a full-Hausdorff-dimension set of orbits**. The
extrema are `0` (at `δ₁`: `D=1` forever) and `1` (at the `ℤ₂`-fixed point `o=3/5`: `D=2` forever), both [PROVEN]. Hence
`max_ν ∫(½−φ)\,dν = +½ > 0`, so a full-dimension set of orbits has `liminf freq(D≥2) < ½`, i.e. violates `(K)`. The bound
is non-universal. (`MINPROP_COUPLING.md` §2.) ∎(2)

*(3).* Exact + Bernoulli ⟹ for `μ=`Haar-a.e. start, `freq(D≥k)→2^{1−k}`, hence `(K)` holds a.e. But the orbit `{T^j o₀}`
is countable, hence `μ`-null; and the non-generic set has full entropy and full Hausdorff dimension (Barreira–Schmeling
2000, `WALLB_INVARIANT_MEASURES.md`). So the a.e. statement says nothing about the specified `o₀`. ∎(3)

*Conclusion.* (C1)–(C3) all assign `o₀` the same verdict they assign to the violating orbits (`δ₁` and the full-dimension
family), because none of them reads data separating `o₀` from those orbits. Since `(K)` is FALSE on those orbits, no such
certificate can prove `(K)` for `o₀`. The separating data is the orbit's magnitude/reachability — that `o₀`'s orbit grows
unboundedly and avoids the basins of the low cycles — which is the content of single-orbit equidistribution = `(K)`. ∎

---

## 4. What the theorem does and does not establish [honest scope]

**Does:**
- Rules out, unconditionally and at the theorem level, the entire FREE-side machinery (bounded residue sub-actions; universal/all-orbits bounds; measure-level/annealed arguments) as a route to `(K)`.
- Localizes the irreducible content to one named arithmetic statement (single-orbit equidistribution = Mahler 3/2 / AEV).
- Explains *why* ~20 independent attack routes stop at the same place (each is, by `BB6_OBSTRUCTION_DICHOTOMY.md`, an instance of one of (C1)–(C3) or the topological register).

**Does NOT:**
- Prove `(K)` is undecidable, independent, or false — only that it is not reachable from structural data.
- Preclude a proof that *does* use orbit-specific arithmetic (solving Mahler 3/2 at `α`-data, or a new tool acting on the orbit). The theorem delimits the *failed* registers, not the problem.
- The one variant the LP does **not** kill is a **magnitude-aware, unbounded** Lyapunov `g(o)=α log o + h(o mod 2^k)` (`α<0` couples to the size drift `D log(3/2)`); but it cannot see `δ₁` (where `log` is constant) as a global obstruction, so it works only as a **conditional** certificate above a threshold, reintroducing the avoidance/genericity content = `(K)`. `[OPEN]` — the honest sole surviving structural variant, still tied to `(K)`.

**Rests on [PROVEN] inputs:** the exact LP infeasibility (`MINPROP_COBOUNDARY_LP.md`, exact `Fraction`, `k=3..12`,
level-independent, tail-audited); the full-branch/specification + multifractal non-universality (`MINPROP_COUPLING.md`); the
induced-map exactness (`INDUCED_RESIDUE_STRUCTURE.md`); Barreira–Schmeling full-dimension of non-generic points
[PROVEN-in-lit].

---

## 5. Statement for an external reader (framework-paper abstract form)

> *For the Antihydra induced map `T(o)=3^{D−1}(3o−1)/2^D` on `ℤ₂^*`, the non-halting criterion `liminf mean D ≥ 3/2` is
> (i) **infeasible for every bounded residue sub-action** (the fixed point `o=1` is a positive-mean obstruction, exact LP,
> all levels), (ii) **non-universal** (violated on a full-Hausdorff-dimension set of orbits, by specification), and
> (iii) **a.e.-true but `o₀`-null** (Bernoulli ergodicity, `o₀` non-generic). Therefore the criterion for the specific seed
> is independent of all residue-finite, all-orbit, and measure-theoretic data, and is equivalent to single-orbit
> equidistribution of `(3/2)^n`-type — Mahler's 3/2 problem / the Andrieu–Eliahou–Vivion normality conjecture at the
> rational base 3/2. The obstruction is proven structural, not a gap in technique.*

**No machine decided. No label upgraded.** `(K)` remains [OPEN] = Mahler 3/2 / AEV.
