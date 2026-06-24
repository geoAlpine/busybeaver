# Research log — new mathematics for BB(6)'s open core
*Append-only, dated. Agenda in `RESEARCH_PROGRAM.md`. Discipline: machine-check, verify vs real orbit, 0
false proofs, retract on falsification.*

## 2026-06-24 — Programme established; Milestone M1 first step (D2: self-generated-process uniqueness)
**Set up:** `RESEARCH_PROGRAM.md` — target = hypothesis (H) (diagonal digit equidistributes); 10 dead ends
mapped; live directions D1 (effective measure rigidity), **D2 (fixed-point uniqueness — in-house, started)**,
D3 (carry calculus), D4 (master conjecture); milestones M1–M5.

**M1 first step [numerical partial]:** Among **order-≤2 Markov self-consistent fixed points** of the renewal
operator Φ, there is a **UNIQUE** one = Bernoulli(½) (even-density 0.5). Verified: 13 starts spanning the
parameter box — including adversarially-skewed ones — ALL converge to it (`M1_fixedpoints.py`). Order-1 was
already unique (Bernoulli) and globally attracting (`phi_fixedpoint.py`). So **no self-consistent parity
process of memory ≤ 2 has even-density ≤ 1/3 ⇒ none halts.** Recall the *adversarial* min (no self-
consistency) was 0 — the self-consistency (diagonal) constraint is what collapses the fixed set to {½}.

**Why this matters / path to rigour.** This is the in-house route that sidesteps "specific-orbit vs a.e.":
instead of equidistributing the specific orbit directly, prove the *structural* fact that Φ has a unique
self-consistent fixed point. The proven contraction `δ(P^k)=0` (chain forgets its state in k steps) is the
candidate engine: it should force the output process's dependence on the incoming far-past to decay ⇒ a
unique fixed point. Turning "numerically unique for order ≤ 2" into "provably unique for all orders" is the
M1 research line.

**Next steps (M1):**
1. Extend the fixed-point characterisation to order 3, 4 — confirm uniqueness persists.
2. Prove uniqueness *structurally* from `δ(P^k)=0`: show Φ is a contraction in a process metric (total-
   variation on k-blocks), giving a unique fixed point by Banach — independent of order. This would be the
   first genuinely NEW theorem of the programme (a self-consistency uniqueness theorem).
3. Compute the fixed point's even-density exactly (= 1/p) from the bijection F_k structure.
4. Then: connect "Φ-unique-fixed-point = Bernoulli" to "the real orbit's empirical bit-measure is a Φ-fixed
   point" — the remaining bridge (this is where (H)'s residue concentrates).
