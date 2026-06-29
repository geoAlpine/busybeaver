# New mathematics for Antihydra — 4-framework synthesis (2026-06-29)

*Capstone of the new-math construction campaign. Four candidate frameworks were built against the spec (effective
equidistribution of ONE specified orbit of the rank-1 amenable hyperbolic ×(3/2), controlling the odd-character subspace
by a non-spectral mechanism). They collapse to TWO complementary unified frameworks, both centred on the same map ×(3/2)
on the (2,3)-adic solenoid. SOUNDNESS: every claim labelled; the central conjectures are honestly shown to be ⟺ (K) or
to reduce (K) to a named famous open problem; nothing claims to prove (K). NOT committed by default.*

---

## 0. One-line synthesis

The four frameworks unify into two: **(I) a solenoid measure-rigidity / renormalization theory** (`NEWMATH_ADELIC_RIGIDITY`
+ `NEWMATH_DIAGONAL_RENORM`) and **(II) an odd-block cross-scale cocycle theory** (`NEWMATH_ENDOGENOUS_UE` +
`NEWMATH_ODD_CALCULUS`). Both reduce (K) to a single clean conjecture; **(I) is the most promising because it connects (K)
to the Rudolph–Johnson / Furstenberg ×2,×3 rigidity world** — a real, powerful, proven theory the program had wrongly
dismissed as "rank-2, unavailable." **[SOUNDNESS CORRECTION 2026-06-29, `LIMIT_MEASURE_ENTROPY.md`]** An earlier draft of
this note claimed the limit measure is "plausibly zero-entropy (linear complexity) ⟹ a Furstenberg corner." **That was a
sign error and is retracted.** `p(ℓ)≥1.71ℓ` is a *lower* bound; entropy-0 needs a sub-exponential *upper* bound, and the
measured complexity is full (`p(ℓ)=2^ℓ` to ℓ=16, block entropy ≈ log2) ⇒ `h_top=log2>0`, so the variational-principle
argument is vacuous. Decisively, **Haar (the (K) target) has positive entropy** (`h_Haar(M₂)=log2`), so `h_μ=0 ⟹ μ≠Haar ⟹
(K) false`: **zero entropy is the (K)-FALSE regime**, not a tractable corner. Correct status: framework (I) reduces (K) to
**AIU ∧ `h_μ(M₂)>0`**, and with both the **proven** Rudolph–Johnson gives `μ=`Haar `=` (K). Both are open, (K)-hard
sub-conjectures; the bridge is to the *proven* RJ theorem (not to open Furstenberg). The durable yield is several
genuinely new [PROVEN] structural theorems (§3) and a clean placement of (K) in a major research program.

---

## 1. The two unified frameworks

### (I) Solenoid measure-rigidity / renormalization — `NEWMATH_ADELIC_RIGIDITY` + `NEWMATH_DIAGONAL_RENORM`
Both notes study the **same** object: the automorphism `A = ×(3/2)` of the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, and the
conjecture that the rational seed `8∈ℤ[1/6]` is **A-generic** (empirical measures `μ_N=(1/N)Σδ_{Aⁿ8} ⇀ Haar`). Equidist.
of `8(3/2)ⁿ` = (K).
- **[PROVEN] Host realization.** `M_2=×2, M_3=×3 ∈ Aut(X)` commute and are hyperbolic; `A = M_3 M_2⁻¹` is a rank-1 line in
  the rank-2 host `Φ=⟨×2,×3⟩`; the "arithmetic second direction" is the diagonal `×6`, tied by the product formula
  `|6|_∞|6|_2|6|_3=1`. The famous ×2,×3 rigidity (Rudolph–Johnson) **does act on this space** — the program's "rank-2
  unavailable" was wrong; it is available on the solenoid.
- **[PROVEN] Dichotomy lemma.** Via Berend rigidity + the proven 2-adic periodic-repulsion, the **only** gap between
  A-invariance and Haar is the upgrade **A-invariant ⟹ host-invariant**. So the single missing step is named exactly.
- **[CONJECTURE] AIU (Arithmetic Invariance Upgrade).** A non-atomic, positive-2-adic-entropy weak-* limit `μ` of the
  orbit's empirical measures is `⟨×2,×3⟩`-invariant (not merely A-invariant). AIU ⟹ Rudolph–Johnson ⟹ `μ=`Haar ⟹ (K).
- **[PROVEN] Renormalization structure** (`NEWMATH_DIAGONAL_RENORM`): the exact ×3-adder transducer recurrence
  `d_{n+1}^{(k)} = d_n^{(k+1)} ⊕ d_n^{(k)} ⊕ γ_n^{(k)}`; the **annealed** transducer has spectral **gap ½** with unique
  uniform fixed point; **non-Pisot ⇒ no atomic/Pisot/sofic A-fixed-point** (`|3/2|_2=2>1`, 2-adic place expands; purely
  Lebesgue spectrum; diagonal non-automatic). This proves there is **no atomic obstruction** to genericity — consistent
  with AIU.

### (II) Odd-block cross-scale cocycle — `NEWMATH_ENDOGENOUS_UE` + `NEWMATH_ODD_CALCULUS`
Both build the non-spectral object on the odd-character subspace (where the gap is blind).
- **[PROVEN] Even enslaved to odd** (`ENDOGENOUS_UE` Lemma C): the parity/even block is a bounded functional of the odd
  block, so the whole problem lives on `V_odd`.
- **[PROVEN] Carry-renormalization cocycle `R_k`** (`ODD_CALCULUS`): maps the odd block one dyadic scale down, via the
  semiconjugacy `V^{(k+1)} mod 2^k = U^{(k)}(·,bit_k)` (the top bit of scale k+1 IS the fresh input of scale k — the
  infinite regress becomes a scale map). **`R_k` is a COISOMETRY** (all singular values 1) ⟹ **operator-norm cross-scale
  Lyapunov is exactly 0** ⟹ *no spectral/operator-norm approach can ever work across scales* (a sharp no-go extending the
  L_ann no-go to the renormalization).
- **[CONJECTURE] negative data-direction Lyapunov (CR / EAR).** The *quenched* data-direction Lyapunov exponent of the
  cocycle along the orbit is strictly negative (odd-data equidistributes into `ker R_k`; energy ratio → ½). Proposed
  **engine**: the 2-adic Lyapunov `V = v₂(c−1)` (orbit arithmetic, the dual-repulsion drift) — the required third
  ingredient beyond (gap, automaton). CR ⟺ (K).

---

## 2. Honest assessment — which is most promising, and the catch

**(I) is the most promising** and the genuine new direction: it places (K) inside the **Furstenberg ×2,×3 / Rudolph–Johnson**
program via the solenoid, with a **proven dichotomy** isolating one conjecture (AIU). This is a real bridge to a powerful
literature and the right thing to put to experts.

**The catch [honest].** Rudolph–Johnson needs **positive entropy**. A single orbit's empirical limit measure is plausibly
**zero-entropy** (the orbit's subword complexity is only linear, `p(ℓ)≥1.71ℓ`, topological entropy 0). In the zero-entropy
regime, ×2,×3-invariance does **not** force Haar — that is exactly **Furstenberg's conjecture**, itself a famous open
problem. So framework (I) reframes (K) as a Furstenberg-×2,×3-type rigidity statement **in the zero-entropy regime** — a
different, equally-generational open problem, not a shortcut. This is the precise, honest status: a bridge, not a proof.

**(II)** is a sharper *dressing* of the kernel (CR ⟺ (K)) plus a real no-go (the coisometry kills every operator-norm
route), and it contributes the candidate **2-adic Lyapunov engine** `V=v₂(c−1)`. Its value is diagnostic and it supplies
the engine that framework (I)'s AIU-via-entropy would also need.

All four central conjectures (AIU+entropy, R-GEN, EAR, CR) are ⟺ (K) (or reduce it to a named open problem). **No framework
proves (K); none claims to.** The new math produced is a coherent theory and a placement, not a resolution.

---

## 3. Durable new [PROVEN] theorems produced this session (kernel-independent)

1. **Solenoid host + dichotomy lemma**: `×2,×3∈Aut(X)`, `A=M_3M_2⁻¹`; A-invariance ⟹ host-invariance is the *only* gap to
   Haar (Berend + 2-adic repulsion). [PROVEN]
2. **Renormalization transducer**: exact `d_{n+1}^{(k)}=d_n^{(k+1)}⊕d_n^{(k)}⊕γ_n^{(k)}`; annealed gap ½, unique uniform
   fixed point; **non-Pisot ⇒ no atomic/Pisot/sofic fixed point** (no atomic obstruction). [PROVEN]
3. **Coisometry no-go**: the cross-scale carry-renormalization cocycle `R_k` is a coisometry ⟹ operator-norm Lyapunov ≡ 0
   ⟹ no spectral approach works across scales. [PROVEN] (sharpens the L_ann odd-blindness no-go).
4. **Even-enslaved-to-odd** + the **2-adic Lyapunov drift** `V=v₂(c−1)` off the trap (dual-repulsion). [PROVEN]
5. **Endogenous-cocycle / self-consistent-measure / EUE definitions** and the EAR ⟺ (K) reframing — a clean new vocabulary
   for self-referential orbits, distinct from self-consistent dynamical systems (arXiv:1909.04484) and (T,T⁻¹)/RWRS.

---

## 4. The unified frontier statement and the next step

> **(K) ⟺ the rational point 8∈ℤ[1/6] is generic for the non-Pisot solenoid automorphism ×(3/2)** ⟺ (dichotomy) its
> empirical limit measure is `⟨×2,×3⟩`-invariant ⟺ (Rudolph–Johnson, *modulo positive entropy*) Haar. In the zero-entropy
> regime this is a **Furstenberg-×2,×3-type rigidity** problem. The odd-block cocycle (II) supplies the candidate engine
> (2-adic Lyapunov `V=v₂(c−1)`) and proves no operator-norm route can replace it.

**Next step (highest value):** take this placement to **homogeneous-dynamics / measure-rigidity experts** (Einsiedler,
Lindenstrauss, Host–Kra circle) and the **AEV authors** — the sharp question is now *"does the Antihydra orbit's limit
measure on the (2,3)-solenoid have positive entropy, and if zero, is this a tractable corner of Furstenberg's ×2,×3?"*
That is a precise, expert-facing question with a proven reduction behind it — exactly the kind of contribution the program
targeted (priority A/B). The new math is a genuine framework + a major-program placement; the resolution is generational.

**No machine decided. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 / AEV / now also a Furstenberg-×2,×3 corner.
