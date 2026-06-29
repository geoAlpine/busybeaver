# VERIFY_NEWMATH.md — adversarial verification of the new-math + AIU/ENT + reduction cluster (2026-06-30)

*Adversarial pass: FIND ERRORS, not confirm. Findings labelled
[OK]/[OVER-CLAIM]/[INCONSISTENCY]/[CIRCULAR]/[NUMERIC-SUSPECT].
Ground-truth numerics re-verified this pass with `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(N=10^5, exact big-int, <2s): v3(o')=D-1 **0 fail**; unit(o')=(-1)^{D+1} mod 3 **0 fail**;
E[D]=2.0007, E[D^2]=6.004, E[D-1]=1.001; subword p(l)=2^l **FULL** through every resolvable l
(2^11 at M=2e4 windows; 2^13 at N=1e5 residues) -> block entropy log2. No master numeric is contradicted by data.*

---

## SUMMARY

Two genuine in-scope over-claims/inconsistencies survive (both are leftover, un-propagated corrections),
plus one in the foundational referenced note `AIU_ATTACK.md`, plus two minor slips. The AIU and ENT notes
are otherwise mutually consistent and honestly labelled ([CONJECTURE] central conjectures; reductions
valid, non-circular). Most important fix: **NEWMATH_SYNTHESIS §2 still contains the retracted
zero-entropy/Furstenberg-corner claim**, contradicting its own §0 correction, LIMIT_MEASURE_ENTROPY, and
the measured full complexity.

---

## FINDINGS TABLE

| # | claim / location | status | fix |
|---|---|---|---|
| **F1** | `NEWMATH_SYNTHESIS.md` §2 "The catch [honest]", lines 76-80: *"A single orbit's empirical limit measure is plausibly **zero-entropy** (the orbit's subword complexity is only linear, p(l)≥1.71l, topological entropy 0). In the zero-entropy regime, ×2,×3-invariance does not force Haar — that is exactly Furstenberg's conjecture … framework (I) reframes (K) as a Furstenberg-×2,×3-type rigidity statement **in the zero-entropy regime**."* | **[INCONSISTENCY] + [NUMERIC-SUSPECT]** | This is the **retracted** claim, un-propagated. It contradicts (a) the SAME file's §0 SOUNDNESS CORRECTION (lines 17-25) and §3/§4 corrected text; (b) `LIMIT_MEASURE_ENTROPY` §0-§3 + ledger ("zero entropy is the (K)-FALSE regime", "Furstenberg corner is a misframing"); (c) master numerics p(l)=2^l FULL, h_top=log2 — so "topological entropy 0" is false. Rewrite §2 to the corrected statement: positive entropy is the (K)-true regime; the gap is {AIU ∧ h_μ(M₂)>0} via *proven* Rudolph–Johnson; zero-entropy = (K)-false, not a Furstenberg corner. NB `LIMIT_MEASURE_ENTROPY` §3 flagged "§0/§4" as the misleading spot, but the surviving leftover is **§2**. |
| **F2** | `ENT_PRESSURE_LY.md` §0 line 20 ("…even **global non-atomicity**…") and §3 table line 83: *"**global** non-atomicity of μ **(PROVEN, 2-adic repulsion)**"* | **[OVER-CLAIM] + [INCONSISTENCY]** | Reproduces the exact retracted phrasing ("non-atomic [PROVEN] via 2-adic repulsion"). Contradicts the authoritative `ENT_NONATOMIC.md` (non-atomicity = **OPEN**, verdict (b)), `LIMIT_MEASURE_ENTROPY` ledger ("μ non-atomic **[OPEN]** — CORRECTED from an earlier [PROVEN] over-claim"), and `NEWMATH_ADELIC_RIGIDITY` §2 item 3. Fix: demote to "global non-atomicity (OPEN; only per-visit periodic-avoidance is PROVEN)". The §3 logical *point* (non-atomic ⇏ non-atomic conditionals) is unaffected; only the PROVEN label is wrong. |
| **F3** | `AIU_ATTACK.md` §3.2 (lines ~97-99) and verdict table line 145: *"μ is non-atomic **[PROVEN, 2-adic repulsion, REPELLER_ESCAPE]**"* | **[OVER-CLAIM]** (out of stated 15-file scope, but it is the foundational AIU note that NEWMATH_ADELIC_RIGIDITY §2 and AIU_SEED_SHIFT cite as authority) | Same retracted claim. Its "AIU ⟹ μ non-atomic [PROVEN] ⟹ then need {h_μ>0 ∨ Furstenberg}" makes the Furstenberg branch look like 2 inputs when (per LIMIT_MEASURE_ENTROPY §3) it is now **3** (AIU, non-atomicity, Furstenberg). Fix: relabel non-atomic [OPEN]; the main RJ branch (h_μ>0 ⟹ non-atomic) is unaffected. |
| M1 | `ENT_PRESSURE_LY.md` line 67 calls "D_j=v2(3c'_j-1) geometric(½), entropy 2 bits" (E[D]=2 convention) but line 105 reports "E[D]=0.9937 (≈1) … geometric(½): E=1"; `ENT_HOCHMAN` line 114 "E[D]=0.994". | **[INCONSISTENCY] minor (notational)** | Same symbol "D" used for the depth v2(3o-1) (E≈2, the corpus/master convention E[D]=2.001) and for the renewal jump = D-1 (E≈1). H(D)≈2 is convention-invariant so no soundness impact. Disambiguate the symbol. |
| M2 | `ENT_PESIN_MARGULIS.md` §2.3 line ~106 attributes the "archimedean place is a transported copy of the 2-adic information" to "(T2) of NEWMATH_ADELIC_RIGIDITY §3.3". | **[INCONSISTENCY] minor (cross-ref)** | In ADELIC_RIGIDITY §3.3, **(T2)** is "3-adic place = invertible time-shift of the 2-adic" (v3=D-1); the archimedean↔2-adic mean lock is **(T1)**. Mislabel only; the structural point stands. |

---

## TARGETED CHECKS REQUESTED BY THE BRIEF

**1. "Two gaps, not one" (AIU + ENT).** Consistently corrected in `NEWMATH_ADELIC_RIGIDITY` (§3.2, §Honest
status), `LIMIT_MEASURE_ENTROPY` (§0,§3, ledger), and `NEWMATH_SYNTHESIS` §0/§1/§3/§4. **No leftover "AIU is
the only gap"** and **no leftover "[PROVEN] dichotomy Φ-inv⟹Haar"** — both explicitly [RETRACTED]/[WITHDRAWN]
(ADELIC §3.2, SYNTHESIS §1, §3). **EXCEPT** the SYNTHESIS §2 "catch" (F1), which reverts to the old
single-gap/zero-entropy framing. [OK except F1]

**2. Non-atomicity status.** Should be OPEN everywhere. It is OPEN in `ENT_NONATOMIC`,
`LIMIT_MEASURE_ENTROPY` (ledger + §3), `NEWMATH_ADELIC_RIGIDITY` §2 item 3, `AIU_JOININGS`/`ENT_PESIN_MARGULIS`
(which build the atomic counterexample). **Leftover [PROVEN] non-atomic survives in `ENT_PRESSURE_LY` (F2)
and `AIU_ATTACK` (F3).** Note `AIU_JOININGS` §3.1 "[PROVEN-in-lit] μ_x³ non-atomic" is a *conditional*
(leafwise) statement equivalent to ENT, correctly labelled — not the global-non-atomic over-claim.

**3. Zero-entropy retraction.** Corrected "positive entropy = (K)-true regime, zero-entropy = (K)-false" is
consistent in `LIMIT_MEASURE_ENTROPY` and all ENT notes. **Leftover "Furstenberg zero-entropy corner / plausibly
zero-entropy" survives only in SYNTHESIS §2 (F1).** [OK except F1]

**4. AIU notes mutual consistency.** Consistent and each correctly labelled:
   - `AIU_SKEW_ROTATION`: A is a skew product A(v,u)=(v+1, R_2⁻¹u) over a **dissipative** base (radial v=v3, the
     A-contraction), so unique ergodicity of the fiber rotation R_2 is **inert** — [PROVEN obstruction]; reduces to (K).
   - `AIU_THREEADIC_FOURIER`: angle is D-slaved, raw orbit unit part non-Haar (S_χ|m=1 = freq(D odd)-freq(D even) ≈ 1/3) —
     [PROVEN identity + OBSERVED]; "orbit-level AIU-3adic" DISPROVEN, ambient AIU untouched. Matches master
     unit(o')=(-1)^{D+1} mod 3 (re-verified 0 fail).
   - `AIU_JOININGS`: ENT ⇏ AIU; ENT and AIU logically independent — [PROVEN — no collapse].
   These three are **mutually consistent** (skew-rotation explicitly notes "two independent obstructions": neutral
   ⇒ no entropy leverage [joinings], contracting base ⇒ no isometric-extension leverage [skew]). **No note claims
   AIU or ENT is closer-than-(K)-hard**; every verdict is (b)/(c) = strictly-weaker-but-(K)-hard / reduces-to-(K).
   `AIU_SEED_SHIFT` correctly refutes the orbit-coupling shortcut. [OK]

**5. Central conjectures honestly labelled & reductions valid (non-circular).**
   - ADELIC_RIGIDITY: **AIU [CONJECTURE]**; AIU∧ENT ⟹ (K) via *proven* Rudolph–Johnson + proven periodic-exclusion. Valid, non-circular. [OK]
   - DIAGONAL_RENORM: **R-GEN [CONJECTURE]** = (K); honest reframing (annealed gap ½ + non-Pisot no-atom both PROVEN; R-GEN ⟺ (K)). [OK]
   - ENDOGENOUS_UE: **EAR [CONJECTURE]** ⟺ (K); Lemmas A-E [PROVEN] genuinely scaffold; reduction valid. [OK]
   - ODD_CALCULUS: **CR [CONJECTURE]** ⟹ (K); coisometry/operator-norm-Lyapunov≡0 [PROVEN]; "irreducible kernel in new dress" honest. [OK]
   - SYNTHESIS: all four ⟺ (K), correctly stated — except the §2 catch (F1).

---

## VERDICT

The cluster is, with the F1/F2/F3 exceptions, soundly labelled: every central new principle is a
[CONJECTURE], each reduction to (K) is valid and non-circular, and the AIU/ENT notes are mutually
consistent (two independent gaps, two independent AIU obstructions, ENT⇏AIU). The surviving defects are all
**un-propagated retractions** of the same two corrections (zero-entropy sign error; non-atomic [PROVEN]
over-claim), not new mathematical errors.

No machine decided. No label upgraded.
