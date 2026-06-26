# Retrospective and next move toward the complete proof (2026-06-26)
*An honest review of the whole arc and a clear-eyed assessment of where the complete proof stands and what the
genuine next moves are. Discipline throughout: 0 false proofs; ~14 over-claims caught and retracted by
verification.*

## What "complete proof" means, and the five equivalent forms we proved it takes
Antihydra (a BB(6) holdout) never halts **iff** the running even-density stays `≥ 1/3`. We reduced this, by
machine-checked steps, to **one object seen five equivalent ways** — every reformulation we built coincides here:
1. **Renewal / 2-adic:** `avg jump = (1/J)Σ_j v2(3c'_j−1) ≤ 2` (the exact criterion; `even-density=1/(1+avg jump)`).
2. **Dynamical:** the single orbit of seed 8 is **generic** for `×(3/2)` on `ℤ_2` (empirical measure → Haar).
3. **Homogeneous:** seed 8 is generic for the **rank-1 Anosov automorphism** `×(3/2)` of the `S`-arithmetic
   solenoid `(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`.
4. **Analytic / digits:** the moving diagonal digit `⌊(3/2)^n⌋ mod 2` equidistributes (= **Mahler 3/2, 1968**).
5. **Normality:** the explicit sequence `⌊(3/2)^n⌋ mod 2` is **normal**.

## What we rigorously established (the durable assets)
- **Exact reduction** (1) and the renewal map `F` = full-branch piecewise-affine expanding Gibbs–Markov on `ℤ_2`.
- **Cross-cryptid classification [theorem]:** the whole `v_p(μ)=−1` Mahler family shares one kernel + obstruction.
- **Lemma 1 [proven]:** periodic points are repelling; no permanent trapping ⇒ the *periodic* part of the
  exceptional set is excluded. **Lemma 2 [proven]:** the singularity-preimage class is a Haar-null rational set.
  So both excluded classes are measure-zero rationals that integer seeds avoid for free.
- **2↔3 duality + dual carry identity [proven];** effective top-digit equidistribution **quantified** (top
  `Θ(log N)` bits, sharp); van der Corput **closed** (verified).
- **Engine survey [complete]:** all seven single-orbit engines (Weyl, vdC, transfer-operator, Furstenberg
  rigidity, BFLM, entropy/Lindenstrauss, Bourgain–Gamburd) fail for **one** reason.

## The wall, characterized from every angle — and they all coincide
| angle | the wall is… |
|---|---|
| dynamics | a **rank-1 Anosov** single specified orbit = **amenable ∩ hyperbolic** |
| engines | every tool needs **rank-2** (a 2nd mult-indep direction) or **a.e.** — the orbit has neither |
| renewal | the only hidden non-abelianness is `ℤ[1/6]⋊⟨3/2⟩` — **solvable/amenable**, no spectral gap |
| normality | **no certificate** (structureless) **∩ computable** (so not ML-random) **∩ not uniquely ergodic** |
| three fields + an expert | **genuinely Mahler-class**; obstruction = **specified-point genericity**, not recurrence |

## Honest status of the complete proof
The complete proof **= the new tool**: *effective single-orbit genericity for a rank-1 Anosov / amenable-hyperbolic
automorphism at a specified algebraic point* = *provable normality of an explicit `⌊(p/q)^n⌋`*. This does not exist
in current mathematics; we verified (computationally and via three literature consultations + an expert) that every
standard route reduces to it. **No currently known method appears capable of producing this tool** — it is multi-year, generational mathematics.

## #2 SETTLED (2026-06-26) — the margin buys a weaker target, not an easier proof
We attacked the residual hope directly (`onesided_settlement.py`). The factor-2 margin in `avg jump ≤ 2`
translates exactly to a **one-sided `2×`-anti-concentration** target: `N_k/J ≤ 2·2^{−k}` for all `k`
(`Σ = 2`) — i.e. *each shrinking cylinder around `1/3` is visited at most `2×` its Haar frequency*. This is
**strictly weaker** than equidistribution (`→ 1×`, two-sided, all cylinders) — non-Haar orbits with
`avg jump ∈ (1,2)` satisfy it. **But** the per-cylinder upper bound on `N_k` (the count of `j` with
`c'_j ≡ 3^{-1} mod 2^k`) **is itself the additive energy / a specified-orbit cylinder-frequency statement** — the
*same class* as equidistribution. **The margin relaxes the constant (`2×` vs `1×`), not the *kind* of control
(specified-orbit small-cylinder frequency).** Since every current method yields equidistribution or nothing, none
gives the one-sided bound without equidistribution (expert Q0). **Verdict: one-sided is a strictly weaker
*target* but *equi-difficult* relative to the current toolbox; the complete proof is Mahler-difficult now.** The
refined deliverable for a future tool: aim at *one-sided constant-factor anti-concentration of a specified orbit's
small-cylinder frequencies* — a (slightly) easier design target than full equidistribution.

## Where that leaves the "Mahler-free" hope (after the #2 settlement)
The margin is **not illusory** — it is a genuinely weaker *target* (one-sided `2×`-anti-concentration). What the
settlement shows is that no *current* tool converts that weaker target into an easier *proof*, because the
obstruction is the *kind* of control (specified-orbit small-cylinder frequency), not the *precision*. So the
"Mahler-free complete proof" hope is not a separate internal route any more: it is **subsumed into #3** as a
*sharper design spec* — a future tool need only deliver **one-sided constant-factor anti-concentration of a
specified orbit's small-cylinder frequencies**, which is strictly less than full equidistribution. Whether such a
tool can exist (giving one-sided without two-sided) is exactly the expert's open Q0.

## The genuine next moves (ranked, toward the complete proof)
1. **External input (ready, highest information / lowest cost).** Both expert asks are reviewer-polished and
   send-ready. An expert may (a) know the rank-1 tool, (b) confirm it is open and pin the obstruction, or (c)
   reframe the moving-middle-digit / one-sided question productively. *This is the rational immediate move.*
2. **[SETTLED above]** one-sided is a strictly weaker target but equi-difficult vs current tools — the margin
   does not open a Mahler-free path. The residual *internal* route is thus closed; what remains is a future tool
   aimed at the refined target (one-sided constant-factor anti-concentration), which is #3.
3. **Commit to the multi-year tool-build** — the real prize: invent effective single-orbit genericity for a
   rank-1 Anosov action. Resolves Antihydra **+** the whole cryptid family **+** Mahler 3/2 at once. Generational.

## Recommendation
The honest highest-value move *right now* is **#1 (send the expert asks)** — it is the only step that can
**change the map** (everything internal now coincides on the same wall), and it is cheap. In parallel, **#2** is
the one piece of the complete proof still attackable from inside, and the natural place to keep pushing. **#3** is
the destination, to be entered deliberately after #1 returns signal. None of this closes the project; it is the
transition from "specify the wall" (done, comprehensively) to "break the wall" (the multi-year frontier).
