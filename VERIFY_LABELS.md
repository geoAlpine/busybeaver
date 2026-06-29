# VERIFY_LABELS.md — adversarial [PROVEN]-label audit of the carry / 2nd-diagonal / odd-subspace / E[K²] / magnitude cluster (2026-06-30)

*Task: hunt for the 24th over-claim. For every [PROVEN] label in the 18+1 named notes decide:
[confirmed-PROVEN] / [should-be-OBSERVED] / [should-be-CONJECTURE] / [CIRCULAR] / [PROVEN-in-lit-recite].
Numerics: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, scratchpad `verify_labels.py`, `verify_coiso.py`, `verify_lann.py`, N≤2·10⁵, <60s. No commit.*

---

## 0. Bottom line

**The cluster is SOUND. No [PROVEN] label was found to be a disguised proof of the kernel, a circular
assumption of (K), or an upgraded numeric.** Every [PROVEN] tag in these notes attaches to one of three
honest categories: (i) an **exact arithmetic/algebraic identity** (machine-verified, big-int), (ii) a
**structural operator fact** (coisometry, L_ann annihilation, coupling closed form, coboundary/sign-tension
no-go), or (iii) a **PROVEN-in-lit recitation** (Erdős–Salem Rajchman, Varjú–Yu rate, Spiegelhofer–Wallner
longest-run, the valuation budget). Every *asymptotic/limit* statement (Inj_a→0, M₂ᵒᵈᵈ=o(2ᵏ), energy
ratio→½, E[K²]<∞, μ({1})=0, equidistribution) is consistently carried as **[OBSERVED]** or
**[OPEN]/[CONJECTURE]**. The self-catching discipline ("circular escape routes" flagged as circular by the
authors themselves; the longest-run route retracted in EK2_PARTIAL_MOMENTS; E[K]<∞-in-limit downgraded to
the open even-density) is intact. **No 24th over-claim located.** Three *soft* concerns (framing, not label
errors) are listed in §3.

---

## 1. Numeric spot-checks (all PASS)

| claim | source | result |
|---|---|---|
| `2ⁿcₙ+Sₙ=8·3ⁿ`, `S_{n+1}=3Sₙ+2ⁿbₙ`, `βₙ=bit_{n+k}(8·3ⁿ−Sₙ)` | ODD_3ADIC/CARRY_* | **0 failures**, n<4000, k∈{2,5,9} |
| seam `Sₙ≡8·3ⁿ (mod 2ⁿ)` (borrow_n=0) | CARRY_COBOUNDARY §1a | **0 failures** |
| ΣK² telescope `ΣK²=2Σd−#{d≥1}+(d_N²−d_0²)` and `Σd=½(ΣK²+ΣK)` | EK2_SECOND_BUDGET | **exact match** (N=2·10⁵, d_N=0): ΣK²=297625=297625; Σd=198794=198794 |
| mean depth, ΣK²/N, freq{d≥k} | EK2/NONATOMIC | mean depth 0.9940, ΣK²/N=1.4881, maxK=20, freq{d≥k}=0.50,0.25,0.124,0.061,…≈2⁻ᵏ ✓ |
| E[D], E[D²], freq(D=1), D=1 drift exact (o₀=27) | MAGNITUDE/ADELIC | **E[D]=2.0007, E[D²]=6.0035, freq(D=1)=0.49948**; `(o′−1)/(o−1)≡3/2` exact on all D=1 steps |
| 3-place D=1 drift `(log3/2,log2,−log3)` sums to 0 | ADELIC_SUBACTION §1b | sum = −2.2e−16 ✓ |
| `α*=(1/3)Σbⱼ(2/3)ʲ` | TWO_DIAGONAL §1a | **0.135822737943** (matches claimed value to all digits) |
| **R_k coisometry**: `R_kR_k*=I`, all σ=1, dim ker=2^{k−1} | NEWMATH_ODD_CALCULUS §2.1 | **CONFIRMED** k=2..6: ‖R_kR_k*−I‖≤4.8e−15, σ∈[1.0000,1.0000], ker dim = 2,4,8,16,32 = 2^{k−1} ✓ |
| `L_ann χ_a≡0` (odd a); C1 `U(s,1)=U(s,0)+2^{k−1}` | ENDOGENOUS_UE_BUILD C1/C2 | C1 exact; **max_{a odd}‖L_ann χ_a‖_∞ ≤ 1e−13**, k=2..8 ✓ |
| annealed Weyl tail const `C_{k,1}` | SECOND_DIAGONAL_RAJCHMAN §1 | **0.7748, 0.9847, 0.999** (k=0,2,4) — exact match ✓ |

All load-bearing numerics named in the task reproduce. The coisometry — the strongest single structural
claim in the cluster — is genuine: R_k (2^{k−1}×2^k) has every singular value exactly 1 and a kernel of
exactly half the source dimension.

---

## 2. Per-note [PROVEN]-label verdicts

| note | the [PROVEN] claims | verdict |
|---|---|---|
| CARRY_COBOUNDARY | borrow decomp `β=d⊕σ⊕ρ`; finite-range borrow lemma; no-telescope (√N partial sums) | **confirmed-PROVEN** (identities verified; √N-growth is a correct disproof of "bounded coboundary") |
| CARRY_BOUNDED_MEMORY | `d*(k)=1.71k+2.7` threshold; unbounded memory `m(k)=n−O(k)`; `Sₙ mod 3ᵐ` exact m-memory | **confirmed-PROVEN** (exact/structural); flip-sensitivity is [OBSERVED] and so labelled |
| CARRY_EXOGENIZATION | exact split `Inj=Inj^{exo}+Inj^{carry}`, identity 0 failures | **confirmed-PROVEN** (identity); annealed-indistinguishability correctly [OBSERVED] |
| SECOND_DIAGONAL_RAJCHMAN | annealed Weyl = ν̂_{2/3}(ξₙ) identity; ξₙ→∞ ⇒ Rajchman ⇒ →0 | identity **confirmed-PROVEN**; the decay step is **PROVEN-in-lit-recite** (Erdős–Salem + Varjú–Yu, cited inline — acceptable) |
| SECOND_DIAGONAL_COCYCLE | predictability `σₙ∈F_{n−1}`; injection below read; degenerate-RWRS | **confirmed-PROVEN** (structural; `corr(σ,bₙ)≈0` is [OBSERVED] and so marked) |
| TWO_DIAGONAL_COMPARISON | `cₙ=Hₙ−Gₙ`; `Gₙ=⌊α*(3/2)ⁿ⌋`; both diagonals = AEV digit `bit_k⌊α(3/2)ⁿ⌋` | **confirmed-PROVEN** (α* verified; independence corr≈0 is [OBSERVED]) |
| ODD_SUBSPACE_SYNTHESIS | unification `β=bit_{n+k}(8·3ⁿ−Sₙ)`; 100%-odd; sign-aware framing | **confirmed-PROVEN** (algebraic identities) |
| ODD_3ADIC_ODOMETER | rewrite; fixed-position periodicity (rational Cesàro mean); diagonal=Mahler | **confirmed-PROVEN** (Inj_a≤CLT floor is [OBSERVED] and so marked) |
| ODD_AUTOMATON_ALGEBRA | coupling closed form `m_{b,a}`; v₂(b)=1 pair rule; no-coboundary (fixed point s=0, cycle-sum 1≠0); half-dim | **confirmed-PROVEN** (machine-verified k=2..7; cohomology argument sound) |
| ODD_ADDITIVE_ENERGY | `M₂ᵒᵈᵈ=2ᵏC₂(k)−2^{k−1}C₂(k−1)`; `avgjump=1+(2/J)Σεₖ`, εₖ pure-odd; only free ineq `M₂ᵒᵈᵈ≥0` | **confirmed-PROVEN** (exact Parseval identities); `M₂ᵒᵈᵈ=o(2ᵏ)` correctly [OPEN] |
| ODD_TWO_DESCRIPTION | (C3) `Sₙ≡8·3ⁿ mod 2^{k+1}`; (C4) parity-blindness; (C5) Mahler×carry split | **confirmed-PROVEN** (exact, verified to 1e-15) |
| EK2_SECOND_BUDGET | four telescopes incl. `ΣK²=2Σd−#{d≥1}+bdry`; self-closure 0=0 | **confirmed-PROVEN** (reproduced exactly) |
| EK2_TAIL_SEPARATION | countdown forces min-gap=1; "separation cannot bound occupancy tail" | **confirmed-PROVEN** — correctly scoped to *these tools*, not "no proof exists" |
| EK2_PARTIAL_MOMENTS | no fractional moment from support/count; longest-run route does NOT apply to orbit; E[K]<∞-in-limit ⟹ even-density>0 (open) | **confirmed-PROVEN** + a self-correction (a *downgrade*, not an over-claim) |
| MAGNITUDE_LYAPUNOV | size-drift identity; sign-tension theorem; per-step failure for o>M0; orbit grows | **confirmed-PROVEN** (sub-action theory + verified drift) |
| ADELIC_SUBACTION | 3-place D=1 drift sums to 0; product-formula closes sign tension (α₃≥0 & α∞log(3/2)≥α₃log3 ⟹ α∞≥0) | **confirmed-PROVEN** (drift verified; LP argument sound) |
| NONATOMIC_FIXEDPOINT | countdown; mean-depth identity `Σd=Σfₖ`; reduction `μ({1})=0⟸E[K²]<∞` | **confirmed-PROVEN** (reduction is an implication, not an assumption of (K)) |
| ENDOGENOUS_UE_BUILD | C1/C2 (`L_ann χ_odd≡0`); seam identity C4; no-go (gap blind + adversary); escape routes circular | **confirmed-PROVEN** (C2 verified 1e-13; circularity is correctly *attributed* to the escape routes, not committed by the note) |
| NEWMATH_ODD_CALCULUS | semiconjugacy; exact `d^{(k)}=R_k d^{(k+1)}`; pure odd→odd; **coisometry**; ker dim; op-norm Lyapunov≡0 | **confirmed-PROVEN** (coisometry verified to 1e-15); (CR) correctly **[CONJECTURE]** — see §3.1 |

**Count: ~70 distinct [PROVEN] assertions audited across 19 notes. Confirmed-PROVEN: all except the
Rajchman-decay step (PROVEN-in-lit-recite, properly cited). 0 should-be-OBSERVED. 0 should-be-CONJECTURE.
0 CIRCULAR.**

---

## 3. Soft concerns (framing, NOT label errors)

**3.1 NEWMATH_ODD_CALCULUS §0 — "clean reduction of (K)" adjacent to "[PROVEN]".** The §0 one-liner places
"a sharp [PROVEN] structure theorem and a clean reduction of (K)" in one breath. The reduction itself,
(CR)⟹(K), is *not* in the [PROVEN] inventory — §4 correctly files it under **[CONJECTURE CR / OPEN]** and §3
calls it "[NEW THEOREM TO BUILD]". I add: the §3 reduction argument is in fact only **heuristic** — it
combines the scale limit m→∞ with empirical vectors `d^{(k+m)}` at *fixed* N, and uses the very loose trivial
bound `‖d^{(k+m)}‖²≤2^{k+m−1}`; at fixed N the data is meaningful only to k≈log₂N, so the m→∞ step is
degenerate. This does not contradict any label (the conclusion is openly [CONJECTURE]), but the §0 wording
slightly oversells. **Verdict: label correct, prose optimistic.**

**3.2 CARRY_COBOUNDARY vs CARRY_EXOGENIZATION / TWO_DIAGONAL — apparent tension on "is the carry
negligible".** COBOUNDARY §0/§3 say the carry "contributes at full order, not negligible; carry piece ≳
Mahler piece, dominates at k=5,6." EXOGENIZATION §2/§4 and TWO_DIAGONAL §2c say the carry is
"annealed-indistinguishable, net contribution to Inj_a ≈ 0." These are **reconcilable, not contradictory**:
the carry-piece *self-energy* is large (0.45–0.56·floor) but is cancelled by a negative cross-term
(−0.38…−0.52) that an iid carry reproduces identically — so |carry piece| is large while (carry piece +
cross) ≈ 0. Both notes carry these as **[OBSERVED]**. COBOUNDARY's separate headline [PROVEN no-telescope]
(√N partial sums) is about the carry piece *not being a bounded coboundary*, which is independent and
correct. **Verdict: no label error; COBOUNDARY's one-line framing overstates "not negligible" relative to
the net-≈0 finding, worth a cross-reference.**

**3.3 "[PROVEN reduction]" tag is non-standard.** Many notes tag "(c) reduces to (K)" as [PROVEN reduction].
In every audited case this denotes a *proven identification* of the residual object with a known-open
problem (e.g. σₙ = `bit_k⌊α*(3/2)ⁿ⌋`, an AEV digit — verified), **not** a proof of any theorem and **not** an
assumption of (K). It is sound and non-circular, but the word "PROVEN" attached to "reduction" could mislead
a skimming reader into thinking something was decided. **Verdict: cosmetic.**

---

## 4. Checks specifically requested

- **Coisometry (R_k unitary/coisometry):** CONFIRMED numerically, k=2..6 — `R_kR_k*=I` to ≤4.8e−15, all
  singular values exactly 1, dim ker R_k = 2^{k−1}. Genuine [PROVEN].
- **Telescoping self-closure (ΣK² identity):** CONFIRMED exact at N=2·10⁵ (d_N=0): both `ΣK²=2Σd−#{d≥1}` and
  `Σd=½(ΣK²+ΣK)` hold to the integer. The "closes on itself = 0=0" reasoning is correct; the note rightly
  concludes it carries no second-moment information.
- **Finite-range borrow lemma (ρₙ reads k-bit window):** the enabling seam `Sₙ≡8·3ⁿ (mod 2ⁿ)` verified 0
  failures; lemma is genuine [PROVEN].
- **L_ann annihilates odd characters:** CONFIRMED, max_{a odd}‖L_ann χ_a‖_∞ ≤ 1e−13, k=2..8. Genuine [PROVEN].
- **Magnitude-Lyapunov sign tension + adelic product-formula no-go:** the D=1 three-place drift
  `(log3/2,log2,−log3)` sums to 0 exactly; the LP closure (α₃≥0 & α∞log(3/2)≥α₃log3 ⟹ α∞≥0 vs useful α∞<0)
  is internally valid. Genuine [PROVEN] no-go, correctly scoped to magnitude-aware sub-actions.

No NO-GO in the cluster is stated more broadly than proven: each ("separation can't bound the tail",
"no telescoping", "no adelic escape", "gap blind to odd block") is explicitly scoped to a named tool/route
and backed by either an exact identity or an adversarial witness with identical structural data.

---

## 5. Verdict

The carry / second-diagonal / odd-subspace / E[K²] / magnitude cluster is **clean**. Suspect [PROVEN]
labels: **0** (one is a properly-cited PROVEN-in-lit recitation; one reduction is openly [CONJECTURE] with
optimistic surrounding prose). No circular reduction. No NO-GO over-stated. All named numeric spot-checks
reproduce exactly. The program's ~23 self-caught over-claims appear to have exhausted the supply within this
cluster; the 24th was not found here.

No machine decided. No label upgraded.
