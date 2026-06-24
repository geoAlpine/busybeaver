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

## 2026-06-24 (cont.) — D3 carry calculus: foundation laid + a genuine AFFINE structural lead
Pivoted to D3 (coupling-respecting, in-house). Set up and **verified** the carry calculus
(`D3_carrycalculus.py`, `D3_linear.py`):
- **Exact identities [verified]:** `2^n c_n = 8·3^n − S_n`, `S_{n+1}=3S_n+2^n[c_n odd]`, and
  `depth_n = v2(8·3^n − S_n − 2^n) − n`.
- **Trivial bound only:** empirically `depth_n ≤ 0.319·log2(c_n)`, but the provable (trivial) ceiling is
  `depth_n ≤ log2(c_n) ≈ 0.585n`. Closing even this factor-3 gap unconditionally is open (Milestone M2).
- **★ Structural lead [verified, genuinely new handle]:** `S_n = Σ_{j<n, c_j odd} 2^j 3^{n−1−j}` is **LINEAR
  in the parity bits** `e_j=[c_j odd]` (explicit coefficients), so **`depth_n ≥ L ⟺ S_n ≡ 8·3^n−2^n
  (mod 2^{n+L})` is an AFFINE condition on the parity history.** The even-density / depth statistics are
  therefore controlled by **linear forms** in `(e_0,…,e_{n−1})` with explicit `2^j3^{n−1−j}` coefficients.
- **Why it's promising (and honest about limits):** linear/affine conditions are the regime where
  **exponential-sum / Fourier methods** can succeed even when the nonlinear digit-equidistribution cannot
  (cf. the Mahler wall is fundamentally *nonlinear*). This is a handle the other directions lacked. The
  self-reference (`e_j` is itself a low bit of the orbit) is NOT removed — but the concrete D3 sub-problem is
  now sharp: **bound the linear-form exponential sum `Σ_n e(t·Φ_n(e))`** where `Φ_n` is the explicit affine
  depth-form, using the `2^j3^{n−1−j}` (mixed 2,3) coefficient structure. *Not* the same as the general
  equidistribution — a genuinely different, more linear target.
- **Status:** D3 foundation + lead established; **no unconditional bound yet** (no over-claim — this is a
  framework + a sharp sub-problem, not a result). This is now the most promising live in-house direction.
- **Next (D3/M2):** (i) write the affine depth-form `Φ_n(e)` explicitly; (ii) attempt a 2nd-moment / large-
  sieve bound on `Σ_n e(t·Φ_n)` exploiting the linearity (where the nonlinear large sieve died on self-
  clustering, the *linear* form may separate); (iii) target any unconditional `even-density ≥ ε` partial.

## 2026-06-24 (cont.) — D3 dive-in: linear-form sum evaluated; controls off-diagonal, diagonal still open
Evaluated the linear-form exponential sum `Σ_n e(t·S_n/2^M)` (`D3_linearsum.py`, `D3_position.py`):
- **Fixed-modulus cancellation is REAL and UNCONDITIONAL** [verified]: `|Σ e(t S_n/2^M)|/√N ≈ 0.01–0.12`
  (sub-√N). Reason: for `n ≥ M`, `S_n ≡ 3^{n−M}S_M (mod 2^M)` — the `×3`-isometry coset; the character sum
  over the coset is small (Gauss/Ramanujan-type), provably.
- **But it controls the WRONG position** [7th over-claim AVOIDED by checking]: this cancellation is at the
  **low bits** of `S_n` (`×3`-isometry, *off-diagonal*) — the part already known fine. The even-density /
  depth need the bit at the **moving/middle position** (`parity e_n = bit_n(8·3^n−S_n)`; `c_n mod 2^k` =
  bits `[n,n+k]`), i.e. the **diagonal**. The lowest set bit of `S_n` sits at position ~3 (bounded); the
  depth-relevant bit at position ~`n` (grows). The linear structure controls the low end, not the middle.
  **Same opposite-ends wall. NOT a crack.**
- **D3 is NOT dead (unlike D2).** The linear structure is a genuine handle and the remaining target is **sharp
  and genuinely linear**, unlike the general nonlinear equidistribution: *bound the MOVING-modulus linear
  exponential sum `Σ_n e(t·Φ_n(e))` with the explicit `2^j 3^{n−1−j}` coefficients, where the modulus
  `2^{n+L}` grows with `n`.* Fixed-modulus is solved (character sum); the moving-modulus linear sum is the
  open core — but it is a LINEAR object, a different (and arguably more approachable) target than Mahler's
  nonlinear wall.
- **Status:** D3 mapped; off-diagonal part unconditionally controlled; the sharp open sub-problem isolated
  (moving-modulus linear exp-sum). No unconditional even-density bound yet; no over-claim. D3 remains the
  most promising live in-house direction.
- **Next (D3):** attack the moving-modulus linear sum directly — (i) van der Corput on the LINEAR phase
  (differencing a linear form may NOT be closed the way the multiplicative `(3/2)^n` was — worth checking);
  (ii) a large-sieve over the modulus family `{2^{n+L}}` exploiting linearity; (iii) connect to Stewart/Baker
  bounds on the digits of `3^n` (the coefficients are `3^{n−1−j}`).
