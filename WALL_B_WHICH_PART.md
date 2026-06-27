# Wall (B): which PART of the parity carries it? — a_n = bit_n(8·3ⁿ) vs b_n = bit_n(Tₙ)

Attack of 2026-06-28. Target: wall (B) only (named-orbit selection), via the angle
"which half of the Antihydra parity carries it?" The parity is
`r_n = a_n XOR b_n` with

- `a_n = bit_n(8·3ⁿ)` — **fully explicit, deterministic, NON-self-generated**. The middle digit
  (position n of ~1.585 n) of `8·3ⁿ`. Equivalently `a_n = floor(8·(3/2)ⁿ) mod 2`.
- `b_n = bit_n(Tₙ)` — the **self-generated carry**, `T_{n+1}=3Tₙ+2ⁿrₙ`, closed loop `r=a XOR b`.

Script: `wall_b_which_part.py` (exact big-int arithmetic, `.venv`). **Zero false proofs.**

---

## [PROVEN, exact] Soundness cross-check — the decomposition is the real orbit
The closed-loop identity sequence `r_n` equals the **real Hydra orbit parity** `h_n mod 2`
(`h₀=8, h_{k+1}=⌊3h/2⌋`) at offset 0 with **agreement = 1.0000** over N=60000
(any other offset → 0.498 ≈ chance). So `a_n`/`b_n` is a faithful decomposition of the actual
Antihydra parity, not a model. First 24 bits identical:
`r = 000100010101110001101010 = h&1`.

---

## [PROVEN, exact] a_n ALONE is the specific-point (3/2)ⁿ equidistribution (= Mahler-for-a-point)
By exact integer arithmetic (0 mismatches over n<20000):
> `a_n = 0  ⟺  {4·(3/2)ⁿ} ∈ [0, ½)`,  where `{4·(3/2)ⁿ} = (8·3ⁿ mod 2^{n+1})/2^{n+1}`.

Therefore the balance `(1/N)Σ(−1)^{a_n} → 0` is **literally** the statement that the
**specific named point** `{4·(3/2)ⁿ} = {3ⁿ/2^{n−2}}` has half-interval frequency ½. That is the
classical **powers-of-3/2 mod 1 problem (Mahler)** for a specific computable point — it is not even
known that `{(3/2)ⁿ}` is *dense* mod 1, let alone equidistributed. **[OPEN]**, same class as the
kernel `(K)` of `PROOF_STATUS.md`.

**Explicitness does NOT make a_n tractable.** `8·3ⁿ` being explicit only gives its *leading* bits
(governed by `{n·log₂3}`, effectively equidistributed by Weyl). But `a_n` is the **middle digit**
`bit_n` (position n of ~1.585 n), governed by `{4·(3/2)ⁿ}` = the open (3/2)ⁿ object. This is exactly
the gap flagged in `PROOF_STATUS.md` §3.6 ("the parity uses the middle digit, not the leading bits"),
here pinned to an exact integer equivalence.

### Verdict on point 2 (refined, the bankable structural result)
**The specific-point (3/2)ⁿ equidistribution = the essence of wall (B) is ALREADY fully present in
the explicit, NON-self-referential half a_n.** It does **not** require the self-generated orbit at
all. `a_n` is a pure deterministic powers-of-3/2 sequence with **no feedback, no ensemble** — the
cleanest possible incarnation of a named-point (3/2)ⁿ equidistribution.

This **refines** the (A)/(B) split of `SESSION_2026-06-28_TWISTED_RPF.md`: wall (B) was framed as
"named-*orbit* selection" (selecting the self-generated c₀=8). The finding here is sharper —
**named-point (3/2)ⁿ equidistribution is not about self-reference**; it is incarnate in `a_n`, which
has no self-reference. The self-generation lives entirely in `b_n` and is a *separate, decorrelated*
layer (it is wall (A)'s quenched/closed-loop aspect), **not** the source of wall (B).

---

## [OBSERVED] a_n and b_n are decorrelated — NO conspiracy, but a softer requirement appears
Numerics (N=60000):

| quantity | value |
|---|---|
| mean a_n | 0.49925 |
| mean b_n | 0.49970 |
| **Pearson(a_n,b_n)** | **−0.00143** (≈ 0 within 1/√N ≈ 0.004) |
| `A_r = E[(−1)^a(−1)^b]` | −0.00143 |
| `A_a·A_b` (if independent) | +0.00000 |

`a_n` and `b_n` are **essentially independent / cross-decorrelated** (matches `PROOF_STATUS.md` §3.2:
"the two Mahler digits are cross-decorrelated"). There is **no anti-correlation conspiracy** where
neither is balanced but the XOR is — the XOR is balanced because the two pieces are uncorrelated.

### Verdict on point 3 (the consequential subtlety)
Halting depends **only** on the partial sums of `r_n`; `a_n`/`b_n` is an artificial split. So the
proof needs only `A_r → 0`, and
> `A_r = (1/N)Σ(−1)^{a_n}(−1)^{b_n}` → 0  **⟺  the two sign sequences are asymptotically ORTHOGONAL**.

Orthogonality is **weaker than, and different from, "each balanced."** In particular, *if* `a_n ⊥ b_n`
(decorrelated, as observed) and `b_n` is balanced, then `A_r → 0` **without `a_n` needing to be
balanced at all.** So **a_n's specific-point Mahler is NOT strictly on the critical path for the XOR**:
the complete proof could in principle route entirely through `b_n` (= wall (A), the carry-balance /
Mauduit–Rivat object for the closed loop) **plus the decorrelation `a_n ⊥ b_n`**, never touching the
explicit (3/2)ⁿ point.

**Honest caveat [CONDITIONAL/OPEN].** This is a *re-routing of the requirement*, not an easing of it.
Proving `a_n ⊥ b_n` (decorrelation of the explicit (3/2)ⁿ middle digit from the self-generated carry
digit) is itself a correlation statement spanning both (3/2)ⁿ structures, and the `coupling_brick`
result (parity decorrelated from *every provable* surrogate) suggests it is comparably hard. So the
binding object is **not** "a_n balanced" and **not** "b_n balanced" in isolation, but the
**joint orthogonality of the explicit digit and the self-generated carry digit** — a statement that
genuinely couples wall (A) and wall (B) rather than localizing on either.

---

## [OBSERVED] Balance + rates (N up to 60000)

| M | A_a (explicit) | A_b (carry) | A_r (parity) |
|---|---|---|---|
| 1000 | 0.03000 | −0.03200 | −0.00200 |
| 10000 | −0.00980 | −0.00220 | −0.00920 |
| 30000 | −0.00213 | −0.00713 | −0.00033 |
| 60000 | 0.00150 | 0.00060 | −0.00143 |

log-log decay exponents `A(M) ~ M^slope` (−0.5 = √-cancellation):
`a_n: −0.399`, `b_n: −0.479`, `r_n: −0.397`.

All three decay near the √-cancellation rate. `b_n` (carry) is closest to clean −0.5 (consistent with
the annealed Mauduit–Rivat carry lemma); `a_n` and `r_n` track each other (−0.40), consistent with
`a_n` being the slower / harder explicit (3/2)ⁿ digit.

---

## Returned conclusions (the three asks)
1. **Is wall (B) already in the explicit part a_n?** **YES, exactly.** `a_n = bit_n(8·3ⁿ)` balance
   `⟺ {4·(3/2)ⁿ}` half-interval frequency ½ (proven by exact integer identity, 0 mismatches). This is
   the named-point powers-of-3/2 mod 1 problem (Mahler), **OPEN**, present with **no self-reference**.
   Explicitness gives only the leading bits (`{n log₂3}`), not the middle `bit_n`. So the
   non-self-referential half already inherits an open specific-point (3/2)ⁿ equidistribution.
2. **Could a_n/b_n conspire so only the XOR needs balance?** **No conspiracy is observed** (Pearson
   ≈ 0, not anti-correlation). But a related, real structural fact holds: the proof needs only
   `A_r→0 ⟺ a_n ⊥ b_n` (asymptotic orthogonality), which is **weaker than each-balanced** and could be
   satisfied via `b_n` balance + decorrelation **without** balancing the explicit `a_n`. So a_n's
   specific-point Mahler is dodgeable in principle — the truly binding object is the
   **joint a_n⊥b_n decorrelation** (couples walls A and B). [CONDITIONAL — decorrelation is likely
   comparably hard; `coupling_brick` evidence.]
3. **Numerics:** see tables above. a_n balanced (slope −0.40), b_n balanced (slope −0.48), r_n
   balanced (slope −0.40); a_n and b_n **decorrelated** (Pearson −0.0014).
