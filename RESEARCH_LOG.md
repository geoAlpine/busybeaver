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

## 2026-06-24 (cont.) — M1 structural attempt: D2 clarified as EQUIVALENT to the conditional theorem (redirect)
Pursued M1's structural proof (`δ(P^k)=0 → Φ contraction → uniqueness`). Two findings, both honest negatives:
1. **Φ is NOT a pathwise contraction** (`M1_influence.py`): a single incoming-bit flip's influence on the
   future parity does **not decay** — it jumps to `~0.5` at lag k and stays there (sum of influence diverges).
   So `δ(P^k)=0` (forgets the START) does **not** give forgetting of incoming PERTURBATIONS. The Banach-via-
   pathwise-coupling route fails.
2. **The fixed-point uniqueness is equivalent to (H), not a step past it** [the key realisation]. The
   fixed-point simulations feed incoming bits from an RNG = **independent of the state**. But state-
   independence *is* (H). So "the unique self-consistent process is Bernoulli" really proves
   `(H) ⟹ Bernoulli ⟹ even-density ½ ⟹ non-halt` = **the conditional theorem we already hold**. The real
   orbit's incoming is *state-coupled* (incoming `bit_k(c_n)` and state `c_n mod 2^k` are digits of the same
   `c_n`); RNG-feeding erases exactly that coupling. **D2 presupposes (H); it does not advance toward proving it.**

**Consequence for the programme.** **D2 (self-generated-process uniqueness) is closed** as a route to (H):
any analysis that feeds the incoming independently of the state assumes (H). A genuine attack must engage the
**state–incoming coupling of the actual deterministic orbit** — which is exactly what D1 (effective measure
rigidity: control a specific orbit, coupling intact) and D3 (carry calculus: the arithmetic of the coupling)
are about. The in-house D2 shortcut does not exist.
- **6th tempting result caught on scrutiny** (the M1 "partial" assumed (H)). Discipline holds: 0 false claims.
- **Revised next step:** pivot to **D3 (carry calculus)** — the most concrete coupling-respecting in-house
  line: model the carry of `×3` into the moving bit directly and seek any unconditional anti-concentration,
  however weak (Milestone M2: any non-trivial unconditional bound). And begin reading into **D1** (effective
  equidistribution) as the external frontier.
