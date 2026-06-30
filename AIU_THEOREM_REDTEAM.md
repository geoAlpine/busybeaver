# RED-TEAM of the "AIU Neutral-Direction Obstruction Theorem" (2026-06-30)

*Adversarial verification. Target claim (sibling agent): the Einsiedler–Lindenstrauss (EL) high-entropy
measure-rigidity method is **structurally inapplicable** to the AIU host-invariance upgrade because AIU's
surplus invariance lives along a **NEUTRAL (zero-Lyapunov) coarse direction** — `×2` acting on `ℚ₃`,
`|2|_3=1`. JOB: try to BREAK or over-claim-check it against the literature. Soundness paramount; every claim
labelled. No machine decided. No label upgraded.*

---

## 0. VERDICT — **[NEEDS-CAVEAT]** (sound for the narrow scope "the EL high-entropy method"; OVER-CLAIM if it asserts "no measure-rigidity method reaches central directions")

The theorem **survives** as a statement about the EL **high-entropy** method: that method does propagate
invariance only along **nonzero-exponent coarse-Lyapunov subgroups of a rank-≥2 action**, and the AIU
surplus (`×2|_{ℚ₃}`) is a zero-exponent neutral direction carrying no leafwise entropy. All three premises
check out against the literature (§1–§3). **BUT** the red team found one genuine over-claim risk and one
premise-framing flaw that the theorem MUST absorb or it over-states:

- **(OVER-CLAIM RISK)** There **is** a dedicated measure-rigidity method that manufactures invariance
  **precisely from zero central exponents**: the **Furstenberg–Ledrappier–Avila–Viana Invariance
  Principle** (and its homogeneous cousin, the Anzai–Furstenberg–Veech isometric-extension theory used in
  `AIU_SKEW_ROTATION.md`). "Zero exponent ⟹ rigidity" is the Invariance Principle's *thesis*, not its
  blind spot. So a blanket "central/neutral directions are where measure rigidity has no leverage" is
  **false** and would be an over-claim. The correct obstruction is two-ingredient (neutrality **AND**
  non-recurrence), not neutrality alone (§1, §4).

- **(PREMISE FRAMING)** The high-entropy method is a **consumer** of rank-≥2 invariance, not a **producer**
  of it. AIU is exactly the step that would *produce* the rank-2 (host) invariance from rank-1
  (`A`)-invariance. So "one would try the high-entropy method to supply AIU" is ill-posed: that method
  presupposes the very `Φ`-invariance AIU is trying to establish. The neutral-direction obstruction, while
  true, is partly aimed at the wrong tool (§2).

The precise correct form is in §5. It is the conjunction already present (split across two repo notes) —
`AIU_JOININGS.md §3.3` (neutrality / no entropy leverage) **and** `AIU_SKEW_ROTATION.md §2.2` (dissipative,
non-recurrent base kills the isometric-extension / Invariance-Principle route). **Neither note alone is the
theorem; the theorem is their conjunction**, and stating only the neutrality half is the over-claim.

---

## 1. Q1 — Does ANY method generate invariance along CENTRAL / NEUTRAL directions? **YES — flag it.**

The literature is unambiguous that zero-central-exponent directions are **not** a universal dead zone for
rigidity; there is a whole industry built on extracting rigidity *from* vanishing exponents.

- **Furstenberg–Ledrappier–Avila–Viana Invariance Principle.** "It is expected that measures with zero
  center exponents satisfy some rigidity… the center disintegration of invariant measures with zero center
  exponents is invariant by a family of holonomies, known as the Invariance Principle" (Avila–Viana,
  extending Ledrappier, extending Furstenberg for random matrix products). "The Invariance Principle asserts
  that for the Lyapunov exponents to vanish the system must exhibit rather rigid (holonomy invariant)
  features." This is **invariance generated exactly along the zero-exponent (central) direction** — the
  opposite of "no leverage on neutral directions." Eskin–Mirzakhani and Zimmer-program work use it.
  `[PROVEN-in-lit]`
- **Homogeneous analogue (already in the repo).** `AIU_SKEW_ROTATION.md` correctly identifies the
  Anzai–Furstenberg–Veech isometric-extension theorem: an invariant measure of a compact-group (here
  `ℤ₃^*`-rotation) extension over a **probability-preserving** base has **Haar-coset fibers**; if the fiber
  rotation is ergodic (here `R_2` uniquely ergodic, `2` a topological generator of `ℤ₃^*`) the fibers are
  full Haar. That **would deliver AIU** — invariance along the neutral rotation — *if its hypothesis held*.
  `[PROVEN-in-lit]`

**Consequence for the theorem.** A statement of the form "the high-entropy/product-structure method
generates invariance only along entropy-carrying directions" is **correct and defensible** (§2, §3). A
statement of the form "AIU's invariance is neutral, hence **no** measure-rigidity method can reach it" is an
**OVER-CLAIM**: the Invariance Principle / isometric-extension theory is a counter-method aimed squarely at
neutral directions. The theorem must (a) scope itself to the high-entropy method, **and** (b) separately
dispatch the Invariance-Principle route — which the repo does, via non-recurrence (§4), but the
*Neutral-Direction* theorem as titled does not, by itself.

---

## 2. Q2 — Is the coarse-Lyapunov / high-entropy apparatus correctly applied? Rank-1 vs rank-2 premise. **Premise needs sharpening.**

- **The high-entropy method is intrinsically rank-≥2.** Literature: it "uses crucially leaf-wise measures
  for the coarse Lyapunov subgroups," and "when we have **two non-commuting coarse Lyapunov weights**, the
  theorem finds a unipotent invariance" (Einsiedler–Katok 2005; survey arXiv:2207.10132). For a **rank-1**
  action (the single `A=×3/2` we iterate) the high-entropy method **does not apply in standard form** — the
  rank-1 tool is the **low-entropy method** (Einsiedler–Lindenstrauss, *Rank-One case and the general
  Low-Entropy method*, JMD 2008). So the theorem's sharpened premise — "the method needs rank ≥ 2 **and**
  nonzero-exponent directions" — is **correct** and is the better statement than "neutral direction" alone.
  `[PROVEN-in-lit]`
- **But the rank-2 host IS available**, so the rank deficit is not the whole story. The AIU upgrade targets
  the rank-2 host `Φ=⟨×2,×3⟩`, which genuinely acts on the solenoid. Note `ℚ₃` **is** a coarse-Lyapunov
  subgroup of `Φ` with a *nonzero* weight (it is contracted by `M_3` and by `A`). So the high-entropy method
  *can* propagate Haar **along** the `ℚ₃` leaf — i.e. it can give **additive** translation-Haar of the
  `ℚ₃`-conditionals. What AIU needs is **multiplicative** `ℤ₃^*`-rotation invariance of those conditionals,
  and the operator supplying that surplus, `×2|_{ℚ₃}`, has **zero** weight. The neutrality is real and is
  the right pinpoint **for the surplus operator**, not for the leaf.
- **The decisive framing flaw.** The high-entropy method (and Rudolph–Johnson) are **classifiers of
  `Φ`-invariant measures** — they *presuppose* full rank-2 invariance and then conclude Haar. AIU is the
  step *upstream*: get from `A`-invariance **to** `Φ`-invariance. So the high-entropy method is a
  **consumer**, not a **producer**, of the invariance AIU needs; "trying the high-entropy method to supply
  AIU" is category-mismatched. The genuine *producer* candidate for central invariance is the Invariance
  Principle / isometric extension (§1) — which is the route that must be, and is (§4), separately closed.

**Net for Q2:** the rank-1-vs-rank-2 sharpening is right and improves the theorem; but the sharpest true
statement is "the high-entropy method is the wrong *kind* of tool (it consumes rank-2 invariance), and the
right *kind* of tool (Invariance Principle, a central-direction producer) is defeated by non-recurrence."

---

## 3. Q3 — Is "zero exponent ⟹ no entropy ⟹ no invariance" a valid step or too glib? **Valid as stated; do NOT strengthen.**

- **Entropy half is rigorously correct.** Ledrappier–Young: `h_μ = Σ λ_i⁺ · γ_i` over **positive** exponents
  only; "zero Lyapunov exponents contribute no entropy" (multiplicity-one center contributes none). So the
  neutral `×2|_{ℚ₃}` direction carries **zero leafwise entropy**. `[PROVEN-in-lit]` This is a *correct*
  premise.
- **The valid inference is narrow.** "Zero entropy on that direction ⟹ the **high-entropy method** has no
  entropy budget to spend there and no expansion to translate Haar along it" — **valid**, this is precisely
  the high-entropy mechanism (it spreads Haar across *expanding* coarse-Lyapunov directions). `[valid]`
- **The over-strong inference to avoid.** "Zero entropy on that direction ⟹ **no method** can derive
  invariance there" — **invalid / too glib**. The Invariance Principle derives invariance *because of* the
  zero exponent, not despite it (§1). So "no entropy ⟹ no invariance" is true **only relative to
  entropy-driven methods**; it is false as a universal. The theorem's proof step is sound **iff** it is
  read as a statement about the high-entropy method's *budget*, and must not be inflated to a universal
  no-go. The correct universal-level obstruction is supplied by **non-recurrence**, a separate fact (§4),
  not by the entropy count.

---

## 4. The fact that actually closes the central-direction route (must be cited by the theorem)

The Invariance-Principle / isometric-extension route (§1) is the real threat to a neutral-direction no-go,
and it is **defeated not by neutrality but by non-recurrence**, exactly as `AIU_SKEW_ROTATION.md §2.2`
shows `[PROVEN, repo]`:

- In coordinates `ℚ₃^* = 3^ℤ × ℤ₃^*`, `A(v,u) = (v+1, R_2^{-1}u)` is a skew product whose **base** is the
  radial coordinate `v=v_3` — the **A-contracting (dissipative)** direction, `|3/2|_3 = 1/3`. The base shift
  `v↦v+1` is a `ℤ`-translation: **no invariant probability, not uniquely ergodic, non-recurrent**. The
  Invariance Principle and Anzai–Furstenberg–Veech **require a finite invariant (recurrent) measure on the
  base**; that hypothesis **fails**.
- Equivalently: `A` maps each 3-adic sphere `{|y|_3 = 3^{-k}}` to the next and never returns, so the
  neutral rotation `R_2` is iterated **zero times per sphere** — its unique ergodicity is **inert**; the
  `n→∞` equidistribution is never triggered. The only recurrence is the renewal `Γ=ℤ[1/6]` cocycle, whose
  rotation-time is the 2-adic depth `D=v_2(3o−1)` — i.e. exactly the open (K)/Mahler-3/2 statistic.

**This is the load-bearing fact.** It is what genuinely closes the *central-direction* method that §1
exposes — and it lives in the **skew-rotation** note, not in the neutral-direction reasoning. The
neutral-direction theorem is incomplete without it.

---

## 5. PRECISE CORRECT FORM OF THE THEOREM

> **AIU host-invariance upgrade is unreachable by the standard measure-rigidity toolkit, for two distinct
> and individually necessary reasons.**
>
> **(A) The EL high-entropy method cannot supply it.** That method (i) is intrinsically **rank-≥2** and
> **consumes** rank-2 invariance to conclude Haar (Rudolph–Johnson; Einsiedler–Katok high-entropy), so it
> is downstream of, not a producer of, the `A`⟹`Φ` upgrade AIU is; and (ii) propagates invariance only
> along **nonzero-exponent coarse-Lyapunov subgroups**, whereas AIU's surplus operator `×2|_{ℚ₃}`
> (`|2|_3=1`) is **neutral / zero-exponent**, carrying **zero leafwise entropy** (Ledrappier–Young), so the
> method has neither budget nor expansion to act on it. `[PROVEN-in-lit + repo]`
>
> **(B) The dedicated central-direction method (Furstenberg–Ledrappier–Avila–Viana Invariance Principle /
> Anzai–Furstenberg–Veech isometric extension), which *does* manufacture invariance from zero central
> exponents, is also inapplicable — but for the orthogonal reason that its base-recurrence hypothesis
> fails**: in the AIU skew-product the base is the `A`-contracting, dissipative radial direction with no
> invariant probability, so the neutral rotation is iterated zero times and the principle is inert; the only
> recurrence is the renewal cocycle, whose rotation-time is the open (K) depth statistic `D`. `[PROVEN, repo]`
>
> **Caveat (mandatory).** Neutrality (zero Lyapunov exponent) **alone** is NOT an obstruction to measure
> rigidity — the Invariance Principle is a rigidity engine *for* neutral directions. The obstruction is the
> **conjunction**: the surplus invariance is (i) neutral (defeating entropy-driven methods, A) **and** (ii)
> supported only over a non-recurrent / dissipative base (defeating central-direction methods, B). A
> theorem asserting "neutral direction ⟹ no method" would be an **OVER-CLAIM**.

This is strictly the conjunction `AIU_JOININGS.md §3.3` **and** `AIU_SKEW_ROTATION.md §2.2`. The sibling
agent's theorem is sound **iff** it is stated as this conjunction; stated as the neutrality half alone it
over-claims.

---

## Sources

- A. Avila, M. Viana, J. Santamaria, *Invariance Principle*; M. Viana et al., Astérisque **358** (2013) 13–
  — center disintegration is holonomy-invariant when central exponents vanish; rigidity FROM zero exponents.
  numdam.org/item/AST_2013__358__13_0.pdf `[PROVEN-in-lit — the central-direction counter-method]`
- F. Ledrappier; H. Furstenberg — Invariance Principle origins (random matrix products / linear cocycles);
  *Invariance principle and rigidity of high entropy measures*, arXiv:1606.09429. `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case
  and the general low-entropy method*, JMD **2** (2008) 83–. (rank-1 ⇒ low-entropy method, not high-entropy)
  aimsciences.org/article/doi/10.3934/jmd.2008.2.83 `[PROVEN-in-lit]`
- M. Einsiedler, A. Katok, *Rigidity of measures — the high entropy case and non-commuting foliations*,
  Israel J. Math. (2005); survey *Joinings classification… [after Einsiedler–Lindenstrauss]*,
  arXiv:2207.10132 (high-entropy needs ≥2 non-commuting coarse-Lyapunov weights). `[PROVEN-in-lit]`
- L.-S. Young, F. Ledrappier, entropy formula `h_μ = Σ λ_i⁺ γ_i` (zero exponents contribute no entropy);
  *Entropy, Lyapunov exponents, and rigidity of group actions*, arXiv:1809.09192. `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  arXiv:2101.11120 (Rudolph–Johnson on solenoids — consumes rank-2 invariance). `[PROVEN-in-lit]`
- S. Anzai (1951); H. Furstenberg (1961, strict ergodicity); W. Veech (1969) — isometric-extension /
  uniquely-ergodic skew products require a probability-preserving base. `[PROVEN-in-lit]`
- Repo: `AIU_JOININGS.md` (§3.3 neutral-direction / no-entropy-leverage), `AIU_SKEW_ROTATION.md`
  (§2.2 dissipative non-recurrent base kills isometric extension — the load-bearing closure of route B),
  `NEWMATH_ADELIC_RIGIDITY.md` (§2 AIU, §3.3 T1–T2), `ADELIC_COUPLING.md` (`v_3=D−1`, Mahler-3/2 = (K)).

No machine decided. No label upgraded.
