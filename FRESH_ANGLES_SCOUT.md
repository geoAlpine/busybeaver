# Fresh-angles scout for the open kernel — effective o(N) on Σ_{n<N} e(t(3/2)^n), t=4
*(2026-06-28. SOUNDNESS PARAMOUNT. Every line labelled [PROVEN]/[CONDITIONAL]/[OPEN] or by
evidence type. Goal: GENUINELY NEW analytic angles 2018–2026 not among the closed routes
[vdC/Weyl, Mauduit–Rivat, Baker/Padé, Bernoulli-conv/Rajchman, twisted transfer, ergodic a.e.].
NOT committed.)*

## 0. The kernel and the two walls (recap, so "new" is judged against the right bar)
The live lead = effective single-orbit cancellation `S_N(t)=Σ_{n<N} e(t·ξ(3/2)^n)=o(N)` for the
SPECIFIC orbit-determined `ξ` (the parity word is literally the dyadic-arc itinerary of `{4(3/2)^n}`,
verified exactly in `BAKER_LINFORMS.md`). Every known cancellation result for geometric/lacunary
`b^n` (b non-integer fixed) sits behind **exactly one of two walls**:
- **Wall I — metric / a.e.-in-ξ** (Salem–Zygmund CLT, Erdős–Gál LIL, Aistleitner, Algom–Chang–Wu–Wu,
  Koksma/Cassels discrepancy, decoupling L^p means). Cannot be specialised to our single algebraic `ξ`.
- **Wall II — annealed / measure-level** (Fourier decay of an associated measure ν_{2/3}, Furstenberg/
  self-similar/Gibbs measures, sum-product, L²-flattening, Rajchman). Controls the i.i.d. **mean**, not
  the quenched single realisation (`NONPISOT_FOURIER_CHAIN.md` Link C).

A genuinely new lead must escape BOTH walls. The verdict of this scout: **every 2018–2026 technique
surveyed lands behind one of the two walls; there is no new unconditional single-orbit angle.** This is
a clean, honest "no new angle." The one constructive item is a re-framing (§7) and two calibrations that
sharpen *why* the walls hold.

---

## 1. Decoupling (Bourgain–Demeter; Bourgain–Demeter–Guth) — [CLOSED = Wall I]
- **What it is.** ℓ²/ℓ^p decoupling for curved manifolds (parabola, moment curve) ⇒ Vinogradov MVT,
  zeta bounds (Bourgain–Demeter 2015 Annals; Bourgain–Demeter–Guth 2016 Annals).
- **Does it touch lacunary/geometric?** There IS a "discrete L^p decoupling for lacunary exponential
  sums" (Hadamard-gap frequencies `λ_{n+1}>λλ_n`), but it is an **L^p inequality over the torus**:
  it bounds `(∫_𝕋 |Σ a_n e(λ_n x)|^p dx)^{1/p}` by the `ℓ²`/`ℓ^p` sum of the pieces — for lacunary
  frequencies this is essentially **Littlewood–Paley / Rubio de Francia**, i.e. the gain is mere
  Plancherel orthogonality, no curvature.
- **Verdict (c) a.e./ensemble-only.** Decoupling delivers a **mean-over-x** (equivalently a moment /
  additive-energy) bound = the L^p face of Salem–Zygmund's √N. It says **nothing about the value of the
  sum at the single point `x=ξ`** that is our orbit. Identical to the `vdc_num.py` finding that the
  observed √N is provable on average but not for the specific ξ. **Wall I. Closed for the same reason vdC
  is (lacunarity gives only orthogonality, not single-point cancellation).**
- Refs: Bourgain–Demeter, *The proof of the l² decoupling conjecture*, Ann. of Math. 182 (2015);
  Bourgain–Demeter–Guth, Ann. of Math. 184 (2016); Demeter ICM-2018 survey
  (math.uni-bonn.de/ag/ana/WiSe1819/geo-harmonic/ICM-Demeter.pdf).

## 2. Additive combinatorics / sum-product / measure Fourier decay — [CLOSED = Wall II]
The modern engine for "Fourier decay of fractal/dynamical measures": discretised sum-product ⇒
`|μ̂(ξ)|≤C|ξ|^{-a}`.
- **Jialun Li**, *Discretized sum-product and Fourier decay in ℝ^n* (arXiv:1811.06852) and **Li–Sahlsten**,
  Fourier decay for self-affine/self-conformal measures; **Furstenberg-measure decay** (Li, et al.);
  **L²-flattening** Fourier decay (arXiv:2407.16699, 2024): polynomial decay for Patterson–Sullivan,
  Gibbs (non-integrable C² systems), stationary self-affine measures.
- **Lauritz Streck**, *On the Fourier decay and the dimension of self-similar measures* (Cambridge thesis,
  2023–24) + arXiv:2602.05593 *Self-similar measures with slow Fourier decay*: for **algebraic non-Pisot**
  parameters the proven decay can be only **logarithmic** — matches our Varjú–Yu/Kershner verdict for
  ν_{2/3}.
- **Verdict (b)/(c) annealed/measure-only — already closed.** Every output is `|μ̂(ξ)|→0` for a
  **MEASURE** = the i.i.d. average over the random ± signs. The single deterministic orbit is one
  Haar-null realisation; sum-product flattening **cannot be specialised to it** (exactly Link C / the
  Solomyak a.e. exceptional-set wall). The 2024–26 machinery would at best **strengthen the annealed
  ν_{2/3} bound** (which `NONPISOT_FOURIER_CHAIN.md` already shows controls only the *easy* annealed
  carry balance) — **zero quenched gain.** **Wall II.**
- Sum-product over the reals for `{(3/2)^n}` itself (Bourgain/Konyagin-type): the set is an additive
  Sidon-like geometric set; low additive energy of the *frequencies* only controls the **L⁴ mean**
  `∫|Σe(λ_n x)|⁴dx` = additive energy = Wall-I moment again. No single-`t` bound.

## 3. Entropy decrement (Tao 2016; Tao–Teräväinen) — [CLOSED for structural reason]
- **What it is.** The engine behind log-averaged Chowla/Sarnak (Tao, arXiv:1605.04628): an entropy-
  decrement inequality exploiting the **multiplicative dilation structure of ℤ** (correlations of a
  *multiplicative* function along `n` and `pn`) + Matomäki–Radziwiłł short-interval averages.
- **Verdict (b) does not transfer.** Three independent blockers: (i) it produces only **logarithmically
  averaged** correlations; (ii) it is built for **multiplicative functions** (Liouville/Möbius), not a
  deterministic geometric phase; (iii) it requires the **arithmetic dilation/restriction structure** of
  the primes — the single orbit `(3/2)^n` has **no multiplicative semigroup action** to run the
  decrement on. The known obstruction to generalising it ("need a higher-order restriction theorem for
  the primes") has no analogue here. **Not a route.**
- Refs: Tao, *Equivalence of log-averaged Chowla and Sarnak* (arXiv:1605.04628); arXiv:2406.06956
  (arbitrarily slow decay) confirms the method is log-averaged and zero-entropy-system specific.

## 4. Nilsequences / Host–Kra / Frantzikinakis–Host — [CLOSED, same "not polynomial" wall as vdC]
- **What it is.** Structure theorem: bounded sequences = nilsequence (structured) + Gowers-uniform.
  Nilsequences have **polynomial arguments** `g(n)=∏ a_i^{p_i(n)}` in a nilpotent Lie group.
- **Verdict (b) does not apply.** `(3/2)^n` has **exponential** growth — it is provably **not** a
  nilsequence/polynomial orbit (confirmed: exponential ≠ polynomial of any degree; nilpotent Lie groups
  admit no exponential-growth ℤ-homomorphism of this type). The HK/FH machinery controls precisely the
  **polynomial** phases (`{n log₂3}` leading bits) that are **already known equidistributed**; it is
  structurally **blind to the middle-bit / geometric remainder** that is the actual obstruction. Same
  wall as van der Corput. (And the parity word is **not automatic** — subword complexity ≥1.71ℓ,
  IRREGULAR — so the Konieczny/BKM Gowers-uniformity-of-automatic-sequences results in `ATTACK_MAUDUIT_RIVAT.md`
  also do not bite.)
- Refs: Host–Kra–Maass (arXiv:0905.3098); Wikipedia "Nilsequence"; Northwestern Kra *Complexity of
  nilsystems*.

## 5. Effective ×2,×3 / homogeneous-dynamics equidistribution — [CLOSED, integer-only / measure-level]
- **Lindenstrauss–Mohammadi(-Wang)** polynomial effective density (Invent. 2022; arXiv:2211.11099 etc.):
  effective equidistribution of **unipotent/horocycle orbits on homogeneous spaces** — wrong category
  (the ×3/2 endomorphism orbit is not such an orbit).
- **Furstenberg ×p×q**: the single-orbit Diophantine density result (`log p/log q` irrational ⇒ dense)
  is for the **INTEGER** semigroup; measure rigidity (Rudolph–Johnson, Lindenstrauss) needs a
  **positive-entropy invariant MEASURE**. For the non-integer single orbit `(3/2)^n` the dense/equidist
  question **is literally Mahler** (arXiv:2303.01089 "×p-invariant measures with large Fourier coeffs"
  is again about measures).
- **Datta–Jana**, *On Fourier asymptotics and effective equidistribution* (arXiv:2407.11961, 2024) — the
  **sharpest recent Fourier→equidistribution bridge**: a Borel measure `μ` with
  `Σ_{|m|≤X}|μ̂(m)| = O(X^{1/2-θ})`, `θ>7/64`, gives effective horocycle equidistribution; and they prove
  it **fails** for decay `|ξ|^{-1/2+ε}`. **Verdict (c) measure-level** — it still takes a *measure* as
  input, cannot take a single orbit.
- **Two useful calibrations from this paper for our notes:**
  1. Even the *bridge* from Fourier decay to equidistribution needs **annealed decay strictly better
     than square-root-summable** (`>1/2`). Our ν_{2/3} has only **logarithmic** proven decay
     (Varjú–Yu/Kershner) — astronomically below the `−1/2` threshold. So the annealed route is **doubly
     dead**: wrong functional (Link C) AND decay far too slow even if the functional were right.
  2. This independently corrects the AEV_METHODS.md §4 suggestion ("effective power Fourier-decay rate
     for ν_{2/3} ⇒ density via Erdős–Turán"): that route was **superseded/retracted** by
     `NONPISOT_FOURIER_CHAIN.md` (gives only the annealed carry balance), and §5.1 here shows the
     required rate is unattained anyway. **Flag: do not re-pursue the ν_{2/3}-rate route.**

## 6. Mahler 3/2 — specific progress 2020–2026 — [no density help]
- **arXiv:2411.03468** *Mahler's 3/2 problem in ℤ⁺* (2024): **no Z-number is a positive integer**.
  SUPPORT/confinement-level (forbids permanent one-sided confinement for integer x); **NOT** a
  frequency/density bound. Does not touch the kernel.
- **AEV arXiv:2510.11723** (2025/26): normality ⇔ equidistribution (Thm 1.7); combinatorial; **no
  analytic handle, no partial density** (already fully mined in `AEV_METHODS.md`).
- **Base-3/2 / 3x+1 combinatorics**: arXiv:2504.13716 (rational base 3/2 & 3x+1), de Bruijn graphs
  arXiv:1811.02254 — structural, no density.
- **arXiv:1806.03559** *On the Uniformity of (3/2)^n mod 1* (Neeley–Taylor–Veerman, PDX): **purely
  NUMERICAL** to n=10⁸ (strongly consistent with u.d.); **no theorem**.
- **Verdict:** NO 2020–2026 result yields single-orbit cancellation/density. All recent progress is
  support-level or equivalence-reformulation. (Easy regime `p>q²` results — Akiyama/Dubickas Cantor-set/
  short-interval confinement — structurally fail at 3/2 since `p=3<q²=4`, the hardest regime.)

---

## 7. The single most promising NOT-YET-TRIED framing (honest, [OPEN], speculative)
There is **no new unconditional angle.** The cleanest constructive item — genuinely absent from the
existing notes — is a **deterministic (quenched) analogue of the L²-flattening / sum-product Fourier
decay**, run on the orbit's **own finite-N renewal blocks** instead of on a measure:

> **[OPEN, speculative]** Does the single orbit admit a *deterministic finite-time flattening* estimate
> — an effective entropy/L²-increase for the empirical measure `μ_N = (1/N)Σ_{n<N} δ_{ξ(3/2)^n}` under
> one step of the ×3/2 map that beats additive concentration — i.e. a **single-orbit, finite-N sum-product
> inequality** turning the orbit's self-expansion into its own decorrelation?

- **Why it is new.** Wall-II tools (Li, Datta, Streck) flatten a *measure* (annealed average). Nobody has
  formulated/attempted a *deterministic* flattening of one orbit's empirical spectral measure. The
  self-referential coupling (`ATTACK_VDC.md §3`: weight `w_n` correlated with phase) is currently a
  liability; this would try to convert the ×3 self-expansion into an asset (`feedback_solve_only` stance).
- **Why it is hard / what it needs.** A deterministic flattening at this strength would essentially **be**
  effective single-orbit equidistribution — `S_N(t)=o(N)` for fixed ξ. There is **no current technique
  delivering deterministic (vs measure) flattening**; sum-product gives entropy growth only after
  averaging over the random signs. So this **re-frames the wall rather than breaking it**, and must be
  labelled [OPEN] honestly. It is the only direction surveyed that is *not already explicitly closed* —
  worth a small numerical probe (does a finite-N additive-energy / multiplicative-energy increment of the
  orbit's frequency set beat the trivial bound block-by-block?), but with no expectation of a theorem.

## 8. Bottom line (deliverables)
1. **Surveyed new techniques + verdicts:**
   - Decoupling (BD/BDG) — **(c) a.e./mean-only, Wall I.**
   - Sum-product / measure Fourier decay (Li, Li–Sahlsten, L²-flattening, Streck) — **(b)/(c)
     annealed/measure-only, Wall II.**
   - Entropy decrement (Tao) — **(b) closed: needs multiplicative dilation structure, log-averaged only.**
   - Nilsequences / Host–Kra / Frantzikinakis–Host — **(b) closed: phase not polynomial; controls only
     the already-equidistributed leading-bit part.**
   - Effective ×2×3 / homogeneous dynamics (Lindenstrauss–Mohammadi, Datta–Jana) — **(c) measure-level /
     integer-only.**
2. **Most promising not-yet-tried angle:** none unconditional; the only un-closed *framing* is a
   **deterministic single-orbit flattening** (§7), which re-states the difficulty and is [OPEN].
3. **Mahler 3/2 2020–2026:** no help for the density kernel (all support-level / equivalence-only /
   numerical).
4. **Two corrections fed back to the notes:** (i) the AEV_METHODS "effective ν_{2/3} Fourier-rate ⇒
   density" route is doubly dead (wrong functional per NONPISOT, and required rate `>1/2` vs proven
   logarithmic per Datta–Jana §5.1) — **do not re-pursue**; (ii) Datta–Jana gives a clean numeric
   threshold for any future Fourier→equidistribution bridge.

**Honest headline:** the field has exactly two walls (metric-a.e. and annealed-measure); **every
2018–2026 technique surveyed sits behind one of them.** Consistent with `ATTACK_VDC.md`,
`ATTACK_MAUDUIT_RIVAT.md`, `BAKER_LINFORMS.md`, `NONPISOT_FOURIER_CHAIN.md`, `AEV_METHODS.md`. The kernel
(K) = AEV q=2 / Mahler remains [OPEN]; the reduction to it remains the unconditional contribution.

### Citations
- Bourgain–Demeter, Ann. of Math. 182 (2015) 351–389; Bourgain–Demeter–Guth, Ann. of Math. 184 (2016) 633–682.
- J. Li, *Discretized sum-product and Fourier decay in ℝ^n*, arXiv:1811.06852; Li–Sahlsten, Fourier decay self-affine.
- L²-flattening Fourier decay, arXiv:2407.16699 (2024).
- L. Streck, *On the Fourier decay and the dimension of self-similar measures* (Cambridge, 2023–24); arXiv:2602.05593.
- Tao, *Equivalence of log-averaged Chowla and Sarnak conjectures*, arXiv:1605.04628; arXiv:2406.06956.
- Host–Kra–Maass, *Nilsequences and a structure theorem*, arXiv:0905.3098.
- Lindenstrauss–Mohammadi, *Polynomial effective density*, Invent. Math. (2022); arXiv:2211.11099.
- Datta–Jana, *On Fourier asymptotics and effective equidistribution*, arXiv:2407.11961 (2024).
- Mahler 3/2 in ℤ⁺, arXiv:2411.03468; AEV, arXiv:2510.11723; uniformity numerics, arXiv:1806.03559;
  base-3/2 & 3x+1, arXiv:2504.13716; de Bruijn & powers of 3/2, arXiv:1811.02254.
</content>
</invoke>
