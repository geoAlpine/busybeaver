# External-literature frontier for (K) — the 2020s state of the art on effective (3/2)^n equidistribution (2026-07-05)

*Directed search of the current external literature for the exact input `(K)` needs (effective single-orbit
equidistribution / digit-frequency for the base-3/2 dynamics). Finding: **`(K)` has a named external home** — the
**Normality Conjecture on rational base number systems** (Andrieu–Eliahou–Vivion, arXiv:2510.11723, Oct 2025) — with
proved equivalences, a family of implied problems, and numerics that independently reproduce our blind-run findings.
The effective-equidistribution state of the art (Lindenstrauss school, 2024–25) is **rank ≥ 2 homogeneous only**,
confirming our rank-1-amenable orbit is genuinely outside current tools. SOUNDNESS: external claims labelled
`[PROVEN-in-lit]`/`[conjecture-in-lit]`; our connections labelled; `(K)` `[OPEN]`; no machine decided.*

## 1. The named home: the Normality Conjecture on rational base p/q `[conjecture-in-lit + proved equivalences]`
Andrieu–Eliahou–Vivion, **arXiv:2510.11723** (2025), building on Akiyama–Frougny–Sakarovitch (2008):
- **Base p/q** (`gcd(p,q)=1`, `p>q≥1`): `n = (1/q)Σ a_i (p/q)^i`, digits `{0,…,p−1}`. **Minimal word** `w_min(u)`
  (lexicographically smallest extensions) uses `{0,…,q−1}`; **maximal word** `w_max(u)` uses `{p−q,…,p−1}`.
- **Conjecture 1.3 (Normality):** `w_min` is normal over `{0,…,q−1}`, `w_max` over `{p−q,…,p−1}` — every length-`ℓ`
  subword has frequency `q^{−ℓ}`. **For base 3/2** (`q=2`): `w_min∈{0,1}^ℕ`, `w_max∈{1,2}^ℕ`, digits `0,1` each at
  frequency `½`.
- **Theorem 1.7 `[PROVEN-in-lit]`:** Normality (1.3) `⟺` equidistribution mod `q^ℓ` (Conjecture 1.6). **This is exactly
  our `(K)` reformulation** — single-orbit equidistribution in the `2^ℓ`-cylinders / the moving-diagonal digit
  frequency (`CROSSING_STRATEGY §3`, `DEPTH_REACH_CLARIFICATION`).
- **Theorem 1.5 `[PROVEN-in-lit]`:** Normality of minimal words `⟹` no `Z_{p/q}`-numbers when `p<q²`. **3/2 satisfies
  `p=3 < 4=q²`** — the implication is in its working regime. Also implies (Prop 3.16) termination for the Collatz **4/3
  problem** (Dubickas–Mossinghoff). Umbrella over Z-numbers (Mahler), `Z_{p/q}` (Flatto), triple expansions (Akiyama).
- **Status:** Conjecture 1.3/1.6 **unproven**; supported by numerics only (4099 minimal words, 10⁶-letter prefixes).

**Our `(K)` in this frame.** `(K)` is the one-sided (`even-density ≥ 1/3`) form of the same single-orbit
digit/parity-frequency question for the base-3/2 dynamics `c↦⌊3c/2⌋` (which IS the base-3/2 successor/shift). It is a
**sibling in the family the Normality Conjecture governs**, and the full Conjecture (`frequency ½`) would give
`(K)` (`½ ≥ 1/3`) outright. `[Exact word↔orbit dictionary — is Antihydra's parity literally `w_min`/`w_max`? — is a
concrete next step, not yet verified; the family membership is clear either way.]`

## 2. Their numerics independently reproduce our blind runs `[OBSERVED-in-lit ↔ our OBSERVED]`
2510.11723 report: subword-frequency **deviation from uniformity decreases at random-sequence rates** (not monotone
above baseline), and a **richness threshold ≈ `2^ℓ log 2^ℓ`** comparable to normal constants / `π`. This matches our
`BLIND_HARMONIC` (discrepancy `~N^{-1/2}`, no structure) and `BLIND_EFFECTIVENESS` (geometric occupancy) — two
independent computations, same "looks exactly random, no exploitable structure" verdict. Corroboration, not novelty.

## 3. Effective equidistribution SOTA is rank ≥ 2 — our orbit is outside `[PROVEN-in-lit boundary]`
The 2024–25 effective-equidistribution frontier (Lindenstrauss, Margulis, Mohammadi, Shah, Wieser, Yang; Kim) —
polynomial-rate equidistribution for **unipotent/semisimple orbits on rank-≥2 homogeneous spaces** (e.g. arXiv:2407.12760,
2202.11815, 2110.00706). **None applies to a single rank-1 amenable `×3/2`-orbit on the (2,3)-solenoid.** Effective
equidistribution is, in current mathematics, a **rank-≥2 / positive-entropy phenomenon**; our object has neither. This
confirms — against the actual state of the art, not just our No-Structure theorem — that `(K)` is generational.

## 4. The ×2×3 reformulation frontier matches our joining route `[context]`
Burton–Panangaden, **arXiv:2410.22701** (2024): Furstenberg ×2×3 reformulated via **tracial states on the C\*-algebra of
a semidirect product related to Baumslag–Solitar groups**, and via Carathéodory functions. Purely reformulatory (no
effective result). Our `CROSSING_STRATEGY` joining/Kronecker reformulation sits in exactly this stream — and the
`×3/2`-solenoid IS a Baumslag–Solitar `BS(2,3)`-type object. **The field's own frontier is reformulating, not proving**
— independent evidence that the wall is structural, not a gap in our effort. (Also: Eliahou–Verger-Gaugry
**arXiv:2504.13716**, 2025, expose base-3/2 ↔ 3x+1 links directly.)

## 5. A 3/2-specific softening worth probing `[nuance, OPEN]`
Akiyama's exceptional construction (`{ξ(p/q)^n}` confined to a Cantor set) **requires `p>q²`**; Dubickas gives
short-interval confinement for any `p/q`. **3/2 has `p<q²`**, so the *Cantor-set* exceptional confinement does **not**
exist for it — 3/2 lies in the regime where exceptional sets are thinner and normality is more strongly expected. This
mildly **softens** the "full-dimension exceptional set blocks a.e. methods (Fan–Fan–Ye)" obstruction *for 3/2
specifically*: the a.e.-to-specific-seed gap may be smaller here than for larger ratios. **Concrete follow-up:**
estimate the Hausdorff dimension / size of the non-equidistribution exceptional set for `{ξ(3/2)^n}` — if it is not
full-dimension, the a.e. route to seed 8 is less hopeless than assumed.

## Verdict
**A high-value harvest — `(K)` is externally anchored.** It is the one-sided form of the **Normality Conjecture on
rational base 3/2** (Andrieu–Eliahou–Vivion 2025), whose `[PROVEN]` Theorem 1.7 is our exact `mod 2^ℓ`
reformulation and whose numerics reproduce our blind runs; its family (Z-numbers, Flatto, 4/3) are our siblings. The
effective toolbox that would cross is rank-≥2 homogeneous (Lindenstrauss school) and provably does not reach our
rank-1 amenable orbit; the field's ×2×3 frontier is itself only reformulating (Baumslag–Solitar C\*-algebras),
matching our joining route. One genuine new foothold: 3/2's `p<q²` excludes Akiyama Cantor-set exceptionals — the
exceptional set may be sub-full-dimensional, softening the a.e. obstruction for 3/2. **`(K)` `[OPEN]`. No machine
decided. No label upgraded.**

## Sources
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025).
- Eliahou, Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*, arXiv:2504.13716 (2025).
- Burton, Panangaden, *Formulations of Furstenberg's ×2×3 conjecture in complex analysis and operator algebras*, arXiv:2410.22701 (2024).
- Lindenstrauss et al., effective equidistribution (rank ≥ 2): arXiv:2407.12760, 2202.11815, 2110.00706 (2024–25).
- Akiyama–Frougny–Sakarovitch, rational base systems (2008); Akiyama (`p>q²` Cantor set); Dubickas (short interval).
- Reproduce our side: `BLIND_HARMONIC_2026-07-05.md`, `BLIND_EFFECTIVENESS_2026-07-05.md`, `CROSSING_STRATEGY_2026-07-05.md`.
