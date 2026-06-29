# Hochman/Varjú dimension theory vs. h_μ>0 — does self-similar-measure dimension give an UNCONDITIONAL quenched partial? (2026-06-29)

*Assigned: assess whether Hochman (Annals 2014) / Hochman–Shmerkin / Varjú (Annals 2019) dimension theory for
self-similar / Bernoulli-convolution measures delivers an UNCONDITIONAL positive lower bound on the 2-adic
entropy / dimension of the QUENCHED single-`⟨3/2⟩`-orbit limit measure `μ` (`c₀=8`, `c_{n+1}=⌊3c_n/2⌋`), a genuine
partial toward (K) that AIU lacks — or whether it is ANNEALED-only. SOUNDNESS PARAMOUNT: every claim labelled
[PROVEN]/[PROVEN-in-lit]/[CONJECTURE]/[OBSERVED]/[OPEN]; (K) NOT proven; NO label upgraded. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/hochman_dim.py` (N=2·10⁶, <1s). NOT committed.*

---

## 0. One-line verdict

**Verdict (b): ANNEALED-ONLY, with the gap doubled.** `dim ν_{2/3} = 1` is **PROVEN** (Hochman 2014; the rational
case is the *easy* corner — no exact overlaps is forced by the rational-root theorem, similarity dim
`log2/log(3/2)=1.71>1`, so `dim=min(1,1.71)=1`; Varjú not even needed). But this dimension is (i) a property of the
**annealed self-similar MEASURE** `ν_{2/3}` (the law of the random sum with i.i.d. coefficients), whereas the
Antihydra orbit is **one deterministic point** of that measure — a single point has dimension 0, and Hochman/Varjú
say *nothing* about the genericity of a specified point; and (ii) the **archimedean (ℝ)** dimension of `ν_{2/3}`,
whereas `h_μ(M₂)` is the **2-adic** entropy RJ needs — a second place-mismatch. **No Hochman/Varjú result gives any
unconditional positive lower bound on the quenched `h_μ`.** The transfer "single orbit is `ν_{2/3}`-generic" is
itself (K)/Mahler. This is the *same* annealed/quenched wall already documented for Rajchman decay
(`SECOND_DIAGONAL_RAJCHMAN`) and for the contraction `‖F‖` (`NONPISOT_FOURIER_CHAIN` Link C), now exhibited on the
dimension axis. **No machine decided. No label upgraded.**

---

## 1. Which measure is self-similar, and dim(ν_{2/3}) status `[PROVEN-in-lit]`

The carry of the Open Lemma is `S_n = Σ_{j<n} b_j 2^j 3^{n-1-j}`, `b_j = c_j mod 2`, so
`S_n/3^{n-1} = Σ_{j<n} b_j (2/3)^j` lands on the **support of the Bernoulli convolution `ν_{2/3}`** (contraction
ratio `λ=2/3`, `1/λ=3/2`), the law of `X = Σ_{j≥0} b_j (2/3)^j` with `b_j` i.i.d. fair (`SECOND_DIAGONAL_RAJCHMAN §1`,
`NONPISOT_FOURIER_CHAIN §1.1`). `ν_{2/3}` is a **self-similar measure** on ℝ for the IFS `{x↦(2/3)x, x↦(2/3)x+1}`.

> **`[PROVEN-in-lit]` `dim ν_{2/3} = 1` (Hausdorff = entropy dimension), unconditionally.**
> *Reason (Hochman 2014, Thm 1.1 + the algebraic exact-overlap dichotomy).* For a self-similar measure on ℝ with
> exponential separation, `dim = min(1, similarity dimension)`. Here `sim dim = h/χ = log2 / log(3/2) = 1.7095 > 1`.
> For **algebraic** `λ`, Hochman proves "**no exact overlaps ⇒ exponential separation**", and the Bernoulli
> convolution has an exact overlap iff some `{-1,0,1}`-coefficient polynomial vanishes at `λ`. For `λ=2/3` (lowest
> terms `p/q=2/3`) the **rational-root theorem** forbids this: any rational root `p/q` of an integer polynomial needs
> `q | (leading coeff)`, but a `{-1,0,1}`-polynomial has leading coeff `∈{-1,1}` and `3∤±1`. **So `2/3` is a root of
> no `{-1,0,1}`-polynomial ⇒ NO exact overlaps ⇒ exponential separation ⇒ `dim ν_{2/3}=min(1,1.71)=1`.** The
> rational parameter is the *trivial* case of the exact-overlap test — Varjú's algebraic machinery (Mahler-measure
> bounds) is needed for hard irrational algebraics, **not** for `2/3`.

(Caveat, not needed here: `dim=1` does **not** assert `ν_{2/3}` absolutely continuous; a.c.-ness of this specific
rational `λ` is a separate, finer question. Dimension 1 is all Hochman gives and all we cite.)

**Numerics (T1, `hochman_dim.py`, N=2·10⁶):** per-scale entropy increment `dH_m/dm` of binned `X` rides **0.999±0.001
bit** through every fully-sampled dyadic scale `m=5…16` (fill=1.000), rolling off only at `m≥18` where the sample
undersamples (`fill<0.97`) — the entropy dimension of `ν_{2/3}` is numerically `=1`, matching the proven value.
**Relation to annealed gap-½ / Rajchman:** YES, consistent — the proven `ν_{2/3}` Rajchman decay
(`NONPISOT_FOURIER_CHAIN` Link A) and the annealed transducer gap ½ (`NEWMATH_DIAGONAL_RENORM §3.1`) are the
Fourier/operator shadows of the same `dim=1`; all three are **annealed** statements about `ν_{2/3}` / the i.i.d.-carry
model, and `dim ν_{2/3}=1` ⇔ the annealed carry marginal is full-dimensional (positive-dimensional, indeed maximal).

---

## 2. DECISIVE — does it transfer to a lower bound on the QUENCHED h_μ? `[PROVEN obstruction — NO]`

**No.** Two independent, fatal gaps, each by itself decisive:

**(G1) Annealed measure vs. single deterministic orbit (a point has dimension 0).** Hochman/Varjú compute the
dimension of the **measure** `ν_{2/3}` = the distribution of `Σ b_j(2/3)^j` over **i.i.d. random** `b_j`. The
Antihydra orbit fixes `b_j = c_j mod 2` — **one deterministic sequence**, i.e. **one point** `x* ∈ supp ν_{2/3}`.
A single point has dimension 0; `dim ν_{2/3}=1` is an average over the whole randomised ensemble and says **nothing**
about whether the specific point `x*` is `ν_{2/3}`-generic. Hochman's theorem has **no single-orbit / genericity
clause**. To use `dim ν_{2/3}=1` for the orbit one would have to *first* prove the orbit's empirical measure converges
to `ν_{2/3}` (or is `ν_{2/3}`-distributed) — that is exactly the quenched equidistribution = (K)/Mahler
(`SECOND_DIAGONAL_RAJCHMAN §3`, `NONPISOT_FOURIER_CHAIN §3` Link C, `NEWMATH_DIAGONAL_RENORM §4` R-GEN). The
self-similar-measure dimension is delivered **by construction** for the i.i.d. (annealed) model and is destroyed the
instant the coefficients become the deterministic orbit parities. `[PROVEN — definitional]`

**(G2) Archimedean dimension of `ν_{2/3}` vs. 2-adic entropy `h_μ(M₂)`.** Even granting (counterfactually) that the
orbit were `ν_{2/3}`-generic, `dim ν_{2/3}=1` is a **real-place (ℝ)** Hausdorff dimension of the *contracting* sum
`Σ b_j(2/3)^j`. The entropy RJ needs is `h_μ(M₂)` on the **`ℚ₂`-factor** of the solenoid — the *expanding* place
`|3/2|₂=2`. These are different completions; `dim_ℝ ν_{2/3}` does not bound `dim_{ℚ₂} μ₂`. The 2-adic local dimension
of `μ` is the genuinely (K)-relevant quantity (`LIMIT_MEASURE_ENTROPY §2`, `POSITIVE_ENTROPY_ATTACK §1`), and
Hochman's ℝ-dimension theory is mute about it. `[PROVEN-in-lit place distinction; Lind–Schmidt–Ward]`

> **Net.** Hochman/Varjú give an **unconditional `dim ν_{2/3}=1` — for the annealed real-place measure only.** It
> yields **no** unconditional lower bound on the quenched 2-adic `h_μ`. Outcome **(a) is NOT achieved**; this is **(b)
> annealed-only**, and the transfer to the orbit is **(c) = (K)**.

---

## 3. No-exact-overlaps / no-atom — does the PROVEN non-Pisot no-atom upgrade via Hochman? `[PROVEN — partial only annealed]`

- The **no-exact-overlaps** condition Hochman needs holds for `ν_{2/3}` trivially (§1, rational-root theorem). So the
  hypothesis is met **for the annealed measure**, giving `dim ν_{2/3}=1`. This is a real, clean, unconditional fact —
  but about `ν_{2/3}`, not `μ`.
- The repo's **PROVEN non-Pisot no-atom** result (`NEWMATH_DIAGONAL_RENORM §3.2`: `|3/2|₂=2>1`, `R*:ξ↦(3/2)ξ` has no
  nonzero periodic point ⇒ no atomic/Pisot/sofic `A`-fixed point) lives on the **2-adic / solenoid** side and is a
  statement about the *operator/spectrum*, i.e. it rules out the **dimension-0 (atomic) extreme** for any
  `A`-invariant smooth-on-`ℚ₂` measure. **It does not upgrade to a positive dimension lower bound on the quenched `μ`
  via Hochman:** Hochman needs a self-similar *measure* with separation in the place where dimension is measured;
  the quenched `μ₂` is not presented as a self-similar measure with i.i.d. coding (its "coefficients" are the
  deterministic carries), so Hochman is inapplicable to it. No-atom excludes `h_μ=0`-via-concentration but gives **no
  positive lower bound** on `H_ℓ/ℓ` (`POSITIVE_ENTROPY_ATTACK §3`, row 4). Non-Pisot ⇒ no-atom is the annealed/spectral
  shadow; Hochman ⇒ `dim=1` is the annealed/real shadow; **neither crosses to the quenched orbit.** `[PROVEN]`

---

## 4. Numerics `[OBSERVED]`

`scratchpad/hochman_dim.py`, N=2·10⁶, exact float sums, `nterms=60`.

| object | quantity | value | reading |
|---|---|---|---|
| `ν_{2/3}` similarity dim | `log2/log(3/2)` | **1.7095** | `>1` ⇒ predicted `dim=min(1,·)=1` |
| `ν_{2/3}` entropy-dim (T1) | `dH_m/dm`, m=5…16 (fill=1) | **0.999 ± 0.001** | numeric `dim=1`, matches Hochman |
| `ν_{2/3}` deep scales | m≥18 | rolloff (fill<0.97) | pure undersampling artifact, not a deficit |
| exact-overlap test | `3 ∣ {-1,1}`? | **impossible** | no `{-1,0,1}`-poly root at 2/3 ⇒ no overlaps |
| quenched 2-adic (cross-ref) | `ĥ_μ(M₂)` (`pos_entropy.py`) | `1.00±0.02` bits, OPEN | annealed-indistinguishable; positivity unproven |

Both axes (annealed `ν_{2/3}` real dim, quenched `μ` 2-adic per-bit entropy) sit at `≈1` numerically — the
equidistribution evidence, read on the dimension axis. Neither is a proof for the orbit.

---

## 5. Honest verdict (the four asks)

| ask | answer | label |
|---|---|---|
| **dim(ν_{2/3})=1 proven?** | **Yes, unconditionally.** Hochman 2014: no exact overlaps (rational-root theorem, the trivial case) + sim dim 1.71>1 ⇒ `dim=min(1,1.71)=1`. Varjú not required. | **`[PROVEN-in-lit]`** |
| **(a) unconditional positive lower bound on QUENCHED `h_μ`?** | **No.** `dim ν_{2/3}=1` is annealed (the i.i.d.-coefficient *measure*) and archimedean. The orbit is one deterministic point (dim 0); Hochman has no genericity clause; and `h_μ(M₂)` is 2-adic. | **none** |
| **(b) annealed-only? exact gap.** | **Yes.** Two gaps: **(G1)** self-similar *measure* (i.i.d. coding) vs. *single deterministic orbit* — "orbit is `ν_{2/3}`-generic" = (K)/Mahler; **(G2)** real-place `dim ν_{2/3}` vs. 2-adic `h_μ(M₂)` (different completions). | **`[PROVEN obstruction]`** |
| **(c) reduces to (K)?** | **Yes** — the transfer (orbit `ν_{2/3}`-generic / quenched inherits annealed full dimension) is R-GEN = AEV Conj 1.6 = Mahler 3/2 at α=8. | **`[PROVEN reduction]`** |

**Exact residual gap.** Hochman closes the **annealed** dimension question (`dim ν_{2/3}=1`, no-overlap trivial for
rational λ). What stays open is identical to the Rajchman and `‖F‖` walls: show the **single deterministic orbit** is
generic for its annealed model — and, additionally, push from the archimedean ℝ-dimension to the 2-adic `h_μ(M₂)`
that Rudolph–Johnson reads. Both are (K). Hochman/Varjú give a *favorable structural fact* (the annealed object is
maximally spread, dim 1) but **no implication** for the quenched orbit. AIU still lacks a quenched positive-entropy
partner, and this route does not supply one.

---

## 6. Genuinely new vs prior

- **vs `LIMIT_MEASURE_ENTROPY` / `POSITIVE_ENTROPY_ATTACK`:** those proved `h_μ(M₂)>0` is necessary, (K)-hard, and
  unprovable from proven structure, the obstruction being unweighted-linear vs. weighted-exponential count. This note
  adds the **specific Hochman/Varjú dimension result** as a candidate weapon and **rules it out** by naming the two
  exact transfer gaps (G1 annealed-measure-vs-point, G2 ℝ-vs-ℚ₂) — Hochman is precisely a "frequency-weighted
  exponential spreading" theorem, but only for the **annealed** measure, so it cannot supply the missing quenched
  lower bound.
- **vs `NONPISOT_FOURIER_CHAIN` (Rajchman, Link A/C) / `SECOND_DIAGONAL_RAJCHMAN`:** those established the
  Fourier-decay annealed/quenched split for `ν_{2/3}`. This note shows the **dimension** of the *same* `ν_{2/3}` is
  also unconditionally maximal (=1, Hochman) and splits at the *same* seam — Rajchman decay and `dim=1` are two faces
  of `ν_{2/3}` being a non-Pisot full-dimension measure, both annealed, both stopped by the single-orbit wall.
- **vs `NEWMATH_DIAGONAL_RENORM §3` (annealed gap ½, non-Pisot no-atom):** this note supplies the **dimension-theoretic
  reading** of those: gap ½ / no-atom ⇔ the annealed attractor is full-dimensional Haar; Hochman `dim ν_{2/3}=1` is
  the matching real-place statement. The no-atom result does **not** upgrade to a quenched positive-dim bound via
  Hochman (Hochman needs the i.i.d.-coded self-similar measure, which the quenched `μ` is not).

## Sources
- **Hochman**, *On self-similar sets and measures on the line*, Annals of Math. 180 (2014) 773–822 — `dim = min(1,
  sim dim)` under exponential separation; for algebraic params, no exact overlaps ⇒ exponential separation. `[PROVEN-in-lit]`
- **Hochman–Shmerkin**, *Local entropy averages and projections of fractal measures*, Annals 175 (2012). `[PROVEN-in-lit]`
- **Varjú**, *On the dimension of Bernoulli convolutions for algebraic parameters*, Annals 189 (2019) 1001–1011 —
  `dim ν_λ=1` for algebraic `λ∈(1/2,1)` of bounded Mahler measure (needed for hard irrational λ, **not** for rational 2/3). `[PROVEN-in-lit]`
- **Breuillard–Varjú**, *On the dimension of Bernoulli convolutions* (2019); **Shmerkin** (GAFA 2019, `L^q` dimensions);
  Peres–Schlag–Solomyak, *Sixty Years of Bernoulli Convolutions*. `[PROVEN-in-lit]`
- **Rudolph** (ETDS 1990) / **Johnson** (1992) / solenoid form arXiv:2101.11120 — `AIU + h_μ(M₂)>0 ⟹ Haar ⟹ (K)`;
  **Lind–Schmidt–Ward** (solenoid entropy `h(×u)=Σ_v log⁺|u|_v`, the place distinction G2). `[PROVEN-in-lit]`
- **Mahler 3/2** (1968, open); **AEV** arXiv:2510.11723 (Conj 1.6 = (K) at α=8).
- Repo: `LIMIT_MEASURE_ENTROPY.md`, `POSITIVE_ENTROPY_ATTACK.md`, `NONPISOT_FOURIER_CHAIN.md` (Links A/B/C),
  `SECOND_DIAGONAL_RAJCHMAN.md`, `NEWMATH_DIAGONAL_RENORM.md` (annealed gap ½, no-atom, R-GEN), `AIU_JOININGS.md`.
- Numerics: `scratchpad/hochman_dim.py` (N=2·10⁶, <1s): sim dim 1.7095; entropy-dim increment 0.999±0.001 over fully
  sampled scales m=5…16; rational-root exact-overlap impossibility.

**No machine decided. No label upgraded.**
