# Endogenous-cocycle unique ergodicity — direct build toward the §5 crux (2026-06-29)

*Assigned task: directly attempt the ENDOGENOUS-COCYCLE UNIQUE-ERGODICITY statement (the §5 crux of
`WEAPONS_AUDIT_2026-06-29.md`). Build as far as rigor allows; mark the irreducible open step as a clean lemma;
state honestly whether the outcome is (a) a partial a-priori bound on the injection, (b) a sharp no-go showing
the self-reference is irreducible, or (c) only a reframing. SOUNDNESS PARAMOUNT — every claim labelled. The
kernel is NOT proven. Numerics: exact big-int, `scratchpad/seam_identity.py`, N=2·10⁵, all identities
machine-verified. Not committed.*

---

## 0. One-line verdict

**Outcome = (b) a SHARP NO-GO, made operator-explicit, plus a rigorous by-product of flavour (a)/(c).**
The annealed transfer operator `L_ann` **exactly annihilates every odd additive character**
(`L_ann χ_a ≡ 0` for `a` odd, machine-verified to `1e-13`), while the unique-ergodicity / equidistribution
conclusion is **exactly** the vanishing of those same odd-character empirical averages. Therefore the spectral
gap of `L_ann` — the only contraction in hand — acts on a subspace that is **complementary to and
non-interacting with** the subspace where the conclusion lives. The self-reference (the fresh bit
`β_n = bit_k(c_n)`) is the *sole* carrier of the odd-character content, and it is precisely what the annealed
model discards by construction. **No bound `Inj(k) ≤ F(ρ, automaton-data)` can exist** (proved by an
adversarial input with the *same* automaton and *same* gap whose feedback is bounded away from 0). The
by-product: the previously *measured* endogeneity recursion `Def(k+1) ≤ ρ·Def(k)+Inj(k)` is upgraded to an
**exact operator identity**, and the open kernel is reframed in its sharpest form.

---

## 1. The target theorem (precise statement)

**Target (Endogenous-cocycle unique ergodicity, EUE).** For the single orbit `c₀ = 8`,
`c_{n+1} = ⌊3 c_n/2⌋` on `ℤ₂`, fix any scale `k` and let `s_n := c_n mod 2^k ∈ ℤ/2^k`. Let
`π_N := (1/N) Σ_{n<N} δ_{s_n}` be the empirical measure. Then

> `π_N ⟶ Haar (= uniform on ℤ/2^k)` as `N → ∞`, for every `k`.

By the [PROVEN] reduction chain (`COMPLETE_PROOF_CAPSTONE.md` §2: even-density `≥ 1/3 ⟺ mean D ≥ 3/2 ⟺`
single-orbit equidistribution mod `2^k`), EUE for all `k` is **equivalent to** the kernel (K) and hence
implies Antihydra never halts. EUE is to be proved **without** an independence / genericity hypothesis on the
orbit — the "Dirac-quenched" transfer the annealed model cannot supply. This is exactly the §5 crux.

---

## 2. Formalisation of the closed-loop cocycle  [PROVEN — all identities exact, machine-verified]

### 2.1 The dynamical system (carry automaton γ coupled to ×(3/2))

The low-`k` bits evolve by an **exact deterministic finite-state machine driven by one fresh input bit per
step.** Writing `c_n mod 2^{k+1} = s_n + β_n·2^k` with `β_n := bit_k(c_n) ∈ {0,1}`:

> **γ (the carry automaton).** `s_{n+1} = U(s_n, β_n)`, where
> `U(s,β) := ⌊3(s + β·2^k)/2⌋ mod 2^k`.   [exact; `seam_identity.py` C1]

`U : ℤ/2^k × {0,1} → ℤ/2^k` is the full automaton; `β_n` is the **incoming high bit** consumed each step.
The self-reference is now explicit: **`β_n = bit_k(c_n)` is a digit of the very state being transported** — the
orbit furnishes its own next input bit (the closed loop).

**[PROVEN, C1]** `U(s,1) = U(s,0) + 2^{k-1} (mod 2^k)` for all `s`: the fresh bit flips *exactly* bit `k-1` of
the next state — a one-bit, top-of-window perturbation.

### 2.2 The annealed operator and its exact action on characters

> **Annealed model.** Replace `(β_n)` by i.i.d. `Bernoulli(½)`. Then `s_n` is Markov with
> `L_ann f(s) = ½[f(U(s,0)) + f(U(s,1))]`, stationary = uniform, spectral gap `1−λ₂(k) > 0`
> (`λ₂ = 0.0001 … 0.34`, k=1..7; `seam_identity.py`, matches `ENDOGENEITY_DEFECT.md`).

Let `χ_a(s) = e^{2πi a s/2^k}`, `a ∈ ℤ/2^k`. Using C1 and `χ_a(2^{k-1}) = (−1)^a`:

> **[PROVEN, C2 — the decisive identity]**
> `L_ann χ_a = ½(1+(−1)^a)·(χ_a∘U(·,0))`, i.e.
> **`L_ann χ_a ≡ 0` for every ODD `a`**, and `L_ann χ_a = χ_a∘U(·,0)` for every EVEN `a`.
> (Machine-verified: `max_{a odd}‖L_ann χ_a‖_∞ ≤ 1e-13`, k=2..8.)

The annealing of one fresh bit averages a character over the `±2^{k-1}` pair `{U(s,0), U(s,1)}`; an odd
character is **exactly cancelled** by this average. So **one annealing step annihilates the entire odd-character
subspace.**

### 2.3 The EXACT seam identity (where the self-reference enters)

Pointwise, `f(s_{n+1}) = f(U(s_n,0)) + β_n·Δf(s_n)` with `Δf(s) := f(U(s,1))−f(U(s,0))`, and
`L_ann f(s) = f(U(s,0)) + ½Δf(s)`. Subtracting and averaging gives the central identity:

> **[PROVEN — exact, C4]  Seam identity.**  For every test function `f`,
> `((I − L_ann^*) π_N)(f) = Feedback_N(f) + O(1/N)`,   where
> `Feedback_N(f) := (1/N) Σ_{n<N} (β_n − ½)·Δf(s_n)`.

For characters, using `Δχ_a = ((−1)^a − 1)·(χ_a∘U(·,0))`:

> **[PROVEN, C4]**  `Feedback_N(χ_a) = 0` for `a` EVEN; and for `a` ODD (since then also `L_ann χ_a = 0`):
> `π_N(χ_a) = Feedback_N(χ_a) + O(1/N)`, i.e. the odd-character empirical average **IS** the feedback.
> Explicitly `Feedback_N(χ_a) = −2·(1/N) Σ_n (β_n−½)·χ_a(U(s_n,0))` — the **correlation of the fresh bit
> `β_n = bit_k(c_n)` with a character of the low state**. (Verified on the real orbit, k=4,6,8: the three
> columns `|(I−L_ann^*)π_N|`, `|Feedback_N|`, `|π_N|` coincide for odd `a` to `O(1/N)`.)

This recovers and **sharpens** the `antihydra_renewal_attack.md` §12 conditional theorem: "`bit_k(c_n) ⊥ low
state ⇒ even-density ½`" is exactly "`Feedback_N(χ_a) → 0 ∀a`", now an exact identity rather than a heuristic.

---

## 3. How far the construction goes — the even/odd splitting  [PROVEN]

The character space splits as `V_even ⊕ V_odd`. By §2.2–2.3 the operator is **block-triangular**:
`L_ann χ_odd = 0` (zero columns at odd inputs); `L_ann χ_even = χ_even∘U(·,0)` has components in **both**
`V_even` and `V_odd` (because `U(·,0)=⌊3s/2⌋ mod 2^k` is *not* a group homomorphism). Feeding this into the
seam identity:

- **Odd block (carries the conclusion).** `π_N(χ_a) = Feedback_N(χ_a)+O(1/N)` for odd `a`. The gap gives **no
  equation** here: the odd components are pure inputs = the feedback = the self-reference.
- **Even block (carries the gap).** `π_N(χ_b) = π_N(L_ann χ_b) + O(1/N)` for even `b`, an exact, feedback-free
  annealed equation — but `L_ann χ_b = Σ_a m_{b,a}χ_a` mixes in **odd** `a`, so the even averages are *driven
  by* the odd/feedback inputs.

> **[PROVEN] Conditional contraction (exact form of the endogeneity recursion).** With the gap, the even block
> is the unique bounded solution of its annealed equation **given** the odd inputs, yielding
> `‖π_N|_{V_even}‖ ≤ (1/(1−λ₂))·‖coupling‖·‖π_N|_{V_odd}‖ + O(1/N)`.
> This is the recursion `Def(k+1) ≤ ρ·Def(k) + Inj(k)` of `ENDOGENEITY_DEFECT.md` — previously *measured*,
> now **derived exactly** with `ρ = λ₂` (even-block contraction) and `Inj(k) =` odd-character feedback.

So the build is complete up to one term: **the cumulative even-defect (which contains parity, the character
`a=2^{k-1}`, hence even-density) is rigorously controlled by the contraction — modulo the odd-character
feedback `Inj(k)`, which the gap does not touch.** EUE `⟺ Inj(k) → 0`.

---

## 4. The irreducible open step (clean lemma for a specialist)

> **Open Lemma (Endogenous odd-character cancellation).** For the orbit `c₀=8`, for each fixed odd
> `a ∈ ℤ/2^k`,
> `Inj_a(N) := (1/N) Σ_{n<N} (β_n − ½)·χ_a(U(s_n,0)) ⟶ 0`   as `N→∞`,
> where `β_n = bit_k(c_n)`, `s_n = c_n mod 2^k`, `U(s,0) = ⌊3s/2⌋ mod 2^k`.

Equivalently: **the fresh bit `bit_k(c_n)` asymptotically decorrelates from every character of the low state
`c_n mod 2^k`.** This is the single residue. It is OBSERVED to hold at the CLT floor (`|π_N(χ_1)| ≈ 0.001` vs
`1/√N ≈ 0.002`, k=6,8), but is **[OPEN]** — it is the kernel (K)/Mahler-3/2 in its sharpest endogenous dress.

---

## 5. Why no a-priori bound on Inj(k) exists from contraction + automaton  [PROVEN no-go]

> **No-Go Theorem.** There is **no function `F(λ₂(k), γ)`** of the spectral gap and the automaton data such
> that, for every input bit-sequence `(β_n)` and the resulting trajectory `s_{n+1}=U(s_n,β_n)`,
> `limsup_N |Inj_a(N)| ≤ F` for odd `a`.

**Proof.** Two independent reasons, both exact.

1. **Blindness of the gap (structural).** By C2, `L_ann χ_a = 0` for odd `a`: the odd-character subspace
   consists of **zero columns** of `L_ann`. The spectral gap is a statement about the action of `L_ann` on its
   range, which lies in the even-driven part; it provides *zero* information about the odd components. But by
   §2.3 the conclusion **is** the vanishing of exactly those odd components. The contraction and the conclusion
   live on non-interacting subspaces. ∎(structural)

2. **Adversary with identical (γ, gap) (constructive).** `seam_identity.py` C5: with the *same* automaton and
   *same* gap, adversarial inputs give `|π_N(χ_1)| = |Feedback_N(χ_1)|` equal to `0.235` (β≡0, k=6), `0.278`
   (β≡1), `0.9998` (β≡0, k=8) — **bounded away from 0**, while the real orbit gives `0.001`. Since the only
   thing that changed is the input bit-sequence, no `F(λ₂,γ)` can bound the feedback. ∎(constructive)

**Consequence (irreducibility).** Any bound on `Inj(k)` must use a property *specific to the endogenous input*
`β_n = bit_k(c_n)` — i.e. the self-reference / the orbit's arithmetic — not `(L_ann, gap, γ)` alone. The
endogeneity does buy something [PROVEN, `antihydra_renewal_attack.md` §6 + Dual-Repulsion]: the *exact* trap
(`β` driving `c≡1 mod 2^k` permanently) is excluded because the integer orbit grows (`c≡1` forever ⇒ `c=1`,
off-orbit). But endogeneity does **not** exclude *intermittent / approximate* trapping, and the residual
condition "residence time near `c≡1 mod 2^k` is `o(N)`" is **exactly** the Open Lemma = (K). The self-reference
is therefore irreducible at the level of all finite-window / structural data — independently re-deriving the
two §5 meta-theorems of `COMPLETE_PROOF_CAPSTONE.md` (the obstruction is shared with the halting orbit `o=1`)
and the `QUENCHED_ANNEALED_SEAM.md` finding (the difference lives below every finite-order statistic).

### Why the natural escape routes are circular  [PROVEN they reduce to the conclusion]

- "Assume `β_n` balanced/independent" = assume `bit_k(c_n)` equidistributes = assume a slice of EUE = circular.
- "Bootstrap via the gap from scale `k` to `k+1`": the feedback at scale `k` is the top bit of the scale-`(k+1)`
  state, whose control needs the scale-`(k+1)` feedback — infinite regress; the gap never reaches the fresh end
  (matches the §13 `antihydra_renewal_attack.md` falsification of the CA-cascade).
- "Use the even-block gap alone": proved insufficient in §3 — even-block is *driven by* the odd/feedback inputs.

---

## 6. Honest verdict

- **(a) partial a-priori bound on Inj(k):** achieved only **conditionally** — the exact recursion
  `even-defect ≤ (1/(1−λ₂))·‖coupling‖·odd-defect + O(1/N)` (§3) rigorously bounds the *cumulative/even* defect
  (incl. even-density) by the *odd/fresh-bit* feedback. **No unconditional bound on Inj(k) itself**, and §5
  proves none can come from `(gap, γ)`.
- **(b) sharp no-go:** **YES, and this is the main result** — `L_ann` annihilates the odd subspace where the
  conclusion lives (exact, C2), and an adversary with identical `(γ, gap)` realises feedback `≈1` (C5). The
  self-reference is the unique carrier of the odd content and is irreducible to structural data.
- **(c) reframing:** also yes — the endogeneity recursion is upgraded from measured to an **exact operator
  identity** (the seam identity), and the kernel is restated as the single clean Open Lemma §4.

**Net:** the build closes the construction to one exact term and proves that term lies provably outside the
reach of the only available contraction; the gap of `L_ann` and the self-reference act on complementary,
non-interacting character subspaces. This is the precise, operator-level form of "the closed loop cannot be
opened by the annealed gap." The kernel (K) is untouched and remains [OPEN] = AEV/Mahler-3/2. The deliverable
is a sharp no-go (b) with a rigorous conditional bound (a) and an exact reframing (c).

No machine decided. No label upgraded.
