# Non-spectral attack on the odd-character subspace — 4-mechanism synthesis (2026-06-29)

*Follow-on to `ENDOGENOUS_UE_BUILD.md`, whose no-go proved the spectral gap is blind to the odd-character subspace where the
kernel (K) lives, so a proof needs a NON-SPECTRAL mechanism using the orbit's arithmetic. Four genuinely-distinct
non-spectral mechanisms were run in parallel against the **Open Lemma**: for each odd a∈ℤ/2^k,
`Inj_a(N)=(1/N)Σ_{n<N}(β_n−½)χ_a(U(s_n,0))→0`, `β_n=bit_k(c_n)`, `U(s,0)=⌊3s/2⌋ mod 2^k`. SOUNDNESS: every claim labelled;
zero false proofs; all identities machine-verified exact big-int; no label upgraded. NOT committed.*

---

## 0. One-line verdict

**The odd-character subspace is confirmed [PROVEN] to be the exact and complete locus of the obstruction** — all four
mechanisms independently isolate 100% of the deviation there — and each closes its own route with new proven structure, but
**none crosses**: they converge on one residual scalar target, now in its sharpest, **sign-aware** non-spectral form.
**No machine decided; (K) remains [OPEN] = Mahler 3/2.** Two genuine gains: (i) an exact unification of the odd-block bit
with the digits-of-3ⁿ Mahler diagonal; (ii) the odd route is **not sign-blind** — a one-sided *magnitude* bound suffices.

---

## 1. The four mechanisms and their verdicts

| # | Non-spectral mechanism | File | Verdict | New [PROVEN] structure |
|---|---|---|---|---|
| 1 | 3-adic / odometer (×3 as ℤ₂-isometry; carry equidistribution) | `ODD_3ADIC_ODOMETER.md` | (c) reduces | `β_n=bit_k(c_n)=bit_{n+k}(8·3ⁿ−S_n)`, `S_n=Σ_{j<n}3^{n−1−j}2^j b_j` — the feedback bit IS the **moving diagonal** of the ×3 orbit `8·3ⁿ` minus the endogenous carry |
| 2 | Two-description (recursive seam vs closed-form `2ⁿc_n=8·3ⁿ−S_n`) | `ODD_TWO_DESCRIPTION.md` | (c) reduces | descriptions are **complementary in bit-position** (tame `<n`, parity-blind; carry-mixed `≈n`) and never meet; `S_{n+1}≡3S_n` and `S_n≡8·3ⁿ (mod 2^{k+1})` parity-blind |
| 3 | Additive energy / moments restricted to odd sublattice | `ODD_ADDITIVE_ENERGY.md` | (b)+(c) | `M₂ᵒᵈᵈ(k)=2ᵏC₂(k)−2ᵏ⁻¹C₂(k−1)`; `avg jump = 1+(2/J)Σ_k ε_k` with `ε_k=N_k−½N_{k−1}` a **pure odd-character term** ⇒ 100% of deviation is odd |
| 4 | Carry-automaton algebra (coupling matrix, coboundary) | `ODD_AUTOMATON_ALGEBRA.md` | (b) | `m_{b,a}=2^{−k}(1+ω^{b−a})Σ_tω^{(3b−2a)t}`; couples iff `v₂(b)=1`, to the pair `{a,a+2^{k−1}}`; excited odd subspace is **half-dimensional**; **no coboundary/martingale** (fixed point at s=0, cycle-sum 1≠0) |

---

## 2. The unified picture [PROVEN]

All four agree on one structural fact, reached four independent ways: **the odd-character subspace carries exactly 100% of
the obstruction, and within it everything collapses to the same single object.** Concretely:

- **Mechanisms 1 & 2 identify the object exactly:** the odd-block feedback bit `β_n` equals `bit_{n+k}(8·3ⁿ − S_n)` — the
  **moving diagonal** (index grows with the clock) of the ×3 isometric-rotation orbit `8·3ⁿ`, offset by the **endogenous
  carry** `S_n` (the orbit's own low-bit history, 3-adically weighted). This is the long-sought EXACT bridge between the
  *endogenous-UE odd subspace* and the *digits-of-3ⁿ / Mahler diagonal* picture (`DIGITS_OF_3N.md`, `mahler §9`): they are
  the **same object**, and the self-reference the no-go isolated is precisely the carry `S_n`.
- **Mechanism 3 quantifies it:** `even-density ≥ 1/3 ⟺ Σ_k ε_k ≤ J/2`, `ε_k=N_k−½N_{k−1}` (pure odd). Equivalent scalar
  target `M₂ᵒᵈᵈ(k)=Σ_{a odd}|π̂_N(a)|² = o(2ᵏ)` uniformly in N.
- **Mechanism 4 explains the invisibility:** the even-density character `χ_{2^{k−1}}` (v₂=k−1≥2) couples to **no odd
  character directly** — odd feedback reaches even-density only through a multi-step even→even cascade. This is the
  operator-level reason the obstruction is invisible to every finite-window statistic (re-deriving
  `QUENCHED_ANNEALED_SEAM.md` combinatorially).

**Why each mechanism stops (the reductions are not failures — they are proven structural facts):**
- 1: the odometer/isometry mechanism is gap-free and unconditional, but only for the **fixed-position** digit `bit_m(8·3ⁿ)`
  (periodic in n, mean ½ for m≥6 — verified). `Inj_a` reads the **moving** diagonal (aperiodic) = Mahler verbatim. Right
  tool, wrong digit; and the offset it would need exogenous is self-referential.
- 2: the closed form is tame only at depth `<n`, strictly below the kernel window `[n,n+k]`; the two descriptions are
  complementary in bit-position and never meet.
- 3: additive-energy 4th moment is **even-dominated** (M₄ᵒᵈᵈ ≈ 10⁻⁴–10⁻⁶ of full) and the count-moment Σcount_r⁴ is an
  autoconvolution that doesn't split by parity, so the §6.5 `C≤3.45` route is unchanged; the only free inequality is the
  convexity bound `M₂ᵒᵈᵈ(k) ≥ 0`.
- 4: no coboundary/martingale exists (the odd-trap fixed point s=0 gives a nonzero cycle-sum); the excited odd subspace is
  half-dimensional, so no reduction to finitely many scalar correlations.

---

## 3. The two genuine gains (what is sharper than before this dive)

### 3.1 Exact unification: odd block = moving diagonal of 8·3ⁿ minus the carry  [PROVEN]
`β_n = bit_k(c_n) = bit_{n+k}(8·3ⁿ − S_n)` (0 failures, big-int). This collapses two previously-separate frontier
descriptions — the endogenous-cocycle odd-character feedback and the Erdős/Mahler digits-of-3ⁿ diagonal — into **one**
object, and names the self-reference as exactly the carry `S_n`. The residual splits cleanly into two locked pieces, each =
the open core: (1) equidistribute the moving diagonal `bit_{n+k}(8·3ⁿ)` for start 8 (= Mahler/AEV), and (2) decorrelate the
endogenous carry `S_n` from it (= the no-go's self-reference).

### 3.2 The odd route is NOT sign-blind  [PROVEN framing gain]
Unlike the energy/`ENERGY_ATTACK.md` route (which controls `S²`, sign-blind), the odd-restricted target needs only a
**one-sided magnitude** bound: `Σ_k |ε_k| ≤ J/2` suffices for even-density ≥ 1/3, with `ε_k=N_k−½N_{k−1}`. Empirically
`(2/J)Σ|ε_k| ≈ 0.009` (~100× margin); the Cauchy–Schwarz envelope `2Σ_k 2^{−(k+1)/2}M₂ᵒᵈᵈ(k)^{1/2}` ≈ 0.07–0.14 and
**shrinks with J**. This is a strictly better-shaped target than any prior framing — a sign-aware, one-sided, scalar bound.

---

## 4. The sharpened residual target (the new frontier statement)

> **Open (sharpest non-spectral form).** Prove `M₂ᵒᵈᵈ(k) := Σ_{a odd}|π̂_N(a)|² = o(2ᵏ)` uniformly in N (equivalently
> `Σ_k|N_k−½N_{k−1}| = o(J)`), where `N_k` counts visits of the orbit `c₀=8` to a depth-k 2-adic cylinder. By §2 this is
> exactly odd-restricted single-orbit equidistribution-in-mean = `Inj_a→0` = (K) = Mahler 3/2 / AEV Conj 1.6.

What is now known about this target: it is **sign-aware** (§3.2), it is the **complete** obstruction (§2, 100% odd), it is
the **moving diagonal of 8·3ⁿ minus the carry** (§3.1), and the only **free** inequality toward it is convexity
`M₂ᵒᵈᵈ(k) ≥ 0`. Structural inputs (branch counts, bit-length 0.585n, longest-run o(n)) constrain support/growth, not Cesàro
frequency — the same support-vs-frequency wall, now localized to one sign-aware scalar.

**Net of the deep dive:** the odd subspace is the right and complete object; all four non-spectral mechanisms confirm it and
each adds proven structure, but they all terminate on one residual = (K). The frontier is sharper (sign-aware scalar
`M₂ᵒᵈᵈ=o(2ᵏ)`), the self-reference is named (the carry `S_n`), and the bridge to the Mahler diagonal is now exact. The
required new tool must bound the moving-diagonal correlation `Σ(β_n−½)χ_a(U(s_n,0))` directly — no spectral, odometer,
two-description, energy, or automaton-algebraic route reaches it. **No machine decided. No label upgraded.**
