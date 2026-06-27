# Thermodynamic formalism / transfer-operator spectral gap for the twisted RPF operator L_t — survey + verdict (2026-06-28)

Target (attack d, `SESSION_2026-06-28_QUENCHED_ATTACK.md`): can transfer-operator spectral-gap theory
(Ruelle–Pollicott resonances, Dolgopyat's method, Naud resonance-free strips, Bourgain–Dyatlov) prove
`ρ(L_t) < 1` for the twisted RPF operator = quenched `(3/2)^j` exponential-sum cancellation = `‖F‖<1` =
Mahler? And does **3/2 non-Pisot** feed a Dolgopyat-type **non-lattice** condition?

**One-line verdict.** The machinery is real, citable, and the **non-Pisot ⇒ non-lattice ⇒ Dolgopyat/Rajchman
gap** chain **is viable — but only for the operator whose spectrum encodes the ANNEALED / equilibrium-measure
average** (the self-similar Fourier operator, where it merely re-proves the already-proven Erdős–Salem Link B,
now with an effective rate). It **hits the identical single-orbit wall**: `ρ(L_t)<1` delivers (i) the annealed
sum → 0, and (ii) a quenched CLT/equidistribution for **μ-a.e.** sequence — never for the one specified,
computable, Haar-null Antihydra orbit. The pressure/variational route does **not** help (the real pressure is
exactly 0; all the decay must come from oscillatory cancellation, i.e. the Dolgopyat input itself). Every line
labelled. Zero false proofs.

---

## 1. The citable spectral-gap theorems and their EXACT hypotheses

All of these give **exponential decay of a twisted/weighted transfer operator via a spectral gap / resonance-free
strip**, and **all** require a **non-arithmetic (non-lattice / non-integrability / Diophantine) hypothesis** on
the system. Listed with the precise condition each needs.

### 1.1 Dolgopyat's method (the prototype) [CITABLE]
- **Dolgopyat, "On decay of correlations in Anosov flows," Ann. of Math. 147 (1998) 357–390.**
- **Object.** Twisted transfer operators `L_{a+ib}` of the symbolic model of a flow; `b` = frequency.
- **Theorem (schematic).** `‖L_{a+ib}^n‖ ≤ C ρ^n` with `ρ < e^{P(a)}` **uniformly for |b| ≥ b₀**, where `P` is
  topological pressure. ⇒ resonance-free strip ⇒ exponential mixing.
- **EXACT hypothesis = the (U)NI / non-lattice condition.** The **temporal-distance / roof function `r` must
  NOT be cohomologous to a function valued in a discrete subgroup `cℤ`** (equivalently the stable/unstable
  foliations are not jointly integrable; "non-lattice" / "uniform non-integrability"). If `r` IS so
  cohomologous (the **lattice / arithmetic** case) the operator family is *periodic* in `b` and there is **no
  gap**. Also needs: hyperbolicity (uniform expansion of the symbolic map) + Hölder/`C^1` regularity of the
  potential and the holonomies.
- **One-dimensional / Cantor-set form.** The (U)NI condition becomes: the **branch inverse-derivatives (the
  log-contraction-ratios) are not all arithmetically related** (their differences generate a dense, not a
  cyclic, additive group).

### 1.2 Naud, resonance-free strip for expanding Cantor sets [CITABLE — closest 1-D analytic statement]
- **Naud, "Expanding maps on Cantor sets and analytic continuation of zeta functions," Ann. Sci. ÉNS 38
  (2005) 116–153** (numdam ASENS_2005_4_38_1_116_0). Memoir-form refinements: AMS Memoir 1404.
- **Object.** Ruelle dynamical zeta function / transfer operator of a uniformly expanding map on a Cantor set.
- **Theorem.** Under the **NLI (non-local-integrability) condition**, the zeta function has a **non-vanishing
  analytic continuation in a strip to the left of the abscissa of absolute convergence** (= a resonance-free
  strip = spectral gap for the twisted operator at high frequency).
- **EXACT hypotheses.** (a) the map is **real-analytic** (or `C^{1+α}` with analytic refinements) and
  **uniformly expanding** on a finite-branch Cantor set; (b) **NLI**: the family of inverse branches is not
  conjugate to an affine/arithmetic family — concretely, the "temporal distance function" is non-constant on
  pairs of branches, i.e. the log-derivatives are **not cohomologous to a locally constant function valued in a
  discrete group**. This is the *exact same non-lattice condition* as Dolgopyat's, in the expanding-map setting.

### 1.3 Stoyanov / Avila–Gouëzel–Yoccoz — the (U)NI condition made uniform [CITABLE]
- **Avila, Gouëzel, Yoccoz, "Exponential mixing for the Teichmüller flow," Publ. IHÉS 104 (2006).**
  Stoyanov, "Spectra of Ruelle transfer operators for axiom A flows."
- **Object/Theorem.** Uniform Dolgopyat bound for twisted operators on non-Markov / countable-branch systems.
- **EXACT hypothesis = UNI (Uniform Non-Integrability):** a quantitative lower bound on the spread of the
  temporal-distance function across branches — the effective, uniform form of "non-lattice."

### 1.4 Bourgain–Dyatlov, Fourier decay of Patterson–Sullivan via spectral gap [CITABLE]
- **Bourgain, Dyatlov, "Fourier dimension and spectral gaps for hyperbolic surfaces," arXiv:1704.02909
  (GAFA 2017)**; companion "Spectral gaps without the pressure condition," arXiv:1612.09040.
- **Theorem.** Convex-cocompact hyperbolic surface ⇒ essential spectral gap depending only on `δ = dim(limit
  set)>0` ⇒ polynomial Fourier decay `|μ̂(ξ)| ≲ |ξ|^{-ε}` of the Patterson–Sullivan measure.
- **EXACT hypothesis.** **Non-linearity** of the group elements (Möbius maps with non-vanishing Schwarzian) +
  Bourgain's **discretized sum–product / additive-energy** input. *Key for us:* the decay rate comes from
  **additive combinatorics**, and the hypothesis that makes it work is precisely that the IFS is **not affine /
  not arithmetic**. For a purely **linear/affine** single-ratio IFS (our annealed object), this nonlinearity
  is absent — see §2.
- Follow-ups giving polynomial PS-decay: arXiv:2404.09424 (polynomial Fourier decay for PS measures); Li–
  Sahlsten and "Fourier decay, renewal theorem and spectral gaps for SL(3,ℝ)".

### 1.5 Self-similar / stationary-measure Fourier decay = the operator that matches OUR annealed object [CITABLE]
- **Solomyak, "Fourier decay for self-similar measures," arXiv:1906.12164 (PAMS 2022).**
  **Li–Sahlsten, "Trigonometric series and self-similar sets," arXiv:1910.03463** (Rajchman ⇔ non-Pisot).
  **Varjú–Yu** (logarithmic rate for algebraic non-Pisot-non-Salem). **arXiv:2305.00527 "Exponential mixing
  via additive combinatorics."**
- **Theorem.** A self-similar measure on ℝ is **Rajchman (μ̂(ξ)→0) iff the inverse contraction ratio is not
  Pisot** (Erdős–Salem, transfer-operator proof). A **polynomial rate** needs a **Diophantine** condition on
  the ratio; non-Pisot alone gives only `→0`.
- **EXACT hypotheses for a RATE.** (a) Rajchman: inverse ratio **non-Pisot** (this is the **non-lattice
  condition for the self-similar Fourier operator**). (b) Polynomial rate: **Diophantine** ratio, holding
  **outside a zero-dimensional exceptional set** — an a.e. statement that **cannot be specialised to the single
  value 2/3** (Solomyak explicitly: results hold outside an exceptional set; specific ratios need individual
  verification). For 3/2: non-Pisot ⇒ Rajchman ✓; effective rate ⇒ **only logarithmic** (Varjú–Yu/Kershner),
  polynomial **[OPEN for this λ]** — exactly as `NONPISOT_FOURIER_CHAIN.md` §1 already concluded.

### 1.6 Foundations (pressure = log spectral radius) [CITABLE]
- Parry–Pollicott, *Zeta functions and the periodic orbit structure of hyperbolic dynamics* (Astérisque 187–188);
  Baladi, *Dynamical zeta functions and dynamical determinants for hyperbolic maps*; Sarig, lecture notes on
  thermodynamic formalism. Gives `ρ(L_φ) = e^{P(φ)}` for **real** potentials φ (§4).

---

## 2. The crucial question: is "non-Pisot ⇒ non-lattice ⇒ Dolgopyat gap ⇒ ρ(L_t)<1" viable?

### 2.1 There are TWO different "non-lattice" conditions — get the right operator
This is the pivot, and it is where naive optimism fails. **Which transfer operator?**

- **(A) The suspension-FLOW / decay-of-correlations operator (Dolgopyat 1998, §1.1).** Its non-lattice
  condition is on the **roof function** `r = -log(contraction ratio)`. Our system has a **single ratio 2/3**,
  so the roof is **CONSTANT** `r ≡ log(3/2)`. A constant roof ⇒ the period set is `log(3/2)·ℤ` = a **LATTICE**
  ⇒ **the flow Dolgopyat condition FAILS** (numerically confirmed below: `log(3/2)=0.4054…`, periods = `r·ℤ`).
  So if one phrases the problem as a suspension flow, it is the **worst, fully arithmetic** case and there is
  **no gap from this operator**. *This is the trap to avoid.*

- **(B) The self-similar FOURIER operator (§1.5).** `L_ξ f(x) = Σ_i p_i e(ξ·a_i) f(λ x + a_i)`, twisted by the
  character `e(ξ·)`; the leading eigenvalue's modulus is `|μ̂(ξ)|`. Its non-arithmeticity condition is
  **"inverse ratio non-Pisot,"** which **3/2 satisfies**. This operator's gap (`|μ̂(ξ)|→0`) is exactly our
  **annealed object** `Φ(N) = Π_j |cos(π{(3/2)^j/4})| = ν̂_{2/3}((3/2)^N/8)` (the exact identity of
  `NONPISOT_FOURIER_CHAIN.md` Link B). We are evaluating at `ξ_N=(3/2)^N/8 → ∞` = the **large-frequency regime
  where Dolgopyat-type gaps live** — so the regime is correct.

**Verdict on viability (the honest answer).**
> For the **correct** operator (B), the chain **non-Pisot ⇒ non-lattice ⇒ spectral gap ⇒ ρ(L_ξ)<1** is
> **VIABLE and CITABLE** — it is precisely the transfer-operator proof of Erdős–Salem/Rajchman, and with
> Varjú–Yu it even carries an **effective (logarithmic) rate** for our specific 3/2. **But its output is the
> ANNEALED average `|μ̂(ξ)| = Φ(N) → 0`, which we already have (Link B).** It does **not** reach the quenched
> single-orbit sum. For the operator (A) (flow), the chain **FAILS at the first step** because a single ratio
> = constant roof = lattice.

### 2.2 The single-orbit-vs-measure wall (the recurring wall, stated precisely for this route)
`ρ(L_t)<1` for the twisted operator gives exactly three things, by standard Nagaev–Guivarc'h /
Aaronson–Denker–Gouëzel perturbation theory of the twisted Gibbs–Markov operator:
1. **Annealed decay:** `μ̂(t)= ⟨L_t^n 1, ·⟩ → 0` exponentially — the equilibrium-measure (= i.i.d.-weights)
   average. **[= Link B, already proven via Erdős–Salem.]**
2. **Quenched CLT / equidistribution for μ-a.e. sequence:** a local limit theorem ⇒ the parity Birkhoff sum
   equidistributes for **μ-almost every** weight-sequence. **[= skeleton line (4), already PROVEN at the Haar
   level.]**
3. **Periodic-orbit counting** (via the zeta function) — irrelevant: the Antihydra orbit is **not periodic**
   (PROOF_STATUS §1, transience).

What it does **NOT** give: equidistribution / genericity of **one specified non-periodic orbit**. The single
Antihydra orbit `c₀=8` is **Haar-null** and **computable** (hence never Martin-Löf-random, never provably
μ-generic a priori — identical to PROOF_STATUS route (a) and skeleton line (5)). A spectral gap is a statement
about the operator's action on a **function space / a measure**; selecting the value of an observable along
**one deterministic trajectory** is outside what any `ρ(L_t)<1` provides. **This is exactly skeleton line (5) =
Mahler/AEV** — the wall is not removed, only re-encoded as "the orbit is μ-generic for the twisted operator."

So: **`ρ(L_t)<1` ⇎ Mahler.** Correctly stated, **`ρ(L_t)<1` ⟺ the ANNEALED cancellation** (which is `‖F‖`'s
annealed/open-loop version, ≈0 because it is multiplied by `Φ→0`), **not** the quenched `‖F‖` for the orbit.
This refines the `SESSION` claim "ρ(L_t)<1 ⇔ Mahler": the equivalence holds only for the **annealed** tier;
the quenched tier (the real `‖F‖≈0.04`, line (5)) is **strictly beyond** the operator's spectrum.

---

## 3. Pressure / variational characterisation — does it help? [VERDICT: NO]

### 3.1 The characterisation
For a **real** potential φ, `ρ(L_φ) = e^{P(φ)}`, `P(φ)= sup_μ ( h_μ + ∫ φ dμ )` (variational principle;
Parry–Pollicott, Sarig; survey arXiv:2107.02166 connects spectral radius ↔ pressure ↔ t-entropy). For the
**probability-preserving** (one-step-exact, λ₂≈0) Antihydra step operator, the leading eigenvalue is **1**, so
`P(0)=0` exactly. Entropy and the (zero-mean) potential **balance**.

### 3.2 Why it does not close the gap
- The twist is **imaginary** (`e(ξ·)`, a unitary character). The variational principle is a theorem about
  **real** potentials and controls only the **modulus/real part**. It gives `|ρ(L_{ξ})| ≤ e^{P(Re)} = e^{P(0)}
  = 1` — i.e. `ρ(L_t) ≤ 1`, the trivial bound. It **cannot** produce the strict inequality `ρ(L_t)<1`.
- Therefore the correct statement is **not "P(twist)<0"** (the real pressure is 0; there is no entropy/pressure
  deficit to exploit). The gap is `ρ(L_{a+ib}) < ρ(L_a)` for `b≠0` (mod lattice), and **all** of it must come
  from **oscillatory cancellation among the complex phases** — i.e. from the **Dolgopyat non-lattice argument
  itself**, not from any thermodynamic/variational quantity. Pressure tells you *where the decay cannot come
  from*, confirming the difficulty is genuinely the oscillatory-cancellation (Mahler) input, not a pressure
  deficit.
- **Honest payoff of the pressure view:** it cleanly explains *why* the problem is hard — there is **zero
  thermodynamic slack** (P=0), so the entire burden is on phase cancellation. This matches the rest of the
  program: the obstruction is not dynamical/energetic, it is the arithmetic of `{(3/2)^j}`.

### 3.3 The non-coboundary fact (commit 794b450) and the non-lattice condition
The parity cocycle being a **non-coboundary** (unbounded recurrent Birkhoff sums, Furstenberg/Conze) is
**necessary** for a Dolgopyat gap (it rules out the degenerate `b=0`/trivial-cocycle case) but is **strictly
weaker than non-lattice**:
- **Non-coboundary:** the cocycle ψ is not `g - g∘T` (Birkhoff sums unbounded). [PROVEN, 794b450]
- **Non-lattice (what Dolgopyat needs):** ψ is **not cohomologous to a locally constant function valued in any
  discrete subgroup `cℤ`** — a *dense-periods* condition, properly stronger.
So non-coboundary **feeds** the non-lattice condition (it is the first of two requirements) but does **not by
itself** establish it. For the **self-similar Fourier operator (B)** the non-lattice condition is supplied
instead by **non-Pisot** (which we have); for the **flow operator (A)** the non-lattice condition **fails**
(constant roof). The non-coboundary fact is therefore best read as: it removes the trivial obstruction, leaving
the genuine non-lattice content carried by non-Pisot — in the annealed tier only.

---

## 4. Numerics (confirming the §2.1 dichotomy) [verified, `.venv`]
```
3/2: min poly 2x-3 not monic ⇒ not an algebraic integer ⇒ non-Pisot, non-Salem      [trivial, PROVEN]
single ratio λ=2/3 ⇒ suspension roof r = -log λ = log(3/2) = 0.40546…
   ⇒ period set r·ℤ = a LATTICE ⇒ FLOW-Dolgopyat (operator A) condition FAILS
self-similar Fourier operator (B): |Π_{j<60} cos(π{(3/2)^j/4})| = 6.96e-22 → 0       [Rajchman gap, non-Pisot]
   −ln(prod)/J = 0.812  vs  ln2 = 0.693
   ⇒ the OBSERVED decay is EXPONENTIAL (≈2^{−N}) = the QUENCHED/Mahler rate, strictly
     faster than anything operator (B)'s annealed spectrum certifies (only log-rate via Varjú–Yu).
```
The last line is the wall in numbers: the annealed operator (B) certifies (rigorously, with rate) only a
**logarithmic** floor; the orbit **observes exponential** cancellation. The gap between them = quenched = (5) =
Mahler, and no `ρ(L_t)` closes it.

---

## 5. Bottom line for the program (bankable, zero false proofs)
1. **[CITABLE survey]** The exact spectral-gap theorems and their hypotheses are pinned (§1): Dolgopyat
   (non-lattice/UNI), Naud (NLI, analytic expanding Cantor set), AGY/Stoyanov (uniform NI), Bourgain–Dyatlov
   (nonlinearity + sum–product), Solomyak/Li–Sahlsten/Varjú–Yu (self-similar: Rajchman ⇔ non-Pisot, rate ⇔
   Diophantine outside a null exceptional set), Parry–Pollicott/Sarig/Baladi (pressure = log spectral radius).
2. **[VERDICT, viability]** "non-Pisot ⇒ non-lattice ⇒ Dolgopyat gap ⇒ ρ(L_t)<1" is **viable for the
   self-similar Fourier operator (B)** and there **re-proves the annealed Erdős–Salem balance with an
   effective (logarithmic) rate** — a genuine, citable, transfer-operator packaging of Link B. It is **NOT
   viable for the flow operator (A)** (single ratio = constant roof = lattice). Either way it **hits the
   single-orbit wall**: `ρ(L_t)<1` ⟺ **annealed** cancellation, **not** quenched/Mahler.
3. **[VERDICT, pressure]** No help. Real pressure `P=0` (zero thermodynamic slack); the gap is purely
   oscillatory-cancellation, i.e. the Mahler input itself. The variational principle gives only the trivial
   `ρ≤1`.
4. **[REFINEMENT of the SESSION claim]** Correct the `SESSION_2026-06-28` statement "ρ(L_t)<1 ⇔ Mahler" to:
   **ρ(L_t)<1 ⇔ ANNEALED cancellation = ‖F‖_annealed ≈ 0** (provable, non-Pisot/Rajchman). The **quenched**
   `‖F‖` for the single orbit = line (5) = Mahler is **strictly beyond** the twisted operator's spectrum.
5. **[Still-live, narrow use]** The right precise tool for the *a.e.* tier is the **twisted Gibbs–Markov
   operator** (Aaronson–Denker–Gouëzel; Nagaev–Guivarc'h): on the renewal map `G` of the skeleton, with the
   parity cocycle non-lattice (non-coboundary ✓ + non-Pisot ✓ for the annealed twist), it gives a **local CLT
   ⇒ ρ(L_t)<1 ⇒ quenched equidistribution for μ-a.e. renewal-block sequence** = skeleton line (4). It does
   **not** select the computable orbit (line (5)). So thermodynamic formalism **completes the a.e. side cleanly
   and names the gap exactly** — it does not cross it.

**Net:** thermodynamic formalism / Dolgopyat gives the cleanest *citable* statement and rate for the **annealed
/ a.e.** tier and pins the obstruction to oscillatory cancellation with zero pressure slack, but `ρ(L_t)<1`
is **equivalent to the annealed cancellation, not Mahler**, and the single-orbit wall is untouched. Banked as a
partial result (effective annealed rate, transfer-operator framing); the quenched line (5) remains [OPEN=Mahler].

## 6. References (arXiv ids / venues)
- Dolgopyat, Ann. of Math. 147 (1998) 357. — non-lattice / temporal-distance gap.
- Naud, Ann. Sci. ÉNS 38 (2005) 116 (numdam ASENS_2005_4_38_1_116_0); AMS Memoir 1404. — NLI, resonance-free strip.
- Avila–Gouëzel–Yoccoz, Publ. IHÉS 104 (2006); Stoyanov. — UNI (uniform non-integrability).
- Bourgain–Dyatlov, arXiv:1704.02909 (GAFA 2017); arXiv:1612.09040. — PS Fourier decay via sum–product.
- Polynomial PS decay: arXiv:2404.09424; Li–Sahlsten et al. SL(3,ℝ) renewal/spectral gaps.
- Solomyak, arXiv:1906.12164; Li–Sahlsten arXiv:1910.03463; arXiv:2305.00527 (exp. mixing via additive combinatorics).
- Varjú–Yu (log decay, algebraic non-Pisot-non-Salem); Kershner (rational λ).
- Parry–Pollicott, Astérisque 187–188; Baladi, *Dynamical zeta functions…*; Sarig, *Thermodynamic Formalism* notes;
  arXiv:2107.02166 (spectral radius ↔ pressure ↔ t-entropy).
- Aaronson–Denker (Gibbs–Markov local limit theorem); Gouëzel (LCLT for GM maps); Nagaev–Guivarc'h perturbation.
- Internal: `NONPISOT_FOURIER_CHAIN.md`, `exp_sum.py`, `PROOF_STATUS.md` (skeleton lines 4,5), commit 794b450.
