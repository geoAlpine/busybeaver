# The non-Pisot ⇒ Fourier-decay ⇒ ‖F‖-contraction chain — rigorous audit (2026-06-28)

Auditing the `mckean_contraction.py` reading:
> "the smallness of ‖F‖ (the contraction) IS the Fourier decay of ν_{2/3}, which holds because 3/2 is non-Pisot."

Verdict up front: the chain has **one rigorous link, one genuine correspondence, and one broken link.**
The measure whose decay is *provably* delivered by the non-Pisot property (the contracting Bernoulli
convolution ν_{2/3}) controls the **annealed mean** (the easy, already-provable carry balance), **not** the
feedback operator ‖F‖. ‖F‖ is a derivative/quenched object governed by the **expanding** self-generated
(3/2)^j exponential sum = Mahler. So **non-Pisot ⇒ ‖F‖ < 1−λ₂ is an ANALOGY, not an implication.** Every
line is labelled. Zero false proofs.

---

## 1. Precise objects

### 1.1 ν_{2/3} — the Bernoulli convolution [definition]
ν_λ = law of `X = Σ_{j≥0} ±λ^j` (signs i.i.d. fair). Fourier transform
`ν̂_λ(ξ) = Π_{j≥0} cos(2π ξ λ^j)` (this is exactly `bc_fourier` in `bernoulli.py`).
Here **λ = 2/3** (in the "fat"/overlapping regime (1/2,1)), so `ξ ↦ Σ ±(2/3)^j` is a **contracting** sum
converging to a measure on ℝ. `1/λ = 3/2`.

### 1.2 Classification of 3/2 [PROVEN, elementary]
- 3/2 is **not an algebraic integer** (rational non-integer; minimal polynomial `2x−3`, not monic).
- ⇒ **not Pisot** and **not Salem** (both are classes of algebraic integers >1).
- It is algebraic (rational). So 3/2 ∈ {algebraic, non-Pisot, non-Salem}.

### 1.3 The Antihydra carry object [PROVEN identity, `exp_sum.py`]
The carry parity is governed by the **expanding** weighted sum
`T_n/2^{n+1} = (1/4) Σ_{j} e_{n−1−j} (3/2)^j  (mod 1)`, weights **growing** like (3/2)^j.
Annealed (i.i.d. Bernoulli p): the characteristic function factorises; at p=1/2
`Φ := |E[e(T_n/2^{n+1})]| = Π_j |cos(π {(3/2)^j/4})|`.

### 1.4 F — the self-generation feedback [definition, `NEW_FRAMEWORK.md` §3, `perturbation_F.py`]
Linearise the self-consistency map ν = L_ν ν at Haar: `δ = (L+F)δ`. With L one-step-exact (λ₂≈0), the
contraction constant is `≤ λ₂ + ‖F‖`. **F is the response (a derivative/sensitivity operator)** of the
output carry/parity **density** to a perturbation of the input **density/correlation**:
`‖F‖ = sup_panel |d(output density)/d(input density)|`. Re-measured this session: **sup ≈ 0.041**
(0.0408 parity, 0.0406 carry; gain *at the real orbit* ≈ +0.007 parity / −0.0007 carry). F is **not** a
Fourier coefficient of any measure — it is a derivative.

---

## 2. The three links, audited

### LINK A. non-Pisot ⇒ ν_{2/3} is Rajchman (ν̂→0) [PROVEN — citable]
**Erdős–Salem dichotomy.** For λ∈(0,1), ν_λ is Rajchman (`ν̂_λ(ξ)→0` as |ξ|→∞) **iff 1/λ is not Pisot.**
- Erdős (1939): 1/λ Pisot ⇒ ν̂_λ ↛ 0.
- Salem (1944): 1/λ not Pisot ⇒ ν̂_λ → 0.
Since 1/λ = 3/2 is non-Pisot, **ν_{2/3} is Rajchman.** [PROVEN, classical.]
Numerically confirmed (`bernoulli.py`, this session): |ν̂_{2/3}(ξ)| falls 1.6e-3 (ξ=10) → 9e-19 (ξ=1e9).
Pisot contrast (golden, 1/λ=φ): along resonant ξ=φ^m it stays ~5e-4 (no decay).

**Effective rate [CONDITIONAL on which theorem you invoke]:**
- Salem's direction gives only `→0`, **no rate**.
- **Varjú–Yu**: if the ratios are powers of λ with 1/λ **algebraic but neither Pisot nor Salem**, then
  ν̂ has **at least logarithmic decay**. 3/2 is exactly algebraic-non-Pisot-non-Salem ⇒ **ν_{2/3} has
  ≥ logarithmic Fourier decay** [CITABLE, effective]. **Kershner**: a power-of-log bound for rational λ.
- **Polynomial decay** for ν_{2/3} is **[OPEN/NOT established for this specific λ].** Solomyak's polynomial
  decay holds for self-similar measures *outside a zero-dimensional exceptional set of ratios* — an a.e.
  statement that **cannot be specialised to the single algebraic value 2/3.** The commit-984f70f claim of a
  "Bourgain–Dyatlov polynomial rate (slope ≈ −1.6)" for ν_{2/3} is a **numerical observation, not a
  theorem**: Bourgain–Dyatlov is about fractal measures on specific Cantor sets, not ν_{2/3}.
  **So the honest effective bound for ν_{2/3} is logarithmic (Varjú–Yu/Kershner), not polynomial.**

### LINK B. ν_{2/3} Fourier decay ⇄ annealed carry balance [PROVEN correspondence — this session]
**A genuine, exact correspondence** (not analogy), newly verified numerically:
`xi*(2/3)^j` with `ξ_N = (3/2)^N/8` gives `(3/2)^{N−j}/8`, so
`|ν̂_{2/3}((3/2)^N/8)| = Φ(N) · (convergent tail)`.
Measured ratio is a **constant 0.7748** across N=5..80 (the N=150 row is float overflow in `1.5**150`,
disregard). So the annealed carry product Φ **is** ν̂_{2/3} sampled along the sparse subsequence
ξ_N=(3/2)^N/8. Since ξ_N→∞, **Rajchman ⇒ Φ→0**: the non-Pisot property *does* rigorously give the
**annealed (i.i.d.) carry balance**.
**Caveat [important]:** the annealed balance is the **easy** part — it is *not* Mahler. Mahler/AEV is the
**quenched** statement for the orbit's *own* self-generated weights `e`, which Link B does **not** touch.

### LINK C. ν_{2/3} Fourier decay ⇒ ‖F‖ < 1−λ₂ [ANALOGY, NOT an implication — the broken link]
This is the link the `mckean_contraction.py` reading asserts. It does **not** hold as a literal implication:

1. **Wrong functional.** Rajchman/Link B controls the **magnitude** |Φ| = the **annealed mean** (first
   moment). ‖F‖ is a **derivative** — the response of the output density to an input perturbation. The two
   are different functionals of the same family; decay of the mean does not bound the derivative.

2. **Wrong measure / wrong direction of the geometric sum.** ν_{2/3} is the **contracting** sum Σ±(2/3)^j.
   The object controlling F is the **expanding** self-generated sum Σ e_j (3/2)^j. Computing the annealed F
   explicitly (`d log Φ/dp` at p=1/2, derived this session):
   `d log Φ/dp = Σ_j 2 i · tan(π {(3/2)^j/4})`.
   **So the true analytic object controlling F is the cancellation of the `tan`-sum `Σ_j tan(π{(3/2)^j/4})`
   over the (3/2)^j orbit** — a (3/2)^j equidistribution/Korobov quantity. Numerics (`Fobj.py`): while
   |Φ|→0 cleanly (Rajchman), the partial tan-sums behave like a random walk (±3.5 at J=10, −562 at J=1000,
   tan terms have no decay) — their control is a **delicate equidistribution fact, not delivered by
   Rajchman.**

3. **Quenched vs annealed.** Even the tan-sum above is the **annealed** (open-loop) F, which is ≈0 because
   Φ→0 multiplies it. The ‖F‖≈0.04 that matters is the **closed-loop/quenched** gain with the orbit's own
   correlated weights. Controlling *that* for the specific orbit **is exactly the Mahler/AEV core** —
   precisely the [OPEN] line (5) of the GM skeleton. Rajchman of ν_{2/3} says nothing about a single
   Haar-null quenched realisation.

**Conclusion on Link C:** "non-Pisot ⇒ ‖F‖ small" is a **structural analogy** — both phenomena are governed
by the *same* 3/2-Pisot dichotomy and the *same* (3/2)^j equidistribution, which is why the heuristic feels
right and why 3/2 being non-Pisot is genuinely *favorable*. But there is **no rigorous chain** from the
provable decay of the contracting ν_{2/3} (annealed mean) to a bound on the quenched derivative ‖F‖.

---

## 3. The true analytic object controlling ‖F‖
**[OPEN = Mahler]** ‖F‖ is governed by the cancellation of the **self-generated (quenched) (3/2)^j
exponential/`tan`-sum** `Σ_{j} w_j tan(π{(3/2)^j/4})` (annealed form), with `w` the orbit's own parity —
i.e. effective equidistribution of `{(3/2)^j}` for the specified orbit. This is identical to GM-skeleton
line (5) / Mahler / AEV-normality (arXiv:2510.11723). Non-Pisot gives the *annealed* version
(Link B, provable) but not the *quenched* version (the actual ‖F‖).

## 4. What IS rigorously bankable from the non-Pisot fact
- **[PROVEN]** ν_{2/3} is Rajchman (Erdős–Salem; 3/2 non-Pisot).
- **[PROVEN, this session]** That Rajchman decay, along ξ_N=(3/2)^N/8, **equals** the annealed carry
  product Φ→0 ⇒ the **annealed (i.i.d.) carry bit is balanced** — a clean closed proof of the *annealed*
  model, with an effective **logarithmic** rate (Varjú–Yu/Kershner, since 3/2 is algebraic-non-Pisot-non-Salem).
- **[NOT bankable]** any bound on ‖F‖ or on the quenched single-orbit sum from these facts.

## 5. Citable references
- **Erdős–Salem dichotomy** (Rajchman ⇔ 1/λ non-Pisot): see survey *Self-similar measures and the Rajchman
  property* (Li–Sahlsten, arXiv:1910.03463); *Sixty Years of Bernoulli Convolutions* (Peres–Schlag–Solomyak).
- **Varjú–Yu** — logarithmic Fourier decay when ratios are powers of λ, 1/λ algebraic but not Pisot/Salem
  (the directly applicable effective theorem for 3/2). **Kershner** — power-of-log bound for rational λ.
- **Solomyak** — polynomial decay outside a zero-dimensional exceptional set (a.e.; **not** specialisable to 2/3).
- **Mahler's 3/2 problem** (Wikipedia; arXiv:2411.03468 "Mahler's 3/2 problem in ℤ⁺"; arXiv:1806.03559
  "On the Uniformity of (3/2)^n mod 1"); **AEV normality** arXiv:2510.11723.

## 6. Recommendation for `mckean_contraction.py`
Retract the verbatim claim that "‖F‖ small IS the Fourier decay of ν_{2/3}." Replace with the honest
two-tier statement: (i) **[PROVEN]** non-Pisot ⇒ Rajchman ⇒ the *annealed* carry balance (Link B, with a
citable logarithmic rate); (ii) **[OPEN]** ‖F‖ is the *quenched* (3/2)^j cancellation = Mahler, for which
non-Pisot supplies a favorable structural analogy but **no implication.** The non-Pisot fact strengthens the
annealed engine; it does not close the tracking/quenched gap.
