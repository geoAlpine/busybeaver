# New attack-KINDS, generated divergently and stress-tested against the known no-gos (2026-06-30)

*Fresh-eyes divergent pass (external request). GOAL: generate genuinely new attack-KINDS for `(K)` — the single
specified 2-adic Bernoulli orbit `o_0=27`, `D_j=v₂(3o_j−1)`, want `liminf_N (1/N)Σ_{j<N} D_j ≥ 3/2` — and
**immediately adversarially triage each** against the program's proven no-gos, so nothing already-closed is
re-proposed as if new. SOUNDNESS: this is a brainstorming/positioning note. Nothing here proves or attacks `(K)`;
every verdict is a triage label, not a theorem. No `[PROVEN]` upgraded. `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
NOT committed.*

---

## The five gates every candidate must pass (the distilled no-gos)

A new angle is only worth a probe if it survives **all five**. These are the program's proven/verdict walls,
compressed into pass/fail tests:

1. **δ₁ gate (No-Structure C1/shared-free-structure).** The halting fixed point `o=1` (`D≡1`, mean 1) shares the
   orbit's entire *free* structure and is the ergodic-optimization maximizer (`β=+½`). Any argument that would also
   hold at `o=1` is dead, because `o=1` *halts*. → kills bounded-coboundary / Lyapunov / inductive-invariant certs.
2. **Heavy-tail-adversary gate.** A purely-2-adic depth process with `E[K²]=∞`, **first-moment-matched, white
   spectrum**, *halts* yet satisfies **every** proven one-orbit fact (`EXCURSION_SYNTHESIS.md`). Any argument using
   only first-moment / spectral-whiteness / proven-fact information cannot separate `o_0=27` from it. → kills all
   first-moment, valuation-budget, countdown, and white-noise/spectral arguments.
3. **Specification gate (No-Structure C2).** Full-branch `T` has specification ⟹ a **full-Hausdorff-dimension**
   set of orbits has `liminf freq(D≥2) < ½`. → kills every all-orbits / universal / topological argument.
4. **a.e./annealed gate (No-Structure C3).** `{o_0}` is Haar-null and the non-generic set has full entropy + full
   dimension (Barreira–Schmeling). → kills Birkhoff / decay-of-correlations / transfer-operator-spectral-gap /
   cone-contraction / convex-order-fixed-point / effective-ergodic-for-random-points arguments.
5. **Strength gate.** If the angle's natural output is *full equidistribution* (or "is this computable orbit
   normal"), it is at-least-as-hard as `(K)` and morally in the "is √2 normal" abyss; an honest crack must target
   the *weaker* one-sided `liminf` and exhibit a separator the adversaries lack.

The single recurring lesson: **a live angle must use a property the real orbit has that BOTH `δ₁` AND the
heavy-tail white adversary LACK, that is not annealed, and that is not itself ⟺ (K).** The candidate pool is
essentially the search for such a property.

---

## §0. The 1–2 least-dead candidates (lead)

### LEAST-DEAD #1 — Ostrowski / inhomogeneous Diophantine control at the *moving diagonal* using the continued fraction of `log₂3`  `[LONG-SHOT]`

**(a) Idea.** The leading-digit process of `c_n=⌊8(3/2)ⁿ⌋` is literally the irrational rotation by `α=log₂3`
(`log₂c_n = nα + O(1)`). `α` has **finite irrationality measure** (`μ(α) ≲ 5.1`, Rhin-type), so the rotation is
non-Liouville and its Birkhoff sums admit *polynomial-rate* equidistribution via the Ostrowski expansion of `n`
and three-distance/inhomogeneous-approximation control. The probe: push that effective control from the *leading*
digits down the 2-adic scale toward the parity/depth bit, exploiting that the renewal (inducing) structure links
adjacent scales.

**(b) Why it might evade the no-gos.** This is the one input that is **genuinely a property of `×(3/2)` that
neither adversary has**: the heavy-tail white adversary is a free-standing 2-adic depth process with **no `log₂3`
and no archimedean realization**; `δ₁` is `(3/2)`-constant and sees no rotation. So it passes gates 1–2 in
principle. It is not annealed (it concerns the one specified rotation orbit, which *is* effectively
equidistributed — Weyl + finite `μ(α)`), passing gate 4. It targets a one-sided density, passing gate 5.

**(c) Single most likely collapse.** **The depth-reach gap is exponential.** Diophantine information on `α` controls
only the **top `Θ(log N)` 2-adic digits** (banked partial #2: foothold reach `k(N)/log₂N ≈ 0.85`), because the
rotation governs the *archimedean size*. The depth bit `D_j` lives at 2-adic depth `Θ(j)` — exponentially deeper
than the rotation can see — and the only thing coupling the top digits to the bottom digit across that gap is
digit-mixing, i.e. equidistribution itself `= (K)`. Renormalizing through the inducing map adds only `O(1)` depth
per level while shrinking the orbit, so the reach cannot compound to `Θ(j)`.

**(d) Verdict `[LONG-SHOT]`.** The only candidate that wields a real `×(3/2)`-specific separator both adversaries
lack, and no *proven* theorem forbids extending Diophantine reach below the leading digits — but the log-vs-linear
depth gap is severe and is exactly where every prior digit attack (Mauduit–Rivat, top-digit) also stalled.

### LEAST-DEAD #2 — Principled partial construction of the adaptive *data-direction* (quenched/Oseledets) certificate  `[WORTH-A-PROBE, narrowly]`

**(a) Idea.** The coisometry no-go (`P-EUE`) is explicitly *operator-norm / top-exponent only*; it leaves the
**data-direction route OPEN** — a contraction in an anisotropic, orbit-adapted (Oseledets-filtration) weight that
encodes *where the specific orbit vector sits*. The program says "any such weight reduces to `(K)`." Probe whether
a **two-piece** construction sidesteps the circularity: a *magnitude-aware conditional* Lyapunov
`g(o)=α log o + h(o mod 2^k)` (`α<0`), valid **above a size threshold** (`P-EUE` / No-Structure §3 already note this
is the one cert the LP does not kill), **plus a separate, non-circular argument** that the threshold is crossed with
positive frequency — sourced from the *increasing-integer* constraint rather than from genericity.

**(b) Why it might evade the no-gos.** The conditional `g` is **unbounded**, so it is outside the LP/coboundary
class the δ₁ gate kills — it "cannot see δ₁ as a global obstruction" because `log` is constant there. That is the
single documented hole in the C1 no-go. It is orbit-specific (passes gates 3–4 by construction).

**(c) Single most likely collapse.** **The threshold-crossing sub-argument is itself the genericity content.** Every
known way to certify "the orbit spends positive density above the threshold" is a positive-density depth statement
`= (K)`, and the only threshold-free input — the valuation budget — is first-moment, so the heavy-tail adversary
(gate 2) crosses-or-fails the threshold *identically* to a halting orbit. The unboundedness buys freedom from δ₁ but
re-imports the wall at the threshold.

**(d) Verdict `[WORTH-A-PROBE, narrowly]`.** Honestly this is "LONG-SHOT that the program already flags OPEN." Its
only claim to a probe is that it is the **one route the proven no-gos do not close** (`P-EUE` scope is operator-norm
only; the unbounded conditional cert escapes the LP). The realistic value is to *precisely characterize* what the
threshold-crossing sub-lemma would have to be — and confirm whether it can be anything other than `(K)` in disguise.

---

## §1. Full triaged table (all candidates)

| # | Angle (kind) | Evades which no-go (hypothesis NOT needed) | Most likely collapse | Verdict |
|---|---|---|---|---|
| 1 | **Ostrowski / inhomog. Diophantine at moving diagonal** (§0 #1) — effective rotation-by-`log₂3` control pushed down-scale | Uses `×(3/2)`-specific `α`=`log₂3`; not shared with δ₁ or the white heavy-tail adversary; not annealed | log-vs-linear **depth-reach gap**: Diophantine sees top `Θ(log N)` digits, parity bit is at depth `Θ(j)` | **LONG-SHOT** |
| 2 | **Adaptive data-direction / Oseledets certificate** (§0 #2) — unbounded conditional Lyapunov + separate threshold-crossing | Unbounded ⟹ outside LP/coboundary (δ₁ gate); is the *one* route `P-EUE` leaves open | threshold-crossing sub-lemma = positive-density depth bound `= (K)` | **WORTH-A-PROBE** (narrowly; program-acknowledged OPEN) |
| 3 | **Birkhoff / Hilbert-projective-metric (positive-cone) contraction** — positive operators contract in projective metric even at op-norm-Lyapunov 0 | Sidesteps `P-EUE` (a *different* contraction notion than operator-norm/top-exponent) | cone contraction = transfer-operator spectral gap = **decay of correlations = annealed** (gate 4); already in closed thermodynamic class | **DEAD** |
| 4 | **Two-orbit coupling / monotone comparison** — relate `o_0=27` to a reference orbit or 2-adic ball | pathwise, not purely first-moment | ball-average = annealed (gate 4); difference doesn't close (`T` nonlinear via `3^{D−1}`); self-coupling = isometric rotation; random-copy coupling = **endogeneity defect**; any first-moment domination is satisfied by heavy-tail adversary (gate 2) | **DEAD** |
| 5 | **Non-termination prover / inductive-invariant (program-verification) reframing** — `balance_n≥0 ∀n` as a safety property; search a closed invariant in `(c, balance)`-space | fresh community/language (SV-COMP, recurrence-set provers) not in the catalogue | bounded invariant on `(c,balance)` **= C1 coboundary**, PROVEN infeasible via δ₁ (gate 1); unbounded invariant = magnitude-aware conditional `= (K)` | **DEAD** (= C1; mild *outreach* value only) |
| 6 | **Order-theoretic Tarski/Knaster fixed point** (vi, nonlinear) — monotone refinement operator on occupation-measure lattice; least=greatest would pin density | monotone ≠ contraction, so evades the isometric-rotation no-go | Tarski yields the **extremal** fixed points = exactly the `M_feas` extremes (Haar value **and** the δ₁ value); the interval does not collapse — re-derives the dichotomy, no uniqueness | **DEAD** |
| 7 | **Convex-order / stochastic-domination fixed point** — depth-law refinement under inducing, unique fixed point = geometric(½) | order-theoretic, not spectral | uniqueness of the geometric(½) fixed point is the **annealed** statement (holds a.e.-start, C3); the named Haar-null orbit is not pinned (gate 4) | **DEAD** |
| 8 | **Reverse / proof-by-contradiction via increasing-integer + Countdown budget** (viii) — assume halting ⟹ positive density of `D=1` ⟹ must replenish `v₂(o−1)` at positive rate ⟹ contradiction | uses the archimedean increasing-integer constraint + orbit-specific countdown | replenishment budget is **first-moment** (`ΣD_i = n+v₂(c_n)`; quadratic telescope reduces to it); heavy-tail adversary satisfies the budget and *halts* (gate 2) | **DEAD** |
| 9 | **Algorithmic-randomness / effective-Birkhoff at the computable point** — effective ergodic theorems for the specified orbit | targets a single specified point directly | effective Birkhoff (Galatolo–Hoyrup–Rojas; Pathak–Rojas–Simpson) holds at **ML/Schnorr-random** points; our orbit is **computable ⟹ not random**, so the theorem provably does *not* apply (this is *why* it is hard) — gate 4 in computability clothing | **DEAD** |
| 10 | **Additive-combinatorics inverse theorem in reverse** — halting ⟹ parity word correlates with a structured (nilsequence/multiplicative) object ⟹ contradiction with `×3` structure | structure-vs-randomness dichotomy applied for contradiction | the structured contradiction sought is a Gowers-norm / sum-product / multiplicative-energy statement — **the closed Mauduit–Rivat/Gowers/sum-product classes**; carry is the entire self-fed history (unbounded), outside Subspace/MR reach | **DEAD** |
| 11 | **Cross-place / adelic-consistency separator** — the heavy-tail adversary has no consistent `{8(3/2)ⁿ}` archimedean shadow | distinguishes the real orbit from the abstract adversary | the **3-adic sliding-lock + factor identities** PROVE the other places are deterministic factors of `(D_j)`, so any depth process lifts to a *formal* consistent shadow; the only genuine constraint is that the real shadow is `{8(3/2)ⁿ}` = **Mahler = (K)** (circular) | **DEAD** (`MINIMAL_CORE_2ADIC.md`) |

---

## §last. Honest net: is the space closed, or is there a crack?

**Net: the space is ~closed, with exactly one hairline crack worth a single careful probe.** Of the eleven kinds,
nine are **DEAD** — each collapses through one of the five gates, and in every case the collapse reason is *proven*
in the program (δ₁, heavy-tail adversary, specification, annealed-null, or the sliding-lock), not merely "unsuccessful."
Most strikingly, the heavy-tail white adversary alone executes seven of the nine kills: any argument built from
first-moment, spectral-whiteness, coupling-to-a-reference, budget, or order/convexity information is defeated by an
object that provably *halts* while matching all of it. And the strength gate places `(K)`'s full-equidistribution
sibling in the same abyss as "is √2 / log 2 normal," where current mathematics proves nothing for any natural
constant — a strong independent signal that the *generic* attack space is genuinely empty, consistent with the
recent literature (2024–25 effective-equidistribution advances are all unipotent/semisimple/rank-2; effective-Birkhoff
results require randomness our computable orbit lacks; no rank-1 amenable single-specified-orbit tool appeared).

**The one hairline crack** is the conjunction the proven no-gos *do not* close: an **adaptive, unbounded,
orbit-adapted (data-direction) certificate** (#2) — the sole route `P-EUE` explicitly leaves open because it is
operator-norm-only — **fed by a `log₂3`-Diophantine input at the moving diagonal** (#1), the only separator both
adversaries lack. Each alone is a LONG-SHOT (depth-reach gap; circular threshold-crossing); their *combination* is
the honest frontier, because #1 supplies precisely the orbit-specific, non-annealed data #2 needs to populate its
weight without invoking genericity. I would not bet on it, but it is the one place the program's own proven walls
genuinely stop short of, rather than a route already shown to reduce. Everything else re-proposes a closed class.
**No label upgraded; `(K)` remains `[OPEN]`.**

*Sources consulted (2024–26 sweep): Lindenstrauss–Mohammadi–Wang–Yang, effective equidistribution rank-2
(arXiv:2503.21064) and the unipotent/semisimple line (arXiv:2407.12760, 2211.11099) — all higher-rank/unipotent;
Mahler-3/2 recent (arXiv:2411.03468 ℤ⁺-restriction; arXiv:2502.17090 asymptotic Mahler) — no density/single-orbit
tool; effective-Birkhoff for random points (arXiv:1007.5249, 2202.13465; Pathak–Rojas–Simpson) — requires
ML/Schnorr randomness, inapplicable to a computable orbit.*
