# Space Needle (μ = 5/2) — the easy-regime (p > q²) angle

*2026-06-29. SOUNDNESS PARAMOUNT. Every line is labelled `[PROVEN]` / `[VERIFIED]` (machine-checked
this session via the exact-bigint `bb_sim`, not promoted to a proof) / `[OBSERVED]` / `[OPEN]`.
**No decision is made. Default HOLDOUT stands.** All numerics: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`,
exact integer tape, cross-checked against `bb_sim.run`.*

Machine: **Space Needle** = `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD` (verbatim from `suite.py:33`).

---

## 0. Bottom line (read this first)

- **Space Needle is HOLDOUT.** `far_dfa`, `far_finder` (k≤6), `far_cegar` (120 rounds) all return HOLDOUT;
  `bb_sim` shows no halt to 6·10⁷ steps with 1231 F-entries, **all reading 1** `[VERIFIED]`. No sound
  certificate; the cryptid gate is never reached; **no `[DECIDED]` claim is made.**
- **The easy-regime lead is real in the literature but does NOT decide Space Needle.** `p>q²` (5>4) is
  genuinely the regime where unconditional positive theorems exist (unlike Antihydra's 3/2). **But those
  theorems are the wrong shape twice over:** they are either (i) *all-x but a spread/range lower bound*
  (Flatto–Lagarias–Pollington / Dubickas), not avoidance; or (ii) *existence of some confined orbit*
  (Kaneko/Pollington construction), not a statement about the specific Space Needle orbit. **Neither
  delivers `K_SN`.**
- **Honest verdict:** Space Needle is **NOT more tractable for a decision** than the hard-regime cryptids;
  it hits the **same specific-orbit wall** (plus an extra facet mismatch). The easy regime is a real
  *differentiator in the literature*, not a *decision*. **HOLDOUT.**

---

## 1. Verified spec, dynamics, and the exact ×5/2 kernel `[VERIFIED]`

**Transitions.** A:`0→1RB,1→1LA`; B:`0→1LC,1→0RE`; C:`0→1LF,1→1LD`; D:`0→0RB,1→0LA`;
E:`0→1RC,1→1RE`; F:`0→---,1→0LD`.

**Halt discriminator `[PROVEN from spec, VERIFIED]`.** The unique halt is **F reading 0**. F is reached
*only* via `C:0→1LF` (write 1, step left into F). So Space Needle halts ⟺ a leftward `C→F` sweep, having
just written a 1, finds a **0 immediately to its left** at the left frontier — a left-frontier
0-adjacency / 2-adic carry-alignment event. `[VERIFIED]` 1231 F-entries in 6·10⁷ steps, every one reads 1.

**The growth kernel is exactly ×5/2 `[VERIFIED]` (re-reproduced this session).** Clean reset configs
`1¹ 0 1ᵇ` over 6·10⁷ steps give inner-counter milestones

```
b = 12, 36, 96, 246, 621   (then the intermittent 3-block phase: 308, 1090, …)
first differences  Δb = 24, 60, 150, 375     each exactly ×2.5  (60=24·5/2, 150=60·5/2, 375=150·5/2)
```

So the clean induced map is `T(x) = ⌊5x/2⌋`-type: **μ = 5/2, numerator p = 5, denominator q = 2,
v₂(5/2) = −1** (clean 2-to-1 Haar-preserving expanding kernel; `5/2` is one of the multipliers explicitly
`[VERIFIED]`-clean in `BB6_STRUCTURAL_LIMIT_THEOREM.md` §4.1). This **confirms and re-pins the catalogue
finding** (`CATALOGUE_O13_SN.md` §1): the multiplier is **5/2, not 3/2**. `5/2 ∉ {2^a/3^b}`, so Space
Needle is neither Antihydra's literal 3/2 orbit nor the Erdős/`8·3⁻¹` cluster.

**Decider status `[VERIFIED]` this session.**
```
far_dfa.prove   → HOLDOUT (no verified invariant, m≤8, N≤8000)
far_finder.prove→ HOLDOUT (no verified invariant, k≤6, N≤5000)
far_cegar.prove → HOLDOUT (not closed in 120 rounds, |negs|=120)
```

---

## 2. The exact kernel statement `K_SN` `[PROVEN reduction, existence facet]`

Space Needle runs a `⌊5x/2⌋` Mahler counter (the tall "needle" tower, width ~ (5/2)^epoch). Its halt is a
**hitting/alignment event**, so non-halting is an **avoidance** statement for the *single specific orbit*:

> **`K_SN` (non-halt) `[OPEN]`.** Let `O` be the Space-Needle 5/2-counter orbit (the integer iteration
> generating the clean resets `b ↦ ⌊5b/2⌋` plus its intermittent 3-block excursions, seeded by the
> machine). Then **Space Needle does not halt ⟺ `O` never produces a left-frontier 0-adjacency**, i.e. the
> orbit of the seed under the ×5/2 map on ℤ₂ **avoids the clopen carry-alignment set `H` ⊂ ℤ₂ forever.**

**Facet = EXISTENCE (avoidance), not density.** This is the q=2, multiplier-5/2 analogue of o18's q=3
base-3 carry-avoidance (`BB6_STRUCTURAL_LIMIT_THEOREM.md` §3.3/§7), *not* of Antihydra's density underflow.
Empirically `H` is **thin**: 1231 frontier reads, 0 hits — consistent with a measure-zero / summable target
(so Haar-a.e. seed avoids `H` by Borel–Cantelli I ⇒ annealed non-halt a.e.; the specific seed is one
Haar-null point — exactly the o18 situation). What non-halt reduces to is therefore **single-orbit
avoidance / Erdős–Z-number-type confinement of `{seed·(5/2)ⁿ}`** — an **existence** statement, **not** a
Mahler-density statement.

There is **no `β`-barrier here** (that is a density-facet object, `[PROVEN]` for Antihydra only). The
relevant obstruction is the over-approximation/avoidance axis, which the framework labels `[OPEN]`.

---

## 3. What is unconditionally KNOWN for p/q = 5/2 (the easy regime p > q²)

The threshold separating "hard" from "easy" is **p vs q²** (numerator vs denominator²). Antihydra `3/2`:
`3 < 4 = q²` (hard). o18/o15 `8/3`: `8 < 9 = q²` (hard). o5 `4/3`: `4 < 9` (hard). **Space Needle `5/2`:
`5 > 4 = q²` — the EASY regime.** Here genuine unconditional theorems exist. The relevant ones:

### 3.1 All-x spread / range lower bound — Flatto–Lagarias–Pollington & Dubickas `[PROVEN, ALL x]`
> For coprime `p > q ≥ 1` and **every** `ξ ≠ 0` (Dubickas's form requires only `ξ∉ℚ` **or** `α=p/q∉ℤ`,
> which is automatic here since `5/2∉ℤ`):
> `limsup_n {ξ(p/q)ⁿ} − liminf_n {ξ(p/q)ⁿ} ≥ 1/p.`
> Equivalently (FLP): the orbit `{ξ(p/q)ⁿ}` **cannot all lie in an interval shorter than `1/p`**; and
> `Ω(p/q) := inf_ξ (limsup−liminf) ∈ [1/p, q/(p−q)]`.
> **For 5/2:** spread `≥ 1/5` for every seed; `Ω ∈ [1/5, 2/3]`.
- This is the **strongest ALL-x result** and it **does hold for the Space-Needle seed**. But it is a
  **spread/range** statement (the orbit visits ≥ 1/5 of the circle), **not** an avoidance-of-`H`
  statement. (FLP, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 70 (1995) 125–147; Bugeaud,
  Acta Arith. 114 (2004); Dubickas, Math. Nachr. 281 (2008) and *On the fractional parts of rational
  powers*.)

### 3.2 Easy-regime EXISTENCE of confined orbits — Kaneko / Pollington `[PROVEN, EXISTS some x]`
> For `p > q²` there is a set `A(ε) ⊂ [0,1)` of **arbitrarily small Lebesgue measure** such that
> **uncountably many** real `λ > 0` satisfy `{λ(p/q)ⁿ} ∈ A(ε)` for **all** `n`.
- This is exactly the easy-regime positive phenomenon (a nested-interval/Cantor construction; the
  expansion `p/q` is large enough that a confined orbit can be *built*). Equivalently, **`Z_{p/q}`-numbers
  exist for `p > q²`** — which is precisely why the Andrieu–Eliahou–Vivion non-existence conjecture
  (Conj 1.4) carries the hypothesis **`p < q²`** (`AEV_DIGEST.md` §3; arXiv:2510.11723). For `5/2`,
  confined orbits provably **exist**. (Kaneko, *Limit points of fractional parts of geometric sequences*,
  Unif. Distrib. Theory 4 (2009); Pollington-type construction.)

### 3.3 The FLP-range conjecture refinement `[PROVEN, conditional on x algebraic]`
> The conjecture that the orbit is never confined to an interval of length *exactly* `1/p` was established
> for `q < p < q²` (2009) and for `p > q²` **under the assumption `ξ ≠ 0` is algebraic**.
- The Space-Needle seed is rational/integer ⇒ **algebraic**, and `5/2` is `p > q²`, so this *does* apply.
  But again it is a **spread/gap** statement, not avoidance of `H`.

### 3.4 AEV (the umbrella) `[OPEN for all p/q, including 5/2]`
> AEV Conj 1.6 = per-orbit equidistribution mod `qᵏ` of the ceiling map `⌈px/q⌉` is **OPEN for every
> base**, easy regime included. AEV's *only* unconditional easy-regime input is the structural equivalence
> Thm 1.7 and the implication Thm 1.5 (under `p<q²` — which **fails** for 5/2, so even that implication
> does not apply to 5/2). `[VERIFIED]` from `AEV_DIGEST.md`.

---

## 4. The crux — does the easy regime deliver `K_SN` for the SPECIFIC orbit?

Two independent gaps, **both fatal**:

### (a) all-x vs a.e.-x vs specific-x — the recurring wall is NOT escaped
- The **all-x** easy-regime result (§3.1/§3.3) is a **spread** bound — see (b).
- The **specific-x** easy-regime results (§3.2) are **existence of *some* confined orbit** — a
  construction of special `λ`. They say nothing about whether the *given* Space-Needle seed is confined or
  generic. **Wrong quantifier direction.**
- **a.e.-x** equidistribution holds (Koksma/Weyl, for every fixed base > 1) — but that is the metric wall,
  cannot be specialised to one algebraic seed, and for an *avoidance* event it would, if anything, say
  a.e. orbit *hits* a positive-measure target — not what `K_SN` needs.
- **New, important asymmetry:** in the easy regime `p>q²`, confined orbits **provably exist** (§3.2), so
  the clean "all orbits equidistribute / all orbits avoid `H`" route is **provably unavailable** (it is
  *false* as an all-orbits statement). The easy regime, far from giving an all-x decision, is exactly the
  regime where an all-x argument **cannot** exist. The decision still lives in single-orbit genericity of
  the specific seed — **the same wall as the hard-regime cryptids.**

### (b) density vs existence vs the exact form `K_SN` needs — facet mismatch
- `K_SN` needs **avoidance of a thin clopen set `H`** by the specific orbit (existence facet).
- The unconditional easy-regime ALL-x output is a **spread lower bound** (orbit covers ≥ 1/5 of the
  circle). **Spread neither implies nor is implied by avoidance of a measure-zero alignment set:** an
  orbit can have full spread and still hit `H`, or have full spread and miss `H`. So even the *all-x*
  easy-regime theorem is the **wrong facet** for `K_SN`. There is **no** unconditional single-orbit
  *avoidance/equidistribution* statement for `5/2` for any specific orbit.

**Conclusion of the crux.** The easy regime `p>q²` supplies genuine unconditional theorems, but each is
either all-x-but-spread or some-x-existence; **none is specific-orbit avoidance.** `K_SN` is **not
delivered**. Space Needle is **not decided** and **not decidable by this route.**

---

## 5. Triple-check status (per the discipline)

A `[DECIDED]` claim would require (i) the SOUND `far_dfa.verify` confirming an invariant, **AND** (ii) the
cryptid gate passing, **AND** (iii) `bb_sim` cross-check ≥ 10⁷ steps. **Step (i) fails** — all three
deciders HOLDOUT, no invariant is verified, so the cryptid gate is never reached. `bb_sim` (iii) shows
non-halt to 6·10⁷ but that is *evidence of HOLDOUT, never a decision*. **Therefore: HOLDOUT. No decision.**

---

## 6. Honest verdict

1. **Is Space Needle genuinely more tractable than the hard-regime cryptids?**
   **No — not for a decision.** It is genuinely *different in the literature*: `5/2` sits in the easy
   regime `p>q²` where Antihydra (3/2), o18/o15 (8/3), o5 (4/3) do not, and where unconditional positive
   theorems exist. But every such theorem is the wrong shape for `K_SN` (all-x-spread, or
   some-x-existence). The **decision-relevant** content — single-orbit avoidance of a thin carry set by
   the *specific* seed — is **equally open** as for the hard-regime cryptids. If anything the easy regime
   makes the *all-orbits* shortcut **provably impossible** (confined orbits exist), so the burden lands
   squarely back on single-orbit genericity.

2. **Is Space Needle decidable (by our sound tools)?** **No.** HOLDOUT under `far_dfa`/`far_finder`/
   `far_cegar` with generous parameters; no sound certificate; no cryptid-gate pass.

3. **Does the easy regime escape the specific-orbit wall?** **No.** It hits the identical specific-orbit
   wall, with an additional facet mismatch (the available easy-regime ALL-x result is *spread*, while
   `K_SN` is *avoidance*).

4. **What is the real differentiator?** Purely a **literature/placement** differentiator: Space Needle's
   kernel `5/2` is the one frontier multiplier in the *easy* `p>q²` regime, so its non-halt reduces to an
   **easy-regime single-orbit avoidance/Z-number-type statement** (q=2, μ=5/2) rather than the hard-regime
   Mahler/Erdős statements — a cleaner, better-studied neighbourhood (FLP/Bugeaud/Dubickas/Kaneko all give
   *something*), but still no specific-orbit handle. **This is a sharper characterisation, not a decision.**

**Default enforced: HOLDOUT / `[OPEN]`. Zero false proofs. No non-halting asserted unconditionally.**

---

## References
- Flatto, Lagarias, Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 70 (1995) 125–147.
  (gap `≥ 1/p` for all ξ; `Ω(p/q) ≤ q/(p−q)`.)
- Bugeaud, *Linear mod one transformations and the distribution of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 114 (2004).
- Dubickas, *On the powers of 3/2 and other rational numbers*, Math. Nachr. 281 (2008); and *On the
  fractional parts of rational powers* (spread `≥ 1/p` under `ξ∉ℚ` or `p/q∉ℤ`).
- Kaneko, *Limit points of fractional parts of geometric sequences*, Unif. Distrib. Theory 4 (2009) 1–37.
  (easy-regime `p>q²` confined-orbit existence.)
- Tijdeman, *Note on Mahler's 3/2-problem* (1972) (elementary confinement constructions).
- Akiyama, Frougny, Sakarovitch, *Powers of rationals modulo 1 and rational base number systems*, Israel J. Math. (2008).
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723
  (Conj 1.4 non-existence of `Z_{p/q}` **requires `p<q²`** — i.e. `p>q²` is where confined orbits exist;
  Conj 1.6 equidistribution OPEN for all bases).
- Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968).

*Soundness statement: no machine decided; HOLDOUT enforced; every label copied/derived with scope intact;
the ×5/2 kernel is `[VERIFIED]` (exact integer difference ratios, 4 clean epochs, 6·10⁷ steps), not
promoted to `[PROVEN]`. Status files untouched; not committed.*
