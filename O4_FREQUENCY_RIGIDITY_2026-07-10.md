# o4 via the frequency FUNCTION φ on seed-space — rigidity of the invariant function, and why it reveals (K) anew (2026-07-10)

*A genuinely new framing for the o4 (K) wall: instead of bounding the residue-1 frequency of the ONE seed-43 orbit
(all ~14 prior tools failed on the maximal structurelessness of that single sequence), treat the asymptotic
frequency as a FUNCTION `φ` on the whole seed-space `ℤ₃` and attack its rigidity/regularity via the functional
equation `φ = φ∘T` plus preimage-averaging. Hope: a statement about φ on ALL seeds sidesteps single-orbit
genericity. Verdict: the framing is clean and yields a genuine a.e.-rigidity theorem, but it **reveals (K) as the
pointwise regularity of φ at one measure-zero point rather than escaping it** — precisely because a SINGLE expanding
map has no Furstenberg-type rigidity. Interpreter `.venv` python, exact big-int / exact conjugacy. STRICT labels.
Scripts `scratchpad/o4_freq_rigidity.py`, `o4_conjugacy.py`, `o4_funceq.py`. NOT committed.*

---

## 0. One-line verdict
**[INSUFFICIENT — does not decide, no label upgraded].** `φ(v) = freq{ρ_n=1}` is the symbol-`1` frequency of a
**genuine full-shift coding** of `(ℤ₃,T)`; Birkhoff + ergodicity give `φ = 1/3` **Haar-a.e. `[PROVEN]`** (the
invariant function IS a.e. constant — the rigidity is real). But `{φ ≥ 4/5}` is a **Besicovitch–Eggleston set of
Hausdorff dimension 0.582 `[PROVEN]`** — positive-dimensional, NOT the dimension-0 backward orbit of `δ₋₁₄` the task
hypothesized — and membership of seed 43 in it is exactly quenched base-3 digit-frequency = **(K)**. A single
expanding map has no Furstenberg/Rudolph rigidity, so nothing forces φ constant off a dimension-0 exceptional set.
**No machine decided. No label upgraded.**

## 1. φ defined; the map is a FULL 3-SHIFT `[PROVEN, exact]`
`T(G) = (4G + e(G mod 3))/3`, `e = {0:9,1:14,2:1}`, branch fixed points `x_ρ = −e = {−9,−14,−1}`. `φ(v) :=
lim_N (1/N)#{n<N : G_n ≡ 1 (mod 3)}` along the T-orbit. Trivially **`φ(v) = φ(T(v))`** (dropping one term leaves the
tail-frequency unchanged) — φ is T-invariant.

The decisive structural fact: **`v ↦ (ρ_0,ρ_1,…)` is an exact conjugacy of `(ℤ₃,T)` to the one-sided full 3-shift.**
The residue map `G mod 3^k ↦ (ρ_0,…,ρ_{k−1})` is a **bijection** `ℤ/3^k → {0,1,2}^k`, verified exhaustively for
`k=1..8` (all `3^k` words realized, multiplicity 1). Equivalently T is **3-to-1** on `ℤ₃` (each `H` has exactly one
3-adic preimage per residue `ρ`, since `G=(3H−e(ρ))/4` and `4` is a 3-adic unit, and automatically `G≡ρ`), with **no
forbidden transitions** — the full shift. Under this conjugacy **Haar ↔ uniform Bernoulli(1/3,1/3,1/3)**, and
**φ(v) = frequency of symbol `1`** in v's itinerary. So o4 is *literally* a base-3-type digit-frequency problem
(the sibling, in T's own coordinate, of the base-3/2 external anchor `DICT_AND_EXCDIM`).

## 2. The functional equation / preimage averaging — why it does NOT pin φ `[PROVEN]`
The three 3-adic preimages `v_0,v_1,v_2` of `H` (one per residue) each satisfy `φ(v_ρ)=φ(T v_ρ)=φ(H)`. Hence the
transfer/preimage-average equation
> `φ(H) = (1/3) Σ_ρ φ(v_ρ)`   ( `φ = L φ`, L the Haar transfer operator )

holds **trivially — with all three summands already equal to `φ(H)`.** So the cohomological equation `φ=φ∘T` (a
coboundary equation with zero cocycle) imposes only that φ is **constant on grand orbits**. Its **continuous**
solutions are constants (T is topologically transitive); its **measurable** solutions are a.e. constant (exactness,
§3) but pointwise **unconstrained on any Haar-null set**. The solution space "measurable T-invariant functions" is
therefore infinite-dimensional modulo null sets — **preimage-averaging supplies no extra rigidity.** This is the
functional-equation face of the annealed↔quenched wall (`O4_TRANSFER_OPERATOR_BUILD`): L's action is exactly the
averaging that φ already satisfies for free.

## 3. The rigidity theorem that DOES hold `[PROVEN]`
T conjugate to the uniform-Bernoulli full 3-shift ⟹ T is **exact, mixing, ergodic** w.r.t. Haar. Birkhoff applied to
the indicator of the `ρ=1` cylinder ⟹ the time-average converges, for **Haar-a.e. v**, to the cylinder measure:
> **`φ(v) = 1/3` for Haar-a.e. `v ∈ ℤ₃`.  [PROVEN]**

Numerics match exactly: `φ(v) = 0.3317±…` for every integer seed in `[−20,39]` **except** the eventual-fixed-point
seeds `−14 (φ=1)`, `−9,−7,−3,−1 (φ=0)` (these fall onto the `ρ≠1` branch fixed points `x_0=−9, x_2=−1`). This is the
"invariant function is a.e. constant" rigidity the task sought — and it is **genuinely true**. It just says nothing
about any single specified point.

## 4. The crux — regularity of φ, and the exceptional set `{φ ≥ 4/5}` `[PROVEN]`
- **φ is discontinuous EVERYWHERE, not only at `−14`.** Both `{φ≈1/3}` and `{φ≥4/5}` are **dense** (any finite 3-adic
  prefix extends to either a mostly-`1` or a mostly-non-`1` tail — constructed explicitly: two seeds agreeing mod
  `3^5` with prefix-freq `0.71` vs `0.07`). Hence `{φ≥4/5}` is **not closed**; φ is **neither u.s.c. nor l.s.c.**,
  a Baire-class-2 function. **Every topological-regularity route (semicontinuity, oscillation control) is dead.**
- **The exceptional set is a positive-dimension multifractal.** By Besicovitch–Eggleston, `dim_H{φ=f} = H(f)/log3`
  with the entropy-maximizing law `Bernoulli(f,(1−f)/2,(1−f)/2)`. Since this decreases for `f>1/3`,
  > **`dim_H{φ ≥ 4/5} = H(4/5)/log 3 = 0.5817` `[PROVEN]`** (Haar-measure 0, but Hausdorff dimension `0.582`).
- **This REFUTES task-hypothesis (3).** The backward orbit of `δ₋₁₄` is the set of **eventually-all-`1`** itineraries
  — all with `φ=1`, a **dimension-0** set. `{φ≥4/5}` (dim `0.582`) is **vastly larger**; it is a full
  Besicovitch–Eggleston level set, not the closure of `−14`'s backward orbit. The heavy-frequency points are a fat
  fractal, not a thin orbit-closure.

## 5. Why the framing reveals (K) rather than escaping it — no single-map rigidity `[PROVEN reasoning]`
The hope was a Furstenberg-type rigidity forcing φ constant off a negligible set. **Furstenberg/Rudolph rigidity
requires TWO multiplicatively-independent maps** (`×2` and `×3`) **plus positive entropy** (Rudolph); it is a
**higher-rank** phenomenon. Here there is **one** expanding map T. A single expanding map has a **full multifractal
spectrum** of ergodic invariant measures — every `Bernoulli(f,·,·)` is T-invariant and ergodic, realizing `φ=f` on a
positive-dimension set. **So no rigidity theorem forces φ constant off a dimension-0 set; the dimension-`0.582`
exceptional set is unavoidable and correct.** Deciding o4 = deciding whether seed 43 lands in this fat fractal:
- **Seed 43's membership.** Empirically `φ(43) → 1/3` (finite-depth symbol-`1` freq `0.320→0.333` at depth `10²→10⁵`;
  orbit average `0.3339` at `N=2×10⁵`) — so `43 ∉ {φ≥4/5}` **numerically, with huge margin** (`1/3 ≪ 4/5`). But to
  **prove** `43 ∉ {φ≥4/5}` is to prove its itinerary is not `4/5`-heavy in symbol `1` = quenched base-3
  digit-frequency of one specified orbit = **(K)** (the T-coordinate mirror of Mahler 3/2 / AEV Conj 1.6). Birkhoff
  is silent on this one measure-zero point; that silence **is** (K).

## 6. Verdict `[honest]`
The frequency-function framing is the correct language and it delivers a **real** rigidity theorem — `φ = 1/3`
**Haar-a.e. `[PROVEN]`**, the invariant function is a.e. constant, and preimage-averaging + the full-shift conjugacy
are exact. It does **not** decide o4, and it pinpoints why in a **new, sharp** way: (i) the functional equation
`φ=φ∘T` is satisfied by every grand-orbit-constant function and adds no rigidity (the preimage average is trivially
`φ(H)`); (ii) φ is **discontinuous everywhere** and **Baire-class-2**, killing all regularity routes; (iii) the
exceptional set `{φ≥4/5}` is a **Besicovitch–Eggleston fractal of dimension `0.582`**, NOT a dimension-0 orbit
closure — so **no Furstenberg/Rudolph rigidity applies** (that needs two m.i. maps + entropy; o4 has one map). The
new characterization of (K): **o4 ⟺ "seed 43 lies outside the dimension-0.582 fat fractal `{φ≥4/5}`," a pointwise
multifractal-membership question about a single measure-zero point that the a.e. rigidity provably cannot see.** The
framing converts "single-orbit genericity" into "pointwise regularity of an a.e.-constant, everywhere-discontinuous
invariant function" — the same wall, freshly and precisely lit, not crossed.

Reproduce: `scratchpad/o4_freq_rigidity.py` (φ for integer seeds; a.e.=1/3; seed-43 convergence),
`o4_conjugacy.py` (mod-`3^k` bijection to the full 3-shift, k=1..8; Besicovitch–Eggleston dimensions; seed-43 depth
frequencies), `o4_funceq.py` (trivial preimage average; discontinuity-everywhere witnesses; backward-orbit-of-`−14`
= dim-0). Basis: `O4_TRANSFER_OPERATOR_BUILD`, `O4_EXPSUM_FREQUENCY_BUILD`, `O4_RUN_STRUCTURE`, `NEW_MATH_PROGRAM`,
`DICT_AND_EXCDIM`. Literature: Furstenberg ×2×3 / Rudolph (rigidity needs two m.i. maps + entropy);
Besicovitch–Eggleston digit-frequency dimension.

**No machine decided. No label upgraded.**
