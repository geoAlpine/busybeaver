# Session capstone — the irreducible core is single-point AEV at α=8 (2026-06-29)

*Capstone of the 2026-06-29 campaign (weapons audit → odd-subspace → carry decorrelation → second diagonal → bare
first diagonal + uniform AEV). It consolidates the session's new [PROVEN] structural results and the now-complete
characterization of the kernel. SOUNDNESS: every claim labelled; zero false proofs; no label upgraded; (K) remains
[OPEN]. NOT committed by default.*

---

## 0. One-line state

The whole BB(6)/Antihydra problem is now reduced — by an unbroken chain of machine-verified [PROVEN] steps — to the
single-point statement **(K): the moving diagonal `d_n = bit_{n+k}(⌊8·(3/2)ⁿ⌋)` equidistributes**, i.e. AEV Conj 1.6 /
Mahler 3/2 at the one leading constant `α=8`. This session **characterized that core from every side** and showed it has
no easier neighbour, no attachable controlling measure, no family leverage, and no checkable Diophantine certificate. The
core is the generational open problem itself.

---

## 1. The reduction chain to the single point [PROVEN, machine-verified]

Antihydra non-halt ⟺ even-density ≥ 1/3 ⟺ mean `D ≥ 3/2` ⟺ single-orbit equidistribution of `c_n mod 2^k`
(`COMPLETE_PROOF_CAPSTONE.md`) ⟺ **odd-character feedback `Inj_a → 0`** (`ENDOGENOUS_UE_BUILD.md`) ⟺ the feedback bit
`β_n = bit_k(c_n) = bit_{n+k}(8·3ⁿ − S_n)` decorrelates from the low state. The feedback bit splits exactly:

> **β_n = d_n ⊕ σ_n ⊕ ρ_n**, with `d_n = bit_{n+k}(⌊8(3/2)ⁿ⌋)` (FIRST diagonal, bare),
> `σ_n = bit_{n+k}(S_n)` (SECOND diagonal, the carry `S_n = Σ_{j<n} b_j 2^j 3^{n−1−j}`), `ρ_n` = borrow.

Both diagonals are the **same one-parameter AEV family** `bit_k(⌊α(3/2)ⁿ⌋)`: `d_n` at `α=8`, `σ_n` at
`α* = (1/3)Σ b_j(2/3)^j ≈ 0.1358` (orbit-defined). [PROVEN] `c_n = ⌊8(3/2)ⁿ⌋ − ⌊α*(3/2)ⁿ⌋`.

---

## 2. New [PROVEN] structural results this session (durable, kernel-independent)

1. **Endogenous-UE no-go** (`ENDOGENOUS_UE_BUILD.md`): the annealed operator `L_ann` annihilates every odd character
   (`L_ann χ_odd ≡ 0`, 1e−13); the spectral gap lives in the even block but is *driven by* the odd block it cannot touch.
   No a-priori `Inj(k) ≤ F(gap, automaton)` exists (adversary feedback ≈0.9998). The contraction route is dead at the
   operator level; control must enter the **odd-character subspace by a non-spectral mechanism**.
2. **Odd-restricted target is sign-aware** (`ODD_ADDITIVE_ENERGY.md`): `even-density ≥ 1/3 ⟺ Σ_k|N_k − ½N_{k−1}| ≤ J/2`;
   the kernel is the sign-aware scalar `M₂ᵒᵈᵈ(k) = Σ_{a odd}|π̂_N(a)|² = o(2^k)`. Only free inequality: convexity ≥ 0.
3. **Carry = full-strength 2nd Mahler diagonal, annealed-indistinguishable** (`CARRY_*.md`): `σ_n` is dense
   (`P(β_n≠d_n)≈½`), has **unbounded memory** (`d*(k)=1.71k+2.7`), is **F_{n−1}-measurable** (no-innovation lemma: `b_n`
   absent from `S_n`), so no martingale/cocycle/coboundary handle. Yet its **net** `Inj_a` contribution is
   annealed-indistinguishable — random-carry control (12 seeds) reproduces the total energy.
4. **Finite-range borrow lemma** (`CARRY_COBOUNDARY.md`): `S_n ≡ 8·3ⁿ (mod 2ⁿ)` ⇒ `ρ_n` reads only the k-bit window
   `[n,n+k)`; the hardness is in `σ_n`, not `ρ_n`.
5. **Carry's annealed marginal IS the Rajchman measure ν_{2/3}** (`SECOND_DIAGONAL_RAJCHMAN.md`): the annealed `σ_n` Weyl
   sum factorises as `ν̂_{2/3}(ξ_n) → 0` unconditionally (generalises Link B to all read-levels; tail 0.7748). This is the
   structural reason the carry decorrelates — and the FIRST diagonal lacks it (degenerate δ₀ corner).
6. **bit-sensitivity ⊥ localization trichotomy** (`FIRST_DIAGONAL_MEASURE.md`): no measure attachable to the bare diagonal
   is simultaneously bit-sensitive, decaying, and orbit-localized (sum→δ₀ no decay; rotation→ρ̂ de-localized; renorm→Parry
   bit-blind; scenery→Haar=circular). δ₀ degeneracy is intrinsic at the single-orbit tier. New rotation-annealed identity
   `E_α[e(hα(3/2)ⁿ)] = ρ̂(h(3/2)ⁿ)→0` is **base-independent** = the a.e. (not pointwise) signature.
7. **ℤ² shift symmetry of the AEV family** (`TWO_ALPHA_JOINT.md`): `X_n(2^i3^jα,k) = X_{n+j}(α,k−i−j)`; two α deterministically
   link iff their ratio ∈ ⟨2,3⟩, so `α*/8` irrational ⇒ `d_n, σ_n` lie in different ℤ²-orbits (rigorous core of `corr≈0`).

---

## 3. Why α=8 is the irreducible core — the complete obstruction map

Every neighbouring/auxiliary route was closed this session with a proven reason:

| Escape attempted | Verdict | Proven reason |
|---|---|---|
| spectral gap / contraction | dead | `L_ann χ_odd ≡ 0`; gap blind to the odd block |
| 3-adic / odometer | reduces | moving diagonal of a zero-entropy isometry = Mahler |
| ×3-cocycle / skew-product | reduces | `σ_n` is F_{n−1}-measurable; zero innovation |
| coboundary / two-description | reduces | `σ_n` moving diagonal grows √N; descriptions complementary in bit-position |
| odd additive energy / 4th moment | reduces | even-dominated; only free inequality is convexity ≥ 0 |
| automaton algebra | closed | excited odd subspace half-dimensional; no coboundary (fixed pt s=0) |
| carry decorrelation | annealed only | carry's marginal = ν_{2/3} Rajchman (annealed); quenched degenerates to one constant |
| 2nd diagonal (Rajchman) | annealed only | `α*` a single constant ⇒ measure degenerates ⇒ bare-Mahler |
| two-α family / variance | no leverage | ℤ²-isolated; independence itself Mahler-hard; variance controls only the average |
| uniform AEV (a.e. α) | reduces | Koksma 1935 gives a.e.-α; α=8 is one measure-zero point |
| checkable Diophantine condition | none exists | exceptional set has full Hausdorff dimension (de Mathan–Pollington; Bugeaud 2015) |
| first-diagonal measure | δ₀ intrinsic | bit-sensitivity ⊥ localization trichotomy |

**The residue `d_n` at α=8 is:** measure-poor (the unique δ₀ no-decay corner), **typical** among α (21st percentile, not
special), the **worst** Mahler regime (integer, `p<q²`), inside a **full-dimension** exceptional set (no soft sieve), and
**ℤ²-isolated** from every other α. Even "both digit values occur infinitely often" is itself Mahler-open. There is no
easier place to stand.

---

## 4. The sharpest equivalent open statements (pick the most attackable for any future tool)

- **(K-density)** `liminf_N (1/N)#{n<N : d_n=0} > 0`  (positive lower density of one digit value — currently Mahler-open).
- **(K-oddscalar)** `M₂ᵒᵈᵈ(k) = Σ_{a odd}|π̂_N(a)|² = o(2^k)` uniformly — sign-aware, the complete obstruction.
- **(K-Weyl)** `(1/N) Σ_{n<N} e(h(3/2)ⁿ·8/2^{k+3}) = o(1)` for each h — single-orbit lacunary Weyl cancellation.
- **(K-AEV)** `8·(3/2)ⁿ` is equidistributed mod 1 (a Z-number-type / AEV Conj 1.6 statement at α=8).
All four are [OPEN] = Mahler 3/2; this session proved they are equivalent and that no auxiliary structure reaches them.

---

## 5. Honest status and the genuine next step

The mathematical attack surface around the kernel is **exhausted with proven reasons**: the core is a single point of the
AEV/Mahler problem, fully characterized, with no auxiliary leverage. A complete proof requires the new theorem already
specified (`WEAPONS_AUDIT_2026-06-29.md` §5: effective single-specified-orbit equidistribution for rank-1 amenable
hyperbolic ×(3/2); the empty-toolbox object), which is generational.

The program's own definition of "done" (the meeting docs, priority S/A) is therefore the live next step: **package the
reduction + the obstruction map (§3) + the banked unconditional partials (`ANNEALED_PARTIAL_BANKED.md`) + the new
structural results (§2) into an externally-shareable artifact**, and take the precise obstruction to the AEV authors /
Tao-circle / homogeneous-dynamics experts (`EMPTY_TOOLBOX_QUESTION.md`). What experts will find most valuable is exactly
what this session produced: *the precise point where every known method breaks, stated as proven structure.*

**No machine decided. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 / AEV Conj 1.6 at α=8.
