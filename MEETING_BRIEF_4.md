# Meeting brief — round 4 (2026-07-05): (K) is now externally anchored to a NAMED 2025 conjecture

*For a strategy session / outreach. Rounds 1–3 validated the formulation (Mahler-class, rank-1 amenable hyperbolic,
obstruction = specified-orbit genericity). **New since then, and the reason for this brief:** `(K)` is no longer an
isolated oddity — it is the **one-sided form of a named, actively-studied 2025 conjecture** (the Normality Conjecture
on rational base number systems, Eliahou et al.), with a proved equivalence that is *exactly* our reformulation, a
verified digit-frequency dictionary, and a sharpened crossing map. All machine-checked or literature-anchored; 0 false
proofs (one 2026-07-05 foothold red-teamed and retracted). This is the outreach-actionable state.*

## 1. One-line state (updated)
Antihydra non-halt ⟺ `(K)`: the single `×(3/2)`-orbit of seed 8 has base-3/2 digit-`0` frequency `≥ 1/3` ⟺ the
**one-sided form of the Normality Conjecture on rational base 3/2** (Andrieu–Eliahou–Vivion, arXiv:2510.11723, 2025).
The full conjecture (frequency `= ½`) implies `(K)` (`½ ≥ ⅓`). Still a rank-1 amenable-hyperbolic single-orbit
equidistribution = Mahler 3/2 — unbroken — but now with an external home and a research group.

## 2. The external anchor (NEW, the headline) `[literature, proved parts verified]`
**arXiv:2510.11723**, base `p/q` (Akiyama–Frougny–Sakarovitch 2008): minimal/maximal words over `{0..q−1}`/`{p−q..p−1}`.
- **Thm 1.7 `[PROVEN in lit]`:** normality ⟺ equidistribution mod `q^ℓ`. **This is verbatim our `(K)` reformulation**
  (single-orbit equidistribution in `2^ℓ`-cylinders / moving-diagonal digit frequency). Independent confirmation the
  framing is the accepted one.
- **Thm 1.5 `[PROVEN in lit]`:** normality ⟹ no `Z_{p/q}`-numbers when `p<q²`; **3/2 has `p=3<4=q²`** (working regime);
  also ⟹ Collatz **4/3** termination. Family umbrella: Z-numbers (Mahler), Flatto, triple expansions, 4/3.
- **Their numerics reproduce ours** (deviation-from-uniformity at random rates, richness `≈2^ℓ log2^ℓ`) — matching our
  three "structureless-face" axes (§4). Conjecture itself **unproven** (numerics only).
- Companion: Eliahou–Verger-Gaugry, arXiv:2504.13716 (base-3/2 ↔ 3x+1).
> **Outreach implication:** `(K)` is a concrete sibling of an active conjecture with named authors. A crossing for
> `(K)` and for their Conjecture 1.3 need the same missing input; collaboration is the natural proof path.

## 3. The verified dictionary (NEW) `[OBSERVED exact + PROVEN]`
The base-3/2 last-digit `a₀=2c mod 3` read along the orbit `c↦⌊3c/2⌋`, `c₀=8`, has freq `0:0.4991, 1:0.0000,
2:0.5009`. **Digit `1` is arithmetically forbidden** (`⌊3c/2⌋ ≡ 0 mod 3` if `c` even, `≡1` if odd, never `≡2`), so the
orbit word lives on alphabet `{0,2}`, and **digit-`0` frequency `=` the `(K)` even-density exactly.** So `(K)` is
*literally* a base-3/2 digit-frequency statement — a Normality-Conjecture **sibling** (its `{0,2}`-word is a distinct
distinguished sequence, not the min/max word).

## 4. The crossing map, sharpened (NEW) `[reformulation + blind-tested]`
- **Joining/renormalization reformulation.** The two factors of the `(2,3)`-solenoid are the **2-adic odometer**
  (Kronecker, deterministic countdown) and the **archimedean** `{θ(3/2)ⁿ}` (equidistribution). Joining over the
  Kronecker factor ⟹ crossing ⟺ equidistribution of `{θ(3/2)ⁿ}` along dyadic progressions `n≡r mod 2^j` = the same
  Mahler problem with ratio `(3/2)^{2^j}`. **The duality is a renormalization** (2-adic determinism = time-doubling
  self-similarity).
- **Blind test:** dyadic-subsample discrepancy is flat `~1×` random across `j=0..4` ⟹ the joining is **product-benign**
  (no multi-scale obstruction) and self-similar (no contraction). **So the crossing reduces to a *single* archimedean
  effective-equidistribution input** — the solenoid/rank-1 coupling is a red herring.
- **The obstruction, one line:** that single input needs an **exponential** moving-diagonal rate (`2^{-Θ(n)}`, depth
  `Θ(n)`), while any discrepancy statement gives only **polynomial** (`N^{-1/2}`, capped at depth `log₂N` by the
  information-theoretic counting ceiling). **The needed rate sits below the counting horizon** — this is the rank-1
  amenable / Furstenberg-×2×3 wall in one sentence.

## 5. The "structureless face" confirmed on 3 independent axes (NEW) `[OBSERVED]`
Blind runs (predictions stated first, all confirmed): **harmonic** (Weyl `~√N`, discrepancy `~N^{-1/2}`, correlations
at noise floor), **occupancy** (exact countdown renewal; all content in one up-jump law = `(K)`), **symbolic
complexity** (the parity word is a **full 2-shift**, `p(ℓ)=2^ℓ`, complete de Bruijn graph, non-sofic). The `(K)` word
is a deterministic single orbit yet full-entropy — nothing for a structure-based proof to grip.

## 6. SOTA boundary — why current tools do not reach it `[literature boundary]`
Effective equidistribution is, in 2024–25, a **rank-≥2 / semisimple / unipotent** phenomenon (Lindenstrauss school:
arXiv:2407.12760, 2202.11815, 2110.00706). **None applies to a single rank-1 amenable `×3/2`-orbit.** The field's own
×2×3 frontier (Burton–Panangaden, arXiv:2410.22701) is **reformulating**, not proving — via Baumslag–Solitar
C\*-algebra tracial states (the `×3/2`-solenoid is a `BS(2,3)`-type object), exactly our joining stream. The literature
frontier for effective single-specified-orbit equidistribution of a rank-1 amenable hyperbolic action is **empty**.

## 7. What a crossing needs (the ask) `[P1′]`
An **effective single-orbit equidistribution** for `×(3/2)` on the `(2,3)`-solenoid with an **exponential moving-diagonal
rate** — equivalently, an effective normality rate for the base-3/2 minimal/maximal (or `{0,2}`-orbit) word. This is
genuinely new mathematics at the counting horizon; no internal route reaches it. **The concrete outreach target: the
Eliahou group's Normality Conjecture and whether its proved fragments (Thm 1.5/1.7) admit a one-sided, effective
strengthening for the `{0,2}`-orbit word.**

## Soundness
`(K)` `[OPEN]`; no machine decided; no label upgraded. 2026-07-05 red-team: the "`p<q²` softens the exceptional set for
3/2" foothold was **retracted** — `p<q²` thins only the already-thin confinement set (Flatto `dim≤0.585`), while the
equidistribution-exceptional set is full-dimension. Basis notes: `FRONTIER_LIT_2026-07-05`, `DICT_AND_EXCDIM_2026-07-05`,
`CROSSING_STRATEGY_2026-07-05`, `BLIND_{HARMONIC,EFFECTIVENESS}_2026-07-05`, `PARITY_FULLSHIFT_2026-07-05`, `CITATIONS #11`.
