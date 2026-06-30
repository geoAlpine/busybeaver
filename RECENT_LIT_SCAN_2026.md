# RECENT LITERATURE SCAN — BB(6)/Antihydra program (scan date: 2026-06-30)

Scope: hunt for anything GENUINELY NEW or MISSED (2023–2026) that is a *usable weapon* against
the kernel **(K)** = single specified 2-adic Bernoulli orbit (o₀=27, c→⌊3c/2⌋) has liminf depth-mean ≥ 3/2
= single-orbit base-3/2 normality = Mahler 3/2 = **AEV Conjecture 1.6**.
Ethos: ZERO false proofs. Every citation labeled [VERIFIED] (abstract fetched directly) /
[UNVERIFIED] (search-snippet only, not independently fetched). (K) is NOT solved.

---

## §0 — VERDICT

**NO genuinely new, usable weapon.** Every 2023–2026 hit lands on exactly the same two walls the
program already mapped: (a) **a.e.-vs-specified** (results hold for almost-every point / almost-every
point in support, never for one named orbit), and (b) **rank-2 / non-amenable / unipotent hypotheses**
(every effective-equidistribution and measure-rigidity advance requires a structure our rank-1 amenable
hyperbolic A=×(3/2) single orbit provably lacks). The central conjecture (AEV / Mahler 3/2) was *revised
April 2026* but remains **purely conjectural with numerical evidence — zero unconditional partial density
bound, no one-sided result, no specific-orbit result**. Antihydra is **still an open Cryptid**; no partial
bound, no conditional theorem, no reduction beyond the known Collatz-like / Mahler-3/2 reduction the
program already owns. **One genuinely-new VERIFIED citation worth banking** (context, not a weapon):
the formal determination of BB(5) (arXiv:2509.12337) — establishes that BB(6) is now the live frontier
and is gated precisely on Antihydra.

Net change to the frontier state: **none**. Confirms "empty toolbox" through current literature.

---

## §1 — EFFECTIVE EQUIDISTRIBUTION / RIGIDITY, very recent (2023–2026)

The wave of effective-equidistribution / effective-rigidity work continues, but every advance keeps the
disqualifying hypotheses. Ruthless rank / amenability / a.e. audit:

- **Simion Filip, "Measure Rigidity beyond Homogeneous Dynamics," arXiv:2512.13865 (15 Dec 2025) [VERIFIED].**
  Extends measure & topological rigidity from Lie-homogeneous settings to general manifolds. Direct fetch
  of the PDF confirms it still requires **higher rank or non-amenable / smooth hyperbolic manifold
  structure**, positive entropy, and concerns orbit-closure / global behavior — NOT single-orbit. Explicitly
  does **not** cover a rank-1 amenable abelian action on a solenoid for one specified orbit.
  → DISQUALIFIED (rank, amenability, a.e. vs specified). Newest, most "beyond-homogeneous" item; still walls out.

- **Lindenstrauss–Mohammadi–Wang–Yang, "Effective equidistribution in rank 2 homogeneous spaces and
  values of quadratic forms" (2025) [UNVERIFIED — search snippet only].** Rank 2 by title.
  → DISQUALIFIED (rank ≥ 2; A is rank 1).

- **Einsiedler–Lindenstrauss–Mohammadi–Wieser, "Effective equidistribution of semisimple adelic periods…"
  (2025) [UNVERIFIED].** Semisimple group + period orbits.
  → DISQUALIFIED (semisimple / non-amenable; periods, not a single endomorphism orbit).

- **"Polynomially effective equidistribution for unipotent orbits in products of SL₂ factors,"
  arXiv:2601.09983 (Jan 2026) [UNVERIFIED]; Lindenstrauss–Mohammadi–Wang (effective unipotent, polynomial
  rate, arXiv:2202.11815) [UNVERIFIED]; "An effective closing lemma for unipotent flows" (Lindenstrauss–
  Margulis–Mohammadi–Shah–Wieser, 2024) [UNVERIFIED].**
  → DISQUALIFIED (unipotent + non-abelian; A is abelian/hyperbolic, no unipotent direction). Matches the
  program's existing "effective Ratner needs unipotent" assessment.

- **"Rigidity of non-maximal torus actions, unipotent quantitative recurrence, and Diophantine
  approximations," arXiv:2307.04163 (2023) [UNVERIFIED]; survey "Recent progress on rigidity of higher rank
  diagonalizable actions," arXiv:2101.11114 [UNVERIFIED].** Higher-rank diagonalizable + positive-entropy
  measure classification.
  → DISQUALIFIED (rank ≥ 2; positive entropy is an *input* there, but it is (K)-hard for us — exactly the
  ENT gap the program already isolated).

- **Han Yu, "Times two, three, five orbits on T²," arXiv:2009.00441 [UNVERIFIED]; "Times two, three orbits"
  family.** Density (topological), and crucially a **rank ≥ 2 semigroup** (×2,×3,×5 jointly).
  → DISQUALIFIED (rank ≥ 2; topological density, not Cesàro frequency / one-sided liminf).

**§1 verdict:** the entire 2023–2026 effective-equidistribution / rigidity frontier is rank-2, unipotent,
semisimple, or positive-entropy-as-hypothesis. None populates the {amenable ∩ hyperbolic ∩ rank-1 ∩ single
specified orbit} cell. This *re-confirms* the program's Coverage No-Go (RANK1_AMENABLE_EQUIDISTRIBUTION.md)
through the newest literature. No transfer.

---

## §2 — ANTIHYDRA / BB(6) CRYPTID community status

**Antihydra is STILL OPEN; no partial proof exists.** Sources (bbchallenge.org/antihydra,
wiki.bbchallenge.org/wiki/Antihydra, fetched directly):

- **No proof, and "even *attempts* at a proof have been elusive"** (bbchallenge.org/antihydra [VERIFIED fetch]).
  Described as "the smallest open problem in mathematics, on the Busy Beaver scale."
- **Iteration / reduction (matches our kernel):** core map H(n)=⌊3n/2⌋; halting ⟺ the orbit ever produces
  more odd than 2× even values; explicitly tied by the wiki to **Mahler's Z-number / equidistribution of
  {ξ·(3/2)ⁿ}** — i.e. the community's own framing is identical to (K). No sharper reduction than the program
  already holds.
- **Probabilistic heuristic [HEURISTIC, not a proof]:** halting probability estimated ≈ (5−√2)^237 ≈
  2.884×10⁻²⁸⁷²³⁰⁴²⁵⁶⁵; random-walk steps +2/−1 with equal probability. Strongly suggests non-halting; proves nothing.
- **Simulation (May 2026):** simulated to 2³⁸ rule steps, parameter a > 2³⁷; memory is the bottleneck
  (per wiki TMBR Aug 2025). No counterexample, no bound.
- **Formalization:** Lean repositories formalize the *recurrence-equivalence* (that the TM's halting is
  equivalent to the Collatz-like predicate) — this is a **reduction certificate, NOT** a proof of (non-)halting.
- A dozen+ other 6-state Cryptids remain; BB(6) is unresolved.

**BB(5) is now DONE (genuinely new, relevant context):**
- **The bbchallenge Collaboration et al., "Determination of the fifth Busy Beaver value," arXiv:2509.12337
  (submitted 15 Sep 2025; revised 23 Mar 2026) [VERIFIED fetch].** S(5)=47,176,870, Coq-verified; first new
  Busy Beaver value in 40+ years. Abstract does **not** mention BB(6)/Antihydra/Cryptids — but it cements
  that **the live frontier is now BB(6), gated on Antihydra**.

**§2 verdict:** community status = open Cryptid, no partial bound / conditional result / new reduction
beyond Mahler-3/2. Nothing here the program does not already have; the only new artifact is the BB(5) paper.

---

## §3 — MAHLER 3/2 / Z-NUMBER / base-3/2 normality (2023–2026)

- **Andrieu–Eliahou–Vivion, "A Normality Conjecture on Rational Base Number Systems," arXiv:2510.11723
  (6 Oct 2025; revised 7 Apr 2026) [VERIFIED fetch].** This is the program's (K)=Conj-1.6 source. Direct
  fetch confirms: **entirely conjectural, supported only by extensive numerical experiments** (richness
  thresholds, deviation from normality). **No unconditional proof, no partial density bound, no one-sided
  result, no specific-orbit/seed result.** Conjecture: every minimal/maximal word is normal over an
  appropriate subalphabet; would imply Z-numbers (Mahler 1968), Z_{p/q} (Flatto 1992), triple expansions
  (Akiyama 2008), the 4/3 problem (Dubickas–Mossinghoff 2009). NEW only in that the revision date moved to
  Apr 2026 — content still conjectural. **No moving-digit / one-sided-density advance for any specific orbit.**

- **Eliahou–Verger-Gaugry, "The number system in rational base 3/2 and the 3x+1 problem," arXiv:2504.13716
  (18 Apr 2025) [VERIFIED fetch].** Confirms the base-3/2 ↔ Collatz bridge (already banked). Explicitly
  *motivational* — "expose these links and motivate further research," **no definitive proofs**.

- **"Mahler's 3/2 problem in ℤ⁺," arXiv:2411.03468 [UNVERIFIED — listed, not re-fetched this scan].**
  Already in the program's awareness (2024). No new partial beyond it surfaced.

**§3 verdict:** no partial result beyond AEV 2025. The single named conjecture equal to (K) remains a
conjecture with numerics only. No one-sided density / moving-digit statement for a specific orbit exists in
the literature.

---

## §4 — WILDCARDS (transferable weapons?)

Skeptical sweep of adjacent areas:

- **Effective ×2,×3 / Furstenberg quantitative density (2023–2026):** quantitative strengthenings of the
  ×2,×3 *topological* theorem exist and Varjú is active in the circle, but all are (i) density/topological,
  not Cesàro frequency, and (ii) rank-2 (joint ×2,×3). Furstenberg's *measure* conjecture remains open.
  → No transfer (rank-2; density ≠ one-sided liminf frequency). Matches prior "needs rank ≥ 2."

- **Normality of specific computable reals / single-orbit Weyl sums:** no 2024–2026 breakthrough surfaced.
  Searches returned only pre-2022 normal-number work and noise. → Nothing.

- **Collatz-adjacent arXiv 2025–2026 ("one-bit orbit mixing," "phantom universality," "sprint lock ρ≤1/3,"
  structural reductions): all [UNVERIFIED] and bearing strong markers of crank / LLM-assisted non-refereed
  preprints (arXiv:2603.25753, 2603.11066, etc.).** → DO NOT BANK; not credible weapons. Flagged only to
  record they were seen and rejected.

- **Random-walk / stationary-measure effective density (Eskin–Lindenstrauss / Benoist–Quint style),
  "Effective Density of Non-Degenerate Random Walks…" (arXiv:2303.09499) [UNVERIFIED]:** needs genuine
  randomness / non-degenerate measure on a non-amenable group. Our orbit is deterministic + amenable.
  → DISQUALIFIED (already assessed: stationary-measure rigidity needs randomness the orbit lacks).

**§4 verdict:** no transferable weapon. The only credible recent items reduce to the same a.e./rank-2 walls;
the rest is non-credible.

---

## §5 — NET + citations to bank

**Net:** the literature scan finds **no crack**. Every 2023–2026 advance respects the a.e.-vs-specified and
rank-2/non-amenable/unipotent walls the program proved are binding. The empty-toolbox assessment is
re-confirmed against current (through June 2026) literature. (K) remains OPEN; AEV/Mahler-3/2 remains a
conjecture with numerics only; Antihydra remains an open Cryptid.

**Verified citations to bank / refresh (all [VERIFIED] by direct abstract fetch this scan):**

| arXiv id | Authors / title | Date | Use |
|---|---|---|---|
| 2510.11723 | Andrieu–Eliahou–Vivion, *A Normality Conjecture on Rational Base Number Systems* | 6 Oct 2025, rev. 7 Apr 2026 | (K)=Conj 1.6 source; **conjectural only** — refresh revision date |
| 2504.13716 | Eliahou–Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem* | 18 Apr 2025 | base-3/2↔Collatz bridge (motivational, no proofs) |
| 2509.12337 | bbchallenge Collaboration et al., *Determination of the fifth Busy Beaver value* | 15 Sep 2025, rev. 23 Mar 2026 | **NEW** context: S(5)=47,176,870 Coq-verified; BB(6) is now the frontier, gated on Antihydra |
| 2512.13865 | Simion Filip, *Measure Rigidity beyond Homogeneous Dynamics* | 15 Dec 2025 | newest rigidity frontier; **DISQUALIFIED** (rank/amenability) — bank as a checked no-transfer |

**Flagged [UNVERIFIED]** (search-snippet only; verify id before any citation): 2601.09983, 2202.11815,
2307.04163, 2101.11114, 2009.00441, 2303.09499, 2411.03468, and the two 2025 Lindenstrauss-circle effective
papers (rank-2 quadratic forms; semisimple adelic periods).

**Do NOT commit.** (Per task instruction.)
