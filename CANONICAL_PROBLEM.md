# The canonical problem — Antihydra / BB(6), expert-validated statement (2026-06-26)
*After mapping the wall from three independent fields (analytic NT / Mahler; Erdős ternary; homogeneous
dynamics) + all computational probes + an expert consultation, the problem has one canonical statement. The
expert verdict: the **formulation is correct** ("the way you've cut the problem is right"); the obstruction is
named; it is genuinely Mahler-class. This file records that endpoint of the "specify the wall" phase.*

## The canonical statement
> **Effective genericity of a specified algebraic point for a rank-1 hyperbolic / `S`-arithmetic automorphism.**

Concretely: for `A = ×(3/2)`, a hyperbolic automorphism of the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, is the **single
specified algebraic point** `x₀ = ` image of `1` (seed `8`) **generic** (its forward orbit equidistributes to
Haar)? `A` is ergodic+mixing, so a.e. point is generic; the named `x₀` is the open question.

## The obstruction, in one line (expert phrasing)
> **The obstruction is not recurrence; it is specified-point genericity.**

The one-sided margin (`avg jump ≤ 2` vs `→ 1`) is a **real logical weakening** but **current methods do not
exploit it**, because the bound is controlled by the **low-cylinder frequencies of one specified orbit** — which
returns to single-orbit genericity. Spectral gap gives Haar-a.e.; dense/aperiodic non-Haar orbits exist; so
"spread out" is not enough — only `x₀`-specific genericity suffices.

## Expert verdict on each face (2026-06-26 consultation)
- **Q0 (one-sided vs equidistribution):** *"I do not know of a theorem that separates the one-sided recurrence
  bound from full equidistribution for a specified orbit of a rank-1 expanding p-adic / Gibbs–Markov map."* →
  one-sided is **not provably easier** by current methods.
- **Homogeneous / Route 3:** *"The S-arithmetic formulation clarifies the hyperbolic structure, but I do not see
  a known mechanism by which the contracting 3-adic direction forces genericity of the specific algebraic
  point."* → the framing is **natural and correct**; the 3-adic stable direction aids *understanding*, not
  *proof*.
- **Q3 (moving middle digit):** *"I am not aware of any method reaching beyond the `Θ(log N)` top/bottom
  footholds for a specified orbit."* → confirms the foothold barrier.
- **Overall:** *"This appears to be genuinely Mahler-class. The one-sided margin is real as a logical weakening,
  but current methods do not exploit it because the bound is controlled by low-cylinder frequencies of one
  specified orbit."*

## What this validates (the value of the phase)
The expert explicitly confirms the **problem is cut correctly** and the **reason it is unknown is itself clear** —
which is exactly what makes it worth presenting to specialists. The programme's output is:
- an **exact reduction** (BB(6)/Antihydra → the canonical statement, machine-verified);
- the wall **mapped on every side** and shown to **coincide** across analytic NT, Erdős, and homogeneous dynamics;
- the obstruction **named precisely** (specified-point genericity, rank-1) with the literature deficiency anchored;
- rigorous partials that **excise the tractable part** of the exceptional set (Lemma 1: periodic points are
  repelling, no permanent trapping) — leaving the positive-entropy genericity as the irreducible core.

## The named multi-year target
> Invent **effective single-orbit genericity** for a **rank-1** hyperbolic / `S`-arithmetic automorphism at a
> **specified algebraic point**, where measure rigidity (rank ≥ 2) and a.e.-methods do not apply — possibly via a
> Diophantine input on `log₂3`.

This is the prize: a genuinely new equidistribution mechanism. It would resolve Antihydra **and** the whole
`v_p(μ)=−1` cryptid family **and** make progress on Mahler's 3/2 problem simultaneously. The companion expert
asks are `EXPERT_ASK.md` (p-adic / Gibbs–Markov) and `EXPERT_ASK_HOMOGENEOUS.md` (homogeneous dynamics).
