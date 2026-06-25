# Complete-proof meeting brief — Antihydra non-halt (2026-06-25)
*Purpose-built for a strategy session (incl. ChatGPT) aimed at the **complete proof**, not partials. Synthesises
the current state into: the exact target, the routes we have ruled out *ourselves*, the single surviving
question, and what we want from the meeting. Companions: `OPEN_PROBLEMS.md` (full list), `EXPERT_ASK.md`
(throwable), `STATE_FOR_REVIEW.md` (technical). Everything below is machine-verified or labelled. 0 false proofs.*

## 1. The target, exactly (verified)
Antihydra (`c_{n+1}=⌊3c_n/2⌋`, `c_0=8`) **never halts ⟺ `avg jump ≤ 2`** (running, all prefixes), where
`avg jump = (1/J)Σ_j v2(3c'_j−1) = (1/J)Σ_j v2(c'_j − 1/3)` = the renewal orbit's **average 2-adic proximity to
the single point `1/3 ∈ ℤ₂`** (`c'_j` = the renewal subsequence; `N_k/J` = visit frequency to the ball `2^{−k}`
around `1/3`). True value `≈ 1.00`; threshold `2` ⇒ a **factor-2 margin**.

## 2. Three nested statements — the complete proof is the middle one
| | bound | relation |
|---|---|---|
| positive density (partial, **not** the goal) | `avg jump ≤ const` | weaker than the proof |
| **COMPLETE PROOF** | **`avg jump ≤ 2`** | one-sided, factor-2 margin |
| equidistribution (Mahler 3/2) | `avg jump → 1` | **stronger** than needed |

**Key verified facts:** (a) the complete proof is **strictly weaker as a *condition*** than equidistribution — we
built a non-Haar orbit with `avg jump = 1.56 ∈ (1,2)` that satisfies non-halt without equidistributing. *(NB:
"weaker condition" does not by itself mean "easier to prove" — those are independent; see §3–§4.)* (b) it is
**seed-universal** — every natural seed gives `avg jump ≈ 1.00`, `N_2/J ≈ 0.25`, `N_3/J ≈ 0.125` (spread <1%), so
seed 8 is not a special pathology (the difficulty is the standard a.e.→specific gap, not a seed-8 anomaly); this
is an *observation*, not evidence that a structural argument exists — §3 proves no universal one does. (c) the
difficulty localizes to **small `k` (`k=2,3`, the orbit mod 4 / mod 8)** — the large-`k` tail is a separable
p-adic-Baker target.

## 3. Routes we have ruled out *ourselves* (the wall, mapped on every side — verified)
| route to `avg jump ≤ 2` | why it fails | tag |
|---|---|---|
| unique ergodicity | `F` has a continuum of invariant measures | [PROVEN] |
| rank-≥2 rigidity (Furstenberg/RL) | the orbit is rank 1 (one map `×3/2`) | [PROVEN] |
| Weyl / van der Corput | closed on the multiplicative recurrence `(3/2)^n` | [PROVEN] |
| transfer-operator spectral gap | orbit-blind — gives only μ-a.e. (lit-confirmed: all such results are a.e.) | [PROVEN] |
| non-shadowing / "spread out" | insufficient — built a dense, fully-supported orbit with `avg jump = 3.1` | [PROVEN] |
| growth / counting / telescoping | circular — `n = #even+#odd = J+ΣD` cancels `ΣD` | [PROVEN] |
| **universal drift / Lyapunov / sub-additive** | impossible — the bound is *false for some orbits*, so no orbit-independent `V` can prove it | [PROVEN] |
| second moment / variance | bounds *deviation*, not the mean — needs the limit (circular) | [PROVEN] |
| algebraic / self-referential | blocked — parity sequence has **maximal linear complexity** | [PROVEN] |
| distinct-integer counting | vacuous — orbit range `(9/4)^J ≫ 2^k` | [PROVEN] |
| p-adic Baker / linear forms | reaches only the **large-`k` tail** (non-binding); not the small-`k` core | [partial] |

**Net:** the factor-2 margin **weakens the tool required** (a one-sided moment `E_{μ_J}[D] ≤ 2` instead of full
Haar `E[D] → 1`) but **opens no new mechanism**. Mechanistically, the complete proof sits exactly where
Mahler 3/2 sits — it needs a *new orbit-specific tool*, just a strictly weaker one.

## 4. The single surviving question (for the meeting)
> **Is the one-sided, margin-2 moment `E_{μ_J}[D] ≤ 2` provable for the seed-8 orbit when full equidistribution
> (`E[D] → 1`) is not — i.e. does any technique *distinguish* a one-sided shrinking-target / recurrence bound
> from equidistribution for a single rank-1 orbit?** Concretely it asks for a one-sided bound on the orbit's
> visit frequency to the fixed cylinders `c' ≡ 3 mod 4, mod 8` *from above* (within the 2× margin) without
> pinning the exact frequency. (Drift/Lyapunov is already ruled out — §3 — so the mechanism, if it exists, is
> not a universal potential function.)

**What we want from the meeting:** (i) a **separating example** in the literature (one-sided shrinking-target
attainable while equidistribution open) — or a theorem that the two are **equivalent in difficulty**; (ii) any
**shrinking-target / recurrence** machinery for a single rank-1 `p`-adic orbit under a Diophantine hypothesis;
(iii) routing — which of these is best for a human ergodic-theory specialist vs an analytic number theorist.

## 4½. The theme has become its own object (framing note)
The question is no longer really "about Antihydra" — it is **"one-sided recurrence / shrinking-target vs
equidistribution for a single orbit of a rank-1 expanding `p`-adic (Gibbs–Markov) map."** Antihydra is the
concrete instance that motivates it, but the object is independent and is what will "land" with a dynamicist.
If anything is written up or asked externally, lead with the *dynamical* statement, not the Turing machine.

## 5. Honest stance
The complete proof is Mahler-3/2-class and we have **not** found a route; we have, rigorously, **closed every
standard one** and pinned the residue to a single weaker-than-equidistribution target. This is the "specify the
wall" phase delivering its sharpest output: the meeting is to confirm the wall's *type* (is the one-sided margin
a real opening, or the same wall?), not to ask anyone to solve Mahler. The independent deliverables
(cross-cryptid kernel classification, certificate-complexity hierarchy, the verified obstruction map) stand
regardless of whether the complete proof falls.
