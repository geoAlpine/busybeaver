# The new-mathematics program for Antihydra / Mahler 3/2 — a research-program specification (2026-06-30)

*A precise specification of the new mathematics that a proof of `(K)` (= Mahler 3/2 / AEV Conj 1.6 = Antihydra
non-halting) requires — NOT a proof, and not a claim that one is imminent. `(K)` is a generational open problem; this
session **proved** the attack landscape closed in every register and that no sub-`(K)` problem or un-pre-empted route
remains, so the only honest forward path is to *develop the missing tool as a multi-year research program*. This document
assembles that program from the corpus: the foundations in hand (`NEWMATH_FOUNDATIONS.md`), the spec sharpened by every
no-go (`NEWMATH_SPEC_SHARPENED.md`), and the home theory + roadmap (`NEWMATH_ROADMAP.md`). SOUNDNESS: foundations
[PROVEN]; targets [CONJECTURE]; directions [PROGRAM]; no label upgraded. NOT committed by default.*

---

## 1. The central new object (the precise target)

> **Effective unique ergodicity for a single *specified* orbit of a rank-1, amenable, hyperbolic action on the
> (2,3)-adic solenoid** `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` — i.e. force the seed-`8` orbit of `A=×(3/2)=M_3M_2^{-1}` to be generic
> for Haar — by controlling the surplus host-invariance along the **neutral, zero-Lyapunov** coarse direction (`×2` on
> `ℚ₃`) via an **a-priori excursion / return-time estimate** that is **non-spectral** (forced by the coisometry no-go)
> and **non-structural** (forced by the No-Structure theorem), yet **uniform over the specified orbit** rather than
> a.e./annealed.

Equivalently in arithmetic terms: an a-priori bound on the second moment / tail of the depth-jumps `K_i=v₂(3c_i−1)`
(the moving-middle Mahler digits) that excludes the heavy-tailed, white, first-moment-matched adversary — i.e. a
**count→energy bridge** = power-saving on the quenched Weyl sum `(1/N)Σ e(t(3/2)ⁿ)`.

## 2. The foundations in hand [PROVEN] (`NEWMATH_FOUNDATIONS.md`)

The tool does **not** start from zero; it gets to use:
- **Reduction scaffold:** halt ⟺ even-density ≥ 1/3 ⟺ mean `D ≥ 3/2` ⟺ single-orbit equidist of `c_n mod 2^k`; the
  induced map `T(o)=3^{D−1}(3o−1)/2^D`, `o₀=27`; the exact seam identity; the carry split `β_n=d_n⊕σ_n⊕ρ_n`.
- **The candidate engine:** the 2-adic Lyapunov potential `V=v₂(c−1)` (countdown drift `−1`) and the **Dual-Repulsion**
  (`×3/2` archimedean, `×2` 2-adic, `×3` odd-part) — the one structure every un-pre-empted route runs on.
- **The external bridge:** the solenoid host `⟨×2,×3⟩` realization, the `ℤ²` shift symmetry, the exact coupling
  `v₃(o')=D−1`, and **proven Rudolph–Johnson** as the finisher (needs AIU + ENT).
- **The annealed/renorm layer:** `T` exact-Bernoulli (measure side complete); annealed gap (`λ₂`; transducer gap ½);
  non-Pisot ⇒ no atomic/sofic fixed point; `dim ν_{2/3}=1`, Rajchman/Varjú–Yu.
- **The banked partials:** `#even ≥ 0.89 log n`, foothold `~0.85 log₂N`, valuation budget, subword `≥1.71ℓ`, FLP, Vaaler.
- **Proven no-gos as structural facts** the proof shape must respect (see §3).

## 3. What the tool must do and must not be — the spec by negation [PROVEN no-gos] (`NEWMATH_SPEC_SHARPENED.md`)

Seven constraints, each a closed route turned into a requirement:
1. **Non-spectral** — `L_ann χ_odd ≡ 0`; control the odd-character block `V_odd` without the spectral gap.
2. **Haar-selecting (orbit-arithmetic)** — `β(ψ)=+½` + specification ⇒ closure/first-moment/annealed data is constant on
   `M_feas`; the tool must use seed-specific arithmetic.
3. **Not a sub-action/coboundary** (bounded, magnitude-aware, or adelic) — the sign-tension + product-formula lock.
4. **Excursion-level, not per-step** — the per-step feedback is white; act on return-times / multi-scale.
5. **Reads the magnitudes, not the depth** — every `σ(d_n)` potential self-closes to `0=0`; the relevant functional is
   `~K²` (the hidden lower 2-adic / moving-middle digits).
6. **A-priori, breaking the circularity** — the conditional return-time law *is* `E[K²]` *is* the occupancy *is* `(K)`;
   the estimate must exclude the heavy-tailed adversary **without** assuming the D-law.
7. **Central-direction mechanism** — AIU's surplus invariance is along a neutral, zero-Lyapunov direction, blind to the
   high-entropy (EKL) / unique-ergodicity / Host machinery.

## 4. The home theory and the two build-targets (`NEWMATH_ROADMAP.md`)

**Most plausible home:** the **Einsiedler–Lindenstrauss leafwise-measure / adelic Ledrappier–Young program on solenoids**
(the apparatus around arXiv:2101.11120, finished by proven Rudolph–Johnson). The object lives there natively; the new
tool would be a **low-entropy / neutral-direction extension of the high-entropy method**.

The two equivalent build-targets (same wall, two languages):
- **(I) AIU — neutral-direction host-invariance.** Prove the `A`-stable `ℚ₃`-leaf conditionals are spherically Haar
  (`(×2)_*μ=μ`) by a mechanism converting non-atomicity into rotation-invariance along the zero-Lyapunov `×2|_{ℚ₃}`
  axis — *without* entropy / unique-ergodicity / joinings (all proven inert there).
- **(II) ENT — a-priori excursion estimate.** Prove `h_μ(M₂)>0` ⟺ `E[K²]<∞` ⟺ `Σ v₂(c_n−1)=O(N)` ⟺ `μ({1})=0` from
  the orbit's specific 2-adic arithmetic, excluding the heavy-tailed adversary.

## 5. Ranked research roadmap (honest; all (K)-hard to complete)

| # | sub-problem | nearest precedent | what it needs | first publishable partial |
|---|---|---|---|---|
| (a) | **AIU** (host-invariance, neutral dir.) | Host 1995 / EKL high-entropy | a central-coarse-direction invariance-upgrade mechanism | **the neutral-direction obstruction theorem** (high-entropy method is structurally blind to a central Lyapunov direction) — *the strongest near-term partial* |
| (b) | **ENT** (`h_μ(M₂)>0`, one number) | Pesin–Ledrappier–Young / Hochman | a count→energy bridge for the quenched orbit | the L–Y collapse `ENT ⟺ γ>0`; the proven excursion no-go |
| (c) | **EUE** (endogenous cocycle, `Inj→0`) | (T,T⁻¹)/RWRS (which abandons UE) | non-spectral odd-block control past the coisometry | the exact seam identity + coisometry no-go |
| (d) | **rank-1 amenable effective equidistribution** | BFLM (non-abelian), effective Ratner (unipotent) | the whole missing theory (empty-toolbox) | generational |

**First publishable contribution:** the **AIU neutral-direction obstruction theorem** — a clean statement that the
high-entropy rigidity method cannot reach a central (zero-Lyapunov) coarse direction, with the leafwise reduction and the
conditional `AIU ∧ ENT ⟹ (K)` chain. This is a genuine, self-contained result about the *limits* of measure rigidity,
publishable independently of `(K)`.

## 6. Durable intermediate outputs (stand regardless of `(K)`)

The machine-verified **reduction-chain framework** (`BB6_FRAMEWORK_PACKAGE.md`); the **No-Structure-Only-Selection theorem**;
the **obstruction dichotomy** (topological-closure vs Haar-selecting; mirror 2-adic/3-adic first-vs-second-moment); the
**solenoid placement** (AIU + ENT via proven Rudolph–Johnson); the **coisometry no-go + exact seam identity**; the
**banked unconditional partials**; and the **cross-field empty-toolbox verdict** (~19 fields + 2 probes). These are the
publishable artifacts now.

## 7. Honest timeline

`(K)` is generational; the full program is multi-year and its completion equals solving Mahler 3/2 / AEV. The program's
*value now* is (i) the durable outputs of §6, (ii) the precise spec of the missing tool (§1–§4) for the
homogeneous-dynamics / aperiodic-order / numeration communities, and (iii) the AIU neutral-direction obstruction theorem
as a first self-contained partial. The right immediate action is **external** — take §1–§6 to the
Einsiedler–Lindenstrauss–Host circle and the AEV authors — not further internal attack (proven futile).

**No machine decided. No label upgraded.** `(K)` remains [OPEN] = Mahler 3/2 / AEV.

---

## 8. Long-haul charter (2026-06-30): the multi-year build, with the corrected frontier

*Added when the decision was made to treat this as a serious multi-year program ("腰を据えて新しい数学を作り、Busy
Beaver に挑む"). This section is the durable backbone a future session or external collaborator picks up.*

### 8.1 The single central target (corrected, precise)
> Build a tool that yields a **one-sided positive-density lower bound for the moving-diagonal binary digit of `3ⁿ`**
> (equivalently `liminf #even(n)/n ≥ 1/3` for the seed-8 orbit; equivalently single-specified-orbit quenched
> genericity for the 2-adic Bernoulli map `T`, `o_0=27`). NOTE the `DEPTH_REACH_CLARIFICATION.md` correction: the
> target is a **digit-frequency** statement, NOT an empirical-equidistribution-depth statement (the latter is
> counting-capped at `log₂N` and irrelevant).

### 8.2 What is proven-CLOSED (the backdrop the tool must respect) `[PROVEN]`
- No structure-only certificate (No-Structure thm, `BB6_NO_STRUCTURE_THEOREM.md`): (C1) bounded coboundary, (C2)
  all-orbits/topological, (C3) measure-level all fail (δ₁ maximizer β=+½).
- No decider (`DECIDER_PREEMPTION.md`): Kind-R regular = (C2) kill `[PROVEN]`; Kind-W (WFA) = (C1) `[ARGUED]`. This
  **explains the empirical Cryptid status** via the No-Structure theorem.
- The (a)(b)(c)(d) no-gos + the whole fixed-point family (`FIXEDPOINT_COUPLING_PROBE.md`) + non-escape/Margulis +
  Tao/Syracuse (a.e.) + every cross-field probe — all collapse to the same wall.
- The tool must be: **non-spectral** (L_ann odd-blind), **non-structural** (No-Structure), **quenched/seed-specific**
  (not a.e./annealed), **digit-frequency** (not equidistribution-depth), and **a-priori** (not assuming the D-law).

### 8.3 The milestone ladder (honest intermediate targets between known and `(K)`)
Each rung is a genuine unconditional result strictly stronger than the last; `(K)` is the top.
1. `[PROVEN]` `#even(n) ≥ 0.89 log n` (current best, `LIMIT_THEOREM.md`).
2. `[OPEN, near-frontier]` `#even(n) ≥ (log n)^{1+ε}` or `≥ exp(c√log n)` — **first genuine new rung**; any
   super-logarithmic unconditional bound on the moving-diagonal digit of `3ⁿ` would be publishable and new.
3. `[OPEN]` `#even(n) ≥ n^{c}` for some `c∈(0,1)` — a polynomial (still sub-linear) density; would be a major result.
4. `[OPEN]` `#even(n) ≥ εn` for some `ε>0` (positive density, one cell) — at this point essentially `(K)`-grade.
5. `[OPEN = (K)]` `liminf #even(n)/n ≥ 1/3`.
> Rungs 2–4 are the **measurable progress** a multi-year program should target; none is known, and even rung 2 is at
> the current research frontier (no unconditional positive-rate digit bound for `3ⁿ` exists).

### 8.4 Two-track plan
- **Track A (internal, partial rungs):** attack rung 2 — a super-logarithmic unconditional `#even` bound — via the
  proven 2-adic potential `V=v₂(c−1)` + the exact growth `bitlen(c_n)=0.585n+O(1)` + integrality, searching for an
  argument that the carry cannot suppress the even-count below super-log. This is the one place a new *positive*
  theorem might live without solving `(K)`.
- **Track B (external, the tool):** take the corrected central target (§8.1) + the proven-closed backdrop (§8.2) +
  the sharp question (log-vs-linear is a digit-frequency gap) to the Einsiedler–Lindenstrauss–Host circle, the AEV
  authors, and the Lee–Palvannan ergodic-skew-product circle. The framework package (`BB6_FRAMEWORK_PACKAGE.md`) +
  Coverage No-Go + decider-preemption are the outreach artifacts.

### 8.5 Connection to Busy Beaver
`(K)` true `⟹` Antihydra never halts `⟹` one BB(6) Cryptid resolved. BB(5)=47,176,870 is proven (Coq, 2024); BB(6)'s
lower bound is `Σ(6) > 2↑↑↑5` (mxdys, Jun 2025) and its *exact determination* is gated on resolving the Cryptids,
Antihydra among them. So this program's completion is one necessary step toward pinning BB(6). The honest framing for
any audience: **we have reduced one BB(6) Cryptid to a sharp, classical, generational number-theory frontier (Mahler
3/2 / AEV) and mapped exactly why every existing tool fails; building the missing tool is the multi-year goal.**

**No machine decided. No label upgraded.** `(K)` remains [OPEN] = Mahler 3/2 / AEV.
