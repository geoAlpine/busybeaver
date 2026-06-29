# The Missing Tool, Defined by its Negative Space — sharpened new-math spec (2026-06-30)

*Mines ALL the proven/observed no-gos in the BB(6)/Antihydra program to extract the PRECISE CONSTRAINTS the
missing tool must satisfy. The method is definition-by-negation: each closed route forbids a class of tools, and
the intersection of those prohibitions is the tightest available specification of what the tool must be. This is a
legitimate research-program spec, **not a proof claim**: nothing here decides (K); the no-gos cited are about
which methods provably cannot reach (K), not about (K)'s truth value. Every constraint is labelled by the source
no-go and its status `[PROVEN no-go]` / `[OBSERVED]`. NOT committed by default.*

---

## 0. The object and the target, fixed once

- **Induced odd map** `T(o) = 3^{D−1}(3o−1)/2^D`, `D = D(o) = v₂(3o−1) ≥ 1`, on `ℤ₂^*`, seed `o₀ = 27`
  (equivalently `c_{n+1}=⌊3c_n/2⌋`, `c₀=8`). `T` is Haar-preserving, exact, Bernoulli; `(D_j)` i.i.d. geometric
  `P(D=d)=2^{−d}` under Haar. `[PROVEN, INDUCED_RESIDUE_STRUCTURE / COMPLETE_PROOF_CAPSTONE]`
- **The kernel (K)** ⟺ `liminf mean D ≥ 3/2` ⟺ even-density `≥ 1/3` ⟺ single-orbit equidistribution of
  `c_n mod 2^k` for all `k` ⟺ Mahler 3/2 / AEV Conj 1.6 at α=8 ⟺ Antihydra never halts. All [PROVEN]-equivalent.
- **The Haar mean is favourable** (`∫ψ dHaar = −1/4`, margin 1/4): (K) holds a.e.; the entire difficulty is the
  *single specified orbit* `o₀`.

The seven no-gos below each carve away a class of candidate tools. The tool that survives all seven is specified
in §8.

---

## 1. NOT spectral / NOT a contraction — must control the ODD block non-spectrally

**No-go (source: `ENDOGENOUS_UE_BUILD.md` §2.2, §5).** `[PROVEN no-go]`
The annealed transfer operator `L_ann` (one fresh bit i.i.d. Bernoulli(½)) **exactly annihilates every odd
additive character**: `L_ann χ_a ≡ 0` for all odd `a` (machine-verified ≤1e-13). Its spectral gap `1−λ₂(k)>0`
acts only on `V_even`; the conclusion (K) is *exactly* the vanishing of the odd-character empirical averages
`π_N(χ_a)`, `a` odd. The gap and the conclusion live on **complementary, non-interacting** subspaces. No bound
`Inj(k) ≤ F(λ₂, automaton γ)` can exist — an adversary with the *same* automaton and *same* gap realises feedback
`≈1` (constructive, C5).

> **Constraint 1.** The tool must control the **odd-character subspace `V_odd`** by a mechanism that is **NOT a
> spectral gap / not a contraction of `L_ann`** (or of any operator that anneals the fresh bit), because every
> such operator is provably blind to `V_odd`. It must use a property *specific to the endogenous input*
> `β_n = bit_k(c_n)` — the self-reference — not `(L_ann, gap, γ)` alone.

---

## 2. NOT structure-only / measure-constant — must SELECT Haar within M_feas

**No-go (source: `BB6_NO_STRUCTURE_THEOREM.md` §3, Thm; `MINPROP_ERGODIC_OPT.md`).** `[PROVEN no-go]`
No certificate in classes (C1) bounded residue sub-action, (C2) universal/all-orbits, (C3) measure-level/annealed
proves (K). Reasons, all [PROVEN]: (C1) the fixed point `o=1` is a positive-mean (`∫ψ dδ₁=+½>0`) obstruction at
every level (exact LP, `k=3..12`, level-independent, tail-audited); (C2) (K) is violated on a full-Hausdorff-
dimension set of orbits (specification + multifractal); (C3) a.e.-true but `o₀` is `μ`-null and non-generic
(full-dimension non-generic set, Barreira–Schmeling). The ergodic-optimization value is `β(ψ)=+½` and the
maximiser is the fixed point — so every closure/first-moment/annealed certificate is **constant on the feasible
measure set `M_feas`** and assigns `o₀` the same verdict as the violating orbits.

> **Constraint 2.** The tool's certificate must be **non-constant on `M_feas`** — it must **SELECT Haar** (or the
> sub-family satisfying (K)) from within `M_feas`, using **orbit-specific arithmetic** (the magnitude/reachability
> of `o₀`'s itinerary, not residue-finite / all-orbit / invariant-measure data). A tool that reads only the
> invariant measure cannot separate `o₀` from `δ₁` and the full-dimension violating family.

---

## 3. NOT a sub-action / coboundary of any of these forms — bounded, unbounded, or adelic

**No-go (sources: `MINPROP_COBOUNDARY_LP.md`; `MAGNITUDE_LYAPUNOV.md`; `ADELIC_SUBACTION.md`).** `[PROVEN no-go]`
- **Bounded residue coboundary** `g:(ℤ/2^kℤ)^*→ℝ`, `ψ ≤ g∘T − g`: infeasible at every `k` (the `δ₁` self-loop,
  `∫ψ dδ₁=+½>0`).
- **Unbounded magnitude-aware** `g = α log₂o + h(o mod 2^k)`: **sign tension** `[PROVEN]`. Useful telescoping needs
  `α<0` (to convert `log₂o_N→∞` into `Σψ→−∞`), but `α<0` is infeasible — high-`D` measures give `∫ψ̃=ψ(d)+|α|c·d→+∞`,
  and even *conditionally* on `o>M₀` the per-step constraint fails because `D=v₂(3o−1)` is unbounded at arbitrarily
  large `o`. The feasible sign `α≥0.855` makes the bound vacuous (`Σψ ≤ α log₂o_N→+∞`).
- **Adelic 3-place** `α_∞ log|o|_∞ + α_2,α_3` potentials: closed by the **product formula**. The `D=1` drift is
  exactly `(log(3/2), log2, −log3)`, saturating `Σ_v Δlog|o−1|_v = 0`. Feasibility forces `α_3≥0` (high-`e`) and
  `α_∞ log(3/2) ≥ α_3 log3` (high-`D`) ⟹ `α_∞≥0`, antipodal to the useful `α_∞<0`. The 3-adic place is the
  invertible time-shift `e=D_prev−1` of the 2-adic depth (T2), not an independent direction — it *reinforces* the
  tension.

> **Constraint 3.** The tool is **NOT a Lyapunov sub-action / telescoping coboundary** of the residue, magnitude-
> aware, or adelic forms. Any potential built from `(log|o|_v, residues)` is product-formula-locked: the only
> place with unbounded useful telescoping is `∞`, and the boundedness constraint forces its sign to be exactly the
> useless one. A useful certificate would need an **independent third drift the (2,3)-solenoid does not provide.**

---

## 4. NOT per-step — must act at the EXCURSION / return-time / multi-scale level

**No-go (sources: `CORE_CARRY_LEVER.md`; `ENDOGENOUS_UE_BUILD.md` §5; `EXCURSION_SYNTHESIS.md`).** `[PROVEN/OBSERVED]`
On the odd channel `V_odd` where (K) lives, the self-referential feedback `β_n=bit_k(c_n)` is **white**: autocorr
≤0.006 all lags, `I(β;state)≈3·10⁻⁵` bits. A tempting per-step block mean-reversion signal (−0.14) was killed by a
shuffle control (−0.06±0.12, <1σ) — artifact. So no per-step drift exists.

> **Constraint 4.** The tool's relevant functional must act at the **excursion / return-time / multi-scale**
> level, NOT per-step. The decrease (if any) must live in the **conditional return-time law** of the countdown
> excursions, because the per-step feedback is provably white (no per-step supermartingale, no conserved quantity;
> the depth random-walk has partial sums ~√N).

---

## 5. NOT a depth-function potential — must read refill MAGNITUDES (~K²), not depth alone

**No-go (sources: `EK2_SECOND_BUDGET.md`; `EK2_PARTIAL_MOMENTS.md`; `NONATOMIC_FIXEDPOINT.md`).** `[PROVEN no-go]`
Every potential that is a function of the current depth `d_n` telescopes into (countdown decrements) + (refill
injections `Σ K_i^p`), and the two sides are the *same* `p`-th moment — the telescope **closes on itself**. For
`p=1` the refill sum is a **count** `#{d≥1}≤N` (free: `Σ K_i ≤ N`, mean gap ≈2, a tautology). For `p=2` the
identity `ΣK² = 2Σ_n d_n − #{d≥1} + bdry` equates `ΣK²` to `Σ_n d_n` = the second moment **itself** — no a-priori
`O(N)` cap (one `K≈0.585n` run gives `ΣK²/N→∞`, atom `μ({1})≥0.585`, consistent with every proven identity). The
degree-2 potential `Q=d²` telescopes to the `0=0` tautology. Bounded 2-adic potentials (`2^{−d}`) under-weight
exactly the heavy tail.

> **Constraint 5.** The tool's functional must **NOT be a function of the depth `d_n` alone** (all such self-close
> at the first moment). It must read the **refill MAGNITUDES** — the entry-depths `K_i = v₂(3c'−1)`, the hidden
> lower 2-adic digits / moving-middle (Mahler) bit injected at each refill — and produce control of the **second
> moment `E[K²]` / `Σ_n v₂(c_n−1) = O(N)`** (≡ `μ({1})=0`), which the first-moment / count register cannot reach.

---

## 6. MUST AVOID the circularity — produce an A-PRIORI estimate not assuming the D-law

**No-go (sources: `EXCURSION_SYNTHESIS.md` §1; `CORE_ORBIT_ARITHMETIC.md` §5; `ENDOGENOUS_UE_BUILD.md` §5).**
`[PROVEN no-go]`
The conditional return-time law of `V=v₂(c−1)` **IS** the D-statistics, which **IS** (K). Concretely: the occupancy
`f_K = freq{o≡1 mod 2^K}`, the second moment `E[K²]`, the return-time energy — each is a restatement of (K). A
**heavy-tailed adversary** (`E[K²]=∞`, white, first-moment-matched) satisfies *every* proven identity, count,
support bound, adelic budget, and excursion drift, yet halts — it is drift-indistinguishable from the real orbit
for every candidate potential. Every "natural escape" is circular: "assume `β_n` balanced/independent" = assume a
slice of (K); "bootstrap scale `k→k+1`" regresses infinitely (the gap never reaches the fresh end). The second
moment is the **conclusion, never a usable input**.

> **Constraint 6.** The tool must produce an **A-PRIORI estimate of the conditional return-time law / `E[K²]` /
> occupancy `f_K` WITHOUT assuming the D-law** — i.e. it must derive a return-time decrease from `o₀`'s **specific
> 2-adic arithmetic** in a way that **excludes the heavy-tailed first-moment-matched adversary**. Any argument
> whose only inputs are the proven unconditional facts is circular (those facts are consistent with both (K) and
> its negation). The tool must read something the adversary does not share: the actual arithmetic of the orbit.

---

## 7. NOT high-entropy rigidity — must use a CENTRAL/neutral-direction mechanism

**No-go (sources: `AIU_JOININGS.md`; `AIU_SKEW_ROTATION.md`).** `[PROVEN no-go]`
On the (2,3)-solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, `A=×(3/2)` hyperbolic, the host-invariance upgrade AIU (=`(×2)_*μ=μ`)
is invariance of the `A`-stable `ℚ₃`-leaf conditionals under the rotation `×2`, and `×2` on `ℚ₃` is **neutral**
(`|2|_3=1`, dilation 1, **zero Lyapunov exponent, zero entropy**). Two independent obstructions, both [PROVEN]:
- **EKL high-entropy / leafwise method is blind to neutral directions** — it manufactures invariance only along
  coarse-Lyapunov directions that *carry* entropy. Entropy (the (K)-bit) lives on the `∞/2` axis; the missing
  invariance lives on the orthogonal neutral `ℚ₃`-rotation axis. ENT ⇏ AIU; ENT and AIU are *logically
  independent* (rank-1 non-rigidity gives positive-entropy non-Φ-invariant measures).
- **Skew-product / unique-ergodicity is inert** — `A` is the skew product `A(v,u)=(v+1, R_2^{−1}u)` over the
  *contracting (dissipative) radial base* `v=v₃`; `R_2:u↦2u` is uniquely ergodic, but `A` iterates it **zero
  times per sphere** (no finite invariant base measure), so the isometric-extension theorem has no purchase. The
  only recurrence is the renewal cocycle, whose rotation-time is exactly `D` = the (K) data. Host (1995) needs a
  *second multiplicatively-independent expanding ergodic map* (we have only `A`; `×2` is isometric) and yields
  a.e.-normality, not measure-invariance of `μ`, and not the seed.

> **Constraint 7.** The host-invariance upgrade the tool must supply lives on a **neutral / central direction**
> (zero entropy, zero Lyapunov exponent). The tool must use a **central-direction mechanism** — NOT a high-entropy
> / high-rank rigidity engine (EKL, positive-entropy joinings), which is structurally blind there; NOT a unique-
> ergodicity / isometric-extension argument (the base is dissipative, the fiber rotation is iterated zero times);
> and NOT a Host-type joining (the adelic coupling `v₃=D−1` makes the place-disintegrations deterministically
> DEPENDENT, the wrong side for disjointness). It must convert *non-atomicity* of the stable conditionals into
> *rotation-invariance (spherical Haar)* across a direction no entropy/expansion method reaches.

---

## 8. The synthesized tightest spec — what the tool MUST do and MUST NOT be

> **The missing tool.** A method that takes the **single specified orbit** `o₀=27` of `T` and produces an
> **a-priori, orbit-specific estimate of the conditional return-time / refill-magnitude law** of the 2-adic
> potential `V=v₂(c−1)` — specifically a tail bound `E[K²]<∞` ⟺ `Σ_n v₂(c_n−1)=O(N)` ⟺ occupancy `f_K` summable,
> equivalently the vanishing of the odd-character feedback `Inj_a(N)→0`, equivalently spherical-Haar-ness of the
> `A`-stable `ℚ₃`-leaf conditionals of the limit measure.
>
> **It acts on:** the *single orbit's specific 2-adic / archimedean arithmetic* (the refill magnitudes `K_i`, the
> moving-middle / hidden lower-digit injections), at the **excursion / return-time** level — never per-step, never
> on the invariant measure alone, never on a depth-function-only potential.
>
> **Its mechanism must be:** **non-spectral** (controls `V_odd`, where `L_ann` is blind, via the endogenous
> self-reference `β_n=bit_k(c_n)`), **measure-selecting** (non-constant on `M_feas`, selects Haar by orbit-specific
> data), and **central-direction** (acts on the neutral, zero-entropy `ℚ₃`-rotation axis where the host-invariance
> gap lives — not by entropy, expansion, unique ergodicity, or joinings).
>
> **It must NOT be:** a contraction / spectral gap; a bounded, magnitude-aware, or adelic sub-action / coboundary
> (product-formula-locked); a first-moment / count / annealed / all-orbits / residue-finite certificate; a per-step
> drift; a depth-function potential (self-closes at `0=0`); a high-entropy / unique-ergodicity / Host-joining
> rigidity argument.
>
> **The circularity it must avoid:** the conditional return-time law of `V` = the `D`-statistics = `E[K²]` = the
> occupancy `f_K` = (K) itself. The tool must derive its estimate **without assuming the D-law** and must
> **exclude the heavy-tailed, first-moment-matched, white adversary** that satisfies every proven unconditional
> fact yet halts. Equivalently: it must read the orbit's actual arithmetic, the one thing the adversary does not
> share — not the unconditional facts, which are consistent with both (K) and ¬(K).

In one sentence: **the tool is an a-priori single-orbit excursion estimate, acting on the refill magnitudes of
`V=v₂(c−1)` via the endogenous self-reference on a neutral/central direction, that selects Haar within `M_feas`
without reading the return-time law it is trying to bound.**

---

## 9. The two reduced build-targets, stated precisely

These are the two surviving, sharply-stated objects to BUILD (each is exactly one of the irreducible open lemmas
the no-gos isolate; both are (K)-hard but are the *precise* things a tool would have to deliver):

> **Build-target I — AIU neutral-direction host-invariance.** Prove that the `A`-stable `ℚ₃`-leaf conditionals
> `μ_x^3` of the Krylov–Bogolyubov limit measure `μ` are **`ℤ₃^*`-rotation-invariant (spherically Haar)** —
> equivalently `(×2)_*μ=μ` — via a **central-direction mechanism** that converts *non-atomicity* (which ENT gives)
> into *rotation-invariance* along the neutral `×2|_{ℚ₃}` axis (`|2|_3=1`, zero entropy). It must NOT route
> through entropy/expansion (EKL-blind), unique ergodicity (dissipative base, inert), or Host joinings (coupling
> is dependence). Source no-go: `AIU_JOININGS.md`, `AIU_SKEW_ROTATION.md`. The missing input: invariance along a
> zero-Lyapunov direction — a genuine, currently-toolless ergodic-theory target.

> **Build-target II — the a-priori excursion second-moment estimate (ENT / `E[K²]`).** Prove `E[K²]<∞` (⟺
> `Σ_n v₂(c_n−1)=O(N)` ⟺ `μ({1})=0` ⟺ a return-time decrease in the conditional law of `V=v₂(c−1)`) for the
> single orbit `o₀`, **a-priori** — from the orbit's specific 2-adic arithmetic (refill magnitudes / moving-middle
> digit), at the excursion level, **without** assuming the D-law and in a form that **excludes the heavy-tailed
> first-moment-matched adversary**. It must NOT be a depth-function potential (self-closes), a per-step drift
> (white), a count/first-moment budget (free but blind), or a sub-action (sign-locked). Source no-go:
> `EXCURSION_SYNTHESIS.md`, `EK2_SECOND_BUDGET.md`, `CORE_ORBIT_ARITHMETIC.md`. The missing input: a count→energy
> bridge in the proven 2-adic arithmetic — equivalently a power-saving on the quenched Weyl sum
> `(1/N)Σ e(t·(3/2)ⁿ)=o(1)`.

Both targets are the *same wall* in two languages (measure-rigidity vs. excursion-arithmetic): a single-orbit /
neutral-direction equidistribution that no existing method delivers for one growing-height, non-Pisot, degree-1
orbit. The tool of §8 is precisely what would supply either.

---

No machine decided. No label upgraded.
