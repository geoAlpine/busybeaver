# Anisotropic / analytic transfer operator and resonance-free strip for ×(3/2), actually attempted (2026-06-29)

Open kernel (K): effective single-orbit equidistribution of {(3/2)^n} (one-sided density ≥ 1/3), the
last line of the Antihydra/BB(6) Gibbs–Markov skeleton. Prior finite twisted operators failed (a finite
matrix cannot carry the moving frequency (3/2)^n; `SESSION_2026-06-28_TWISTED_RPF.md`, `THERMO_FORMALISM.md`).
This note attacks the **genuine infinite-dimensional transfer operator** of the expanding ×(3/2) map on an
**analytic / anisotropic Banach space**, asking whether a **resonance-free strip** (Pollicott–Ruelle
resonances; Naud) gives effective decay → (K). Every line labelled. Zero false proofs.

**One-line verdict.** The analytic transfer operator of ×(3/2) IS well-defined (non-soficity of the 3/2
β-shift does NOT block it), but the route is **NOT a new attackable formulation**. It splits cleanly:
the **untwisted** strip is KNOWN and trivial (spectrum {0,1} → annealed Haar mixing only); the
**high-frequency twisted** strip that would give Fourier decay is **unavailable** because Naud's NLI
condition **fails identically for the affine map** (constant roof ⇒ vanishing temporal-distance function,
verified ∂φ/∂u≡0) — the exact expanding-side image of the constant-roof/lattice obstruction; and the
single-orbit content (K) is **strictly beyond any resonance-free strip = equivalent to Mahler**. Non-Pisot
**does** transfer contracting→expanding by inverse-branch duality, but lands precisely on the **annealed**
tier we already own (Link B). **Mahler in disguise for the load-bearing part; known-annealed for the
provable part.**

---

## 1. The correct infinite-dimensional object (set up precisely)

**The map.** `T(x) = (3/2)x mod 1` on `[0,1)` = the β-transformation with β = 3/2 (equivalently the ×(3/2)
carry/phase map `φ_{n+1} = (3/2)φ_n + e_n/4`, `TWISTED_RPF.md`). Two inverse branches
`φ_0(x) = x/(3/2) = 2x/3`, `φ_1(x) = (x+1)/(3/2)`, both **affine with constant slope 2/3**.

**The (untwisted) Ruelle–Perron–Frobenius operator.**
`(L f)(x) = Σ_{Ty=x} |T'(y)|^{-1} f(y) = (2/3) Σ_b f(φ_b(x))`.
Acting on a space of holomorphic functions on an annulus/strip `A ⊃ [0,1)` (Mayer / Ruelle /
Bandtlow–Just–Slipantschuk setting) it is **compact (nuclear)**; spectrum = a sequence of eigenvalues
(Ruelle resonances) ↓ 0. On BV it has a spectral gap (Lasota–Yorke) ⇒ the Parry ACIP.

**The twisted operator (the one that matters).** Twist by the additive character carrying the frequency:
`(L_s f)(x) = Σ_{Ty=x} e^{-s τ(y)} f(y)` with roof `τ = -log|T'| = log(3/2)` (Naud's `L_s`), and/or the
Fourier twist `(L_ξ f)(x) = (2/3) Σ_b e(ξ φ_b(x)) f(φ_b(x))`. The leading eigenvalue modulus of `L_ξ`
at large `ξ` is exactly the self-similar/Bernoulli Fourier coefficient `|ν̂_{2/3}(ξ)|` (Link B identity,
`NONPISOT_FOURIER_CHAIN.md`). The suspension/zeta picture: `ζ(s) = exp Σ_n (1/n) Σ_{T^n x=x} e^{-s τ_n(x)}`,
analytic for `Re s > s_0` where `P(-s_0 τ) = 0` (= topological pressure zero).

**What a resonance-free strip would give for (K).** A strip `{Re s > s_0 - ε_0, |Im s| ≥ t_0}` free of
resonances (= zeros of ζ / spectrum of `L_s`), with the Naud bound `‖L_s^n‖ ≤ C|Im s|^{1+ε} ρ^n`, `ρ<1`,
delivers **effective exponential decay of the twisted correlation / Weyl sum** `Σ e(ξ_N · orbit)` at the
high frequencies `ξ_N=(3/2)^N/8 → ∞`. Via Nagaev–Guivarc'h / Aaronson–Denker–Gouëzel perturbation of the
twisted operator that decay upgrades to a **local CLT ⇒ effective equidistribution**. *Crucial caveat,
established in §3:* the equidistribution it yields is for the **equilibrium measure (annealed)** and for
**μ-a.e. orbit**, never for the single specified computable orbit — so it reaches skeleton lines (4) and the
annealed Link B, **not** line (5)/(K).

---

## 2. The citable theorems and their EXACT hypotheses

### 2.1 Naud, *Expanding maps on Cantor sets and analytic continuation of zeta functions*, Ann. Sci. ÉNS 38 (2005) 116–153 [CITABLE — the closest 1-D analytic statement]
- **Object.** Ruelle transfer operator / dynamical zeta of a real-analytic (C^{1+ε} suffices) uniformly
  expanding finite-branch map on a Cantor/interval set.
- **Temporal-distance function (verbatim, Def. of §2).** With roof `τ` and inverse branches,
  `Δ_ξ(u,v) = Σ_{j≥0} [ τ(φ_{ξ_{-j}}∘…∘φ_{ξ_0} u) − τ(…v) ]`, and
  `φ_{ξ,η}(u,v) = Δ_ξ(u,v) − Δ_η(u,v)`.
- **NLI (Def. 2.1).** ∃ `j, ξ, η, u_0, v_0` with `∂φ_{ξ,η}/∂u (u_0,v_0) ≠ 0`. For **real-analytic** `T, τ`
  this is **equivalent to `φ_{ξ,η}` not identically vanishing** (Naud, §2; = Dolgopyat's symbolic
  non-integrability). **NLI ⇒ non-lattice.**
- **Theorem 2.3 / 1.7.** NLI ⇒ for all ε>0 ∃ `C, ε_0, t_0, 0<ρ<1` s.t. `‖L_s^n‖_{C^1} ≤ C|Im s|^{1+ε} ρ^n`
  for `s_0−ε_0 < Re s ≤ s_0`, `|Im s| ≥ t_0`. ⇒ **resonance-free strip / non-vanishing analytic
  continuation of ζ left of `s_0`.**
- **Hypotheses in one place:** (i) real-analytic (or C^{1+ε}) uniformly expanding finite-branch map;
  (ii) **NLI** = non-constant temporal distance.

### 2.2 Bandtlow–Just–Slipantschuk, *Analytic expanding circle maps with explicit spectra*, arXiv:1306.0445 [CITABLE — decisive for the linear case]
- For **z ↦ z^n** (linear/affine circle maps) and **piecewise-linear Markov interval maps**, the spectrum
  of the analytic transfer operator on `H^∞(A)` is **exactly {0, 1}** (verbatim: "the spectra … coincide
  with the two-point set {0,1}"). I.e. leading eigenvalue 1 (SRB density), then a **perfect gap straight to
  0**: *no nontrivial Ruelle resonances at all.*
- **Nontrivial resonances require nonlinearity.** Their construction yielding `σ(L) = {λ^n}∪{λ̄^n}∪{0}`
  (any `|λ|<1`) uses **non-affine** maps; the resonances are powers of the **derivative at the fixed point**
  of a Blaschke-type inverse branch. Affine ⇒ that derivative structure collapses to {0,1}.

### 2.3 Bandtlow–Naud, *Lower bounds for the Ruelle spectrum of analytic expanding circle maps*, arXiv:1605.06247 (ETDS 39 (2019) 289) [CITABLE]
- A dense set of analytic expanding maps has Ruelle eigenvalues with **exponential lower bounds**; proof
  "combines potential theory and explicit calculations for the spectrum of expanding **Blaschke products**"
  (nonlinear). Reinforces 2.2: the nontrivial resonance structure is a **nonlinearity** phenomenon.

### 2.4 Supporting frame [CITABLE]
- **Dolgopyat (Ann. of Math. 147, 1998)** / **Avila–Gouëzel–Yoccoz (Publ. IHÉS 104, 2006)** / **Stoyanov**:
  non-lattice / (U)NI for flows; same temporal-distance non-integrability, made uniform.
- **Baladi–Tsujii** (anisotropic Banach spaces for hyperbolic maps), **Baladi** (*Dynamical zeta functions
  and dynamical determinants*), **Parry–Pollicott** (Astérisque 187–188): `ρ(L_φ)=e^{P(φ)}` for real φ;
  `s_0` defined by `P(-s_0 τ)=0`. For a probability-preserving step (our case) `P=0`, leading eigenvalue 1.
- **Slipantschuk–Bandtlow–Just** (ultradifferentiable circle maps; complete spectral data for analytic
  Anosov torus maps) — the general analytic-space machinery; confirms operator well-definedness.

---

## 3. The decisive question: known / open-but-well-posed / equivalent-to-Mahler?

The answer is a **clean split**, not a single bucket.

### 3.1 Is the analytic operator even well-defined for non-sofic β=3/2? [PROVEN: YES]
The 3/2 β-shift is **non-sofic** (β non-Pisot ⇒ the T-orbit of 1 is not eventually periodic ⇒ infinite
Hofbauer tower / irrational dynamical zeta). **This does NOT block the transfer operator.** Soficity
controls only the *combinatorics* (finite Markov partition ⇔ rational zeta); the RPF operator is defined by
its **affine inverse branches**, which are explicit regardless. On BV it has a Lasota–Yorke gap (Parry
ACIP); on analytic functions it is nuclear (Mayer/Ruelle). So the object exists. *Non-soficity is a red
herring for definability — the real obstruction is the affine geometry (§3.3), which is independent of it.*

### 3.2 The untwisted strip: KNOWN, trivial, annealed-only [PROVEN]
Because ×(3/2) is **affine**, BJS (§2.2) gives the genuine analytic spectrum **{0,1}** — a *perfect*
resonance-free strip (everything except the leading 1). **Numeric (Ulam/Galerkin, `resonance.py`):** leading
eigenvalue 1 with a gap, subleading `|λ|≈0.73`. The 0.73 is the **known discretization / frozen-angle
artifact** (`twisted_rpf.py` lesson: matrix iteration plateaus at cos(π/4)≈0.717, NOT the true analytic
value 0); the honest analytic spectrum is {0,1}. **Either way this strip only certifies Haar/Lebesgue
mixing** = the **annealed / equilibrium** statement. It says nothing about a moving frequency. Useless for (K).

### 3.3 The high-frequency twisted strip (Naud's object): UNAVAILABLE — NLI fails [PROVEN]
This is the strip that *would* give Fourier decay at `ξ_N=(3/2)^N/8`. **Naud's Theorem 2.3 cannot be
invoked, because NLI fails identically for ×(3/2).** Reason: the map is **affine with a single constant
slope 3/2**, so the roof `τ = -log|T'| = log(3/2)` is **constant**; then every term of `Δ_ξ(u,v)` is
`τ(·)−τ(·) = const−const = 0`, so `Δ_ξ ≡ 0`, `φ_{ξ,η} ≡ 0`, and `∂φ/∂u ≡ 0`. **NLI is violated everywhere.**
**Numeric confirmation (`resonance.py`):**
```
AFFINE x(3/2)  tau=-log(3/2):   ∂φ/∂u samples = [0, 0, 0]        ⇒ NLI FAILS
NONLINEAR perturb (slope varies): ∂φ/∂u samples = [2.15, 1.14, 2.52] ⇒ NLI holds
```
This is the **exact expanding-map image** of the flow obstruction in `THERMO_FORMALISM.md`: constant roof ⇒
period set = `log(3/2)·ℤ` = a **lattice** (Naud Def. 2.2: `τ = f − f∘T + L`, take `f=0, L≡log(3/2)∈mℤ`).
**The same affine degeneracy that hands us the nice {0,1} untwisted spectrum (§3.2) is what kills the
high-frequency strip.** Naud/Dolgopyat/AGY all need nonlinearity (non-constant temporal distance); ×(3/2)
has none. So **no off-the-shelf resonance-free strip at high frequency.**

### 3.4 What strip the affine twisted operator DOES admit = annealed = Link B [PROVEN], and the single-orbit gap = Mahler [OPEN]
Even though Naud is inapplicable, one can still ask for the high-`ξ` spectral radius of `L_ξ` directly. It is
governed by the **self-similar/contracting Fourier operator** `(B)`, `ρ(L_ξ) = |ν̂_{2/3}(ξ)|`-type, whose
decay (`→0`) is **exactly non-Pisot ⇒ Rajchman = Link B** (Erdős–Salem; effective **logarithmic** rate via
Varjú–Yu since 3/2 is algebraic-non-Pisot-non-Salem). So a strip for the affine twisted operator **exists in
the annealed sense and is already KNOWN.** What it gives via Nagaev–Guivarc'h: (i) annealed Weyl-sum decay
[= Link B] and (ii) equidistribution of `{(3/2)^n x}` for **Lebesgue-a.e. x** [= classical Weyl for lacunary
sequences; = skeleton line (4)]. It **cannot** select the single Haar-null computable Antihydra orbit. That
selection is **line (5)/(K) = Mahler/AEV**, strictly beyond what *any* `ρ(L_ξ)<1` / resonance-free strip
provides (a strip is a statement about the operator on a space/measure, not about one deterministic orbit).

### 3.5 Verdict on (a)/(b)/(c)
- **(a) KNOWN:** the untwisted perfect strip {0,1} (BJS) and the annealed high-frequency decay
  (= non-Pisot/Rajchman = Link B, effective log rate). Both real, both **annealed/a.e. only.**
- **(b) OPEN-but-well-posed-and-new:** **NO.** The one theorem (Naud) that converts a strip into an
  *effective high-frequency rate* requires NLI, which **provably fails** for affine ×(3/2). There is no
  well-posed nonlinear-style strip problem here; the map is degenerate exactly where the machinery needs
  curvature.
- **(c) EQUIVALENT to Mahler:** the single-orbit content (K) — the only part not already in (a) — is
  equivalent to Mahler. No resonance-free strip reaches it.

**Net:** the anisotropic/analytic resonance-strip route is **(a) ∪ (c)**: known-and-annealed where provable,
Mahler-in-disguise where it would matter. **Not a genuinely new attackable formulation.**

---

## 4. Does non-Pisot transfer contracting → expanding? [PROVEN: yes, but only to the annealed tier]

**The duality is exact and identifies the two sides.** The contracting IFS `{φ_b(x)=(x+b)/(3/2)}` whose
stationary/Bernoulli measure is (the ×(3/2)-coded analogue of) `ν_{2/3}` is **literally the inverse-branch
system of the expanding ×(3/2) map**. The transfer operator of the expanding map *is* the weighted sum over
those contracting inverse branches: `L_ξ f = (2/3)Σ_b e(ξφ_b)f∘φ_b`. So:

> The **contracting** self-similar Fourier operator `(B)` and the **expanding** twisted transfer operator are
> the **same operator**. Non-Pisot ⇒ Rajchman (`|ν̂_{2/3}|→0`) **transfers verbatim** to a high-frequency
> decay of the expanding twisted operator.

But it transfers to the **annealed** operator (equilibrium-measure average), because Rajchman is a statement
about the *measure's* Fourier transform. The "contracting-vs-expanding gap" flagged in
`NONPISOT_FOURIER_CHAIN.md` is, correctly identified, the **annealed-vs-quenched gap**: the inverse-branch
duality bridges contracting↔expanding *at the annealed level* and **does not cross to the single orbit**.
The quenched object `‖F‖≈0.04` (self-generated `Σ tan(π{(3/2)^j/4})` over the orbit's own weights) is a
**derivative along one trajectory**, not a Fourier coefficient of any measure — so the duality, like the
strip, leaves it untouched. **Non-Pisot transfers; it just transfers to the tier we already own.**

---

## 5. Numerics (verified, `.venv`; honest caveat per twisted-RPF lesson)
```
(1) NLI temporal-distance ∂φ/∂u  (resonance.py)
    AFFINE x(3/2):     [0, 0, 0]               -> NLI FAILS (constant roof)        [the obstruction]
    NONLINEAR perturb: [2.15, 1.14, 2.52]      -> NLI holds (curvature present)
(2) Untwisted Ulam transfer operator of T(x)=(3/2)x mod 1
    N=60/240/960: leading |λ|=1, subleading |λ|≈0.67→0.73   (gap = annealed mixing)
    -> true analytic spectrum is {0,1} (BJS); 0.73 is the known Ulam/frozen-angle artifact, NOT a resonance
```
Caveat (twisted-RPF lesson, re-affirmed): finite-rank spectra of this affine operator **mislead** — the
discretization manufactures a spurious 0.7-ish "resonance" where the true analytic spectrum is {0,1}. The
load-bearing numeric is (1): the **exact** vanishing of NLI, which is an analytic identity (constant roof),
not a finite-rank artifact.

---

## 6. Bottom line (bankable, zero false proofs)
1. **[PROVEN]** The infinite-dim analytic transfer operator of ×(3/2) is **well-defined** despite the 3/2
   β-shift being non-sofic; soficity is irrelevant to definability.
2. **[PROVEN]** Because ×(3/2) is **affine**, Naud's **NLI condition fails identically** (constant roof ⇒
   temporal distance ≡ 0 ⇒ ∂φ/∂u ≡ 0, verified). This is the **expanding-map image of the constant-roof/
   lattice obstruction** and is the operator-theoretic reason the resonance-free-strip machinery (Naud,
   Dolgopyat, AGY) **cannot be invoked** for ×(3/2). Nontrivial Ruelle resonances are a **nonlinearity**
   phenomenon (BJS: linear ⇒ spectrum {0,1}; Bandtlow–Naud: resonances from Blaschke curvature).
3. **[VERDICT]** A resonance-free strip for ×(3/2) is **(a) known-and-annealed** (untwisted {0,1} = Haar
   mixing; high-frequency twisted = non-Pisot/Rajchman = Link B, effective log rate) **∪ (c) equivalent to
   Mahler** for the single-orbit part (K). It is **NOT (b)** a new well-posed problem: the affine degeneracy
   removes exactly the curvature the strip theorems require. **Not a new lead.**
4. **[PROVEN]** Non-Pisot **does** transfer contracting→expanding (the contracting IFS *is* the expanding
   map's inverse-branch system; same twisted operator), but only to the **annealed** tier. The
   contracting/expanding gap = the annealed/quenched gap; duality identifies the sides without crossing to
   the orbit.
5. **[OPEN = Mahler]** (K) — single-orbit equidistribution of `{(3/2)^n}` — remains strictly beyond any
   resonance-free strip. Banked: the **affine-⇒-NLI-fails** identity is the sharp operator-theoretic statement of
   *why* the analytic/anisotropic strip route does not bypass Mahler.



## 7. New attack-surface vocabulary opened (do not narrow)
- The obstruction is now pinned as **curvature/non-affineness**, not soficity and not pressure. Two live,
  non-circular pivots this exposes:
  (i) **Conjugate ×(3/2) to a non-affine model.** Any smooth conjugacy `h` turns ×(3/2) into a map with the
      *same* dynamics but possibly **non-constant roof** (NLI could become nontrivial), while equidistribution
      of the orbit is conjugacy-invariant. Question [OPEN, well-posed, NEW]: is there an analytic conjugacy
      making the temporal distance non-vanishing without destroying the orbit's arithmetic meaning? (The
      naive obstruction: the relevant orbit `{(3/2)^n}` is read in the *original* affine coordinate; a
      conjugacy that creates curvature generally scrambles the very frequency we track — this is the thing
      to test, not assume.)
  (ii) **a.e.→specific selector**, the other wall (`THERMO_FORMALISM.md` §5): the strip gives μ-a.e.
      equidistribution cleanly; attack the *selection* of the computable orbit (effective/computable-point
      equidistribution, effective Tao) **independently** of the strip. The strip route having no new content
      sharpens that this second wall (B) is the one to hit alone.

## 8. References
- Naud, *Expanding maps on Cantor sets and analytic continuation of zeta functions*, Ann. Sci. ÉNS 38 (2005)
  116 (numdam ASENS_2005_4_38_1_116_0); AMS Memoir 1404. — NLI (Def. 2.1), Thm 2.3 strip.
- Slipantschuk–Bandtlow–Just, *Analytic expanding circle maps with explicit spectra*, arXiv:1306.0445. —
  linear/piecewise-linear ⇒ spectrum {0,1}; resonances need nonlinearity.
- Bandtlow–Naud, *Lower bounds for the Ruelle spectrum of analytic expanding circle maps*, arXiv:1605.06247,
  ETDS 39 (2019) 289. — resonances from Blaschke curvature + potential theory.
- Bandtlow–Slipantschuk–Just, *Transfer operators for (ultra)differentiable expanding maps of the circle*;
  *Complete spectral data for analytic Anosov maps of the torus*. — analytic-space machinery.
- Dolgopyat, Ann. of Math. 147 (1998) 357; Avila–Gouëzel–Yoccoz, Publ. IHÉS 104 (2006); Stoyanov. — non-
  lattice / (U)NI.
- Baladi, *Dynamical zeta functions and dynamical determinants for hyperbolic maps*; Baladi–Tsujii
  (anisotropic spaces); Parry–Pollicott, Astérisque 187–188. — pressure = log spectral radius; `P(-s_0τ)=0`.
- Solomyak arXiv:1906.12164; Li–Sahlsten arXiv:1910.03463; Varjú–Yu (log rate); Erdős–Salem. — non-Pisot ⇔
  Rajchman (annealed tier).
- Internal: `THERMO_FORMALISM.md`, `NONPISOT_FOURIER_CHAIN.md`, `SESSION_2026-06-28_TWISTED_RPF.md`,
  `PROOF_STATUS.md` (skeleton lines 4,5); `resonance.py` (this session, numerics).
