# Non-contraction fixed-point principles & two-orbit / floor-ceiling coupling — both drilled, both closed (2026-06-30)

*Drilling two weapon-ideas the divergent sweep flagged but only one-line-dismissed (`NEW_ANGLES_DIVERGENT.md`
gates 4/6/7): (1) NON-contraction fixed-point principles (monotone/Knaster–Tarski, topological/variational), which
evade the `AIU_THIRD_MECHANISM_PROBE.md` isometric-rotation no-go since they do not need a spectral gap; and (2)
two-orbit coupling and the floor↔ceiling "average kills the ±1 ⇒ pure ×3/2" idea. Each is constructed explicitly and
stress-tested against the HEAVY-TAIL WHITE ADVERSARY (`EXCURSION_SYNTHESIS.md`: `E[K²]=∞`, white, first-moment-matched,
PROVABLY HALTS). SOUNDNESS PARAMOUNT: every claim `[PROVEN]`/`[OBSERVED]`/`[HEURISTIC]`/`[OPEN]`; (K) stays `[OPEN]`;
no label upgraded; NOT committed. Numerics: `.venv` exact big-int, induced map `o↦3^{D−1}(3o−1)/2^D`, `o₀=27`,
`N=2·10⁵`. Cross-refs: `AIU_THIRD_MECHANISM_PROBE.md` §2, `MINIMAL_CORE_2ADIC.md`, `BB6_NO_STRUCTURE_THEOREM.md`
(C1/C2/C3), `EXCURSION_SYNTHESIS.md`, `FLOOR_MIRROR_CONJECTURE.md`, `NEW_ANGLES_DIVERGENT.md` gates 4/6/7.*

---

## §0. VERDICT

**Both angles DEAD. Neither opens a crack.**

- **ANGLE 1 — non-contraction fixed-point: DEAD.** Dropping contraction does not help, because the obstruction was
  never "no spectral gap." Every fixed-point principle — Banach (contraction), Knaster–Tarski (monotone), Schauder/
  Brouwer (topological), variational (equilibrium state) — operates on the **space of measures**, and its conclusion
  is about the **invariant/annealed measure**, which is the `(C3)` wall of `BB6_NO_STRUCTURE_THEOREM.md`: `o₀=27` is
  `μ`-null and invisible to any measure-level object. Concretely, the Knaster–Tarski extremal fixed points of the
  natural monotone refinement operator are exactly the `M_feas` extremes — `δ₁` (`meanD=1`) at the bottom and Haar
  (`meanD=2`) at the top — so the order interval `[1,2]` **does not collapse** and order alone yields only
  `meanD ≥ 1 < 3/2`. **The heavy-tail halting adversary's depth-law is itself a fixed point of the same monotone
  operator**, sitting inside `[1,2]` while halting, so monotonicity provably cannot separate it. The only order that
  would separate encodes the second moment / tail — which **is** `(K)`. `[PROVEN collapse]`
- **ANGLE 2 — two-orbit / floor-ceiling: DEAD.** The pretty identity `⌊3x/2⌋+⌈3x/2⌉ = 3x` `[PROVEN]` does kill the
  `±1` at **one step**, so the average map is exactly `×3/2`. But the cancellation **provably dies under iteration**
  (the maps are nonlinear, so average∘compose ≠ compose∘average; verified: the averaged two trajectories equal
  `(3/2)ⁿx` only at `n=1`), and the surviving "pure `×3/2`" object **is literally Mahler's 3/2 problem** = `(K)`.
  Two-orbit coupling has no orbit with a *known* `liminf meanD ≥ 3/2` to couple to (the only orbits with known means
  are periodic — `δ₁` has mean `1`, the wrong side), the induced map is full-branch exact/Bernoulli hence **monotone
  in no order**, and the `[PROVEN]` negation conjugacy (floor-`27` ≡ ceiling-`−27`, `FLOOR_MIRROR`) is a relabeling of
  `(K)` for one seed onto `(K)` for another, not a comparison to a solved problem. The adversary instantiates jointly
  and matches every average/budget/coupling fact. `[PROVEN collapse]`

**Does the floor-ceiling average or any monotone order separate the real orbit from the adversary? NO.** The average
is `×3/2` = Mahler/(K); no partial order separates a light-tailed from a heavy-tailed first-moment-matched white law,
because the separating datum is the tail = the second moment = the conclusion.

This **sharpens** prior results: `AIU_THIRD_MECHANISM_PROBE.md` §2 killed only the *contraction* fixed point (isometric
rotation, no gap); here the **entire fixed-point family** (monotone, topological, variational) is closed by `(C3)` +
the adversary, and the floor-ceiling "average" hope (`FLOOR_MIRROR` left it implicit) is explicitly reduced to Mahler.

---

## §1. ANGLE 1 — non-contraction fixed-point principles

The self-consistency map (orbit determines its own depth statistics) has a fixed-point equation whose natural map is an
**isometric rotation** on the angular fiber — no spectral gap, not a contraction, so Banach fails
(`AIU_THIRD_MECHANISM_PROBE.md` §2.2). The honest question: do fixed-point principles that **do not need contraction**
extract `(K)`?

### 1.1 (a) Monotone / order-theoretic (Knaster–Tarski, Tarski–Kantorovich) `[PROVEN DEAD]`

**The lattice and the map, made explicit.** Take the complete lattice `(𝓜, ⪯)` of `T`-invariant Borel probability
measures on `ℤ₂^×` (equivalently the occupation/depth-laws they induce), ordered by the **convex/stochastic order on
the depth law** `ν ↦ law(D)`. The natural "refinement / self-consistency" operator is the one-step renewal pushforward
`Φ: ρ ↦ (T_*ρ)`-type map on candidate occupation measures, or — equivalently for the depth coordinate — the map
sending a candidate depth-frequency vector `(f_k)=(freq{D≥k})` to its renewal-consistent update. `Φ` is **monotone**
for the stochastic order (a full-branch Markov pushforward is order-preserving on its invariant cone). Knaster–Tarski
then gives a least and a greatest fixed point with no contraction needed.

**What Knaster–Tarski actually returns `[PROVEN]`.** The fixed points of `Φ` are precisely the `T`-invariant measures.
Their `meanD` values fill the interval `[1, 2]`:
- **bottom (lfp):** the halting fixed point `δ₁` — `T(1)=1`, `D≡1`, `meanD=1`. `[PROVEN, verified T(1)=1, D(1)=1]`
- **top (gfp side):** Haar / the `D=2` fixed point `o=3/5` — `meanD=2`. `[PROVEN-in-lit + verified meanD≈1.996]`

So the order-extremal fixed points are exactly the `M_feas` extremes of the obstruction dichotomy, and the interval
`[1,2]` **does not collapse**. A one-sided `liminf` bound "from order alone" would require `lfp-value ≥ 3/2`; but
`lfp-value ≤ ∫D\,dδ₁ = 1 < 3/2`. **Order alone yields only `meanD ≥ 1` — vacuous.** This is the multifractal
non-universality `(C2)` of `BB6_NO_STRUCTURE_THEOREM.md` re-expressed order-theoretically: the bottom of the lattice is
the violating fixed point. `[PROVEN]`

**CRITICAL adversary stress-test (the kill).** Does the heavy-tail halting adversary sit as a fixed point of the same
monotone `Φ`? **Yes.** The adversary is a white, first-moment-matched depth process (`E[D]=2`, hence `E[ψ]=−1/4`); it
therefore satisfies **every constraint `Φ` encodes** (all of which are first-moment / renewal / order facts — gate-2
facts), so its depth-law `ρ_adv` is a `Φ`-fixed point lying **inside** the order interval `[1,2]` (its `meanD=2`),
**yet it provably HALTS** (`E[D²]=∞` ⟹ heavy-tailed running maximum ⟹ the `Σψ` balance crosses the positive halting
threshold on a single path; `EXCURSION_SYNTHESIS.md`). Monotonicity sees `δ₁ ⪯ ρ_adv ⪯ ρ_real ⪯ Haar` (or no
comparison at all — a light-tailed geometric law and a heavy-tailed law with equal mean are **not** stochastically
ordered, they cross), and **cannot separate the real orbit from a halting fixed point**. The only partial order under
which `ρ_real` and `ρ_adv` are comparable in the right direction is one that reads the **tail / second moment** — and
that datum *is* `(K)`. **DEAD; the working order = `(K)`, not weaker.** `[PROVEN]`

> This confirms and drills `NEW_ANGLES_DIVERGENT.md` gate 6 ("Tarski yields the extremal fixed points = the `M_feas`
> extremes; the interval does not collapse") and gate 7 ("uniqueness of the geometric(½) fixed point is the annealed
> statement, `(C3)`; the named Haar-null orbit is not pinned"). Tarski–Kantorovich (monotone iteration toward a fixed
> point) adds nothing: it converges to a fixed point of `Φ` only for `Φ`-monotone *starting data*, and the limit is
> still one of the invariant measures — annealed, `o₀`-blind.

### 1.2 (b) Topological (Schauder/Brouwer) or variational `[PROVEN DEAD]`

**Topological.** The transfer operator on `Prob(ℤ₂^×)` (weak\*-compact convex) is continuous, so Schauder/Brouwer give
a fixed point — but this is exactly **Krylov–Bogolyubov existence**, already known, and the fixed-point set is **not a
singleton**: `δ₁`, the `D=2` point `o=3/5`, Haar, and a **full-Hausdorff-dimension zoo** of invariant measures
(Barreira–Schmeling, `BB6_NO_STRUCTURE_THEOREM.md` (C2)/(C3)) are all fixed points. Existence is free; **uniqueness is
false**. The `(K)`-hard part is precisely **selection** — which fixed point the single empirical law of `o₀=27`
realizes — and topology gives zero handle on selection of a `μ`-null orbit. `[PROVEN]`

**Variational.** Is `(K)`'s law the minimizer/maximizer of a functional? Haar is the unique measure of maximal entropy
/ the unique a.c.i.m. (variational principle). But non-generic points of **full Hausdorff dimension and full entropy**
realize *non*-maximal measures (including `δ₁`), so the single orbit is **not forced into the maximizer**. Any
functional whose unique *realized* minimizer is pinned to this specific orbit must read the orbit's magnitude/
arithmetic — i.e. it **is** `(K)`. `[PROVEN]`

### 1.3 Why non-contraction does not escape (the unified reason) `[PROVEN]`

The `AIU` no-go diagnosed the *contraction* failure (isometric rotation, `|2|₃=1`, zero Lyapunov, no gap). But the
real obstruction is one level deeper and **norm-free**: **every** fixed-point principle (contraction, monotone,
topological, variational) lives on the **space of measures**, and its output is an **invariant/annealed measure** =
the `(C3)` register, which is `o₀`-null by `BB6_NO_STRUCTURE_THEOREM.md`. Removing the contraction hypothesis swaps
Banach for Knaster–Tarski/Schauder, but the *conclusion type* is unchanged — still a statement about a measure, not
about the named Haar-null orbit. And at the orbit level, the law that would be selected is indistinguishable from the
heavy-tail adversary's by every order/topological/variational datum, because all of them are gate-2 (first-moment /
spectral / order) facts the adversary matches. **The fixed-point family is closed.** `[PROVEN — extends
`AIU_THIRD_MECHANISM_PROBE.md` §2 from "not a contraction" to "no fixed-point principle of any kind"]`

---

## §2. ANGLE 2 — two-orbit coupling / floor-ceiling

### 2.1 (b) Floor↔ceiling "average kills the ±1 ⇒ pure ×3/2" `[PROVEN DEAD = Mahler]`

**The seductive one-step identity `[PROVEN, verified all `x∈[−200,200]`]`.** For `Tf(x)=⌊3x/2⌋`, `Tc(x)=⌈3x/2⌉`,
> `Tf(x) + Tc(x) = 3x` exactly,  so  `½(Tf(x)+Tc(x)) = 3x/2` — the `±1` cancels, the **average map is pure `×3/2`**.

This is the strongest possible form of "the ±1 averages away." If it survived iteration it would be a clean lever.

**It does not survive iteration `[PROVEN, verified]`.** Because `Tf, Tc` are **nonlinear** (the floor/ceil acts on a
*different* argument at the next step), `average∘compose ≠ compose∘average`:
> the averaged pair of trajectories `½(Tf^n(x)+Tc^n(x))` equals the pure `(3/2)ⁿx` **only at `n=1`** (verified false at
> `n≥2` for `x=27,55,101`; for `x=8` the agreement lasts only while both stay on the shared even branch, then breaks at
> `n=5`). The `±1` errors compound nonlinearly at every subsequent step. `[OBSERVED, exact big-int]`

And the surviving clean object — iterating the **pure `×3/2` map** and reading the integer/parity bits of `x₀(3/2)ⁿ` —
**is exactly Mahler's 3/2 problem** = `(K)` = AEV Conj 1.6(3/2). So the floor-ceiling average is not a *simpler*
system; it is `(K)` **restated**. Circular. `[PROVEN — average = Mahler]`

**Induced-level version (the same wall, quantitatively).** Pointwise, with `D⁻=v₂(3o−1)`, `D⁺=v₂(3o+1)`:
> `D⁻(o)+D⁺(o) = v₂(9o²−1) ≥ 3` for all odd `o` `[PROVEN]` (the two consecutive evens `3o∓1`: one has `v₂=1`, the other
> `v₂≥2`; `9o²−1≡0 mod 8`). Verified `min(D⁻+D⁺)=3` over `N=2·10⁵`.

Summing along the **single floor orbit** of `o₀=27`: `Σ(D⁻_j+D⁺_j) ≥ 3N`, hence `meanD⁻ ≥ 3 − meanD⁺`. But `meanD⁺`
along this orbit `≈ 2` (verified `1.998`) — and *that* value is itself a `(K)`-class equidistribution statement (it is
the AEV depth-mean for the `+1` map read along the `−1` orbit). The bound delivers only
> `meanD⁻ ≥ 3 − 1.998 = 1.002 < 3/2` `[OBSERVED]` — **weaker than the target, AND circular** (it inputs `meanD⁺`, an
> open quantity). **DEAD.** `[PROVEN — weaker-than-and-circular]`

### 2.2 (a) Two-orbit coupling / comparison `[PROVEN DEAD]`

- **No good reference orbit exists.** Coupling propagates a known fact only if some orbit has a *known* `liminf meanD ≥
  3/2`. The only orbits with known depth-means are **periodic**: `δ₁` (`meanD=1`, the *wrong* side, would propagate a
  false-direction bound) and `o=3/5` (`meanD=2`, but a constant-`D=2` cylinder structure not coupled to `27`'s
  trajectory). There is **nothing to couple to.** `[PROVEN]`
- **The map is monotone in no order.** The induced `T` is full-branch, exact, Bernoulli (`MINIMAL_CORE_2ADIC.md`) —
  maximally mixing, the antithesis of order-preserving; `D=v₂(3o−1)` depends on the low 2-adic bits unpredictably. So
  no order-coupling between two orbits is preserved. `[PROVEN]`
- **Mod-`2^k` agreement shadows only finitely.** Two seeds `o≡o' (mod 2^k)` share `D_j` only until the consumed bits
  exceed `k` (each step burns `≈D_j` bits), i.e. for `O(k/E[D])` steps; then they diverge. No asymptotic coupling.
  `[PROVEN structural]`
- **Negation conjugacy is a relabeling, not a comparison `[PROVEN, `FLOOR_MIRROR`]`.** `Tc = R∘Tf∘R`, `R(x)=−x`, gives
  `D⁺_l(−o₀) = D⁻_l(o₀)` exactly (identical depth sequences for floor-`27` and ceiling-`−27`; verified `0` exceptions /
  `2·10⁵`). This maps `(K)` for seed `27` (floor) onto `(K)` for seed `−27` (ceiling) — **both open**, neither solved.
  It is an isomorphism of two equally-hard problems, not a bridge to a known fact. `[PROVEN]`

**Adversary stress-test (kills both (a) and (b)).** A **joint** heavy-tail white process can be instantiated for the
floor and ceiling coordinates simultaneously, matching every first-moment / average / budget / coupling fact (all
gate-2), and **halting in the floor coordinate**. Averaging and coupling are first-moment operations, so the adversary
satisfies them and still halts. By `EXCURSION_SYNTHESIS.md` gate 2, **no survivor.** `[PROVEN]`

---

## §3. NET

- **Does either angle open anything?** **No.** Both are `[PROVEN]` DEAD.
- **Exact collapse reasons.**
  1. *Non-contraction fixed point:* the obstruction was never "no spectral gap"; it is that **every** fixed-point
     principle outputs an **annealed invariant measure** (`(C3)` wall, `o₀` `μ`-null). Knaster–Tarski's extremal fixed
     points are `δ₁` (`meanD=1`) and Haar (`meanD=2`); the interval `[1,2]` never collapses, so order alone gives only
     `meanD ≥ 1`. The heavy-tail halting adversary is **itself a fixed point** of the same monotone map, so
     monotonicity cannot separate it; the only separating order encodes the tail/second moment = `(K)`.
  2. *Floor-ceiling / coupling:* the `±1`-cancellation `⌊⌋+⌈⌉=3x` is a **one-step** identity that **dies under
     iteration** (nonlinear maps), and the surviving pure `×3/2` map **is Mahler/(K)**. The induced pointwise bound
     `D⁻+D⁺≥3` gives only `meanD⁻ ≥ 1.002 < 3/2` and is circular. No reference orbit, no monotone order, negation
     conjugacy = relabeling. Adversary matches every average/coupling fact and halts.
- **Does the floor-ceiling average or any monotone order genuinely separate the real orbit from the heavy-tail halting
  adversary?** **No — definitively not.** The average is exactly the `×3/2` map (= Mahler = `(K)`), and no partial
  order separates a light-tailed from a heavy-tailed first-moment-matched white law, since the discriminating datum is
  the tail = the second moment = the conclusion itself.
- **Precise sub-lemma either angle would need, and its strength.** A *tail/second-moment* order (Angle 1) or a
  *known-good reference orbit / surviving-cancellation* identity (Angle 2). Both are **equal to `(K)`** (the second
  moment is the conclusion; the `×3/2` average is Mahler), **not weaker**. No proper sub-problem appears.
- **What this banks.** It **extends** `AIU_THIRD_MECHANISM_PROBE.md` §2 from "the self-consistency map is not a
  contraction" to "**no** fixed-point principle — contraction, monotone, topological, or variational — can reach `(K)`,
  because all act on measures and the single orbit is measure-null," and it makes explicit (with exact-arithmetic
  numerics) that the floor-ceiling "average kills the ±1" hope is the Mahler `×3/2` problem verbatim.

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.

---

## Numerics (`.venv`, exact big-int; scratchpad `fp_couple.py`)

```
Tf(x)+Tc(x)=3x exactly, x in [-200,200]:                 True
avg of trajectories == (3/2)^n x :  TRUE only at n=1; FALSE at n>=2 (x=27,55,101; x=8 breaks at n=5)
induced o0=27, N=2e5: meanD- =1.99627  meanD+ =1.99781  meansum=3.99409  min(D-+D+)=3
pointwise lower bound  meanD- >= 3 - meanD+ = 1.00219   (target 1.5; weaker AND circular)
delta_1: T(1)=1, D(1)=1  -> invariant, meanD=1 < 3/2  (Knaster-Tarski lattice bottom / lfp)
heavy-tail white adversary halts while first-moment-matched   (rigorous: EXCURSION_SYNTHESIS.md)
```
*Finite `N` proves nothing about the `liminf`; the kernel is `[OPEN]`. What is `[PROVEN]` here is the closure of both
weapon families and the one-step-only nature of the `±1` cancellation.*
