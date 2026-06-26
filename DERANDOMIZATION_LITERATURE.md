# Known derandomization principles — literature survey for the contraction/derandomization tool (2026-06-26)
*Three parallel literature agents (QUE/rigidity · single-orbit/Mahler · pseudorandomness/TCS). Question: is there a
known principle that derandomizes an a.e./Haar equidistribution (from a transfer-operator spectral gap) to a single
specified algebraic orbit of a rank-1 expanding map (`×3/2`), using effective irrationality of `log₂3`? Citations
verified where noted; unverifiable items flagged. 0 fabricated references.*

## Verdict (decisive): no known principle reaches our case
**Every** rigorous principle that removes "almost-every" and reaches a *specified* / *every* object requires
structure our **self-dual rank-1 amenable-hyperbolic** `×3/2` system lacks. Our derandomization step **is** Mahler's
3/2 problem, an explicitly open problem.

| principle | what it needs | why it cannot reach our orbit |
|---|---|---|
| **Quantum Unique Ergodicity** (Lindenstrauss *Annals* 2006, AQUE; Holowinsky–Soundararajan *Annals* 172, 2010) | a commuting **Hecke** algebra; gap alone gives only *quantum ergodicity* (a.e./density-1) | no Hecke / arithmetic symmetry on a bare cyclic map; no Hecke-recurrence analogue |
| **Measure rigidity** (Furstenberg ×2×3; Rudolph 1990/Johnson; Einsiedler–Katok–Lindenstrauss *Annals* 2006) | a **2nd multiplicatively-independent map** (rank ≥ 2); the entropy-coupling identity `log q·h(σ_p)=log p·h(σ_q)` is the *source* of rigidity | one map ⇒ **uncountable invariant-measure simplex**, no cross-direction entropy constraint (Lindenstrauss *JMD* 2008: rank-1 needs an extra recurrence from a second factor) |
| **Effective equidistribution** (effective Ratner SL(3,ℝ) *Annals* 2025, arXiv:2208.02525; Lindenstrauss–Mohammadi) | a **unipotent/polynomial** law (slow, polynomial divergence) | `×3/2` is expanding (exponential divergence) — the opposite regime; Ratner-type rigidity fails for diagonalizable/expanding |
| **Sarnak–Möbius disjointness** (Sarnak 2011; Tao arXiv:1605.04628) | **zero topological entropy** ("deterministic") | our orbit is **positive-entropy / full-complexity**; for positive entropy orthogonality *provably fails* (Karagulyan arXiv:1701.01968, 2017) |
| **Bourgain–Sarnak–Ziegler** (arXiv:1110.0992) | a **multiplicative** test + bilinear `p·n,q·n` de-correlation | wrong target (orthogonality-to-multiplicative, not equidistribution); our orbit is multiplicatively structureless (matches our own bilinear probe) |
| **Algorithmic randomness ⇒ normal** (Downey–Hirschfeldt) | **non-computability** (ML/computable/Schnorr-random) | our orbit is **computable**, `K=O(\log N)` — never ML-random; a computable martingale predicts it. **Normality is the right strictly-weaker target — but must be proven directly** |
| **PRG / derandomization (TCS)** (Nisan–Wigderson 1994; Impagliazzo–Wigderson 1997) | bounded test class; usually **conditional** (circuit lower bounds), gives **computational** indistinguishability | class-relative + computational, not unconditional/statistical; arithmetic tests lie outside the fooled class |
| **Weyl / Gowers norms** (Weyl 1916; Green–Tao–Ziegler *Annals* 176, 2012, arXiv:1009.3998; Gowers–Wolf *PLMS* 2010) | a **direct** bound on the exponential / `U^k` sums | the **right framing** but a *reduction, not a deduction* — for `(3/2)^n` the needed cancellation **is** Mahler 3/2, open |

## The closest result to "single specified seed", and the exact gap
- **Flatto–Lagarias–Pollington (1995, *Acta Arith.* 70(2):125–147):** for **every** specified `ξ` (single seed,
  unconditional), `limsup_n {ξ(p/q)^n} − liminf_n {ξ(p/q)^n} ≥ 1/p` (`=1/3` for `3/2`). This is the **only**
  nontrivial fact provably true of our exact orbit — and it is a **range** statement, infinitely far from density
  or equidistribution. **This independently validates our 2-adic-FLP analog** (`VALUATION_BUDGET.md`: the
  unconditional range `n ≤ Σ_{odd}v2 ≤ 1.585n` — same flavour: range, not density.)
- **Tao (2019, arXiv:1909.03562, *Forum Math Pi*):** controls the **same** 3-adic skew-random-walk characteristic
  function we reconstructed, but at **logarithmic-density-1 over seeds** — never one seed. Exact gap = the
  density-average / a.e.→specified descent. (Confirms our "closest known = Tao 2019" claim, with the precise
  quantifier.)
- **arXiv:2510.11723 (2025), rational-base normality conjecture:** poses **single-orbit normality** as an explicit
  **open conjecture**, naming Mahler 3/2 / Flatto Z-numbers / Dubickas–Mossinghoff 4/3 as consequences. *(Author
  attribution unverified — inferred from PDF metadata; existence/content of the conjecture confirmed by two
  fetches.)* So our "central conjecture" is the literature's recognized open frontier.

## What the literature confirms about our blueprint
1. **Our derandomization framing is exactly right and exactly open.** "a.e. (spectral-gap CLT) → specified orbit"
   is the unbridged gap everywhere; no transfer-operator argument promotes it to the algebraic orbit (= Mahler).
2. **The cleanest "why rank-1 fails" is the entropy-coupling identity** — rigidity *needs* a second
   multiplicatively-independent map; one map's invariant measures are an uncountable simplex. This sharpens our
   "amenable ∩ hyperbolic / self-dual ×3/2" wall with the precise rigidity-theory reason.
3. **The right language is Weyl/Gowers — a reduction to a cancellation bound** — which is *exactly* our
   character-sum reduction and **Theorem E** (`avgD_odd ≥ 3/2` ⟸ low-moduli power-saving character cancellation).
   The literature agrees this is the correct certificate to supply directly, not derive for free.
4. **Provable normality always uses a bespoke designed certificate** (Champernowne 1933; Copeland–Erdős 1946;
   Stoneham/Bailey–Crandall; Korobov) — never a general "pseudorandom ⇒ normal" transfer. This **confirms
   `NEW_ENGINE`**: a *given* arithmetic orbit carries no certificate, only its generating dynamics.

## Honest conclusion
There is **no known derandomization principle** that supplies what we need. The genuine precedents for "gap ⇒ every
orbit" (QUE, rigidity, effective Ratner) all draw on higher-rank/arithmetic/unipotent structure absent from a
self-dual rank-1 expanding map; the pseudorandomness routes (Sarnak/BSZ/ML-random/PRG) each fail for a precise
stated reason (entropy / multiplicativity / computability / class-relativity). The **one correct framing
(Weyl/Gowers) is a reduction to the open Mahler cancellation** — which is exactly where our Theorem E lands. So the
multi-year tool is genuinely new mathematics, the literature confirms its necessity and its precise shape, and the
closest unconditional fact about our specific orbit is the FLP-type **range** bound we had already reproduced
2-adically. **The map is now grounded in the literature; the central conjecture is the recognized open frontier.**

### Citation status
*Verified:* Lindenstrauss *Annals* 2006; Holowinsky–Soundararajan *Annals* 172 (2010) 1517–1528; Rudolph/Johnson;
EKL *Annals* 2006; Lindenstrauss *JMD* 2008; effective Ratner *Annals* 2025 (arXiv:2208.02525); FLP *Acta Arith.*
70(2) (1995); Tao arXiv:1909.03562; Koksma 1935 (classical); Sarnak Möbius (IAS 2011) + Tao arXiv:1605.04628;
Karagulyan arXiv:1701.01968; BSZ arXiv:1110.0992; Green–Tao–Ziegler *Annals* 176 (2012), arXiv:1009.3998;
Gowers–Wolf *PLMS* 2010, arXiv:0711.0185; Nisan–Wigderson JCSS 1994; Impagliazzo–Wigderson STOC 1997.
*Unverified / flagged:* arXiv:2510.11723 author attribution; exact pages of Lindenstrauss 2006 / EKL 2006;
Champernowne/Copeland–Erdős full texts (metadata only); Downarowicz–Serafin positive-entropy-yet-disjoint example.
No arXiv IDs fabricated.
