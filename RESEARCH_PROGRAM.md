# Research programme — new mathematics to prove BB(6)'s open core
*A long-horizon agenda (not a one-session attack). Target: prove the single hypothesis (TIER 0), i.e. the
diagonal base-p digit of a 2^a/3^b orbit equidistributes — which decides Antihydra/o18 and their families via
the rigorous conditional theorem. = Mahler 3/2 (1968) + Erdős ternary (1979).*

## 0. The precise target (sharpened to the bone — already done)
Decide a cryptid ⟸ the **conditional theorem** (`UNIFIED_CONDITIONAL_THEOREM.md`, rigorous core, exact
arithmetic) whose ONLY open input is:
> **(H)** the incoming high digit `dig_k(c_n)` is asymptotically independent of the low-digit state
> `c_n mod p^k` (equivalently the diagonal digit `⌊μ^n⌋ mod p` equidistributes; equivalently the orbit's
> middle bits equidistribute).
Everything else (model-exactness, total contraction `δ(P^k)=0`, bijective equidistribution transfer, family
universality) is PROVEN. The programme is: build the mathematics that proves (H).

## 1. The map of the terrain (what 10 attacks established — so we don't repeat)
**Dead ends (proven why each fails):** van der Corput / Weyl (differencing-closed); sum-product
(log-size-subgroup regime, exp below threshold); ×2,×3 measure rigidity *as invariant-measure theorems*
(a single orbit furnishes no positive-entropy invariant measure); subspace theorem (fixed number vs moving
orbit); Benford foothold (capped at Θ(log n), exponentially short of the diagonal); solenoid bundling (the
two unstable directions coincide; no extra leverage); foothold+contraction combination (opposite ends, open
middle); CA randomization (model unfaithful — falsified). All converge to the same wall: **specific-orbit vs
a.e.** / **control of the uncontrolled middle bits**.

## 2. Where new mathematics could genuinely come from (live directions, honestly ranked)
**(D1) Effective measure rigidity for the specific orbit** — the Einsiedler–Lindenstrauss–Venkatesh
*effective* equidistribution programme (active 2010s–2020s frontier). The non-effective ×2,×3 theory can't
touch a single orbit; an *effective* version with a Diophantine-genericity input on the seed might. This is
the most likely external source of the eventual tool. *Programme task:* learn the effective machinery; find
the precise Diophantine condition; test whether seed 8 / the orbit satisfies it.
**(D2) A uniqueness theorem for SELF-GENERATED processes** — *ours to build*, grounded in our proven renewal
contraction. The orbit's parity law is a fixed point of Φ under the *diagonal* constraint (incoming law =
output law, because the bits are one sequence). The adversarial min=0 shows free fixed points are bad, but
the diagonal self-coupling is a strong extra constraint. *Conjecture to prove:* the only diagonally-self-
consistent shift-invariant fixed point of Φ is Bernoulli(1/p). This may be provable by ergodic/algebraic
means WITHOUT the full equidistribution. **Most promising in-house direction.**
**(D3) A carry calculus / additive combinatorics of the ×3-in-base-2 carry** — the core object (the
"carry into bit n of 3^n") is under-theorised. Build the combinatorics/anti-concentration of these carries
directly (beyond sum-product's regime). *Programme task:* develop the carry-propagation algebra; seek an
anti-concentration inequality uniform in the moving modulus.
**(D4) Embedding in a master conjecture** — reduce (H) to a single named conjecture (effective
equidistribution of `{(p/q)^n}`, or a Furstenberg-type orbit-closure statement), turning "open" into
"conditional on X", which clarifies and connects to others' progress.

## 3. Milestones (stepping stones — each a real result short of the full proof)
- **M1 [in-house, start here].** Prove the **fixed-point uniqueness** (D2) for processes determined by
  ≤ m-blocks, for increasing m — a rigorous partial: "no self-consistent parity law of memory ≤ m has
  even-density ≤ 1/3." Push m upward; seek the structural reason it holds for all m.
- **M2.** An **unconditional partial bound** beyond the trivial `depth ≤ 0.585n`: any explicit
  `even-density ≥ ε > 0` (density sense), or `depth = o(n)` along a positive-density subsequence, or an
  effective discrepancy bound on the orbit's bits at depth `ω(log n)`.
- **M3.** Reduce (H) to a **named conjecture** (D1/D4) — a clean conditional theorem under a standard
  hypothesis.
- **M4.** Build the **new tool** (D2 full / D3) that removes the hypothesis.
- **M5.** The full unconditional proof of (H) ⇒ decide the cryptid cores ⇒ (with the mechanical TIER 3)
  BB(6).

## 4. Infrastructure (for sustained multi-session work)
- This file = the standing agenda. `RESEARCH_LOG.md` = dated progress entries (append-only).
- Discipline carried over: every claim machine-checked; verify key predictions vs the real orbit before
  claiming; 0 false proofs; retract on falsification (5 caught so far).
- Reusable artefacts: `UNIFIED_CONDITIONAL_THEOREM.md` (the rigorous spine), `BB6_KERNEL_PROBLEM.md` (the
  paste-ready open statement), the renewal/contraction toolkit (`rigor_*.py`).

## 5. The stance
Mahler-3/2 is 57 years open; this is a marathon, pursued across many sessions. Progress = milestones, new
techniques, and partial results — not a single leap. We have already brought the problem to its sharpest
known form (one located hypothesis + a proven core). The next real step is M1.
