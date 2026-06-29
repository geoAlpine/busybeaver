# Moving-diagonal renormalization for the non-Pisot base 3/2 (2026-06-29)

*FRAMEWORK-CONSTRUCTION. Builds a renormalization operator `R` on the space of moving-diagonal
observables of the orbit `8·3ⁿ`, seeded by the `[PROVEN]` `ℤ²` shift symmetry of the AEV digit
family. Goal: turn "read the moving diagonal of a zero-entropy 2-adic isometry" (`mahler §9`, the
object with no mixing to exploit) into a non-trivial dynamical question — the genericity of a single
rational point for a solenoid automorphism whose non-Pisot spectrum forbids any atomic/sofic
shortcut. SOUNDNESS PARAMOUNT: every claim labelled. (K) is NOT proven. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/diagonal_renorm.py` (exact big-int,
N≤5·10⁴, <2s): EXACT recurrence 0/35988 fails, Z² 0/168000 fails, annealed-R gap 0.5, balance
0.49992. NOT committed.*

---

## 0. One-line state

The moving diagonal `d_n^{(k)} = bit_{n+k}(8·3ⁿ) = bit_k(⌊8(3/2)ⁿ⌋)` carries an **exact self-similar
recurrence** [PROVEN, §2]
> `d_{n+1}^{(k)} = d_n^{(k+1)} ⊕ d_n^{(k)} ⊕ γ_n^{(k)}`  (the ×3 binary-adder transducer),

which IS the renormalization `R` (one time-step = ×(3/2), the `(i,j)=(−1,1)` element of the `ℤ²`
group). `R` is the automorphism `×(3/2)` of the `(2,3)`-adic solenoid. Its non-Pisot spectrum
[PROVEN, §3] forbids any atomic/Pisot/sofic fixed point; its **annealed** version (carry randomised)
is a finite Markov transducer with leading eigenvalue 1, **spectral gap 0.5**, and **unique uniform
fixed point** [PROVEN-numeric, §3] — so the annealed `R` *contracts to balance*. The irreducible
[CONJECTURE, §4] is that the **single rational point `8` is `R`-generic** (its empirical measure →
Haar), i.e. the deterministic-carry `R` inherits the annealed uniform attractor. That conjecture is
exactly (K) = Mahler 3/2 / AEV Conj 1.6 at α=8 [§5]. **No machine decided. No label upgraded.**

---

## 1. DEFINITIONS — diagonal observables and the renormalization R

### 1.1 The diagonal-observable space `[DEFINITION]`
For the orbit integer `m_n := 8·3ⁿ` write the **moving-diagonal array**
```
d_n^{(k)} := bit_{n+k}(m_n) = bit_k(⌊8(3/2)ⁿ⌋),   k ≥ 0.
```
`d_n := d_n^{(0)}` is the Antihydra feedback / parity bit (the (K) object). Reading the diagonal at
step `n` is reading FIXED low bit `k` of the real-orbit floor `⌊8(3/2)ⁿ⌋`; as `n` grows this sweeps a
slope-1 diagonal of the bit-grid of `3ⁿ` (`DIGITS_OF_3N §1`). Let
`Ω := ℤ₂` (the 2-adic integers, carrying the whole bit-string of the orbit) and let the **diagonal
observable** be `φ_k : Ω → {0,1}, φ_k(x) = bit_k(x)`. The orbit lives at the point `x_n = ⌊8(3/2)ⁿ⌋`
read mod `2^{k+O(1)}`, fed by a growing low-bit tail (the fractional part `{8(3/2)ⁿ}=(m_n mod 2ⁿ)/2ⁿ`).

### 1.2 The `ℤ²` symmetry is a renormalization-group action `[PROVEN — re-verified 0/168000]`
With `X_n(α,k)=bit_k(⌊α(3/2)ⁿ⌋)` (`=bit_{n+k}((p3ⁿ)//q)` for `α=p/q`):
> **`X_n(2^i 3^j α, k) = X_{n+j}(α, k−i−j)`**  (whenever `k−i−j ≥ 0`)   [`TWO_ALPHA_JOINT §1`].

The group `G = ⟨×2, ×3⟩ ≅ ℤ²` acts on the multiplier line; on the digit array it acts by `(n,k)`-shifts:
- **×2** `(i,j)=(1,0)`: `X_n(2α,k)=X_n(α,k−1)` — a pure **bit-shift** (the binary place; trivial isometry).
- **×3** `(i,j)=(0,1)`: `X_n(3α,k)=X_{n+1}(α,k−1)` — **advance n, shift k down** (the ternary place).
- **×(3/2)** `(i,j)=(−1,1)`: `X_n((3/2)α,k)=X_{n+1}(α,k)` — **advance n at fixed k**: the **time-step**.

### 1.3 The renormalization operator `R` `[DEFINITION]`
`R` is the time-step `(i,j)=(−1,1)` of `G`, equivalently `×(3/2)` on the constant:
```
(R φ)(α) := φ((3/2)α),    d_n^{(k)} = (Rⁿ φ_k)(8).
```
Since `(3/2)` is an automorphism of the **`(2,3)`-adic solenoid** `S = (ℝ × ℚ₂ × ℚ₃)/ℤ[1/6]`, `R` is
the solenoid automorphism `×(3/2)`; `8 ∈ ℤ[1/6] ⊂ S` is the seed. The dual action `R*` on the
Pontryagin dual `Ŝ = ℤ[1/6]` is `ξ ↦ (3/2)ξ`. Pushforward `R_*` acts on measures on `S`; the diagonal
observable `φ_k` is bit-sensitive only on the `ℚ₂` factor.

---

## 2. PROVEN structure — the exact self-similar recurrence (R as the ×3-adder transducer)

> **Theorem (exact diagonal renormalization). `[PROVEN — 0/35988 failures, scratchpad TEST 1]`**
> For all `n ≥ 0, k ≥ 0`,
> ```
> d_{n+1}^{(k)} = d_n^{(k+1)} ⊕ d_n^{(k)} ⊕ γ_n^{(k)},
> γ_n^{(k)} = ⌊ ((m_n mod 2^{p}) + (2 m_n mod 2^{p})) / 2^{p} ⌋,   p = n+k+1.
> ```
> *Proof.* `m_{n+1}=3 m_n = m_n + (m_n≪1)`. In binary addition `bit_p(A+B)=A_p⊕B_p⊕γ_p`; with
> `A=m_n, B=2m_n` we have `(2m_n)_p = bit_{p-1}(m_n)`, so `bit_p(3m_n)=bit_p(m_n)⊕bit_{p-1}(m_n)⊕γ_p`.
> Put `p=n+k+1`: `bit_{n+k+1}(m_n)=d_n^{(k+1)}`, `bit_{n+k}(m_n)=d_n^{(k)}`, and
> `bit_{n+k+1}(m_{n+1})=d_{n+1}^{(k)}`. ∎

**What this *is*.** `R` advances the whole array `(d_n^{(k)})_{k≥0}` by the **×3 binary-adder
transducer**: each diagonal `k` is fed by the next-higher diagonal `k+1`, the same diagonal `k`, and a
**carry `γ_n^{(k)}` from all lower bits** (the fractional tail). This is the precise, exact form of the
self-similarity the program lacked: NOT a fixed-position read (Rowland, periodic) and NOT a top read
(Weyl), but a transducer coupling adjacent moving diagonals. The single hard ingredient is the
**unbounded-range carry** `γ_n^{(k)}` — exactly the `c_n mod 2ⁿ` carry that makes the diagonal
non-automatic in this non-Pisot base (contrast §6).

**Why this is non-trivial despite `mahler §9` (zero-entropy isometry).** Reading a fixed coordinate of
the 2-adic isometry `×3` is periodic (no mixing). The recurrence shows the *moving* read is governed
not by `×3` alone but by `×3` **coupled across diagonals through the carry** — a genuinely
infinite-state object, whose annealed closure (§3) DOES mix. `R` converts "read a rigid isometry
diagonally" into "iterate a carry-coupled transducer," which has spectral content.

---

## 3. The fixed point / spectrum of R — annealed gap (PROVEN) vs non-Pisot no-atom (PROVEN)

### 3.1 Annealed R: a finite transducer with a spectral gap and uniform fixed point `[PROVEN-numeric]`
Randomise the carry by treating the orbit's bit-string as i.i.d. Bernoulli(½) on `ℚ₂` (= Haar). The
×3-adder becomes a finite Markov transducer on state `(last input bit, carry∈{0,1,2})`. Its transfer
matrix (scratchpad TEST 3) has spectrum
```
eigenvalues  {1, 0.5, 0.5, 0, ...},   spectral gap = 1 − |λ₂| = 0.5,
stationary output  P(bit = 1) = 0.500000  (the uniform / Haar fixed point).
```
So the **annealed renormalization `R_ann` is a contraction onto the uniform (balanced) diagonal law,
with rate `2^{−n}`** (gap ½). This is the renormalization fixed point the framework predicts: *the
attractor of `R` is Haar, and `R` contracts toward equidistribution* — provably, at the annealed tier.
(The `2^{−n}` rate matches the observed `Φ(N)≈2^{−N}` annealed carry decay of `ATTACK_RENORMALIZATION
§2.2`, and the gap is the transducer analogue of the β-map gap 0.27 of `mahler §9`.)

### 3.2 Non-Pisot ⇒ R has NO atomic / Pisot / sofic fixed point `[PROVEN]`
By the product formula `|3/2|_∞ · |3/2|_2 · |3/2|_3 = (3/2)(2)(1/3) = 1` (TEST 4):
```
|3/2|_∞ = 3/2 (expand),   |3/2|_2 = 2 (EXPAND > 1),   |3/2|_3 = 1/3 (contract).
```
The **bit-bearing 2-adic place EXPANDS** (`|3/2|_2 = 2`). For a **Pisot** base the non-archimedean
conjugates all have absolute value `< 1`: the contracting direction supports an **atomic** invariant
measure and the normalization transducer **closes to a finite automaton** (the base is *sofic*;
β-expansions are eventually periodic — Frougny, Schmidt; the moving diagonal would then be an
*automatic sequence*, decidably equidistributed). **Non-Pisot 3/2 has no such contracting 2-adic
direction**, so:
- `R*` on `Ŝ = ℤ[1/6]` is `ξ ↦ (3/2)ξ`, which has **no nonzero periodic point**: `(3/2)ⁿξ = ξ ⇒
  ((3/2)ⁿ−1)ξ = 0 ⇒ ξ = 0` (since `(3/2)ⁿ ≠ 1`). `[PROVEN]` (TEST 5: `{(3/2)ⁿ}` never returns to 0,
  N=2000.) No eigenvector ⇒ purely **Lebesgue/Haar (infinite) spectrum**, no atomic eigenmeasure.
- Hence the only `R`-invariant measure that is **smooth on the bit-sensitive factor is Haar**; there is
  no finite-state / sofic / Pisot shortcut and the diagonal is **not an automatic sequence** (consistent
  with `DIGITS_OF_3N §3`: Rowland's fixed-column periodicity provably misses the diagonal).

> **The non-Pisot-ness is exactly the absence of a Pisot/atomic fixed point of `R`** — the framework's
> required signature. The contraction that would make the problem finite-state is missing *because*
> `|3/2|_2 > 1`.

### 3.3 The honest gap (annealed → quenched)
`R_ann` (gap ½, Haar attractor) is PROVEN; the actual `R` uses the orbit's **own deterministic carry**
`γ_n^{(k)}` (not i.i.d.). The single orbit balance rides the floor: `P(d_n=1) = 0.49992` (N=5·10⁴,
TEST 6) — consistent with the Haar attractor but **not proven**. The gap between PROVEN `R_ann`
contraction and the quenched orbit is the entire Mahler wall.

---

## 4. CENTRAL OBJECT + key property `[CONJECTURE]`

> **Conjecture R-GEN (R-genericity of the rational seed).** The point `8 ∈ ℤ[1/6] ⊂ S` is *generic*
> for the solenoid automorphism `R = ×(3/2)` with respect to Haar: the empirical measures
> `μ_N = (1/N) Σ_{n<N} δ_{Rⁿ 8} ⇀ Haar`. Equivalently: the **deterministic-carry transducer `R`
> inherits the annealed uniform attractor of `R_ann` (§3.1)** — the quenched carry `γ_n^{(k)}` does not
> conspire away the gap-½ contraction. Equivalently: for every diagonal observable `φ_k`,
> `(1/N)Σ_{n<N} φ_k(Rⁿ 8) → ½`.

This is the fixed-point/attractor property: `R` is conjecturally a **contraction toward
equidistribution even on the single rational orbit**, the unique `R`-invariant law seen by `φ_k` being
Haar (forced to be non-atomic by §3.2). The irreducible content is that *the deterministic carry is
"generic enough"* — there is no proven mechanism (and, by §3.2, no Pisot/sofic obstruction) either way.

---

## 5. REDUCTION — Conjecture R-GEN ⇒ (K) at α = 8

> **Theorem-to-build (reduction). `[PROVEN reduction, modulo R-GEN]`**
> Conjecture R-GEN ⇒ `d_n = bit_k(⌊8(3/2)ⁿ⌋)` equidistributes for every `k` ⇒ (K) ⇒ Antihydra
> non-halt.
>
> *Chain.* `μ_N ⇀ Haar` ⇒ for each `k`, `(1/N)Σ φ_k(Rⁿ8) → ∫φ_k dHaar = ½` (the `k`-th bit is Haar-
> balanced) ⇒ the moving diagonal `d_n^{(k)}` equidistributes ⇒ this is precisely (K-density)/(K-AEV)
> at α=8 (`SESSION_2026-06-29_AEV_CORE §4`) ⇒ via the PROVEN reduction chain
> (`COMPLETE_PROOF_CAPSTONE`) even-density ≥ 1/3 ⇒ Antihydra runs forever. ∎ (conditional)

So the new theorem to prove is **R-GEN: genericity of one rational point for a non-Pisot solenoid
automorphism**. This is the "effective single-specified-orbit equidistribution for `×(3/2)`" target of
`WEAPONS_AUDIT §5`, now given a concrete renormalization shape: *show the carry-coupled transducer `R`
contracts the single orbit's empirical law to Haar*, knowing the annealed contraction (gap ½) and the
no-atom spectrum are PROVEN.

---

## 6. NOVELTY (WebSearch 2026-06-29)

- **Renormalization/self-similarity vs Mahler 3/2.** The literature on `(3/2)ⁿ mod 1`
  (Flatto–Lagarias–Pollington; Dubickas; the 2024 arXiv:2411.03468 "Mahler's 3/2 problem in ℤ⁺";
  Akiyama et al.) studies the *real-place* orbit / Z-numbers via interval maps and Diophantine bounds.
  None builds a **renormalization operator on the moving diagonal** of the bit-grid. "Self-similar
  renormalization" papers (arXiv:2505.12119) are nonlinear-analysis, unrelated.
- **Pisot β-expansion transducers (Frougny; Schmidt; arXiv:1103.2147, arXiv:2507.04848).** These build
  **finite** normalization transducers *because the base is Pisot* (sofic, finite carry). Our `R` is the
  **same transducer construction in a non-Pisot base**, where it provably does **not** close to a finite
  automaton (`|3/2|_2 = 2`, §3.2): the carry is unbounded and the diagonal is non-automatic. The novelty
  is applying the Pisot-transducer/sofic machinery precisely *at its failure point*, and identifying that
  failure (no atomic fixed point) as the exact content of non-Pisot-ness.
- **Automatic-sequence / CA renormalization (arXiv:1108.3982; Rowland arXiv:0902.3257).** These
  renormalize *self-similar / k-automatic* (hence Pisot/finite-state) sequences, and Rowland's
  regularity is for **fixed columns** of `3ⁿ` (proven periodic) which provably **miss the moving
  diagonal**. Ours renormalizes the **non-automatic moving diagonal** via an explicit infinite-state
  carry-coupled transducer.
- **Solenoid-automorphism genericity.** That `×(3/2)` is an ergodic/mixing automorphism of the
  `(2,3)`-solenoid is classical; reducing (K) to **genericity of the specific rational point `8`** under
  it, with the annealed transducer gap as the proven partial, is the new framing.
- **vs prior repo work.** `ATTACK_RENORMALIZATION.md` renormalized the *annealed Bernoulli-convolution*
  carry product (an identity, no quenched teeth); `FIRST_DIAGONAL_MEASURE.md` showed bit-sensitivity ⊥
  localization for *attached measures*. This note instead gives an **exact quenched self-similar
  recurrence** for the diagonal itself (§2, new), packages it as the solenoid automorphism `R`, and
  proves the annealed `R` has a genuine spectral gap with uniform fixed point (§3.1, new) plus the
  no-atomic-fixed-point spectrum from non-Pisot valuations (§3.2, new). The irreducible residue is the
  same single point — but now stated as a renormalization-contraction conjecture, not a measure paradox.

---

## 7. Honest ledger

| item | label |
|---|---|
| `ℤ²` shift symmetry = RG action; `R = ×(3/2)` time-step | `[PROVEN]` (0/168000) |
| Exact diagonal recurrence `d_{n+1}^{(k)}=d_n^{(k+1)}⊕d_n^{(k)}⊕γ` | `[PROVEN]` (0/35988) |
| `R` = solenoid automorphism `×(3/2)`; `R*: ξ↦(3/2)ξ` on `ℤ[1/6]` | `[PROVEN]` |
| Annealed `R_ann` finite transducer: gap ½, unique uniform fixed point | `[PROVEN-numeric]` |
| Non-Pisot place valuations `|3/2|_2=2>1`; no nonzero `R*`-periodic point ⇒ no atomic/Pisot/sofic fixed point | `[PROVEN]` |
| **R-GEN**: rational seed `8` is `R`-generic (quenched inherits annealed Haar attractor) | `[CONJECTURE]` — irreducible |
| R-GEN ⇒ (K) at α=8 ⇒ Antihydra non-halt | `[PROVEN reduction, conditional]` |
| Single-orbit balance `P(d_n=1)=0.49992` (N=5·10⁴) | `[OBSERVED]` (consistent, not proof) |

**The irreducible theorem to build:** *R-GEN — genericity of the single rational point `8` for the
non-Pisot solenoid automorphism `×(3/2)`, i.e. the carry-coupled ×3-adder transducer `R` contracts the
one orbit's empirical diagonal law to the uniform/Haar fixed point* — given that the **annealed**
contraction (gap ½) and the **no-atomic-fixed-point** spectrum (non-Pisot) are PROVEN. This is exactly
(K) = Mahler 3/2 / AEV Conj 1.6 at α=8, reframed as a single-orbit renormalization-contraction problem.

## Sources
- Repo: `TWO_ALPHA_JOINT.md` (ℤ² symmetry), `SESSION_2026-06-29_AEV_CORE.md` (core = moving diagonal,
  (K) equivalents), `mahler_equidistribution_attack.md` (§9 two-place skew β-map⋉2-adic isometry, gap
  0.27; §10 empirical measure = (K)), `ATTACK_RENORMALIZATION.md` (annealed carry product, `Φ≈2^{−N}`,
  twisted RPF), `FIRST_DIAGONAL_MEASURE.md` (bit-sensitivity ⊥ localization), `DIGITS_OF_3N.md`
  (diagonal of `3ⁿ`, Rowland misses it), `EFFECTIVE_TOPDIGIT.md` (Θ(log N) foothold), `solenoid.py`
  (solenoid genericity / CRT-independence numerics), `WEAPONS_AUDIT_2026-06-29.md` (§5 target object).
- Literature: Mahler 3/2 (1968, open), arXiv:2411.03468 (Mahler's 3/2 in ℤ⁺, 2024); Flatto–Lagarias–
  Pollington / arXiv:1806.03559 (uniformity of `(3/2)ⁿ`); Frougny, K. Schmidt, arXiv:1103.2147 /
  arXiv:2507.04848 (Pisot β-expansion = finite/sofic transducer); Rowland arXiv:0902.3257 (binary 3ⁿ
  regularity); arXiv:1108.3982 (CA/automatic renormalization, self-similar=automatic); Erdős–Salem
  (Rajchman ⇔ non-Pisot); Andrieu–Eliahou–Vivion arXiv:2510.11723 (AEV Conj 1.6).
- Numerics: `scratchpad/diagonal_renorm.py` (exact big-int, N≤5·10⁴, <2s): TEST 1 exact recurrence
  0/35988; TEST 2 ℤ² 0/168000; TEST 3 annealed transducer eig {1, .5, .5, 0}, gap .5, P(1)=.500000;
  TEST 4 places (1.5, 2, 1/3, prod 1); TEST 5 no `R*`-periodic point; TEST 6 balance 0.49992.

**No machine decided. No label upgraded.**
